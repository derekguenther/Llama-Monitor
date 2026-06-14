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

from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_socketio import SocketIO, emit

# Local imports
from config import load_config, find_config

# Try to import database
try:
    from db import Database
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

# Try to import aggregator daemon for direct data access
try:
    from aggregator_daemon import Aggregator
    AGGREGATOR_AVAILABLE = True
except ImportError:
    AGGREGATOR_AVAILABLE = False


app = Flask(__name__, static_folder=None)
app.config["SECRET_KEY"] = "llama-monitor-secret-key"

# Configure SocketIO
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

# Global metrics_cache reference (set by start_server())
_metrics_cache: Optional[Any] = None


def get_aggregator() -> Optional[Aggregator]:
    """Get aggregator instance if available."""
    if AGGREGATOR_AVAILABLE:
        return Aggregator()
    return None


def get_config() -> Any:
    """Get configuration."""
    config_path = find_config()
    return load_config(config_path)


def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:
    """Fetch latest metrics from aggregator daemon via HTTP API.

    Returns:
        Metrics data dictionary or None if aggregator unavailable
    """
    import urllib.request
    import urllib.error

    config = get_config()
    port = getattr(config, "web_http_port", 8080)

    try:
        url = f"http://localhost:{port}/api/metrics/latest"
        with urllib.request.urlopen(url, timeout=5) as response:
            return json.loads(response.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, Exception):
        return None


