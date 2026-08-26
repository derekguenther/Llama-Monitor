#!/usr/bin/env python3
"""Tests for the bp3 eliminate-daemon backports.

Verifies the enhancements backported from the retired daemon module into
aggregator.py:
- Step 1 (D1): idle-baseline tracking wired and gated on meaningful values.
- Step 1a (B1): last_metrics populated by collect_all_metrics.
- Step 2 (D2/G1): real elapsed-duration energy deltas + duration literals.
- Step 3 (D3/G2): cumulative-energy persistence with ISO session_start.
- Step 6 (S1): /api/status returns standalone, never 500.
"""
import os
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.dirname(__file__))

from aggregator import Aggregator


def _make_system_metrics(cpu_percent=50.0, gpu_usage=80.0, power_w=300.0):
    """Build a realistic system_metrics dict for mocks."""
    return {
        "timestamp": 1234567890,
        "cpu": {"percent": cpu_percent, "cores": [], "process_cpu": {}},
        "gpu": {"usage": gpu_usage, "power_w": power_w * 0.8,
                "memory_used": 8192, "memory_total": 16384},
        "memory": {"used": 16384, "total": 32768, "percent": 50.0},
        "system": {"system_power_w": power_w, "cpu_power_w": power_w * 0.2},
        "process_gpu": {},
    }


class TestIdleTrackingBackport(unittest.TestCase):
    """Step 1 (D1): idle-baseline wiring gated on meaningful values."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.tmp.close()
        self.db_path = self.tmp.name

    def tearDown(self):
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    @patch("aggregator.IdleBaselineTracker")
    @patch("aggregator.ServerMetricsCollector._make_request")
    def test_check_idle_called_when_values_meaningful(self, mock_req, mock_idle):
        """check_idle is called only when power/cpu/gpu are all > 0."""
        aggregator = Aggregator(
            db_path=self.db_path, idle_baseline_w=40.0, collect_metrics=False
        )
        # Replace idle tracker with a real mock to assert the call
        mock_tracker = Mock()
        aggregator.idle_tracker = mock_tracker

        mock_req.return_value = {
            "prompt_tokens_total": 100, "requests_processing": 0,
        }
        with patch("aggregator.SystemMetricsCollector.collect") as mock_sys:
            mock_sys.return_value = _make_system_metrics(
                cpu_percent=50.0, gpu_usage=80.0, power_w=300.0
            )
            aggregator.collect_all_metrics()

        mock_tracker.check_idle.assert_called_once_with(50.0, 80.0, 240.0, 60.0)
        aggregator.close()

    @patch("aggregator.IdleBaselineTracker")
    @patch("aggregator.ServerMetricsCollector._make_request")
    def test_check_idle_not_called_when_all_zero(self, mock_req, mock_idle):
        """check_idle is NOT called when system values are all 0 (no false baseline)."""
        aggregator = Aggregator(
            db_path=self.db_path, idle_baseline_w=40.0, collect_metrics=False
        )
        mock_tracker = Mock()
        aggregator.idle_tracker = mock_tracker

        mock_req.return_value = {
            "prompt_tokens_total": 0, "requests_processing": 0,
        }
        with patch("aggregator.SystemMetricsCollector.collect") as mock_sys:
            mock_sys.return_value = _make_system_metrics(
                cpu_percent=0.0, gpu_usage=0.0, power_w=0.0
            )
            aggregator.collect_all_metrics()

        mock_tracker.check_idle.assert_not_called()
        aggregator.close()


class TestLastMetricsBackport(unittest.TestCase):
    """Step 1a (B1): last_metrics populated by collect_all_metrics."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.tmp.close()
        self.db_path = self.tmp.name

    def tearDown(self):
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    @patch("aggregator.ServerMetricsCollector._make_request")
    def test_last_metrics_set_on_collect(self, mock_req):
        """collect_all_metrics stores its result in last_metrics."""
        aggregator = Aggregator(
            db_path=self.db_path, idle_baseline_w=40.0, collect_metrics=False
        )
        mock_req.return_value = {
            "prompt_tokens_total": 100, "requests_processing": 0,
        }
        with patch("aggregator.SystemMetricsCollector.collect") as mock_sys:
            mock_sys.return_value = _make_system_metrics()
            result = aggregator.collect_all_metrics()

        self.assertEqual(aggregator.last_metrics, result)
        self.assertIn("timestamp", aggregator.last_metrics)
        aggregator.close()


