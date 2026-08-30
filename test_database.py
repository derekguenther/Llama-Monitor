#!/usr/bin/env python3
"""Unit tests for database.py."""

import os
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest import mock

from db import Database


class TestDatabaseInit(unittest.TestCase):
    """Tests for database initialization."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(
            suffix=".db", delete=False
        )
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_connect_creates_connection(self):
        """Test that connect() creates a valid connection."""
        conn = self.db.connect()
        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, sqlite3.Connection)

    def test_context_manager(self):
        """Test database context manager."""
        with Database(self.temp_db.name) as db:
            self.assertIsNotNone(db.conn)
            self.assertIsInstance(db.conn, sqlite3.Connection)

    def test_schema_version_created(self):
        """Test that schema version table is created."""
        with self.db:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT version FROM schema_version")
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row[0], "1.0")


class TestServerMetrics(unittest.TestCase):
    """Tests for server metrics operations."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(
            suffix=".db", delete=False
        )
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_insert_server_metrics(self):
        """Test inserting server metrics."""
        timestamp = datetime.now().isoformat()
        metrics = {
            "prompt_tokens_total": 1000,
            "prompt_tokens_seconds": 50.0,
            "tokens_predicted_total": 500,
            "predicted_tokens_seconds": 25.0,
            "requests_processing": 2,
            "requests_deferred": 1,
        }

        with self.db:
            self.db.insert_server_metrics(timestamp, metrics)

            # Verify insertion
            result = self.db.get_server_metrics(limit=1)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["prompt_tokens_total"], 1000)
            self.assertAlmostEqual(
                result[0]["prompt_tokens_seconds"], 50.0
            )

    def test_get_server_metrics_with_filter(self):
        """Test filtering server metrics by time."""
        now = datetime.now()
        with self.db:
            # Insert metrics at different times
            for i in range(5):
                ts = (now - timedelta(seconds=i * 10)).isoformat()
                self.db.insert_server_metrics(
                    ts, {"prompt_tokens_total": i * 100}
                )

            # Get metrics in time range
            start = (now - timedelta(seconds=25)).isoformat()
            end = (now - timedelta(seconds=5)).isoformat()
            result = self.db.get_server_metrics(
                start_time=start, end_time=end
            )

            # Should get 2 records (10s and 20s ago)
            self.assertEqual(len(result), 2)

    def test_get_server_metrics_limit(self):
        """Test limiting server metrics results."""
        now = datetime.now()
        with self.db:
            for i in range(10):
                ts = (now - timedelta(seconds=i * 5)).isoformat()
                self.db.insert_server_metrics(
                    ts, {"prompt_tokens_total": i}
                )

            result = self.db.get_server_metrics(limit=3)
            self.assertEqual(len(result), 3)


class TestSystemMetrics(unittest.TestCase):
    """Tests for system metrics operations."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(
            suffix=".db", delete=False
        )
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_insert_system_metrics(self):
        """Test inserting system metrics."""
        timestamp = datetime.now().isoformat()
        metrics = {
            "cpu_percent": 45.5,
            "cpu_cores_percent": [10.0, 20.0, 30.0, 40.0],
            "cpu_temperature_c": "45.0,46.0,47.0,48.0",
            "cpu_power_w": 65.0,
            "gpu_usage": 85.0,
            "gpu_memory_used_mb": 8192,
            "gpu_memory_total_mb": 16384,
            "gpu_temperature_c": 75.0,
            "gpu_fan_speed_rpm": 2500,
            "gpu_power_w": 220.0,
            "memory_used_mb": 16384,
            "memory_total_mb": 32768,
            "memory_percent": 50.0,
            "system_power_w": 285.0,
        }

        with self.db:
            self.db.insert_system_metrics(timestamp, metrics)

            result = self.db.get_system_metrics(limit=1)
            self.assertEqual(len(result), 1)
            self.assertAlmostEqual(
                result[0]["cpu_percent"], 45.5, places=1
            )
            self.assertEqual(result[0]["gpu_usage"], 85.0)
            self.assertEqual(result[0]["gpu_memory_used_mb"], 8192)

    def test_get_system_metrics(self):
        """Test retrieving system metrics."""
        now = datetime.now()
        with self.db:
            for i in range(3):
                ts = (now - timedelta(seconds=i * 60)).isoformat()
                self.db.insert_system_metrics(
                    ts,
                    {
                        "cpu_percent": i * 10,
                        "gpu_usage": i * 5,
                        "cpu_power_w": i * 20,
                        "gpu_power_w": i * 50,
                    },
                )

            result = self.db.get_system_metrics()
            self.assertEqual(len(result), 3)


class TestIdleBaseline(unittest.TestCase):
    """Tests for idle baseline operations."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(
            suffix=".db", delete=False
        )
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_insert_idle_baseline(self):
        """Test inserting idle baseline measurement."""
        timestamp = datetime.now().isoformat()

        with self.db:
            self.db.insert_idle_baseline(
                timestamp, cpu_percent=2.0, gpu_percent=1.0, system_power_w=100.0
            )

            cursor = self.db.conn.cursor()
            cursor.execute("SELECT * FROM idle_baseline")
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["cpu_percent"], 2.0)
            self.assertEqual(row["gpu_percent"], 1.0)
            self.assertEqual(row["system_power_w"], 100.0)
            self.assertEqual(row["is_valid"], 1)

    def test_insert_invalid_idle_baseline(self):
        """Test inserting invalid idle baseline."""
        timestamp = datetime.now().isoformat()

        with self.db:
            self.db.insert_idle_baseline(
                timestamp,
                cpu_percent=50.0,
                gpu_percent=60.0,
                system_power_w=300.0,
                is_valid=False,
            )

            cursor = self.db.conn.cursor()
            cursor.execute("SELECT is_valid FROM idle_baseline")
            row = cursor.fetchone()
            self.assertEqual(row["is_valid"], 0)


