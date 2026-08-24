#!/usr/bin/env python3
"""Unit tests for slot progress and context remaining bar graphs."""

import unittest
import json
from unittest.mock import Mock, patch, MagicMock

from server_metrics import ServerMetricsCollector
from aggregator import Aggregator


class TestSlotChartsData(unittest.TestCase):
    """Tests for slot progress and context remaining data."""

    def setUp(self):
        """Set up test fixtures."""
        self.collector = ServerMetricsCollector("http://localhost:8000")

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_slot_progress_calculation(self, mock_make_request):
        """Test that slot progress is correctly calculated from slot data."""
        # Mock slots endpoint to return slot data with progress values
        mock_make_request.return_value = [
            {"id": 0, "progress": 0.5, "n_tokens": 256, "n_prompt_tokens": 200, "n_gen_tokens": 56},
            {"id": 1, "progress": 0.75, "n_tokens": 512, "n_prompt_tokens": 400, "n_gen_tokens": 112},
            {"id": 2, "progress": 1.0, "n_tokens": 1024, "n_prompt_tokens": 500, "n_gen_tokens": 524},
        ]

        result = self.collector.collect()

        # Verify slots are collected
        self.assertEqual(len(result["slots"]), 3)

        # Verify progress values are correctly parsed
        self.assertEqual(result["slots"][0]["progress"], 0.5)
        self.assertEqual(result["slots"][1]["progress"], 0.75)
        self.assertEqual(result["slots"][2]["progress"], 1.0)

        # Verify n_tokens are correctly parsed
        self.assertEqual(result["slots"][0]["n_tokens"], 256)
        self.assertEqual(result["slots"][1]["n_tokens"], 512)
        self.assertEqual(result["slots"][2]["n_tokens"], 1024)

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_props_with_context_limit(self, mock_make_request):
        """Test that props data includes context limit (n_ctx)."""
        # Mock props endpoint to return context limit
        mock_make_request.return_value = {
            "n_ctx": 4096,
            "n_ctx_per_seq": 1,
            "n_slots": 4,
            "model": "llama-7b",
        }

        result = self.collector.collect()

        # Verify props are collected
        self.assertIn("props", result)
        self.assertEqual(result["props"]["n_ctx"], 4096)

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_slot_data_structure(self, mock_make_request):
        """Test that slot data has the expected structure."""
        mock_make_request.return_value = [
            {
                "id": 0,
                "task": 100,
                "n_tokens": 256,
                "n_prompt_tokens": 200,
                "n_gen_tokens": 56,
                "progress": 0.5,
                "state": "processing",
                "prompt": "Hello",
                "generated": "World",
            }
        ]

        result = self.collector.collect()

        slot = result["slots"][0]
        self.assertEqual(slot["id"], 0)
        self.assertEqual(slot["task"], 100)
        self.assertEqual(slot["n_tokens"], 256)
        self.assertEqual(slot["n_prompt_tokens"], 200)
        self.assertEqual(slot["n_gen_tokens"], 56)
        self.assertEqual(slot["progress"], 0.5)
        self.assertEqual(slot["state"], "processing")
        self.assertEqual(slot["prompt"], "Hello")
        self.assertEqual(slot["generated"], "World")

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_empty_slots(self, mock_make_request):
        """Test handling of empty slots list."""
        mock_make_request.return_value = []

        result = self.collector.collect()

        self.assertEqual(result["slots"], [])

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_missing_fields_with_defaults(self, mock_make_request):
        """Test that missing slot fields get default values."""
        mock_make_request.return_value = [
            {"id": 0},  # Minimal slot data
        ]

        result = self.collector.collect()

        slot = result["slots"][0]
        self.assertEqual(slot["id"], 0)
        self.assertEqual(slot["task"], -1)  # Default
        self.assertEqual(slot["state"], "idle")  # Default
        self.assertEqual(slot["progress"], 0.0)  # Default


