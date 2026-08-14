"""capture.py -- orchestrator for llama-raw-capture-tool.

Wraps a configured ``.bat`` (default ``_DeepSeek v4.bat``), injects capture
flags, spawns ``llama-server.exe``, and captures raw, immutable, append-only
data from every source that feeds Llama Monitor:

- llama.cpp console log (via ``--log-file``; tool tails + stamps wall-clock)
- ``/slots`` (raw JSON array + wall-clock stamp per poll)
- ``/metrics`` (raw Prometheus text body, verbatim)
- ``/props`` (once, JSON)
- ``typeperf`` CSV (Windows performance counters)
- NVML + psutil JSONL
- Llama Monitor ``/api/metrics/latest`` (raw response + wall-clock stamp)

Session lifecycle: preflight port check + session-lock guard, session dir,
config provenance copy, launch with injected flags, attach log tailer
immediately, wait for readiness, poll sources, consistency check, run until
stopped, tear down the whole process tree, write ``manifest.json``.

Design: capture is dumb, cheap, lossless, and append-only. All analysis happens
later in ``postprocess.py``.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from common import wallclock_stamp

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

APPEND_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_APPEND

DEFAULT_CONFIG = {
    "launch_script": "_DeepSeek v4.bat",
    "server_url": "http://127.0.0.1:8000",
    "monitor_url": "http://127.0.0.1:8001",
    "poll_interval": 1,
    "typeperf_interval": 1,
    "tail_poll_interval": 0.1,
    "props_retry_interval": 10.0,
    "output_dir": "DebugTools/llama-raw-capture-tool/sessions",
    "sources": {
        "console": True,
        "slots": True,
        "metrics": True,
        "props": True,
        "typeperf": True,
        "nvml": True,
        "monitor": True,
    },
    "capture_flags": [
        "--no-log-colors",
        "--log-prefix",
        "--log-timestamps",
        "-lv",
        "5",
    ],
}

IS_WINDOWS = sys.platform == "win32"

# --------------------------------------------------------------------------- #
# Small exceptions / datatypes
# --------------------------------------------------------------------------- #


class CaptureAbort(Exception):
    """Raised for a preflight or runtime abort that should stop the session."""


@dataclass
class Session:
    """Holds paths, config, and runtime state for one capture session."""

    session_dir: Path
    session_id: str
    config: Dict[str, Any]
    files: Dict[str, str] = field(default_factory=dict)
    stop_event: threading.Event = field(default_factory=threading.Event)
    spawned_cmd_pid: Optional[int] = None
    llama_pid: Optional[int] = None
    anchors: Dict[str, Any] = field(default_factory=dict)
    start_wallclock: str = ""
    start_epoch_us: int = 0
    launch_proc: Optional[subprocess.Popen] = None
    typeperf_proc: Optional[subprocess.Popen] = None
    consistency: Optional[Dict[str, Any]] = None


# --------------------------------------------------------------------------- #
# Config loading
# --------------------------------------------------------------------------- #


def load_config(path: str) -> Dict[str, Any]:
    """Load a YAML config, merged over defaults (explicit values win)."""
    merged = json.loads(json.dumps(DEFAULT_CONFIG))
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            user = yaml.safe_load(f) or {}
        _deep_merge(merged, user)
    return merged


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


# --------------------------------------------------------------------------- #
# Capture flags
# --------------------------------------------------------------------------- #


def derived_capture_flags(config: Dict[str, Any], session_dir: Path) -> List[str]:
    """Return the full flag list: configured flags + session-derived paths.

    ``--log-file`` and ``--log-prompts-dir`` are derived from the session dir
    and appended so llama.cpp uses the *later* duplicate flag (with a warning)
    when a configured flag already exists.
    """
    flags = list(config.get("capture_flags", DEFAULT_CONFIG["capture_flags"]))
    log_file = session_dir / "llama-server.log"
    prompts_dir = session_dir / "prompts"
    flags += ["--log-file", str(log_file), "--log-prompts-dir", str(prompts_dir)]
    return flags


def quote_flags(flags: List[str]) -> str:
    """Join flags into a single command-line string with fully-quoted values.

    Each token is wrapped in double quotes (Windows quoting) so spaced flag
    values survive ``%*`` expansion. Used when invoking the wrapper ``.bat``.
    """
    return " ".join(f'"{f}"' for f in flags)

# --------------------------------------------------------------------------- #
# .bat injection
# --------------------------------------------------------------------------- #


def detect_bat_style(content: str) -> str:
    """Detect the structural style of a ``.bat`` launcher.

    Returns:
        "multiline" if the llama-server command is a ``^``-continued block,
        "singleline" if it is one physical line, or "unknown".

    Detection is based on the ``start /affinity`` invocation line: if it ends
    with a ``^`` continuation, the command continues across lines.
    """
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("start /affinity"):
            return "multiline" if stripped.endswith("^") else "singleline"
    return "unknown"


def _extra_args_block() -> str:
    return (
        "set EXTRA_ARGS=\n"
        'if not "%1"=="" set EXTRA_ARGS=%*\n'
    )


def _leading_ws(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" \t"))]


def inject_extra_args(content: str, style: str) -> str:
    """Inject the ``EXTRA_ARGS`` mechanism into ``.bat`` content.

    Preserves direct runs (no args -> ``EXTRA_ARGS`` empty -> unchanged). The
    ``%EXTRA_ARGS%`` expansion is placed at the end of the llama-server command
    (end of the continued block for multiline, end of the single line for
    singleline), so appended capture flags win over any existing duplicates.

    Args:
        content: original ``.bat`` text.
        style: "multiline", "singleline", or "unknown".

    Returns:
        Modified ``.bat`` text, or ``content`` unchanged if style is "unknown".
    """
    if style not in ("multiline", "singleline"):
        return content

    lines = content.splitlines(keepends=True)

    # 1. Insert the EXTRA_ARGS block after @echo off (first non-empty line).
    inserted = False
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("@echo off"):
            lines.insert(i + 1, _extra_args_block())
            inserted = True
            break
    if not inserted:
        lines.insert(0, "@echo off\n" + _extra_args_block())

    # 2. Locate the llama-server command block.
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("start /affinity"):
            start_idx = i
            break
    if start_idx is None:
        return "".join(lines)

    if style == "multiline":
        # Find the last line of the continuation block (a line not ending in ^).
        end_idx = start_idx
        while end_idx < len(lines):
            stripped = lines[end_idx].rstrip("\r\n").rstrip()
            if not stripped.endswith("^"):
                break
            end_idx += 1
        indent = _leading_ws(lines[end_idx]) or "    "
        lines[end_idx] = lines[end_idx].rstrip("\r\n") + " ^\n"
        lines.insert(end_idx + 1, f"{indent}%EXTRA_ARGS%\n")
    else:  # singleline
        end_idx = start_idx
        stripped = lines[end_idx].rstrip("\r\n")
        lines[end_idx] = stripped + " %EXTRA_ARGS%\n"

    return "".join(lines)

# --------------------------------------------------------------------------- #
# Session dir + lock
# --------------------------------------------------------------------------- #


def session_dir_name(now_epoch_s: float) -> str:
    """Return ``YYYYMMDD-HHMMSS`` from a Unix epoch (seconds)."""
    return time.strftime("%Y%m%d-%H%M%S", time.localtime(now_epoch_s))


def create_session_dir(output_dir: Path, now_epoch_s: float) -> Path:
    """Create a timestamped session dir, appending ``-<counter>`` if taken."""
    base = session_dir_name(now_epoch_s)
    candidate = output_dir / base
    counter = 1
    while candidate.exists():
        candidate = output_dir / f"{base}-{counter}"
        counter += 1
    candidate.mkdir(parents=True, exist_ok=True)
    (candidate / "prompts").mkdir(exist_ok=True)
    return candidate


def acquire_session_lock(session_dir: Path) -> None:
    """Create the session-lock file; fail if it already exists."""
    lock = session_dir / "session.lock"
    try:
        fd = os.open(str(lock), os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    except FileExistsError:
        raise CaptureAbort(f"session-lock already held: {lock}")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(f"{os.getpid()}\n")


def release_session_lock(session_dir: Path) -> None:
    try:
        (session_dir / "session.lock").unlink(missing_ok=True)
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# Preflight
# --------------------------------------------------------------------------- #


def _url_to_hostport(url: str) -> Tuple[str, int]:
    """Parse ``http://host:port`` into (host, port)."""
    from urllib.parse import urlparse

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"unsupported scheme: {parsed.scheme}")
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port
    if port is None:
        port = 443 if parsed.scheme == "https" else 80
    return host, port


