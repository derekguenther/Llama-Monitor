#!/usr/bin/env python3
"""Unit tests for Tokens/Sec graph reset on idle."""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_tokens_graph_resets_on_idle():
    """Verify Tokens/Sec graph resets to [0] when both values are 0."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Check for idle reset logic in updateCharts
    if 'tokensGeneratedPerSec === 0 && tokensProcessedPerSec === 0' not in content:
        errors.append("Missing idle reset check for both token values")

    if 'historyData.tokens = [0]' not in content:
        errors.append("Missing tokens array reset to [0]")

    if 'historyData.promptTokens = [0]' not in content:
        errors.append("Missing promptTokens array reset to [0]")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Idle reset check present")
    print("[PASS] tokens array resets to [0]")
    print("[PASS] promptTokens array resets to [0]")
    return True


if __name__ == "__main__":
    success = test_tokens_graph_resets_on_idle()
    sys.exit(0 if success else 1)
