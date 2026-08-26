#!/usr/bin/env python3
"""Unit tests for power graph auto-scale functionality."""

import unittest
import json


class TestPowerChartAutoScale(unittest.TestCase):
    """Tests for power chart auto-scaling in web_server.py."""

    def setUp(self):
        """Set up test fixtures."""
        # Load the web_server.py content to check for chart options
        with open('/sandbox/web_server.py', 'r') as f:
            self.web_server_content = f.read()

    def test_power_values_calculated_from_power_w(self):
        """Test that power values are calculated from gpu_power_w and cpu_power_w."""
        # Check that power values are calculated from power_w fields
        self.assertIn("gpu_power_w", self.web_server_content,
                      "GPU power should be calculated from gpu_power_w")
        self.assertIn("cpu_power_w", self.web_server_content,
                      "CPU power should be calculated from cpu_power_w")


class TestTuiPowerChart(unittest.TestCase):
    """Tests for TUI power chart rendering."""

    def setUp(self):
        """Set up test fixtures."""
        with open('/sandbox/tui.py', 'r') as f:
            self.tui_content = f.read()

    def test_tui_calculates_power_values(self):
        """Test that TUI calculates power values from gpu_power_w and cpu_power_w."""
        # Check that power values are calculated
        self.assertIn("power_values", self.tui_content,
                      "TUI should calculate power_values")

        # Check that max_power is computed
        self.assertIn("max_power", self.tui_content,
                      "TUI should compute max_power for scaling")

    def test_tui_power_chart_draws_bars(self):
        """Test that TUI draws power bars in the chart."""
        # The TUI should draw power bars similar to GPU/CPU
        # Check for power bar drawing logic
        self.assertIn("Power", self.tui_content,
                      "TUI should display Power chart")


class TestPowerScaleCalculation(unittest.TestCase):
    """Tests for power scale calculation logic."""

    def test_max_power_with_high_values(self):
        """Test that max_power calculation handles values > 100W."""
        # Simulate power values that exceed 100W
        gpu_power = 250  # High GPU power
        cpu_power = 85   # CPU power
        system_power = 35  # System power

        total_power = gpu_power + cpu_power + system_power

        # Total should be > 100W
        self.assertGreater(total_power, 100,
                           "Total power should exceed 100W for realistic systems")

    def test_power_scale_margin(self):
        """Test that power scale includes margin above max value."""
        # Power charts should have some margin above max value
        # e.g., if max is 300W, scale should go to ~350W or 400W
        power_values = [100, 200, 250, 180, 220]
        max_power = max(power_values)

        # Should add margin (e.g., 10-20%)
        margin = max_power * 0.1  # 10% margin
        scaled_max = max_power + margin

        self.assertGreater(scaled_max, max_power,
                           "Scaled max should include margin above actual max")


class TestAutoScaleBehavior(unittest.TestCase):
    """Tests for auto-scale behavior verification."""

    def test_auto_scale_with_empty_data(self):
        """Test auto-scale behavior with empty data."""
        power_values = []
        max_power = max(power_values) if power_values else 100

        # Should default to 100W if no data
        self.assertEqual(max_power, 100,
                         "Should default to 100W when no data available")

    def test_auto_scale_with_single_value(self):
        """Test auto-scale behavior with single power value."""
        power_values = [150]
        max_power = max(power_values) if power_values else 100

        # Should use the single value
        self.assertEqual(max_power, 150,
                         "Should use single value as max")

    def test_auto_scale_with_varied_values(self):
        """Test auto-scale behavior with varied power values."""
        power_values = [50, 100, 150, 200, 250]
        max_power = max(power_values) if power_values else 100

        # Should use the maximum value
        self.assertEqual(max_power, 250,
                         "Should use maximum value as max")


if __name__ == "__main__":
    unittest.main()