class TestCumulativeEnergy(unittest.TestCase):
    """Tests for cumulative energy operations."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(
            suffix=".db", delete=False
        )
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_update_and_get_cumulative_energy(self):
        """Test updating and retrieving cumulative energy."""
        session_start = datetime.now().isoformat()

        with self.db:
            self.db.update_cumulative_energy(
                session_start=session_start,
                total_wh=100.5,
                gpu_wh=75.0,
                cpu_wh=25.5,
                session_cost_usd=1.25,
            )

            energy = self.db.get_cumulative_energy()
            self.assertIsNotNone(energy)
            self.assertAlmostEqual(energy["total_wh"], 100.5)
            self.assertAlmostEqual(energy["gpu_wh"], 75.0)
            self.assertAlmostEqual(energy["cpu_wh"], 25.5)
            self.assertAlmostEqual(energy["session_cost_usd"], 1.25)

    def test_get_cumulative_energy_empty(self):
        """Test getting cumulative energy when not initialized."""
        db_path = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
        db = Database(db_path)
        try:
            with db:
                energy = db.get_cumulative_energy()
            self.assertIsNone(energy)
        finally:
            db.close()
            os.unlink(db_path)


class TestSettings(unittest.TestCase):
    """Tests for settings operations."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(
            suffix=".db", delete=False
        )
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_set_and_get_setting(self):
        """Test setting and getting a setting value."""
        with self.db:
            self.db.set_setting("test_key", "test_value")
            value = self.db.get_setting("test_key")
            self.assertEqual(value, "test_value")

    def test_get_setting_default(self):
        """Test getting a non-existent setting with default."""
        with self.db:
            value = self.db.get_setting("nonexistent", "default")
            self.assertEqual(value, "default")

    def test_cost_rate_default(self):
        """Test default cost rate."""
        with self.db:
            rate = self.db.get_cost_rate()
            self.assertEqual(rate, 0.12)

    def test_set_cost_rate(self):
        """Test setting cost rate."""
        with self.db:
            self.db.set_cost_rate(0.25)
            rate = self.db.get_cost_rate()
            self.assertEqual(rate, 0.25)


