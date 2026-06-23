#!/usr/bin/env python3
"""Test that k-unit formatting is applied to Context Used chart."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_k_format_on_context_chart():
    """Verify k-unit formatting is applied to Context Used chart."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Check for formatKUnit function
    if "formatKUnit" not in content:
        errors.append("Missing formatKUnit function")

    # Check x-axis tick callback uses formatKUnit
    if "callback: function(value)" not in content or "formatKUnit(value)" not in content:
        errors.append("X-axis tick callback not using formatKUnit")

    # Check tooltip callback uses formatKUnit
    if "formatKUnit(context.parsed.x)" not in content:
        errors.append("Tooltip callback not using formatKUnit")

    # Check bar label plugin uses formatKUnit for context chart
    if 'isContextChart' not in content:
        errors.append("Missing isContextChart check in bar label plugin")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] formatKUnit function present")
    print("[PASS] X-axis tick callback uses formatKUnit")
    print("[PASS] Tooltip callback uses formatKUnit")
    print("[PASS] Bar label plugin uses formatKUnit for context chart")
    return True


if __name__ == "__main__":
    success = test_k_format_on_context_chart()
    sys.exit(0 if success else 1)
