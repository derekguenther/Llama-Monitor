"""SQLite database initialization and management for llama-monitor."""

import datetime
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class Database:
    """Manages SQLite database for llama-monitor."""

    SCHEMA_VERSION = "1.0"

    def __init__(self, db_path: str):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._lock = threading.RLock()  # Reentrant lock for thread-safe access
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Ensure database directory exists."""
        path = Path(self.db_path)
        path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        """Open database connection if not already open.

        Returns:
            SQLite connection object
        """
        with self._lock:
            if self.conn is None:
                # check_same_thread=False allows using the connection from any thread
                # This is necessary because the aggregator runs in a background thread
                self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
                self.conn.row_factory = sqlite3.Row
                self._initialize_schema()
            return self.conn

    def close(self) -> None:
        """Close database connection."""
        with self._lock:
            if self.conn is not None:
                self.conn.close()
                self.conn = None

    def __enter__(self) -> "Database":
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    def lock(self):
        """Context manager for acquiring database lock.

        Use this to ensure thread-safe database operations.
        """
        return self._lock

    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
        """Execute a SQL statement with the lock.

        Args:
            sql: SQL statement to execute
            params: Parameters for the statement

        Returns:
            Cursor object
        """
        with self._lock:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.conn.commit()
            return cursor

    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
        """Execute a SELECT query with the lock.

        Args:
            sql: SQL query to execute
            params: Parameters for the query

        Returns:
            First row result or None
        """
        with self._lock:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor.fetchone()

    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:
        """Execute a SELECT query and return all results with the lock.

        Args:
            sql: SQL query to execute
            params: Parameters for the query

        Returns:
            List of all row results
        """
        with self._lock:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor.fetchall()

    def _initialize_schema(self) -> None:
        """Initialize database schema if not already initialized."""
        cursor = self.conn.cursor()

        # Check if schema already exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'"
        )
        if cursor.fetchone():
            return  # Schema already initialized

        # Create schema version table
        cursor.execute(
            """
            CREATE TABLE schema_version (
                version TEXT PRIMARY KEY,
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        cursor.execute(
            "INSERT INTO schema_version (version) VALUES (?)",
            (self.SCHEMA_VERSION,),
        )

        # Create server metrics tables
        self._create_server_metrics_tables(cursor)

        # Create system metrics tables
        self._create_system_metrics_tables(cursor)

        # Create per-process GPU metrics tables
        self._create_process_gpu_metrics_tables(cursor)

        # Create per-process CPU metrics tables (from Public Documents schema)
        self._create_process_cpu_metrics_tables(cursor)

        # Create auxiliary tables
        self._create_auxiliary_tables(cursor)

        self.conn.commit()

    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
        """Create server metrics tables."""
        # Raw server metrics (1-second intervals)
        cursor.execute(
            """
            CREATE TABLE server_metrics_raw (
                timestamp TEXT PRIMARY KEY,
                prompt_tokens_total INTEGER,
                prompt_tokens_seconds REAL,
                tokens_predicted_total INTEGER,
                predicted_tokens_seconds REAL,
                requests_processing INTEGER,
                requests_deferred INTEGER,
                slots_active INTEGER DEFAULT 0,
                slots_processing INTEGER DEFAULT 0
            )
            """
        )

        # 1-minute compressed server metrics with bucket-based aggregation
        cursor.execute(
            """
            CREATE TABLE server_metrics_1m (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bucket_start INTEGER NOT NULL,
                bucket_end INTEGER NOT NULL,
                prompt_tokens_total INTEGER DEFAULT 0,
                prompt_tokens_seconds REAL DEFAULT 0,
                tokens_predicted_total INTEGER DEFAULT 0,
                predicted_tokens_seconds REAL DEFAULT 0,
                requests_processing_avg REAL DEFAULT 0,
                requests_deferred_avg REAL DEFAULT 0,
                slots_active_avg REAL DEFAULT 0,
                slots_processing_avg REAL DEFAULT 0
            )
            """
        )

        # 1-hour compressed server metrics with bucket-based aggregation
        cursor.execute(
            """
            CREATE TABLE server_metrics_1h (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bucket_start INTEGER NOT NULL,
                bucket_end INTEGER NOT NULL,
                prompt_tokens_total INTEGER DEFAULT 0,
                prompt_tokens_seconds REAL DEFAULT 0,
                tokens_predicted_total INTEGER DEFAULT 0,
                predicted_tokens_seconds REAL DEFAULT 0,
                requests_processing_avg REAL DEFAULT 0,
                requests_deferred_avg REAL DEFAULT 0,
                slots_active_avg REAL DEFAULT 0,
                slots_processing_avg REAL DEFAULT 0
            )
            """
        )

    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
        """Create system metrics tables."""
        # Raw system metrics (1-second intervals)
        cursor.execute(
            """
            CREATE TABLE system_metrics_raw (
                timestamp TEXT PRIMARY KEY,
                cpu_percent REAL,
                cpu_cores_percent TEXT,
                cpu_temperature_c TEXT,
                cpu_power_w REAL,
                gpu_usage REAL,
                gpu_memory_used_mb INTEGER,
                gpu_memory_total_mb INTEGER,
                gpu_temperature_c REAL,
                gpu_fan_speed_rpm INTEGER,
                gpu_power_w REAL,
                memory_used_mb INTEGER,
                memory_total_mb INTEGER,
                memory_percent REAL,
                system_power_w REAL
            )
            """
        )

        # 1-minute compressed system metrics with bucket-based aggregation
        cursor.execute(
            """
            CREATE TABLE system_metrics_1m (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bucket_start INTEGER NOT NULL,
                bucket_end INTEGER NOT NULL,
                cpu_percent_avg REAL DEFAULT 0,
                cpu_temperature_c_avg REAL DEFAULT 0,
                cpu_power_w_avg REAL DEFAULT 0,
                gpu_usage_avg INTEGER DEFAULT 0,
                gpu_memory_used_mb_avg INTEGER DEFAULT 0,
                gpu_temperature_c_avg INTEGER DEFAULT 0,
                gpu_fan_speed_rpm_avg INTEGER DEFAULT 0,
                gpu_power_w_avg REAL DEFAULT 0,
                memory_used_mb_avg INTEGER DEFAULT 0,
                memory_percent_avg REAL DEFAULT 0,
                system_power_w_avg REAL DEFAULT 0
            )
            """
        )

        # 1-hour compressed system metrics with bucket-based aggregation
        cursor.execute(
            """
            CREATE TABLE system_metrics_1h (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bucket_start INTEGER NOT NULL,
                bucket_end INTEGER NOT NULL,
                cpu_percent_avg REAL DEFAULT 0,
                cpu_temperature_c_avg REAL DEFAULT 0,
                cpu_power_w_avg REAL DEFAULT 0,
                gpu_usage_avg INTEGER DEFAULT 0,
                gpu_memory_used_mb_avg INTEGER DEFAULT 0,
                gpu_temperature_c_avg INTEGER DEFAULT 0,
                gpu_fan_speed_rpm_avg INTEGER DEFAULT 0,
                gpu_power_w_avg REAL DEFAULT 0,
                memory_used_mb_avg INTEGER DEFAULT 0,
                memory_percent_avg REAL DEFAULT 0,
                system_power_w_avg REAL DEFAULT 0
            )
            """
        )

    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
        """Create per-process GPU metrics tables."""
        # Raw per-process GPU metrics
        cursor.execute(
            """
            CREATE TABLE process_gpu_metrics_raw (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                process_name TEXT NOT NULL,
                pid INTEGER NOT NULL,
                gpu_utilization INTEGER DEFAULT 0,
                gpu_memory_mb INTEGER DEFAULT 0
            )
            """
        )

        # 1-minute compressed per-process GPU metrics with bucket-based aggregation
        cursor.execute(
            """
            CREATE TABLE process_gpu_metrics_1m (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bucket_start INTEGER NOT NULL,
                bucket_end INTEGER NOT NULL,
                process_name TEXT NOT NULL,
                pid INTEGER NOT NULL,
                gpu_utilization_avg INTEGER DEFAULT 0,
                gpu_memory_mb_avg INTEGER DEFAULT 0
            )
            """
        )

        # 1-hour compressed per-process GPU metrics with bucket-based aggregation
        cursor.execute(
            """
            CREATE TABLE process_gpu_metrics_1h (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bucket_start INTEGER NOT NULL,
                bucket_end INTEGER NOT NULL,
                process_name TEXT NOT NULL,
                pid INTEGER NOT NULL,
                gpu_utilization_avg INTEGER DEFAULT 0,
                gpu_memory_mb_avg INTEGER DEFAULT 0
            )
            """
        )

    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
        """Create per-process CPU metrics tables (from Public Documents schema)."""
        # Raw per-process CPU metrics
        cursor.execute(
            """
            CREATE TABLE process_cpu_metrics_raw (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                process_name TEXT NOT NULL,
                pid INTEGER NOT NULL,
                cpu_percent REAL DEFAULT 0,
                cpu_power_w REAL DEFAULT 0
            )
            """
        )

        # 1-minute compressed per-process CPU metrics
        cursor.execute(
            """
            CREATE TABLE process_cpu_metrics_1m (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bucket_start INTEGER NOT NULL,
                bucket_end INTEGER NOT NULL,
                process_name TEXT NOT NULL,
                pid INTEGER NOT NULL,
                cpu_percent_avg REAL DEFAULT 0,
                cpu_power_w_avg REAL DEFAULT 0
            )
            """
        )

        # 1-hour compressed per-process CPU metrics
        cursor.execute(
            """
            CREATE TABLE process_cpu_metrics_1h (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bucket_start INTEGER NOT NULL,
                bucket_end INTEGER NOT NULL,
                process_name TEXT NOT NULL,
                pid INTEGER NOT NULL,
                cpu_percent_avg REAL DEFAULT 0,
                cpu_power_w_avg REAL DEFAULT 0
            )
            """
        )

    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:
        """Create auxiliary tables."""
        # Idle baseline power consumption
        cursor.execute(
            """
            CREATE TABLE idle_baseline (
                timestamp TEXT PRIMARY KEY,
                cpu_percent REAL,
                gpu_percent REAL,
                system_power_w REAL,
                is_valid BOOLEAN DEFAULT 1
            )
            """
        )

        # Cumulative energy counters
        cursor.execute(
            """
            CREATE TABLE cumulative_energy (
                id INTEGER PRIMARY KEY DEFAULT 1,
                session_start TEXT NOT NULL,
                last_update TEXT,
                total_wh REAL DEFAULT 0,
                gpu_wh REAL DEFAULT 0,
                cpu_wh REAL DEFAULT 0,
                session_cost_usd REAL DEFAULT 0
            )
            """
        )

        # Combined metrics with cost
        cursor.execute(
            """
            CREATE TABLE combined_metrics (
                timestamp TEXT PRIMARY KEY,
                server_data JSON,
                system_data JSON,
                cost_data JSON
            )
            """
        )

        # Session tracking
        cursor.execute(
            """
            CREATE TABLE sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                total_gpu_wh REAL DEFAULT 0,
                total_cpu_wh REAL DEFAULT 0,
                total_cost_usd REAL DEFAULT 0
            )
            """
        )

        # Daily energy tracking table
        cursor.execute(
            """
            CREATE TABLE daily_energy (
                date TEXT PRIMARY KEY,
                total_wh REAL DEFAULT 0,
                gpu_wh REAL DEFAULT 0,
                cpu_wh REAL DEFAULT 0,
                last_update TEXT
            )
            """
        )

        # Settings table for persistent configuration
        cursor.execute(
            """
            CREATE TABLE settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT DEFAULT (datetime('now'))
            )
            """
        )

        # Insert default cost rate if not exists
        cursor.execute(
            """
            INSERT OR IGNORE INTO settings (key, value)
            VALUES ('cost_rate_usd_per_kwh', '0.12')
            """
        )

    def insert_server_metrics(
        self,
        timestamp: str,
        metrics: Dict[str, Any],
        table: str = "server_metrics_raw",
    ) -> None:
        """Insert server metrics into database.

        Args:
            timestamp: Timestamp of the measurement
            metrics: Dictionary of metrics
            table: Table name (raw, 1m, or 1h)
        """
        with self._lock:
            cursor = self.conn.cursor()

            columns = [
                "timestamp",
                "prompt_tokens_total",
                "prompt_tokens_seconds",
                "tokens_predicted_total",
                "predicted_tokens_seconds",
                "requests_processing",
                "requests_deferred",
            ]

            values = [
                timestamp,
                metrics.get("prompt_tokens_total"),
                metrics.get("prompt_tokens_seconds"),
                metrics.get("tokens_predicted_total"),
                metrics.get("predicted_tokens_seconds"),
                metrics.get("requests_processing"),
                metrics.get("requests_deferred"),
            ]

            placeholders = ", ".join(["?" for _ in columns])
            column_names = ", ".join(columns)

            cursor.execute(
                f"""
                INSERT OR REPLACE INTO {table} ({column_names})
                VALUES ({placeholders})
                """,
                values,
            )
            self.conn.commit()

    def insert_system_metrics(
        self,
        timestamp: str,
        metrics: Dict[str, Any],
        table: str = "system_metrics_raw",
    ) -> None:
        """Insert system metrics into database.

        Args:
            timestamp: Timestamp of the measurement
            metrics: Dictionary of metrics
            table: Table name (raw, 1m, or 1h)
        """
        with self._lock:
            cursor = self.conn.cursor()

            # Convert JSON fields
            cpu_cores_percent = (
                metrics.get("cpu_cores_percent")
                if metrics.get("cpu_cores_percent") is None
                else str(metrics.get("cpu_cores_percent"))
            )
            cpu_temperature_c = (
                metrics.get("cpu_temperature_c")
                if metrics.get("cpu_temperature_c") is None
                else str(metrics.get("cpu_temperature_c"))
            )

            columns = [
                "timestamp",
                "cpu_percent",
                "cpu_cores_percent",
                "cpu_temperature_c",
                "cpu_power_w",
                "gpu_usage",
                "gpu_memory_used_mb",
                "gpu_memory_total_mb",
                "gpu_temperature_c",
                "gpu_fan_speed_rpm",
                "gpu_power_w",
                "memory_used_mb",
                "memory_total_mb",
                "memory_percent",
                "system_power_w",
            ]

            values = [
                timestamp,
                metrics.get("cpu_percent"),
                cpu_cores_percent,
                cpu_temperature_c,
                metrics.get("cpu_power_w"),
                metrics.get("gpu_usage"),
                metrics.get("gpu_memory_used_mb"),
                metrics.get("gpu_memory_total_mb"),
                metrics.get("gpu_temperature_c"),
                metrics.get("gpu_fan_speed_rpm"),
                metrics.get("gpu_power_w"),
                metrics.get("memory_used_mb"),
                metrics.get("memory_total_mb"),
                metrics.get("memory_percent"),
                metrics.get("system_power_w"),
            ]

            placeholders = ", ".join(["?" for _ in columns])
            column_names = ", ".join(columns)

            cursor.execute(
                f"""
                INSERT OR REPLACE INTO {table} ({column_names})
                VALUES ({placeholders})
                """,
                values,
            )
            self.conn.commit()

    def insert_process_gpu_metrics(
        self,
        timestamp: str,
        process_name: str,
        pid: int,
        gpu_utilization: float,
        gpu_memory_mb: int,
        table: str = "process_gpu_metrics_raw",
    ) -> None:
        """Insert per-process GPU metrics.

        Args:
            timestamp: Timestamp of the measurement
            process_name: Name of the process
            pid: Process ID
            gpu_utilization: GPU utilization percentage
            gpu_memory_mb: GPU memory usage in MB
            table: Table name (raw, 1m, or 1h)
        """
        with self._lock:
            cursor = self.conn.cursor()

            cursor.execute(
                f"""
                INSERT OR REPLACE INTO {table} (
                    timestamp, process_name, pid, gpu_utilization, gpu_memory_mb
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (timestamp, process_name, pid, gpu_utilization, gpu_memory_mb),
            )
            self.conn.commit()

    def insert_idle_baseline(
        self,
        timestamp: str,
        cpu_percent: float,
        gpu_percent: float,
        system_power_w: float,
        is_valid: bool = True,
    ) -> None:
        """Insert idle baseline measurement.

        Args:
            timestamp: Timestamp of the measurement
            cpu_percent: CPU utilization percentage
            gpu_percent: GPU utilization percentage
            system_power_w: System power in watts
            is_valid: Whether this is a valid baseline
        """
        with self._lock:
            cursor = self.conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO idle_baseline (
                    timestamp, cpu_percent, gpu_percent, system_power_w, is_valid
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (timestamp, cpu_percent, gpu_percent, system_power_w, 1 if is_valid else 0),
            )
            self.conn.commit()

    def insert_server_metrics_raw(
        self,
        timestamp: int,
        prompt_tokens_total: int = 0,
        prompt_tokens_seconds: float = 0,
        tokens_predicted_total: int = 0,
        predicted_tokens_seconds: float = 0,
        requests_processing: int = 0,
        requests_deferred: int = 0,
        slots_active: int = 0,
        slots_processing: int = 0,
    ) -> None:
        """Insert server metrics raw data.

        Args:
            timestamp: Unix timestamp.
            prompt_tokens_total: Total prompt tokens processed.
            prompt_tokens_seconds: Time spent processing prompts.
            tokens_predicted_total: Total tokens predicted.
            predicted_tokens_seconds: Time spent predicting tokens.
            requests_processing: Number of processing requests.
            requests_deferred: Number of deferred requests.
            slots_active: Number of active slots.
            slots_processing: Number of processing slots.
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO server_metrics_raw (
                    timestamp, prompt_tokens_total, prompt_tokens_seconds,
                    tokens_predicted_total, predicted_tokens_seconds,
                    requests_processing, requests_deferred, slots_active, slots_processing
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    timestamp,
                    prompt_tokens_total,
                    prompt_tokens_seconds,
                    tokens_predicted_total,
                    predicted_tokens_seconds,
                    requests_processing,
                    requests_deferred,
                    slots_active,
                    slots_processing,
                ),
            )
            self.conn.commit()

    def insert_system_metrics_raw(
        self,
        timestamp: int,
        cpu_percent: float = 0,
        cpu_cores_percent: str = "[]",
        cpu_temperature_c: str = "[]",
        cpu_power_w: float = 0,
        gpu_usage: int = 0,
        gpu_memory_used_mb: int = 0,
        gpu_memory_total_mb: int = 0,
        gpu_temperature_c: int = 0,
        gpu_fan_speed_rpm: int = 0,
        gpu_power_w: float = 0,
        memory_used_mb: int = 0,
        memory_total_mb: int = 0,
        memory_percent: float = 0,
        system_power_w: float = 0,
    ) -> None:
        """Insert system metrics raw data.

        Args:
            timestamp: Unix timestamp.
            cpu_percent: Total CPU usage percentage.
            cpu_cores_percent: Per-core CPU usage as JSON string.
            cpu_temperature_c: CPU temperatures as JSON string.
            cpu_power_w: CPU power in watts.
            gpu_usage: GPU usage percentage.
            gpu_memory_used_mb: GPU memory used in MB.
            gpu_memory_total_mb: GPU memory total in MB.
            gpu_temperature_c: GPU temperature in Celsius.
            gpu_fan_speed_rpm: GPU fan speed in RPM.
            gpu_power_w: GPU power in watts.
            memory_used_mb: System memory used in MB.
            memory_total_mb: System memory total in MB.
            memory_percent: System memory usage percentage.
            system_power_w: System power in watts.
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO system_metrics_raw (
                    timestamp, cpu_percent, cpu_cores_percent, cpu_temperature_c,
                    cpu_power_w, gpu_usage, gpu_memory_used_mb, gpu_memory_total_mb,
                    gpu_temperature_c, gpu_fan_speed_rpm, gpu_power_w,
                    memory_used_mb, memory_total_mb, memory_percent, system_power_w
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    timestamp,
                    cpu_percent,
                    cpu_cores_percent,
                    cpu_temperature_c,
                    cpu_power_w,
                    gpu_usage,
                    gpu_memory_used_mb,
                    gpu_memory_total_mb,
                    gpu_temperature_c,
                    gpu_fan_speed_rpm,
                    gpu_power_w,
                    memory_used_mb,
                    memory_total_mb,
                    memory_percent,
                    system_power_w,
                ),
            )
            self.conn.commit()

    def insert_process_gpu_metrics_raw(
        self,
        timestamp: int,
        process_name: str,
        pid: int,
        gpu_utilization: int = 0,
        gpu_memory_mb: int = 0,
    ) -> None:
        """Insert process GPU metrics raw data.

        Args:
            timestamp: Unix timestamp.
            process_name: Name of the process.
            pid: Process ID.
            gpu_utilization: GPU utilization percentage.
            gpu_memory_mb: GPU memory used in MB.
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO process_gpu_metrics_raw (
                    timestamp, process_name, pid, gpu_utilization, gpu_memory_mb
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (timestamp, process_name, pid, gpu_utilization, gpu_memory_mb),
            )
            self.conn.commit()

    def insert_process_cpu_metrics_raw(
        self,
        timestamp: int,
        process_name: str,
        pid: int,
        cpu_percent: float = 0,
        cpu_power_w: float = 0,
    ) -> None:
        """Insert process CPU metrics raw data.

        Args:
            timestamp: Unix timestamp.
            process_name: Name of the process.
            pid: Process ID.
            cpu_percent: CPU utilization percentage.
            cpu_power_w: CPU power in watts.
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO process_cpu_metrics_raw (
                    timestamp, process_name, pid, cpu_percent, cpu_power_w
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (timestamp, process_name, pid, cpu_percent, cpu_power_w),
            )
            self.conn.commit()

    def update_cumulative_energy(
        self,
        session_start: str,
        total_wh: float,
        gpu_wh: float,
        cpu_wh: float,
        session_cost_usd: float,
    ) -> None:
        """Update cumulative energy counters.

        Args:
            session_start: Session start timestamp
            total_wh: Total energy in watt-hours
            gpu_wh: GPU energy in watt-hours
            cpu_wh: CPU energy in watt-hours
            session_cost_usd: Session cost in USD
        """
        with self._lock:
            cursor = self.conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO cumulative_energy (
                    id, session_start, last_update, total_wh, gpu_wh, cpu_wh, session_cost_usd
                )
                VALUES (1, ?, datetime('now'), ?, ?, ?, ?)
                """,
                (session_start, total_wh, gpu_wh, cpu_wh, session_cost_usd),
            )
            self.conn.commit()

    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
        """Get current cumulative energy values.

        Returns:
            Dictionary of energy values or None if not initialized
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT session_start, last_update, total_wh, gpu_wh, cpu_wh, session_cost_usd
            FROM cumulative_energy
            WHERE id = 1
            """
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_today_energy(self) -> Optional[Dict[str, Any]]:
        """Get today's energy consumption from midnight.

        Returns:
            Dictionary of energy values or None if not initialized
        """
        cursor = self.conn.cursor()
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            """
            SELECT date, total_wh, gpu_wh, cpu_wh, last_update
            FROM daily_energy
            WHERE date = ?
            """,
            (today,),
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def update_today_energy(
        self,
        total_wh: float,
        gpu_wh: float,
        cpu_wh: float,
    ) -> None:
        """Update today's energy consumption.

        Args:
            total_wh: Total energy in watt-hours
            gpu_wh: GPU energy in watt-hours
            cpu_wh: CPU energy in watt-hours
        """
        with self._lock:
            cursor = self.conn.cursor()
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            now = datetime.datetime.now().isoformat()

            cursor.execute(
                """
                INSERT INTO daily_energy (date, total_wh, gpu_wh, cpu_wh, last_update)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                    total_wh = ?,
                    gpu_wh = ?,
                    cpu_wh = ?,
                    last_update = ?
                """,
                (today, total_wh, gpu_wh, cpu_wh, now, total_wh, gpu_wh, cpu_wh, now),
            )
            self.conn.commit()

    def get_server_metrics(
        self,
        table: str = "server_metrics_raw",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Get server metrics with optional filtering.

        Args:
            table: Table name to query
            start_time: Start timestamp (inclusive)
            end_time: End timestamp (inclusive)
            limit: Maximum number of records

        Returns:
            List of metric records
        """
        cursor = self.conn.cursor()

        query = f"SELECT * FROM {table} WHERE 1=1"
        params = []

        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time)
        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time)

        query += " ORDER BY timestamp DESC"
        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_system_metrics(
        self,
        table: str = "system_metrics_raw",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Get system metrics with optional filtering.

        Args:
            table: Table name to query
            start_time: Start timestamp (inclusive)
            end_time: End timestamp (inclusive)
            limit: Maximum number of records

        Returns:
            List of metric records
        """
        cursor = self.conn.cursor()

        query = f"SELECT * FROM {table} WHERE 1=1"
        params = []

        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time)
        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time)

        query += " ORDER BY timestamp DESC"
        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def vacuum(self) -> None:
        """Run VACUUM to reclaim space."""
        cursor = self.conn.cursor()
        cursor.execute("VACUUM")

    def get_table_size(self, table: str) -> int:
        """Get row count for a table.

        Args:
            table: Table name

        Returns:
            Number of rows
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        return cursor.fetchone()[0]

    def get_tables(self) -> List[str]:
        """Get list of all user tables.

        Returns:
            List of table names
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        return [row[0] for row in cursor.fetchall()]

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value.

        Args:
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value or default
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            return row[0]
        return default

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value.

        Args:
            key: Setting key
            value: Value to set
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, datetime('now'))
                """,
                (key, str(value)),
            )
            self.conn.commit()

    def get_cost_rate(self) -> float:
        """Get the cost rate from settings.

        Returns:
            Cost rate in USD per kWh
        """
        value = self.get_setting("cost_rate_usd_per_kwh", "0.12")
        try:
            return float(value)
        except ValueError:
            return 0.12

    def set_cost_rate(self, rate: float) -> None:
        """Set the cost rate in settings.

        Args:
            rate: Cost rate in USD per kWh
        """
        self.set_setting("cost_rate_usd_per_kwh", str(rate))

    def compress_to_1m(self) -> int:
        """Compress raw metrics to 1-minute buckets.

        Compresses data from raw tables into 1-minute aggregated tables
        using bucket_start/bucket_end for proper time-windowed aggregation.

        Returns:
            Number of rows compressed.
        """
        cursor = self.conn.cursor()
        compressed = 0

        # Find the latest timestamp in 1m tables
        cursor.execute(
            """
            SELECT COALESCE(MAX(bucket_end), 0) as last_bucket
            FROM system_metrics_1m
            """
        )
        result = cursor.fetchone()
        last_bucket = result["last_bucket"] if result else 0

        # Current minute bucket
        current_time = int(time.time())
        current_bucket = (current_time // 60) * 60

        # Only compress if we have data from a previous minute
        if current_bucket > last_bucket:
            # Compress system metrics
            cursor.execute(
                """
                INSERT INTO system_metrics_1m (
                    bucket_start, bucket_end,
                    cpu_percent_avg, cpu_temperature_c_avg,
                    cpu_power_w_avg, gpu_usage_avg,
                    gpu_memory_used_mb_avg, gpu_temperature_c_avg,
                    gpu_fan_speed_rpm_avg, gpu_power_w_avg,
                    memory_used_mb_avg, memory_percent_avg,
                    system_power_w_avg
                )
                SELECT
                    (timestamp / 60) * 60 as bucket_start,
                    (timestamp / 60) * 60 + 60 as bucket_end,
                    AVG(cpu_percent) as cpu_percent_avg,
                    AVG(cpu_temperature_c) as cpu_temperature_c_avg,
                    AVG(cpu_power_w) as cpu_power_w_avg,
                    AVG(gpu_usage) as gpu_usage_avg,
                    AVG(gpu_memory_used_mb) as gpu_memory_used_mb_avg,
                    AVG(gpu_temperature_c) as gpu_temperature_c_avg,
                    AVG(gpu_fan_speed_rpm) as gpu_fan_speed_rpm_avg,
                    AVG(gpu_power_w) as gpu_power_w_avg,
                    AVG(memory_used_mb) as memory_used_mb_avg,
                    AVG(memory_percent) as memory_percent_avg,
                    AVG(system_power_w) as system_power_w_avg
                FROM system_metrics_raw
                WHERE timestamp >= ? AND timestamp < ?
                GROUP BY (timestamp / 60)
                """,
                (last_bucket, current_bucket),
            )
            compressed += cursor.rowcount

            # Compress server metrics
            cursor.execute(
                """
                INSERT INTO server_metrics_1m (
                    bucket_start, bucket_end,
                    prompt_tokens_total, prompt_tokens_seconds,
                    tokens_predicted_total, predicted_tokens_seconds,
                    requests_processing_avg, requests_deferred_avg
                )
                SELECT
                    (timestamp / 60) * 60 as bucket_start,
                    (timestamp / 60) * 60 + 60 as bucket_end,
                    SUM(prompt_tokens_total) as prompt_tokens_total,
                    SUM(prompt_tokens_seconds) as prompt_tokens_seconds,
                    SUM(tokens_predicted_total) as tokens_predicted_total,
                    SUM(predicted_tokens_seconds) as predicted_tokens_seconds,
                    AVG(requests_processing) as requests_processing_avg,
                    AVG(requests_deferred) as requests_deferred_avg
                FROM server_metrics_raw
                WHERE timestamp >= ? AND timestamp < ?
                GROUP BY (timestamp / 60)
                """,
                (last_bucket, current_bucket),
            )
            compressed += cursor.rowcount

            # Compress process GPU metrics
            cursor.execute(
                """
                INSERT INTO process_gpu_metrics_1m (
                    bucket_start, bucket_end,
                    process_name, pid,
                    gpu_utilization_avg, gpu_memory_mb_avg
                )
                SELECT
                    (timestamp / 60) * 60 as bucket_start,
                    (timestamp / 60) * 60 + 60 as bucket_end,
                    process_name, pid,
                    AVG(gpu_utilization) as gpu_utilization_avg,
                    AVG(gpu_memory_mb) as gpu_memory_mb_avg
                FROM process_gpu_metrics_raw
                WHERE timestamp >= ? AND timestamp < ?
                GROUP BY (timestamp / 60), process_name, pid
                """,
                (last_bucket, current_bucket),
            )
            compressed += cursor.rowcount

            # Compress process CPU metrics
            cursor.execute(
                """
                INSERT INTO process_cpu_metrics_1m (
                    bucket_start, bucket_end,
                    process_name, pid,
                    cpu_percent_avg, cpu_power_w_avg
                )
                SELECT
                    (timestamp / 60) * 60 as bucket_start,
                    (timestamp / 60) * 60 + 60 as bucket_end,
                    process_name, pid,
                    AVG(cpu_percent) as cpu_percent_avg,
                    AVG(cpu_power_w) as cpu_power_w_avg
                FROM process_cpu_metrics_raw
                WHERE timestamp >= ? AND timestamp < ?
                GROUP BY (timestamp / 60), process_name, pid
                """,
                (last_bucket, current_bucket),
            )
            compressed += cursor.rowcount

            self.conn.commit()

        return compressed

    def compress_to_1h(self) -> int:
        """Compress 1-minute metrics to 1-hour buckets.

        Compresses data from 1-minute tables into 1-hour aggregated tables
        using bucket_start/bucket_end for proper time-windowed aggregation.

        Returns:
            Number of rows compressed.
        """
        cursor = self.conn.cursor()
        compressed = 0

        # Find the latest timestamp in 1h tables
        cursor.execute(
            """
            SELECT COALESCE(MAX(bucket_end), 0) as last_bucket
            FROM system_metrics_1h
            """
        )
        result = cursor.fetchone()
        last_bucket = result["last_bucket"] if result else 0

        # Current hour bucket
        current_time = int(time.time())
        current_bucket = (current_time // 3600) * 3600

        # Only compress if we have data from a previous hour
        if current_bucket > last_bucket:
            # Compress system metrics
            cursor.execute(
                """
                INSERT INTO system_metrics_1h (
                    bucket_start, bucket_end,
                    cpu_percent_avg, cpu_temperature_c_avg,
                    cpu_power_w_avg, gpu_usage_avg,
                    gpu_memory_used_mb_avg, gpu_temperature_c_avg,
                    gpu_fan_speed_rpm_avg, gpu_power_w_avg,
                    memory_used_mb_avg, memory_percent_avg,
                    system_power_w_avg
                )
                SELECT
                    bucket_start,
                    bucket_end,
                    AVG(cpu_percent_avg) as cpu_percent_avg,
                    AVG(cpu_temperature_c_avg) as cpu_temperature_c_avg,
                    AVG(cpu_power_w_avg) as cpu_power_w_avg,
                    AVG(gpu_usage_avg) as gpu_usage_avg,
                    AVG(gpu_memory_used_mb_avg) as gpu_memory_used_mb_avg,
                    AVG(gpu_temperature_c_avg) as gpu_temperature_c_avg,
                    AVG(gpu_fan_speed_rpm_avg) as gpu_fan_speed_rpm_avg,
                    AVG(gpu_power_w_avg) as gpu_power_w_avg,
                    AVG(memory_used_mb_avg) as memory_used_mb_avg,
                    AVG(memory_percent_avg) as memory_percent_avg,
                    AVG(system_power_w_avg) as system_power_w_avg
                FROM system_metrics_1m
                WHERE bucket_start >= ? AND bucket_start < ?
                GROUP BY bucket_start
                """,
                (last_bucket, current_bucket),
            )
            compressed += cursor.rowcount

            # Compress server metrics
            cursor.execute(
                """
                INSERT INTO server_metrics_1h (
                    bucket_start, bucket_end,
                    prompt_tokens_total, prompt_tokens_seconds,
                    tokens_predicted_total, predicted_tokens_seconds,
                    requests_processing_avg, requests_deferred_avg
                )
                SELECT
                    bucket_start,
                    bucket_end,
                    SUM(prompt_tokens_total) as prompt_tokens_total,
                    SUM(prompt_tokens_seconds) as prompt_tokens_seconds,
                    SUM(tokens_predicted_total) as tokens_predicted_total,
                    SUM(predicted_tokens_seconds) as predicted_tokens_seconds,
                    AVG(requests_processing_avg) as requests_processing_avg,
                    AVG(requests_deferred_avg) as requests_deferred_avg
                FROM server_metrics_1m
                WHERE bucket_start >= ? AND bucket_start < ?
                GROUP BY bucket_start
                """,
                (last_bucket, current_bucket),
            )
            compressed += cursor.rowcount

            # Compress process GPU metrics
            cursor.execute(
                """
                INSERT INTO process_gpu_metrics_1h (
                    bucket_start, bucket_end,
                    process_name, pid,
                    gpu_utilization_avg, gpu_memory_mb_avg
                )
                SELECT
                    bucket_start,
                    bucket_end,
                    process_name, pid,
                    AVG(gpu_utilization_avg) as gpu_utilization_avg,
                    AVG(gpu_memory_mb_avg) as gpu_memory_mb_avg
                FROM process_gpu_metrics_1m
                WHERE bucket_start >= ? AND bucket_start < ?
                GROUP BY bucket_start, process_name, pid
                """,
                (last_bucket, current_bucket),
            )
            compressed += cursor.rowcount

            # Compress process CPU metrics
            cursor.execute(
                """
                INSERT INTO process_cpu_metrics_1h (
                    bucket_start, bucket_end,
                    process_name, pid,
                    cpu_percent_avg, cpu_power_w_avg
                )
                SELECT
                    bucket_start,
                    bucket_end,
                    process_name, pid,
                    AVG(cpu_percent_avg) as cpu_percent_avg,
                    AVG(cpu_power_w_avg) as cpu_power_w_avg
                FROM process_cpu_metrics_1m
                WHERE bucket_start >= ? AND bucket_start < ?
                GROUP BY bucket_start, process_name, pid
                """,
                (last_bucket, current_bucket),
            )
            compressed += cursor.rowcount

            self.conn.commit()

        return compressed
