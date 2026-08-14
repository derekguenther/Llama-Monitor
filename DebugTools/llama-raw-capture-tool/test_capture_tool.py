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