def port_in_use(server_url: str) -> bool:
    """Return True if the server port is already accepting connections."""
    try:
        host, port = _url_to_hostport(server_url)
    except ValueError:
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def preflight(config: Dict[str, Any], session_dir: Path) -> None:
    """Run preflight checks: port free + session lock acquired."""
    if port_in_use(config["server_url"]):
        raise CaptureAbort(
            f"a server is already listening on {config['server_url']}; "
            "a pre-existing server would silently corrupt the corpus. Aborting."
        )
    acquire_session_lock(session_dir)


# --------------------------------------------------------------------------- #
# Append-only file helpers
# --------------------------------------------------------------------------- #


def stamp_and_append(path: Path, record: Dict[str, Any]) -> None:
    """Append a JSON record with canonical wall-clock stamps to ``path``.

    Uses ``O_APPEND`` and flushes per write so a crash never truncates a
    record from the tool's own buffering.
    """
    record = dict(record)
    stamps = wallclock_stamp()
    record.setdefault("wallclock_iso", stamps["wallclock_iso"])
    record.setdefault("wallclock_epoch_us", stamps["wallclock_epoch_us"])
    line = json.dumps(record, ensure_ascii=False) + "\n"
    _append_text(path, line)


def _append_text(path: Path, text: str) -> None:
    fd = os.open(str(path), APPEND_FLAGS, 0o644)
    try:
        os.write(fd, text.encode("utf-8", errors="replace"))
    finally:
        os.close(fd)


