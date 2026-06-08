"""Aggregator daemon for llama-monitor.

This module provides the background collector process that:
- Polls llama.cpp server API at configurable intervals
- Stores metrics in SQLite database
- Serves HTTP REST API for TUI and web server
- Handles automatic data compression

The daemon can run as a Windows service via NSSM or as a standalone process.
"""

import argparse
import json
import os
import signal
import sys
import threading
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

try:
    import socketio
    import eventlet
    eventlet.monkey_patch()
    SOCKETIO_AVAILABLE = True
except ImportError:
    SOCKETIO_AVAILABLE = False

# Local imports
from config import load_config, find_config
from db import Database
from server_metrics import ServerMetricsCollector
from system_metrics import SystemMetricsCollector
from electricity_cost import ElectricityCostCalculator


class Aggregator:
    """Main aggregator class that orchestrates metrics collection and storage."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the aggregator.

        Args:
            config_path: Path to config.yaml file. If None, searches default locations.
        """
        self.config_path = config_path or find_config()
        self.config = load_config(self.config_path)

        # Database
        self.db = Database(self.config.get("database.path", "llama-monitor.db"))

        # Collectors
        self.server_collector = ServerMetricsCollector(
            server_url=self.config.get("server.url", "http://localhost:8080"),
            metrics_endpoint=self.config.get("server.metrics_endpoint", "/metrics")
        )
        self.system_collector = SystemMetricsCollector(
            tracked_processes=self.config.get("metrics_collection.tracked_processes", ["llama.cpp"])
        )

        # Cost calculator
        self.cost_calculator = ElectricityCostCalculator(self.db)

        # State
        self.running = False
        self.collection_thread: Optional[threading.Thread] = None
        self.last_metrics: Dict[str, Any] = {}

        # Compression tracking
        self.last_compression_check = time.time()
        self.compression_interval = 300  # Check every 5 minutes

    def connect(self) -> None:
        """Open database connection."""
        self.db.connect()

    def close(self) -> None:
        """Close database connection and cleanup."""
        self.system_collector.close()
        self.db.close()

    def collect_all_metrics(self) -> Dict[str, Any]:
        """Collect all metrics from all sources.

        Returns:
            Dictionary with timestamped metrics from all sources
        """
        timestamp = datetime.now().isoformat()

        # Collect server metrics
        server_data = self.server_collector.collect()
        if server_data:
            server_metrics = self._extract_server_metrics(server_data)
        else:
            server_metrics = {}

        # Collect system metrics
        system_data = self.system_collector.collect()
        system_metrics = self._extract_system_metrics(system_data)

        # Collect per-process GPU metrics
        process_gpu_metrics = self._extract_process_gpu_metrics(system_data)

        # Calculate cost
        cost_data = self._calculate_cost(system_metrics)

        result = {
            "timestamp": timestamp,
            "server": server_metrics,
            "system": system_metrics,
            "process_gpu": process_gpu_metrics,
            "cost": cost_data,
        }

        self.last_metrics = result
        return result

    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract server metrics from collector data.

        Args:
            server_data: Raw server metrics data

        Returns:
            Extracted server metrics dictionary
        """
        server = server_data.get("server", {})
        return {
            "prompt_tokens_total": server.get("prompt_tokens_total"),
            "prompt_tokens_seconds": server.get("prompt_tokens_seconds"),
            "tokens_predicted_total": server.get("tokens_predicted_total"),
            "predicted_tokens_seconds": server.get("predicted_tokens_seconds"),
            "requests_processing": server.get("requests_processing"),
            "requests_deferred": server.get("requests_deferred"),
        }

    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract system metrics from collector data.

        Args:
            system_data: Raw system metrics data

        Returns:
            Extracted system metrics dictionary
        """
        cpu = system_data.get("cpu", {})
        gpu = system_data.get("gpu", {})
        memory = system_data.get("memory", {})
        system = system_data.get("system", {})

        return {
            "cpu_percent": cpu.get("percent"),
            "cpu_cores_percent": json.dumps(cpu.get("cores", [])),
            "cpu_temperature_c": json.dumps(cpu.get("temperature_c", [])),
            "cpu_power_w": cpu.get("power_w"),
            "gpu_usage": gpu.get("usage"),
            "gpu_memory_used": gpu.get("memory_used"),
            "gpu_memory_total": gpu.get("memory_total"),
            "gpu_temperature_c": gpu.get("temperature_c"),
            "gpu_fan_speed_rpm": gpu.get("fan_speed_rpm"),
            "gpu_power_w": gpu.get("power_w"),
            "memory_used": memory.get("used"),
            "memory_total": memory.get("total"),
            "memory_percent": memory.get("percent"),
            "system_power_w": system.get("power_w"),
        }

    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract per-process GPU metrics.

        Args:
            system_data: Raw system metrics data

        Returns:
            Dictionary mapping process names to GPU metrics
        """
        return system_data.get("process_gpu", {})

    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate electricity cost from system metrics.

        Args:
            system_metrics: Current system metrics

        Returns:
            Cost calculation results
        """
        gpu_power = system_metrics.get("gpu_power_w", 0) or 0
        cpu_power = system_metrics.get("cpu_power_w", 0) or 0

        # Use a fixed duration for each calculation (1 second since we poll frequently)
        duration = 1.0

        return self.cost_calculator.calculate_power_cost(
            gpu_power_w=gpu_power,
            cpu_power_w=cpu_power,
            duration_seconds=duration
        )

    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
        """Store raw metrics in database.

        Args:
            metrics: Dictionary of metrics to store
        """
        cursor = self.db.conn.cursor()

        # Store server metrics
        server = metrics.get("server", {})
        self.db.insert_server_metrics(
            timestamp=metrics["timestamp"],
            metrics=server,
            table="server_metrics_raw"
        )

        # Store system metrics
        system = metrics.get("system", {})
        self.db.insert_system_metrics(
            timestamp=metrics["timestamp"],
            metrics=system,
            table="system_metrics_raw"
        )

        # Store per-process GPU metrics
        process_gpu = metrics.get("process_gpu", {})
        for process_name, data in process_gpu.items():
            self.db.insert_process_gpu_metrics(
                timestamp=metrics["timestamp"],
                process_name=process_name,
                pid=data.get("pid", 0),
                gpu_utilization=data.get("gpu_utilization", 0),
                gpu_memory_mb=data.get("gpu_memory_mb", 0),
                table="process_gpu_metrics_raw"
            )

        # Store cost data
        cost = metrics.get("cost", {})
        combined_data = {
            "server": metrics.get("server", {}),
            "system": metrics.get("system", {}),
            "cost": cost,
        }

        cursor.execute(
            """
            INSERT INTO combined_metrics (timestamp, server_data, system_data, cost_data)
            VALUES (?, ?, ?, ?)
            """,
            (
                metrics["timestamp"],
                json.dumps(metrics.get("server", {})),
                json.dumps(metrics.get("system", {})),
                json.dumps(cost),
            )
        )

        # Update cumulative energy
        self.db.update_cumulative_energy(
            session_start=self.cost_calculator.session_start or datetime.now().isoformat(),
            total_wh=self.cost_calculator.total_energy_wh,
            gpu_wh=self.cost_calculator.gpu_energy_wh,
            cpu_wh=self.cost_calculator.cpu_energy_wh,
            session_cost_usd=self.cost_calculator.calculate_cost(self.cost_calculator.total_energy_wh),
        )

        self.db.conn.commit()

    def check_compression(self) -> None:
        """Check if data compression is needed based on retention rules."""
        current_time = time.time()
        if current_time - self.last_compression_check < self.compression_interval:
            return

        self.last_compression_check = current_time

        # Check if compression is enabled
        if not self.config.get("compression.enabled", True):
            return

        # Check for 1-minute compression (raw data older than 1 week)
        self._compress_to_minute()

        # Check for 1-hour compression (1-minute data older than 1 month)
        self._compress_to_hour()

    def _compress_to_minute(self) -> None:
        """Compress raw data to 1-minute buckets."""
        # Get the cutoff time (1 week ago)
        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            SELECT datetime('now', '-7 days')
            """
        )
        cutoff = cursor.fetchone()[0]

        # Get distinct minute buckets
        cursor.execute(
            """
            SELECT DISTINCT substr(timestamp, 1, 16) as minute_bucket
            FROM server_metrics_raw
            WHERE timestamp < ?
            ORDER BY minute_bucket
            """,
            (cutoff,)
        )

        buckets = cursor.fetchall()
        if not buckets:
            return

        for (bucket,) in buckets:
            # Get min/max timestamp for this bucket
            cursor.execute(
                """
                SELECT MIN(timestamp), MAX(timestamp)
                FROM server_metrics_raw
                WHERE substr(timestamp, 1, 16) = ?
                """,
                (bucket,)
            )
            min_ts, max_ts = cursor.fetchone()

            # Aggregate server metrics
            cursor.execute(
                """
                INSERT OR REPLACE INTO server_metrics_1m (
                    timestamp, prompt_tokens_total, prompt_tokens_seconds,
                    tokens_predicted_total, predicted_tokens_seconds,
                    requests_processing, requests_deferred
                )
                SELECT
                    ?,
                    AVG(prompt_tokens_total),
                    AVG(prompt_tokens_seconds),
                    AVG(tokens_predicted_total),
                    AVG(predicted_tokens_seconds),
                    AVG(requests_processing),
                    AVG(requests_deferred)
                FROM server_metrics_raw
                WHERE substr(timestamp, 1, 16) = ?
                """,
                (bucket + ":00", bucket)
            )

            # Aggregate system metrics
            cursor.execute(
                """
                INSERT OR REPLACE INTO system_metrics_1m (
                    timestamp, cpu_percent, cpu_temperature_c, cpu_power_w,
                    gpu_usage, gpu_memory_used, gpu_temperature_c,
                    gpu_fan_speed_rpm, gpu_power_w, memory_percent, system_power_w
                )
                SELECT
                    ?,
                    AVG(cpu_percent),
                    AVG(cpu_temperature_c),
                    AVG(cpu_power_w),
                    AVG(gpu_usage),
                    AVG(gpu_memory_used),
                    AVG(gpu_temperature_c),
                    AVG(gpu_fan_speed_rpm),
                    AVG(gpu_power_w),
                    AVG(memory_percent),
                    AVG(system_power_w)
                FROM system_metrics_raw
                WHERE substr(timestamp, 1, 16) = ?
                """,
                (bucket + ":00", bucket)
            )

            # Delete raw data for this bucket
            cursor.execute(
                "DELETE FROM server_metrics_raw WHERE substr(timestamp, 1, 16) = ?",
                (bucket,)
            )
            cursor.execute(
                "DELETE FROM system_metrics_raw WHERE substr(timestamp, 1, 16) = ?",
                (bucket,)
            )

        self.db.conn.commit()

    def _compress_to_hour(self) -> None:
        """Compress 1-minute data to 1-hour buckets."""
        cursor = self.db.conn.cursor()

        # Get the cutoff time (1 month ago)
        cursor.execute(
            """
            SELECT datetime('now', '-1 month')
            """
        )
        cutoff = cursor.fetchone()[0]

        # Get distinct hour buckets
        cursor.execute(
            """
            SELECT DISTINCT substr(timestamp, 1, 13) as hour_bucket
            FROM server_metrics_1m
            WHERE timestamp < ?
            ORDER BY hour_bucket
            """,
            (cutoff,)
        )

        buckets = cursor.fetchall()
        if not buckets:
            return

        for (bucket,) in buckets:
            # Aggregate server metrics
            cursor.execute(
                """
                INSERT OR REPLACE INTO server_metrics_1h (
                    timestamp, prompt_tokens_total, prompt_tokens_seconds,
                    tokens_predicted_total, predicted_tokens_seconds,
                    requests_processing, requests_deferred
                )
                SELECT
                    ?,
                    AVG(prompt_tokens_total),
                    AVG(prompt_tokens_seconds),
                    AVG(tokens_predicted_total),
                    AVG(predicted_tokens_seconds),
                    AVG(requests_processing),
                    AVG(requests_deferred)
                FROM server_metrics_1m
                WHERE substr(timestamp, 1, 13) = ?
                """,
                (bucket + ":00:00", bucket)
            )

            # Aggregate system metrics
            cursor.execute(
                """
                INSERT OR REPLACE INTO system_metrics_1h (
                    timestamp, cpu_percent, cpu_temperature_c, cpu_power_w,
                    gpu_usage, gpu_memory_used, gpu_temperature_c,
                    gpu_fan_speed_rpm, gpu_power_w, memory_percent, system_power_w
                )
                SELECT
                    ?,
                    AVG(cpu_percent),
                    AVG(cpu_temperature_c),
                    AVG(cpu_power_w),
                    AVG(gpu_usage),
                    AVG(gpu_memory_used),
                    AVG(gpu_temperature_c),
                    AVG(gpu_fan_speed_rpm),
                    AVG(gpu_power_w),
                    AVG(memory_percent),
                    AVG(system_power_w)
                FROM system_metrics_1m
                WHERE substr(timestamp, 1, 13) = ?
                """,
                (bucket + ":00:00", bucket)
            )

            # Delete 1-minute data for this bucket
            cursor.execute(
                "DELETE FROM server_metrics_1m WHERE substr(timestamp, 1, 13) = ?",
                (bucket,)
            )
            cursor.execute(
                "DELETE FROM system_metrics_1m WHERE substr(timestamp, 1, 13) = ?",
                (bucket,)
            )

        self.db.conn.commit()

    def start(self) -> None:
        """Start the aggregation loop."""
        self.running = True
        self.cost_calculator.start_session()

        polling_interval = self.config.get("metrics_collection.interval_seconds", 1.0)

        def collection_loop():
            while self.running:
                try:
                    # Collect all metrics
                    metrics = self.collect_all_metrics()

                    # Store raw metrics
                    self.store_raw_metrics(metrics)

                    # Check compression
                    self.check_compression()

                except Exception as e:
                    print(f"Error in collection loop: {e}", file=sys.stderr)

                # Wait for next interval
                time.sleep(polling_interval)

        self.collection_thread = threading.Thread(target=collection_loop, daemon=True)
        self.collection_thread.start()

    def stop(self) -> None:
        """Stop the aggregation loop and cleanup."""
        self.running = False
        self.cost_calculator.stop_session()
        if self.collection_thread:
            self.collection_thread.join(timeout=5)
        self.close()


class MetricsHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the aggregator API."""

    aggregator: Optional[Aggregator] = None

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def send_json_response(self, data: Any, status: int = 200) -> None:
        """Send JSON response.

        Args:
            data: Data to serialize as JSON
            status: HTTP status code
        """
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self) -> None:
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/metrics/latest":
            self._handle_latest_metrics()
        elif path == "/api/metrics/range":
            self._handle_range_metrics(query)
        elif path == "/api/metrics/list":
            self._handle_metrics_list()
        elif path == "/api/status":
            self._handle_status()
        elif path == "/api/shutdown":
            self._handle_shutdown()
        elif path == "/api/restart":
            self._handle_restart()
        else:
            self.send_error(404, "Not found")

    def _handle_latest_metrics(self) -> None:
        """Handle /api/metrics/latest endpoint."""
        if not self.aggregator:
            self.send_error(503, "Aggregator not initialized")
            return

        # Get latest from database
        cursor = self.aggregator.db.conn.cursor()
        cursor.execute(
            """
            SELECT timestamp, server_data, system_data, cost_data
            FROM combined_metrics
            ORDER BY timestamp DESC
            LIMIT 1
            """
        )
        row = cursor.fetchone()

        if row:
            self.send_json_response({
                "timestamp": row["timestamp"],
                "server": json.loads(row["server_data"]),
                "system": json.loads(row["system_data"]),
                "cost": json.loads(row["cost_data"]),
            })
        else:
            # Return last collected metrics if available
            if self.aggregator.last_metrics:
                self.send_json_response(self.aggregator.last_metrics)
            else:
                self.send_json_response({"error": "No metrics available"})

    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:
        """Handle /api/metrics/range endpoint."""
        if not self.aggregator:
            self.send_error(503, "Aggregator not initialized")
            return

        start_time = query.get("start", [None])[0]
        end_time = query.get("end", [None])[0]
        table = query.get("table", ["combined_metrics"])[0]
        limit = query.get("limit", ["100"])[0]

        try:
            limit = int(limit)
        except ValueError:
            limit = 100

        cursor = self.aggregator.db.conn.cursor()

        # Build query
        query_str = f"SELECT * FROM {table} WHERE 1=1"
        params = []

        if start_time:
            query_str += " AND timestamp >= ?"
            params.append(start_time)
        if end_time:
            query_str += " AND timestamp <= ?"
            params.append(end_time)

        query_str += " ORDER BY timestamp DESC LIMIT ?"

        cursor.execute(query_str, params + [limit])
        rows = cursor.fetchall()

        results = []
        for row in rows:
            result = dict(row)
            # Parse JSON fields
            for field in ["server_data", "system_data", "cost_data"]:
                if field in result and result[field]:
                    try:
                        result[field] = json.loads(result[field])
                    except json.JSONDecodeError:
                        pass
            results.append(result)

        self.send_json_response({
            "start": start_time,
            "end": end_time,
            "limit": limit,
            "count": len(results),
            "data": results,
        })

    def _handle_metrics_list(self) -> None:
        """Handle /api/metrics/list endpoint."""
        if not self.aggregator:
            self.send_error(503, "Aggregator not initialized")
            return

        cursor = self.aggregator.db.conn.cursor()

        # Get available tables
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name LIKE 'metrics_%'
            """
        )
        tables = [row[0] for row in cursor.fetchall()]

        # Get columns for each table
        metrics_info = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            metrics_info[table] = columns

        self.send_json_response({
            "tables": tables,
            "metrics": metrics_info,
        })

    def _handle_status(self) -> None:
        """Handle /api/status endpoint."""
        if not self.aggregator:
            self.send_json_response({
                "status": "stopped",
                "error": "Aggregator not initialized",
            })
            return

        cursor = self.aggregator.db.conn.cursor()

        # Get row counts
        cursor.execute("SELECT COUNT(*) FROM server_metrics_raw")
        server_raw_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM system_metrics_raw")
        system_raw_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM combined_metrics")
        combined_count = cursor.fetchone()[0]

        # Get last timestamp
        cursor.execute(
            """
            SELECT timestamp FROM combined_metrics
            ORDER BY timestamp DESC LIMIT 1
            """
        )
        last_timestamp = cursor.fetchone()[0] if cursor.fetchone() else None

        self.send_json_response({
            "status": "running" if self.aggregator.running else "stopped",
            "polling_interval": self.aggregator.config.polling_interval,
            "server_url": self.aggregator.config.server_url,
            "last_metrics": self.aggregator.last_metrics.get("timestamp") if self.aggregator.last_metrics else None,
            "last_timestamp": last_timestamp,
            "metrics_counts": {
                "server_raw": server_raw_count,
                "system_raw": system_raw_count,
                "combined": combined_count,
            },
        })

    def _handle_shutdown(self) -> None:
        """Handle /api/shutdown endpoint."""
        if not self.aggregator:
            self.send_error(503, "Aggregator not initialized")
            return

        self.send_json_response({"status": "shutting_down"})

        def do_shutdown():
            time.sleep(0.5)
            self.aggregator.stop()
            # Exit the process
            os._exit(0)

        threading.Thread(target=do_shutdown, daemon=True).start()

    def _handle_restart(self) -> None:
        """Handle /api/restart endpoint."""
        if not self.aggregator:
            self.send_error(503, "Aggregator not initialized")
            return

        self.send_json_response({"status": "restarting"})

        def do_restart():
            time.sleep(0.5)
            self.aggregator.stop()
            time.sleep(1)
            # Reinitialize and restart
            self.aggregator = Aggregator()
            self.aggregator.connect()
            self.aggregator.start()

        threading.Thread(target=do_restart, daemon=True).start()


class WebSocketHandler:
    """WebSocket handler for real-time client updates."""

    def __init__(self, aggregator: Aggregator):
        """Initialize WebSocket handler.

        Args:
            aggregator: Aggregator instance
        """
        self.aggregator = aggregator
        self.clients: List[Any] = []
        self.socketio = None

    def start(self) -> None:
        """Start WebSocket server."""
        if not SOCKETIO_AVAILABLE:
            print("Warning: flask-socketio not available, WebSocket support disabled")
            return

        # Create SocketIO app
        self.socketio = socketio.Server(async_mode="eventlet")
        self.app = socketio.Middleware(self.socketio)

        @self.socketio.on("connect")
        def handle_connect(sid):
            self.clients.append(sid)
            print(f"Client connected: {sid}")

        @self.socketio.on("disconnect")
        def handle_disconnect(sid):
            if sid in self.clients:
                self.clients.remove(sid)
            print(f"Client disconnected: {sid}")

    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:
        """Broadcast metrics to all connected clients.

        Args:
            metrics: Metrics data to broadcast
        """
        if not self.socketio or not self.clients:
            return

        try:
            self.socketio.emit("metrics_update", metrics, room=None)
        except Exception as e:
            print(f"Error broadcasting metrics: {e}")


def create_app(aggregator: Aggregator) -> HTTPServer:
    """Create the HTTP server application.

    Args:
        aggregator: Aggregator instance

    Returns:
        Configured HTTPServer instance
    """
    MetricsHandler.aggregator = aggregator
    server = HTTPServer(("0.0.0.0", aggregator.config.get("web.http_port", 8080)), MetricsHandler)
    return server


def main() -> int:
    """Main entry point for the aggregator daemon."""
    parser = argparse.ArgumentParser(description="llama-monitor aggregator daemon")
    parser.add_argument(
        "--config",
        "-c",
        help="Path to config.yaml file",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        help="HTTP port (overrides config)",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run as daemon (background process)",
    )
    parser.add_argument(
        "--foreground",
        action="store_true",
        help="Run in foreground (default)",
    )

    args = parser.parse_args()

    # Initialize aggregator
    aggregator = Aggregator(config_path=args.config)
    aggregator.connect()

    # Override port if specified
    if args.port:
        aggregator.config.set("web.http_port", args.port)

    # Start aggregator collection
    aggregator.start()

    port = aggregator.config.get("web.http_port", 8080)
    print(f"Aggregator started on port {port}")
    print("Press Ctrl+C to stop")

    # Create and run HTTP server
    server = create_app(aggregator)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        aggregator.stop()
        server.shutdown()

    return 0


if __name__ == "__main__":
    sys.exit(main())
