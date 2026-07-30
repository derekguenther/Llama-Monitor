# llama-monitor Design Document

## Overview

A real-time monitoring dashboard for llama.cpp servers that combines:
- Server metrics (via `/metrics` and `/slots` endpoints)
- System metrics (CPU, GPU, memory via Windows Performance Counters)
- Optional electricity cost calculation
- Flexible output: TUI (terminal) + Web dashboard

## Goals

1. **Single-pane view** of all relevant monitoring data
2. **Low overhead** - minimal resource usage
3. **Flexible output** - TUI for terminal, web for remote access
4. **History tracking** - SQLite storage with configurable retention/compression
5. **Extensibility** - Easy to add new metrics without schema changes

## Non-Goals

1. Multi-server management (single server focus)
2. Alerting system (no notifications)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     llama-monitor/                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐ │
│  │  Server        │  │  System        │  │  Calculator    │ │
│  │  Metrics       │  │  Metrics       │  │  (optional)    │ │
│  │  - /metrics    │  │  - CPU         │  │  - Cost calc   │ │
│  │  - /slots      │  │  - GPU         │  │                │ │
│  │  - /props      │  │  - Memory      │  │                │ │
│  └────────────────┘  └────────────────┘  └──────────────────┘ │
│                         │                                       │
│                         ▼                                       │
│              ┌────────────────────────┐                         │
│              │   Data Aggregator      │                         │
│              │   - Dedupe/merge       │                         │
│              │   - Timestamp          │                         │
│              │   - Store to SQLite    │                         │
│              └────────────────────────┘                         │
│                         │                                       │
│         ┌───────────────┼───────────────┐                       │
│         ▼               ▼               ▼                       │
│  ┌────────────┐ ┌────────────┐ ┌──────────────┐               │
│  │   TUI      │ │   Web      │ │   CLI Stats  │               │
│  │ (curses)   │ │ (Flask)    │ │ (on-demand)  │               │
│  └────────────┘ └────────────┘ └──────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Power Calculation Strategy

**Goal**: Track power consumption of llama-server.exe specifically, not all system usage.

### CPU Power Calculation
```
cpu_power_llama = cpu_power_total * (cpu_percent_llama / cpu_percent_total)
```
- Get total CPU power from WMI/PSUtil
- Get llama-server.exe CPU % via WMI per-process counters
- Calculate proportional power allocation

### GPU Power Calculation (Primary: NVML)
```
gpu_power_llama = gpu_power_total * (gpu_util_llama / gpu_util_total)
```
- Use NVML's `nvmlDeviceGetGraphicsRunningProcesses_v2()` for per-process GPU utilization
- Match `llama-server.exe` by process name
- Calculate proportional power allocation

### GPU Power Calculation (Fallback: WMI)
- Use `\GPU Process Memory(*)\Local Usage` counter
- Correlate with process names (less reliable)
- Logs warning but continues operation

### Idle Baseline Tracking
- Monitor combined CPU + GPU utilization
- When both < 5% simultaneously, record system power as idle baseline
- Store in `idle_baseline` table
- Used to calculate actual inference power: `power_inference = power_total - power_idle`

---

## Components

### 1. `server_metrics.py` - Server Data Collector

**Purpose**: Fetch metrics from llama.cpp server endpoints

**Endpoints**:
- `GET /metrics?model={model_id}` - Prometheus-format metrics
- `GET /slots` - Slot states with progress
- `GET /props` - Server configuration

**Output**:
```python
{
    "timestamp": "2026-05-30T...",
    "server": {
        "prompt_tokens_total": 1234567,
        "prompt_tokens_seconds": 10005.67,
        "tokens_predicted_total": 987654,
        "predicted_tokens_seconds": 11270.12,
        "requests_processing": 3,
        "requests_deferred": 2,
    },
    "slots": [
        {
            "id": 0,
            "task": 29,
            "n_tokens": 45056,
            "progress": 0.459422,
            "state": "processing"
        }
    ]
}
```

### 2. `system_metrics.py` - System Data Collector

**Purpose**: Collect Windows performance counters

**Libraries**:
- `psutil` - CPU, memory, disk, network (uses WMI under the hood)
- `nvidia-ml-py` (pynvml) - GPU metrics (usage, memory, temp, power) - **primary**
- `wmi` - Fallback GPU metrics if NVML unavailable - **logs warning, not error**

