#!/usr/bin/env python3
"""Unit tests for configurable top-bar slots (bead llama-monitor-fcgq).

Covers the m6p design: cumulative_energy attribution persistence, lifetime
per-category accumulators + restart-resume, strict range energy boundaries,
the /api/metrics/slot endpoint, and slot settings save/reset.
"""
import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

# Set up environment before importing web_server
os.environ['FLASK_ENV'] = 'testing'

from db import Database
from electricity_cost import ElectricityCostCalculator
from web_server import (
    app, _resolve_range, _slot_title, _slot_wh, SLOT_DEFAULTS, SLOT_CATEGORIES,
)


class CumulativeEnergyAttributionTest(unittest.TestCase):
    """cumulative_energy attribution columns persist and reload."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, "test.db")
        self.db = Database(self.db_path)
        self.db.connect()

    def tearDown(self):
        self.db.close()
        self.tmpdir.cleanup()

    def test_update_cumulative_energy_persists_attribution(self):
        self.db.update_cumulative_energy(
            session_start="2026-08-01 00:00:00",
            total_wh=1000.0,
            gpu_wh=700.0,
            cpu_wh=300.0,
            session_cost_usd=0.12,
            direct_wh=400.0,
            baseline_wh=200.0,
            other_wh=150.0,
            unattributed_wh=250.0,
        )
        cum = self.db.get_cumulative_energy()
        self.assertAlmostEqual(cum["direct_wh"], 400.0, places=6)
        self.assertAlmostEqual(cum["baseline_wh"], 200.0, places=6)
        self.assertAlmostEqual(cum["other_wh"], 150.0, places=6)
        self.assertAlmostEqual(cum["unattributed_wh"], 250.0, places=6)

    def test_attribution_defaults_to_zero(self):
        # Legacy call without attribution args -> columns default to 0.
        self.db.update_cumulative_energy(
            session_start="2026-08-01 00:00:00",
            total_wh=100.0,
            gpu_wh=70.0,
            cpu_wh=30.0,
            session_cost_usd=0.01,
        )
        cum = self.db.get_cumulative_energy()
        self.assertAlmostEqual(cum["direct_wh"], 0.0, places=6)
        self.assertAlmostEqual(cum["unattributed_wh"], 0.0, places=6)


class LifetimeAccumulatorTest(unittest.TestCase):
    """Lifetime per-category accumulators persist across restart."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, "test.db")
        self.db = Database(self.db_path)
        self.calc = ElectricityCostCalculator(self.db)

    def tearDown(self):
        self.db.close()
        self.tmpdir.cleanup()

    def _blame_prims(self):
        return {"llama_share": 0.7, "cpu_idle_w": 10.0, "gpu_idle_w": 30.0,
                "llama_running": True}

    def test_lifetime_counters_accumulate(self):
        prims = self._blame_prims()
        self.calc.update_power_readings(240.0, 60.0, 3600.0, primitives=prims)
        self.assertGreater(self.calc.total_direct_wh, 0.0)
        self.assertGreater(self.calc.total_baseline_wh, 0.0)
        self.assertGreater(self.calc.total_other_wh, 0.0)

    def test_restart_restores_lifetime_attribution(self):
        prims = self._blame_prims()
        self.calc.update_power_readings(240.0, 60.0, 3600.0, primitives=prims)
        before = {
            "direct": self.calc.total_direct_wh,
            "baseline": self.calc.total_baseline_wh,
            "other": self.calc.total_other_wh,
            "unattributed": self.calc.total_unattributed_wh,
        }
        # Persist cumulative_energy (as stop_session does on shutdown), then
        # restart: the new calculator must restore the lifetime attribution.
        self.calc.stop_session()
        calc2 = ElectricityCostCalculator(self.db)
        self.assertAlmostEqual(calc2.total_direct_wh, before["direct"], places=3)
        self.assertAlmostEqual(calc2.total_baseline_wh, before["baseline"], places=3)
        self.assertAlmostEqual(calc2.total_other_wh, before["other"], places=3)
        self.assertAlmostEqual(
            calc2.total_unattributed_wh, before["unattributed"], places=3)

    def test_clear_session_resets_lifetime(self):
        prims = self._blame_prims()
        self.calc.update_power_readings(240.0, 60.0, 3600.0, primitives=prims)
        self.assertGreater(self.calc.total_direct_wh, 0.0)
        self.calc.clear_session_energy()
        self.assertEqual(self.calc.total_direct_wh, 0.0)
        self.assertEqual(self.calc.total_unattributed_wh, 0.0)


