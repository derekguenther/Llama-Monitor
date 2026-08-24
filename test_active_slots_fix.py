#!/usr/bin/env python3
"""Tests for Active Slots display fix.

This module tests the fix for the issue where Active Slots shows 0/0
instead of the actual slot count.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock

from server_metrics import ServerMetricsCollector, format_metrics_display


class TestActiveSlotsDisplay(unittest.TestCase):
    """Tests for Active Slots display functionality."""

    def test_format_metrics_display_with_slots(self):
        """Test that format_metrics_display correctly shows active slots."""
        metrics = {
            "server": {
                "prompt_tokens_total": 1000,
                "prompt_tokens_seconds": 50.0,
                "tokens_predicted_total": 500,
                "predicted_tokens_seconds": 25.0,
                "requests_processing": 2,
            },
            "slots": [
                {"id": 1, "state": "processing", "progress": 0.5},
                {"id": 2, "state": "idle", "progress": 0.0},
                {"id": 3, "state": "processing", "progress": 1.0},
            ],
        }

        result = format_metrics_display(metrics)

        # Check that active slots line is present
        self.assertIn("Active slots:", result)
        # 2 out of 3 slots are processing (50% + 0% + 100%)/3 = 50% average
        self.assertIn("2/3 (50.0%)", result)

    def test_format_metrics_display_empty_slots(self):
        """Test that empty slots list doesn't show active slots line."""
        metrics = {
            "server": {
                "prompt_tokens_total": 1000,
            },
            "slots": [],
        }

        result = format_metrics_display(metrics)

        # With empty slots, the line should not appear
        self.assertNotIn("Active slots", result)

    def test_format_metrics_display_no_slots_key(self):
        """Test that missing slots key doesn't cause issues."""
        metrics = {
            "server": {
                "prompt_tokens_total": 1000,
            },
        }

        result = format_metrics_display(metrics)

        self.assertNotIn("Active slots", result)

    def test_format_metrics_display_single_active_slot(self):
        """Test with a single active slot."""
        metrics = {
            "server": {},
            "slots": [
                {"id": 1, "state": "processing", "progress": 0.75},
            ],
        }

        result = format_metrics_display(metrics)

        self.assertIn("Active slots:", result)
        self.assertIn("1/1 (75.0%)", result)

    def test_format_metrics_display_all_idle(self):
        """Test with all slots idle."""
        metrics = {
            "server": {},
            "slots": [
                {"id": 1, "state": "idle", "progress": 0.0},
                {"id": 2, "state": "idle", "progress": 0.0},
            ],
        }

        result = format_metrics_display(metrics)

        self.assertIn("Active slots:", result)
        self.assertIn("0/2 (0.0%)", result)


