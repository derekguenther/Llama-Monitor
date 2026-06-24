#!/usr/bin/env python3
"""Test per-slot n_gen_tokens delta graph implementation."""

import ast
import os
import sys


TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "templates",
    "index.html",
)


def test_previous_slot_tokens_state():
    """Verify previousSlotTokens state variable exists."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    assert "previousSlotTokens" in content, "Missing previousSlotTokens state variable"
    print("[PASS] previousSlotTokens state variable present")


def test_crosshair_registered_for_tokens():
    """Verify crosshair plugin is registered for tokensChart."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    # Find the tokensChart initialization
    tokens_idx = content.find("tokensChart = new Chart")
    assert tokens_idx != -1, "tokensChart not found"

    # Check that crosshairPlugin is registered before tokensChart
    before_tokens = content[max(0, tokens_idx - 200):tokens_idx]
    assert "crosshairPlugin" in before_tokens, "crosshairPlugin not registered before tokensChart"
    print("[PASS] crosshairPlugin registered for tokensChart")


def test_interaction_mode_index():
    """Verify tokensChart has interaction mode: index for crosshair."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    tokens_idx = content.find("tokensChart = new Chart")
    assert tokens_idx != -1, "tokensChart not found"

    # Check for interaction mode in tokensChart options
    tokens_section = content[tokens_idx:tokens_idx + 1000]
    assert "mode: 'index'" in tokens_section, "interaction mode: index not found in tokensChart"
    print("[PASS] tokensChart has interaction mode: index")


def test_legend_displayed():
    """Verify tokensChart shows legend for per-slot labels."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    tokens_idx = content.find("tokensChart = new Chart")
    assert tokens_idx != -1, "tokensChart not found"

    tokens_section = content[tokens_idx:tokens_idx + 1000]
    assert "legend: { display: true" in tokens_section, "legend not enabled in tokensChart"
    print("[PASS] tokensChart legend is displayed")


def test_delta_calculation():
    """Verify delta calculation logic exists."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    assert "currentTokens - prevTokens" in content or "currentTokens - previousSlotTokens" in content, \
        "Delta calculation not found"
    assert "n_gen_tokens" in content, "n_gen_tokens not used for delta calculation"
    print("[PASS] Delta calculation with n_gen_tokens present")


def test_per_slot_datasets():
    """Verify per-slot dataset generation."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    assert "Slot ${slotId}" in content or "Slot ${i}" in content, \
        "Per-slot label not found"
    print("[PASS] Per-slot dataset labels present")


def test_no_tokens_per_sec_usage():
    """Verify predicted_tokens_seconds is no longer used for the graph."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    # Check that historyData.tokens is no longer populated from predicted_tokens_seconds
    update_idx = content.find("function updateCharts")
    assert update_idx != -1, "updateCharts function not found"

    # Find the next function after updateCharts
    next_func = content.find("function ", update_idx + 20)
    update_section = content[update_idx:next_func if next_func != -1 else update_idx + 2000]

    assert "predicted_tokens_seconds" not in update_section, \
        "predicted_tokens_seconds still used in updateCharts"
    assert "historyData.tokens" not in update_section, \
        "historyData.tokens still used in updateCharts"
    print("[PASS] predicted_tokens_seconds removed from updateCharts")


def test_slot_colors():
    """Verify per-slot color scheme."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    assert "slotColors" in content, "slotColors array not found"
    print("[PASS] Per-slot color scheme present")


if __name__ == "__main__":
    tests = [
        test_previous_slot_tokens_state,
        test_crosshair_registered_for_tokens,
        test_interaction_mode_index,
        test_legend_displayed,
        test_delta_calculation,
        test_per_slot_datasets,
        test_no_tokens_per_sec_usage,
        test_slot_colors,
    ]

    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed.append(test.__name__)
        except Exception as e:
            print(f"[ERROR] {test.__name__}: {e}")
            failed.append(test.__name__)

    if failed:
        print(f"\n{len(failed)} test(s) failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        print(f"\nAll {len(tests)} tests passed!")
        sys.exit(0)