class TestRealDurationBackport(unittest.TestCase):
    """Step 2 (D2/G1): real elapsed-duration energy deltas + duration literals."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.tmp.close()
        self.db_path = self.tmp.name

    def tearDown(self):
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    def test_store_uses_real_duration_not_hardcoded(self):
        """store_raw_metrics passes elapsed time (not 1.0) to update_power_readings."""
        aggregator = Aggregator(
            db_path=self.db_path, idle_baseline_w=40.0, collect_metrics=False
        )
        metrics = {
            "timestamp": 1234567890,
            "server": {"prompt_tokens_total": 100, "requests_processing": 0},
            "system": {
                "cpu_percent": 50.0, "gpu_usage": 80.0, "system_power_w": 300.0,
                "gpu_power_w": 240.0, "cpu_power_w": 60.0,
                "process_gpu": {},
            },
            "system_raw": _make_system_metrics(),
        }
        # Call twice. The FIRST call initializes _last_cost_time (duration ~ 0);
        # the SECOND call uses real elapsed time. Neither should be the hardcoded
        # 1.0 — that is the G1 fix being verified.
        with patch.object(aggregator.cost_calculator, "update_power_readings",
                          wraps=aggregator.cost_calculator.update_power_readings) as spy:
            aggregator.store_raw_metrics(metrics)
            aggregator.store_raw_metrics(metrics)

        self.assertEqual(spy.call_count, 2)
        # Second call's duration reflects real elapsed time, NOT the hardcoded 1.0
        second_duration = spy.call_args_list[1].kwargs["duration_seconds"]
        self.assertNotEqual(second_duration, 1.0)
        aggregator.close()


class TestCumulativeEnergyBackport(unittest.TestCase):
    """Step 3 (D3/G2): cumulative-energy persistence with ISO session_start."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.tmp.close()
        self.db_path = self.tmp.name

    def tearDown(self):
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    def test_store_persists_cumulative_energy(self):
        """store_raw_metrics calls update_cumulative_energy with ISO session_start."""
        aggregator = Aggregator(
            db_path=self.db_path, idle_baseline_w=40.0, collect_metrics=False
        )
        metrics = {
            "timestamp": 1234567890,
            "server": {"prompt_tokens_total": 100, "requests_processing": 0},
            "system": {
                "cpu_percent": 50.0, "gpu_usage": 80.0, "system_power_w": 300.0,
                "gpu_power_w": 240.0, "cpu_power_w": 60.0,
                "process_gpu": {},
            },
            "system_raw": _make_system_metrics(),
        }
        with patch.object(aggregator.db, "update_cumulative_energy") as mock_upd:
            aggregator.store_raw_metrics(metrics)

        # update_cumulative_energy is called at least once by store_raw_metrics
        # (Step 3). It may also be called internally by start_session() during
        # update_power_readings — both are legitimate. Verify it persisted with
        # an ISO (string) session_start, never an integer.
        self.assertGreaterEqual(mock_upd.call_count, 1)
        for call in mock_upd.call_args_list:
            kwargs = call.kwargs
            self.assertIn("session_start", kwargs)
            # session_start must be a string (ISO), not an int
            self.assertIsInstance(kwargs["session_start"], str)
        aggregator.close()


class TestApiStatusRework(unittest.TestCase):
    """Step 6 (S1 / Finding 1): /api/status returns standalone, never 500."""

    def test_api_status_returns_standalone(self):
        """api_status returns {'status': 'standalone', 'aggregator_available': False}."""
        os.environ['FLASK_ENV'] = 'testing'
        from web_server import app
        client = app.test_client()

        resp = client.get("/api/status")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "standalone")
        self.assertFalse(data["aggregator_available"])


if __name__ == "__main__":
    unittest.main()
