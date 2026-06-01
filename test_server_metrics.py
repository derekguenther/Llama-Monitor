#!/usr/bin/env python3
"""Unit tests for server_metrics.py."""

import unittest
from unittest.mock import Mock, patch

from server_metrics import ServerMetricsCollector, format_metrics_display


class TestServerMetricsCollector(unittest.TestCase):
    """Tests for ServerMetricsCollector."""

    def setUp(self):
        """Create a collector for testing."""
        self.collector = ServerMetricsCollector("http://localhost:8000")

    def test_init_strips_trailing_slash(self):
        """Test that init strips trailing slash from URL."""
        collector = ServerMetricsCollector("http://localhost:8000/")
        self.assertEqual(collector.server_url, "http://localhost:8000")

    @patch("server_metrics.requests.get")
    def test_make_request_success(self, mock_get):
        """Test successful HTTP request."""
        mock_response = Mock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = self.collector._make_request("/test")

        self.assertEqual(result, {"test": "data"})
        mock_get.assert_called_once_with("http://localhost:8000/test", timeout=5)

    @patch("server_metrics.requests.get")
    def test_make_request_failure(self, mock_get):
        """Test failed HTTP request."""
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("Connection error")

        result = self.collector._make_request("/test")

        self.assertIsNone(result)

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_get_metrics(self, mock_make_request):
        """Test getting metrics from /metrics endpoint."""
        mock_make_request.return_value = {"prompt_tokens_total": 1000}

        result = self.collector.get_metrics()

        self.assertEqual(result, {"prompt_tokens_total": 1000})
        mock_make_request.assert_called_once_with("/metrics")

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_get_slots(self, mock_make_request):
        """Test getting slots from /slots endpoint."""
        mock_make_request.return_value = [{"id": 1}]

        result = self.collector.get_slots()

        self.assertEqual(result, [{"id": 1}])
        mock_make_request.assert_called_once_with("/slots")

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_get_props(self, mock_make_request):
        """Test getting props from /props endpoint."""
        mock_make_request.return_value = {"model": "llama"}

        result = self.collector.get_props()

        self.assertEqual(result, {"model": "llama"})
        mock_make_request.assert_called_once_with("/props")

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_collect(self, mock_make_request):
        """Test collecting all metrics."""
        # Setup mock responses
        def mock_side_effect(endpoint):
            if endpoint == "/metrics":
                return {
                    "prompt_tokens_total": 1000,
                    "prompt_tokens_seconds": 50.0,
                    "tokens_predicted_total": 500,
                    "predicted_tokens_seconds": 25.0,
                    "requests_processing": 2,
                    "requests_deferred": 1,
                }
            elif endpoint == "/slots":
                return [
                    {"id": 1, "state": "processing", "progress": 0.5},
                    {"id": 2, "state": "idle", "progress": 0.0},
                ]
            elif endpoint == "/props":
                return {"model": "llama-7b"}
            return None

        mock_make_request.side_effect = mock_side_effect

        result = self.collector.collect()

        # Check structure
        self.assertIn("timestamp", result)
        self.assertIn("server", result)
        self.assertIn("slots", result)
        self.assertIn("props", result)

        # Check server metrics
        self.assertEqual(result["server"]["prompt_tokens_total"], 1000)
        self.assertEqual(result["server"]["requests_processing"], 2)

        # Check slots
        self.assertEqual(len(result["slots"]), 2)
        self.assertEqual(result["slots"][0]["state"], "processing")

        # Check props
        self.assertEqual(result["props"]["model"], "llama-7b")

    @patch("server_metrics.ServerMetricsCollector._make_request")
    def test_collect_partial_failure(self, mock_make_request):
        """Test collecting when some endpoints fail."""
        def mock_side_effect(endpoint):
            if endpoint == "/metrics":
                return {"prompt_tokens_total": 1000}
            elif endpoint == "/slots":
                return None  # This will fail
            elif endpoint == "/props":
                return {"model": "llama"}
            return None

        mock_make_request.side_effect = mock_side_effect

        result = self.collector.collect()

        # Should still have what succeeded
        self.assertIn("server", result)
        self.assertEqual(result["server"]["prompt_tokens_total"], 1000)
        self.assertEqual(result["props"]["model"], "llama")
        # Slots should be empty list when None
        self.assertEqual(result["slots"], [])