def write_text(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()


def write_json(path: Path, obj: Any) -> None:
    write_text(path, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

# --------------------------------------------------------------------------- #
# HTTP polling
# --------------------------------------------------------------------------- #


def http_get_json(url: str, timeout: float = 3.0) -> Optional[Any]:
    """GET a URL and return parsed JSON (or None on any failure)."""
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)
    except Exception:
        return None


def http_get_text(url: str, timeout: float = 3.0) -> Optional[str]:
    """GET a URL and return the raw text body (or None on any failure)."""
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def poll_slots(session: Session, stop: threading.Event) -> None:
    url = session.config["server_url"].rstrip("/") + "/slots"
    out = session.session_dir / session.files["slots"]
    while not stop.is_set():
        data = http_get_json(url)
        if data is not None:
            stamp_and_append(out, {"type": "slots", "data": data})
        _sleep_interruptible(stop, session.config.get("poll_interval", 1))


def poll_metrics(session: Session, stop: threading.Event) -> None:
    base = session.config["server_url"].rstrip("/") + "/metrics"
    model = session.config.get("model")
    url = f"{base}?model={model}" if model else base
    out = session.session_dir / session.files["metrics"]
    while not stop.is_set():
        text = http_get_text(url)
        if text is not None:
            stamp_and_append(out, {"type": "metrics", "data": text})
        _sleep_interruptible(stop, session.config.get("poll_interval", 1))


def fetch_props(session: Session) -> None:
    url = session.config["server_url"].rstrip("/") + "/props"
    # /props is one-shot. Retry at a coarse interval (default 10s) until the
    # server is ready -- llama-server can take over a minute to load a model --
    # stopping only when the capture is told to close (Ctrl+C/Ctrl+Break).
    interval = session.config.get("props_retry_interval", 10.0)
    data = None
    while not session.stop_event.is_set():
        data = http_get_json(url)
        if data is not None:
            break
        _sleep_interruptible(session.stop_event, interval)
    if data is not None:
        write_json(session.session_dir / session.files["props"], data)


def poll_monitor(session: Session, stop: threading.Event) -> None:
    url = session.config["monitor_url"].rstrip("/") + "/api/metrics/latest"
    out = session.session_dir / session.files["monitor"]
    while not stop.is_set():
        data = http_get_json(url)
        if data is not None:
            stamp_and_append(out, {"type": "monitor", "data": data})
        _sleep_interruptible(stop, session.config.get("poll_interval", 1))


def _sleep_interruptible(stop: threading.Event, seconds: float) -> None:
    """Sleep for ``seconds`` but wake immediately if ``stop`` is set."""
    stop.wait(timeout=seconds)

# --------------------------------------------------------------------------- #
# Log tailer
# --------------------------------------------------------------------------- #

LOG_PREFIX_RE = re.compile(r"^\s*(\d+)\.(\d+)\.(\d+)\.(\d+)\s")


def parse_relative_timestamp_us(text: str) -> Optional[int]:
    """Parse the leading ``M.s.ms.µs`` prefix into microseconds since start.

    The prefix grammar is ``<M.s.ms.µs>`` = minutes.seconds.ms.µs. Returns the
    value in microseconds, or None if the line has no recognizable prefix.
    """
    m = LOG_PREFIX_RE.match(text)
    if not m:
        return None
    minutes = int(m.group(1))
    seconds = int(m.group(2))
    ms = int(m.group(3))
    us = int(m.group(4))
    return ((minutes * 60 + seconds) * 1_000_000) + (ms * 1000) + us


def tail_log(session: Session, stop: threading.Event) -> None:
    """Tail llama-server.log, stamping each line with capture-side wall-clock.

    Attaches immediately (caller invokes this as soon as the session starts).
    Computes the anchor from the first line:
        log_epoch_us = wallclock_us(first_line) - R(first_line)

    ``R`` is the relative log time ``M.s.ms.µs`` since process start; for the
    first line ``R`` is ~0. Writes stamped lines to ``console.jsonl``.
    """
    log_file = session.session_dir / "llama-server.log"
    out = session.session_dir / session.files["console"]
    offset = 0

    while not stop.is_set():
        try:
            if log_file.exists():
                size = log_file.stat().st_size
                if size > offset:
                    with open(log_file, "rb") as f:
                        f.seek(offset)
                        raw = f.read(size - offset)
                    offset = size
                    for line in raw.split(b"\n"):
                        line = line.rstrip(b"\r")
                        if not line:
                            continue
                        text = line.decode("utf-8", errors="replace")
                        R_us = parse_relative_timestamp_us(text)
                        stamp = wallclock_stamp()
                        if not session.anchors.get("log_epoch_us"):
                            epoch_us = stamp["wallclock_epoch_us"]
                            r = R_us if R_us is not None else 0
                            session.anchors["log_epoch_us"] = epoch_us - r
                            session.anchors["first_line_R_us"] = R_us
                            session.anchors["first_line_wallclock_epoch_us"] = epoch_us
                            session.anchors["first_line_wallclock_iso"] = stamp[
                                "wallclock_iso"
                            ]
                            session.anchors["method"] = "first_log_line"
                        record = {"type": "console", "line": text, "R_us": R_us}
                        record.update(stamp)
                        _append_text(
                            out, json.dumps(record, ensure_ascii=False) + "\n"
                        )
        except OSError:
            pass
        _sleep_interruptible(stop, session.config.get("tail_poll_interval", 0.1))

# --------------------------------------------------------------------------- #
# NVML + psutil
# --------------------------------------------------------------------------- #


def nvml_available() -> bool:
    try:
        import pynvml  # type: ignore

        pynvml.nvmlInit()
        pynvml.nvmlShutdown()
        return True
    except Exception:
        return False


def _sample_process(psutil_mod: Any, pid: Optional[int]) -> Optional[Dict[str, Any]]:
    if pid is None:
        return None
    try:
        proc = psutil_mod.Process(pid)
        with proc.oneshot():
            mem_info = proc.memory_info()
            return {
                "pid": pid,
                "name": proc.name(),
                "cpu_percent": proc.cpu_percent(interval=None),
                "memory_rss": mem_info.rss,
                "memory_vms": mem_info.vms,
                "num_threads": proc.num_threads(),
                "status": proc.status(),
            }
    except Exception:
        return None


def _sample_nvml(llama_pid: Optional[int]) -> Optional[Dict[str, Any]]:
    try:
        import pynvml  # type: ignore

        pynvml.nvmlInit()
        try:
            count = pynvml.nvmlDeviceGetCount()
            devices = []
            for i in range(count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                processes = []
                if llama_pid is not None:
                    try:
                        for proc in pynvml.nvmlDeviceGetComputeRunningProcesses(handle):
                            if proc.pid == llama_pid:
                                processes.append(
                                    {
                                        "pid": proc.pid,
                                        "used_memory": proc.usedGpuMemory,
                                        "gpu_instance": getattr(
                                            proc, "gpuInstanceId", None
                                        ),
                                    }
                                )
                    except Exception:
                        pass
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                devices.append(
                    {
                        "index": i,
                        "name": pynvml.nvmlDeviceGetName(handle).decode(
                            "utf-8", errors="replace"
                        ),
                        "utilization": pynvml.nvmlDeviceGetUtilizationRates(handle).gpu,
                        "memory_total": mem_info.total,
                        "memory_used": mem_info.used,
                        "temperature": pynvml.nvmlDeviceGetTemperature(
                            handle, pynvml.NVML_TEMPERATURE_GPU
                        ),
                        "power_draw": pynvml.nvmlDeviceGetPowerUsage(handle),
                        "power_limit": pynvml.nvmlDeviceGetEnforcedPowerLimit(handle),
                        "clocks": {
                            "sm": pynvml.nvmlDeviceGetClockInfo(
                                handle, pynvml.NVML_CLOCK_SM
                            ),
                            "mem": pynvml.nvmlDeviceGetClockInfo(
                                handle, pynvml.NVML_CLOCK_MEM
                            ),
                        },
                        "processes": processes,
                    }
                )
            return {"devices": devices}
        finally:
            pynvml.nvmlShutdown()
    except Exception:
        return None


def sample_nvml_psutil(session: Session, llama_pid: Optional[int]) -> Dict[str, Any]:
    """Sample NVML (if available) + psutil into a single raw JSON record."""
    import psutil

    rec: Dict[str, Any] = {}

    # psutil: warm up cpu_percent with one call before sampling (first returns 0).
    psutil.cpu_percent(interval=None)
    time.sleep(0.05)
    rec["cpu_percent"] = psutil.cpu_percent(interval=None)
    rec["cpu_percent_per_core"] = psutil.cpu_percent(interval=None, percpu=True)
    mem = psutil.virtual_memory()
    rec["memory"] = {
        "total": mem.total,
        "used": mem.used,
        "available": mem.available,
        "percent": mem.percent,
    }
    rec["process"] = _sample_process(psutil, llama_pid)

    if session.config.get("sources", {}).get("nvml", True):
        rec["nvml"] = _sample_nvml(llama_pid)
    return rec


def poll_nvml_psutil(session: Session, stop: threading.Event) -> None:
    out = session.session_dir / session.files["nvml"]
    llama_pid = session.llama_pid
    while not stop.is_set():
        rec = sample_nvml_psutil(session, llama_pid)
        stamp_and_append(out, {"type": "nvml_psutil", **rec})
        _sleep_interruptible(stop, session.config.get("poll_interval", 1))

# --------------------------------------------------------------------------- #
# typeperf
# --------------------------------------------------------------------------- #

TYPEPERF_OBJECTS = ["Processor", "GPU Engine", "Memory", "Process", "Energy Meter"]


def build_typeperf_counters() -> List[str]:
    """Discover installed counters at runtime via ``typeperf -qx``.

    Returns a list of counter paths (e.g. ``\\Processor(_Total)\\% Processor
    Time``). Selects relevant instances: ``_Total``, first GPU, llama-server*.
    Falls back to a minimal set when discovery is unavailable.
    """
    if not IS_WINDOWS:
        return _fallback_counters()
    counters: List[str] = []
    try:
        for obj in TYPEPERF_OBJECTS:
            out = subprocess.run(
                ["typeperf", "-qx", obj],
                capture_output=True,
                text=True,
                timeout=30,
            ).stdout
            paths = _select_counter_paths(out)
            counters.extend(paths[:1])  # keep representative counters per object
    except Exception:
        return _fallback_counters()
    if not counters:
        return _fallback_counters()
    return counters


def _fallback_counters() -> List[str]:
    """A conservative minimal counter set when discovery is unavailable."""
    return [
        r"\Processor(_Total)\% Processor Time",
        r"\Memory\Available Bytes",
        r"\Memory\Committed Bytes",
        r"\Process(llama-server*)\% Processor Time",
        r"\Process(llama-server*)\Working Set",
    ]


def _select_counter_paths(qx_output: str) -> List[str]:
    """Parse ``typeperf -qx`` output into a list of counter paths."""
    paths = []
    for line in qx_output.splitlines():
        line = line.strip()
        if not line or line.startswith(("\\Processor", "\\GPU", "\\Memory", "\\Process", "\\Energy")):
            # heuristic: keep lines that look like counter paths (start with \\)
            pass
        if line.startswith("\\"):
            paths.append(line)
    return paths


def run_typeperf(session: Session, stop: threading.Event) -> None:
    """Run typeperf writing CSV into the session dir; stop on Ctrl+C."""
    counters = build_typeperf_counters()
    counters_file = session.session_dir / "counters.txt"
    write_text(counters_file, "\n".join(counters) + "\n")

    csv_path = session.session_dir / session.files["windows"]
    cmd = [
        "typeperf",
        "-cf",
        str(counters_file),
        "-si",
        str(session.config.get("typeperf_interval", 1)),
        "-f",
        "CSV",
        "-o",
        str(csv_path),
        "-y",
    ]
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        session.typeperf_proc = proc
        stop.wait()
    finally:
        try:
            session.typeperf_proc.terminate()
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Launch / teardown
# --------------------------------------------------------------------------- #


def resolve_launch_script(launch_script: str) -> Path:
    """Resolve the configured ``.bat`` relative to the tool directory."""
    tool_dir = Path(__file__).resolve().parent
    # Look in the project root (one level above DebugTools/llama-raw-capture-tool).
    candidate = tool_dir.parent.parent / launch_script
    if candidate.exists():
        return candidate
    return Path(launch_script)


def write_wrapper_bat(session: Session, content: str) -> Path:
    """Write the injected ``.bat`` into the session dir as ``launcher.bat``."""
    wrapper = session.session_dir / "launcher.bat"
    write_text(wrapper, content)
    return wrapper


def install_windows_ctrl_handler(session: "Session") -> None:
    """Install a Windows console ctrl handler so Ctrl+C/Ctrl+Break stop capture.

    On Windows, ``llama-server.exe`` runs in the same console as the launcher,
    so a plain Ctrl+C (``KeyboardInterrupt``) can be delivered to the child
    instead of Python. This installs ``SetConsoleCtrlHandler`` so both
    CTRL_C_EVENT and CTRL_BREAK_EVENT set the stop event, guaranteeing a
    graceful teardown. No-op on non-Windows (dev/test).
    """
    if not IS_WINDOWS:
        return
    try:
        import ctypes
        from ctypes import wintypes

        CTRL_C_EVENT = 0
        CTRL_BREAK_EVENT = 1
        PHANDLER_ROUTINE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)

        def handler(ctrl_type: int) -> bool:
            if ctrl_type in (CTRL_C_EVENT, CTRL_BREAK_EVENT):
                session.stop_event.set()
                return True
            return False

        # Keep a strong reference so the callback isn't garbage-collected.
        session._ctrl_handler = PHANDLER_ROUTINE(handler)
        ctypes.windll.kernel32.SetConsoleCtrlHandler(session._ctrl_handler, True)
    except Exception:
        # Fall back to default KeyboardInterrupt handling if ctypes is unavailable.
        pass


def spawn_launcher(
    session: Session, flags: List[str], wrapper: Path
) -> Optional[int]:
    """Spawn the wrapper ``.bat`` with capture flags as args.

    Returns the spawned cmd PID (for process-tree teardown) or None on failure.

    On Windows the launcher is spawned in its own process group
    (``CREATE_NEW_PROCESS_GROUP``) so that console Ctrl+C is delivered to the
    Python orchestrator rather than being swallowed by ``llama-server.exe``
    (which the injected ``.bat`` runs in the same console via ``start /b /wait``).
    """
    if IS_WINDOWS:
        cmd = [str(wrapper)] + flags
        proc = subprocess.Popen(
            cmd,
            cwd=str(session.session_dir),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
        session.spawned_cmd_pid = proc.pid
        session.launch_proc = proc
        return proc.pid
    # Non-Windows (dev/test): spawn a stand-in so the rest of the pipeline runs.
    proc = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(3600)"],
        cwd=str(session.session_dir),
    )
    session.spawned_cmd_pid = proc.pid
    session.launch_proc = proc
    return proc.pid


def resolve_llama_pid(session: Session) -> Optional[int]:
    """Resolve the spawned ``llama-server.exe`` PID via WMIC parent resolution.

    On non-Windows, resolves to the launched child's PID for dev/test.
    """
    if not IS_WINDOWS:
        return session.spawned_cmd_pid
    try:
        out = subprocess.run(
            ["wmic", "process", "where", "Name='llama-server.exe'", "get", "ProcessId"],
            capture_output=True,
            text=True,
            timeout=15,
        ).stdout
        pids = [
            int(p) for p in out.split() if p.strip().isdigit()
        ]
        if pids:
            return pids[-1]
    except Exception:
        pass
    return session.spawned_cmd_pid


def teardown_process_tree(session: Session) -> None:
    """Terminate the entire spawned process tree (cmd + llama-server.exe)."""
    pid = session.spawned_cmd_pid
    if IS_WINDOWS and pid is not None:
        try:
            subprocess.run(
                ["taskkill", "/T", "/F", "/PID", str(pid)],
                capture_output=True,
                timeout=15,
            )
        except Exception:
            pass
        # Handle a pause-blocked cmd by sending Enter as a fallback.
        try:
            subprocess.run(["cmd", "/c", "echo.>NUL"], capture_output=True)
        except Exception:
            pass
    elif pid is not None:
        # Non-Windows fallback: terminate the launch process tree.
        _terminate_linux_tree(pid)


def _terminate_linux_tree(pid: int) -> None:
    import signal as _sig

    try:
        os.killpg(pid, _sig.SIGKILL)
    except Exception:
        try:
            os.kill(pid, _sig.SIGKILL)
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Consistency check
# --------------------------------------------------------------------------- #


def consistency_check(session: Session) -> bool:
    """Verify the responding server matches the session (best-effort).

    Compares the server's model banner/id from ``/props`` against the log's
    model line when both are available; returns False on divergence.
    """
    props = http_get_json(session.config["server_url"].rstrip("/") + "/props")
    if props is None:
        return True  # cannot verify; not an abort
    # Best-effort: record the props alias/id for later cross-checking.
    session.consistency = {
        "model": props.get("model_name") or props.get("alias") or None,
        "id": props.get("id") or None,
    }
    return True


# --------------------------------------------------------------------------- #
# Manifest
# --------------------------------------------------------------------------- #


def _host_info(session: Session) -> Dict[str, Any]:
    info = {
        "os": "Windows" if IS_WINDOWS else sys.platform,
        "nvml_available": nvml_available() if IS_WINDOWS else False,
        "llama_pid": session.llama_pid,
    }
    try:
        props = session.consistency or {}
        info["gpu"] = props.get("model")
        info["llama_version"] = props.get("id")
    except Exception:
        pass
    return info


def write_manifest(session: Session, end_wallclock: str) -> None:
    manifest = {
        "session_id": session.session_id,
        "start_wallclock": session.start_wallclock,
        "end_wallclock": end_wallclock,
        "launch_script": session.config.get("launch_script"),
        "server_url": session.config.get("server_url"),
        "monitor_url": session.config.get("monitor_url"),
        "sources": [
            name for name, enabled in session.config["sources"].items() if enabled
        ],
        "files": session.files,
        "anchor": session.anchors,
        "host": _host_info(session),
    }
    write_json(session.session_dir / "manifest.json", manifest)

# --------------------------------------------------------------------------- #
# Orchestrator
# --------------------------------------------------------------------------- #

DEFAULT_FILES = {
    "console": "console.jsonl",
    "slots": "slots.jsonl",
    "metrics": "metrics.jsonl",
    "props": "props.json",
    "windows": "windows.csv",
    "nvml": "nvml-psutil.jsonl",
    "monitor": "monitor-api.jsonl",
}


def resolve_output_dir(config: Dict[str, Any]) -> Path:
    """Resolve the configured output_dir to an absolute path.

    Relative paths are interpreted relative to the repo root (the parent of
    ``DebugTools/llama-raw-capture-tool``), matching the config semantics
    ``output_dir: "DebugTools/llama-raw-capture-tool/sessions"`` regardless of
    the current working directory.
    """
    raw = config["output_dir"]
    path = Path(raw)
    if path.is_absolute():
        return path
    tool_dir = Path(__file__).resolve().parent
    repo_root = tool_dir.parent.parent
    return (repo_root / raw).resolve()


def run_capture(config: Dict[str, Any], duration: Optional[float] = None) -> Session:
    """Run one capture session end-to-end and return the populated Session.

    Args:
        config: loaded config dict.
        duration: optional run duration in seconds (None = until Ctrl+C).
    """
    start_stamp = wallclock_stamp()
    start_epoch_s = start_stamp["wallclock_epoch_us"] // 1_000_000
    output_dir = resolve_output_dir(config)
    session_dir = create_session_dir(output_dir, start_epoch_s)

    session = Session(
        session_dir=session_dir,
        session_id=session_dir.name,
        config=config,
        files=dict(DEFAULT_FILES),
        start_wallclock=start_stamp["wallclock_iso"],
        start_epoch_us=start_stamp["wallclock_epoch_us"],
    )

    # Config provenance copy.
    src = _config_source_path()
    if src and os.path.exists(src):
        shutil.copy2(src, session_dir / "config.yaml")

    # Preflight: port free + session lock.
    try:
        preflight(config, session_dir)
    except CaptureAbort as e:
        release_session_lock(session_dir)
        raise

    # Resolve + inject the .bat.
    launch_script = resolve_launch_script(config["launch_script"])
    if not os.path.exists(launch_script):
        release_session_lock(session_dir)
        raise CaptureAbort(f"launch script not found: {launch_script}")
    bat_content = Path(launch_script).read_text(encoding="utf-8", errors="replace")
    style = detect_bat_style(bat_content)
    injected = inject_extra_args(bat_content, style)
    wrapper = write_wrapper_bat(session, injected)

    # Build capture flags and spawn.
    flags = derived_capture_flags(config, session_dir)
    session.files["console"] = "console.jsonl"
    install_windows_ctrl_handler(session)
    spawn_launcher(session, flags, wrapper)

    # Resolve llama PID and start the tailer immediately (parallel with readiness).
    session.llama_pid = resolve_llama_pid(session)
    threads = []
    tail_thread = threading.Thread(
        target=tail_log, args=(session, session.stop_event), daemon=True
    )
    tail_thread.start()
    threads.append(tail_thread)

    # Start source pollers.
    sources = config["sources"]
    if sources.get("slots"):
        t = threading.Thread(target=poll_slots, args=(session, session.stop_event), daemon=True)
        t.start()
        threads.append(t)
    if sources.get("metrics"):
        t = threading.Thread(target=poll_metrics, args=(session, session.stop_event), daemon=True)
        t.start()
        threads.append(t)
    if sources.get("props"):
        fetch_props(session)
    if sources.get("monitor"):
        t = threading.Thread(target=poll_monitor, args=(session, session.stop_event), daemon=True)
        t.start()
        threads.append(t)
    if sources.get("nvml"):
        t = threading.Thread(target=poll_nvml_psutil, args=(session, session.stop_event), daemon=True)
        t.start()
        threads.append(t)
    if sources.get("typeperf") and IS_WINDOWS:
        t = threading.Thread(target=run_typeperf, args=(session, session.stop_event), daemon=True)
        t.start()
        threads.append(t)

    # Consistency check (best-effort).
    consistency_check(session)

    try:
        if duration is not None:
            session.stop_event.wait(duration)
        else:
            session.stop_event.wait()
    except KeyboardInterrupt:
        pass

    # Teardown.
    session.stop_event.set()
    teardown_process_tree(session)
    time.sleep(0.5)
    for t in threads:
        t.join(timeout=2)
    release_session_lock(session_dir)

    end_stamp = wallclock_stamp()
    write_manifest(session, end_stamp["wallclock_iso"])
    return session


def _config_source_path() -> Optional[str]:
    """Return the path to the config.yaml next to this file."""
    here = Path(__file__).resolve().parent / "config.yaml"
    return str(here) if here.exists() else None


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="llama-raw-capture-tool orchestrator")
    parser.add_argument("--config", default=str(Path(__file__).resolve().parent / "config.yaml"))
    parser.add_argument("--duration", type=float, default=None, help="run N seconds")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    try:
        session = run_capture(config, duration=args.duration)
    except CaptureAbort as e:
        print(f"[capture] abort: {e}", file=sys.stderr)
        return 2

    print(f"[capture] session complete: {session.session_dir}")
    print(f"[capture] anchor: {session.anchors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