class ResolveRangeTest(unittest.TestCase):
    """_resolve_range week/month boundaries (Sunday week start, 1st-of-month)."""

    def _resolve(self, timeframe, y, m, d):
        from datetime import datetime
        return _resolve_range(timeframe, datetime(y, m, d))

    def test_this_week_sunday_start(self):
        # 2026-08-27 is a Thursday; this week starts Sunday 8/23, ends 8/27.
        self.assertEqual(self._resolve("this_week", 2026, 8, 27),
                         ("2026-08-23", "2026-08-27"))

    def test_this_week_on_sunday(self):
        # On a Sunday (8/23), this week is just that day.
        self.assertEqual(self._resolve("this_week", 2026, 8, 23),
                         ("2026-08-23", "2026-08-23"))

    def test_this_week_when_monday(self):
        # 8/24 is Monday; week starts Sunday 8/23.
        self.assertEqual(self._resolve("this_week", 2026, 8, 24),
                         ("2026-08-23", "2026-08-24"))

    def test_last_week_sunday_to_saturday(self):
        # 2026-08-27 Thursday -> last week Sun 8/16 .. Sat 8/22.
        self.assertEqual(self._resolve("last_week", 2026, 8, 27),
                         ("2026-08-16", "2026-08-22"))

    def test_this_month_starts_first(self):
        self.assertEqual(self._resolve("this_month", 2026, 8, 27),
                         ("2026-08-01", "2026-08-27"))

    def test_last_month(self):
        self.assertEqual(self._resolve("last_month", 2026, 8, 27),
                         ("2026-07-01", "2026-07-31"))

    def test_yesterday(self):
        self.assertEqual(self._resolve("yesterday", 2026, 8, 27),
                         ("2026-08-26", "2026-08-26"))

    def test_rolling_7(self):
        self.assertEqual(self._resolve("rolling_7", 2026, 8, 27),
                         ("2026-08-21", "2026-08-27"))

    def test_rolling_30(self):
        self.assertEqual(self._resolve("rolling_30", 2026, 8, 27),
                         ("2026-07-29", "2026-08-27"))

    def test_all_time_none(self):
        self.assertIsNone(self._resolve("all_time", 2026, 8, 27))


