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
        self._idle_power_samples: list = []
        self._is_idle: bool = False

    def check_idle(
        self, cpu_percent: float, gpu_percent: float, system_power_w: float
    ) -> Optional[float]:
        """Check if system is idle and track baseline.

        Args:
            cpu_percent: CPU utilization percentage.
            gpu_percent: GPU utilization percentage.
            system_power_w: Current system power in watts.

        Returns:
            Current average baseline if system just went idle, None otherwise.
        """
        # Determine if system is idle (both CPU and GPU < 5%)
        is_now_idle = (cpu_percent + gpu_percent) < 5.0

        # If just became idle, start timer
        if is_now_idle and not self._is_idle:
            self._idle_start = time.time()
            self._idle_power_samples = [system_power_w]
            self._is_idle = True
            return None

        # If already idle, accumulate samples
        if is_now_idle:
            elapsed = time.time() - self._idle_start
            self._idle_power_samples.append(system_power_w)

            # Only record baseline after minimum time has passed
            if elapsed >= self.minimum_time_seconds:
                # Calculate average baseline
                baseline = sum(self._idle_power_samples) / len(self._idle_power_samples)
                self._store_baseline(baseline)
                return baseline

            return None

        # If just became non-idle, reset
        if not is_now_idle and self._is_idle:
            self._idle_start = None
            self._idle_power_samples = []
            self._is_idle = False

        return None

    def _store_baseline(self, baseline_w: float) -> None:
        """Store baseline reading in database.

        Args:
            baseline_w: Average baseline power in watts.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO idle_baseline (timestamp, cpu_percent_avg, gpu_percent_avg, system_power_w, is_active)
            VALUES (?, ?, ?, ?, ?)
            """,
            (int(time.time()), 0.0, 0.0, baseline_w, 1),
        )
        self.db.commit()

    def get_baseline_average(self) -> Optional[float]:
        """Get the average of all stored baseline readings.

        Returns:
            Average baseline power in watts, or None if no readings.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT AVG(system_power_w) as avg_power
            FROM idle_baseline
            WHERE is_active = 1
            """
        )
        result = cursor.fetchone()
        if result and result[0] is not None:
            return float(result[0])
        return None

    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
        """Get average of most recent baseline readings.

        Args:
            count: Number of recent readings to average.

        Returns:
            Average of recent baseline readings, or None if not enough readings.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT AVG(system_power_w) as avg_power
            FROM (
                SELECT system_power_w
                FROM idle_baseline
                WHERE is_active = 1
                ORDER BY timestamp DESC
                LIMIT ?
            )
            """,
            (count,),
        )
        result = cursor.fetchone()
        if result and result[0] is not None:
            return float(result[0])
        return None

    def clear_baseline_data(self) -> None:
        """Clear all baseline data from the database."""
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM idle_baseline WHERE is_active = 1")
        self.db.commit()

    def reset(self) -> None:
        """Reset tracker state without clearing database."""
        self._idle_start = None
        self._idle_power_samples = []
        self._is_idle = False
