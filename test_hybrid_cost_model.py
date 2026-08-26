"""Hybrid cost model tests (llama-monitor-h9z0 / ym0 / 2byy).

Mirrors the 18-item testing plan in docs/SPEC-hybrid-cost-model.md. Covers
compute_blame invariants, per-component idle baselines, migration/backfill,
rollover, restart recovery, start_session lockstep, and write-path blame.
"""
import unittest
import os
import sqlite3
import tempfile
from unittest.mock import patch, Mock

from db import Database
from electricity_cost import ElectricityCostCalculator
from aggregator import Aggregator


def _blame(gpu_power_w, cpu_power_w, primitives):
    calc = ElectricityCostCalculator.__new__(ElectricityCostCalculator)
    return calc.compute_blame(gpu_power_w, cpu_power_w, primitives)


class BlameInvariantTest(unittest.TestCase):
    """Tests 1, 2, 3, 11: blame categories sum to totalPower."""

    def sum_matches(self, gpu_w, cpu_w, primitives):
        b = _blame(gpu_w, cpu_w, primitives)
        total = gpu_w + cpu_w
        return abs((b["direct_w"] + b["baseline_w"] + b["other_w"]
                    + b["unattributed_w"]) - total) < 1e-6

    def test_invariant_representative(self):
        prims = {
            "llama_share": 0.7, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
            "llama_running": True,
        }
        self.assertTrue(self.sum_matches(240.0, 60.0, prims))

    def test_netflix_llama_idle_gets_baseline_only(self):
        # llama idle (share 0) + high other activity -> direct 0, baseline only
        b = _blame(300.0, 50.0, {
            "llama_share": 0.0, "cpu_idle_w": 10.0, "gpu_idle_w": 40.0,
            "llama_running": True,
        })
        self.assertAlmostEqual(b["direct_w"], 0.0, places=6)
        self.assertAlmostEqual(b["baseline_w"], 50.0, places=6)

    def test_both_active_splits_delta(self):
        # llama active at share 0.8 -> delta splits proportionally
        b = _blame(200.0, 100.0, {
            "llama_share": 0.8, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
            "llama_running": True,
        })
        total = 300.0
        baseline = 40.0
        delta = total - baseline
        self.assertAlmostEqual(b["direct_w"], 0.8 * delta, places=6)
        self.assertAlmostEqual(b["other_w"], 0.2 * delta, places=6)
        self.assertAlmostEqual(b["baseline_w"], baseline, places=6)

    def test_power_below_baseline_clamped(self):
        # totalPower < baseline -> terms clamp so they still sum to totalPower
        b = _blame(10.0, 5.0, {
            "llama_share": 1.0, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
            "llama_running": True,
        })
        self.assertAlmostEqual(b["direct_w"] + b["baseline_w"]
                               + b["other_w"] + b["unattributed_w"],
                               15.0, places=6)

    def test_llama_not_running_all_unattributed(self):
        b = _blame(240.0, 60.0, {
            "llama_share": 1.0, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
            "llama_running": False,
        })
        self.assertEqual(b["direct_w"], 0.0)
        self.assertEqual(b["unattributed_w"], 300.0)

    def test_no_primitives_backward_compat(self):
        # Test 8: without primitives, all energy -> unattributed
        b = _blame(240.0, 60.0, None)
        self.assertEqual(b["direct_w"], 0.0)
        self.assertEqual(b["unattributed_w"], 300.0)


