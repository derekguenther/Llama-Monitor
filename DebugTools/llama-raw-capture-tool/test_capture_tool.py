"""Tests for llama-raw-capture-tool (capture.py, postprocess.py, common.py).

Run with ``pytest`` from the tool directory:

    python -m pytest test_capture_tool.py -v
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

# Ensure the tool directory is importable.
TOOL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOL_DIR))

import capture
import postprocess
from common import iso_from_epoch_us, wallclock_stamp


# --------------------------------------------------------------------------- #
# common.py
# --------------------------------------------------------------------------- #


def test_wallclock_stamp_has_both_fields():
    stamp = wallclock_stamp()
    assert "wallclock_iso" in stamp
    assert "wallclock_epoch_us" in stamp
    assert stamp["wallclock_epoch_us"] > 1_000_000_000_000  # year ~2001+


def test_iso_from_epoch_us_known_epoch():
    # 1609459200123000 us = 2021-01-01T00:00:00.123Z (UTC); local tz may shift
    # the date but the ms precision and local date must be consistent.
    import time

    epoch_us = 1609459200123000
    epoch_s = epoch_us // 1_000_000
    iso = iso_from_epoch_us(epoch_us)
    lt = time.localtime(epoch_s)
    assert iso.startswith(time.strftime("%Y-%m-%dT%H:%M:%S", lt))
    assert ":00.123" in iso


# --------------------------------------------------------------------------- #
# capture.py -- .bat injection
# --------------------------------------------------------------------------- #

MULTILINE_BAT = """\
@echo off

call conda activate llama.cpp
set SERVER_BIN=C:\\path\\llama-server.exe

start /affinity FFFF /b /wait "" "%SERVER_BIN%" ^
    -m "%MODEL_PATH%" ^
    --port 8000 ^
    --ubatch-size 1024

if %ERRORLEVEL% NEQ 0 pause
"""

SINGLELINE_BAT = """\
@echo off

