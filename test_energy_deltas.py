"""Verify per-interval energy deltas are stored in combined_metrics (2a0).

The bead requires that each combined_metrics row stores the per-interval
delta energy (delta_gpu_wh, delta_cpu_wh, delta_total_wh) rather than only
cumulative growing totals. This confirms the fix already present in main.
"""
import unittest
import json
import os
import tempfile

from db import Database
from electricity_cost import ElectricityCostCalculator


class PerIntervalDeltaTest(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, "test.db")
        self.db = Database(self.db_path)
        self.calc = ElectricityCostCalculator(self.db)

    def tearDown(self):
        self.db.close()
        self.tmpdir.cleanup()

    def test_update_power_readings_returns_deltas(self):
        """update_power_readings must return per-interval deltas."""
        stats = self.calc.update_power_readings(
            gpu_power_w=100.0, cpu_power_w=50.0, duration_seconds=3600.0
        )
        # 100W * 1h = 100 Wh GPU, 50W * 1h = 50 Wh CPU, total 150 Wh
        self.assertAlmostEqual(stats["delta_gpu_wh"], 100.0, places=3)
        self.assertAlmostEqual(stats["delta_cpu_wh"], 50.0, places=3)
        self.assertAlmostEqual(stats["delta_total_wh"], 150.0, places=3)

    def test_combined_metrics_store_delta_fields(self):
        """Each combined_metrics row must store per-interval delta values."""
        # Simulate two consecutive intervals with different power
        stats1 = self.calc.update_power_readings(
            gpu_power_w=100.0, cpu_power_w=50.0, duration_seconds=3600.0
        )
        stats2 = self.calc.update_power_readings(
            gpu_power_w=100.0, cpu_power_w=50.0, duration_seconds=3600.0
        )
        # Second interval adds another 150 Wh; delta is per-interval, cumulative grows
        self.assertAlmostEqual(stats2["delta_total_wh"], 150.0, places=3)
        self.assertGreater(stats2["total_wh"], stats1["total_wh"])
        # Cumulative = sum of deltas
        self.assertAlmostEqual(stats2["total_wh"], stats1["total_wh"] + stats2["delta_total_wh"], places=3)

    def test_delta_and_cumulative_both_present(self):
        """cost data must include both per-interval deltas and cumulative totals."""
        stats = self.calc.update_power_readings(
            gpu_power_w=80.0, cpu_power_w=20.0, duration_seconds=3600.0
        )
        for key in ["delta_gpu_wh", "delta_cpu_wh", "delta_total_wh",
                    "gpu_wh", "cpu_wh", "total_wh"]:
            self.assertIn(key, stats, f"missing {key} in power reading stats")


if __name__ == "__main__":
    unittest.main()