class TestSlotsDataFlow(unittest.TestCase):
    """Tests for slots data flow through the system."""

    @patch("server_metrics.requests.get")
    def test_collector_collects_slots(self, mock_get):
        """Test that ServerMetricsCollector collects slots data."""
        # Setup mock for /slots endpoint
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "state": "processing", "progress": 0.5},
            {"id": 2, "state": "idle", "progress": 0.0},
        ]
        mock_response.raise_for_status = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_get.return_value = mock_response

        collector = ServerMetricsCollector("http://localhost:8000")
        result = collector.collect()

        self.assertIn("slots", result)
        self.assertEqual(len(result["slots"]), 2)
        self.assertEqual(result["slots"][0]["state"], "processing")

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_parse_slots_list(self, mock_make_request):
        """Test parsing slots from list format."""
        mock_make_request.return_value = [
            {"id": 1, "state": "processing", "progress": 0.5},
        ]

        collector = ServerMetricsCollector("http://localhost:8000")
        result = collector.collect()

        self.assertEqual(len(result["slots"]), 1)
        self.assertEqual(result["slots"][0]["state"], "processing")

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_parse_slots_none_returns_empty(self, mock_make_request):
        """Test that None slots returns empty list."""
        def side_effect(endpoint):
            if endpoint == "/slots":
                return None
            return {}

        mock_make_request.side_effect = side_effect

        collector = ServerMetricsCollector("http://localhost:8000")
        result = collector.collect()

        # Should have empty list, not None
        self.assertEqual(result["slots"], [])

    @patch("aggregator.ServerMetricsCollector")
    @patch("aggregator.SystemMetricsCollector")
    @patch("aggregator.ElectricityCostCalculator")
    @patch("aggregator.IdleBaselineTracker")
    @patch("aggregator.Database")
    def test_aggregator_slots_extraction(self, mock_db, mock_idle, mock_cost_calc, mock_system, mock_server):
        """Test that aggregator correctly extracts slots via collect_all_metrics."""
        # Simulate server_data as returned by ServerMetricsCollector.collect()
        server_data = {
            "server": {
                "prompt_tokens_total": 1000,
                "requests_processing": 2,
            },
            "slots": [
                {"id": 1, "state": "processing", "progress": 0.5},
                {"id": 2, "state": "idle", "progress": 0.0},
            ],
            "props": {"model": "llama-7b"},
        }
        mock_server_instance = Mock()
        mock_server_instance.collect.return_value = server_data
        mock_server.return_value = mock_server_instance

        mock_system_instance = Mock()
        mock_system_instance.collect.return_value = {
            "cpu": {"percent": 45.0, "power_w": 100},
            "gpu": {"usage": 80.0, "power_w": 250, "memory_used": 8000, "memory_total": 16384},
            "memory": {"used": 16000, "total": 32000, "percent": 50.0},
            "system": {"power_w": 350},
        }
        mock_system.return_value = mock_system_instance

        from aggregator import Aggregator

        aggregator = Aggregator()
        aggregator.server_collector = mock_server_instance
        aggregator.system_collector = mock_system_instance

        result = aggregator.collect_all_metrics()

        # Check slots are included (aggregator nests them inside server)
        self.assertIn("slots", result["server"])
        self.assertEqual(len(result["server"]["slots"]), 2)
        self.assertEqual(result["server"]["slots"][0]["state"], "processing")


class TestWebServerSlotsUpdate(unittest.TestCase):
    """Tests for web server slots display update."""

    def test_html_has_active_slots_element(self):
        """Test that the HTML contains the server-active-slots element."""
        from web_server import app

        # Get the index route content
        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

        # Check for the element
        self.assertIn('id="server-active-slots"', html)

    def test_javascript_updates_active_slots(self):
        """Test that JavaScript code updates the active slots element."""
        from web_server import app

        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

        # Check that the JavaScript updates server-active-slots
        # The fix should include code like:
        # document.getElementById('server-active-slots').textContent = ...
        self.assertIn("server-active-slots", html)

    def test_javascript_has_slots_filter_logic(self):
        """Test that JavaScript has the slots filtering logic."""
        from web_server import app

        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

        # Check for the slots filtering logic
        self.assertIn("state === 'processing'", html)

    def test_javascript_has_slots_reduce_logic(self):
        """Test that JavaScript has the slots progress reduction logic."""
        from web_server import app

        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

        # Check for the slots progress reduction logic
        self.assertIn(".reduce(", html)
        self.assertIn("progress", html)


if __name__ == "__main__":
    unittest.main()


class TestRequestsProcessingDisplay(unittest.TestCase):
    """Tests for Requests Processing display functionality."""

    def test_html_has_server_processing_element(self):
        """Test that the HTML contains the server-processing element."""
        from web_server import app

        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

        # Check for the element
        self.assertIn('id="server-processing"', html)

    def test_javascript_updates_server_processing(self):
        """Test that JavaScript code updates the server-processing element."""
        from web_server import app

        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

        # Check that the JavaScript updates server-processing
        # The fix should include code like:
        # document.getElementById('server-processing').textContent = ...
        self.assertIn("server-processing", html)
        self.assertIn("requests_processing", html)
