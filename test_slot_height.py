#!/usr/bin/env python3
"""Test that slot chart height calculation provides adequate space."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_slot_height_adequate():
    """Verify the slot height calculation provides adequate space for labels."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Check heightPerSlot is at least 20 (compact but readable)
    height_per_slot_match = re.search(r'const heightPerSlot = (\d+);', content)
    if not height_per_slot_match:
        errors.append("heightPerSlot not found")
    else:
        hps = int(height_per_slot_match.group(1))
        if hps < 20:
            errors.append(f"heightPerSlot is {hps}, should be at least 20")

    # Check baseHeight is at least 30 (compact minimum for single bar + label)
    base_height_match = re.search(r'const baseHeight = (\d+);', content)
    if not base_height_match:
        errors.append("baseHeight not found")
    else:
        bh = int(base_height_match.group(1))
        if bh < 30:
            errors.append(f"baseHeight is {bh}, should be at least 30")

    # Verify no max-height constraint on slot-context-card
    if re.search(r'max-height.*slot-context-card', content):
        errors.append("slot-context-card should not have max-height constraint")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print(f"[PASS] heightPerSlot is {hps} (adequate space per slot)")
    print(f"[PASS] baseHeight is {bh} (adequate minimum)")
    print("[PASS] slot-context-card has no max-height constraint")
    return True


if __name__ == "__main__":
    success = test_slot_height_adequate()
    sys.exit(0 if success else 1)
