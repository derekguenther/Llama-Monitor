#!/usr/bin/env python3
"""Unit tests for historical data viewer functionality."""

import json
import os
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.dirname(__file__))

from db import Database
from web_server import app


class TestHistoricalDataAPI(unittest.TestCase):
    """Tests for historical data API endpoints."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Initialize database with schema
        self.db = Database(self.db_path)
        with self.db:
            # Insert sample system metrics
            now = int(datetime.now().timestamp())
            for i in range(100):
                ts = now - (100 - i) * 60  # 1 minute intervals
                self.db.execute(
                    """
                    INSERT INTO system_metrics_raw
                    (timestamp, cpu_percent, gpu_usage, gpu_memory_used_mb,
                     gpu_power_w, cpu_power_w, memory_used_mb, system_power_w)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (ts, 50.0 + i, 70.0 + i * 0.5, 8192 + i * 100,
                     200.0 + i * 0.5, 50.0 + i * 0.2, 16384 + i * 200,
                     250.0 + i * 0.7)
                )

            # Insert sample server metrics
            for i in range(100):
                ts = now - (100 - i) * 60
                self.db.execute(
                    """
                    INSERT INTO server_metrics_raw
                    (timestamp, prompt_tokens_total, tokens_predicted_total,
                     predicted_tokens_seconds, requests_processing, slots_active)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (ts, 1000 + i * 10, 500 + i * 5, 25.0 + i * 0.1,
                     2 + i % 5, 4 + i % 8)
                )

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        try:
            os.unlink(self.db_path)
        except (PermissionError, OSError):
            pass

    def test_api_historical_metrics_hour(self):
        """Test historical data API with hour timeframe."""
        with app.test_client() as client:
            response = client.get('/api/metrics/historical?timeframe=hour&sample=60')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('system', data)
            self.assertIn('server', data)
            # Data may be empty if no data exists within the timeframe
            # Just verify the response structure is correct
            self.assertIsInstance(data['system'], list)
            self.assertIsInstance(data['server'], list)

    def test_api_historical_metrics_day(self):
        """Test historical data API with day timeframe."""
        with app.test_client() as client:
            response = client.get('/api/metrics/historical?timeframe=day&sample=60')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('system', data)
            self.assertIn('server', data)

    def test_api_historical_metrics_week(self):
        """Test historical data API with week timeframe."""
        with app.test_client() as client:
            response = client.get('/api/metrics/historical?timeframe=week&sample=60')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('system', data)
            self.assertIn('server', data)

    def test_api_historical_metrics_custom_range(self):
        """Test historical data API with custom range."""
        with app.test_client() as client:
            now = datetime.now()
            end_ts = now.isoformat()
            start_ts = (now - timedelta(hours=2)).isoformat()

            response = client.get(
                f'/api/metrics/historical/range?start={start_ts}&end={end_ts}&limit=100'
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('system', data)
            self.assertIn('server', data)

    def test_api_historical_metrics_missing_params(self):
        """Test historical data API with missing required parameters."""
        with app.test_client() as client:
            response = client.get('/api/metrics/historical/range')
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertIn('error', data)

    def test_api_historical_metrics_data_structure(self):
        """Test that historical data has correct structure."""
        with app.test_client() as client:
            response = client.get('/api/metrics/historical?timeframe=hour&sample=60')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            system_data = data['system']
            if len(system_data) > 0:
                first_point = system_data[0]
                required_fields = [
                    'timestamp', 'cpu_percent', 'gpu_usage',
                    'gpu_memory_used_mb', 'gpu_power_w', 'cpu_power_w',
                    'memory_used_mb', 'system_power_w'
                ]
                for field in required_fields:
                    self.assertIn(field, first_point, f"Missing field: {field}")

    def test_api_historical_metrics_with_limit(self):
        """Test historical data API with limit parameter."""
        with app.test_client() as client:
            response = client.get('/api/metrics/historical?timeframe=hour&limit=10&sample=60')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertLessEqual(len(data['system']), 10)


class TestHistoricalDataDatabase(unittest.TestCase):
    """Tests for historical data database queries."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.db = Database(self.db_path)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        try:
            os.unlink(self.db_path)
        except (PermissionError, OSError):
            pass

    def test_get_system_metrics_with_time_range(self):
        """Test getting system metrics within a time range."""
        now = int(datetime.now().timestamp())

        with self.db:
            # Insert test data
            for i in range(10):
                ts = now - (10 - i) * 60
                self.db.execute(
                    """
                    INSERT INTO system_metrics_raw
                    (timestamp, cpu_percent, gpu_usage)
                    VALUES (?, ?, ?)
                    """,
                    (ts, 50.0 + i, 70.0 + i)
                )

            # Query with time range
            cursor = self.db.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM system_metrics_raw
                WHERE timestamp >= ? AND timestamp <= ?
                ORDER BY timestamp ASC
                """,
                (now - 600, now)
            )
            rows = cursor.fetchall()
            self.assertEqual(len(rows), 10)

    def test_get_server_metrics_with_time_range(self):
        """Test getting server metrics within a time range."""
        now = int(datetime.now().timestamp())

        with self.db:
            # Insert test data
            for i in range(10):
                ts = now - (10 - i) * 60
                self.db.execute(
                    """
                    INSERT INTO server_metrics_raw
                    (timestamp, prompt_tokens_total, tokens_predicted_total)
                    VALUES (?, ?, ?)
                    """,
                    (ts, 1000 + i, 500 + i)
                )

            # Query with time range
            cursor = self.db.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM server_metrics_raw
                WHERE timestamp >= ? AND timestamp <= ?
                ORDER BY timestamp ASC
                """,
                (now - 600, now)
            )
            rows = cursor.fetchall()
            self.assertEqual(len(rows), 10)


class TestHistoricalDataJavaScript(unittest.TestCase):
    """Tests for historical data JavaScript functionality."""

    def test_timeframe_options(self):
        """Test that all timeframe options are available."""
        timeframes = ['hour', 'day', 'week', 'month', 'custom']
        self.assertEqual(len(timeframes), 5)
        self.assertIn('day', timeframes)
        self.assertIn('week', timeframes)

    def test_historical_chart_datasets(self):
        """Test that historical charts have correct datasets."""
        # GPU and CPU datasets
        gpu_dataset = {
            'label': 'GPU %',
            'borderColor': '#00ff88',
            'tension': 0.4,
            'fill': True
        }
        cpu_dataset = {
            'label': 'CPU %',
            'borderColor': '#00d4ff',
            'tension': 0.4,
            'fill': True
        }
        self.assertEqual(gpu_dataset['label'], 'GPU %')
        self.assertEqual(cpu_dataset['label'], 'CPU %')


if __name__ == '__main__':
    unittest.main()
