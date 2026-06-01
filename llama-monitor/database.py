"""SQLite database initialization and management for llama-monitor."""

import sqlite3
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
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self._initialize_schema()
        return self.conn

    def close(self) -> None:
        """Close database connection."""
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
                requests_deferred INTEGER
            )
            """
        )

        # 1-minute compressed server metrics
        cursor.execute(
            """
            CREATE TABLE server_metrics_1m (
                timestamp TEXT PRIMARY KEY,
                prompt_tokens_total INTEGER,
                prompt_tokens_seconds REAL,
                tokens_predicted_total INTEGER,
                predicted_tokens_seconds REAL,
                requests_processing INTEGER,
                requests_deferred INTEGER
            )
            """
        )

        # 1-hour compressed server metrics
        cursor.execute(
            """
            CREATE TABLE server_metrics_1h (
                timestamp TEXT PRIMARY KEY,
                prompt_tokens_total INTEGER,
                prompt_tokens_seconds REAL,
                tokens_predicted_total INTEGER,
                predicted_tokens_seconds REAL,
                requests_processing INTEGER,
                requests_deferred INTEGER
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
                gpu_memory_used INTEGER,
                gpu_memory_total INTEGER,
                gpu_temperature_c REAL,
                gpu_fan_speed_rpm INTEGER,
                gpu_power_w REAL,
                memory_used INTEGER,
                memory_total INTEGER,
                memory_percent REAL,
                system_power_w REAL
            )
            """
        )

        # 1-minute compressed system metrics
        cursor.execute(
            """
            CREATE TABLE system_metrics_1m (
                timestamp TEXT PRIMARY KEY,
                cpu_percent REAL,
                cpu_temperature_c REAL,
                cpu_power_w REAL,
                gpu_usage REAL,
                gpu_memory_used INTEGER,
                gpu_temperature_c REAL,
                gpu_fan_speed_rpm INTEGER,
                gpu_power_w REAL,
                memory_percent REAL,
                system_power_w REAL
            )
            """
        )

        # 1-hour compressed system metrics
        cursor.execute(
            """
            CREATE TABLE system_metrics_1h (
                timestamp TEXT PRIMARY KEY,
                cpu_percent REAL,
                cpu_temperature_c REAL,
                cpu_power_w REAL,
                gpu_usage REAL,
                gpu_memory_used INTEGER,
                gpu_temperature_c REAL,
                gpu_fan_speed_rpm INTEGER,
                gpu_power_w REAL,
                memory_percent REAL,
                system_power_w REAL
            )
            """
        )

    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
        """Create per-process GPU metrics tables."""
        # Raw per-process GPU metrics
        cursor.execute(
            """
            CREATE TABLE process_gpu_metrics_raw (
                timestamp TEXT,
                process_name TEXT,
                pid INTEGER,
                gpu_utilization REAL,
                gpu_memory_mb INTEGER,
                PRIMARY KEY (timestamp, process_name, pid)
            )
            """
        )

        # 1-minute compressed per-process GPU metrics
        cursor.execute(
            """
            CREATE TABLE process_gpu_metrics_1m (
                timestamp TEXT,
                process_name TEXT,
                avg_gpu_utilization REAL,
                avg_gpu_memory_mb REAL,
                PRIMARY KEY (timestamp, process_name)
            )
            """
        )

        # 1-hour compressed per-process GPU metrics
        cursor.execute(
            """
            CREATE TABLE process_gpu_metrics_1h (
                timestamp TEXT,
                process_name TEXT,
                avg_gpu_utilization REAL,
                avg_gpu_memory_mb REAL,
                PRIMARY KEY (timestamp, process_name)
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
            "gpu_memory_used",
            "gpu_memory_total",
            "gpu_temperature_c",
            "gpu_fan_speed_rpm",
            "gpu_power_w",
            "memory_used",
            "memory_total",
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
            metrics.get("gpu_memory_used"),
            metrics.get("gpu_memory_total"),
            metrics.get("gpu_temperature_c"),
            metrics.get("gpu_fan_speed_rpm"),
            metrics.get("gpu_power_w"),
            metrics.get("memory_used"),
            metrics.get("memory_total"),
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
