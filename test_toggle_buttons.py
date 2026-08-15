#!/usr/bin/env python3
"""Test that the Toggle Cost button is removed and Toggle Temps is hidden."""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_toggle_buttons():
    """Verify toggle-cost-btn is removed and toggle-temps-btn is hidden."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    if 'id="toggle-cost-btn"' in content:
        errors.append("toggle-cost-btn element still present")
    if "toggle-cost-btn" in content:
        errors.append("toggle-cost-btn reference still present")
    if "costDisplayEnabled" in content:
        errors.append("costDisplayEnabled variable still present")

    # Toggle Temps should be hidden (kept in markup)
    if 'id="toggle-temps-btn"' not in content:
        errors.append("toggle-temps-btn element missing (should be kept, hidden)")
    if 'id="toggle-temps-btn" hidden' not in content and 'id="toggle-temps-btn" style="display:none"' not in content:
        errors.append("toggle-temps-btn not hidden")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] toggle-cost-btn removed")
    print("[PASS] toggle-temps-btn kept but hidden")
    return True


if __name__ == "__main__":
    success = test_toggle_buttons()
    sys.exit(0 if success else 1)
