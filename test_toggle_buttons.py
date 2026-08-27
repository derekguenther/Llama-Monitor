#!/usr/bin/env python3
"""Test that the Toggle Cost and Toggle Temps buttons are removed."""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_toggle_buttons():
    """Verify toggle-cost-btn and toggle-temps-btn are both removed."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    if 'id="toggle-cost-btn"' in content:
        errors.append("toggle-cost-btn element still present")
    if "toggle-cost-btn" in content:
        errors.append("toggle-cost-btn reference still present")
    if "costDisplayEnabled" in content:
        errors.append("costDisplayEnabled variable still present")

    # Toggle Temps button should be removed (dead UI removed)
    if 'id="toggle-temps-btn"' in content:
        errors.append("toggle-temps-btn element still present")
    if "toggle-temps-btn" in content:
        errors.append("toggle-temps-btn reference still present")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] toggle-cost-btn removed")
    print("[PASS] toggle-temps-btn removed")
    return True


if __name__ == "__main__":
    success = test_toggle_buttons()
    sys.exit(0 if success else 1)
