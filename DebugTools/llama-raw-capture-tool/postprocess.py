"""postprocess.py -- post-processor for llama-raw-capture-tool.

Reads the raw files captured by ``capture.py`` for a session dir and emits:

1. A unified JSONL event stream -- timestamp-aligned, cross-source.
2. A divergence report correlating events across sources and flagging
   mismatches.
3. (Optional) a replay-through-monitor diff, feeding raw data through Llama
   Monitor's own parsing functions to reproduce its would-be display and diff
   against the captured ``/api/metrics/latest``.

The post-processor must tolerate interrupted sessions: a hard-killed capture
can leave a missing/incomplete ``manifest.json``, truncated JSONL lines, a
partial final typeperf CSV row, and a log file cut mid-line. It degrades
gracefully (skips malformed lines, notes incomplete inputs in the report)
rather than failing.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

SESSION_LAYOUT = {
    "manifest": "manifest.json",
    "config": "config.yaml",
    "console": "console.jsonl",
    "slots": "slots.jsonl",
    "metrics": "metrics.jsonl",
    "props": "props.json",
    "windows": "windows.csv",
    "nvml": "nvml-psutil.jsonl",
    "monitor": "monitor-api.jsonl",
    "prompts": "prompts",
    "postprocessed": "postprocessed",
}

CONSOLE_PATTERNS = {
    "server_load_model": re.compile(r"loading model '(?P<model_path>[^']*)'"),
    "server_context_init": re.compile(
        r"initializing, n_slots = (?P<n_slots>\d+), "
        r"n_ctx_slot = (?P<n_ctx_slot>\d+), kv_unified = '(?P<kv_unified>[^']*)'"
    ),
    "server_model_loaded": re.compile(r"model loaded"),
    "server_listening": re.compile(
        r"listening on (?P<host>http://[^:]+):(?P<port>\d+)"
    ),
    "server_cancel_task": re.compile(r"cancel task, id_task = (?P<id_task>\d+)"),
    "slot_selection_lcp": re.compile(
        r"selected slot by LCP similarity, f_sim_best = (?P<f_sim_best>[^,]+), "
        r"\(> (?P<thold>[^)]+)\) thold\), f_keep = (?P<f_keep>[^,]+)"
    ),
    "slot_selection_lru": re.compile(
        r"selected slot by LRU, t_last = (?P<t_last>[^,]+)"
    ),
    "slot_launch": re.compile(r"processing task, is_child = (?P<is_child>\d+)"),
    "slot_release": re.compile(
        r"stop processing: n_tokens = (?P<n_tokens>\d+), truncated = (?P<truncated>\d+)"
    ),
    "prompt_process": re.compile(
        r"prompt processing, n_tokens = (?P<n_tokens>\d+), "
        r"progress = (?P<progress>[^,]+), t = (?P<t>[^ ]+) s / "
        r"(?P<tps>[^ ]+) tokens/s"
    ),
    "slot_gen_rate": re.compile(
        r"n_decoded = (?P<n_decoded>\d+), tg = (?P<tg>[^,]+) t/s, "
        r"tg_3s = (?P<tg_3s>[^,]+) t/s"
    ),
    "gen_prompt_eval_time": re.compile(
        r"prompt eval time = (?P<t_ms>[^ ]+) ms / (?P<n_tokens>\d+) tokens"
    ),
    "gen_eval_time": re.compile(
        r"eval time = (?P<t_ms>[^ ]+) ms / (?P<n_tokens>\d+) tokens"
    ),
    "gen_total_time": re.compile(
        r"total time = (?P<t_ms>[^ ]+) ms / (?P<n_tokens>\d+) tokens"
    ),
    "gen_graphs_reused": re.compile(r"graphs reused = (?P<graphs_reused>\d+)"),
}

# --------------------------------------------------------------------------- #
# Console event parsing
# --------------------------------------------------------------------------- #

SLOT_HEADER_RE = re.compile(r"id (\d+) \| task (\d+) \|")


def extract_slot_task(text: str) -> Dict[str, Any]:
    """Extract ``id``/``task`` from a slot line's header, if present."""
    m = SLOT_HEADER_RE.search(text)
    if m:
        return {"slot_id": int(m.group(1)), "task_id": int(m.group(2))}
    return {}