class TestParseMetrics(unittest.TestCase):
    """Tests for _parse_metrics method."""

    def setUp(self):
        self.collector = ServerMetricsCollector("http://localhost:8000")

    def test_parse_metrics_dict(self):
        """Test parsing dict-format metrics."""
        metrics = {
            "prompt_tokens_total": 1000,
            "prompt_tokens_seconds": 50.5,
            "requests_processing": 2,
        }

        result = self.collector._parse_metrics(metrics)

        self.assertEqual(result, metrics)

    def test_parse_metrics_string_prometheus(self):
        """Test parsing Prometheus-format string metrics."""
        metrics = """# HELP test metric
# TYPE test counter
prompt_tokens_total 1000
prompt_tokens_seconds 50.5
requests_processing 2
"""

        result = self.collector._parse_metrics(metrics)

        self.assertEqual(result["prompt_tokens_total"], 1000.0)
        self.assertEqual(result["prompt_tokens_seconds"], 50.5)
        self.assertEqual(result["requests_processing"], 2.0)

    def test_parse_metrics_string_with_comments(self):
        """Test parsing metrics with comment lines."""
        metrics = """# This is a comment
prompt_tokens_total 1000

# Another comment
requests_processing 2
"""

        result = self.collector._parse_metrics(metrics)

        self.assertEqual(result["prompt_tokens_total"], 1000.0)
        self.assertEqual(result["requests_processing"], 2.0)
        self.assertNotIn("# This is a comment", result)

    def test_parse_metrics_string_invalid_value(self):
        """Test parsing metrics with invalid values."""
        metrics = """prompt_tokens_total not_a_number
requests_processing 2
"""

        result = self.collector._parse_metrics(metrics)

        # Invalid value should be skipped
        self.assertNotIn("prompt_tokens_total", result)
        self.assertEqual(result["requests_processing"], 2.0)

    def test_parse_metrics_empty_string(self):
        """Test parsing empty metrics string."""
        result = self.collector._parse_metrics("")
        self.assertEqual(result, {})

    def test_parse_metrics_empty_dict(self):
        """Test parsing empty metrics dict."""
        result = self.collector._parse_metrics({})
        self.assertEqual(result, {})


class TestParseSlots(unittest.TestCase):
    """Tests for _parse_slots method."""

    def setUp(self):
        self.collector = ServerMetricsCollector("http://localhost:8000")

    def test_parse_slots_list(self):
        """Test parsing list of slots."""
        slots = [
            {
                "id": 1,
                "task": 100,
                "n_tokens": 50,
                "n_prompt_tokens": 30,
                "n_gen_tokens": 20,
                "progress": 0.5,
                "state": "processing",
                "prompt": "Hello",
                "generated": "World",
            },
            {
                "id": 2,
                "state": "idle",
            },
        ]

        result = self.collector._parse_slots(slots)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["state"], "processing")
        self.assertEqual(result[0]["progress"], 0.5)
        self.assertEqual(result[1]["id"], 2)
        self.assertEqual(result[1]["state"], "idle")

    def test_parse_slots_dict_single(self):
        """Test parsing single slot as dict."""
        slot = {"id": 1, "state": "processing"}

        result = self.collector._parse_slots(slot)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

    def test_parse_slots_empty_list(self):
        """Test parsing empty slot list."""
        result = self.collector._parse_slots([])
        self.assertEqual(result, [])

    def test_parse_slots_none(self):
        """Test parsing None slots."""
        result = self.collector._parse_slots(None)
        self.assertEqual(result, [])

    def test_parse_slots_missing_fields(self):
        """Test parsing slots with missing fields."""
        slots = [{"id": 1}]

        result = self.collector._parse_slots(slots)

        self.assertEqual(result[0]["id"], 1)
        # Missing fields should have defaults
        self.assertEqual(result[0]["task"], -1)
        self.assertEqual(result[0]["state"], "idle")
        self.assertEqual(result[0]["progress"], 0.0)


class TestFormatMetricsDisplay(unittest.TestCase):
    """Tests for format_metrics_display function."""

    def test_format_metrics_display_full(self):
        """Test formatting metrics with all data."""
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
            ],
        }

        result = format_metrics_display(metrics)

        self.assertIn("Prompt tokens:    1,000 (50/s)", result)
        self.assertIn("Generated:        500 (25/s)", result)
        self.assertIn("Requests:         2 processing", result)
        # Average progress: (0.5 + 0.0) / 2 = 0.25 = 25.0%
        self.assertIn("Active slots:     1/2 (25.0%)", result)

    def test_format_metrics_display_empty(self):
        """Test formatting empty metrics."""
        result = format_metrics_display({})

        self.assertEqual(result, "")

    def test_format_metrics_display_no_slots(self):
        """Test formatting metrics without slots."""
        metrics = {
            "server": {
                "prompt_tokens_total": 1000,
                "prompt_tokens_seconds": 50.0,
            }
        }

        result = format_metrics_display(metrics)

        self.assertIn("Prompt tokens:    1,000 (50/s)", result)
        self.assertNotIn("Active slots", result)

    def test_format_metrics_display_zero_values(self):
        """Test formatting metrics with zero values."""
        metrics = {
            "server": {
                "prompt_tokens_total": 0,
                "prompt_tokens_seconds": 0.0,
                "tokens_predicted_total": 0,
                "predicted_tokens_seconds": 0.0,
            },
            "slots": [],
        }

        result = format_metrics_display(metrics)

        self.assertIn("Prompt tokens:    0 (0/s)", result)
        # With empty slots, the "Active slots" line should not appear
        self.assertNotIn("Active slots", result)


if __name__ == "__main__":
    unittest.main()
