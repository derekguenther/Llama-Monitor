# llama-raw-capture-tool

A data capture and correlation utility for Llama Monitor. It captures a live
run of `llama-server.exe` **raw** and **immutably** across every source of truth
that feeds Llama Monitor — the llama.cpp console log, `/slots`, `/metrics`,
`/props`, Windows performance counters, NVML/psutil — plus Llama Monitor's own
derived `/api/metrics` output. It then **post-processes** the raw capture into a
timestamp-aligned, cross-source correlated JSONL stream and a divergence report.

**Core design principle:** capture is dumb, cheap, lossless, and append-only.
Analysis is rich and repeatable — the post-processor can be re-run arbitrarily
against an existing raw capture without re-running a live session.

This tool lives **fully separate** from the main Llama Monitor project under
`DebugTools/`. It is excluded from `REPO_MAP.md` generation.

## Requirements

- Windows host (the tool targets `llama-server.exe` on Windows; `typeperf`,
  NVML, WMIC, and `taskkill` are Windows-specific).
- Python 3.9+
- `pip install -r requirements.txt` (`requests`, `psutil`, `pynvml`, `PyYAML`)

## Layout

```
DebugTools/llama-raw-capture-tool/
├── capture.py            # orchestrator
├── postprocess.py        # post-processor (+ replay helper)
├── common.py             # shared wall-clock stamp helpers
├── config.yaml           # user config (launch_script default _DeepSeek v4.bat)
├── README.md
├── requirements.txt
└── sessions/             # timestamped session dirs (gitignored)
```

## Capturing

```bash
python capture.py --config config.yaml          # run until Ctrl+C
python capture.py --config config.yaml --duration 120   # run 120 s
```

### What gets captured

| Source | Raw format | File |
|--------|-----------|------|
| llama.cpp console/log | plain text (`--log-file`) | `llama-server.log` |
| `/slots` | raw JSON array + wall-clock stamp | `slots.jsonl` |
| `/metrics` | raw Prometheus text body | `metrics.jsonl` |
| `/props` | JSON (once) | `props.json` |
| Windows perf counters | CSV (`typeperf`) | `windows.csv` |
| NVML + psutil | JSONL | `nvml-psutil.jsonl` |
| Monitor `/api/metrics/latest` | JSON + wall-clock stamp | `monitor-api.jsonl` |
| Prompt files | `--log-prompts-dir` | `prompts/<ms>.txt` |

Every capture-time write is **append-only** (`O_APPEND`) and flushed per write,
so a crash leaves a recoverable file.

### `.bat` wrapping and flag injection

The tool wraps the configured `.bat` (default `_DeepSeek v4.bat`) by writing an
injected copy (`launcher.bat`) into the session dir and running it with the
capture flags passed as arguments. The injection adds the `EXTRA_ARGS` mechanism
documented in the spec:

```bat
set EXTRA_ARGS=
if not "%1"=="" set EXTRA_ARGS=%*
... existing llama-server command ... %EXTRA_ARGS%
```

- Direct runs of the original `.bat` (no args) are unchanged.
- Tool runs pass fully-quoted capture flags; llama-server uses the *later*
  duplicate flag (with a warning), so appended flags win.

Injection differs per `.bat` structure (multi-line `^`-continued vs.
single-line); the tool detects the style and injects accordingly. A known
gotcha is `%*` quoting when a flag value contains spaces — the tool passes
fully-quoted values to mitigate this.

### Session lifecycle

1. Preflight port check (a pre-existing server aborts) + session-lock guard.
2. Timestamped session dir `sessions/<YYYYMMDD-HHMMSS>/`.
3. Config provenance copy + `launcher.bat` written.
4. Spawn the wrapper with injected flags; record the spawned PID and resolve
   `llama-server.exe` PID (via WMIC) for per-process NVML/psutil matching.
5. Attach the log tailer **immediately** (in parallel with readiness checks) and
   compute the anchor from the first log line.
6. Wait for readiness; start `/slots`, `/metrics`, `/props`, monitor,
   NVML/psutil, and `typeperf` polls.
7. Consistency check (server responding matches the session, best-effort).
8. Run until Ctrl+C / duration / signal.
9. Teardown the **entire process tree** (`taskkill /T /F /PID`), handle a
   `pause`-blocked cmd, stop `typeperf`, release the lock.
10. Write `manifest.json` (anchor, host, files, versions).

## Post-processing

```bash
python postprocess.py sessions/<YYYYMMDD-HHMMSS>/
```

Writes into `sessions/<...>/postprocessed/`:

- `events.jsonl` — unified, timestamp-aligned event stream.
- `comparison-report.md` — divergence report correlating events across sources.
- `replay-monitor.jsonl` — replay-through-monitor diff (optional).

### Timestamp anchoring

The primary anchor is the capture-side **first-log-line calibration**:
`log_epoch_us = wallclock_us(first_line) - R(first_line)`, where `R` is the log's
relative `M.s.ms.µs` time since process start (≈0 for the first line). The
tailer attaches the instant `--log-file` appears so attach latency is minimal.

Self-checks (reported as `anchor_uncertain` when they fail):

- Log file NTFS creation time vs. `wallclock(first_line) - R(first_line)`.
- `--log-prompts-dir` filename clock vs. the log-prefix clock.
- `/slots`/`/metrics`-implied activity windows vs. the log's activity spans.

### Divergence report rules

Findings are defined per source pair with a matching rule + tolerance, e.g.:

- console `slot_gen_rate` `tg` vs. `/metrics` bucket-average tokens/s (50%
  tolerance to absorb bucket-window + sampling skew).
- console activity spans vs. `/slots` processing + NVML/psutil busy windows.
- monitor latency: `/api/metrics/latest` lags raw sources by the aggregator's
  write interval and may return `{"error": "No metrics available"}` — skipped
  rather than flagged as divergence.

### Replay-through-monitor

The post-processor optionally imports Llama Monitor's own parsing functions
(`server_metrics.ServerMetrics._parse_metrics`,
`web_server._transform_metrics`) to reproduce its would-be display values and
diff against the captured `/api/metrics/latest`. This pulls main-project code
into the tool (trading against the "fully separate" goal) and is called out in
the output. The monitor version should be pinned in the report.

## Notes & limitations

- The tool is Windows-targeted; on non-Windows hosts, capture degrades to a
  dev/test stand-in (no real `llama-server.exe`).
- `typeperf` counter discovery happens at runtime (`typeperf -qx <object>`)
  because exact counter paths vary by hardware; some counters may be absent.
- NVML absence (AMD/no NVIDIA driver) falls back to psutil-only degraded mode.