def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
    """Fetch latest metrics from SQLite database.

    Args:
        db_path: Path to SQLite database

    Returns:
        Metrics data dictionary or None if database unavailable
    """
    import sqlite3

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, server_data, system_data, cost_data
            FROM combined_metrics
            ORDER BY timestamp DESC
            LIMIT 1
            """
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "timestamp": row["timestamp"],
                "server": json.loads(row["server_data"]),
                "system": json.loads(row["system_data"]),
                "cost": json.loads(row["cost_data"]),
            }
    except Exception:
        pass

    return None


@app.route("/")
def index() -> str:
    """Serve the main dashboard HTML."""
    config = get_config()
    port = getattr(config, "web_http_port", 8080)
    cost_rate = getattr(config, "cost_rate", 0.12)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Llama Monitor Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/socket.io-client@4.7.2/dist/socket.io.min.js"></script>
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

        .status {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.9rem;
        }

        .indicator-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #00ff88;
        }

        .indicator-dot.offline {
            background: #ff4757;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: #16213e;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #333;
        }

        .card h2 {
            font-size: 1rem;
            color: #00d9ff;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #333;
        }

        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #2a2a4a;
        }

        .metric-row:last-child {
            border-bottom: none;
        }

        .metric-label {
            color: #888;
            font-size: 0.9rem;
        }

        .metric-value {
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 1rem;
            color: #eee;
        }

        .metric-rate {
            font-size: 0.8rem;
            color: #00d9ff;
        }

        .progress-bar {
            height: 6px;
            background: #2a2a4a;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 5px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00d9ff, #00ff88);
            transition: width 0.3s ease;
        }

        .chart-container {
            position: relative;
            height: 200px;
            width: 100%;
        }

        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .btn {
            background: #00d9ff;
            color: #1a1a2e;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
        }

        .btn:hover {
            background: #00b8d9;
        }

        .btn.secondary {
            background: #333;
            color: #eee;
        }

        .btn.secondary:hover {
            background: #444;
        }

        .cost-display {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .cost-display h3 {
            font-size: 0.9rem;
            color: #888;
            margin-bottom: 5px;
        }

        .cost-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #00ff88;
        }

        .cost-sub {
            font-size: 0.85rem;
            color: #666;
            margin-top: 5px;
        }

        .history-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }

        .history-card {
            background: #16213e;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #333;
        }

        .history-card h3 {
            font-size: 0.85rem;
            color: #00d9ff;
            margin-bottom: 10px;
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .empty-state p {
            margin-top: 10px;
        }

        .refresh-indicator {
            font-size: 0.75rem;
            color: #666;
            text-align: right;
        }

        @media (max-width: 600px) {
            .history-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Llama Monitor Dashboard</h1>
        <div class="status">
            <div class="status-indicator">
                <div class="indicator-dot" id="status-dot"></div>
                <span id="status-text">Connecting...</span>
            </div>
            <a href="/settings" class="btn secondary"><i class="fa-solid fa-sliders"></i> Settings</a>
            <button class="btn secondary" id="refresh-btn">Refresh</button>
        </div>
    </div>

    <div class="cost-display">
        <h3>Today's Energy Cost</h3>
        <div class="cost-value" id="cost-value">$0.0000</div>
        <div class="cost-sub" id="cost-sub">Today's energy: 0 Wh @ $0.12/kWh</div>
    </div>

    <div class="grid">
        <div class="card">
            <h2>Server Status</h2>
            <div class="metric-row">
                <span class="metric-label">Prompt Tokens</span>
                <span class="metric-value" id="server-prompt-tokens">0</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Generated Tokens</span>
                <span class="metric-value" id="server-generated-tokens">0</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Generation Rate</span>
                <span class="metric-value metric-rate" id="server-gen-rate">0/s</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Active Slots</span>
                <span class="metric-value" id="server-active-slots">0/0</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Requests Processing</span>
                <span class="metric-value" id="server-processing">0</span>
            </div>
        </div>

        <div class="card">
            <h2>System Resources</h2>
            <div class="metric-row">
                <span class="metric-label">CPU Usage</span>
                <div style="text-align: right;">
                    <span class="metric-value" id="cpu-percent">0%</span>
                    <div class="progress-bar">
                        <div class="progress-fill" id="cpu-bar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
            <div class="metric-row">
                <span class="metric-label">GPU Usage</span>
                <div style="text-align: right;">
                    <span class="metric-value" id="gpu-percent">0%</span>
                    <div class="progress-bar">
                        <div class="progress-fill" id="gpu-bar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
            <div class="metric-row">
                <span class="metric-label">Memory</span>
                <div style="text-align: right;">
                    <span class="metric-value" id="memory-percent">0%</span>
                    <div class="progress-bar">
                        <div class="progress-fill" id="memory-bar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
            <div class="metric-row">
                <span class="metric-label">GPU Memory</span>
                <span class="metric-value" id="gpu-memory">0 MB</span>
            </div>
        </div>

        <div class="card">
            <h2>Power & Energy</h2>
            <div class="metric-row">
                <span class="metric-label">GPU Power</span>
                <span class="metric-value" id="gpu-power">0 W</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">CPU Power</span>
                <span class="metric-value" id="cpu-power">0 W</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Total System</span>
                <span class="metric-value" id="system-power">0 W</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Session Energy</span>
                <span class="metric-value" id="session-energy">0 Wh</span>
            </div>
        </div>

        <div class="card">
            <h2>Process GPU</h2>
            <div id="process-gpu-list">
                <div class="empty-state">
                    <p>No tracked processes found</p>
                </div>
            </div>
        </div>
    </div>

    <div class="history-grid">
        <div class="history-card">
            <h3>Usage (60s)</h3>
            <div class="chart-container">
                <canvas id="combined-chart"></canvas>
            </div>
        </div>
        <div class="history-card">
            <h3>Power (60s)</h3>
            <div class="chart-container">
                <canvas id="power-chart"></canvas>
            </div>
        </div>
    </div>

    <div class="refresh-indicator" id="refresh-time">Last update: Never</div>

    <script>
        // Helper function for 4 significant digits formatting
        function formatSignificantDigits(value, digits = 4) {
            if (value === null || value === undefined || isNaN(value)) {
                return '0';
            }
            if (value === 0) {
                return '0';
            }
            const absValue = Math.abs(value);
            // Calculate the number of decimal places needed
            const exponent = Math.floor(Math.log10(absValue));
            let decimalPlaces = digits - 1 - exponent;
            if (decimalPlaces < 0) {
                decimalPlaces = 0;
            }
            return absValue.toLocaleString('en-US', {
                minimumFractionDigits: 0,
                maximumFractionDigits: decimalPlaces,
                useGrouping: true
            });
        }

        // Global state
        let historyData = {
            gpu: [],
            cpu: [],
            power: [],
            timestamps: []
        };

        let chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#888' }
                }
            },
            scales: {
                x: {
                    grid: { color: '#2a2a4a' },
                    ticks: { color: '#666', maxTicksLimit: 6 }
                },
                y: {
                    min: 0,
                    max: 100,
                    grid: { color: '#2a2a4a' },
                    ticks: { color: '#666' }
                }
            }
        };

        // Charts
        let combinedChart, powerChart;

        function initCharts() {
            const ctx = document.getElementById('combined-chart').getContext('2d');
            combinedChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'GPU %',
                        data: [],
                        borderColor: '#00ff88',
                        backgroundColor: 'rgba(0, 255, 136, 0.1)',
                        tension: 0.4,
                        fill: true
                    }, {
                        label: 'CPU %',
                        data: [],
                        borderColor: '#00d4ff',
                        backgroundColor: 'rgba(0, 212, 255, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: chartOptions
            });

            const ctx2 = document.getElementById('power-chart').getContext('2d');
            powerChart = new Chart(ctx2, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'GPU Power (W)',
                            data: [],
                            borderColor: '#00d9ff',
                            tension: 0.4
                        },
                        {
                            label: 'CPU Power (W)',
                            data: [],
                            borderColor: '#00ff88',
                            tension: 0.4
                        }
                    ]
                },
                options: chartOptions
            });
        }

        function updateMetrics(data) {
            if (!data) return;

            // Convert Unix epoch seconds to hh:mm:ss format
            const now = new Date();
            const timestamp = data.timestamp ? new Date(data.timestamp * 1000) : now;
            const timeString = timestamp.toLocaleTimeString('en-US', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });

            // Update server metrics
            const server = data.server || {};
            document.getElementById('server-prompt-tokens').textContent =
                (server.prompt_tokens_total || 0).toLocaleString();
            document.getElementById('server-generated-tokens').textContent =
                (server.tokens_predicted_total || 0).toLocaleString();
            document.getElementById('server-gen-rate').textContent =
                (server.predicted_tokens_seconds || 0).toLocaleString() + '/s';

            // Update system metrics
            const system = data.system || {};
            const cpuPercent = system.cpu_percent || 0;
            const gpuPercent = system.gpu_usage || 0;
            const memoryPercent = system.memory_percent || 0;

            document.getElementById('cpu-percent').textContent = formatSignificantDigits(cpuPercent) + '%';
            document.getElementById('cpu-bar').style.width = Math.min(cpuPercent, 100) + '%';

            document.getElementById('gpu-percent').textContent = formatSignificantDigits(gpuPercent) + '%';
            document.getElementById('gpu-bar').style.width = Math.min(gpuPercent, 100) + '%';

            document.getElementById('memory-percent').textContent = formatSignificantDigits(memoryPercent) + '%';
            document.getElementById('memory-bar').style.width = Math.min(memoryPercent, 100) + '%';

            document.getElementById('gpu-memory').textContent =
                (system.gpu_memory_used || 0) + ' MB';

            // Update power metrics
            document.getElementById('gpu-power').textContent =
                formatSignificantDigits(system.gpu_power_w || 0) + ' W';
            document.getElementById('cpu-power').textContent =
                formatSignificantDigits(system.cpu_power_w || 0) + ' W';
            document.getElementById('system-power').textContent =
                formatSignificantDigits(system.system_power_w || 0) + ' W';

            // Update cost - show today's energy cost
            const cost = data.cost || {};
            const todayWh = cost.today_wh || 0;
            const costRate = cost.cost_rate || 0.12;
            const costUsd = todayWh / 1000 * costRate;

            document.getElementById('cost-value').textContent = '$' + formatSignificantDigits(costUsd);
            document.getElementById('cost-sub').textContent =
                'Today\'s energy: ' + formatSignificantDigits(todayWh) + ' Wh @ $' + formatSignificantDigits(costRate) + '/kWh';

            // Update process GPU list
            const processGpu = data.process_gpu || {};
            const processList = document.getElementById('process-gpu-list');
            const processNames = Object.keys(processGpu);

            if (processNames.length === 0) {
                processList.innerHTML = '<div class="empty-state"><p>No tracked processes</p></div>';
            } else {
                processList.innerHTML = processNames.map(name => {
                    const proc = processGpu[name];
                    return `
                        <div class="metric-row">
                            <span class="metric-label">${name} (PID: ${proc.pid || '?'})</span>
                            <div style="text-align: right;">
                                <span class="metric-value">${formatSignificantDigits(proc.gpu_utilization || 0)}%</span>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${Math.min(proc.gpu_utilization || 0, 100)}%"></div>
                                </div>
                                <span class="metric-rate" style="margin-top: 3px;">
                                    ${formatSignificantDigits(proc.gpu_memory_mb || 0)} MB
                                </span>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // Update history data with formatted time string
            updateHistory(timeString, system, server);

            // Update charts
            updateCharts();

            // Update status
            document.getElementById('status-dot').className = 'indicator-dot';
            document.getElementById('status-text').textContent = 'Connected';
            document.getElementById('refresh-time').textContent =
                'Last update: ' + new Date().toLocaleTimeString();
        }

        function updateHistory(timestamp, system, server) {
            // Add new data point
            historyData.gpu.push(system.gpu_usage || 0);
            historyData.cpu.push(system.cpu_percent || 0);
            historyData.power.push((system.gpu_power_w || 0) + (system.cpu_power_w || 0));
            historyData.timestamps.push(timestamp);

            // Keep only last 60 data points (60 seconds if 1s polling)
            const maxPoints = 60;
            if (historyData.gpu.length > maxPoints) {
                historyData.gpu.shift();
                historyData.cpu.shift();
                historyData.power.shift();
                historyData.timestamps.shift();
            }
        }

        function updateCharts() {
            // Update combined GPU/CPU chart
            combinedChart.data.labels = historyData.timestamps.slice(-60);
            combinedChart.data.datasets[0].data = historyData.gpu.slice(-60);
            combinedChart.data.datasets[1].data = historyData.cpu.slice(-60);
            combinedChart.update('none');

            // Update power chart
            powerChart.data.labels = historyData.timestamps.slice(-60);
            // Combine GPU and CPU power into a single array for display
            const totalPower = historyData.power.slice(-60);
            powerChart.data.datasets[0].data = totalPower;
            powerChart.update('none');
        }

        async function fetchMetrics() {
            try {
                const port = 8080;
                const response = await fetch('http://localhost:' + port + '/api/metrics/latest');
                if (response.ok) {
                    const data = await response.json();
                    updateMetrics(data);
                } else {
                    throw new Error('Bad response');
                }
            } catch (error) {
                // Fallback to database if aggregator unavailable
                try {
                    const dbResponse = await fetch('/api/metrics/latest-db');
                    if (dbResponse.ok) {
                        const data = await dbResponse.json();
                        updateMetrics(data);
                    }
                } catch (dbError) {
                    document.getElementById('status-dot').className = 'indicator-dot offline';
                    document.getElementById('status-text').textContent = 'Disconnected';
                }
            }
        }

        // WebSocket connection
        const socket = io();

        socket.on('connect', () => {
            console.log('WebSocket connected');
            document.getElementById('status-dot').className = 'indicator-dot';
            document.getElementById('status-text').textContent = 'Connected';
        });

        socket.on('disconnect', () => {
            console.log('WebSocket disconnected');
            document.getElementById('status-dot').className = 'indicator-dot offline';
            document.getElementById('status-text').textContent = 'Disconnected (polling)';
        });

        socket.on('metrics_update', (data) => {
            updateMetrics(data);
        });

        // Initial load
        initCharts();
        fetchMetrics();

        // Poll for updates (fallback to WebSocket)
        setInterval(fetchMetrics, 1000);

        // Refresh button
        document.getElementById('refresh-btn').addEventListener('click', fetchMetrics);
    </script>
</body>
</html>
"""
    return html