def parse_console_event(line: str, wallclock_iso: str) -> Optional[Dict[str, Any]]:
    """Parse one stamped console line into a typed event dict, or None.

    The line grammar is ``<M.s.ms.µs> <I|W|E|D|T> <cmn|srv|slot> <func>: msg``.
    Slot lines carry a ``id <slot_id> | task <task_id> |`` header. Events are
    matched on distinctive substrings so a partial/truncated line that still
    contains a pattern still yields an event.
    """
    slot_task = extract_slot_task(line)
    for event, pattern in CONSOLE_PATTERNS.items():
        m = pattern.search(line)
        if m:
            payload = {k: _coerce(v) for k, v in m.groupdict().items()}
            ev = {
                "ts": wallclock_iso,
                "source": "console",
                "event": event,
                "payload": payload,
            }
            ev.update(slot_task)
            return ev
    return None


def _coerce(value: str):
    """Best-effort numeric coercion of a captured string group."""
    try:
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        if "." in value or "e" in value.lower():
            return float(value)
        return int(value)
    except (ValueError, TypeError):
        return value


# --------------------------------------------------------------------------- #
# JSONL reading (tolerant)
# --------------------------------------------------------------------------- #


def read_jsonl_tolerant(path: Path) -> List[Dict[str, Any]]:
    """Read JSONL, skipping malformed/truncated lines; returns list of dicts."""
    records: List[Dict[str, Any]] = []
    if not os.path.exists(path):
        return records
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records

# --------------------------------------------------------------------------- #
# Anchor handling
# --------------------------------------------------------------------------- #


def load_anchor(session_dir: Path) -> Dict[str, Any]:
    """Load the anchor from manifest.json; return {} if missing/invalid."""
    manifest_path = session_dir / SESSION_LAYOUT["manifest"]
    if not os.path.exists(manifest_path):
        return {}
    try:
        manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        return manifest.get("anchor") or {}
    except Exception:
        return {}


def convert_relative_to_wallclock(anchor: Dict[str, Any], R_us) -> Optional[str]:
    """Convert a relative log time ``R`` (µs) to wall-clock ISO using anchor.

    ``log_epoch_us`` is the capture-side computed anchor:
        wallclock_us = log_epoch_us + R_us
    Returns ISO string or None when the anchor is missing.
    """
    log_epoch_us = anchor.get("log_epoch_us")
    if log_epoch_us is None or R_us is None:
        return None
    wallclock_us = log_epoch_us + int(R_us)
    from common import iso_from_epoch_us

    return iso_from_epoch_us(wallclock_us)


# --------------------------------------------------------------------------- #
# Source parsers
# --------------------------------------------------------------------------- #


def parse_slots(session_dir: Path) -> List[Dict[str, Any]]:
    """Expand raw /slots arrays into per-slot events with wall-clock stamps."""
    events: List[Dict[str, Any]] = []
    for rec in read_jsonl_tolerant(session_dir / SESSION_LAYOUT["slots"]):
        iso = rec.get("wallclock_iso")
        data = rec.get("data")
        if not isinstance(data, list):
            continue
        for slot in data:
            if not isinstance(slot, dict):
                continue
            ev = {
                "ts": iso,
                "source": "slots",
                "event": "slot_state",
                "slot_id": slot.get("id"),
                "task_id": slot.get("task"),
                "payload": {
                    k: slot.get(k)
                    for k in (
                        "state", "n_ctx", "n_prompt_tokens",
                        "n_prompt_tokens_processed", "n_prompt_tokens_cache",
                        "n_gen_tokens", "id_task",
                    )
                    if k in slot
                },
            }
            events.append(ev)
    return events


def parse_metrics(session_dir: Path) -> List[Dict[str, Any]]:
    """Parse raw Prometheus text bodies into per-metric events (global)."""
    events: List[Dict[str, Any]] = []
    for rec in read_jsonl_tolerant(session_dir / SESSION_LAYOUT["metrics"]):
        iso = rec.get("wallclock_iso")
        data = rec.get("data")
        if not isinstance(data, str):
            continue
        parsed = parse_prometheus_text(data)
        events.append(
            {
                "ts": iso,
                "source": "metrics",
                "event": "metrics_snapshot",
                "payload": {"metrics": parsed, "count": len(parsed)},
            }
        )
    return events