**GPU Power Detection Priority**:
1. **NVML** (`nvmlDeviceGetPowerUsage`) - Direct hardware access, most accurate
2. **WMI** (`Win32_PerfFormattedData`) - Fallback if NVML fails

**Per-Process GPU Monitoring** (for power calculation):
- Uses NVML's `nvmlDeviceGetGraphicsRunningProcesses_v2()` to get per-process GPU utilization
- Matches processes by name (e.g., `llama-server.exe`) to track specific workloads
- Calculates process power: `gpu_power_process = gpu_power_total * (gpu_util_process / gpu_util_total)`
- Falls back to WMI if NVML unavailable (less reliable, logs warning)

**Per-Process GPU Monitoring**:
- Uses NVML's `nvmlDeviceGetGraphicsRunningProcesses_v2()` to get process-specific GPU utilization
- Matches processes by name (e.g., `llama-server.exe`) to track specific workloads
- Calculates process power: `gpu_power_process = gpu_power_total * (gpu_util_process / gpu_util_total)`

**Polling Interval**: Configurable (default: 1 second)

**Output**:
```python
{
    "timestamp": "2026-05-31T...",
    "cpu": {
        "percent": 45.2,
        "cores": [12.3, 8.1, 22.4, ...],
        "temperature_c": [45, 50, 55, 48],  # Per-core temps
        "power_w": 65.0
    },
    "gpu": {
        "usage": 87.5,
        "memory_used": 12288,  # MB
        "memory_total": 24576,
        "temperature_c": 72,
        "fan_speed_rpm": 2500,
        "power_w": 250.0  # From NVML or WMI
    },
    "process_gpu": {  # Per-process GPU utilization (if tracked)
        "llama-server.exe": {
            "pid": 12345,
            "gpu_utilization": 85.0,  # Percentage (0-100)
            "gpu_memory_mb": 12288
        }
    },
    "memory": {
        "used": 32768,  # MB
        "total": 65536,
        "percent": 50.0
    },
    "system": {
        "power_w": 380.0  # Total system power (if available)
    }
}
```

**Extensible Metrics**: New metrics can be added via `ALTER TABLE` - nullable columns add minimal storage overhead

### 3. `electricity_cost.py` - Cost Calculator

**Purpose**: Calculate electricity cost of inference

**Inputs**:
- GPU power draw (W) - configurable or auto-detected
- CPU power draw (W) - estimated from usage
- Duration (seconds)
- Electricity rate ($/kWh) - configurable

**Per-Process Power Calculation**:
- CPU: `cpu_power_process = cpu_power_total * (cpu_percent_process / cpu_percent_total)`
- GPU: `gpu_power_process = gpu_power_total * (gpu_utilization_process / gpu_utilization_total)`
- System idle baseline tracked when CPU+GPU < 5% combined

**Output**:
```python
{
    "gpu_power_w": 250.0,
    "cpu_power_w": 65.0,
    "duration_seconds": 3600,
    "energy_kwh": 0.315,
    "cost_usd": 0.038  # at $0.12/kWh
}
```

**Per-Process Cost Tracking**:
```python
{
    "process_name": "llama-server.exe",
    "pid": 12345,
    "gpu_power_w": 212.5,  # 250W * (85% / 100%)
    "cpu_power_w": 55.0,
    "duration_seconds": 3600,
    "energy_kwh": 0.2625,
    "cost_usd": 0.0315
}
```

### 4. `aggregator.py` - Data Aggregator

**Purpose**: Merge server + system metrics, store to SQLite with configurable retention/compression

**Configuration Structure**:
```yaml
data:
  polling_interval: 1  # seconds (1, 2, 5, 10, 15, 20, 30)
  
  compression_level_1:
    interval: 1  # minute, hour, day (aggregation interval)
    start_after: 1  # 1, 2, 5, 10, 15, 20, 30
    unit: week  # second, minute, hour, day, week, month
  
  compression_level_2:
    interval: 1  # hour (aggregation interval)
    start_after: 1  # 1, 2, 5, 10, 15, 20, 30
    unit: month  # second, minute, hour, day, week, month
  
  retention:
    raw_forever: false  # If true, never compress
    archive_path: "archive/"  # Optional archive directory
```

