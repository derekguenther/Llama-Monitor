#!/usr/bin/env python3
"""Test that the dashboard template uses correct card naming."""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_daily_cost_naming():
    """Verify Daily Cost card is present and Monthly Cost is not."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # The visible card title should be "Daily Cost"
    if "<h2>Daily Cost</h2>" not in content:
        errors.append("Missing <h2>Daily Cost</h2> card title")

    # The old "Monthly Cost" card title should not exist
    if "<h2>Monthly Cost</h2>" in content:
        errors.append("Found old <h2>Monthly Cost</h2> card title — should be Daily Cost")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Daily Cost card title present")
    print("[PASS] Monthly Cost card title removed")
    return True


if __name__ == "__main__":
    success = test_daily_cost_naming()
    sys.exit(0 if success else 1)
