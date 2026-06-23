#!/usr/bin/env python3
"""Test that redundant graph subtitles have been removed."""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_no_redundant_subtitles():
    """Verify redundant graph subtitles are removed."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # These specific subtitles should not exist
    if '<div class="graph-label">CPU % & GPU %</div>' in content:
        errors.append("Found redundant 'CPU % & GPU %' subtitle — should be removed")

    if '<div class="graph-label">Tokens/Sec</div>' in content:
        errors.append("Found redundant 'Tokens/Sec' subtitle — should be removed")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Redundant 'CPU % & GPU %' subtitle removed")
    print("[PASS] Redundant 'Tokens/Sec' subtitle removed")
    return True


if __name__ == "__main__":
    success = test_no_redundant_subtitles()
    sys.exit(0 if success else 1)
