#!/usr/bin/env python3
"""Unit tests for Tokens/Sec graph source fix.

The graph previously used delta-computed _instant rates (predicted_tokens_seconds_instant /
prompt_tokens_seconds_instant) which are noisy — 0 most of the time with spikes to 500+.
It now uses llama.cpp's own instantaneous gauges (predicted_tokens_seconds /
prompt_tokens_seconds) gated on requests_processing so the graph shows accurate rates
during activity and decays to 0 when idle.
"""

import os
import re

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def _read_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()


def test_uses_authoritative_gauges_not_instant():
    """The graph should use predicted/prompt_tokens_seconds, not _instant delta rates."""
    content = _read_template()

    # Extract the updateCharts function body
    update_idx = content.find("function updateCharts")
    assert update_idx != -1, "updateCharts function not found"
    next_func = content.find("function ", update_idx + 20)
    update_section = content[update_idx:next_func if next_func != -1 else update_idx + 3000]

    # Delta-computed _instant fields must NOT be used for the graph
    assert "predicted_tokens_seconds_instant" not in update_section, \
        "predicted_tokens_seconds_instant still used in updateCharts"
    assert "prompt_tokens_seconds_instant" not in update_section, \
        "prompt_tokens_seconds_instant still used in updateCharts"

    # Authoritative llama.cpp gauges must be used
    assert "serverMetrics.predicted_tokens_seconds" in update_section, \
        "predicted_tokens_seconds (authoritative gauge) not used in updateCharts"
    assert "serverMetrics.prompt_tokens_seconds" in update_section, \
        "prompt_tokens_seconds (authoritative gauge) not used in updateCharts"

    print("[PASS] No _instant delta rates in updateCharts")
    print("[PASS] Uses authoritative llama.cpp gauges")


def test_gates_on_activity_for_idle_decay():
    """Rates should be gated on requests_processing so idle decays to 0."""
    content = _read_template()
    update_idx = content.find("function updateCharts")
    next_func = content.find("function ", update_idx + 20)
    update_section = content[update_idx:next_func if next_func != -1 else update_idx + 3000]

    # Gating on requests_processing must be present
    assert "requests_processing > 0" in update_section, \
        "Missing requests_processing activity gate in updateCharts"

    # Rates must resolve to 0 when idle (ternary gate)
    assert "? (serverMetrics.predicted_tokens_seconds || 0) : 0" in update_section, \
        "predicted rate not gated to 0 on idle"
    assert "? (serverMetrics.prompt_tokens_seconds || 0) : 0" in update_section, \
        "prompt rate not gated to 0 on idle"

    print("[PASS] Rates gated on requests_processing (idle -> 0)")


def test_still_appends_data_for_smooth_decay():
    """The graph must still always append data so idle decays smoothly to 0."""
    content = _read_template()

    assert "historyData.promptTokens.push(tokensProcessedPerSec)" in content, \
        "Missing promptTokens.push (should always append)"
    assert "historyData.tokens.push(tokensGeneratedPerSec)" in content, \
        "Missing tokens.push (should always append)"

    print("[PASS] Always appends data (decays to 0 on idle)")


if __name__ == "__main__":
    tests = [
        test_uses_authoritative_gauges_not_instant,
        test_gates_on_activity_for_idle_decay,
        test_still_appends_data_for_smooth_decay,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    import sys
    sys.exit(1 if failed else 0)
