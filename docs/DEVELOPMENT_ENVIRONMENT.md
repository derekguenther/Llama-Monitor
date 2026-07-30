# Development Environment

## Overview

This project is developed in a **multi-host** setup. The development environment
(OpenCode / AI agent) runs inside a Docker container in WSL2, while the
target runtime (llama.cpp, Llama Monitor) runs on the Windows host.

## Host Machine (Windows)

- **OS**: Windows with WSL2
- **RAM**: 96 GB system RAM
- **VRAM**: 16 GB
- **llama.cpp**: Runs natively on Windows, serving models via its HTTP server
- **Llama Monitor (target)**: Designed to run on Windows for full access to:
  - WMI (Windows Management Instrumentation) for CPU/memory metrics
  - NVML (NVIDIA Management Library) for GPU metrics and per-process tracking
  - Per-process power monitoring via `llama-server.exe`

## Development Container (WSL2 Docker)

- The AI agent (OpenCode or similar) runs inside a Docker container in WSL2
- The project source code is mounted at `/sandbox` inside the container
- A mapped port allows the container to reach llama.cpp on the Windows host

### Connectivity

- llama.cpp server is reachable at `http://host.docker.internal:8000`
  (Docker's built-in DNS name for the host machine)
- The agent cannot access WMI/NVML data — those metrics will show as empty
  when testing from within the container
- Web searches are permitted and encouraged for:
  - llama.cpp API documentation (endpoints, response formats)
  - Chart.js documentation
  - General programming references

## Project Structure

```
/sandbox/
├── DESIGN.md                   # Architecture and design document
├── DEVELOPMENT_ENVIRONMENT.md  # This file
├── CLAUDE.md                   # Agent instructions and workflow protocol
├── AGENTS.md                   # Agent-specific guidance
├── REPO_MAP.md                 # Symbol map of the codebase
├── README.md                   # Project README
├── config.yaml                 # Runtime configuration
├── main.py                     # Entry point
├── web_server.py               # Flask web dashboard (primary UI)
├── aggregator.py               # Data aggregation and SQLite storage
├── aggregator_daemon.py        # Aggregator as a background daemon
├── server_metrics.py           # llama.cpp server data collector
├── system_metrics.py           # Windows system data collector (WMI/NVML)
├── electricity_cost.py         # Cost calculation engine
├── config.py                   # Configuration loader
├── db.py                       # Database abstraction layer
├── cli_stats.py                # CLI stats command
├── templates/
│   └── index.html              # Dashboard HTML + JS (Chart.js)
├── memory/                     # AI agent persistent memory
├── .worktrees/                 # Git worktrees (one per task/bead)
└── tests/                      # Test suite
```

## Workflow

Per `CLAUDE.md`, work is done via the **Concurrent Worktree Protocol**:

1. Claim a bead from the issue tracker (`bd update <id> --claim`)
2. Create a git worktree: `git worktree add .worktrees/<task-name> -b <task-name>`
3. Code only inside the worktree
4. When finished: `finish-bead "description"`, then the worktree is merged
   by a reviewer

## Issue Tracking

This project uses **bd (beads)** for issue tracking. Key commands:

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
bd blocked            # Check blocked issues
bd stats              # Project statistics
```

## Database

The project uses a **Dolt-backed SQLite database** for issue tracking
(`.beads/` directory) and a separate **SQLite database** (`llama-monitor.db`)
for metrics storage.

**Schema Migration Note**: If you see a warning about pending schema migrations,
the beads database is out of sync with the remote. Do NOT run a migration
unless you are the single designated migrator (see the bd warning for details).

## Testing

```bash
# Run tests (from worktree)
python -m pytest tests/ -v
```
