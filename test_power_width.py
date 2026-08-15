#!/usr/bin/env python3
"""Test that power card items keep the W unit on the same line.

Verifies .power-value uses white-space: nowrap and .power-item has a
minimum width so values in the hundreds don't wrap the 'W' to a new line.
"""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_power_item_width():
    """Verify power-value is nowrap and power-item has a min-width."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    power_item_match = re.search(r'\.power-item\s*\{([^}]+)\}', content, re.DOTALL)
    if not power_item_match:
        errors.append(".power-item CSS block not found")
    else:
        power_item_css = power_item_match.group(1)
        if "width: 100%" not in power_item_css:
            errors.append("Missing width: 100% on .power-item")
        if "min-width" not in power_item_css:
            errors.append("Missing min-width on .power-item")

    power_value_match = re.search(r'\.power-value\s*\{([^}]+)\}', content, re.DOTALL)
    if not power_value_match:
        errors.append(".power-value CSS block not found")
    elif "white-space: nowrap" not in power_value_match.group(1):
        errors.append("Missing white-space: nowrap on .power-value")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] .power-item has width: 100%")
    print("[PASS] .power-item has a min-width")
    print("[PASS] .power-value has white-space: nowrap")
    return True


if __name__ == "__main__":
    success = test_power_item_width()
    sys.exit(0 if success else 1)