**Example Configuration**:
```yaml
data:
  polling_interval: 1  # Collect every 1 second
  
  compression_level_1:
    interval: 1  # Compress to 1-minute buckets
    start_after: 1  # After 1 week
    unit: week
  
  compression_level_2:
    interval: 1  # Then compress to 1-hour buckets
    start_after: 1  # After 1 month
    unit: month
```

**SQLite Schema**:
```sql
-- Server metrics tables
CREATE TABLE server_metrics_raw (
    timestamp TEXT PRIMARY KEY,
    prompt_tokens_total INTEGER,
    prompt_tokens_seconds REAL,
    tokens_predicted_total INTEGER,
    predicted_tokens_seconds REAL,
    requests_processing INTEGER,
    requests_deferred INTEGER
);

CREATE TABLE server_metrics_1m (
    timestamp TEXT PRIMARY KEY,
    prompt_tokens_total INTEGER,
    prompt_tokens_seconds REAL,
    tokens_predicted_total INTEGER,
    predicted_tokens_seconds REAL,
    requests_processing INTEGER,
    requests_deferred INTEGER
);

CREATE TABLE server_metrics_1h (
    timestamp TEXT PRIMARY KEY,
    prompt_tokens_total INTEGER,
    prompt_tokens_seconds REAL,
    tokens_predicted_total INTEGER,
    predicted_tokens_seconds REAL,
    requests_processing INTEGER,
    requests_deferred INTEGER
);

-- System metrics tables
CREATE TABLE system_metrics_raw (
    timestamp TEXT PRIMARY KEY,
    cpu_percent REAL,
    cpu_cores_percent TEXT,  -- JSON array of per-core usage
    cpu_temperature_c TEXT,  -- JSON array of per-core temps
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
);

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
);

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
);

-- Per-process GPU metrics (tracked separately)
CREATE TABLE process_gpu_metrics_raw (
    timestamp TEXT,
    process_name TEXT,
    pid INTEGER,
    gpu_utilization REAL,
    gpu_memory_mb INTEGER,
    PRIMARY KEY (timestamp, process_name, pid)
);

CREATE TABLE process_gpu_metrics_1m (
    timestamp TEXT,
    process_name TEXT,
    avg_gpu_utilization REAL,
    avg_gpu_memory_mb REAL,
    PRIMARY KEY (timestamp, process_name)
);

CREATE TABLE process_gpu_metrics_1h (
    timestamp TEXT,
    process_name TEXT,
    avg_gpu_utilization REAL,
    avg_gpu_memory_mb REAL,
    PRIMARY KEY (timestamp, process_name)
);

-- Idle baseline power consumption (stored only when system is idle)
-- This is occasional data - only written when CPU+GPU < 5%
CREATE TABLE idle_baseline (
    timestamp TEXT PRIMARY KEY,
    cpu_percent REAL,
    gpu_percent REAL,
    system_power_w REAL,
    is_valid BOOLEAN DEFAULT 1
);

-- Cumulative energy counters (ever-increasing values)
-- Separate table because these are counters, not sampled metrics
CREATE TABLE cumulative_energy (
    id INTEGER PRIMARY KEY DEFAULT 1,  -- Single row tracker
    session_start TEXT NOT NULL,
    last_update TEXT,
    total_wh REAL DEFAULT 0,
    gpu_wh REAL DEFAULT 0,
    cpu_wh REAL DEFAULT 0,
    session_cost_usd REAL DEFAULT 0
);

-- Combined metrics with cost
CREATE TABLE combined_metrics (
    timestamp TEXT PRIMARY KEY,
    server_data JSON,
    system_data JSON,
    cost_data JSON
);
```

**Compression Logic**:
- **Level 1**: Raw → 1-minute (e.g., 60 samples → 1 value)
- **Level 2**: 1-minute → 1-hour (e.g., 60 values → 1 value)
- Numeric fields: `AVG()` for rates, `SUM()` for counters
- Timestamp: `MIN(timestamp)` or rounded boundary
- JSON fields (cores_percent, temps): averaged or stored as-is if single value