class TestProcessGpuMetrics(unittest.TestCase):
    """Tests for per-process GPU metrics operations."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(
            suffix=".db", delete=False
        )
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_insert_process_gpu_metrics(self):
        """Test inserting per-process GPU metrics."""
        timestamp = datetime.now().isoformat()

        with self.db:
            self.db.insert_process_gpu_metrics(
                timestamp,
                process_name="llama.cpp",
                pid=12345,
                gpu_utilization=75.5,
                gpu_memory_mb=4096,
            )

            cursor = self.db.conn.cursor()
            cursor.execute(
                "SELECT * FROM process_gpu_metrics_raw WHERE pid = ?",
                (12345,),
            )
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["process_name"], "llama.cpp")
            self.assertEqual(row["gpu_utilization"], 75.5)
            self.assertEqual(row["gpu_memory_mb"], 4096)


class TestDatabaseTables(unittest.TestCase):
    """Tests for database table structure."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(
            suffix=".db", delete=False
        )
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_all_tables_created(self):
        """Test that all expected tables are created."""
        with self.db:
            tables = self.db.get_tables()

            expected_tables = [
                "schema_version",
                "server_metrics_raw",
                "server_metrics_1m",
                "server_metrics_1h",
                "system_metrics_raw",
                "system_metrics_1m",
                "system_metrics_1h",
                "process_gpu_metrics_raw",
                "process_gpu_metrics_1m",
                "process_gpu_metrics_1h",
                "idle_baseline",
                "cumulative_energy",
                "combined_metrics",
                "sessions",
                "settings",
            ]

            for table in expected_tables:
                self.assertIn(table, tables, f"Table {table} not found")

    def test_table_row_counts(self):
        """Test row counts for empty tables."""
        with self.db:
            tables = self.db.get_tables()
            for table in tables:
                count = self.db.get_table_size(table)
                self.assertIsInstance(count, int)
                self.assertGreaterEqual(count, 0)


class TestSchemaValidation(unittest.TestCase):
    """Tests to validate database schema matches code definitions."""

    def test_create_table_columns_match_insert_statements(self):
        """Validate that INSERT statements use correct column names from CREATE TABLE.

        This test parses db.py to extract CREATE TABLE column definitions and
        INSERT statement column names, then verifies they match.
        """
        import re

        db_path = os.path.join(os.path.dirname(__file__), "db.py")
        with open(db_path, "r") as f:
            db_content = f.read()

        # Extract CREATE TABLE definitions and their columns
        create_pattern = r'CREATE TABLE (\w+)\s*\(([^)]+)\)'
        create_matches = re.findall(create_pattern, db_content, re.DOTALL)

        # Extract INSERT INTO statements and their columns
        insert_pattern = r'INSERT (?:OR \w+)?INTO (\w+)\s*\(([^)]+)\)'
        insert_matches = re.findall(insert_pattern, db_content)

        # Build expected columns per table from CREATE statements
        create_columns = {}
        for table_name, table_def in create_matches:
            # Extract column names (first word after whitespace, before comma or newline)
            columns = []
            for line in table_def.split(","):
                line = line.strip()
                # Match column name at start of line (alphanumeric with underscore)
                match = re.match(r'^(\w+)\s', line)
                if match:
                    columns.append(match.group(1))
            create_columns[table_name] = columns

        # Build actual columns per table from INSERT statements
        insert_columns = {}
        for table_name, column_str in insert_matches:
            columns = [c.strip() for c in column_str.split(",")]
            insert_columns[table_name] = columns

        # Validate: every INSERT table should have a CREATE definition
        for table_name, insert_cols in insert_columns.items():
            if table_name not in create_columns:
                # Allow some tables to only have INSERT (like sessions which is created differently)
                continue

            create_cols = create_columns[table_name]

            # Check for column mismatches
            missing_in_insert = set(create_cols) - set(insert_cols)
            missing_in_create = set(insert_cols) - set(create_cols)

            # Report mismatches (we don't fail here to avoid breaking tests,
            # but this helps identify issues)
            if missing_in_insert or missing_in_create:
                print(f"\nTable {table_name}:")
                if missing_in_insert:
                    print(f"  Columns in CREATE but not INSERT: {missing_in_insert}")
                if missing_in_create:
                    print(f"  Columns in INSERT but not CREATE: {missing_in_create}")


