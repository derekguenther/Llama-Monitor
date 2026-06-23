#!/usr/bin/env python3
"""Test that grid items have min-width:0 and overflow prevention."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_overflow_prevention():
    """Verify grid items have min-width:0 and overflow prevention."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Check for min-width: 0 on grid items
    if "min-width: 0" not in content:
        errors.append("Missing min-width: 0 on grid items")

    # Check for overflow-x: hidden on html
    if "overflow-x: hidden" not in content:
        errors.append("Missing overflow-x: hidden on html")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Grid items have min-width: 0")
    print("[PASS] HTML has overflow-x: hidden")
    return True


if __name__ == "__main__":
    success = test_overflow_prevention()
    sys.exit(0 if success else 1)
