#!/usr/bin/env python3
"""Test that CPU usage is normalized by logical core count and clamped at 100%.

Covers the 7sc fix in aggregator.py: the summed per-process cpu_percent is
divided by cpu_count, and clamped to 100 when it would exceed 100%, logging a
warning on each clamp.
"""

import os
import sys
import tempfile
import unittest
from unittest import mock


def _build_aggregator():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import aggregator as agg_mod

    db_path = os.path.join(tempfile.gettempdir(), "llama-monitor-test.db")
    for suffix in ("", "-wal", "-shm"):
        try:
            os.remove(db_path + suffix)
        except OSError:
            pass

    agg = agg_mod.Aggregator(db_path=db_path, collect_metrics=False)
    # Stub the server collector so collect_all_metrics doesn't hit the network
    agg.server_collector.collect = mock.Mock(return_value={"server": {}})
    return agg, agg_mod


def _make_system_metrics(cpu_count, process_cpu_values):
    """Build a system_metrics dict with the given CPU data."""
    return {
        "timestamp": 1,
        "cpu": {
            "count": cpu_count,
            "cores": [0] * cpu_count,
            "process_cpu": {
                f"proc{i}": {"cpu_percent": val} for i, val in enumerate(process_cpu_values)
            },
        },
        "gpu": {},
        "memory": {},
        "system": {},
    }


class TestCpuNormalization(unittest.TestCase):
    def test_clamped_to_100_when_sum_equals_core_capacity(self):
        agg, _ = _build_aggregator()
        # 4 cores maxed out -> sum = 400 -> /4 = 100 (no clamp, no warning)
        agg.system_collector.collect = mock.Mock(
            return_value=_make_system_metrics(4, [100, 100, 100, 100])
        )
        metrics = agg.collect_all_metrics()
        self.assertEqual(metrics["system"]["cpu_percent"], 100.0)

    def test_clamps_and_warns_when_avg_exceeds_100(self):
        agg, agg_mod = _build_aggregator()
        # 4 cores, summed process cpu = 500 -> /4 = 125 -> clamped to 100 + warning
        agg.system_collector.collect = mock.Mock(
            return_value=_make_system_metrics(4, [125, 125, 125, 125])
        )
        with mock.patch.object(agg_mod.logger, "warning") as mock_warning:
            metrics = agg.collect_all_metrics()
        self.assertEqual(metrics["system"]["cpu_percent"], 100.0)
        mock_warning.assert_called_once()
        # The warning should carry the raw summed CPU and core count
        args, _ = mock_warning.call_args
        self.assertIn("500.0", args[0] % args[1:] if len(args) > 1 else args[0])

    def test_no_clamp_when_avg_within_range(self):
        agg, agg_mod = _build_aggregator()
        # 4 cores, sum = 200 -> /4 = 50
        agg.system_collector.collect = mock.Mock(
            return_value=_make_system_metrics(4, [50, 50, 50, 50])
        )
        with mock.patch.object(agg_mod.logger, "warning") as mock_warning:
            metrics = agg.collect_all_metrics()
        self.assertEqual(metrics["system"]["cpu_percent"], 50.0)
        mock_warning.assert_not_called()

    def test_fallback_to_os_cpu_when_no_process_cpu(self):
        agg, agg_mod = _build_aggregator()
        # No process_cpu -> fall back to total OS percent (no normalization)
        agg.system_collector.collect = mock.Mock(
            return_value={
                "timestamp": 1,
                "cpu": {"count": 4, "percent": 35.0},
                "gpu": {},
                "memory": {},
                "system": {},
            }
        )
        with mock.patch.object(agg_mod.logger, "warning") as mock_warning:
            metrics = agg.collect_all_metrics()
        self.assertEqual(metrics["system"]["cpu_percent"], 35.0)
        mock_warning.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
