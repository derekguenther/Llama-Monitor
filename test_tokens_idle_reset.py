#!/usr/bin/env python3
"""Unit tests for Tokens/Sec graph idle behavior — no reset to [0]."""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_tokens_graph_no_reset_on_idle():
    """Verify Tokens/Sec graph does NOT reset to [0] on idle — appends zeros instead."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Should NOT have old reset-to-[0] logic
    if 'historyData.tokens = [0]' in content:
        errors.append("Still has tokens array reset to [0] — should append zeros instead")

    if 'historyData.promptTokens = [0]' in content:
        errors.append("Still has promptTokens array reset to [0] — should append zeros instead")

    # Should always append data (no conditional that skips on idle)
    if 'historyData.tokens.push(tokensGeneratedPerSec)' not in content:
        errors.append("Missing tokens.push — should always append data")

    # Should trim all arrays to MAX_HISTORY
    if 'historyData.gpu.length > MAX_HISTORY' not in content:
        errors.append("Missing MAX_HISTORY trim for gpu array")

    if 'historyData.tokens.shift()' not in content:
        errors.append("Missing tokens.shift() in trim")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] No tokens reset to [0] on idle")
    print("[PASS] Always appends data (zeros during idle)")
    print("[PASS] All arrays trimmed to MAX_HISTORY")
    return True


if __name__ == "__main__":
    success = test_tokens_graph_no_reset_on_idle()
    sys.exit(0 if success else 1)
