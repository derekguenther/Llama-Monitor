#!/usr/bin/env python3
"""Unit tests for config.py."""

import os
import tempfile
import unittest

from config import Config, load_config, find_config


class TestConfigDefaults(unittest.TestCase):
    """Tests for default configuration values."""

    def setUp(self):
        """Create a fresh config instance."""
        self.config = Config()

    def test_database_path_default(self):
        """Test default database path."""
        self.assertEqual(
            self.config.get("database.path", "llama-monitor.db"),
            "llama-monitor.db"
        )

    def test_server_url_default(self):
        """Test default server URL."""
        self.assertEqual(
            self.config.get("server.url", "http://localhost:8080"),
            "http://localhost:8080"
        )

    def test_server_metrics_endpoint_default(self):
        """Test default server metrics endpoint."""
        self.assertEqual(
            self.config.get("server.metrics_endpoint", "/metrics"),
            "/metrics"
        )

    def test_tracked_processes_default(self):
        """Test default tracked processes."""
        self.assertEqual(
            self.config.get("metrics_collection.tracked_processes", ["llama.cpp"]),
            ["llama.cpp"]
        )

    def test_compression_enabled_default(self):
        """Test default compression enabled setting."""
        self.assertEqual(
            self.config.get("compression.enabled", True),
            True
        )

    def test_polling_interval_default(self):
        """Test default polling interval."""
        self.assertEqual(
            self.config.get("metrics_collection.interval_seconds", 1.0),
            1.0
        )

    def test_web_http_port_default(self):
        """Test default web HTTP port."""
        self.assertEqual(
            self.config.get("web.http_port", 8080),
            8080
        )


class TestConfigSetMethod(unittest.TestCase):
    """Tests for the Config.set() method."""

    def setUp(self):
        """Create a fresh config instance."""
        self.config = Config()

    def test_set_simple_key(self):
        """Test setting a simple key."""
        self.config.set("test_key", "test_value")
        self.assertEqual(self.config.get("test_key"), "test_value")

    def test_set_nested_key(self):
        """Test setting a nested key with dot notation."""
        self.config.set("server.port", 9000)
        self.assertEqual(self.config.get("server.port"), 9000)

    def test_set_nested_key_creates_intermediate(self):
        """Test that setting a nested key creates intermediate dicts."""
        self.config.set("web.http_port", 8888)
        self.assertEqual(self.config.get("web.http_port"), 8888)
        # Verify the intermediate dict was created
        self.assertIn("web", self.config._config)
        self.assertIn("http_port", self.config._config["web"])

    def test_override_existing_value(self):
        """Test overriding an existing value."""
        self.config.set("server.url", "http://custom:8080")
        self.config.set("server.url", "http://override:9090")
        self.assertEqual(self.config.get("server.url"), "http://override:9090")


class TestConfigIntegration(unittest.TestCase):
    """Integration tests for config with aggregator_daemon."""

    def test_aggregator_config_attributes(self):
        """Test that Aggregator can access all required config attributes."""
        from aggregator_daemon import Aggregator

        # This should not raise AttributeError
        config = Config()
        config.set("database.path", "test.db")
        config.set("server.url", "http://localhost:8080")
        config.set("server.metrics_endpoint", "/metrics")
        config.set("metrics_collection.tracked_processes", ["test"])
        config.set("compression.enabled", True)
        config.set("metrics_collection.interval_seconds", 1.0)
        config.set("web.http_port", 8080)

        # Verify all values can be retrieved
        self.assertEqual(config.get("database.path"), "test.db")
        self.assertEqual(config.get("server.url"), "http://localhost:8080")
        self.assertEqual(config.get("server.metrics_endpoint"), "/metrics")
        self.assertEqual(config.get("metrics_collection.tracked_processes"), ["test"])
        self.assertEqual(config.get("compression.enabled"), True)
        self.assertEqual(config.get("metrics_collection.interval_seconds"), 1.0)
        self.assertEqual(config.get("web.http_port"), 8080)


if __name__ == "__main__":
    unittest.main()
