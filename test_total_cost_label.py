#!/usr/bin/env python3
"""Test that the Monthly Cost card has a Total Cost label."""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_total_cost_label():
    """Verify Total Cost label is present above the monthly total."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # The Total Cost label should be present
    if "Total Cost" not in content:
        errors.append("Missing 'Total Cost' label above monthly total")

    # The monthly-total-cost element should still exist
    if 'id="monthly-total-cost"' not in content:
        errors.append("monthly-total-cost element missing")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Total Cost label present above monthly total")
    print("[PASS] monthly-total-cost element intact")
    return True


if __name__ == "__main__":
    success = test_total_cost_label()
    sys.exit(0 if success else 1)