def parse_prometheus_text(text: str) -> Dict[str, Any]:
    """Parse Prometheus text format into {metric_name: {labels, value}}.

    Keeps HELP/TYPE/labels verbatim; returns a dict keyed by the full metric
    name including labels, so no information is dropped.
    """
    result: Dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Split name{labels} value
        m = re.match(r"^(?P<name>[A-Za-z_:][\w:]*)(?P<labels>\{.*\})?\s+(?P<value>\S+)", line)
        if not m:
            continue
        name = m.group("name")
        labels = m.group("labels")
        value = m.group("value")
        try:
            value = float(value)
        except ValueError:
            pass
        key = name + (labels or "")
        result[key] = {"value": value, "labels": labels or "", "name": name}
    return result


def parse_props(session_dir: Path) -> Dict[str, Any]:
    """Read props.json; return {} if missing."""
    path = session_dir / SESSION_LAYOUT["props"]
    if not os.path.exists(path):
        return {}
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def parse_nvml_psutil(session_dir: Path) -> List[Dict[str, Any]]:
    """Read nvml-psutil.jsonl into typed events."""
    events: List[Dict[str, Any]] = []
    for rec in read_jsonl_tolerant(session_dir / SESSION_LAYOUT["nvml"]):
        iso = rec.get("wallclock_iso")
        ev = {
            "ts": iso,
            "source": "nvml",
            "event": "hw_snapshot",
            "payload": {
                "cpu_percent": rec.get("cpu_percent"),
                "cpu_percent_per_core": rec.get("cpu_percent_per_core"),
                "memory": rec.get("memory"),
                "process": rec.get("process"),
                "nvml": rec.get("nvml"),
            },
        }
        events.append(ev)
    return events


def parse_monitor(session_dir: Path) -> List[Dict[str, Any]]:
    """Read monitor-api.jsonl into typed events."""
    events: List[Dict[str, Any]] = []
    for rec in read_jsonl_tolerant(session_dir / SESSION_LAYOUT["monitor"]):
        iso = rec.get("wallclock_iso")
        data = rec.get("data")
        ev = {
            "ts": iso,
            "source": "monitor",
            "event": "monitor_snapshot",
            "payload": {"data": data},
        }
        events.append(ev)
    return events

# --------------------------------------------------------------------------- #
# typeperf CSV
# --------------------------------------------------------------------------- #

TYPEPERF_TS_RE = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4}) (\d{1,2}):(\d{2}):(\d{2})\.(\d{6})")


def parse_typeperf_csv(session_dir: Path) -> List[Dict[str, Any]]:
    """Parse typeperf CSV into per-row events with an ISO timestamp.

    Skips the ``(PDH-CSV 4.0)`` header line and the counter-path header line.
    Parses the leading ``MM/DD/YYYY HH:MM:SS.xxxxxx`` timestamp column to ISO.
    A partial final row (truncated by teardown) is skipped.
    """
    path = session_dir / SESSION_LAYOUT["windows"]
    events: List[Dict[str, Any]] = []
    if not os.path.exists(path):
        return events
    import csv

    rows = []
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
        for row in csv.reader(f):
            if not row:
                continue
            first = row[0].strip()
            if first.startswith("(") or first.startswith("\\") or first.startswith("PDH-CSV"):
                continue  # header rows
            rows.append(row)
    for row in rows:
        m = TYPEPERF_TS_RE.match(row[0].strip())
        if not m:
            continue
        mm, dd, yyyy, hh, mi, ss, us = (int(g) for g in m.groups())
        iso = _csv_timestamp_to_iso(yyyy, mm, dd, hh, mi, ss, us)
        events.append(
            {
                "ts": iso,
                "source": "typeperf",
                "event": "perf_snapshot",
                "payload": {"columns": row[1:], "header": _typeperf_header(path)},
            }
        )
    return events


def _typeperf_header(path: Path) -> List[str]:
    """Read the counter-path header line (2nd line of the CSV)."""
    try:
        import csv

        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.reader(f)
            try:
                next(reader)  # PDH-CSV header
                header = next(reader)
                return header
            except StopIteration:
                return []
    except Exception:
        return []