set ANTHROPIC_BASE_URL=http://127.0.0.1:8000
start /affinity FFFF /b /wait "" "C:\\path\\Release\\llama-server.exe" -m "D:\\model.gguf" --port 8000 --metrics
if %ERRORLEVEL% NEQ 0 pause
"""


def test_detect_bat_style_multiline():
    assert capture.detect_bat_style(MULTILINE_BAT) == "multiline"


def test_detect_bat_style_singleline():
    assert capture.detect_bat_style(SINGLELINE_BAT) == "singleline"


def test_detect_bat_style_unknown():
    assert capture.detect_bat_style("@echo off\nrem nothing here\n") == "unknown"


def test_inject_extra_args_multiline():
    injected = capture.inject_extra_args(MULTILINE_BAT, "multiline")
    assert "set EXTRA_ARGS=" in injected
    assert "%EXTRA_ARGS%" in injected
    # The %EXTRA_ARGS% must be inside the continued command block.
    assert "    %EXTRA_ARGS%\n" in injected
    # The last command line must now be continued.
    assert "--ubatch-size 1024 ^" in injected


def test_inject_extra_args_singleline():
    injected = capture.inject_extra_args(SINGLELINE_BAT, "singleline")
    assert "set EXTRA_ARGS=" in injected
    # %EXTRA_ARGS% appended to the single-line command.
    assert "--metrics %EXTRA_ARGS%\n" in injected


def test_inject_extra_args_unknown_unchanged():
    content = "@echo off\nrem hi\n"
    assert capture.inject_extra_args(content, "unknown") == content


def test_inject_preserves_direct_run_semantics():
    injected = capture.inject_extra_args(MULTILINE_BAT, "multiline")
    # When no args, EXTRA_ARGS is empty -> %EXTRA_ARGS% expands to nothing.
    assert 'if not "%1"=="" set EXTRA_ARGS=%*' in injected


# --------------------------------------------------------------------------- #
# capture.py -- flags
# --------------------------------------------------------------------------- #


def test_derived_capture_flags(tmp_path):
    config = {
        "capture_flags": ["--no-log-colors", "-lv", "5"],
    }
    flags = capture.derived_capture_flags(config, tmp_path)
    assert "--log-file" in flags
    assert str(tmp_path / "llama-server.log") in flags
    assert "--log-prompts-dir" in flags
    assert str(tmp_path / "prompts") in flags


def test_quote_flags_quotes_every_token():
    quoted = capture.quote_flags(["--log-file", "C:/path with space/log"])
    assert quoted == '"--log-file" "C:/path with space/log"'


# --------------------------------------------------------------------------- #
# capture.py -- relative timestamp parsing
# --------------------------------------------------------------------------- #


def test_parse_relative_timestamp_us():
    assert capture.parse_relative_timestamp_us("22.33.678.404 srv foo: bar") == (
        1353 * 1_000_000 + 678 * 1000 + 404
    )


def test_parse_relative_timestamp_us_none():
    assert capture.parse_relative_timestamp_us("no prefix here") is None


# --------------------------------------------------------------------------- #
# capture.py -- session dir + append helpers
# --------------------------------------------------------------------------- #


def test_session_dir_name_format():
    import time

    name = capture.session_dir_name(time.time())
    assert len(name) == 15  # YYYYMMDD-HHMMSS


def test_create_session_dir_and_counter(tmp_path):
    import time

    epoch = time.time()
    first = capture.create_session_dir(tmp_path, epoch)
    second = capture.create_session_dir(tmp_path, epoch + 1)
    assert first.is_dir()
    assert second.is_dir()
    assert first.name != second.name


def test_stamp_and_append(tmp_path):
    path = tmp_path / "out.jsonl"
    capture.stamp_and_append(path, {"type": "slots", "data": []})
    capture.stamp_and_append(path, {"type": "slots", "data": []})
    lines = path.read_text().strip().splitlines()
    assert len(lines) == 2
    rec = json.loads(lines[0])
    assert rec["type"] == "slots"
    assert "wallclock_iso" in rec
    assert "wallclock_epoch_us" in rec


# --------------------------------------------------------------------------- #
# capture.py -- config + preflight helpers
# --------------------------------------------------------------------------- #


def test_load_config_merges_defaults(tmp_path):
    cfg = tmp_path / "c.yaml"
    cfg.write_text("server_url: http://127.0.0.1:9999\nsources:\n  slots: false\n")
    loaded = capture.load_config(str(cfg))
    assert loaded["server_url"] == "http://127.0.0.1:9999"
    assert loaded["sources"]["slots"] is False
    assert loaded["sources"]["metrics"] is True  # default preserved


def test_port_in_use_false_for_unbound():
    # An unused high port should report not-in-use (or error -> False).
    assert capture.port_in_use("http://127.0.0.1:59999") is False


def test_preflight_when_port_free(tmp_path):
    cfg = {"server_url": "http://127.0.0.1:59998"}
    capture.preflight(cfg, tmp_path)
    assert (tmp_path / "session.lock").exists()
    capture.release_session_lock(tmp_path)


def test_preflight_port_in_use_aborts(tmp_path):
    # Bind a socket to a port then preflight should raise CaptureAbort.
    import socket
    import threading

    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]
    cfg = {"server_url": f"http://127.0.0.1:{port}"}
    try:
        capture.preflight(cfg, tmp_path)
        assert False, "expected CaptureAbort"
    except capture.CaptureAbort:
        pass
    finally:
        srv.close()


# --------------------------------------------------------------------------- #
# postprocess.py -- console event parsing
# --------------------------------------------------------------------------- #


def _stamp_line(line):
    return capture.parse_relative_timestamp_us(line)


def test_parse_console_slot_gen_rate():
    line = "22.33.678.404 srv slot id 4 | task 184 | gen: n_decoded = 100, tg = 10.44 t/s, tg_3s = 10.44 t/s"
    ev = postprocess.parse_console_event(line, "2026-08-13T09:15:30.123-07:00")
    assert ev is not None
    assert ev["event"] == "slot_gen_rate"
    assert ev["slot_id"] == 4
    assert ev["task_id"] == 184
    assert ev["payload"]["tg"] == 10.44


def test_parse_console_server_listening():
    line = "0.0.0.1.2 srv server: HTTP server listening on http://0.0.0.0:8000"
    ev = postprocess.parse_console_event(line, "2026-08-13T09:15:30.000-07:00")
    assert ev is not None
    assert ev["event"] == "server_listening"
    assert ev["payload"]["port"] == 8000


def test_parse_console_prompt_process():
    line = (
        "5.10.200.5 srv slot id 1 | task 9 | prompt: prompt processing, "
        "n_tokens = 512, progress = 0.5, t = 1.2 s / 420 tokens/s"
    )
    ev = postprocess.parse_console_event(line, "2026-08-13T09:15:35.000-07:00")
    assert ev is not None
    assert ev["event"] == "prompt_process"
    assert ev["payload"]["n_tokens"] == 512


def test_parse_console_returns_none_for_unmatched():
    assert postprocess.parse_console_event("garbage line", "ts") is None


# --------------------------------------------------------------------------- #
# postprocess.py -- prometheus text
# --------------------------------------------------------------------------- #


def test_parse_prometheus_text_keeps_labels():
    text = (
        "# HELP llamacpp:slots_idle Number of idle slots\n"
        "# TYPE llamacpp:slots_idle gauge\n"
        'llamacpp:slots_idle{model="qwen3"} 3\n'
        "llamacpp:slots_processing 2\n"
    )
    parsed = postprocess.parse_prometheus_text(text)
    assert len(parsed) == 2
    assert 'llamacpp:slots_idle{model="qwen3"}' in parsed
    assert parsed['llamacpp:slots_idle{model="qwen3"}']["value"] == 3
    assert parsed["llamacpp:slots_processing"]["value"] == 2


# --------------------------------------------------------------------------- #
# postprocess.py -- typeperf CSV
# --------------------------------------------------------------------------- #


def test_parse_typeperf_csv_skips_headers(tmp_path):
    csv_content = (
        "(PDH-CSV 4.0) (Eastern Daylight Time) (0)\n"
        "\\Processor(_Total)\\% Processor Time,\\Memory\\Available Bytes\n"
        "08/13/2026 09:15:30.123456,5.0,1024000\n"
        "08/13/2026 09:15:31.123456,6.0,2048000\n"
        "08/13/2026 09:15:32.123456,7.0,3072000\n"
        "08/13/2026 09:15:33.12,8.0,4096000\n"  # truncated final row -> skipped
    )
    (tmp_path / "windows.csv").write_text(csv_content)
    events = postprocess.parse_typeperf_csv(tmp_path)
    assert len(events) == 3
    assert events[0]["ts"].startswith("2026-08-13T09:15:30.123")
    assert events[0]["payload"]["header"][0].startswith("\\Processor")
    assert events[0]["payload"]["columns"] == ["5.0", "1024000"]


def test_parse_typeperf_csv_missing_file(tmp_path):
    assert postprocess.parse_typeperf_csv(tmp_path) == []


# --------------------------------------------------------------------------- #
# postprocess.py -- prompts
# --------------------------------------------------------------------------- #


def test_parse_prompts(tmp_path, anchor_factory):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    # 12-digit ms-since-start filename: 1000 ms -> 000000001000
    (prompts_dir / "000000001000.txt").write_text("Hello world, this is a prompt!")
    anchor = anchor_factory(1_750_000_000_000_000)
    events = postprocess.parse_prompts(tmp_path, anchor)
    assert len(events) == 1
    ev = events[0]
    assert ev["source"] == "prompt"
    assert ev["event"] == "new_prompt"
    assert ev["payload"]["char_count"] == len("Hello world, this is a prompt!")
    assert ev["payload"]["sha256"]
    assert ev["payload"]["prompt_file"] == "000000001000.txt"


# --------------------------------------------------------------------------- #
# postprocess.py -- end-to-end stream + report
# --------------------------------------------------------------------------- #


def test_build_event_stream_and_report(tmp_path):
    _write_minimal_session(tmp_path)
    stream = postprocess.build_event_stream(tmp_path)
    assert stream["events"], "expected at least one event"
    findings = postprocess.build_divergence_report(stream)
    assert isinstance(findings, list)


def test_write_outputs(tmp_path):
    _write_minimal_session(tmp_path)
    outputs = postprocess.write_outputs(tmp_path)
    assert os.path.exists(outputs["events"])
    assert os.path.exists(outputs["report"])
    report = Path(outputs["report"]).read_text()
    assert "# Divergence Report" in report


# --------------------------------------------------------------------------- #
# capture.py -- PID resolution (M2)
# --------------------------------------------------------------------------- #


def test_resolve_llama_pid_non_windows_uses_spawned_pid(monkeypatch):
    monkeypatch.setattr(capture, "IS_WINDOWS", False)
    session = capture.Session(
        session_dir=Path("/tmp"), session_id="s", config={}
    )
    session.spawned_cmd_pid = 1234
    assert capture.resolve_llama_pid(session) == 1234


# --------------------------------------------------------------------------- #
# capture.py -- console ctrl handler (CTRL_CLOSE on X button)
# --------------------------------------------------------------------------- #


def test_ctrl_handler_handles_close_break_and_ctrl_c(monkeypatch):
    import threading

    # Force the handler installation path even on non-Windows (dev/test).
    monkeypatch.setattr(capture, "IS_WINDOWS", True)

    import ctypes
    from ctypes import wintypes

    captured_handler = {}

    class FakeWINFUNCTYPE:
        def __init__(self, *a, **k):
            pass

        def __call__(self, fn):
            return fn

    def fake_set_console_ctrl_handler(callback, add):
        captured_handler["cb"] = callback
        return True

    fake_kernel32 = type("K", (), {"SetConsoleCtrlHandler": staticmethod(fake_set_console_ctrl_handler)})
    fake_windll = type("W", (), {"kernel32": fake_kernel32()})
    monkeypatch.setattr(ctypes, "windll", fake_windll(), raising=False)
    monkeypatch.setattr(ctypes, "WINFUNCTYPE", FakeWINFUNCTYPE, raising=False)

    session = capture.Session(session_dir=Path("/tmp"), session_id="s", config={})
    session.stop_event = threading.Event()
    capture.install_windows_ctrl_handler(session)

    cb = captured_handler["cb"]
    assert callable(cb)

    # Ctrl+C, Ctrl+Break, and Ctrl+Close (X button) all set the stop event.
    for event_id in (0, 1, 2):
        session.stop_event.clear()
        assert cb(event_id) is True
        assert session.stop_event.is_set()

    # An unrelated event is not handled and does not stop capture.
    session.stop_event.clear()
    assert cb(999) is False
    assert not session.stop_event.is_set()


# --------------------------------------------------------------------------- #
# capture.py -- _persist_anchor (hard-kill anchor durability)
# --------------------------------------------------------------------------- #


def test_persist_anchor_writes_anchor_json(tmp_path):
    session = capture.Session(
        session_dir=tmp_path, session_id="s", config={}
    )
    session.anchors["log_epoch_us"] = 1_234_567
    session.anchors["method"] = "first_log_line"
    capture._persist_anchor(session)
    anchor_path = tmp_path / "anchor.json"
    assert anchor_path.exists()
    written = json.loads(anchor_path.read_text())
    assert written["log_epoch_us"] == 1_234_567
    assert written["method"] == "first_log_line"


def test_persist_anchor_noop_without_anchor(tmp_path):
    session = capture.Session(
        session_dir=tmp_path, session_id="s", config={}
    )
    capture._persist_anchor(session)
    assert not (tmp_path / "anchor.json").exists()


# --------------------------------------------------------------------------- #
# postprocess.py -- anchor recovery when manifest missing
# --------------------------------------------------------------------------- #


def test_load_anchor_recovers_from_console_when_no_manifest(tmp_path):
    # No manifest.json; console.jsonl has stamped records (R_us + wallclock).
    (tmp_path / "console.jsonl").write_text(
        json.dumps(
            {
                "type": "console",
                "line": "0.00.045.713 I cmn x: y",
                "R_us": 45713,
                "wallclock_iso": "2026-08-15T03:41:15.418-05:00",
                "wallclock_epoch_us": 1786783275418843,
            }
        )
        + "\n"
    )
    anchor = postprocess.load_anchor(tmp_path)
    assert anchor.get("log_epoch_us") == 1786783275418843 - 45713
    assert anchor.get("recovered") is True
    assert anchor.get("method") == "recovered_from_console"


def test_load_anchor_prefers_manifest_when_present(tmp_path):
    manifest = {
        "anchor": {
            "method": "first_log_line",
            "log_epoch_us": 1_750_000_000_000_000,
        }
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    (tmp_path / "console.jsonl").write_text(
        json.dumps(
            {
                "R_us": 999,
                "wallclock_epoch_us": 1_750_000_000_999_000,
            }
        )
        + "\n"
    )
    anchor = postprocess.load_anchor(tmp_path)
    # Manifest anchor wins; not marked recovered.
    assert anchor.get("log_epoch_us") == 1_750_000_000_000_000
    assert not anchor.get("recovered")


def test_load_anchor_recovers_from_anchor_json(tmp_path):
    # Early anchor.json written by capture.py at anchor time.
    (tmp_path / "anchor.json").write_text(
        json.dumps({"method": "first_log_line", "log_epoch_us": 1_234_567})
    )
    anchor = postprocess.load_anchor(tmp_path)
    assert anchor.get("log_epoch_us") == 1_234_567


def test_load_anchor_empty_when_nothing_available(tmp_path):
    assert postprocess.load_anchor(tmp_path) == {}


# --------------------------------------------------------------------------- #
# postprocess.py -- anchor self-checks (B2)
# --------------------------------------------------------------------------- #


def test_anchor_self_checks_file_creation_skew_flags(tmp_path):
    anchor = {
        "log_epoch_us": 1_750_000_000_000_000,
        "first_line_wallclock_epoch_us": 1_750_000_000_000_000,
        "first_line_R_us": 0,
        # created 30s later than the anchor -> large skew -> uncertain
        "file_creation_epoch_us": 1_750_000_030_000_000,
    }
    events = []
    findings = []
    uncertain = postprocess._anchor_self_checks(anchor, events, findings)
    assert uncertain is True
    assert any(f["rule"] == "file_creation_skew" for f in findings)


def test_anchor_self_checks_file_creation_ok(tmp_path):
    anchor = {
        "log_epoch_us": 1_750_000_000_000_000,
        "first_line_wallclock_epoch_us": 1_750_000_000_000_000,
        "first_line_R_us": 0,
        "file_creation_epoch_us": 1_750_000_002_000_000,  # 2s -> within tol
    }
    uncertain = postprocess._anchor_self_checks(anchor, [], [])
    assert uncertain is False


def test_anchor_self_checks_prompt_clock_misalignment():
    anchor = {"log_epoch_us": 1_750_000_000_000_000}
    # Prompt filename ms (900,000 ms = 900 s) far outside console R_us window
    # (100 ms window) -> misalignment. Units: prompt is ms, R_us is µs; the
    # comparison must convert to a common unit.
    events = [
        {
            "source": "prompt",
            "payload": {"prompt_file": "000000900000.txt"},
        },
        {
            "source": "console",
            "payload": {"R_us": 100_000},  # 100 ms
        },
    ]
    findings = []
    uncertain = postprocess._anchor_self_checks(anchor, events, findings)
    assert uncertain is True
    assert any(f["rule"] == "prompt_clock_alignment" for f in findings)


def test_anchor_self_checks_prompt_clock_aligned_no_flag():
    # Prompt filename ms (60,000 ms = 60 s) INSIDE the console R_us window
    # (10,000,000..100,000,000 µs = 10..100 s). Must NOT flag a divergence.
    anchor = {"log_epoch_us": 1_750_000_000_000_000}
    events = [
        {
            "source": "prompt",
            "payload": {"prompt_file": "000000060000.txt"},  # 60,000 ms
        },
        {
            "source": "console",
            "payload": {"R_us": 10_000_000},  # 10 s in µs
        },
        {
            "source": "console",
            "payload": {"R_us": 100_000_000},  # 100 s in µs
        },
    ]
    findings = []
    uncertain = postprocess._anchor_self_checks(anchor, events, findings)
    assert uncertain is False
    assert not any(f["rule"] == "prompt_clock_alignment" and f["status"] == "divergence"
                   for f in findings)


def test_anchor_self_checks_prompt_clock_uses_session_dir_fallback(tmp_path):
    # Events carry NO console R_us (typed console events drop it), but
    # console.jsonl on disk has R_us. The fallback must read it via session_dir.
    anchor = {"log_epoch_us": 1_750_000_000_000_000}
    (tmp_path / "console.jsonl").write_text(
        json.dumps({"type": "console", "R_us": 10_000_000}) + "\n" +
        json.dumps({"type": "console", "R_us": 100_000_000}) + "\n"
    )
    events = [
        {
            "source": "prompt",
            "payload": {"prompt_file": "000000060000.txt"},  # 60,000 ms, inside window
        },
        # No console R_us in events payloads.
        {"source": "console", "payload": {}},
    ]
    findings = []
    uncertain = postprocess._anchor_self_checks(anchor, events, findings, tmp_path)
    assert uncertain is False
    # The check should be "ok" (data found via fallback), not "skipped".
    pf = [f for f in findings if f["rule"] == "prompt_clock_alignment"]
    assert pf and pf[0]["status"] == "ok"


def test_anchor_self_checks_activity_window_disjoint():
    anchor = {"log_epoch_us": 1_750_000_000_000_000}
    events = [
        {
            "source": "console",
            "ts": "2026-08-13T09:15:30.000-07:00",
        },
        {
            "source": "slots",
            "payload": {"state": "processing"},
            "ts": "2026-08-13T09:16:30.000-07:00",  # 60s later, disjoint
        },
    ]
    findings = []
    uncertain = postprocess._anchor_self_checks(anchor, events, findings)
    assert uncertain is True
    assert any(f["rule"] == "activity_window" for f in findings)


def test_write_anchor_uncertain_writes_manifest(tmp_path):
    manifest = {"session_id": "s1", "anchor": {"method": "first_log_line"}}
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    postprocess._write_anchor_uncertain(tmp_path, True)
    updated = json.loads((tmp_path / "manifest.json").read_text())
    assert updated["anchor_uncertain"] is True
    assert updated["session_id"] == "s1"  # preserved other fields


# --------------------------------------------------------------------------- #
# postprocess.py -- parse_slots task_id (m3)
# --------------------------------------------------------------------------- #


def test_parse_slots_task_id_uses_id_task(tmp_path):
    slots = [
        {
            "type": "slots",
            "wallclock_iso": "2026-08-13T09:15:31.000-07:00",
            "data": [
                {"id": 4, "task": 999, "id_task": 184, "is_processing": True},
            ],
        }
    ]
    with open(tmp_path / "slots.jsonl", "w") as f:
        for rec in slots:
            f.write(json.dumps(rec) + "\n")
    events = postprocess.parse_slots(tmp_path)
    assert len(events) == 1
    # task_id should come from id_task, not the stale 'task' field.
    assert events[0]["task_id"] == 184
    # Real /slots API has is_processing (bool), mapped to state.
    assert events[0]["payload"]["is_processing"] is True
    assert events[0]["payload"]["state"] == "processing"


def test_parse_slots_maps_is_processing_to_state(tmp_path):
    slots = [
        {
            "type": "slots",
            "wallclock_iso": "2026-08-13T09:15:31.000-07:00",
            "data": [
                {"id": 0, "is_processing": False},
                {"id": 1, "is_processing": True},
            ],
        }
    ]
    with open(tmp_path / "slots.jsonl", "w") as f:
        for rec in slots:
            f.write(json.dumps(rec) + "\n")
    events = postprocess.parse_slots(tmp_path)
    states = [e["payload"].get("state") for e in events]
    assert states == ["idle", "processing"]


# --------------------------------------------------------------------------- #
# Helpers / fixtures
# --------------------------------------------------------------------------- #


def _write_minimal_session(session_dir: Path):
    """Write a tiny but valid raw session for post-processing tests."""
    session_dir.mkdir(exist_ok=True)
    (session_dir / "prompts").mkdir(exist_ok=True)

    manifest = {
        "session_id": session_dir.name,
        "anchor": {"method": "first_log_line", "log_epoch_us": 1_750_000_000_000_000},
    }
    (session_dir / "manifest.json").write_text(json.dumps(manifest))

    # console.jsonl
    console = [
        {
            "type": "console",
            "line": "0.0.0.0.1 srv server: HTTP server listening on http://0.0.0.0:8000",
            "wallclock_iso": "2026-08-13T09:15:30.000-07:00",
        },
        {
            "type": "console",
            "line": "0.0.1.0.0 srv slot id 4 | task 184 | gen: n_decoded = 100, tg = 10.44 t/s, tg_3s = 10.44 t/s",
            "wallclock_iso": "2026-08-13T09:15:31.000-07:00",
        },
    ]
    with open(session_dir / "console.jsonl", "w") as f:
        for rec in console:
            f.write(json.dumps(rec) + "\n")

    # slots.jsonl
    slots = [
        {
            "type": "slots",
            "wallclock_iso": "2026-08-13T09:15:31.000-07:00",
            "data": [
                {
                    "id": 4,
                    "task": 184,
                    "state": "processing",
                    "n_prompt_tokens": 100,
                }
            ],
        }
    ]
    with open(session_dir / "slots.jsonl", "w") as f:
        for rec in slots:
            f.write(json.dumps(rec) + "\n")

    # metrics.jsonl
    metrics = [
        {
            "type": "metrics",
            "wallclock_iso": "2026-08-13T09:15:31.000-07:00",
            "data": (
                "# HELP llamacpp:generation_rate Token generation rate\n"
                "# TYPE llamacpp:generation_rate gauge\n"
                "llamacpp:generation_rate 10.44\n"
            ),
        }
    ]
    with open(session_dir / "metrics.jsonl", "w") as f:
        for rec in metrics:
            f.write(json.dumps(rec) + "\n")


import pytest


@pytest.fixture
def anchor_factory():
    def make(log_epoch_us: int) -> dict:
        return {"method": "first_log_line", "log_epoch_us": log_epoch_us}

    return make