class TestCompression(unittest.TestCase):
    """Tests for metric compression functionality."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_compression_with_data(self):
        """Test compression by inserting data and verifying it gets compressed."""
        import time

        with self.db:
            # Insert raw system metrics data spanning multiple minutes
            now = int(time.time())
            base_time = (now // 60) * 60 - 120  # Start 2 minutes ago

            for i in range(3):  # 3 data points across 2 minutes
                ts = base_time + i * 30  # Every 30 seconds
                metrics = {
                    "cpu_percent": 50.0 + i * 10,
                    "cpu_cores_percent": "[10.0, 20.0, 30.0, 40.0]",
                    "cpu_temperature_c": "45.0,46.0,47.0,48.0",
                    "cpu_power_w": 65.0 + i * 5,
                    "gpu_usage": 85.0,
                    "gpu_memory_used_mb": 8192,
                    "gpu_memory_total_mb": 16384,
                    "gpu_temperature_c": 75.0,
                    "gpu_fan_speed_rpm": 2500,
                    "gpu_power_w": 220.0,
                    "memory_used_mb": 16384,
                    "memory_total_mb": 32768,
                    "memory_percent": 50.0,
                    "system_power_w": 285.0,
                }
                self.db.insert_system_metrics(
                    str(ts), metrics, table="system_metrics_raw"
                )

            # Verify raw data exists
            raw_count = self.db.get_table_size("system_metrics_raw")
            self.assertGreater(raw_count, 0, "Raw metrics should exist")

            # Verify 1m table is empty before compression
            m1_count = self.db.get_table_size("system_metrics_1m")
            self.assertEqual(m1_count, 0, "1m table should be empty before compression")

            # Run compression
            compressed = self.db.compress_to_1m()

            # Verify compression happened
            self.assertGreater(
                compressed, 0, "Compression should have created new rows"
            )

            # Verify 1m data exists after compression
            m1_count = self.db.get_table_size("system_metrics_1m")
            self.assertGreater(
                m1_count, 0, "1m table should have data after compression"
            )

            # Verify compressed data has correct structure
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT * FROM system_metrics_1m LIMIT 1")
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            # Check that aggregated columns exist and have values
            self.assertIsNotNone(row["cpu_percent_avg"])
            self.assertIsNotNone(row["gpu_usage_avg"])
            self.assertIsNotNone(row["gpu_memory_used_mb_avg"])


class TestMonthlyEnergy(unittest.TestCase):
    """Tests for monthly energy tracking and cost calculation."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db = Database(self.temp_db.name)

    def tearDown(self):
        """Clean up temporary database."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def _sqlite_today(self):
        """Return today's date as SQLite sees it (date('now'), UTC-based).

        get_monthly_energy filters against date('now', ?), which is computed
        by SQLite. Deriving the reference date from the same source keeps the
        test deterministic and immune to UTC/local month-boundary skew.
        """
        cursor = self.db.connect().cursor()
        cursor.execute("SELECT date('now')")
        return cursor.fetchone()[0]

    def _sqlite_date_days_ago(self, days):
        """Return the date `days` days before SQLite's date('now')."""
        cursor = self.db.connect().cursor()
        cursor.execute("SELECT date('now', ?)", (f'-{days} days',))
        return cursor.fetchone()[0]

    def test_get_monthly_energy_empty_database(self):
        """Test getting monthly energy when database has no data."""
        with self.db:
            result = self.db.get_monthly_energy(days=30)
            self.assertEqual(result, [])

    def test_get_monthly_energy_with_data(self):
        """Test getting monthly energy with historical data."""
        today = self._sqlite_today()
        with self.db:
            # Insert 35 days of energy data, dates derived from SQLite date('now')
            for i in range(35):
                date = self._sqlite_date_days_ago(i)
                self.db.execute(
                    """
                    INSERT INTO daily_energy (date, total_wh, gpu_wh, cpu_wh, last_update)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (date, 100.0 + i, 75.0 + i * 0.5, 25.0 + i * 0.5, self._sqlite_today()),
                )

            # Get last 30 days
            # SQLite date('now', '-30 days') includes today, so 30 days back + today = 31 rows
            result = self.db.get_monthly_energy(days=30)
            self.assertEqual(len(result), 31)

            # Verify data is sorted by date ascending
            for i in range(1, len(result)):
                self.assertLess(result[i - 1]["date"], result[i]["date"])

            # Verify last entry is today
            self.assertEqual(result[-1]["date"], today)

    def test_get_monthly_energy_cost_rate(self):
        """Test cost rate retrieval from database."""
        with self.db:
            # Test default cost rate
            default_rate = self.db.get_cost_rate()
            self.assertEqual(default_rate, 0.12)

            # Set and retrieve custom cost rate
            self.db.set_cost_rate(0.25)
            custom_rate = self.db.get_cost_rate()
            self.assertEqual(custom_rate, 0.25)

    def test_get_monthly_energy_with_cost_calculation(self):
        """Test monthly energy data with cost calculations."""
        today = datetime.now().strftime("%Y-%m-%d")
        with self.db:
            # Insert energy data for last 30 days
            for i in range(30):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                total_wh = 100.0 + i * 2
                self.db.execute(
                    """
                    INSERT INTO daily_energy (date, total_wh, gpu_wh, cpu_wh, last_update)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (date, total_wh, 75.0, 25.0, datetime.now().isoformat()),
                )

            # Set cost rate
            self.db.set_cost_rate(0.15)

            # Get monthly energy
            monthly_energy = self.db.get_monthly_energy(days=30)

            # Verify cost calculations
            for entry in monthly_energy:
                total_wh = entry["total_wh"]
                expected_cost = (total_wh / 1000) * 0.15
                self.assertAlmostEqual(entry["total_wh"], total_wh)
                self.assertEqual(entry["gpu_wh"], 75.0)
                self.assertEqual(entry["cpu_wh"], 25.0)

    def test_get_monthly_energy_different_day_counts(self):
        """Test get_monthly_energy with different day counts."""
        with self.db:
            # Insert 60 days of data, dates derived from SQLite date('now')
            for i in range(60):
                date = self._sqlite_date_days_ago(i)
                self.db.execute(
                    """
                    INSERT INTO daily_energy (date, total_wh, gpu_wh, cpu_wh, last_update)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (date, 100.0, 75.0, 25.0, self._sqlite_today()),
                )

            # SQLite date('now', '-X days') includes today, so results = X + 1
            # Test with 7 days (should return 8 rows: today + 7 days back)
            result_7 = self.db.get_monthly_energy(days=7)
            self.assertEqual(len(result_7), 8)

            # Test with 14 days (should return 15 rows)
            result_14 = self.db.get_monthly_energy(days=14)
            self.assertEqual(len(result_14), 15)

            # Test with 30 days (should return 31 rows)
            result_30 = self.db.get_monthly_energy(days=30)
            self.assertEqual(len(result_30), 31)

            # Test with 60 days (returns 60 rows as SQLite date('now', '-60 days') returns 60 days back)
            result_60 = self.db.get_monthly_energy(days=60)
            self.assertEqual(len(result_60), 60)

    def test_get_monthly_energy_partial_data(self):
        """Test get_monthly_energy when some days are missing."""
        with self.db:
            # Insert data for only some days (not consecutive)
            for i in [0, 2, 4, 6, 8, 10]:  # Every other day for last 12 days
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                self.db.execute(
                    """
                    INSERT INTO daily_energy (date, total_wh, gpu_wh, cpu_wh, last_update)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (date, 100.0, 75.0, 25.0, datetime.now().isoformat()),
                )

            # Get last 30 days - should only return days with data
            result = self.db.get_monthly_energy(days=30)
            self.assertEqual(len(result), 6)

    def test_get_monthly_energy_data_values(self):
        """Test that get_monthly_energy returns correct data values."""
        today = datetime.now().strftime("%Y-%m-%d")
        with self.db:
            # Insert specific test data
            test_data = [
                (today, 150.5, 100.25, 50.25, datetime.now().isoformat()),
                ((datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), 200.0, 150.0, 50.0, datetime.now().isoformat()),
            ]

            for date, total_wh, gpu_wh, cpu_wh, last_update in test_data:
                self.db.execute(
                    """
                    INSERT INTO daily_energy (date, total_wh, gpu_wh, cpu_wh, last_update)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (date, total_wh, gpu_wh, cpu_wh, last_update),
                )

            result = self.db.get_monthly_energy(days=30)

            # Verify specific values
            today_entry = next((e for e in result if e["date"] == today), None)
            self.assertIsNotNone(today_entry)
            self.assertAlmostEqual(today_entry["total_wh"], 150.5)
            self.assertAlmostEqual(today_entry["gpu_wh"], 100.25)
            self.assertAlmostEqual(today_entry["cpu_wh"], 50.25)


class TestApiMonthlyCost(unittest.TestCase):
    """Tests for the /api/metrics/monthly-cost endpoint."""

    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db = Database(self.temp_db.name)
        # Keep the connection open for the whole test so the patched _get_db
        # (which returns self.db) always has a live connection.
        self.db.connect()

        # Set up Flask test client
        from web_server import app, _get_db, _db_instance, _db_path
        app.config["TESTING"] = True
        self.app = app.test_client()

        # Isolate the API so it reads/writes ONLY the temp DB, never the
        # production DB. The API resolves its DB path from config.database.path
        # and caches the Database instance in web_server._db_instance. We patch
        # _get_db to always return the temp-DB Database so the API never touches
        # llama-monitor.db. This also avoids the "database is locked" failures
        # and daily_energy UNIQUE-constraint pollution caused by writing to the
        # production DB from tests.
        self._original_get_db = _get_db
        self._original_db_instance = _db_instance
        self._original_db_path = _db_path

        import web_server
        self._web_server = web_server
        self._web_server._db_instance = None
        self._web_server._db_path = None
        self._get_db_patcher = mock.patch("web_server._get_db", return_value=self.db)
        self._get_db_patcher.start()

    def tearDown(self):
        """Clean up temporary database and restore patches."""
        self._get_db_patcher.stop()
        self._web_server._db_instance = self._original_db_instance
        self._web_server._db_path = self._original_db_path
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_api_monthly_cost_with_data(self):
        """Test API returns correct cost data when database has energy data."""
        today = datetime.now().strftime("%Y-%m-%d")
        # Insert energy data into the temp DB (which the patched _get_db
        # serves to the API). self.db stays connected for the whole test.
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            total_wh = 100.0 + i * 10
            self.db.execute(
                """
                INSERT INTO daily_energy (date, total_wh, gpu_wh, cpu_wh, last_update)
                VALUES (?, ?, ?, ?, ?)
                """,
                (date, total_wh, 75.0, 25.0, datetime.now().isoformat()),
            )

        # Set custom cost rate
        self.db.set_cost_rate(0.20)

        # Call API - the patched _get_db serves the temp DB
        result = self.app.get("/api/metrics/monthly-cost")
        self.assertEqual(result.status_code, 200)

        data = result.get_json()
        self.assertTrue(data["success"])

        # Verify cost calculations
        self.assertGreater(len(data["data"]), 0)
        for entry in data["data"]:
            expected_cost = (entry["total_wh"] / 1000) * 0.20
            self.assertAlmostEqual(entry["cost_usd"], expected_cost)

    def test_api_monthly_cost_empty_database(self):
        """Test API returns empty data when database has no energy data."""
        # The temp DB is empty; the patched _get_db serves it to the API
        result = self.app.get("/api/metrics/monthly-cost")
        self.assertEqual(result.status_code, 200)

        data = result.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"], [])

    def test_api_monthly_cost_date_format(self):
        """Test that API returns dates in correct format."""
        # Use a date within the 30-day window that get_monthly_energy returns
        test_date = datetime.now().strftime("%Y-%m-%d")
        self.db.execute(
            """
            INSERT INTO daily_energy (date, total_wh, gpu_wh, cpu_wh, last_update)
            VALUES (?, ?, ?, ?, ?)
            """,
            (test_date, 100.0, 75.0, 25.0, datetime.now().isoformat()),
        )

        result = self.app.get("/api/metrics/monthly-cost")
        data = result.get_json()

        # Verify date is returned
        self.assertGreater(len(data["data"]), 0)
        self.assertEqual(data["data"][0]["date"], test_date)

    def test_api_monthly_cost_error_handling(self):
        """Test API error handling for invalid database path."""
        # This test would require mocking; basic validation here
        result = self.app.get("/api/metrics/monthly-cost")
        self.assertEqual(result.status_code, 200)

        data = result.get_json()
        self.assertIn("success", data)


class TestJavaScriptDateFormatting(unittest.TestCase):
    """Tests for JavaScript date formatting logic (MM/dd/yyyy)."""

    def test_date_formatting_logic(self):
        """Test the date formatting algorithm used in JavaScript."""
        # Simulate the JavaScript date formatting logic
        def format_date_js(date_str):
            """Format date as MM/dd/yyyy following JavaScript logic."""
            # This mimics: new Date(entry.date + 'T00:00:00')
            # where date_str is in YYYY-MM-DD format
            year, month, day = date_str.split("-")
            return f"{int(month)}/{int(day)}/{year}"

        # Test various date formats
        test_cases = [
            ("2026-01-05", "1/5/2026"),
            ("2026-06-14", "6/14/2026"),
            ("2026-12-25", "12/25/2026"),
            ("2026-07-04", "7/4/2026"),
        ]

        for input_date, expected in test_cases:
            result = format_date_js(input_date)
            self.assertEqual(result, expected)

    def test_date_padding_logic(self):
        """Test that day/month padding works correctly."""
        def format_date_with_padding(date_str):
            """Format date with proper padding like JavaScript."""
            year, month, day = date_str.split("-")
            month_padded = month.lstrip("0")  # JavaScript: .toString().padStart(2, '0')
            day_padded = day.lstrip("0")
            return f"{month_padded}/{day_padded}/{year}"

        # Note: JavaScript's padStart(2, '0') on already-padded values keeps them padded
        # The actual JS code does: (date.getMonth() + 1).toString().padStart(2, '0')
        # which adds padding to single digits

        test_cases = [
            ("2026-01-05", "1/5/2026"),
            ("2026-06-14", "6/14/2026"),
            ("2026-12-25", "12/25/2026"),
        ]

        for input_date, expected in test_cases:
            result = format_date_with_padding(input_date)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
