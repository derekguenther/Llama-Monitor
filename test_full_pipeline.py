"""
Integration test: feed simulated data through the full pipeline
(aggregator → cache → web transform) and verify the output matches
what the frontend expects.
"""
import json, os, sys, time, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import unittest
from unittest.mock import MagicMock


class TestFullPipeline(unittest.TestCase):
    """Test the full data pipeline end-to-end."""

    def setUp(self):
        self.tmpdb = os.path.join(tempfile.gettempdir(), f"test_pipeline_{os.getpid()}.db")
        if os.path.exists(self.tmpdb):
            os.remove(self.tmpdb)

    def tearDown(self):
        if os.path.exists(self.tmpdb):
            os.remove(self.tmpdb)

    def _make_fake_system_metrics(self):
        """Simulate what SystemMetricsCollector.collect() returns (nested format)."""
        return {
            "cpu": {"percent": 25.0, "cores": [50.0, 0.0, 25.0, 0.0], "count": 4},
            "gpu": {
                "usage": 80.0,
                "memory_used": 4096,
                "memory_total": 8192,
                "temperature_c": 65.0,
                "fan_speed_rpm": 1500,
                "power_w": 120.0,
            },
            "memory": {"used": 16384, "total": 32768, "percent": 50.0, "available": 16384},
            "system": {"cpu_power_w": 45.0, "system_power_w": 65.0},
        }

    def test_full_pipeline_with_fake_data(self):
        """Feed fake data through the pipeline and verify web API output format."""
        from aggregator import Aggregator
        from web_server import _transform_metrics

        # Create aggregator with temp DB and fake llama.cpp URL
        agg = Aggregator(
            server_url="http://localhost:1",
            db_path=self.tmpdb,
            collect_metrics=True,
        )

        # Inject fake system collector so collect_metrics() returns our data
        mock_collector = MagicMock()
        mock_collector.collect.return_value = self._make_fake_system_metrics()
        agg.system_collector = mock_collector

        # Step 1: Collect metrics
        metrics = agg.collect_all_metrics()
        self.assertIn("timestamp", metrics)
        self.assertIn("server", metrics)
        self.assertIn("system", metrics)
        self.assertIn("system_raw", metrics)
        self.assertEqual(metrics["system"]["cpu_percent"], 25.0)
        # cpu_power_w comes from system.system.cpu_power_w
        self.assertEqual(metrics["system"]["cpu_power_w"], 45.0)
        self.assertEqual(metrics["system"]["gpu_usage"], 80.0)
        # gpu_power_w comes from gpu.power_w
        self.assertEqual(metrics["system"]["gpu_power_w"], 120.0)
        # system_power_w is the system total = GPU + CPU power (120 + 45)
        self.assertEqual(metrics["system"]["system_power_w"], 165.0)

        # Step 2: Store raw metrics (simulates DB write)
        agg.store_raw_metrics(metrics)

        # Step 3: Calculate cost
        cost = agg.calculate_cost()
        self.assertIn("session_cost_usd", cost,
            f"calculate_cost must return session_cost_usd, got keys: {list(cost.keys())}")
        self.assertIn("today_cost", cost,
            f"calculate_cost must return today_cost")
        self.assertIn("today_wh", cost,
            f"calculate_cost must return today_wh")
        self.assertIn("cost_rate", cost,
            f"calculate_cost must return cost_rate")

        # Step 4: Add cost to metrics (what llamamonitor.py does)
        metrics["cost"] = cost

        # Step 5: Transform (what web_server.py does on API call)
        transformed = _transform_metrics(metrics.copy())

        # Step 6: Verify output format matches frontend expectations
        # Frontend does: const system = data.system || {};
        system = transformed.get("system", {})
        self.assertIsInstance(system, dict,
            f"system should be a dict, got {type(system).__name__}: {system}")

        # Frontend does: const cpu = system.cpu || {};
        self.assertIn("cpu", system, f"system should have 'cpu' key")
        self.assertIn("gpu", system, f"system should have 'gpu' key")
        self.assertIn("memory", system, f"system should have 'memory' key")
        self.assertIn("system", system, f"system should have 'system' key (system_power)")

        # Frontend accesses system.cpu.percent
        cpu = system.get("cpu", {})
        self.assertIn("percent", cpu,
            f"cpu should have 'percent', got keys: {list(cpu.keys())}")
        self.assertEqual(cpu["percent"], 25.0)

        # Frontend accesses system.gpu.usage
        gpu = system.get("gpu", {})
        self.assertIn("usage", gpu,
            f"gpu should have 'usage', got keys: {list(gpu.keys())}")
        self.assertEqual(gpu["usage"], 80.0)

        # Frontend accesses system.gpu.power_w
        self.assertIn("power_w", gpu, f"gpu should have 'power_w'")
        self.assertIn("power_w", cpu, f"cpu should have 'power_w'")

        # Frontend accesses system.system.power_w (system-level power)
        sys_power = system.get("system", {})
        self.assertIn("power_w", sys_power,
            f"system should have 'power_w', got keys: {list(sys_power.keys())}")

        # Cost format
        c = transformed.get("cost", {})
        self.assertIsInstance(c, dict,
            f"cost should be a dict, got {type(c).__name__}: {c}")
        self.assertIn("session_cost_usd", c,
            f"cost should have 'session_cost_usd', got keys: {list(c.keys())}")
        self.assertIn("today_cost", c,
            f"cost should have 'today_cost'")
        self.assertIn("today_wh", c,
            f"cost should have 'today_wh'")

        # Frontend does: const sessionCost = cost.session_cost_usd ?? cost.total_cost ?? null;
        self.assertIsInstance(c.get("session_cost_usd"), (int, float),
            f"session_cost_usd should be number, got {type(c.get('session_cost_usd'))}")
        self.assertGreaterEqual(c["session_cost_usd"], 0)

        # Frontend does: const todayCost = cost.today_cost ?? null;
        self.assertIsInstance(c.get("today_cost"), (int, float),
            f"today_cost should be number, got {type(c.get('today_cost'))}")

        # Step 7: Verify JSON-serializable (frontend uses fetch/json)
        try:
            json.dumps(transformed)
        except (TypeError, ValueError) as e:
            self.fail(f"Output not JSON-serializable: {e}")

        agg.close()

    def test_pipeline_without_llama_server(self):
        """Test pipeline works even when llama.cpp server is unavailable."""
        from aggregator import Aggregator
        from web_server import _transform_metrics

        agg = Aggregator(
            server_url="http://localhost:1",
            db_path=self.tmpdb,
            collect_metrics=True,
        )

        # Inject fake system collector
        mock_collector = MagicMock()
        mock_collector.collect.return_value = self._make_fake_system_metrics()
        agg.system_collector = mock_collector

        metrics = agg.collect_all_metrics()
        self.assertIn("server", metrics)
        # Server data should have an error but not crash
        server = metrics.get("server", {})
        self.assertIn("error", server,
            "server should have error key when llama is down")

        # System data should still be present and correct
        self.assertEqual(metrics["system"]["cpu_percent"], 25.0)
        self.assertEqual(metrics["system"]["gpu_usage"], 80.0)
        self.assertEqual(metrics["system"]["cpu_power_w"], 45.0)
        self.assertEqual(metrics["system"]["gpu_power_w"], 120.0)
        self.assertEqual(metrics["system"]["system_power_w"], 165.0)

        # Full pipeline should still work
        agg.store_raw_metrics(metrics)
        cost = agg.calculate_cost()
        metrics["cost"] = cost
        transformed = _transform_metrics(metrics.copy())

        # Cost should still be valid
        c = transformed.get("cost", {})
        self.assertIsInstance(c, dict)
        self.assertIn("session_cost_usd", c)

        agg.close()

    def test_frontend_json_compatible(self):
        """Verify the final output is JSON-serializable."""
        from aggregator import Aggregator
        from web_server import _transform_metrics

        agg = Aggregator(
            server_url="http://localhost:1",
            db_path=self.tmpdb,
            collect_metrics=True,
        )
        mock_collector = MagicMock()
        mock_collector.collect.return_value = self._make_fake_system_metrics()
        agg.system_collector = mock_collector

        metrics = agg.collect_all_metrics()
        agg.store_raw_metrics(metrics)
        cost = agg.calculate_cost()
        metrics["cost"] = cost
        transformed = _transform_metrics(metrics.copy())

        try:
            json.dumps(transformed)
        except (TypeError, ValueError) as e:
            self.fail(f"Output not JSON-serializable: {e}")

        agg.close()


if __name__ == "__main__":
    unittest.main()