class RangeEnergyTest(unittest.TestCase):
    """get_range_energy is strict/inclusive on both boundaries."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, "test.db")
        self.db = Database(self.db_path)
        self.db.connect()
        # Seed daily energy across several days with attribution.
        rows = [
            ("2026-08-20", 100.0, 10.0, 20.0, 30.0, 40.0),
            ("2026-08-21", 200.0, 20.0, 40.0, 60.0, 80.0),
            ("2026-08-22", 300.0, 30.0, 60.0, 90.0, 120.0),
        ]
        for date, total, d, b, o, u in rows:
            self.db.update_today_energy_archived(
                date=date, total_wh=total, gpu_wh=total, cpu_wh=0.0,
                timestamp=f"{date} 23:59:59",
                direct_wh=d, baseline_wh=b, other_wh=o, unattributed_wh=u,
            )

    def tearDown(self):
        self.db.close()
        self.tmpdir.cleanup()

    def test_range_inclusive_boundaries(self):
        rows = self.db.get_range_energy("2026-08-21", "2026-08-22")
        dates = [r["date"] for r in rows]
        self.assertEqual(dates, ["2026-08-21", "2026-08-22"])
        # Both boundary days included; 8/20 excluded.

    def test_range_single_day(self):
        rows = self.db.get_range_energy("2026-08-21", "2026-08-21")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "2026-08-21")

    def test_range_empty_when_no_overlap(self):
        rows = self.db.get_range_energy("2026-08-23", "2026-08-24")
        self.assertEqual(rows, [])

    def test_slot_wh_sum_selects_categories(self):
        # All-time uses cumulative; but for range we can verify via a today-less
        # config by calling _slot_wh with a range timeframe.
        from datetime import datetime
        # Patch now so "this_week" resolves deterministically? Instead use
        # _slot_wh directly with the seeded range via a fixed timeframe.
        cfg = {"timeframe": "rolling_7", "unit": "cost",
               "categories": ["direct"]}
        # Rolling 7 from 8/22 covers 8/16-8/22, so includes 8/20, 8/21, 8/22;
        # direct sum = 10 + 20 + 30 = 60.
        with patch("web_server.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 8, 22, 12, 0, 0)
            wh = _slot_wh(self.db, cfg)
        self.assertAlmostEqual(wh, 60.0, places=6)


class SlotEndpointTest(unittest.TestCase):
    """/api/metrics/slot returns wh/usd/title."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        # The slot endpoint uses _get_db(db_path), so patch it to return our db.
        self.patcher = patch('web_server._get_db')
        self.mock_get_db = self.patcher.start()
        self.db = Database(self.temp_db.name)
        self.db.connect()
        self.mock_get_db.return_value = self.db
        # Seed today's energy with attribution.
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        self.db.update_today_energy_archived(
            date=today, total_wh=1000.0, gpu_wh=1000.0, cpu_wh=0.0,
            timestamp=f"{today} 23:59:59",
            direct_wh=400.0, baseline_wh=300.0, other_wh=200.0,
            unattributed_wh=100.0,
        )

    def tearDown(self):
        self.patcher.stop()
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_slot_today_energy(self):
        with self.app:
            resp = self.app.get("/api/metrics/slot?timeframe=today&unit=energy"
                                "&categories=direct,baseline,other,unattributed")
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertAlmostEqual(data["wh"], 1000.0, places=6)
            self.assertEqual(data["title"], "Today's Energy")

    def test_slot_today_cost(self):
        with self.app:
            self.db.set_setting("cost_rate_usd_per_kwh", "0.12")
            resp = self.app.get("/api/metrics/slot?timeframe=today&unit=cost"
                                "&categories=direct,baseline,other,unattributed")
            data = resp.get_json()
            self.assertAlmostEqual(data["usd"], 0.12, places=6)
            self.assertEqual(data["title"], "Today's Cost")

    def test_slot_all_time(self):
        with self.app:
            self.db.update_cumulative_energy(
                session_start="2026-08-01 00:00:00", total_wh=5000.0,
                gpu_wh=3500.0, cpu_wh=1500.0, session_cost_usd=0.60,
                direct_wh=2000.0, baseline_wh=1000.0, other_wh=1000.0,
                unattributed_wh=1000.0,
            )
            resp = self.app.get("/api/metrics/slot?timeframe=all_time&unit=cost"
                                "&categories=direct,baseline,other,unattributed")
            data = resp.get_json()
            self.assertAlmostEqual(data["wh"], 5000.0, places=6)
            self.assertEqual(data["title"], "Total Cost")

    def test_slot_subset_categories(self):
        with self.app:
            resp = self.app.get("/api/metrics/slot?timeframe=today&unit=energy"
                                "&categories=direct")
            data = resp.get_json()
            self.assertAlmostEqual(data["wh"], 400.0, places=6)
            self.assertEqual(data["title"], "Today's Direct Energy")


class SlotSettingsTest(unittest.TestCase):
    """Slot settings save/reset via /api/settings."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.patcher = patch('web_server.get_db')
        self.mock_get_db = self.patcher.start()
        self.db = Database(self.temp_db.name)
        self.db.connect()
        self.mock_get_db.return_value = self.db

    def tearDown(self):
        self.patcher.stop()
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_get_settings_returns_slot_defaults(self):
        with self.app:
            resp = self.app.get("/api/settings")
            data = resp.get_json()
            self.assertEqual(data["slot_1_timeframe"], "today")
            self.assertEqual(data["slot_1_unit"], "cost")
            self.assertEqual(
                data["slot_1_categories"], "direct,baseline,other,unattributed")
            self.assertEqual(data["slot_3_timeframe"], "all_time")

    def test_set_settings_updates_slots(self):
        payload = {
            "slot_1_timeframe": "this_week",
            "slot_1_unit": "energy",
            "slot_1_categories": ["direct", "other"],
        }
        with self.app:
            resp = self.app.post("/api/settings", json=payload)
            self.assertEqual(resp.status_code, 200)
            data = self.app.get("/api/settings").get_json()
            self.assertEqual(data["slot_1_timeframe"], "this_week")
            self.assertEqual(data["slot_1_unit"], "energy")
            self.assertEqual(data["slot_1_categories"], "direct,other")

    def test_reset_settings_restores_slot_defaults(self):
        # Change a slot, then reset.
        with self.app:
            self.app.post("/api/settings", json={
                "slot_4_timeframe": "this_month", "slot_4_unit": "cost",
            })
            self.app.post("/api/settings/reset")
            data = self.app.get("/api/settings").get_json()
            self.assertEqual(data["slot_4_timeframe"], "all_time")
            self.assertEqual(data["slot_4_unit"], "energy")
            self.assertEqual(data["slot_4_categories"],
                             "direct,baseline,other,unattributed")


if __name__ == "__main__":
    unittest.main()