@app.route("/api/metrics/latest")
def api_latest_metrics():
    """Return latest metrics from metrics_cache, aggregator, or database."""
    # Try metrics_cache first (shared with aggregator)
    if _metrics_cache is not None:
        try:
            cached = _metrics_cache.get()
            if cached:
                return jsonify(cached)
        except Exception:
            pass

    # Try aggregator next
    if AGGREGATOR_AVAILABLE:
        aggregator = get_aggregator()
        if aggregator and aggregator.last_metrics:
            return jsonify(aggregator.last_metrics)

    # Fallback to database
    config = get_config()
    db_path = getattr(config, "database_path", "llama_monitor.db")
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


@app.route("/api/metrics/latest-db")
def api_latest_metrics_db():
    """Return latest metrics from database directly."""
    config = get_config()
    db_path = getattr(config, "database_path", "llama_monitor.db")
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
    db_path = getattr(config, "database_path", "llama_monitor.db")

    start = request.args.get("start")
    end = request.args.get("end")
    limit = request.args.get("limit", 100, type=int)

    import sqlite3

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT * FROM combined_metrics WHERE 1=1"
        params = []

        if start:
            query += " AND timestamp >= ?"
            params.append(start)
        if end:
            query += " AND timestamp <= ?"
            params.append(end)

        query += " ORDER BY timestamp DESC LIMIT ?"

        cursor.execute(query, params + [limit])
        rows = cursor.fetchall()
        conn.close()

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


