#!/usr/bin/env python3
"""Test that crosshair hover line is implemented for CPU/GPU graph."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_crosshair_implementation():
    """Verify crosshair plugin is implemented for the CPU/GPU graph."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Check for crosshair plugin
    if "crosshairPlugin" not in content:
        errors.append("Missing crosshairPlugin")

    # Check for Chart.register
    if "Chart.register(crosshairPlugin)" not in content:
        errors.append("Missing Chart.register(crosshairPlugin)")

    # Check for interaction mode
    if "mode: 'index'" not in content:
        errors.append("Missing interaction mode 'index'")

    # Check for intersect: false
    if "intersect: false" not in content:
        errors.append("Missing intersect: false")

    # Check for vertical line drawing
    if "ctx.moveTo" not in content or "ctx.lineTo" not in content:
        errors.append("Missing vertical line drawing code")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] crosshairPlugin present")
    print("[PASS] Chart.register(crosshairPlugin) present")
    print("[PASS] Interaction mode 'index' configured")
    print("[PASS] Intersect: false configured")
    print("[PASS] Vertical line drawing code present")
    return True


if __name__ == "__main__":
    success = test_crosshair_implementation()
    sys.exit(0 if success else 1)