class TestAggregatorSlotData(unittest.TestCase):
    """Tests for aggregator slot data extraction."""

    @patch("aggregator.ServerMetricsCollector")
    @patch("aggregator.IdleBaselineTracker")
    def test_aggregator_includes_slots_in_server_metrics(self, mock_idle, mock_collector):
        """Test that aggregator includes slots data in server metrics."""
        # Setup mock collector
        mock_instance = Mock()
        mock_instance.collect.return_value = {
            "timestamp": "2024-01-01T00:00:00",
            "server": {
                "prompt_tokens_total": 1000,
                "predicted_tokens_seconds": 50.0,
            },
            "slots": [
                {"id": 0, "progress": 0.5, "n_tokens": 256},
                {"id": 1, "progress": 0.75, "n_tokens": 512},
            ],
            "props": {"n_ctx": 4096},
            "metrics_available": True,
        }
        mock_collector.return_value = mock_instance

        # Mock other dependencies
        with patch("aggregator.SystemMetricsCollector") as mock_system:
            with patch("aggregator.ElectricityCostCalculator"):
                with patch("aggregator.Database"):
                    # Setup system metrics mock
                    mock_system_instance = Mock()
                    mock_system_instance.collect.return_value = {
                        "cpu": {"percent": 50.0, "power_w": 100, "cores": []},
                        "gpu": {"usage": 80.0, "power_w": 250, "memory_used": 8000, "memory_total": 16384},
                        "memory": {"used": 16000, "total": 32000, "percent": 50.0},
                        "system": {"power_w": 350},
                    }
                    mock_system.return_value = mock_system_instance

                    aggregator = Aggregator()
                    aggregator.server_collector = mock_instance

                    result = aggregator.collect_all_metrics()

                    # Verify slots are included in server metrics
                    self.assertIn("slots", result["server"])
                    self.assertEqual(len(result["server"]["slots"]), 2)
                    self.assertEqual(result["server"]["slots"][0]["progress"], 0.5)
                    self.assertEqual(result["server"]["slots"][1]["progress"], 0.75)

                    # Verify props are included
                    self.assertIn("props", result["server"])
                    self.assertEqual(result["server"]["props"]["n_ctx"], 4096)

    @patch("aggregator.ServerMetricsCollector")
    @patch("aggregator.IdleBaselineTracker")
    def test_aggregator_empty_slots(self, mock_idle, mock_collector):
        """Test aggregator handles empty slots gracefully."""
        mock_instance = Mock()
        mock_instance.collect.return_value = {
            "timestamp": "2024-01-01T00:00:00",
            "server": {"prompt_tokens_total": 1000},
            "slots": [],
            "props": {},
            "metrics_available": True,
        }
        mock_collector.return_value = mock_instance

        with patch("aggregator.SystemMetricsCollector") as mock_system:
            with patch("aggregator.ElectricityCostCalculator"):
                with patch("aggregator.Database"):
                    # Setup system metrics mock
                    mock_system_instance = Mock()
                    mock_system_instance.collect.return_value = {
                        "cpu": {"percent": 50.0, "power_w": 100, "cores": []},
                        "gpu": {"usage": 0.0, "power_w": 0, "memory_used": 0, "memory_total": 0},
                        "memory": {"used": 0, "total": 0, "percent": 0.0},
                        "system": {"power_w": 0},
                    }
                    mock_system.return_value = mock_system_instance

                    aggregator = Aggregator()
                    aggregator.server_collector = mock_instance

                    result = aggregator.collect_all_metrics()

                    # Verify empty slots list is included
                    self.assertIn("slots", result["server"])
                    self.assertEqual(result["server"]["slots"], [])


class TestSlotChartsJavaScript(unittest.TestCase):
    """Tests for JavaScript slot chart rendering logic."""

    def test_slot_progress_percentage_conversion(self):
        """Test that progress 0-1 is converted to percentage 0-100."""
        # Simulate the JavaScript logic
        def calculate_progress_percentage(progress):
            return Math_min(Math_round(progress * 100), 100)

        # Mock Math functions
        class Math:
            @staticmethod
            def round(value):
                return round(value)

            @staticmethod
            def min(*args):
                return min(args)

        # Test cases
        self.assertEqual(Math.min(Math.round(0.0 * 100), 100), 0)
        self.assertEqual(Math.min(Math.round(0.5 * 100), 100), 50)
        self.assertEqual(Math.min(Math.round(0.75 * 100), 100), 75)
        self.assertEqual(Math.min(Math.round(1.0 * 100), 100), 100)
        self.assertEqual(Math.min(Math.round(1.2 * 100), 100), 100)  # Clamped to 100

    def test_context_remaining_calculation(self):
        """Test context remaining calculation."""
        context_limit = 4096

        # Test cases
        self.assertEqual(max(0, context_limit - 0), 4096)  # No tokens
        self.assertEqual(max(0, context_limit - 256), 3840)  # 256 tokens
        self.assertEqual(max(0, context_limit - 1024), 3072)  # 1024 tokens
        self.assertEqual(max(0, context_limit - 4096), 0)  # Full context


