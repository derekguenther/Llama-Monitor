#!/usr/bin/env python3
"""Aggregator module for llama-monitor."""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)



from db import Database
from electricity_cost import ElectricityCostCalculator
from idle_baseline import IdleBaselineTracker
from server_metrics import ServerMetricsCollector
from system_metrics import SystemMetricsCollector


class Aggregator:
    """Orchestrate all metrics collection and storage."""

    def __init__(
        self,
        server_url: str = "http://localhost:8000",
        db_path: str = "llama-monitor.db",
        idle_baseline_w: float = 40.0,
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

        # Latest collected metrics (populated by collect_all_metrics)
        self.last_metrics: Dict[str, Any] = {}

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

        # Idle baseline tracking. config=None so IdleBaselineTracker falls back
        # to the global get_config(); minimum_time_seconds is a sane hardcoded
        # default (this class is not config-driven).
        self.idle_tracker = IdleBaselineTracker(
            self.db,
            config=None,
            minimum_time_seconds=5,
        )

    def _safe_float(self, value, default=0.0):
        """Convert None or non-numeric values to default."""
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

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
        # The frontend expects nested keys (system.cpu.percent, system.gpu.usage),
        # so we keep both flat keys (for DB storage) and nested keys (for frontend).
        system = system_metrics
        cpu = system.get("cpu", {})
        gpu = system.get("gpu", {})
        memory = system.get("memory", {})

        # Calculate CPU percent: prioritize process CPU if available, otherwise use total OS CPU
        process_cpu = cpu.get("process_cpu", {})
        if process_cpu:
            # Average the summed per-process CPU percentages across logical cores.
            # Each process cpu_percent is a % of total system capacity, so summing
            # them can reach cpu_count*100% (e.g. 1200% on 12 cores). Divide by the
            # logical core count to normalize to 0-100%.
            cpu_count = self._safe_float(cpu.get("count"))
            raw_sum = sum(self._safe_float(p.get("cpu_percent")) for p in process_cpu.values())
            if cpu_count and cpu_count > 0:
                cpu_percent = raw_sum / cpu_count
            else:
                cpu_percent = raw_sum
            if cpu_percent > 100.0:
                # Clamping every collection cycle is a strong signal that this
                # normalization is incorrect, so log it loudly (no rate limiting).
                logger.warning(
                    "CPU usage clamped to 100%% (raw summed CPU=%.1f%% across %d cores); "
                    "repeated clamping may indicate the normalization is wrong",
                    raw_sum, int(cpu_count or 0),
                )
                cpu_percent = 100.0
        else:
            # Fall back to total OS CPU
            cpu_percent = self._safe_float(cpu.get("percent"))

        system_data = {
            # Flat keys for DB storage
            "cpu_percent": cpu_percent,
            "cpu_cores": cpu.get("cores", []),
            "cpu_count": cpu.get("count", 0),
            "cpu_power_w": self._safe_float(system.get("system", {}).get("cpu_power_w")),
            "gpu_usage": self._safe_float(gpu.get("usage")),
            "gpu_memory_used": self._safe_float(gpu.get("memory_used")),
            "gpu_memory_total": self._safe_float(gpu.get("memory_total")),
            "gpu_temperature_c": self._safe_float(gpu.get("temperature_c")),
            "gpu_fan_speed_rpm": self._safe_float(gpu.get("fan_speed_rpm")),
            "gpu_power_w": self._safe_float(gpu.get("power_w")),
            "memory_used": self._safe_float(memory.get("used")),
            "memory_total": self._safe_float(memory.get("total")),
            "memory_percent": self._safe_float(memory.get("percent")),
            "memory_available": self._safe_float(memory.get("available")),
            "system_power_w": self._safe_float(system.get("system", {}).get("system_power_w")),
            "timestamp": system.get("timestamp", int(time.time())),
            # Nested keys for frontend display (system.cpu.percent, system.gpu.usage, etc.)
            "cpu": {
                "percent": cpu_percent,
                "cores": cpu.get("cores", []),
                "count": cpu.get("count", 0),
                "power_w": self._safe_float(system.get("system", {}).get("cpu_power_w")),
            },
            "gpu": {
                "usage": self._safe_float(gpu.get("usage")),
                "memory_used": self._safe_float(gpu.get("memory_used")),
                "memory_total": self._safe_float(gpu.get("memory_total")),
                "temperature_c": self._safe_float(gpu.get("temperature_c")),
                "fan_speed_rpm": self._safe_float(gpu.get("fan_speed_rpm")),
                "power_w": self._safe_float(gpu.get("power_w")),
            },
            "memory": {
                "used": self._safe_float(memory.get("used")),
                "total": self._safe_float(memory.get("total")),
                "percent": self._safe_float(memory.get("percent")),
                "available": self._safe_float(memory.get("available")),
            },
        }

        # Include process GPU metrics if available
        process_gpu = system.get("process_gpu", {})

        # Build server data with slots nested inside (frontend expects data.server.slots)
        server_data_with_slots = {
            **server_data,
            "slots": server_metrics.get("slots", []),
            "props": server_metrics.get("props", {}),
        }

        result = {
            "timestamp": int(time.time()),
            "server": server_data_with_slots,
            "system": system_data,
            "process_gpu": process_gpu,
            "system_raw": system,  # Keep raw nested system data for store_raw_metrics
        }

        # Idle baseline tracking. Gate on meaningful power (>= 0 with at least
        # one component drawing power): the previous gate required gpu_usage > 0,
        # which rejects truly idle systems (GPU usage 0) and made auto-calibration
        # dead. cpu_percent is a local; gpu_usage, cpu_power_w, gpu_power_w are
        # keys in system_data.
        gpu_usage = system_data["gpu_usage"]
        cpu_power_w_sys = system_data["cpu_power_w"]
        gpu_power_w_sys = system_data["gpu_power_w"]
        if cpu_power_w_sys > 0 or gpu_power_w_sys > 0:
            self.idle_tracker.check_idle(
                cpu_percent, gpu_usage, gpu_power_w_sys, cpu_power_w_sys
            )

        # Cache latest metrics for web_server / api consumers
        self.last_metrics = result

        return result

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

        # Track token usage for cost comparison
        prompt_tokens = server.get("prompt_tokens_total", 0)
        generated_tokens = server.get("tokens_predicted_total", 0)
        self.cost_calculator.update_token_tracking(prompt_tokens, generated_tokens)

        # Store system metrics
        # Note: system data is flattened (cpu_percent, gpu_usage, etc.)
        # not nested (system["cpu"]["percent"], etc.)
        system = metrics.get("system", {})

        self.db.insert_system_metrics_raw(
            timestamp=timestamp,
            cpu_percent=system.get("cpu_percent", 0),
            cpu_cores_percent=str(system.get("cpu_cores", [])),
            cpu_power_w=system.get("cpu_power_w", 0),
            gpu_usage=system.get("gpu_usage", 0),
            gpu_memory_used_mb=system.get("gpu_memory_used", 0),
            gpu_memory_total_mb=system.get("gpu_memory_total", 0),
            gpu_temperature_c=system.get("gpu_temperature_c", 0),
            gpu_fan_speed_rpm=system.get("gpu_fan_speed_rpm", 0),
            gpu_power_w=system.get("gpu_power_w", 0),
            memory_used_mb=system.get("memory_used", 0),
            memory_total_mb=system.get("memory_total", 0),
            memory_percent=system.get("memory_percent", 0),
            system_power_w=system.get("system_power_w", 0),
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
        # Process CPU data comes from system_metrics.py as nested dict
        # In flattened system data, it's under system["cpu"]["process_cpu"]
        # But we need to get it from the raw metrics which preserves nesting
        raw_system = metrics.get("system_raw", {})
        if not raw_system:
            # If no raw system data, try to get from system_raw in the metrics
            # Otherwise use empty dict
            raw_system = {}

        process_cpu = raw_system.get("cpu", {}).get("process_cpu", {})
        cpu_power_total = raw_system.get("cpu", {}).get("cpu_power_w", 0)
        cpu_percent_total = raw_system.get("cpu", {}).get("percent", 0)

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

        # Get GPU and CPU power from flattened system data
        gpu_power_w = system.get("gpu_power_w", 0)
        cpu_power_w = system.get("cpu_power_w", 0)

        # Track real elapsed time since the last power reading so energy deltas
        # are accurate even if the polling interval drifts from 1s. First call
        # initializes _last_cost_time to now (duration ~ 0).
        now = time.time()
        if not hasattr(self, "_last_cost_time"):
            self._last_cost_time = now
        duration = now - self._last_cost_time
        self._last_cost_time = now

        # Compute hybrid-blame primitives: llama shares from per-process data,
        # per-component idle baselines from the tracker, llama_running flag.
        primitives = self._compute_blame_primitives(system, raw_system)

        # Update power readings to accumulate energy totals
        energy_stats = self.cost_calculator.update_power_readings(
            gpu_power_w=max(0, gpu_power_w),
            cpu_power_w=max(0, cpu_power_w),
            duration_seconds=duration,
            primitives=primitives,
        )

        # Build cost data from energy stats
        # Store per-interval deltas for historical accuracy, plus cumulative for display
        cost = {
            "gpu_power_w": max(0, gpu_power_w),
            "cpu_power_w": cpu_power_w or 0,
            "duration_seconds": duration,
            "duration_hours": duration / 3600.0,
            "gpu_wh": energy_stats["gpu_wh"],
            "cpu_wh": energy_stats["cpu_wh"],
            "total_wh": energy_stats["total_wh"],
            "delta_gpu_wh": energy_stats.get("delta_gpu_wh", 0),
            "delta_cpu_wh": energy_stats.get("delta_cpu_wh", 0),
            "delta_total_wh": energy_stats.get("delta_total_wh", 0),
            "cost_usd": energy_stats["total_wh"] / 1000.0 * self.cost_calculator.cost_rate,
            "today_wh": energy_stats["today_wh"],
            "today_gpu_wh": energy_stats["today_gpu_wh"],
            "today_cpu_wh": energy_stats["today_cpu_wh"],
            "total_cost": energy_stats["total_wh"] / 1000.0 * self.cost_calculator.cost_rate,
            # Blame primitives + per-interval blame watts
            "gpu_idle_w": primitives["gpu_idle_w"],
            "cpu_idle_w": primitives["cpu_idle_w"],
            "llama_share": primitives["llama_share"],
            "llama_gpu_share": primitives["llama_gpu_share"],
            "llama_cpu_share": primitives["llama_cpu_share"],
            "gpu_util": primitives["gpu_util"],
            "cpu_util": primitives["cpu_util"],
            "llama_running": primitives["llama_running"],
            "direct_w": energy_stats["direct_w"],
            "baseline_w": energy_stats["baseline_w"],
            "other_w": energy_stats["other_w"],
            "unattributed_w": energy_stats["unattributed_w"],
            "today_direct_wh": energy_stats.get("today_direct_wh", 0),
            "today_baseline_wh": energy_stats.get("today_baseline_wh", 0),
            "today_other_wh": energy_stats.get("today_other_wh", 0),
            "today_unattributed_wh": energy_stats.get("today_unattributed_wh", 0),
        }

        # Store system data as flattened structure for combined_metrics
        self.db.execute(
            """
            INSERT OR REPLACE INTO combined_metrics (timestamp, server_data, system_data, cost_data)
            VALUES (?, ?, ?, ?)
            """,
            (
                timestamp,
                json.dumps(server),
                json.dumps(system),
                json.dumps(cost),
            )
        )

        # Persist cumulative energy (session totals) for crash recovery. Use the
        # cost_calculator's session_start which is an ISO string; fall back to an
        # ISO timestamp (NOT int(time.time())) so we never write an integer into
        # the TEXT session_start column (recreating the int-vs-ISO bug).
        session_start = (
            self.cost_calculator.session_start
            or datetime.now().isoformat()
        )
        self.db.update_cumulative_energy(
            session_start=session_start,
            total_wh=self.cost_calculator.total_energy_wh,
            gpu_wh=self.cost_calculator.gpu_energy_wh,
            cpu_wh=self.cost_calculator.cpu_energy_wh,
            session_cost_usd=self.cost_calculator.calculate_cost(
                self.cost_calculator.total_energy_wh
            ),
            direct_wh=self.cost_calculator.total_direct_wh,
            baseline_wh=self.cost_calculator.total_baseline_wh,
            other_wh=self.cost_calculator.total_other_wh,
            unattributed_wh=self.cost_calculator.total_unattributed_wh,
        )

    def _compute_blame_primitives(
        self, system: Dict[str, Any], raw_system: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compute hybrid-blame primitives from per-process data and baselines.

        Args:
            system: Flattened system data (has cpu_count, gpu_usage, etc.)
            raw_system: Raw nested system data (has cpu.process_cpu,
                cpu.percent, gpu.usage, process_gpu).

        Returns:
            Dict with llama shares, per-component idle baselines, llama_running.
        """
        gpu_power_w = system.get("gpu_power_w", 0) or 0
        cpu_power_w = system.get("cpu_power_w", 0) or 0

        # llama GPU share: llama per-process GPU util / total GPU usage
        # process_gpu lives in the raw system dict, not the flattened system.
        proc_gpu = raw_system.get("process_gpu", {}) or {}
        llama_gpu_util = sum(
            p.get("gpu_utilization") or 0 for p in proc_gpu.values()
        )
        gpu_util = system.get("gpu_usage", 0) or 0
        llama_gpu_share = (
            min(llama_gpu_util / gpu_util, 1.0) if gpu_util > 0 else 0.0
        )

        # llama CPU share: normalized per-process CPU / raw OS CPU percent
        process_cpu = (raw_system.get("cpu", {}) or {}).get("process_cpu", {}) or {}
        llama_cpu_util = sum(
            p.get("cpu_percent") or 0 for p in process_cpu.values()
        )
        cpu_count = system.get("cpu_count", 0) or 0
        cpu_util_os = (raw_system.get("cpu", {}) or {}).get("percent", 0) or 0
        llama_cpu_util_norm = llama_cpu_util / cpu_count if cpu_count > 0 else 0.0
        llama_cpu_share = (
            min(llama_cpu_util_norm / cpu_util_os, 1.0) if cpu_util_os > 0 else 0.0
        )
        llama_share = max(llama_gpu_share, llama_cpu_share)

        # llama_running = union of process_cpu / process_gpu presence
        llama_running = bool(proc_gpu) or bool(process_cpu)

        # Per-component idle baselines from auto-calibrated tracker
        cpu_idle_w = 0.0
        gpu_idle_w = 0.0
        recent = self.idle_tracker.get_recent_baseline()
        if recent:
            cpu_idle_w = recent.get("cpu_idle_w", 0.0)
            gpu_idle_w = recent.get("gpu_idle_w", 0.0)

        # Fallback: seed from scalar idle_baseline_w, split proportionally to
        # measured CPU vs GPU power (50/50 if both zero).
        if cpu_idle_w + gpu_idle_w == 0.0:
            scalar = self.cost_calculator.idle_baseline_w
            total = cpu_power_w + gpu_power_w
            if total > 0:
                cpu_idle_w = scalar * cpu_power_w / total
                gpu_idle_w = scalar - cpu_idle_w
            else:
                cpu_idle_w = scalar / 2.0
                gpu_idle_w = scalar / 2.0

        return {
            "llama_share": llama_share,
            "llama_gpu_share": llama_gpu_share,
            "llama_cpu_share": llama_cpu_share,
            "gpu_util": gpu_util,
            "cpu_util": cpu_util_os,
            "gpu_idle_w": gpu_idle_w,
            "cpu_idle_w": cpu_idle_w,
            "llama_running": llama_running,
        }

    def compress_if_needed(self) -> None:
        """Compress data if needed based on time intervals.

        Compresses raw metrics into 1m buckets and 1m into 1h buckets, purging
        the source rows so the database does not grow without bound. After a
        purge, the database file is VACUUMed (throttled to hourly) so deleted
        pages are reclaimed and the file shrinks.
        """
        # Compress to 1-minute (also purges folded raw rows)
        self.db.compress_to_1m()

        # Compress to 1-hour (also purges folded 1m rows) and reclaim disk
        # space at most hourly, since VACUUM rebuilds the entire database file.
        self.db.compress_to_1h()
        self._vacuum_throttled()

    def _vacuum_throttled(self) -> None:
        """Run VACUUM to reclaim disk space, but no more than once per hour.

        VACUUM rebuilds the entire database file, so it is expensive to run on
        every aggregation cycle. Throttling it to hourly keeps the file from
        growing without bound while avoiding constant full-file rebuilds.
        """
        now = time.time()
        last = getattr(self, "_last_vacuum_time", 0)
        if now - last >= 3600:
            self.db.vacuum()
            self._last_vacuum_time = now

    def calculate_cost(self) -> Dict[str, Any]:
        """Calculate current session cost.

        Returns:
            Dictionary with cost information including today's energy stats.
        """
        session_stats = self.cost_calculator.get_session_stats()
        today_stats = self.cost_calculator.get_today_stats()

        # Merge session and today's stats, prioritizing today's stats
        result = session_stats if session_stats else {}
        if today_stats:
            result["today_wh"] = today_stats["total_wh"]
            result["today_gpu_wh"] = today_stats["gpu_wh"]
            result["today_cpu_wh"] = today_stats["cpu_wh"]
            result["today_cost"] = today_stats["total_cost_usd"]

        # Add cost rate (needed by frontend)
        result["cost_rate"] = self.cost_calculator.cost_rate

        # Add total_wh for session energy display
        if session_stats:
            result["total_wh"] = session_stats["total_wh"]
        else:
            # Fallback to cumulative energy from calculator
            result["total_wh"] = self.cost_calculator.total_energy_wh

        return result

    def calculate_today_cost(self) -> Dict[str, Any]:
        """Calculate today's energy cost (from midnight).

        Returns:
            Dictionary with today's cost information.
        """
        return self.cost_calculator.get_today_stats()

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
