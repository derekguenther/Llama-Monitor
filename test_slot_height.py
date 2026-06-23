#!/usr/bin/env python3
"""Test that slot chart height calculation allows multiple slots to be visible."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_slot_height_calculation():
    """Verify the slot height calculation allows multiple slots."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Check heightPerSlot is at least 40
    height_per_slot_match = re.search(r'const heightPerSlot = (\d+);', content)
    if not height_per_slot_match:
        errors.append("heightPerSlot not found")
    else:
        hps = int(height_per_slot_match.group(1))
        if hps < 40:
            errors.append(f"heightPerSlot is {hps}, should be at least 40")

    # Check baseHeight is at least 60
    base_height_match = re.search(r'const baseHeight = (\d+);', content)
    if not base_height_match:
        errors.append("baseHeight not found")
    else:
        bh = int(base_height_match.group(1))
        if bh < 60:
            errors.append(f"baseHeight is {bh}, should be at least 60")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] heightPerSlot is 40 (allows multiple slots)")
    print("[PASS] baseHeight is 60 (adequate minimum)")
    return True


if __name__ == "__main__":
    success = test_slot_height_calculation()
    sys.exit(0 if success else 1)
