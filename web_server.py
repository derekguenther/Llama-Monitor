"""Web server for llama-monitor.

This module provides a Flask-based web server that:
- Serves HTML dashboard with Chart.js for visualizations
- Provides REST API endpoints for metrics data
- Uses WebSocket (via Flask-SocketIO) for real-time client updates
- Connects to the aggregator daemon via HTTP API for data

The web server should be started separately from the aggregator daemon.
"""

import json
import logging
import os
import sys
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Suppress Werkzeug/Flask HTTP request logs (default: WARNING level)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('socketio').setLevel(logging.WARNING)
logging.getLogger('engineio').setLevel(logging.WARNING)

from flask import Flask, jsonify, request, send_from_directory, render_template, render_template_string
from flask_socketio import SocketIO, emit

# Local imports
from config import load_config, find_config

# Try to import database
try:
    from db import Database
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

app = Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates')
app.config["SECRET_KEY"] = "llama-monitor-secret-key"

# Configure SocketIO
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

# Global metrics_cache reference (set by start_server())
_metrics_cache: Optional[Any] = None


def get_config() -> Any:
    """Get configuration."""
    config_path = find_config()
    return load_config(config_path)


# Shared Database instance for read-only access. Centralizing to a single
# connection (instead of opening a new one per request) removes the concurrent
# multi-connection access that corrupted the database file.
_db_instance: Optional[Any] = None
_db_path: Optional[str] = None


def _get_db(db_path: str) -> "Database":
    """Return a shared, thread-safe Database instance for reads.

    Reuses one connection for all web-server read requests rather than opening
    a new sqlite3 connection per request. The Database class guards access with
    an RLock (check_same_thread=False), so it is safe to share across request
    threads. WAL mode (set in Database.connect) keeps this reader safe alongside
    the aggregator's writer.

    Args:
        db_path: Path to the SQLite database file

    Returns:
        A shared Database instance
    """
    global _db_instance, _db_path
    if _db_instance is None or _db_path != db_path:
        _db_instance = Database(db_path)
        _db_instance.connect()
        _db_path = db_path
    return _db_instance


def transform_system_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform flat system metrics keys to nested structure for frontend.

    The database stores system metrics with flat keys (cpu_percent, gpu_usage, etc.)
    but the frontend expects nested structure (system.cpu.percent, system.gpu.usage).

    Args:
        data: System metrics dictionary with flat keys

    Returns:
        System metrics dictionary with nested structure
    """
    def safe_float(value, default=0):
        """Convert None or non-numeric values to default."""
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    return {
        "cpu": {
            "percent": safe_float(data.get("cpu_percent")),
            "cores": data.get("cpu_cores", []),
            "count": data.get("cpu_count", 0),
            "power_w": safe_float(data.get("cpu_power_w")),
        },
        "gpu": {
            "usage": safe_float(data.get("gpu_usage")),
            "memory_used": safe_float(data.get("gpu_memory_used")),
            "memory_total": safe_float(data.get("gpu_memory_total")),
            "temperature_c": safe_float(data.get("gpu_temperature_c")),
            "fan_speed_rpm": safe_float(data.get("gpu_fan_speed_rpm")),
            "power_w": safe_float(data.get("gpu_power_w")),
        },
        "memory": {
            "used": safe_float(data.get("memory_used")),
            "total": safe_float(data.get("memory_total")),
            "percent": safe_float(data.get("memory_percent")),
            "available": safe_float(data.get("memory_available")),
        },
        "system": {
            "power_w": safe_float(data.get("system_power_w")),
        },
        "timestamp": data.get("timestamp", ""),
    }


def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
    """Fetch latest metrics from SQLite database.

    Args:
        db_path: Path to SQLite database

    Returns:
        Metrics data dictionary or None if database unavailable
    """
    try:
        db = _get_db(db_path)
        row = db.execute_query(
            """
            SELECT timestamp, server_data, system_data, cost_data
            FROM combined_metrics
            ORDER BY timestamp DESC
            LIMIT 1
            """
        )

        if row:
            system_data = json.loads(row["system_data"])
            return {
                "timestamp": row["timestamp"],
                "server": json.loads(row["server_data"]),
                "system": transform_system_metrics(system_data),
                "cost": json.loads(row["cost_data"]),
            }
    except Exception:
        pass

    return None


@app.route("/")
def index() -> str:
    """Serve the main dashboard HTML."""
    config = get_config()
    port = config.get("web.http_port", 8080)

    # Prefer user-edited settings from the DB (the source the /settings page
    # writes to), falling back to config.yaml defaults. This keeps the
    # dashboard consistent with what the user configures on the settings page.
    cost_rate = config.get("electricity.cost_rate", 0.12)
    refresh_rate = config.get("web.refresh_rate", 1)
    show_cost = config.get("web.show_cost", True)
    db = get_db()
    if db:
        cost_rate = db.get_cost_rate()
        refresh_rate = db.get_setting("web_refresh_rate", refresh_rate)
        show_cost_setting = db.get_setting("show_cost", None)
        if show_cost_setting is not None:
            show_cost = show_cost_setting.lower() in ("true", "1", "yes")
        try:
            refresh_rate = int(refresh_rate)
        except (ValueError, TypeError):
            refresh_rate = 1

    return render_template(
        "index.html",
        server_url=config.get("server.url", f"http://localhost:{port}"),
        cost_rate=cost_rate,
        refresh_rate=refresh_rate,
        show_cost=show_cost
    )


def _transform_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Transform flat system metrics to nested structure for frontend.
    
    The aggregator/cache stores system metrics flat (cpu_percent, gpu_usage, etc.)
    but the frontend expects nested (system.cpu.percent, system.gpu.usage, etc.).
    """
    if metrics and "system" in metrics and isinstance(metrics["system"], dict):
        system = metrics["system"]
        # Check if system is flat (has cpu_percent) or already nested (has cpu.percent)
        if "cpu_percent" in system or "gpu_usage" in system:
            metrics["system"] = transform_system_metrics(system)
    return metrics