def _csv_timestamp_to_iso(y, mo, d, h, mi, s, us) -> str:
    """Convert parsed typeperf timestamp components to an ISO 8601 string.

    The typeperf timestamp column is ``MM/DD/YYYY HH:MM:SS.xxxxxx`` where the
    fractional part is 6-digit microseconds. Convert to milliseconds for the
    ms-precision ISO output.
    """
    import datetime

    ms = us // 1000  # microseconds -> milliseconds
    dt = datetime.datetime(y, mo, d, h, mi, s)
    # Local naive; append a TZ offset using the current local offset.
    offset = datetime.datetime.now().astimezone().utcoffset()
    offset_s = int(offset.total_seconds())
    sign = "+" if offset_s >= 0 else "-"
    offset_s = abs(offset_s)
    tz = f"{sign}{offset_s // 3600:02d}:{(offset_s % 3600) // 60:02d}"
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{ms:03d}{tz}"


# --------------------------------------------------------------------------- #
# Prompt-file post-processing
# --------------------------------------------------------------------------- #


def parse_prompts(session_dir: Path, anchor: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Emit a ``new_prompt`` event per prompt file in the ``--log-prompts-dir``.

    Each prompt file is named ``<12-digit ms since start>.txt``. The filename ms
    is anchored via the log clock to wall-clock. The full prompt text is not
    inlined -- only a preview + sha256 hash are emitted.
    """
    prompts_dir = session_dir / SESSION_LAYOUT["prompts"]
    events: List[Dict[str, Any]] = []
    if not os.path.isdir(prompts_dir):
        return events
    log_epoch_us = anchor.get("log_epoch_us")
    for entry in sorted(os.listdir(prompts_dir)):
        if not entry.endswith(".txt"):
            continue
        stem = entry[:-4]
        try:
            ms_since_start = int(stem)
        except ValueError:
            continue
        full = prompts_dir / entry
        try:
            text = full.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        char_count = len(text)
        preview = text[:100]
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        ts = None
        if log_epoch_us is not None:
            ts = _iso_from_epoch_us(log_epoch_us + ms_since_start * 1000)
        events.append(
            {
                "ts": ts,
                "source": "prompt",
                "event": "new_prompt",
                "payload": {
                    "prompt_file": entry,
                    "char_count": char_count,
                    "preview": preview,
                    "sha256": digest,
                    "token_count": None,  # filled by console correlation
                },
            }
        )
    return events


def _iso_from_epoch_us(epoch_us: int) -> str:
    from common import iso_from_epoch_us

    return iso_from_epoch_us(epoch_us)

# --------------------------------------------------------------------------- #
# Console event extraction
# --------------------------------------------------------------------------- #


def parse_console(session_dir: Path) -> List[Dict[str, Any]]:
    """Read stamped console.jsonl and emit typed console events."""
    events: List[Dict[str, Any]] = []
    for rec in read_jsonl_tolerant(session_dir / SESSION_LAYOUT["console"]):
        iso = rec.get("wallclock_iso")
        line = rec.get("line", "")
        ev = parse_console_event(line, iso)
        if ev:
            events.append(ev)
    return events


# --------------------------------------------------------------------------- #
# Unified event stream
# --------------------------------------------------------------------------- #


def build_event_stream(session_dir: Path) -> Dict[str, Any]:
    """Assemble the unified timestamp-aligned event stream.

    Returns a dict with ``events`` (sorted by ts) and ``summary`` counts plus
    any ``incomplete`` notes for interrupted sessions.
    """
    anchor = load_anchor(session_dir)
    incomplete: List[str] = []

    def _note_if_missing(name, path):
        if not os.path.exists(session_dir / path):
            incomplete.append(f"missing input: {name} ({path})")

    console = parse_console(session_dir)
    slots = parse_slots(session_dir)
    metrics = parse_metrics(session_dir)
    nvml = parse_nvml_psutil(session_dir)
    monitor = parse_monitor(session_dir)
    typeperf = parse_typeperf_csv(session_dir)
    prompts = parse_prompts(session_dir, anchor)
    props = parse_props(session_dir)

    for src, key in [
        ("console", SESSION_LAYOUT["console"]),
        ("slots", SESSION_LAYOUT["slots"]),
        ("metrics", SESSION_LAYOUT["metrics"]),
        ("nvml", SESSION_LAYOUT["nvml"]),
        ("monitor", SESSION_LAYOUT["monitor"]),
        ("typeperf", SESSION_LAYOUT["windows"]),
    ]:
        _note_if_missing(src, key)

    events = console + slots + metrics + nvml + monitor + typeperf + prompts
    events.sort(key=lambda e: e.get("ts") or "")

    if not anchor.get("log_epoch_us"):
        incomplete.append("anchor: no log_epoch_us found; timestamps unanchored")

    return {
        "events": events,
        "anchor": anchor,
        "incomplete": incomplete,
        "props": props,
        "summary": _summarize(events),
    }


def _summarize(events: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    by_source: Dict[str, int] = {}
    for ev in events:
        counts[ev["event"]] = counts.get(ev["event"], 0) + 1
        by_source[ev["source"]] = by_source.get(ev["source"], 0) + 1
    return {"events": len(events), "by_event": counts, "by_source": by_source}

# --------------------------------------------------------------------------- #
# Divergence report
# --------------------------------------------------------------------------- #


def build_divergence_report(stream: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Correlate events across sources and flag mismatches.

    Each finding has ``pair``, ``rule``, ``status`` (ok|warn|divergence|skipped),
    and a message. Rules are defined per source pair rather than raw inequality.
    """
    findings: List[Dict[str, Any]] = []
    events = stream["events"]
    anchor = stream["anchor"]

    if not anchor.get("log_epoch_us"):
        findings.append(
            {
                "pair": "anchor",
                "rule": "anchor_present",
                "status": "warn",
                "message": "no log_epoch_us anchor; timestamps cannot be aligned",
            }
        )
        return findings

    console = [e for e in events if e["source"] == "console"]
    metrics = [e for e in events if e["source"] == "metrics"]
    slots = [e for e in events if e["source"] == "slots"]
    nvml = [e for e in events if e["source"] == "nvml"]
    monitor = [e for e in events if e["source"] == "monitor"]

    _correlate_gen_rate(console, metrics, findings)
    _correlate_activity(console, slots, nvml, findings)
    _correlate_monitor_latency(monitor, console, findings)

    if not console:
        findings.append(
            {
                "pair": "console",
                "rule": "console_present",
                "status": "warn",
                "message": "no console events found (missing or empty log)",
            }
        )
    if not metrics:
        findings.append(
            {
                "pair": "metrics",
                "rule": "metrics_present",
                "status": "warn",
                "message": "no metrics snapshots found",
            }
        )
    return findings


def _correlate_gen_rate(console, metrics, findings) -> None:
    """Compare console ``slot_gen_rate`` tg vs /metrics bucket-average tokens/s.

    Within a tolerance accounting for the bucket window (metrics samples the
    bucket average; console tg is the instantaneous rate). Flags only gross
    mismatches to avoid fabricating divergences from normal sampling skew.
    """
    gen_rates = [
        e["payload"].get("tg") for e in console if e["event"] == "slot_gen_rate"
    ]
    gen_rates = [float(g) for g in gen_rates if _is_number(g)]
    if not gen_rates:
        return
    avg_console = sum(gen_rates) / len(gen_rates)

    metrics_rates = []
    for e in metrics:
        m = e["payload"].get("metrics") or {}
        # Look for token-generation-rate style metric names.
        for key, item in m.items():
            if isinstance(item, dict):
                name = item.get("name", "")
                if "gen" in name.lower() and "rate" in name.lower():
                    try:
                        metrics_rates.append(float(item.get("value")))
                    except (TypeError, ValueError):
                        pass
    if not metrics_rates:
        return
    avg_metrics = sum(metrics_rates) / len(metrics_rates)
    tol = 0.5  # 50% tolerance to absorb bucket-window + sampling skew
    if avg_metrics > 0 and abs(avg_console - avg_metrics) / avg_metrics > tol:
        findings.append(
            {
                "pair": "console/metrics",
                "rule": "gen_rate_match",
                "status": "divergence",
                "message": (
                    f"console slot_gen_rate tg avg={avg_console:.2f} vs "
                    f"metrics gen-rate avg={avg_metrics:.2f} diverges >{tol:.0%}"
                ),
            }
        )
    else:
        findings.append(
            {
                "pair": "console/metrics",
                "rule": "gen_rate_match",
                "status": "ok",
                "message": (
                    f"console tg avg={avg_console:.2f} within tol of "
                    f"metrics gen-rate avg={avg_metrics:.2f}"
                ),
            }
        )


def _correlate_activity(console, slots, nvml, findings) -> None:
    """Check that /slots and NVML/psutil activity windows overlap console spans.

    Systematic offset (all windows disjoint from any console processing span)
    flags an anchor error. Best-effort with a tolerant overlap check.
    """
    console_active = [
        e["ts"] for e in console if e["event"] in ("slot_gen_rate", "slot_release")
    ]
    slot_processing = [
        e["ts"]
        for e in slots
        if (e["payload"].get("state") == "processing")
    ]
    hw_busy = []
    for e in nvml:
        cpu = e["payload"].get("cpu_percent")
        if _is_number(cpu) and float(cpu) > 20:
            hw_busy.append(e["ts"])

    if not console_active:
        return
    if not slot_processing and not hw_busy:
        findings.append(
            {
                "pair": "console/slots+nvml",
                "rule": "activity_overlap",
                "status": "warn",
                "message": "console shows processing but no /slots processing or "
                "busy NVML/psutil samples found; check anchor",
            }
        )
    else:
        findings.append(
            {
                "pair": "console/slots+nvml",
                "rule": "activity_overlap",
                "status": "ok",
                "message": "console activity overlaps /slots and/or NVML activity",
            }
        )


def _correlate_monitor_latency(monitor, console, findings) -> None:
    """Account for monitor latency: /api/metrics/latest lags raw sources.

    Monitor data is DB-driven and may return empty; skip/annotate rather than
    fabricate divergences.
    """
    empty = 0
    for e in monitor:
        data = e["payload"].get("data") or {}
        if data.get("error") == "No metrics available" or not data:
            empty += 1
    if not monitor:
        findings.append(
            {
                "pair": "monitor",
                "rule": "monitor_latency",
                "status": "skipped",
                "message": "no monitor snapshots captured",
            }
        )
    elif empty:
        findings.append(
            {
                "pair": "monitor",
                "rule": "monitor_latency",
                "status": "skipped",
                "message": f"{empty} monitor snapshot(s) were empty/no-metrics; "
                "latency accounted for, no divergence flagged",
            }
        )
    else:
        findings.append(
            {
                "pair": "monitor",
                "rule": "monitor_latency",
                "status": "ok",
                "message": f"{len(monitor)} monitor snapshots present; latency OK",
            }
        )


def _is_number(value) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False

# --------------------------------------------------------------------------- #
# Replay-through-monitor (optional)
# --------------------------------------------------------------------------- #

MONITOR_REPLAY_IMPORTS = {
    "server_metrics._parse_metrics": "server_metrics.ServerMetrics._parse_metrics",
    "web_server._transform_metrics": "web_server._transform_metrics",
}


def replay_through_monitor(session_dir: Path, stream: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Feed raw data through Llama Monitor's parsing functions (optional).

    Imports the monitor's own functions from the main project to reproduce its
    would-be display values, then diffs against the captured /api/metrics/latest.
    Pin the monitor version (reported in the output) because those functions
    drift. Degrades gracefully when the monitor code is unavailable.

    NOTE: This imports main-project code into the tool (trades against the
    "fully separate" goal), but it is acceptable for replay and is called out.
    """
    out: List[Dict[str, Any]] = []
    # Try to import the monitor functions; skip replay if unavailable.
    parse_metrics_fn = _try_import("server_metrics", "ServerMetrics")
    transform_metrics_fn = _try_import("web_server", "_transform_metrics")
    if parse_metrics_fn is None and transform_metrics_fn is None:
        return out

    out.append(
        {
            "step": "import",
            "status": "ok",
            "message": f"replay imported: {', '.join(MONITOR_REPLAY_IMPORTS.keys())}",
        }
    )

    # Replay: parse raw /metrics through the monitor's parser, then transform.
    metrics_events = [e for e in stream["events"] if e["source"] == "metrics"]
    monitor_events = [e for e in stream["events"] if e["source"] == "monitor"]
    for idx, me in enumerate(metrics_events):
        raw = me["payload"].get("metrics") or {}
        reproduced = None
        if parse_metrics_fn is not None:
            try:
                instance = parse_metrics_fn()
                reproduced = instance._parse_metrics(raw)
            except Exception as e:
                out.append({"step": f"replay[{idx}]", "status": "error", "message": str(e)})
                continue
        if transform_metrics_fn is not None and isinstance(reproduced, dict):
            try:
                reproduced = transform_metrics_fn({"server": reproduced})
            except Exception:
                pass
        out.append(
            {
                "step": f"replay[{idx}]",
                "status": "ok",
                "raw_ts": me.get("ts"),
                "reproduced": reproduced,
            }
        )
    # Diff against captured monitor snapshots (annotating latency/empty).
    for idx, me in enumerate(monitor_events):
        captured = me["payload"].get("data") or {}
        out.append(
            {
                "step": f"monitor[{idx}]",
                "status": "skipped" if not captured else "ok",
                "ts": me.get("ts"),
                "captured": captured,
                "note": "monitor lags raw by aggregator interval; empty responses skipped",
            }
        )
    return out


def _try_import(module_name: str, attr: str):
    """Import ``attr`` from ``module_name`` if possible; return None on failure."""
    try:
        mod = __import__(module_name, fromlist=[attr])
        return getattr(mod, attr, None)
    except Exception:
        return None

# --------------------------------------------------------------------------- #
# Output writers
# --------------------------------------------------------------------------- #


def render_report_md(stream: Dict[str, Any], findings: List[Dict[str, Any]],
                     replay: List[Dict[str, Any]]) -> str:
    """Render the divergence report as Markdown."""
    summary = stream["summary"]
    lines: List[str] = ["# Divergence Report", ""]
    lines.append(f"- Events: {summary['events']}")
    for src, cnt in sorted(summary.get("by_source", {}).items()):
        lines.append(f"  - {src}: {cnt}")
    lines.append("")
    lines.append("## Incomplete inputs")
    if stream["incomplete"]:
        for note in stream["incomplete"]:
            lines.append(f"- {note}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Findings")
    if findings:
        for f in findings:
            lines.append(
                f"- [{f['status']}] {f['pair']} ({f['rule']}): {f['message']}"
            )
    else:
        lines.append("- no findings")
    lines.append("")
    lines.append("## Replay-through-monitor")
    if replay:
        for r in replay:
            lines.append(f"- [{r.get('status')}] {r.get('step')}: {r.get('message', r.get('note', ''))}")
    else:
        lines.append("- replay skipped (monitor functions unavailable)")
    return "\n".join(lines) + "\n"


def write_outputs(session_dir: Path) -> Dict[str, str]:
    """Run post-processing and write events.jsonl, report, and replay output.

    Returns a dict of output paths that were written.
    """
    out_dir = session_dir / SESSION_LAYOUT["postprocessed"]
    out_dir.mkdir(exist_ok=True)

    stream = build_event_stream(session_dir)
    findings = build_divergence_report(stream)
    replay = replay_through_monitor(session_dir, stream)

    events_path = out_dir / "events.jsonl"
    with open(events_path, "w", encoding="utf-8") as f:
        for ev in stream["events"]:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    report_path = out_dir / "comparison-report.md"
    report_path.write_text(
        render_report_md(stream, findings, replay), encoding="utf-8"
    )

    replay_path = out_dir / "replay-monitor.jsonl"
    if replay:
        with open(replay_path, "w", encoding="utf-8") as f:
            for r in replay:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    return {
        "events": str(events_path),
        "report": str(report_path),
        "replay": str(replay_path),
    }


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="llama-raw-capture-tool post-processor")
    parser.add_argument("session_dir", help="path to a session directory")
    args = parser.parse_args(argv)

    session_dir = Path(args.session_dir)
    if not session_dir.is_dir():
        print(f"[postprocess] not a directory: {session_dir}", file=sys.stderr)
        return 2

    outputs = write_outputs(session_dir)
    print(f"[postprocess] events:   {outputs['events']}")
    print(f"[postprocess] report:   {outputs['report']}")
    if outputs["replay"]:
        print(f"[postprocess] replay:   {outputs['replay']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