class ElectricityCostWritePathTest(unittest.TestCase):
    """Tests 12, 14, 15, 16, 17: write-path blame + row invariant."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, "test.db")
        self.db = Database(self.db_path)
        self.calc = ElectricityCostCalculator(self.db)

    def tearDown(self):
        self.db.close()
        self.tmpdir.cleanup()

    def row_blame(self):
        e = self.db.get_today_energy()
        return (e.get("direct_wh", 0.0), e.get("baseline_wh", 0.0),
                e.get("other_wh", 0.0), e.get("unattributed_wh", 0.0))

    def test_blame_columns_accumulate(self):
        # Test 12: blame_w x duration accumulates per-interval
        prims = {"llama_share": 0.7, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
                 "llama_running": True}
        self.calc.update_power_readings(240.0, 60.0, 3600.0, primitives=prims)
        direct, baseline, other, unatt = self.row_blame()
        self.assertGreater(direct, 0.0)
        self.assertGreater(baseline, 0.0)
        self.assertGreater(other, 0.0)
        self.assertAlmostEqual(direct + baseline + other + unatt,
                               self.calc.today_energy_wh, places=3)

    def test_row_invariant_holds(self):
        # Test 14: direct+baseline+other+unattributed == total_wh
        prims = {"llama_share": 0.5, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
                 "llama_running": True}
        self.calc.update_power_readings(200.0, 100.0, 7200.0, primitives=prims)
        e = self.db.get_today_energy()
        self.assertAlmostEqual(
            e["direct_wh"] + e["baseline_wh"] + e["other_wh"]
            + e["unattributed_wh"], e["total_wh"], places=3)

    def test_clear_session_preserves_invariant(self):
        # Test 15: clear_session_energy zeros blame + total together
        self.calc.clear_session_energy()
        e = self.db.get_today_energy()
        self.assertAlmostEqual(
            e["direct_wh"] + e["baseline_wh"] + e["other_wh"]
            + e["unattributed_wh"], e["total_wh"], places=6)

    def test_restart_recovery_restores_blame(self):
        # Test 16: a new calculator restores blame counters from the row
        prims = {"llama_share": 0.7, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
                 "llama_running": True}
        self.calc.update_power_readings(240.0, 60.0, 3600.0, primitives=prims)
        self.calc2 = ElectricityCostCalculator(self.db)
        self.assertAlmostEqual(self.calc2.today_direct_wh,
                               self.calc.today_direct_wh, places=3)
        self.assertAlmostEqual(self.calc2.today_energy_wh,
                               self.calc.today_energy_wh, places=3)

    def test_start_session_preserves_blame(self):
        # Test 17: start_session does NOT reset blame counters
        prims = {"llama_share": 0.7, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
                 "llama_running": True}
        self.calc.update_power_readings(240.0, 60.0, 3600.0, primitives=prims)
        before_direct = self.calc.today_direct_wh
        self.calc.start_session()
        self.assertEqual(self.calc.today_direct_wh, before_direct)

    def test_midnight_rollover_archives_blame(self):
        # Test 13: prior day's blame archived with final values; counters reset;
        # next-day blame lands in the correct row.
        prims = {"llama_share": 0.7, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
                 "llama_running": True}
        self.calc.update_power_readings(240.0, 60.0, 3600.0, primitives=prims)
        # Simulate a day boundary
        self.calc.last_today_date = "1999-01-01"
        self.calc.update_power_readings(240.0, 60.0, 3600.0, primitives=prims)

        # Prior day archived with blame values, today reset then accumulated
        cur = self.db.connect().cursor()
        cur.execute(
            "SELECT direct_wh, baseline_wh, other_wh, unattributed_wh, total_wh "
            "FROM daily_energy WHERE date = '1999-01-01'"
        )
        prev = cur.fetchone()
        self.assertGreater(prev[0] + prev[1] + prev[2] + prev[3], 0.0)
        self.assertAlmostEqual(prev[0] + prev[1] + prev[2] + prev[3],
                               prev[4], places=3)

        # Today's row should only contain the second interval's blame
        today = self.db.get_today_energy()
        self.assertAlmostEqual(today["direct_wh"] + today["baseline_wh"]
                               + today["other_wh"] + today["unattributed_wh"],
                               today["total_wh"], places=3)
        self.assertAlmostEqual(today["total_wh"], 300.0, places=3)


class MigrationTest(unittest.TestCase):
    """Tests 7, 18: column migration + backfill."""

    def _build_legacy_db(self, tmpdir):
        """Create a legacy DB (schema_version present, no blame columns)."""
        db_path = os.path.join(tmpdir.name, "legacy.db")
        conn = sqlite3.connect(db_path)
        conn.execute(
            "CREATE TABLE schema_version (version TEXT PRIMARY KEY, "
            "created_at TEXT DEFAULT (datetime('now')))"
        )
        conn.execute("INSERT INTO schema_version (version) VALUES ('legacy')")
        conn.execute(
            "CREATE TABLE daily_energy (date TEXT PRIMARY KEY, total_wh REAL "
            "DEFAULT 0, gpu_wh REAL DEFAULT 0, cpu_wh REAL DEFAULT 0, "
            "last_update TEXT)"
        )
        conn.execute(
            "CREATE TABLE idle_baseline (timestamp TEXT PRIMARY KEY, "
            "cpu_percent REAL, gpu_percent REAL, system_power_w REAL, "
            "is_valid BOOLEAN DEFAULT 1)"
        )
        conn.commit()
        conn.close()
        return db_path

    def test_columns_added_and_backfill(self):
        # Build a legacy DB without blame columns, insert a row, migrate, verify
        tmpdir = tempfile.TemporaryDirectory()
        db_path = self._build_legacy_db(tmpdir)
        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO daily_energy (date, total_wh) VALUES ('2026-08-01', 500.0)"
        )
        conn.commit()
        conn.close()

        # Opening with Database sees schema_version -> runs _migrate_schema
        db = Database(db_path)

        cur = db.connect().cursor()
        cur.execute("PRAGMA table_info(daily_energy)")
        cols = {row[1] for row in cur.fetchall()}
        for col in ("direct_wh", "baseline_wh", "other_wh", "unattributed_wh"):
            self.assertIn(col, cols)

        # Backfill ran: existing row got unattributed_wh = total_wh
        cur.execute(
            "SELECT direct_wh, baseline_wh, other_wh, unattributed_wh "
            "FROM daily_energy WHERE date = '2026-08-01'"
        )
        row = cur.fetchone()
        self.assertAlmostEqual(row[0] + row[1] + row[2], 0.0, places=6)
        self.assertAlmostEqual(row[3], 500.0, places=6)

        db.close()
        tmpdir.cleanup()

    def test_idle_baseline_columns_added(self):
        tmpdir = tempfile.TemporaryDirectory()
        db_path = self._build_legacy_db(tmpdir)
        db = Database(db_path)

        cur = db.connect().cursor()
        cur.execute("PRAGMA table_info(idle_baseline)")
        cols = {row[1] for row in cur.fetchall()}
        self.assertIn("cpu_idle_w", cols)
        self.assertIn("gpu_idle_w", cols)

        db.close()
        tmpdir.cleanup()

class AggregatorPrimitivesTest(unittest.TestCase):
    """Tests 9, 10: gate fires on true idle; llama_running via process union."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.tmp.close()
        self.db_path = self.tmp.name

    def tearDown(self):
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    def _make_system_metrics(self, cpu_percent=0.0, gpu_usage=0.0,
                             gpu_power_w=100.0, cpu_power_w=20.0,
                             process_cpu=None, process_gpu=None):
        return {
            "timestamp": 1234567890,
            "cpu": {"percent": cpu_percent, "count": 1, "cores": [],
                    "process_cpu": process_cpu or {}},
            "gpu": {"usage": gpu_usage, "power_w": gpu_power_w,
                    "memory_used": 8192, "memory_total": 16384},
            "memory": {"used": 16384, "total": 32768, "percent": 50.0},
            "system": {"system_power_w": gpu_power_w + cpu_power_w,
                       "cpu_power_w": cpu_power_w},
            "process_gpu": process_gpu or {},
        }

    @patch("aggregator.IdleBaselineTracker")
    @patch("aggregator.ServerMetricsCollector._make_request")
    def test_gate_fires_on_true_idle(self, mock_req, mock_idle):
        """Test 9: true idle (0% util, >0W power) triggers baseline capture."""
        agg = Aggregator(db_path=self.db_path, idle_baseline_w=40.0,
                         collect_metrics=False)
        mock_tracker = Mock()
        agg.idle_tracker = mock_tracker
        mock_req.return_value = {"prompt_tokens_total": 0, "requests_processing": 0}
        with patch("aggregator.SystemMetricsCollector.collect") as mock_sys:
            mock_sys.return_value = self._make_system_metrics(
                cpu_percent=0.0, gpu_usage=0.0, gpu_power_w=100.0, cpu_power_w=20.0
            )
            agg.collect_all_metrics()
        mock_tracker.check_idle.assert_called_once_with(0.0, 0.0, 100.0, 20.0)
        agg.close()

    @patch("aggregator.IdleBaselineTracker")
    @patch("aggregator.ServerMetricsCollector._make_request")
    def test_llama_running_via_process_cpu_union(self, mock_req, mock_idle):
        """Test 10: llama_running true via process_cpu on non-NVML system."""
        agg = Aggregator(db_path=self.db_path, idle_baseline_w=40.0,
                         collect_metrics=False)
        mock_tracker = Mock()
        mock_tracker.get_recent_baseline.return_value = None
        agg.idle_tracker = mock_tracker
        mock_req.return_value = {"prompt_tokens_total": 0, "requests_processing": 0}
        sys_metrics = self._make_system_metrics(
            cpu_percent=50.0, gpu_usage=0.0, gpu_power_w=0.0, cpu_power_w=60.0,
            process_cpu={"llama-server": {"pid": 123, "cpu_percent": 30.0}},
        )
        with patch("aggregator.SystemMetricsCollector.collect") as mock_sys:
            mock_sys.return_value = sys_metrics
            agg.collect_all_metrics()
        primitives = agg._compute_blame_primitives(
            agg.last_metrics.get("system", {}),
            sys_metrics,
        )
        self.assertTrue(primitives["llama_running"])
        self.assertGreater(primitives["llama_cpu_share"], 0.0)
        agg.close()


if __name__ == "__main__":
    unittest.main()
