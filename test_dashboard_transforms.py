#!/usr/bin/env python3
"""Unit tests for data transformation functions."""

import unittest
from test_dashboard_mapping import transform_value, get_nested_value


class TestDataTransformation(unittest.TestCase):
    
    def test_transform_width(self):
        """Test width transform converts number to percentage string."""
        self.assertEqual(transform_value(7.1, "width"), "7.1%")
        self.assertEqual(transform_value(0, "width"), "0%")
        self.assertEqual(transform_value(100, "width"), "100%")
    
    def test_transform_count_active(self):
        """Test count_active transform counts processing slots."""
        data = {
            "server": {
                "slots": [
                    {"state": "processing"},
                    {"state": "idle"},
                    {"state": "processing"}
                ]
            }
        }
        result = transform_value(None, "count_active", data)
        self.assertEqual(result, "2/3")
    
    def test_transform_count_active_empty(self):
        """Test count_active with no slots."""
        data = {"server": {"slots": []}}
        result = transform_value(None, "count_active", data)
        self.assertEqual(result, "0/0")
    
    def test_transform_mem_text(self):
        """Test mem_text transform formats memory as used/total MB."""
        data = {
            "system": {
                "gpu": {
                    "memory_used": 8192,
                    "memory_total": 16384
                }
            }
        }
        result = transform_value(None, "mem_text", data)
        self.assertEqual(result, "8192/16384 MB")
    
    def test_transform_mem_text_cpu_fallback(self):
        """Test mem_text falls back to system.memory paths."""
        data = {
            "system": {
                "memory_used": 4096,
                "memory_total": 8192
            }
        }
        result = transform_value(None, "mem_text", data)
        self.assertEqual(result, "4096/8192 MB")
    
    def test_transform_mem_bar(self):
        """Test mem_bar transform calculates memory percentage."""
        data = {
            "system": {
                "gpu": {
                    "memory_used": 4096,
                    "memory_total": 16384
                }
            }
        }
        result = transform_value(None, "mem_bar", data)
        self.assertEqual(result, "25.0%")
    
    def test_transform_mem_bar_zero_total(self):
        """Test mem_bar handles zero total memory."""
        data = {
            "system": {
                "gpu": {
                    "memory_used": 0,
                    "memory_total": 0
                }
            }
        }
        result = transform_value(None, "mem_bar", data)
        self.assertEqual(result, "0%")
    
    def test_transform_mem_bar_cpu_fallback(self):
        """Test mem_bar falls back to system.memory paths."""
        data = {
            "system": {
                "memory_used": 2048,
                "memory_total": 8192
            }
        }
        result = transform_value(None, "mem_bar", data)
        self.assertEqual(result, "25.0%")
    
    def test_transform_sum_power(self):
        """Test sum transform adds GPU and CPU power."""
        data = {
            "system": {
                "gpu": {
                    "power_w": 150
                },
                "cpu": {
                    "power_w": 65
                }
            }
        }
        result = transform_value(None, "sum", data)
        self.assertEqual(result, 215)
    
    def test_transform_sum_with_null(self):
        """Test sum transform handles null values."""
        data = {
            "system": {
                "gpu": {
                    "power_w": None
                },
                "cpu": {
                    "power_w": 65
                }
            }
        }
        result = transform_value(None, "sum", data)
        self.assertEqual(result, 65)
    
    def test_transform_sum_with_minus_one(self):
        """Test sum transform handles -1 sentinel values (should add them)."""
        data = {
            "system": {
                "gpu": {
                    "power_w": -1
                },
                "cpu": {
                    "power_w": -1
                }
            }
        }
        result = transform_value(None, "sum", data)
        self.assertEqual(result, -2)
    
    def test_transform_noop(self):
        """Test that None transform returns value unchanged."""
        self.assertEqual(transform_value(42, None), 42)
        self.assertEqual(transform_value("test", None), "test")
        self.assertIsNone(transform_value(None, None))
    
    def test_get_nested_value_simple(self):
        """Test simple nested value retrieval."""
        data = {"server": {"prompt_tokens_total": 100}}
        self.assertEqual(get_nested_value(data, "server.prompt_tokens_total"), 100)
    
    def test_get_nested_value_missing(self):
        """Test missing nested value returns None."""
        data = {"server": {"prompt_tokens_total": 100}}
        self.assertIsNone(get_nested_value(data, "server.missing_key"))
        self.assertIsNone(get_nested_value(data, "missing.root"))
    
    def test_get_nested_value_null(self):
        """Test null value returns None."""
        data = {"server": {"prompt_tokens_total": None}}
        self.assertIsNone(get_nested_value(data, "server.prompt_tokens_total"))


class TestNegativeOneDetection(unittest.TestCase):
    """Test that -1 values are properly detected in data."""
    
    def test_find_negative_one_in_dict(self):
        """Test -1 detection in dictionary."""
        from test_api_data_integrity import find_negative_one_values
        data = {"system": {"gpu": {"power_w": -1}}}
        result = find_negative_one_values(data)
        self.assertEqual(result, ["system.gpu.power_w"])
    
    def test_find_negative_one_in_list(self):
        """Test -1 detection in list."""
        from test_api_data_integrity import find_negative_one_values
        data = {"server": {"slots": [{"task": -1}, {"task": 5}]}}
        result = find_negative_one_values(data)
        self.assertEqual(result, ["server.slots[0].task"])
    
    def test_find_negative_one_nested(self):
        """Test -1 detection in deeply nested structure."""
        from test_api_data_integrity import find_negative_one_values
        data = {
            "cost": {
                "today_cost": -1,
                "today_wh": -1
            }
        }
        result = find_negative_one_values(data)
        self.assertEqual(len(result), 2)
        self.assertIn("cost.today_cost", result)
        self.assertIn("cost.today_wh", result)
    
    def test_no_negative_one(self):
        """Test that valid data passes."""
        from test_api_data_integrity import find_negative_one_values
        data = {
            "server": {"prompt_tokens_total": 100},
            "system": {"cpu": {"percent": 50}},
            "cost": {"today_cost": 0.01}
        }
        result = find_negative_one_values(data)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