@app.route("/api/metrics/list")
def api_metrics_list():
    """Return list of available metrics and tables."""
    config = get_config()
    db_path = getattr(config, "database_path", "llama_monitor.db")

    import sqlite3

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get tables
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name LIKE 'metrics_%'
            """
        )
        tables = [row[0] for row in cursor.fetchall()]

        # Get columns for each table
        metrics_info = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            metrics_info[table] = columns

        conn.close()

        return jsonify({
            "tables": tables,
            "metrics": metrics_info,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/status")
def api_status():
    """Return aggregator status."""
    if AGGREGATOR_AVAILABLE:
        aggregator = get_aggregator()
        return jsonify({
            "status": "running" if aggregator else "stopped",
            "aggregator_available": True,
        })

    return jsonify({
        "status": "standalone",
        "aggregator_available": False,
    })


def get_db():
    """Get database instance."""
    if not DB_AVAILABLE:
        return None
    config = get_config()
    db_path = getattr(config, "database_path", "llama_monitor.db")
    return Database(db_path)


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
                    <input type="number" id="cost_rate" name="cost_rate" step="0.01" min="0">
                    <div class="hint">Current electricity rate for cost calculations</div>
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

                // Display current values
                document.getElementById('current-values').innerHTML = `
                    <div><strong>Refresh Rate:</strong> <span class="value-display">${settings.web_refresh_rate || 1}s</span></div>
                    <div><strong>Cost Display:</strong> <span class="value-display">${settings.show_cost !== false ? 'Enabled' : 'Disabled'}</span></div>
                    <div><strong>Temp Display:</strong> <span class="value-display">${settings.show_temps !== false ? 'Enabled' : 'Disabled'}</span></div>
                    <div><strong>Electricity Cost:</strong> <span class="value-display">$${parseFloat(settings.cost_rate || 0.12).toFixed(2)}/kWh</span></div>
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
                cost_rate: parseFloat(document.getElementById('cost_rate').value) || 0.12
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
        "cost_rate": db.get_setting("cost_rate_usd_per_kwh", "0.12")
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
        # Delete all settings to reset to defaults
        cursor = db.conn.cursor()
        cursor.execute("DELETE FROM settings")
        db.conn.commit()

        # Re-insert default cost rate
        cursor.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?)",
            ("cost_rate_usd_per_kwh", "0.12")
        )
        db.conn.commit()

        return jsonify({"success": True, "message": "Settings reset to defaults"})
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

    socketio.run(app, host=host, port=port, debug=debug)


# Global server reference for stop_server
_server_thread = None


def start_server(host="0.0.0.0", port=8080, metrics_cache=None, verbose=False):
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
        run_server(host=host, port=port, debug=False, verbose=verbose)

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
