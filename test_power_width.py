#!/usr/bin/env python3
"""Test that power card items have consistent width settings."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_power_item_width():
    """Verify power-item has width constraints for consistent sizing."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Check for width: 100%
    power_item_match = re.search(r'\.power-item\s*\{([^}]+)\}', content, re.DOTALL)
    if not power_item_match:
        errors.append(".power-item CSS block not found")
    else:
        power_item_css = power_item_match.group(1)
        if "width: 100%" not in power_item_css:
            errors.append("Missing width: 100% on .power-item")
        if "min-width: 0" not in power_item_css:
            errors.append("Missing min-width: 0 on .power-item")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] .power-item has width: 100%")
    print("[PASS] .power-item has min-width: 0")
    return True


if __name__ == "__main__":
    success = test_power_item_width()
    sys.exit(0 if success else 1)