**Process Detection**:
- Uses NVML to get running graphics processes
- Matches `llama-server.exe` by name
- Tracks PID changes (restart detection)
- Stores per-process GPU utilization in `process_gpu_metrics_*` tables

**Idle Baseline Tracking**:
- Monitors total CPU + GPU utilization
- When both < 5% simultaneously, records system power as idle baseline
- Stored in `idle_baseline` table with `is_valid` flag
- Used to calculate actual inference power: `power_inference = power_total - power_idle`

### 5. `tui.py` - Terminal UI

**Purpose**: Full-screen terminal dashboard

**Layout**:
```
┌───────────────────────────────────────────────────────────────┐
│  llama-monitor v1.0  |  http://localhost:8000                │
├───────────────────────────────────────────────────────────────┤
│  Server Status                                                │
│  ─────────────                                                │
│  Prompt tokens:    1,234,567 (10,005/s)                      │
│  Generated:        987,654 (11,270/s)                        │
│  Active slots:     1/1 (progress: 45.9%)                     │
│  Processing:       3 | Deferred: 2                           │
├───────────────────────────────────────────────────────────────┤
│  System Resources                                             │
│  ──────────────                                               │
│  CPU: 45.2%    ┌███████████████████░░░░░░░░░░░░░░░░░░░░░░]   │
│  GPU: 87.5%    ┌███████████████████████████████░░░░░░░░░░]   │
│  Mem: 50.0%    ┌████████████████████░░░░░░░░░░░░░░░░░░░░░]   │
│  GPU Mem: 50%  ┌████████████████████░░░░░░░░░░░░░░░░░░░░░]   │
├───────────────────────────────────────────────────────────────┤
│  Power & Cost                                                 │
│  ─────────────                                                │
│  GPU Power:      250 W                                        │
│  CPU Power:       65 W                                        │
│  Total System:   380 W                                        │
│  This session:   $0.038 (12 min @ $0.12/kWh)                 │
│  Today:          $0.42                                                        │
├───────────────────────────────────────────────────────────────┤
│  History (60 seconds)                                         │
│  ─────────────────                                            │
│  GPU %: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇   │
│  CPU %: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇   │
│  GPU Mem:% ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇   │
│  Tokens/s ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇    │
└───────────────────────────────────────────────────────────────┘
```

**Controls**:
- `Q` - Quit
- `R` - Refresh now
- `C` - Toggle cost display
- `T` - Toggle temperature display

**History Graph Implementation**:
- 60-second window on single line (60 characters wide)
- Uses Unicode block characters (█ ▇ ▆ ▅ ▄ ▃ ▂ ▁)
- Shows: GPU%, CPU%, GPU Memory%, Tokens/sec
- If screen too narrow, falls back to 30-second split view

**Handling Data Gaps**:
- Graphs must handle missing data gracefully (e.g., server restart, collection failure)
- Use `NULL` values in SQLite for missing data points
- In TUI: skip missing data points, draw continuous line where data exists
- In Web (Chart.js): use `spanGaps: true` option for continuous lines

### 6. `web_server.py` - Web Dashboard

**Purpose**: HTTP server for web-based dashboard (same data as TUI, different presentation)

**Framework**: Flask (lightweight)

**Endpoints**:
- `GET /` - HTML dashboard with Chart.js for smooth graphs
- `GET /api/metrics` - JSON metrics (for live updates via WebSocket/polling)
- `GET /api/history?start=...&end=...` - Historical data range
- `GET /api/metrics/list` - List of available metrics for graphing

**Frontend**: Vanilla JS + CSS with Chart.js for smooth graphs (vs ASCII in TUI)

**Shared Data Layer**: Both TUI and Web use the same `aggregator.py` module

### 7. `cli_stats.py` - On-Demand Stats

**Purpose**: Command-line stats (like `kubectl top`)

**Usage**:
```bash
python -m llama_monitor.cli_stats --server http://localhost:8000
```

**Output**:
```
llama-monitor stats (2026-05-30 14:30:00)
==========================================
Server:
  Prompt tokens:    1,234,567 (10,005/s)
  Generated:        987,654 (11,270/s)
  Active slots:     1/1 (45.9%)

System:
  CPU: 45.2%
  GPU: 87.5%
  Mem: 50.0%

Cost (this session): $0.038
```

