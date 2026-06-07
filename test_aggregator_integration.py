#!/usr/bin/env python3
"""Integration tests for aggregator.py.

These tests verify the integration between Aggregator and its dependencies:
- ServerMetricsCollector
- SystemMetricsCollector
- ElectricityCostCalculator
- Database
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(__file__))

from aggregator import Aggregator
from db import Database


class TestAggregatorIntegration(unittest.TestCase):
    """Integration tests for Aggregator."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        """Clean up temporary database."""
        try:
            if os.path.exists(self.db_path):
                os.unlink(self.db_path)
        except (PermissionError, OSError):
            # File may be in use on Windows - skip cleanup
            pass

    def test_init_creates_all_components(self):
        """Test that Aggregator initializes all components correctly."""
        aggregator = Aggregator(
            server_url="http://localhost:8000",
            db_path=self.db_path,
            idle_baseline_w=150.0,
            cost_rate=0.12,
            collect_metrics=True
        )

        # Verify all components are initialized
        self.assertIsNotNone(aggregator.db)
        self.assertIsNotNone(aggregator.server_collector)
        self.assertIsNotNone(aggregator.system_collector)
        self.assertIsNotNone(aggregator.cost_calculator)

        # Verify server_collector has correct collect_metrics setting
        self.assertTrue(aggregator.server_collector.collect_metrics)

        aggregator.close()

    def test_init_with_metrics_disabled(self):
        """Test that Aggregator works with metrics collection disabled."""
        aggregator = Aggregator(
            server_url="http://localhost:8000",
            db_path=self.db_path,
            idle_baseline_w=150.0,
            cost_rate=0.12,
            collect_metrics=False
        )

        self.assertIsNotNone(aggregator.db)
        self.assertIsNotNone(aggregator.server_collector)
        self.assertFalse(aggregator.server_collector.collect_metrics)

        aggregator.close()

    def test_collect_all_metrics_integration(self):
        """Test that collect_all_metrics integrates with real collectors."""
        # Use real collectors but mock the actual HTTP calls
        with patch('aggregator.ServerMetricsCollector._make_request') as mock_request, \
             patch('aggregator.SystemMetricsCollector.collect') as mock_system:

            # Setup server metrics mock - this is what ServerMetricsCollector.collect() returns
            mock_request.return_value = {
                "prompt_tokens_total": 1000,
                "prompt_tokens_seconds": 50.0,
                "tokens_predicted_total": 500,
                "predicted_tokens_seconds": 25.0,
                "requests_processing": 2,
                "requests_deferred": 1,
            }

            # Setup system metrics mock
            mock_system.return_value = {
                "timestamp": 1234567890,
                "cpu": {"percent": 50.0, "cores": [], "process_cpu": {}},
                "gpu": {"usage": 80.0, "memory_used": 8192, "memory_total": 16384,
                        "temperature_c": 75, "fan_speed_rpm": 2500, "power_w": 250.0},
                "memory": {"used": 16384, "total": 32768, "percent": 50.0},
                "system": {"system_power_w": 300.0},
                "process_gpu": {},
            }

            aggregator = Aggregator(
                server_url="http://localhost:8000",
                db_path=self.db_path,
                idle_baseline_w=150.0,
                cost_rate=0.12
            )

            result = aggregator.collect_all_metrics()

            # Verify result structure
            self.assertIn("timestamp", result)
            self.assertIn("server", result)
            self.assertIn("system", result)

            # Verify server metrics - result["server"] contains the output of ServerMetricsCollector.collect()
            server = result.get("server", {})
            self.assertEqual(server.get("server", {}).get("prompt_tokens_total"), 1000)

            aggregator.close()

    def test_store_raw_metrics_integration(self):
        """Test that store_raw_metrics stores data to database."""
        with patch('aggregator.ServerMetricsCollector._make_request') as mock_request, \
             patch('aggregator.SystemMetricsCollector.collect') as mock_system:

            # Setup server metrics mock
            mock_request.return_value = {
                "prompt_tokens_total": 1000,
                "prompt_tokens_seconds": 50.0,
                "tokens_predicted_total": 500,
                "predicted_tokens_seconds": 25.0,
                "requests_processing": 2,
                "requests_deferred": 1,
            }

            # Setup system metrics mock - note: column names match db.py schema
            mock_system.return_value = {
                "cpu": {"percent": 50.0, "cores": [10.0, 20.0], "process_cpu": {}},
                "gpu": {"usage": 80.0, "memory_used": 8192, "memory_total": 16384,
                        "temperature_c": 75, "fan_speed_rpm": 2500, "power_w": 250.0},
                "memory": {"used": 16384, "total": 32768, "percent": 50.0},
                "system": {"system_power_w": 300.0},
                "process_gpu": {},
            }

            aggregator = Aggregator(
                server_url="http://localhost:8000",
                db_path=self.db_path,
                idle_baseline_w=150.0,
                cost_rate=0.12
            )

            metrics = aggregator.collect_all_metrics()
            aggregator.store_raw_metrics(metrics)

            # Verify data was stored by querying the database directly
            db = Database(self.db_path)
            db.connect()
            cursor = db.conn.cursor()

            # Get the timestamp that was actually stored
            cursor.execute("SELECT DISTINCT timestamp FROM server_metrics_raw")
            stored_timestamps = [row[0] for row in cursor.fetchall()]
            self.assertEqual(len(stored_timestamps), 1, "Should have exactly one timestamp")

            # Query the raw table directly using the actual timestamp
            cursor.execute("SELECT * FROM server_metrics_raw WHERE timestamp = ?", (stored_timestamps[0],))
            server_metrics = [dict(row) for row in cursor.fetchall()]

            cursor.execute("SELECT * FROM system_metrics_raw WHERE timestamp = ?", (stored_timestamps[0],))
            system_metrics = [dict(row) for row in cursor.fetchall()]

            self.assertEqual(len(server_metrics), 1)
            self.assertEqual(server_metrics[0]["prompt_tokens_total"], 1000)

            self.assertEqual(len(system_metrics), 1)
            self.assertEqual(system_metrics[0]["cpu_percent"], 50.0)

            db.close()
            aggregator.close()

    def test_full_integration_with_real_components(self):
        """Test full integration with real components (no mocks)."""
        aggregator = Aggregator(
            server_url="http://localhost:8000",
            db_path=self.db_path,
            idle_baseline_w=150.0,
            cost_rate=0.12,
            collect_metrics=False  # Disable to avoid connection errors
        )

        # Verify components are properly connected
        self.assertEqual(aggregator.server_collector.server_url, "http://localhost:8000")
        self.assertEqual(aggregator.server_collector.metrics_endpoint, "/metrics")
        # ElectricityCostCalculator stores db as self.database
        self.assertEqual(aggregator.cost_calculator.database, aggregator.db)

        aggregator.close()

    def test_context_manager(self):
        """Test that Aggregator works as a context manager."""
        with Aggregator(
            server_url="http://localhost:8000",
            db_path=self.db_path,
            idle_baseline_w=150.0,
            cost_rate=0.12
        ) as aggregator:
            self.assertIsNotNone(aggregator.db)
            self.assertIsNotNone(aggregator.server_collector)

        aggregator.close()  # Safe to call again


class TestAggregatorWithDatabase(unittest.TestCase):
    """Tests for Aggregator database integration."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        """Clean up temporary database."""
        try:
            if os.path.exists(self.db_path):
                os.unlink(self.db_path)
        except (PermissionError, OSError):
            pass

    def test_aggregator_creates_database_schema(self):
        """Test that Aggregator creates the database schema."""
        aggregator = Aggregator(
            server_url="http://localhost:8000",
            db_path=self.db_path,
            idle_baseline_w=150.0,
            cost_rate=0.12
        )

        # Database should exist after Aggregator initialization
        self.assertTrue(os.path.exists(self.db_path))

        # Verify schema tables exist by querying the database directly
        db = Database(self.db_path)
        db.connect()
        cursor = db.conn.cursor()

        # Check for expected tables
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]

        expected_tables = [
            "schema_version",
            "server_metrics_raw",
            "system_metrics_raw",
            "process_cpu_metrics_raw",
            "process_gpu_metrics_raw",
        ]

        for table in expected_tables:
            self.assertIn(table, tables)

        db.close()
        aggregator.close()


class TestDependencyChecking(unittest.TestCase):
    """Tests for dependency checking functionality."""

    def test_ensure_dependencies_no_missing(self):
        """Test ensure_dependencies when all deps are installed."""
        from main import ensure_dependencies

        # This should not raise or prompt since all deps are installed
        ensure_dependencies()

    def test_ensure_dependencies_with_tui_flag(self):
        """Test ensure_dependencies with check_tui=True."""
        from main import ensure_dependencies

        # This should check for curses but not fail if not on Windows
        ensure_dependencies(check_tui=True)


if __name__ == "__main__":
    unittest.main()
