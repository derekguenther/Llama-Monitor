"""Web server for llama-monitor.

This module provides a Flask-based web server that:
- Serves HTML dashboard with Chart.js for visualizations
- Provides REST API endpoints for metrics data
- Uses WebSocket (via Flask-SocketIO) for real-time client updates
- Connects to the aggregator daemon via HTTP API for data

The web server should be started separately from the aggregator daemon.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit

# Local imports
from config import load_config, find_config

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
    <title>llama-monitor Dashboard</title>
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
        <h1>llama-monitor Dashboard</h1>
        <div class="status">
            <div class="status-indicator">
                <div class="indicator-dot" id="status-dot"></div>
                <span id="status-text">Connecting...</span>
            </div>
            <button class="btn secondary" id="refresh-btn">Refresh</button>
        </div>
    </div>

    <div class="cost-display">
        <h3>Session Cost</h3>
        <div class="cost-value" id="cost-value">$0.0000</div>
        <div class="cost-sub" id="cost-sub">This session: 0 seconds @ $0.12/kWh</div>
    </div>

    <div class="grid">
        <div class="card">
            <h2>Server Status</h2>
            <div class="metric-row">
                <span class="metric-label">Prompt Tokens</span>
                <span class="metric-value" id="server-prompt-tokens">0</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Token Rate</span>
                <span class="metric-value metric-rate" id="server-prompt-rate">0/s</span>
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
            <h3>GPU Usage (60s)</h3>
            <div class="chart-container">
                <canvas id="gpu-chart"></canvas>
            </div>
        </div>
        <div class="history-card">
            <h3>CPU Usage (60s)</h3>
            <div class="chart-container">
                <canvas id="cpu-chart"></canvas>
            </div>
        </div>
        <div class="history-card">
            <h3>Token Rate (60s)</h3>
            <div class="chart-container">
                <canvas id="tokens-chart"></canvas>
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
        // Global state
        let historyData = {
            gpu: [],
            cpu: [],
            tokens: [],
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
                    grid: { color: '#2a2a4a' },
                    ticks: { color: '#666' },
                    suggestedMin: 0
                }
            }
        };

        // Charts
        let gpuChart, cpuChart, tokensChart, powerChart;

        function initCharts() {
            const ctx1 = document.getElementById('gpu-chart').getContext('2d');
            gpuChart = new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'GPU %',
                        data: [],
                        borderColor: '#00d9ff',
                        backgroundColor: 'rgba(0, 217, 255, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: chartOptions
            });

            const ctx2 = document.getElementById('cpu-chart').getContext('2d');
            cpuChart = new Chart(ctx2, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'CPU %',
                        data: [],
                        borderColor: '#00ff88',
                        backgroundColor: 'rgba(0, 255, 136, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: chartOptions
            });

            const ctx3 = document.getElementById('tokens-chart').getContext('2d');
            tokensChart = new Chart(ctx3, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Tokens/s',
                        data: [],
                        borderColor: '#ff00ff',
                        backgroundColor: 'rgba(255, 0, 255, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: chartOptions
            });

            const ctx4 = document.getElementById('power-chart').getContext('2d');
            powerChart = new Chart(ctx4, {
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

            const now = new Date().toISOString();
            const timestamp = data.timestamp || now;

            // Update server metrics
            const server = data.server || {};
            document.getElementById('server-prompt-tokens').textContent =
                (server.prompt_tokens_total || 0).toLocaleString();
            document.getElementById('server-prompt-rate').textContent =
                (server.prompt_tokens_seconds || 0).toLocaleString() + '/s';
            document.getElementById('server-generated-tokens').textContent =
                (server.tokens_predicted_total || 0).toLocaleString();
            document.getElementById('server-gen-rate').textContent =
                (server.predicted_tokens_seconds || 0).toLocaleString() + '/s';

            // Update system metrics
            const system = data.system || {};
            const cpuPercent = system.cpu_percent || 0;
            const gpuPercent = system.gpu_usage || 0;
            const memoryPercent = system.memory_percent || 0;

            document.getElementById('cpu-percent').textContent = cpuPercent.toFixed(1) + '%';
            document.getElementById('cpu-bar').style.width = Math.min(cpuPercent, 100) + '%';

            document.getElementById('gpu-percent').textContent = gpuPercent.toFixed(1) + '%';
            document.getElementById('gpu-bar').style.width = Math.min(gpuPercent, 100) + '%';

            document.getElementById('memory-percent').textContent = memoryPercent.toFixed(1) + '%';
            document.getElementById('memory-bar').style.width = Math.min(memoryPercent, 100) + '%';

            document.getElementById('gpu-memory').textContent =
                (system.gpu_memory_used || 0) + ' MB';

            // Update power metrics
            document.getElementById('gpu-power').textContent =
                (system.gpu_power_w || 0).toFixed(1) + ' W';
            document.getElementById('cpu-power').textContent =
                (system.cpu_power_w || 0).toFixed(1) + ' W';
            document.getElementById('system-power').textContent =
                (system.system_power_w || 0).toFixed(1) + ' W';

            // Update cost
            const cost = data.cost || {};
            const totalWh = cost.total_wh || 0;
            const costRate = {{ cost_rate|default(0.12) }};
            const costUsd = totalWh / 1000 * costRate;

            document.getElementById('cost-value').textContent = '$' + costUsd.toFixed(4);
            document.getElementById('cost-sub').textContent =
                'Session energy: ' + totalWh.toFixed(1) + ' Wh @ $' + costRate.toFixed(2) + '/kWh';

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
                                <span class="metric-value">${proc.gpu_utilization || 0}%</span>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${Math.min(proc.gpu_utilization || 0, 100)}%"></div>
                                </div>
                                <span class="metric-rate" style="margin-top: 3px;">
                                    ${proc.gpu_memory_mb || 0} MB
                                </span>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // Update history data
            updateHistory(timestamp, system, server);

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
            historyData.tokens.push(server.prompt_tokens_seconds || 0);
            historyData.power.push((system.gpu_power_w || 0) + (system.cpu_power_w || 0));
            historyData.timestamps.push(timestamp);

            // Keep only last 60 data points (60 seconds if 1s polling)
            const maxPoints = 60;
            if (historyData.gpu.length > maxPoints) {
                historyData.gpu.shift();
                historyData.cpu.shift();
                historyData.tokens.shift();
                historyData.power.shift();
                historyData.timestamps.shift();
            }
        }

        function updateCharts() {
            // Update GPU chart
            gpuChart.data.labels = historyData.timestamps.slice(-60);
            gpuChart.data.datasets[0].data = historyData.gpu.slice(-60);
            gpuChart.update('none');

            // Update CPU chart
            cpuChart.data.labels = historyData.timestamps.slice(-60);
            cpuChart.data.datasets[0].data = historyData.cpu.slice(-60);
            cpuChart.update('none');

            // Update tokens chart
            tokensChart.data.labels = historyData.timestamps.slice(-60);
            tokensChart.data.datasets[0].data = historyData.tokens.slice(-60);
            tokensChart.update('none');

            // Update power chart
            powerChart.data.labels = historyData.timestamps.slice(-60);
            powerChart.data.datasets[0].data = historyData.power.slice(-60);
            powerChart.update('none');
        }

        async function fetchMetrics() {
            try {
                const port = {{ port|default(8080) }};
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
    """Return latest metrics from aggregator or database."""
    # Try aggregator first
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

    return jsonify({"error": "No metrics available"}), 404


@app.route("/api/metrics/latest-db")
def api_latest_metrics_db():
    """Return latest metrics from database directly."""
    config = get_config()
    db_path = getattr(config, "database_path", "llama_monitor.db")
    metrics = fetch_metrics_from_database(db_path)

    if metrics:
        return jsonify(metrics)

    return jsonify({"error": "No metrics available"}), 404


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


@socketio.on("connect")
def handle_connect():
    """Handle WebSocket connection."""
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print("Client disconnected")


def run_server(host="0.0.0.0", port=8080, debug=False):
    """Run the web server.

    Args:
        host: Host to bind to
        port: Port to listen on
        debug: Enable debug mode
    """
    print(f"llama-monitor web server starting on http://{host}:{port}")
    print("Press Ctrl+C to stop")

    socketio.run(app, host=host, port=port, debug=debug)


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

    args = parser.parse_args()

    run_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