---

## File Structure

```
llama-monitor/
├── README.md
├── requirements.txt
├── DESIGN.md              # This file
├── main.py                # Entry point, CLI args
├── config.py              # Configuration (server URL, rates, etc.)
│
├── server_metrics.py      # Server data collection
├── system_metrics.py      # System data collection
├── electricity_cost.py    # Cost calculator
├── aggregator.py          # Data aggregation + SQLite
│
├── tui.py                 # Terminal UI
├── web_server.py          # Flask web server
├── cli_stats.py           # CLI stats command
│
└── tests/
    ├── test_server_metrics.py
    ├── test_system_metrics.py
    └── test_aggregator.py
```

---

## Configuration

**Config file**: `config.yaml` (YAML for readability)

```yaml
server:
  url: "http://localhost:8000"
  model_id: "qwen3-coder-next"
  metrics_endpoint: "/metrics"

data:
  polling_interval: 1  # seconds (1, 2, 5, 10, 15, 20, 30)
  
  compression_level_1:
    interval: 1  # minute, hour, day (aggregation interval)
    start_after: 1  # 1, 2, 5, 10, 15, 20, 30
    unit: week  # second, minute, hour, day, week, month
  
  compression_level_2:
    interval: 1  # hour (aggregation interval)
    start_after: 1  # 1, 2, 5, 10, 15, 20, 30
    unit: month  # second, minute, hour, day, week, month
  
  retention:
    raw_forever: false
    archive_path: "archive/"

display:
  tui_refresh_rate: 2.0  # seconds
  web_refresh_rate: 1.0  # seconds
  show_cost: true
  show_temps: true
  cost_rate: 0.12  # $/kWh
```

---

## Development Phases

### Phase 1: Core Metrics Collection
- [ ] `server_metrics.py` - Fetch /metrics and /slots
- [ ] `system_metrics.py` - CPU/GPU/Memory collection (with per-process tracking)
- [ ] `aggregator.py` - Store to SQLite (with per-process and idle baseline tables)
- [ ] `config.py` - Configuration management

### Phase 2: Display Options
- [ ] `cli_stats.py` - Basic CLI output
- [ ] `tui.py` - Terminal dashboard
- [ ] `web_server.py` - Flask web interface

### Phase 3: Advanced Features
- [ ] `electricity_cost.py` - Cost calculation (with per-process and idle baseline)
- [ ] History graph in TUI (60-second ASCII chart)
- [ ] Cost tracking over time
- [ ] Data compression with configurable levels
- [ ] Automatic retention management
- [ ] Per-process GPU monitoring (NVML-based)
- [ ] Idle baseline tracking algorithm

### Phase 4: Polish & Testing
- [ ] Unit tests
- [ ] Error handling
- [ ] Documentation
- [ ] Example config

---

## Dependencies

**Core**:
- `requests` - HTTP client for server API
- `psutil` - System metrics (CPU, memory)
- `nvidia-ml-py` - GPU metrics (pynvml) - primary
- `wmi` - Fallback WMI metrics if NVML unavailable

**TUI**:
- `urwid` or `rich` - Terminal UI library

**Web**:
- `flask` - Web server
- `chart.js` - JavaScript charting library (via CDN)

**Config**:
- `pyyaml` - YAML config parsing

**Dev**:
- `pytest` - Testing

**Optional**:
- `nvml-wrapper` - Alternative NVML interface (if needed)

---

## Success Criteria

1. **TUI shows real-time server + system metrics** without lag
2. **SQLite stores configurable retention** (raw + compressed levels)
3. **Web dashboard** accessible from another machine
4. **Cost calculation** accurate to within 10% of actual power meter
5. **Graceful error handling** - continues if server unavailable
6. **Data compression** respects user-configured levels
7. **Extensible metrics** - new metrics can be added via ALTER TABLE

---

## Future Enhancements

1. Multi-server support
2. Alerting (email/Slack on high usage)
3. Export to Prometheus (reverse direction)
4. Historical charts (daily/weekly trends)
5. Additional WMI metrics (per-CPU temps, disk I/O, network throughput)
6. GPU fan speed monitoring (already in Phase 2)
