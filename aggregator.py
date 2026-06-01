"""Data aggregator for llama-monitor.

This module merges server and system metrics, stores to SQLite,
and handles data compression with configurable retention.
"""

import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from database import Database
from electricity_cost import ElectricityCostCalculator
from server_metrics import ServerMetricsCollector
from system_metrics import SystemMetricsCollector


class DataAggregator:
    """Aggregates server and system metrics, stores to SQLite."""

    def __init__(
        self,
        database: Database,
        server_url: str,
        tracked_processes: Optional[List[str]] = None,
        cost_rate: float = 0.12,
    ):
        """Initialize the aggregator.

        Args:
            database: Database instance
            server_url: URL of the llama.cpp server
            tracked_processes: List of process names to track
            cost_rate: Electricity cost in USD per kWh
        """
        self.database = database
        self.server_collector = ServerMetricsCollector(server_url)
        self.system_collector = SystemMetricsCollector(tracked_processes)
        self.cost_calculator = ElectricityCostCalculator(database, cost_rate)

        # Session tracking
        self.session_start = None
        self.last_poll_time = None

        # Metrics storage
        self.last_raw_server_metrics = None
        self.last_raw_system_metrics = None

    def start_session(self) -> None:
        """Start a new aggregation session."""
        self.session_start = datetime.now().isoformat()
        self.last_poll_time = time.time()
        self.cost_calculator.start_session()

    def stop_session(self) -> Dict[str, Any]:
        """Stop current session and return final stats."""
        return self.cost_calculator.stop_session()

    def poll(self) -> Dict[str, Any]:
        """Poll all metrics and store to database.

        Returns:
            Dictionary with collected metrics
        """
        current_time = time.time()

        # Calculate time since last poll
        if self.last_poll_time:
            poll_interval = current_time - self.last_poll_time
        else:
            poll_interval = 0

        self.last_poll_time = current_time

        # Collect server metrics
        server_data = self.server_collector.collect()
        self.last_raw_server_metrics = server_data

        # Collect system metrics
        system_data = self.system_collector.collect()
        self.last_raw_system_metrics = system_data

        # Calculate costs
        gpu_power = system_data.get("gpu", {}).get("power_w", 0)
        cpu_power = system_data.get("cpu", {}).get("power_w", 0)

        cost_data = self.cost_calculator.update_power_readings(
            gpu_power_w=gpu_power,
            cpu_power_w=cpu_power,
            duration_seconds=poll_interval,
        )

        # Store to database
        self._store_metrics(
            timestamp=server_data["timestamp"],
            server_data=server_data,
            system_data=system_data,
            cost_data=cost_data,
        )

        return {
            "timestamp": server_data["timestamp"],
            "server": server_data,
            "system": system_data,
            "cost": cost_data,
        }

    def _store_metrics(
        self,
        timestamp: str,
        server_data: Dict[str, Any],
        system_data: Dict[str, Any],
        cost_data: Dict[str, Any],
    ) -> None:
        """Store metrics to database.

        Args:
            timestamp: Measurement timestamp
            server_data: Server metrics
            system_data: System metrics
            cost_data: Cost data
        """
        cursor = self.database.conn.cursor()

        # Store server metrics
        server_metrics = server_data.get("server", {})
        self.database.insert_server_metrics(timestamp, server_metrics)

        # Store system metrics
        system_metrics = {
            "cpu_percent": system_data.get("cpu", {}).get("percent"),
            "cpu_cores_percent": system_data.get("cpu", {}).get("cores"),
            "cpu_temperature_c": None,  # Not collected yet
            "cpu_power_w": system_data.get("cpu", {}).get("power_w"),
            "gpu_usage": system_data.get("gpu", {}).get("usage"),
            "gpu_memory_used": system_data.get("gpu", {}).get("memory_used"),
            "gpu_memory_total": system_data.get("gpu", {}).get("memory_total"),
            "gpu_temperature_c": system_data.get("gpu", {}).get("temperature_c"),
            "gpu_fan_speed_rpm": system_data.get("gpu", {}).get("fan_speed_rpm"),
            "gpu_power_w": system_data.get("gpu", {}).get("power_w"),
            "memory_used": system_data.get("memory", {}).get("used"),
            "memory_total": system_data.get("memory", {}).get("total"),
            "memory_percent": system_data.get("memory", {}).get("percent"),
            "system_power_w": None,  # Not collected yet
        }
        self.database.insert_system_metrics(timestamp, system_metrics)

        # Store per-process GPU metrics
        process_gpu = system_data.get("process_gpu", {})
        for proc_name, proc_data in process_gpu.items():
            if proc_name != "error":
                self.database.insert_process_gpu_metrics(
                    timestamp=timestamp,
                    process_name=proc_name,
                    pid=proc_data.get("pid", 0),
                    gpu_utilization=proc_data.get("gpu_utilization", 0),
                    gpu_memory_mb=proc_data.get("gpu_memory_mb", 0),
                )

        # Store combined metrics
        combined_data = {
            "server": server_data,
            "system": system_data,
            "cost": cost_data,
        }

        cursor.execute(
            """
            INSERT OR REPLACE INTO combined_metrics
            (timestamp, server_data, system_data, cost_data)
            VALUES (?, ?, ?, ?)
            """,
            (
                timestamp,
                str(server_data),
                str(system_data),
                str(cost_data),
            ),
        )

        self.database.conn.commit()

    def get_recent_server_metrics(
        self, limit: int = 60
    ) -> List[Dict[str, Any]]:
        """Get recent server metrics.

        Args:
            limit: Maximum number of records

        Returns:
            List of recent server metric records
        """
        return self.database.get_server_metrics(limit=limit)

    def get_recent_system_metrics(
        self, limit: int = 60
    ) -> List[Dict[str, Any]]:
        """Get recent system metrics.

        Args:
            limit: Maximum number of records

        Returns:
            List of recent system metric records
        """
        return self.database.get_system_metrics(limit=limit)

    def get_combined_metrics(
        self, start_time: Optional[str] = None, end_time: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get combined metrics with cost.

        Args:
            start_time: Start timestamp (inclusive)
            end_time: End timestamp (inclusive)

        Returns:
            List of combined metric records
        """
        cursor = self.database.conn.cursor()
        query = """
            SELECT * FROM combined_metrics
            WHERE 1=1
        """
        params = []

        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time)
        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time)

        query += " ORDER BY timestamp DESC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
        """Get cumulative energy statistics.

        Returns:
            Dictionary with energy data or None
        """
        return self.database.get_cumulative_energy()

    def get_cost_rate(self) -> float:
        """Get the current cost rate.

        Returns:
            Cost rate in USD per kWh
        """
        return self.database.get_cost_rate()

    def set_cost_rate(self, rate: float) -> None:
        """Update the cost rate.

        Args:
            rate: New cost rate in USD per kWh
        """
        self.database.set_cost_rate(rate)
        self.cost_calculator.set_cost_rate(rate)


def format_metrics_display(aggregator: DataAggregator) -> str:
    """Format metrics for display.

    Args:
        aggregator: DataAggregator instance

    Returns:
        Formatted string for display
    """
    lines = []

    # Get recent metrics
    server_metrics = aggregator.get_recent_server_metrics(limit=1)
    system_metrics = aggregator.get_recent_system_metrics(limit=1)
    energy = aggregator.get_cumulative_energy()

    # Server status
    if server_metrics:
        m = server_metrics[0]
        prompt_tokens = m.get("prompt_tokens_total", 0)
        prompt_rate = m.get("prompt_tokens_seconds", 0)
        generated = m.get("tokens_predicted_total", 0)
        gen_rate = m.get("predicted_tokens_seconds", 0)

        lines.append(f"Prompt tokens:    {prompt_tokens:,} ({prompt_rate:,.0f}/s)")
        lines.append(f"Generated:        {generated:,} ({gen_rate:,.0f}/s)")

    # System status
    if system_metrics:
        m = system_metrics[0]
        cpu = m.get("cpu_percent", 0)
        gpu = m.get("gpu_usage", 0)
        mem = m.get("memory_percent", 0)
        gpu_mem = m.get("gpu_memory_used", 0)
        gpu_total = m.get("gpu_memory_total", 0)

        lines.append(f"CPU: {cpu:.1f}%    GPU: {gpu:.1f}%    Mem: {mem:.1f}%")
        if gpu_mem and gpu_total:
            lines.append(f"GPU Mem: {gpu_mem:,}MB / {gpu_total:,}MB")

    # Cost info
    if energy:
        total_wh = energy.get("total_wh", 0)
        cost = energy.get("session_cost_usd", 0)
        lines.append(f"Session cost:     ${cost:.4f} ({total_wh:.1f} Wh)")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test the aggregator
    db = Database(":memory:")
    with db:
        aggregator = DataAggregator(
            database=db,
            server_url="http://localhost:8000",
            tracked_processes=["llama-server.exe"],
            cost_rate=0.12,
        )

        print("Starting session...")
        aggregator.start_session()

        # Simulate a few polls
        for i in range(3):
            print(f"\nPoll {i+1}:")
            data = aggregator.poll()
            print(f"Timestamp: {data['timestamp']}")
            print(f"Cost this poll: ${data['cost']['total_cost_usd']:.6f}")

        # Get cumulative stats
        energy = aggregator.get_cumulative_energy()
        if energy:
            print(f"\nCumulative Energy:")
            print(f"  Total: {energy['total_wh']:.2f} Wh")
            print(f"  Cost:  ${energy['session_cost_usd']:.4f}")

        # Stop session
        final = aggregator.stop_session()
        print(f"\nFinal Session:")
        print(f"  Total: {final['total_wh']:.2f} Wh")
        print(f"  Cost:  ${final['total_cost_usd']:.4f}")