@app.route("/api/metrics/latest")
def api_latest_metrics():
    """Return latest metrics from metrics_cache, aggregator, or database."""
    # Try metrics_cache first (shared with aggregator)
    if _metrics_cache is not None:
        try:
            cached = _metrics_cache.get()
            if cached:
                return jsonify(_transform_metrics(cached))
        except Exception:
            pass

    # Fallback to database (already transformed by fetch_metrics_from_database)
    config = get_config()
    db_path = config.get("database.path", "llama-monitor.db")
    metrics = fetch_metrics_from_database(db_path)

    if metrics:
        return jsonify(metrics)

    # Return empty data structure instead of 404
    return jsonify({
        "server": {},
        "system": {},
        "cost": None,
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/metrics")
def api_metrics():
    """Alias for /api/metrics/latest for backwards compatibility."""
    return api_latest_metrics()


@app.route("/api/metrics/latest-db")
def api_latest_metrics_db():
    """Return latest metrics from database directly."""
    config = get_config()
    db_path = config.get("database.path", "llama-monitor.db")
    metrics = fetch_metrics_from_database(db_path)

    if metrics:
        return jsonify(metrics)

    # Return empty data structure instead of 404
    return jsonify({
        "server": {},
        "system": {},
        "cost": None,
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/metrics/range")
def api_range_metrics():
    """Return metrics within a time range."""
    config = get_config()
    db_path = config.get("database.path", "llama-monitor.db")

    start = request.args.get("start")
    end = request.args.get("end")
    limit = request.args.get("limit", 100, type=int)

    try:
        db = _get_db(db_path)

        query = "SELECT * FROM combined_metrics WHERE 1=1"
        params = []

        if start:
            query += " AND timestamp >= ?"
            params.append(start)
        if end:
            query += " AND timestamp <= ?"
            params.append(end)

        query += " ORDER BY timestamp DESC LIMIT ?"

        rows = db.execute_all(query, params + [limit])

        results = []
        for row in rows:
            result = dict(row)
            for field in ["server_data", "system_data", "cost_data"]:
                if field in result and result[field]:
                    try:
                        result[field] = json.loads(result[field])
                    except json.JSONDecodeError:
                        pass
            results.append(result)

        return jsonify({
            "start": start,
            "end": end,
            "limit": limit,
            "count": len(results),
            "data": results,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/metrics/monthly-cost")
def api_monthly_cost():
    """Return monthly cost data for the last 30 days."""
    config = get_config()
    db_path = config.get("database.path", "llama-monitor.db")

    try:
        db = _get_db(db_path)

        # Get monthly energy data
        monthly_energy = db.get_monthly_energy(days=30)

        # Calculate cost for each day
        cost_rate = db.get_cost_rate()
        monthly_cost_data = []
        for entry in monthly_energy:
            total_wh = entry.get("total_wh", 0)
            cost_usd = (total_wh / 1000) * cost_rate
            monthly_cost_data.append({
                "date": entry.get("date", ""),
                "total_wh": total_wh,
                "gpu_wh": entry.get("gpu_wh", 0),
                "cpu_wh": entry.get("cpu_wh", 0),
                "cost_usd": cost_usd,
            })

        return jsonify({
            "success": True,
            "cost_rate": cost_rate,
            "data": monthly_cost_data,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/metrics/historical")
def api_historical_metrics():
    """Return historical metrics for a specified timeframe.

    Query params:
    - timeframe: Predefined period (hour, day, week, month)
    - start: Start timestamp (ISO format or Unix epoch)
    - end: End timestamp (ISO format or Unix epoch)
    - limit: Maximum number of data points (default: 1000)
    - sample: Sample interval in seconds (default: 60 for 1-minute intervals)
    """
    config = get_config()
    db_path = config.get("database.path", "llama-monitor.db")

    timeframe = request.args.get("timeframe", "day")
    start = request.args.get("start")
    end = request.args.get("end")
    limit = request.args.get("limit", 1000, type=int)
    sample_interval = request.args.get("sample", 60, type=int)

    try:
        db = _get_db(db_path)

        # Calculate time range based on timeframe if not provided
        now = datetime.now()
        if start is None:
            if timeframe == "hour":
                start_dt = now - timedelta(hours=1)
            elif timeframe == "day":
                start_dt = now - timedelta(days=1)
            elif timeframe == "week":
                start_dt = now - timedelta(weeks=1)
            elif timeframe == "month":
                start_dt = now - timedelta(days=30)
            else:
                start_dt = now - timedelta(hours=1)
            start = start_dt.isoformat()

        if end is None:
            end = now.isoformat()

        # Query system metrics with sampling
        system_query = """
            SELECT
                timestamp,
                AVG(cpu_percent) as cpu_percent,
                AVG(gpu_usage) as gpu_usage,
                AVG(gpu_memory_used_mb) as gpu_memory_used_mb,
                AVG(gpu_power_w) as gpu_power_w,
                AVG(cpu_power_w) as cpu_power_w,
                AVG(memory_used_mb) as memory_used_mb,
                AVG(system_power_w) as system_power_w
            FROM system_metrics_raw
            WHERE timestamp >= strftime('%s', ?) AND timestamp <= strftime('%s', ?)
            GROUP BY (timestamp / ?)
            ORDER BY timestamp ASC
        """

        # Query server metrics with sampling
        server_query = """
            SELECT
                timestamp,
                AVG(prompt_tokens_total) as prompt_tokens_total,
                AVG(tokens_predicted_total) as tokens_predicted_total,
                AVG(predicted_tokens_seconds) as predicted_tokens_seconds,
                AVG(requests_processing) as requests_processing,
                AVG(slots_active) as slots_active
            FROM server_metrics_raw
            WHERE timestamp >= strftime('%s', ?) AND timestamp <= strftime('%s', ?)
            GROUP BY (timestamp / ?)
            ORDER BY timestamp ASC
        """

        system_rows = db.execute_all(system_query, (start, end, sample_interval))

        server_rows = db.execute_all(server_query, (start, end, sample_interval))

        # Apply limit to results if specified
        if limit and limit > 0:
            system_rows = system_rows[-limit:]
            server_rows = server_rows[-limit:]

        # Process system metrics
        system_data = []
        for row in system_rows:
            system_data.append({
                "timestamp": row["timestamp"],
                "cpu_percent": row["cpu_percent"],
                "gpu_usage": row["gpu_usage"],
                "gpu_memory_used_mb": row["gpu_memory_used_mb"],
                "gpu_power_w": row["gpu_power_w"],
                "cpu_power_w": row["cpu_power_w"],
                "memory_used_mb": row["memory_used_mb"],
                "system_power_w": row["system_power_w"],
            })

        # Process server metrics
        server_data = []
        for row in server_rows:
            server_data.append({
                "timestamp": row["timestamp"],
                "prompt_tokens_total": row["prompt_tokens_total"],
                "tokens_predicted_total": row["tokens_predicted_total"],
                "predicted_tokens_seconds": row["predicted_tokens_seconds"],
                "requests_processing": row["requests_processing"],
                "slots_active": row["slots_active"],
            })

        return jsonify({
            "timeframe": timeframe,
            "start": start,
            "end": end,
            "sample_interval": sample_interval,
            "count": len(system_data),
            "system": system_data,
            "server": server_data,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/metrics/historical/range")
def api_historical_range():
    """Return historical metrics for a custom time range.

    Query params:
    - start: Start timestamp (ISO format)
    - end: End timestamp (ISO format)
    - limit: Maximum number of records (default: 5000)
    """
    config = get_config()
    db_path = config.get("database.path", "llama-monitor.db")

    start = request.args.get("start")
    end = request.args.get("end")
    limit = request.args.get("limit", 5000, type=int)

    import sqlite3

    if not start or not end:
        return jsonify({"error": "start and end timestamps are required"}), 400

    try:
        db = _get_db(db_path)

        # Get system metrics
        system_rows = db.execute_all(
            """
            SELECT
                timestamp,
                cpu_percent,
                gpu_usage,
                gpu_memory_used_mb,
                gpu_power_w,
                cpu_power_w,
                memory_used_mb,
                system_power_w
            FROM system_metrics_raw
            WHERE timestamp >= strftime('%s', ?) AND timestamp <= strftime('%s', ?)
            ORDER BY timestamp ASC
            LIMIT ?
            """,
            (start, end, limit)
        )

        # Get server metrics
        server_rows = db.execute_all(
            """
            SELECT
                timestamp,
                prompt_tokens_total,
                tokens_predicted_total,
                predicted_tokens_seconds,
                requests_processing,
                slots_active
            FROM server_metrics_raw
            WHERE timestamp >= strftime('%s', ?) AND timestamp <= strftime('%s', ?)
            ORDER BY timestamp ASC
            LIMIT ?
            """,
            (start, end, limit)
        )

        system_data = []
        for row in system_rows:
            system_data.append({
                "timestamp": row["timestamp"],
                "cpu_percent": row["cpu_percent"],
                "gpu_usage": row["gpu_usage"],
                "gpu_memory_used_mb": row["gpu_memory_used_mb"],
                "gpu_power_w": row["gpu_power_w"],
                "cpu_power_w": row["cpu_power_w"],
                "memory_used_mb": row["memory_used_mb"],
                "system_power_w": row["system_power_w"],
            })

        server_data = []
        for row in server_rows:
            server_data.append({
                "timestamp": row["timestamp"],
                "prompt_tokens_total": row["prompt_tokens_total"],
                "tokens_predicted_total": row["tokens_predicted_total"],
                "predicted_tokens_seconds": row["predicted_tokens_seconds"],
                "requests_processing": row["requests_processing"],
                "slots_active": row["slots_active"],
            })

        return jsonify({
            "start": start,
            "end": end,
            "count": len(system_data),
            "system": system_data,
            "server": server_data,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/status")
def api_status():
    """Return aggregator status (standalone; no separate daemon)."""
    return jsonify({"status": "standalone", "aggregator_available": False})


@app.route("/api/server/stop", methods=["POST"])
def api_stop_server():
    """Stop the web server gracefully."""
    try:
        # Get the shutdown function from the request environment
        func = request.environ.get('werkzeug.server.shutdown')
        if func:
            func()
            return jsonify({"success": True, "message": "Server is shutting down..."})

       # If werkzeug shutdown is not available, try alternative approach
        # Note: Flask-SocketIO doesn't have a clean shutdown method
        # The server will stop when the main process terminates
        import os
        import signal
        # Send SIGTERM to self (works on Unix-like systems)
        os.kill(os.getpid(), signal.SIGTERM)
        return jsonify({"success": True, "message": "Server is shutting down..."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/server/restart", methods=["POST"])
def api_restart_server():
    """Restart the web server by spawning a new process and shutting down the current one."""
    try:
        import os
        import sys
        import subprocess
        import time
        import signal

        # Get the path to the current Python interpreter and main.py
        python_exec = sys.executable
        script_path = os.path.abspath(sys.argv[0])

        # Create a new process group and start the server in a new process
        def restart_server():
            time.sleep(0.5)  # Small delay to allow response to be sent
            # Start new server process in a new process group
            new_process = subprocess.Popen(
                [python_exec, script_path] + sys.argv[1:],
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Give the new process a moment to initialize
            time.sleep(1)
            # Terminate the current process
            os.kill(os.getpid(), signal.SIGTERM)

        # Start restart in a thread so the response can be sent first
        threading.Thread(target=restart_server).start()

        return jsonify({"success": True, "message": "Server is restarting..."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def get_db():
    """Get the shared database instance for settings access.

    Returns the same thread-safe Database instance used by all web-server reads,
    so settings reads/writes share one connection instead of opening a new one
    per request.
    """
    if not DB_AVAILABLE:
        return None
    config = get_config()
    db_path = config.get("database.path", "llama-monitor.db")
    return _get_db(db_path)


@app.route("/settings")
def settings_page():
    """Serve the settings page HTML."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Llama Monitor - Settings</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: #16213e;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .header h1 {
            font-size: 1.5rem;
            color: #00d4ff;
        }

        .header a {
            color: #00d4ff;
            text-decoration: none;
        }

        .card {
            background: #16213e;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
        }

        .card h2 {
            font-size: 1.1rem;
            color: #00d4ff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #2a3b5c;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            font-size: 0.9rem;
            color: #888;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .form-group input[type="number"],
        .form-group input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            background: #0d111d;
            border: 1px solid #2a3b5c;
            border-radius: 6px;
            color: #eee;
            font-family: 'Courier New', monospace;
            font-size: 1rem;
            transition: border-color 0.2s;
        }

        .form-group input:focus {
            outline: none;
            border-color: #00d4ff;
        }

        .form-group .hint {
            font-size: 0.75rem;
            color: #666;
            margin-top: 5px;
        }

        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
            accent-color: #00d4ff;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 600;
            transition: all 0.2s;
        }

        .btn-primary {
            background: #00d4ff;
            color: #1a1a2e;
        }

        .btn-primary:hover {
            background: #00a8cc;
        }

        .btn-secondary {
            background: #2a3b5c;
            color: #eee;
        }

        .btn-secondary:hover {
            background: #3a4b6c;
        }

        .btn-link {
            background: none;
            border: none;
            color: #00d4ff;
            cursor: pointer;
            font-size: 0.9rem;
        }

        .btn-link:hover {
            text-decoration: underline;
        }

        .feedback {
            padding: 12px 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            display: none;
        }

        .feedback.success {
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            color: #00ff88;
            display: block;
        }

        .feedback.error {
            background: rgba(255, 71, 87, 0.1);
            border: 1px solid rgba(255, 71, 87, 0.3);
            color: #ff4757;
            display: block;
        }

        .settings-section {
            margin-bottom: 25px;
            padding-bottom: 25px;
            border-bottom: 1px solid #2a3b5c;
        }

        .settings-section:last-child {
            border-bottom: none;
        }

        .section-title {
            font-size: 0.9rem;
            color: #00d4ff;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .value-display {
            color: #00ff88;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fa-solid fa-sliders"></i> Settings</h1>
            <a href="/" class="btn-link"><i class="fa-solid fa-arrow-left"></i> Back to Dashboard</a>
        </div>

        <div id="feedback" class="feedback"></div>

        <form id="settings-form">
            <div class="settings-section">
                <h2 class="section-title">Display Settings</h2>

                <div class="form-group">
                    <label for="web_refresh_rate">Refresh Rate (seconds)</label>
                    <input type="number" id="web_refresh_rate" name="web_refresh_rate" min="1" max="60" step="1">
                    <div class="hint">How often the dashboard updates</div>
                </div>

                <div class="form-group">
                    <div class="checkbox-group">
                        <input type="checkbox" id="show_cost" name="show_cost">
                        <label for="show_cost">Show Cost Display</label>
                    </div>
                </div>

                <div class="form-group">
                    <div class="checkbox-group">
                        <input type="checkbox" id="show_temps" name="show_temps">
                        <label for="show_temps">Show Temperature Display</label>
                    </div>
                </div>
            </div>

            <div class="settings-section">
                <h2 class="section-title">Cost Settings</h2>

                <div class="form-group">
                    <label for="cost_rate">Electricity Cost ($/kWh)</label>
                    <input type="number" id="cost_rate" name="cost_rate" step="0.001" min="0">
                    <div class="hint">Current electricity rate for cost calculations</div>
                </div>

                <div class="form-group">
                    <label for="idle_baseline_w">Idle Baseline Power (W)</label>
                    <input type="number" id="idle_baseline_w" name="idle_baseline_w" step="1" min="0">
                    <div class="hint">System power draw when idle, used for idle baseline tracking</div>
                </div>
            </div>

            <div class="settings-section">
                <h2 class="section-title">Current Values</h2>
                <div id="current-values" style="font-size: 0.85rem; color: #888;">
                    <!-- Values will be populated by JavaScript -->
                </div>
            </div>

            <div style="display: flex; gap: 10px; justify-content: flex-end;">
                <button type="button" class="btn btn-secondary" id="reset-btn"><i class="fa-solid fa-rotate-right"></i> Reset to Default</button>
                <button type="submit" class="btn btn-primary"><i class="fa-solid fa-save"></i> Save Settings</button>
            </div>
        </form>

        <div class="settings-section">
            <h2 class="section-title">Server Control</h2>
            <div class="card">
                <div class="form-group">
                    <label>Server Status</label>
                    <div id="server-status-display" style="padding: 10px; background: #0d111d; border-radius: 6px; font-family: 'Courier New', monospace; color: #00ff88;">
                        <i class="fa-solid fa-circle-notch fa-spin"></i> Checking...
                    </div>
                </div>

                <div class="form-group">
                    <div class="checkbox-group">
                        <input type="checkbox" id="auto-reload" checked>
                        <label for="auto-reload">Auto-refresh page after restart</label>
                    </div>
                </div>

                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <button type="button" class="btn btn-secondary" id="stop-btn" style="flex: 1; min-width: 120px;"><i class="fa-solid fa-stop"></i> Stop Server</button>
                    <button type="button" class="btn btn-primary" id="restart-btn" style="flex: 1; min-width: 120px;"><i class="fa-solid fa-rotate-right"></i> Restart Server</button>
                </div>
                <div class="hint" style="margin-top: 10px;">
                    <i class="fa-solid fa-info-circle"></i> Use these buttons to stop/restart the server for testing. Auto-refresh will reload the page after restart.
                </div>
            </div>
        </div>
    </form>
    </div>

    <script>
        // Load settings on page load
        document.addEventListener('DOMContentLoaded', async function() {
            await loadSettings();
        });

        async function loadSettings() {
            try {
                const response = await fetch('/api/settings');
                if (!response.ok) throw new Error('Failed to load settings');
                const settings = await response.json();

                // Populate form fields
                document.getElementById('web_refresh_rate').value = settings.web_refresh_rate || 1;
                document.getElementById('show_cost').checked = settings.show_cost !== false;
                document.getElementById('show_temps').checked = settings.show_temps !== false;
                document.getElementById('cost_rate').value = settings.cost_rate || 0.12;
                document.getElementById('idle_baseline_w').value = settings.idle_baseline_w || 40;

                // Display current values
                document.getElementById('current-values').innerHTML = `
                    <div><strong>Refresh Rate:</strong> <span class="value-display">${settings.web_refresh_rate || 1}s</span></div>
                    <div><strong>Cost Display:</strong> <span class="value-display">${settings.show_cost !== false ? 'Enabled' : 'Disabled'}</span></div>
                    <div><strong>Temp Display:</strong> <span class="value-display">${settings.show_temps !== false ? 'Enabled' : 'Disabled'}</span></div>
                    <div><strong>Electricity Cost:</strong> <span class="value-display">$${parseFloat(settings.cost_rate || 0.12).toFixed(2)}/kWh</span></div>
                    <div><strong>Idle Baseline:</strong> <span class="value-display">${parseFloat(settings.idle_baseline_w || 40).toFixed(0)} W</span></div>
                `;
            } catch (error) {
                showFeedback('Error loading settings: ' + error.message, 'error');
            }
        }

        async function saveSettings() {
            const settings = {
                web_refresh_rate: parseInt(document.getElementById('web_refresh_rate').value) || 1,
                show_cost: document.getElementById('show_cost').checked,
                show_temps: document.getElementById('show_temps').checked,
                cost_rate: parseFloat(document.getElementById('cost_rate').value) || 0.12,
                idle_baseline_w: parseFloat(document.getElementById('idle_baseline_w').value) || 40
            };

            try {
                const response = await fetch('/api/settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(settings)
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to save settings');
                }

                showFeedback('Settings saved successfully!', 'success');
                await loadSettings();
            } catch (error) {
                showFeedback('Error saving settings: ' + error.message, 'error');
            }
        }

        function showFeedback(message, type) {
            const feedback = document.getElementById('feedback');
            feedback.textContent = message;
            feedback.className = 'feedback ' + type;

            // Auto-hide after 5 seconds
            setTimeout(function() {
                feedback.style.display = 'none';
            }, 5000);
        }

        // Form submission
        document.getElementById('settings-form').addEventListener('submit', function(e) {
            e.preventDefault();
            saveSettings();
        });

        // Reset button
        document.getElementById('reset-btn').addEventListener('click', async function() {
            if (confirm('Reset all settings to default values?')) {
                try {
                    const response = await fetch('/api/settings/reset', { method: 'POST' });
                    if (!response.ok) throw new Error('Failed to reset settings');
                    showFeedback('Settings reset to defaults', 'success');
                    await loadSettings();
                } catch (error) {
                    showFeedback('Error resetting settings: ' + error.message, 'error');
                }
            }
        });

        // Server status display
        async function checkServerStatus() {
            try {
                const response = await fetch('/api/status');
                if (response.ok) {
                    const data = await response.json();
                    const statusDisplay = document.getElementById('server-status-display');
                    if (data.status === 'running' || data.status === 'standalone') {
                        statusDisplay.innerHTML = `<i class="fa-solid fa-circle" style="color: #00ff88;"></i> Running`;
                    } else {
                        statusDisplay.innerHTML = `<i class="fa-solid fa-circle" style="color: #ff4757;"></i> Stopped`;
                    }
                }
            } catch (error) {
                document.getElementById('server-status-display').innerHTML = `<i class="fa-solid fa-circle" style="color: #ff4757;"></i> Unknown`;
            }
        }

        // Stop server button
        document.getElementById('stop-btn').addEventListener('click', async function() {
            if (confirm('Are you sure you want to stop the server?')) {
                try {
                    const response = await fetch('/api/server/stop', { method: 'POST' });
                    const data = await response.json();
                    if (data.success) {
                        showFeedback(data.message, 'success');
                        checkServerStatus();
                    } else {
                        showFeedback('Failed to stop server: ' + data.error, 'error');
                    }
                } catch (error) {
                    showFeedback('Error stopping server: ' + error.message, 'error');
                }
            }
        });

        // Restart server button
        document.getElementById('restart-btn').addEventListener('click', async function() {
            if (confirm('Are you sure you want to restart the server? The page will reload.')) {
                try {
                    const response = await fetch('/api/server/restart', { method: 'POST' });
                    const data = await response.json();
                    if (data.success) {
                        showFeedback(data.message, 'success');
                        checkServerStatus();
                        // Reload page after short delay if auto-reload is checked
                        const autoReload = document.getElementById('auto-reload').checked;
                        if (autoReload) {
                            setTimeout(function() {
                                window.location.reload();
                            }, 1500);
                        }
                    } else {
                        showFeedback('Failed to restart server: ' + data.error, 'error');
                    }
                } catch (error) {
                    showFeedback('Error restarting server: ' + error.message, 'error');
                }
            }
        });

        // Check server status on page load
        document.addEventListener('DOMContentLoaded', function() {
            checkServerStatus();
        });
    </script>
</body>
</html>"""
    return render_template_string(html)




@app.route("/cost-comparison")
def cost_comparison_page():
    """Serve the cost comparison page HTML."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Llama Monitor - Cost Comparison</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/socket.io-client@4.7.2/dist/socket.io.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #333;
        }

        .header h1 {
            font-size: 1.5rem;
            color: #00d9ff;
        }

        .card {
            background: #16213e;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid #333;
        }

        .card h2 {
            font-size: 1.1rem;
            color: #00d9ff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #333;
        }

        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        .comparison-table th,
        .comparison-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #2a2a4a;
        }

        .comparison-table th {
            background: #0d111d;
            color: #00d9ff;
            font-weight: 600;
            font-size: 0.9rem;
        }

        .comparison-table td {
            font-size: 0.95rem;
        }

        .comparison-table tr:hover {
            background: rgba(255, 255, 255, 0.05);
        }

        .cost-value {
            font-family: 'Consolas', 'Monaco', monospace;
            font-weight: bold;
            color: #00ff88;
        }

        .rate-value {
            font-family: 'Consolas', 'Monaco', monospace;
            color: #00d9ff;
        }

        .token-count {
            font-family: 'Consolas', 'Monaco', monospace;
            color: #ffbb55;
        }

        .local-server-row {
            background: rgba(0, 255, 136, 0.1);
            border-left: 3px solid #00ff88;
        }

        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #666;
        }

        .empty-state i {
            font-size: 2rem;
            margin-bottom: 10px;
            display: block;
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-block;
        }

        .btn-primary {
            background: #00d9ff;
            color: #1a1a2e;
        }

        .btn-primary:hover {
            background: #00b8d9;
        }

        .btn-secondary {
            background: #2a3b5c;
            color: #eee;
        }

        .btn-secondary:hover {
            background: #3a4b6c;
        }

        .metrics-summary {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }

        .summary-card {
            background: #16213e;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid #333;
        }

        .summary-card h3 {
            font-size: 0.85rem;
            color: #888;
            margin-bottom: 10px;
        }

        .summary-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #00ff88;
            font-family: 'Consolas', 'Monaco', monospace;
        }

        .summary-label {
            font-size: 0.8rem;
            color: #666;
            margin-top: 5px;
        }

        .refresh-section {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            align-items: center;
        }

        .refresh-section .btn {
            flex: 1;
        }

        @media (max-width: 600px) {
            .metrics-summary {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fa-solid fa-exchange-alt"></i> Cost Comparison</h1>
        <a href="/" class="btn btn-secondary"><i class="fa-solid fa-arrow-left"></i> Back to Dashboard</a>
    </div>

    <div class="refresh-section">
        <button class="btn btn-primary" id="refresh-btn"><i class="fa-solid fa-sync"></i> Refresh Data</button>
    </div>

    <div class="metrics-summary">
        <div class="summary-card">
            <h3>Total Tokens</h3>
            <div class="summary-value" id="total-tokens">0</div>
            <div class="summary-label">Tokens processed today</div>
        </div>
        <div class="summary-card">
            <h3>Local Server Rate</h3>
            <div class="summary-value" id="local-rate">$0.0000</div>
            <div class="summary-label">per token (electricity cost)</div>
        </div>
        <div class="summary-card">
            <h3>Best Value</h3>
            <div class="summary-value" id="best-value">-</div>
            <div class="summary-label">lowest cost per token</div>
        </div>
    </div>

    <div class="card">
        <h2>Vendor Cost Comparison</h2>
        <div id="comparison-container">
            <div class="empty-state">
                <i class="fa-solid fa-server"></i>
                <p>Loading vendor comparison data...</p>
            </div>
        </div>
    </div>

    <script>
        async function fetchComparisonData() {
            try {
                const response = await fetch('/api/vendor/comparison');
                if (!response.ok) {
                    throw new Error('Bad response');
                }

                const data = await response.json();

                if (data.success) {
                    updateComparisonDisplay(data);
                } else {
                    throw new Error(data.error || 'Failed to fetch comparison data');
                }
            } catch (error) {
                console.error('Error fetching comparison data:', error);
                document.getElementById('comparison-container').innerHTML = `
                    <div class="empty-state">
                        <i class="fa-solid fa-exclamation-triangle"></i>
                        <p>Error loading comparison data: ${error.message}</p>
                        <p style="font-size: 0.85rem; color: #666; margin-top: 10px;">
                            Make sure the database has vendor rates configured.
                        </p>
                    </div>
                `;
            }
        }

        function updateComparisonDisplay(data) {
            const totalTokens = data.total_tokens || 0;
            const localRate = data.local_server_rate || 0;
            const comparison = data.comparison || [];

            // Update summary cards
            document.getElementById('total-tokens').textContent = totalTokens.toLocaleString();
            document.getElementById('local-rate').textContent = '$' + formatRate(localRate) + '/token';

            // Find best value (lowest cost per token)
            if (comparison.length > 0) {
                // Sort by cost to find best value
                const sorted = [...comparison].sort((a, b) => a.cost_usd - b.cost_usd);
                const bestValue = sorted[0];
                document.getElementById('best-value').textContent = bestValue.vendor_name;
            }

            // Generate comparison table
            if (comparison.length === 0) {
                document.getElementById('comparison-container').innerHTML = `
                    <div class="empty-state">
                        <i class="fa-solid fa-list"></i>
                        <p>No vendor rates configured</p>
                        <p style="font-size: 0.85rem; color: #666; margin-top: 10px;">
                            Add vendor rates in Settings to see cost comparisons.
                        </p>
                        <a href="/settings" class="btn btn-primary" style="margin-top: 15px;">
                            <i class="fa-solid fa-sliders"></i> Go to Settings
                        </a>
                    </div>
                `;
                return;
            }

            let tableHTML = `
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Vendor</th>
                            <th>Rate ($/token)</th>
                            <th>Tokens</th>
                            <th>Total Cost</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            comparison.forEach(vendor => {
                const isLocal = vendor.is_local_server ? 'local-server-row' : '';
                const rateDisplay = vendor.is_local_server ? '$' + formatRate(vendor.rate_usd_per_token) + '/token' : '$' + formatRate(vendor.rate_usd_per_token) + '/token';
                const costDisplay = '$' + vendor.cost_usd.toFixed(4);

                tableHTML += `
                    <tr class="${isLocal}">
                        <td>${vendor.vendor_name} ${vendor.is_local_server ? '<i class="fa-solid fa-server" title="Local server"></i>' : ''}</td>
                        <td class="rate-value">${rateDisplay}</td>
                        <td class="token-count">${totalTokens.toLocaleString()}</td>
                        <td class="cost-value">${costDisplay}</td>
                    </tr>
                `;
            });

            tableHTML += '</tbody></table>';
            document.getElementById('comparison-container').innerHTML = tableHTML;
        }

        function formatRate(rate) {
            if (rate === 0) return '0.0000';
            if (rate < 0.0001) return rate.toFixed(6);
            if (rate < 0.01) return rate.toFixed(4);
            return rate.toFixed(2);
        }

        // Initial load
        fetchComparisonData();

        // Refresh button
        document.getElementById('refresh-btn').addEventListener('click', fetchComparisonData);
    </script>
</body>
</html>"""
    return render_template_string(html)


@app.route("/api/settings")
def api_get_settings():
    """Get all settings from the database."""
    if not DB_AVAILABLE:
        return jsonify({
            "web_refresh_rate": 1,
            "show_cost": True,
            "show_temps": True,
            "cost_rate": 0.12
        })

    db = get_db()
    if not db:
        return jsonify({
            "web_refresh_rate": 1,
            "show_cost": True,
            "show_temps": True,
            "cost_rate": 0.12
        })

    settings = {
        "web_refresh_rate": db.get_setting("web_refresh_rate", "1"),
        "show_cost": db.get_setting("show_cost", "true"),
        "show_temps": db.get_setting("show_temps", "true"),
        "cost_rate": db.get_setting("cost_rate_usd_per_kwh", "0.12"),
        "idle_baseline_w": db.get_setting("idle_baseline_w", "40.0")
    }

    # Convert to appropriate types
    try:
        settings["web_refresh_rate"] = int(settings["web_refresh_rate"])
    except (ValueError, TypeError):
        settings["web_refresh_rate"] = 1

    try:
        settings["show_cost"] = settings["show_cost"].lower() in ("true", "1", "yes")
    except (AttributeError, TypeError):
        settings["show_cost"] = True

    try:
        settings["show_temps"] = settings["show_temps"].lower() in ("true", "1", "yes")
    except (AttributeError, TypeError):
        settings["show_temps"] = True

    try:
        settings["cost_rate"] = float(settings["cost_rate"])
    except (ValueError, TypeError):
        settings["cost_rate"] = 0.12

    try:
        settings["idle_baseline_w"] = float(settings["idle_baseline_w"])
    except (ValueError, TypeError):
        settings["idle_baseline_w"] = 40.0

    return jsonify(settings)


@app.route("/api/settings", methods=["POST"])
def api_set_settings():
    """Set settings in the database."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500

    try:
        # Update each setting that was provided
        if "web_refresh_rate" in data:
            db.set_setting("web_refresh_rate", int(data["web_refresh_rate"]))

        if "show_cost" in data:
            db.set_setting("show_cost", "true" if data["show_cost"] else "false")

        if "show_temps" in data:
            db.set_setting("show_temps", "true" if data["show_temps"] else "false")

        if "cost_rate" in data:
            db.set_setting("cost_rate_usd_per_kwh", float(data["cost_rate"]))

        if "idle_baseline_w" in data:
            db.set_setting("idle_baseline_w", float(data["idle_baseline_w"]))

        return jsonify({"success": True, "message": "Settings saved"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/settings/reset", methods=["POST"])
def api_reset_settings():
    """Reset settings to defaults."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500

    try:
        # Ensure a live connection (execute() does not auto-reconnect).
        db.connect()

        # Delete all settings to reset to defaults (uses the locked connection)
        db.execute("DELETE FROM settings")

        # Re-insert default cost rate
        db.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?)",
            ("cost_rate_usd_per_kwh", "0.12")
        )
        # Re-insert default idle baseline
        db.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?)",
            ("idle_baseline_w", "40.0")
        )

        return jsonify({"success": True, "message": "Settings reset to defaults"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/settings/cost_rate", methods=["POST"])
def api_set_cost_rate():
    """Update the cost rate setting."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500

    data = request.get_json()
    if not data or "cost_rate" not in data:
        return jsonify({"error": "No cost_rate provided"}), 400

    try:
        new_rate = float(data["cost_rate"])
        if new_rate < 0:
            return jsonify({"error": "Cost rate must be non-negative"}), 400

        db.set_cost_rate(new_rate)
        return jsonify({"success": True, "message": "Cost rate updated"})
    except ValueError:
        return jsonify({"error": "Invalid cost rate value"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Graph preferences API endpoints
# ======================================================================

@app.route("/api/settings/graph-preferences", methods=["GET"])
def api_get_graph_preferences():
    """Get graph display preferences."""
    prefs = {
        "chk-gpu-pct": True,
        "chk-cpu-pct": True,
        "chk-gpu-power": False,
        "chk-cpu-power": False,
        "chk-llama-gpu-pct": False,
        "chk-llama-cpu-pct": False,
        "chk-llama-gpu-power": False,
        "chk-llama-cpu-power": False,
    }
    if DB_AVAILABLE:
        db = get_db()
        if db:
            try:
                for key in prefs:
                    val = db.get_setting("graph_" + key, None)
                    if val is not None:
                        prefs[key] = val.lower() in ("true", "1", "yes")
            except Exception:
                pass
    return jsonify(prefs)


@app.route("/api/settings/graph-preferences", methods=["POST"])
def api_set_graph_preferences():
    """Save graph display preferences."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500
    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        for key, value in data.items():
            db.set_setting("graph_" + key, "true" if value else "false")
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Vendor rates API endpoints
# ======================================================================

@app.route("/api/vendor/rates", methods=["GET"])
def api_get_vendor_rates():
    """Get all vendor rates."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500

    try:
        rates = db.get_all_vendor_rates()
        return jsonify({"success": True, "rates": rates})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/vendor/rates", methods=["POST"])
def api_add_vendor_rate():
    """Add a new vendor rate."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500

    try:
        vendor_name = data.get("vendor_name")
        rate_usd_per_token = data.get("rate_usd_per_token", 0)
        is_local_server = data.get("is_local_server", False)

        if not vendor_name:
            return jsonify({"error": "vendor_name is required"}), 400

        success = db.add_vendor_rate(vendor_name, rate_usd_per_token, is_local_server)
        if success:
            return jsonify({"success": True, "message": "Vendor rate added"})
        else:
            return jsonify({"error": "Vendor already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/vendor/rates/<vendor_name>", methods=["PUT"])
def api_update_vendor_rate(vendor_name):
    """Update an existing vendor rate."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500

    try:
        rate_usd_per_token = data.get("rate_usd_per_token")
        is_local_server = data.get("is_local_server")

        success = db.update_vendor_rate(vendor_name, rate_usd_per_token, is_local_server)
        if success:
            return jsonify({"success": True, "message": "Vendor rate updated"})
        else:
            return jsonify({"error": "Vendor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/vendor/rates/<vendor_name>", methods=["DELETE"])
def api_delete_vendor_rate(vendor_name):
    """Delete a vendor rate."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500

    try:
        success = db.delete_vendor_rate(vendor_name)
        if success:
            return jsonify({"success": True, "message": "Vendor rate deleted"})
        else:
            return jsonify({"error": "Vendor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Token cost API endpoints
# ======================================================================

@app.route("/api/token/accumulator", methods=["GET"])
def api_get_token_accumulator():
    """Get today's token tracking statistics."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500

    try:
        stats = db.get_today_token_tracking()
        if stats:
            return jsonify({
                "success": True,
                "data": stats
            })
        else:
            return jsonify({
                "success": True,
                "data": {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "total_tokens": 0,
                    "prompt_tokens": 0,
                    "generated_tokens": 0,
                    "last_update": None
                }
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/vendor/comparison", methods=["GET"])
def api_get_vendor_comparison():
    """Get vendor cost comparison based on today's tokens."""
    if not DB_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    db = get_db()
    if not db:
        return jsonify({"error": "Database not available"}), 500

    try:
        # Calculate local server rate based on electricity cost
        calculator = ElectricityCostCalculator(db)

        # Get today's token stats
        today_stats = calculator.get_today_token_stats()
        if not today_stats:
            return jsonify({
                "success": True,
                "comparison": [],
                "local_server_rate": 0
            })

        # Get vendor rates
        vendor_rates = db.get_all_vendor_rates()

        total_tokens = today_stats.get("total_tokens", 0)

        comparison = []
        for vendor in vendor_rates:
            rate = vendor.get("rate_usd_per_token", 0)
            cost = total_tokens * rate
            comparison.append({
                "vendor_name": vendor["vendor_name"],
                "rate_usd_per_token": rate,
                "total_tokens": total_tokens,
                "cost_usd": cost,
                "is_local_server": vendor.get("is_local_server", False),
            })

        # Calculate local server rate
        local_rate = calculator.calculate_local_server_rate()

        return jsonify({
            "success": True,
            "comparison": comparison,
            "local_server_rate": local_rate,
            "total_tokens": total_tokens
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@socketio.on("connect")
def handle_connect():
    """Handle WebSocket connection."""
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print("Client disconnected")


def run_server(host="0.0.0.0", port=8080, debug=False, verbose=False):
    """Run the web server.

    Args:
        host: Host to bind to
        port: Port to listen on
        debug: Enable debug mode
        verbose: Enable verbose logging (INFO level for werkzeug, socketio, engineio)
    """
    # Configure logging based on verbose flag
    if verbose:
        logging.getLogger('werkzeug').setLevel(logging.INFO)
        logging.getLogger('socketio').setLevel(logging.INFO)
        logging.getLogger('engineio').setLevel(logging.INFO)
    else:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        logging.getLogger('socketio').setLevel(logging.WARNING)
        logging.getLogger('engineio').setLevel(logging.WARNING)

    print(f"llama-monitor web server starting on http://{host}:{port}")
    print("Press Ctrl+C to stop")

    # Use allow_unsafe_werkzeug=True to avoid RuntimeError in production
    # use_reloader=False because the server runs in a background thread
    # (the reloader requires the main thread for signal handling)
    socketio.run(app, host=host, port=port, debug=debug, use_reloader=False, allow_unsafe_werkzeug=True)


# Global server reference for stop_server
_server_thread = None


def start_server(host="0.0.0.0", port=8080, metrics_cache=None, verbose=False, debug=False):
    """Start the web server in a background thread.

    Args:
        host: Host to bind to
        port: Port to listen on
        metrics_cache: Optional MetricsCache instance for sharing data
        verbose: Enable verbose logging (INFO level for werkzeug, socketio, engineio)
    """
    global _server_thread, _metrics_cache

    # Store metrics_cache for use by route handlers
    _metrics_cache = metrics_cache

    print(f"Starting web server on http://{host}:{port}")

    # Create and start server thread
    def run():
        run_server(host=host, port=port, debug=debug, verbose=verbose)

    _server_thread = threading.Thread(target=run, daemon=True)
    _server_thread.start()

    print(f"Web server started on http://{host}:{port}")


def stop_server():
    """Stop the running web server."""
    global _server_thread

    if _server_thread:
        print("Stopping web server...")
        # Note: Flask-SocketIO doesn't have a clean shutdown method
        # The thread will be marked daemon=True so it exits when main process ends
        _server_thread = None
        print("Web server stopped")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="llama-monitor web server")
    parser.add_argument(
        "--host",
        "-H",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8080,
        help="Port to listen on (default: 8080)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging (INFO level for werkzeug, socketio, engineio)",
    )

    args = parser.parse_args()

    run_server(host=args.host, port=args.port, debug=args.debug, verbose=args.verbose)


if __name__ == "__main__":
    main()
