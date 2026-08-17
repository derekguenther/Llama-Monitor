#!/usr/bin/env python3
"""Tests for the database compression purge fix (bead djxu).

Previously compress_to_1m / compress_to_1h only INSERTed aggregated rows into
the 1m/1h tables but NEVER deleted the source rows from the _raw / _1m tables,
so llama-monitor.db grew without bound (777MB). The fix:
  - compress_to_1m purges the folded raw rows
  - compress_to_1h purges the folded 1m rows
  - Aggregator.compress_if_needed runs a throttled VACUUM (hourly) to reclaim
    disk space
"""

import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import Database


def _system_metrics(ts, cpu_percent=50.0, cpu_power_w=65.0, gpu_power_w=220.0,
                    system_power_w=285.0):
    return {
        "timestamp": str(ts),
        "cpu_percent": cpu_percent,
        "cpu_cores_percent": "[10.0, 20.0, 30.0, 40.0]",
        "cpu_temperature_c": "45.0,46.0,47.0,48.0",
        "cpu_power_w": cpu_power_w,
        "gpu_usage": 85.0,
        "gpu_memory_used_mb": 8192,
        "gpu_memory_total_mb": 16384,
        "gpu_temperature_c": 75.0,
        "gpu_fan_speed_rpm": 2500,
        "gpu_power_w": gpu_power_w,
        "memory_used_mb": 16384,
        "memory_total_mb": 32768,
        "memory_percent": 50.0,
        "system_power_w": system_power_w,
    }


def _server_metrics(ts):
    return {
        "timestamp": str(ts),
        "prompt_tokens_total": 100,
        "prompt_tokens_seconds": 2.0,
        "tokens_predicted_total": 500,
        "predicted_tokens_seconds": 10.0,
        "requests_processing": 1,
        "requests_deferred": 0,
        "slots_active": 1,
        "slots_processing": 1,
    }


class TestCompressionPurge(unittest.TestCase):
    """Verify compression purges source rows so the DB does not grow unbounded."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db = Database(self.temp_db.name)
        self.db.connect()

    def tearDown(self):
        self.db.close()
        try:
            os.unlink(self.temp_db.name)
        except (PermissionError, OSError):
            pass

    def _insert_system_raw(self, count=3, start_offset_s=120):
        """Insert `count` raw system metrics across ~2 minutes ago."""
        now = int(time.time())
        base_time = (now // 60) * 60 - start_offset_s
        for i in range(count):
            ts = base_time + i * 30
            self.db.insert_system_metrics(
                str(ts), _system_metrics(ts), table="system_metrics_raw"
            )

    def _insert_server_raw(self, count=3, start_offset_s=120):
        now = int(time.time())
        base_time = (now // 60) * 60 - start_offset_s
        for i in range(count):
            ts = base_time + i * 30
            self.db.insert_server_metrics_raw(
                ts, **{k: v for k, v in _server_metrics(ts).items() if k != "timestamp"}
            )

    def test_compress_to_1m_purges_raw_rows(self):
        """After folding into 1m buckets, the source raw rows are deleted."""
        self._insert_system_raw()
        self._insert_server_raw()
        for table in ("system_metrics_raw", "server_metrics_raw"):
            self.assertGreater(self.db.get_table_size(table), 0,
                               f"{table} should have raw rows before compress")

        compressed = self.db.compress_to_1m()
        self.assertGreater(compressed, 0, "compression should fold raw rows")

        # Raw tables should now be purged
        for table in ("system_metrics_raw", "server_metrics_raw",
                      "process_gpu_metrics_raw", "process_cpu_metrics_raw"):
            self.assertEqual(self.db.get_table_size(table), 0,
                             f"{table} should be empty after 1m compression")

        # 1m tables should have aggregated data
        self.assertGreater(self.db.get_table_size("system_metrics_1m"), 0)
        self.assertGreater(self.db.get_table_size("server_metrics_1m"), 0)

    def test_compress_to_1h_purges_1m_rows(self):
        """After folding 1m into 1h buckets, the source 1m rows are deleted."""
        self._insert_system_raw()
        self.db.compress_to_1m()
        # Verify 1m rows exist before 1h compression
        self.assertGreater(self.db.get_table_size("system_metrics_1m"), 0)

        # Insert 1m rows manually spanning an earlier hour so 1h compression runs
        # (the default current-hour guard prevents folding the just-inserted rows).
        # Use a timestamp more than an hour ago.
        now = int(time.time())
        hour_bucket = (now // 3600) * 3600 - 7200  # 2 hours ago
        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            INSERT INTO system_metrics_1m (
                bucket_start, bucket_end, cpu_percent_avg
            ) VALUES (?, ?, ?)
            """,
            (hour_bucket, hour_bucket + 60, 50.0),
        )
        self.db.conn.commit()
        self.assertGreater(self.db.get_table_size("system_metrics_1m"), 0)

        compressed = self.db.compress_to_1h()
        self.assertGreater(compressed, 0, "1h compression should fold 1m rows")

        # The 1m rows in the compressed window should be purged
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) as c FROM system_metrics_1m WHERE bucket_start >= ? AND bucket_start < ?",
            ((now // 3600) * 3600 - 7200, (now // 3600) * 3600),
        )
        row = cursor.fetchone()
        self.assertEqual(row["c"], 0,
                         "1m rows in the compressed hour window should be purged")

        # 1h table should have aggregated data
        self.assertGreater(self.db.get_table_size("system_metrics_1h"), 0)

    def test_repeated_compression_does_not_reaccumulate(self):
        """Running compress_to_1m twice should not purge un-aggregated data or fail."""
        self._insert_system_raw()
        self.db.compress_to_1m()
        # Second call: nothing new to compress, raw already empty
        compressed = self.db.compress_to_1m()
        self.assertEqual(compressed, 0, "no new data to compress on second call")
        self.assertEqual(self.db.get_table_size("system_metrics_raw"), 0)

    def test_compress_if_needed_vacuum_throttled(self):
        """compress_if_needed runs a throttled VACUUM (max hourly) after purging."""
        from unittest.mock import patch
        from aggregator import Aggregator

        agg = Aggregator(
            server_url="http://localhost:8000",
            db_path=self.temp_db.name,
            idle_baseline_w=40.0,
            cost_rate=0.12,
            collect_metrics=False,
        )

        # First call: vacuum should run (no prior vacuum time)
        with patch.object(agg.db, "vacuum") as mock_vacuum:
            agg.compress_if_needed()
            self.assertTrue(mock_vacuum.called,
                            "vacuum should run on first compress_if_needed")

        # Second call within an hour: vacuum should be skipped (throttled)
        with patch.object(agg.db, "vacuum") as mock_vacuum2:
            agg.compress_if_needed()
            self.assertFalse(mock_vacuum2.called,
                             "vacuum should be throttled within the same hour")

        agg.close()

    def test_vacuum_reclaims_space(self):
        """After purging raw rows, VACUUM should reclaim disk space."""
        import sqlite3
        self._insert_system_raw(count=20)
        before_size = os.path.getsize(self.temp_db.name)
        self.db.compress_to_1m()
        self.db.vacuum()
        after_size = os.path.getsize(self.temp_db.name)
        # After purging + vacuum the file should not be larger; typically smaller.
        self.assertLessEqual(after_size, before_size,
                             "file should not grow after purge + vacuum")


if __name__ == "__main__":
    unittest.main()
