#!/usr/bin/env python3
"""Test that bar labels and k-unit formatting are present."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_bar_labels_and_k_unit():
    """Verify bar labels plugin and k-unit formatting are present."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Check for formatKUnit function
    if "formatKUnit" not in content:
        errors.append("Missing formatKUnit function")

    # Check for k-unit formatting logic
    if "1024" not in content or "'k'" not in content:
        errors.append("Missing k-unit formatting logic")

    # Check for barLabelPlugin
    if "barLabelPlugin" not in content:
        errors.append("Missing barLabelPlugin")

    # Check for Chart.register
    if "Chart.register(barLabelPlugin)" not in content:
        errors.append("Missing Chart.register(barLabelPlugin)")

    # Check for label rendering inside/outside bar logic
    if "textWidth" not in content:
        errors.append("Missing text width calculation for inside/outside bar logic")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] formatKUnit function present")
    print("[PASS] k-unit formatting logic present")
    print("[PASS] barLabelPlugin present")
    print("[PASS] Chart.register(barLabelPlugin) present")
    print("[PASS] Inside/outside bar label logic present")
    return True


if __name__ == "__main__":
    success = test_bar_labels_and_k_unit()
    sys.exit(0 if success else 1)
