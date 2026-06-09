#!/usr/bin/env python3
"""Aggregator module for llama-monitor."""

import time
from typing import Any, Dict, List, Optional

from db import Database
from electricity_cost import ElectricityCostCalculator
from server_metrics import ServerMetricsCollector
from system_metrics import SystemMetricsCollector


class Aggregator:
    """Orchestrate all metrics collection and storage."""

    def __init__(
        self,
        server_url: str = "http://localhost:8000",
        db_path: str = "llama-monitor.db",
        idle_baseline_w: float = 150.0,
        cost_rate: float = 0.12,
        collect_metrics: bool = True,
    ):
        """Initialize the aggregator.

        Args:
            server_url: URL of the llama.cpp server.
            db_path: Path to the SQLite database.
            idle_baseline_w: Idle power baseline in watts.
            cost_rate: Cost rate in USD per kWh.
            collect_metrics: Whether to collect /metrics data from server.
        """
        self.server_url = server_url
        self.db_path = db_path
        self.collect_metrics = collect_metrics

        # Initialize components
        self.db = Database(db_path)
        self.db.connect()

        # Set cost rate in database
        self.db.set_cost_rate(cost_rate)

        self.server_collector = ServerMetricsCollector(
            server_url, metrics_endpoint="/metrics", collect_metrics=collect_metrics
        )
        self.system_collector = SystemMetricsCollector()
        self.cost_calculator = ElectricityCostCalculator(self.db, idle_baseline_w)

    def collect_all_metrics(self) -> Dict[str, Any]:
        """Collect all metrics from all sources.

        Returns:
            Dictionary with all metrics (flattened for cache/web).
        """
        server_metrics = self.server_collector.collect()
        system_metrics = self.system_collector.collect()

        # Flatten server metrics for cache/web usage
        # server_metrics from collector has nested structure:
        # { "timestamp": "...", "server": {...}, "slots": [...], "props": {...} }
        # We want to extract just the actual server metrics
        server_data = server_metrics.get("server", {})

        # Flatten system metrics for cache/web usage
        # system_metrics from collector has nested structure:
        # { "timestamp": "...", "cpu": {...}, "gpu": {...}, "memory": {...}, ... }
        # The frontend expects flattened keys, so we extract the nested values
        system = system_metrics
        cpu = system.get("cpu", {})
        gpu = system.get("gpu", {})
        memory = system.get("memory", {})

        system_data = {
            "cpu_percent": cpu.get("percent", 0),
            "cpu_cores": cpu.get("cores", []),
            "cpu_count": cpu.get("count", 0),
            "cpu_power_w": cpu.get("cpu_power_w", 0),
            "gpu_usage": gpu.get("usage", 0),
            "gpu_memory_used": gpu.get("memory_used", 0),
            "gpu_memory_total": gpu.get("memory_total", 0),
            "gpu_temperature_c": gpu.get("temperature_c", 0),
            "gpu_fan_speed_rpm": gpu.get("fan_speed_rpm", 0),
            "gpu_power_w": gpu.get("power_w", 0),
            "memory_used": memory.get("used", 0),
            "memory_total": memory.get("total", 0),
            "memory_percent": memory.get("percent", 0),
            "memory_available": memory.get("available", 0),
            "system_power_w": system.get("system", {}).get("system_power_w", 0),
            "timestamp": system.get("timestamp", int(time.time())),
        }

        return {
            "timestamp": int(time.time()),
            "server": server_data,
            "system": system_data,
        }

    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
        """Store raw metrics in the database.

        Args:
            metrics: Metrics dictionary from collect_all_metrics().
        """
        timestamp = metrics.get("timestamp", int(time.time()))

        # Store server metrics
        server = metrics.get("server", {})
        self.db.insert_server_metrics_raw(
            timestamp=timestamp,
            prompt_tokens_total=server.get("prompt_tokens_total", 0),
            prompt_tokens_seconds=server.get("prompt_tokens_seconds", 0),
            tokens_predicted_total=server.get("tokens_predicted_total", 0),
            predicted_tokens_seconds=server.get("predicted_tokens_seconds", 0),
            requests_processing=server.get("requests_processing", 0),
            requests_deferred=server.get("requests_deferred", 0),
        )

        # Store system metrics
        system = metrics.get("system", {})
        cpu = system.get("cpu", {})
        gpu = system.get("gpu", {})
        memory = system.get("memory", {})
        system_power = system.get("system", {})

        self.db.insert_system_metrics_raw(
            timestamp=timestamp,
            cpu_percent=cpu.get("percent", 0),
            cpu_cores_percent=str(cpu.get("cores", [])),
            cpu_power_w=cpu.get("cpu_power_w", 0),
            gpu_usage=gpu.get("usage", 0),
            gpu_memory_used_mb=gpu.get("memory_used", 0),
            gpu_memory_total_mb=gpu.get("memory_total", 0),
            gpu_temperature_c=gpu.get("temperature_c", 0),
            gpu_fan_speed_rpm=gpu.get("fan_speed_rpm", 0),
            gpu_power_w=gpu.get("power_w", 0),
            memory_used_mb=memory.get("used", 0),
            memory_total_mb=memory.get("total", 0),
            memory_percent=memory.get("percent", 0),
            system_power_w=system_power.get("system_power_w", 0),
        )

        # Store process GPU metrics
        process_gpu = system.get("process_gpu", {})
        for process_name, data in process_gpu.items():
            self.db.insert_process_gpu_metrics_raw(
                timestamp=timestamp,
                process_name=process_name,
                pid=data.get("pid", 0),
                gpu_utilization=data.get("gpu_utilization", 0),
                gpu_memory_mb=data.get("gpu_memory_mb", 0),
            )

        # Store process CPU metrics with power allocation
        process_cpu = cpu.get("process_cpu", {})
        cpu_power_total = cpu.get("cpu_power_w", 0)
        cpu_percent_total = cpu.get("percent", 0)

        # Only calculate per-process power if total CPU percent > 0
        if cpu_percent_total > 0:
            for process_name, data in process_cpu.items():
                cpu_percent_process = data.get("cpu_percent", 0)
                pid = data.get("pid", 0)
                # Calculate proportional CPU power allocation
                cpu_power_process = cpu_power_total * (cpu_percent_process / cpu_percent_total)
                self.db.insert_process_cpu_metrics_raw(
                    timestamp=timestamp,
                    process_name=process_name,
                    pid=pid,
                    cpu_percent=cpu_percent_process,
                    cpu_power_w=cpu_power_process,
                )

        # Store combined metrics for web dashboard
        import json
        cost = self.cost_calculator.calculate_power_cost(
            gpu_power_w=gpu.get("power_w", 0) or 0,
            cpu_power_w=cpu.get("cpu_power_w", 0) or 0,
            duration_seconds=1.0
        )
        self.db.execute(
            """
            INSERT INTO combined_metrics (timestamp, server_data, system_data, cost_data)
            VALUES (?, ?, ?, ?)
            """,
            (
                timestamp,
                json.dumps(server),
                json.dumps({
                    "cpu": cpu,
                    "gpu": gpu,
                    "memory": memory,
                    "system": system_power,
                }),
                json.dumps(cost),
            )
        )

    def compress_if_needed(self) -> None:
        """Compress data if needed based on time intervals."""
        # Check if we should compress to 1-minute
        self.db.compress_to_1m()

        # Check if we should compress to 1-hour
        self.db.compress_to_1h()

    def calculate_cost(self) -> Dict[str, Any]:
        """Calculate current session cost.

        Returns:
            Dictionary with cost information.
        """
        return self.cost_calculator.get_session_stats()

    def close(self) -> None:
        """Clean up resources."""
        self.db.close()
        self.system_collector.close()

    def __enter__(self):
        """Context manager enter."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