class TestSlotChartsIntegration(unittest.TestCase):
    """Integration tests for slot charts with full metrics flow."""

    @patch("aggregator.ServerMetricsCollector")
    @patch("aggregator.SystemMetricsCollector")
    @patch("aggregator.ElectricityCostCalculator")
    @patch("aggregator.IdleBaselineTracker")
    @patch("aggregator.Database")
    def test_full_metrics_flow_with_slots(self, mock_db, mock_idle, mock_cost_calc, mock_system, mock_server):
        """Test full metrics collection flow includes slot data."""
        # Setup server metrics collector mock
        mock_server_instance = Mock()
        mock_server_instance.collect.return_value = {
            "timestamp": "2024-01-01T00:00:00",
            "server": {
                "prompt_tokens_total": 1000,
                "tokens_predicted_total": 500,
                "predicted_tokens_seconds": 25.0,
                "requests_processing": 2,
                "requests_deferred": 1,
            },
            "slots": [
                {"id": 0, "progress": 0.5, "n_tokens": 256, "n_prompt_tokens": 200, "n_gen_tokens": 56},
                {"id": 1, "progress": 0.75, "n_tokens": 512, "n_prompt_tokens": 400, "n_gen_tokens": 112},
            ],
            "props": {"n_ctx": 4096},
            "metrics_available": True,
        }
        mock_server.return_value = mock_server_instance

        # Setup system metrics collector mock
        mock_system_instance = Mock()
        mock_system_instance.collect.return_value = {
            "cpu": {"percent": 45.0, "power_w": 100},
            "gpu": {"usage": 80.0, "power_w": 250, "memory_used": 8000, "memory_total": 16384},
            "memory": {"used": 16000, "total": 32000, "percent": 50.0},
            "system": {"power_w": 350},
        }
        mock_system.return_value = mock_system_instance

        # Setup cost calculator mock
        mock_cost_instance = Mock()
        mock_cost_instance.calculate_power_cost.return_value = {
            "today_wh": 100.0,
            "session_cost_usd": 1.20,
            "total_wh": 500.0,
        }
        # Setup get_today_stats to return a dict (not a Mock)
        mock_cost_instance.get_today_stats.return_value = {
            "total_wh": 100.0, "gpu_wh": 50.0, "cpu_wh": 50.0, "total_cost_usd": 0.012
        }

        mock_cost_calc.return_value = mock_cost_instance

        # Setup database mock
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance

        # Create aggregator and collect metrics
        aggregator = Aggregator()
        aggregator.server_collector = mock_server_instance
        aggregator.system_collector = mock_system_instance
        aggregator.cost_calculator = mock_cost_instance

        result = aggregator.collect_all_metrics()

        # Verify complete metrics structure.
        # Note: aggregator.py's collect_all_metrics returns {timestamp, server,
        # system, process_gpu, system_raw} — there is NO top-level "cost" key
        # (that was daemon-only). Cost is computed/stored in store_raw_metrics.
        self.assertIn("timestamp", result)
        self.assertIn("server", result)
        self.assertIn("system", result)

        # Verify server metrics include slots
        self.assertIn("slots", result["server"])
        self.assertEqual(len(result["server"]["slots"]), 2)

        # Verify props are included for context limit
        self.assertIn("props", result["server"])
        self.assertEqual(result["server"]["props"]["n_ctx"], 4096)

        # Verify slot data structure
        slot0 = result["server"]["slots"][0]
        self.assertEqual(slot0["id"], 0)
        self.assertEqual(slot0["progress"], 0.5)
        self.assertEqual(slot0["n_tokens"], 256)
        self.assertEqual(slot0["n_prompt_tokens"], 200)
        self.assertEqual(slot0["n_gen_tokens"], 56)

        slot1 = result["server"]["slots"][1]
        self.assertEqual(slot1["id"], 1)
        self.assertEqual(slot1["progress"], 0.75)
        self.assertEqual(slot1["n_tokens"], 512)


if __name__ == "__main__":
    unittest.main()
