#!/usr/bin/env python3
"""Idle baseline tracker for llama-monitor."""

import time
from typing import Optional

from config import Config, get_config
from db import Database


class IdleBaselineTracker:
    """Track idle baseline power consumption."""

    def __init__(
        self,
        db: Database,
        config: Optional[Config] = None,
        minimum_time_seconds: Optional[float] = None,
    ):
        """Initialize the idle baseline tracker.

        Args:
            db: Database connection for storing baseline readings.
            config: Configuration instance. If None, uses global config.
            minimum_time_seconds: Minimum idle time before recording baseline.
                If None, uses config value (default 5 seconds).
        """
        self.db = db
        self.config = config or get_config()
        self.minimum_time_seconds = minimum_time_seconds or self.config.get(
            "idle_baseline.minimum_time_seconds", 5.0
        )

        # Idle state tracking
        self._idle_start: Optional[float] = None
        self._cpu_idle_samples: list = []
        self._gpu_idle_samples: list = []
        self._is_idle: bool = False

    def check_idle(
        self,
        cpu_percent: float,
        gpu_percent: float,
        gpu_power_w: float,
        cpu_power_w: float,
    ) -> Optional[dict]:
        """Check if system is idle and track per-component baselines.

        Args:
            cpu_percent: CPU utilization percentage.
            gpu_percent: GPU utilization percentage.
            gpu_power_w: Current GPU power in watts.
            cpu_power_w: Current CPU power in watts.

        Returns:
            Dict with 'cpu_idle_w' and 'gpu_idle_w' if system just went idle,
            None otherwise.
        """
        # Determine if system is idle (both CPU and GPU < 5%)
        is_now_idle = (cpu_percent + gpu_percent) < 5.0

        # If just became idle, start timer
        if is_now_idle and not self._is_idle:
            self._idle_start = time.time()
            self._cpu_idle_samples = [cpu_power_w]
            self._gpu_idle_samples = [gpu_power_w]
            self._is_idle = True
            return None

        # If already idle, accumulate samples
        if is_now_idle:
            elapsed = time.time() - self._idle_start
            self._cpu_idle_samples.append(cpu_power_w)
            self._gpu_idle_samples.append(gpu_power_w)

            # Only record baseline after minimum time has passed
            if elapsed >= self.minimum_time_seconds:
                # Calculate per-component average baselines
                cpu_idle_w = sum(self._cpu_idle_samples) / len(self._cpu_idle_samples)
                gpu_idle_w = sum(self._gpu_idle_samples) / len(self._gpu_idle_samples)
                self._store_baseline(cpu_idle_w, gpu_idle_w)
                return {"cpu_idle_w": cpu_idle_w, "gpu_idle_w": gpu_idle_w}

            return None

        # If just became non-idle, reset
        if not is_now_idle and self._is_idle:
            self._idle_start = None
            self._cpu_idle_samples = []
            self._gpu_idle_samples = []
            self._is_idle = False

        return None

    def _store_baseline(self, cpu_idle_w: float, gpu_idle_w: float) -> None:
        """Store baseline reading in database.

        Args:
            cpu_idle_w: Average CPU idle baseline power in watts.
            gpu_idle_w: Average GPU idle baseline power in watts.
        """
        system_power_w = cpu_idle_w + gpu_idle_w
        self.db.insert_idle_baseline(
            timestamp=str(int(time.time())),
            cpu_percent=0.0,
            gpu_percent=0.0,
            system_power_w=system_power_w,
            is_valid=True,
            cpu_idle_w=cpu_idle_w,
            gpu_idle_w=gpu_idle_w,
        )

    def get_baseline_average(self) -> Optional[dict]:
        """Get the average of all stored baseline readings.

        Returns:
            Dict with 'cpu_idle_w' and 'gpu_idle_w' averages, or None if no
            readings.
        """
        cursor = self.db.connect().cursor()
        cursor.execute(
            """
            SELECT AVG(cpu_idle_w) as avg_cpu, AVG(gpu_idle_w) as avg_gpu
            FROM idle_baseline
            WHERE is_valid = 1
            """
        )
        result = cursor.fetchone()
        if result and result[0] is not None:
            return {"cpu_idle_w": float(result[0]), "gpu_idle_w": float(result[1])}
        return None

    def get_recent_baseline(self, count: int = 10) -> Optional[dict]:
        """Get average of most recent baseline readings.

        Args:
            count: Number of recent readings to average.

        Returns:
            Dict with 'cpu_idle_w' and 'gpu_idle_w' averages, or None if not
            enough readings.
        """
        cursor = self.db.connect().cursor()
        cursor.execute(
            """
            SELECT AVG(cpu_idle_w) as avg_cpu, AVG(gpu_idle_w) as avg_gpu
            FROM (
                SELECT cpu_idle_w, gpu_idle_w
                FROM idle_baseline
                WHERE is_valid = 1
                ORDER BY timestamp DESC
                LIMIT ?
            )
            """,
            (count,),
        )
        result = cursor.fetchone()
        if result and result[0] is not None:
            return {"cpu_idle_w": float(result[0]), "gpu_idle_w": float(result[1])}
        return None

    def clear_baseline_data(self) -> None:
        """Clear all baseline data from the database."""
        cursor = self.db.connect().cursor()
        cursor.execute("DELETE FROM idle_baseline WHERE is_valid = 1")
        self.db.connect().commit()

    def reset(self) -> None:
        """Reset tracker state without clearing database."""
        self._idle_start = None
        self._cpu_idle_samples = []
        self._gpu_idle_samples = []
        self._is_idle = False
