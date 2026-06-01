# llama-monitor

Real-time monitoring dashboard for llama.cpp servers with TUI and Web interfaces.

## Overview

llama-monitor provides a single-pane view of your llama.cpp server's performance and system resources:

- **Server metrics** - Token rates, active slots, request queues
- **System metrics** - CPU/GPU usage, memory, power consumption
- **Cost tracking** - Electricity cost calculation based on power draw
- **History** - Configurable data retention with automatic compression

## Features

- Real-time TUI dashboard in terminal
- Web-based dashboard accessible remotely
- Per-process GPU monitoring (tracks llama-server.exe specifically)
- Idle baseline tracking for accurate power calculations
- Configurable data retention with two compression levels
- SQLite storage with automatic archival

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/llama-monitor.git
cd llama-monitor

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `config.yaml` file in the same directory as `main.py`:

```yaml
server:
  url: "http://localhost:8000"
  model_id: "qwen3-coder-next"
  metrics_endpoint: "/metrics"

data:
  polling_interval: 1  # seconds (1, 2, 5, 10, 15, 20, 30)
  
  compression_level_1:
    interval: 1
    start_after: 1
    unit: week
  
  compression_level_2:
    interval: 1
    start_after: 1
    unit: month
  
  retention:
    raw_forever: false
    archive_path: "archive/"

display:
  tui_refresh_rate: 2.0
  web_refresh_rate: 1.0
  show_cost: true
  show_temps: true
  cost_rate: 0.12  # $/kWh
```

See `example_config.yaml` for complete configuration options.

## Usage

### Running the TUI Dashboard

```bash
python main.py
```

### Running the Web Dashboard

```bash
python main.py --web
```

Then open `https://localhost:2633` in your browser.

### Getting CLI Stats

```bash
python -m llama_monitor.cli_stats --server http://localhost:8000
```

## Controls (TUI)

- `Q` - Quit
- `R` - Refresh now
- `C` - Toggle cost display
- `T` - Toggle temperature display

## System Requirements

- Windows 10/11 (for WMI/NVML support)
- Python 3.10+
- NVIDIA GPU (for GPU monitoring) - CPU-only monitoring available without GPU
- llama.cpp server running with `--metrics` flag

## Architecture

```
llama-monitor/
├── server_metrics.py    # Fetch metrics from llama.cpp server
├── system_metrics.py    # Collect CPU/GPU/memory data
├── electricity_cost.py  # Calculate power costs
├── aggregator.py        # Store data to SQLite
├── tui.py               # Terminal UI
├── web_server.py        # Flask web interface
├── cli_stats.py         # On-demand CLI stats
└── main.py              # Entry point
```

## Database Schema

Data is stored in SQLite with configurable retention:

- `server_metrics_raw/1m/1h` - Server performance data
- `system_metrics_raw/1m/1h` - System resource data
- `process_gpu_metrics_raw/1m/1h` - Per-process GPU utilization
- `idle_baseline` - Idle power consumption baseline
- `cumulative_energy` - Ever-increasing energy counters

## Development

```bash
# Run tests
pytest tests/

# Lint
ruff check .
```

## License

MIT License
