#!/usr/bin/env python3
"""Test that grid items have min-width:0 and overflow prevention."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_overflow_prevention():
    """Verify grid items have min-width:0 and overflow prevention."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Check for min-width: 0 on grid items
    if "min-width: 0" not in content:
        errors.append("Missing min-width: 0 on grid items")

    # Check for overflow-x: hidden on html
    if "overflow-x: hidden" not in content:
        errors.append("Missing overflow-x: hidden on html")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Grid items have min-width: 0")
    print("[PASS] HTML has overflow-x: hidden")
    return True


def test_power_card_has_room_for_items():
    """Verify the Power card column is wide enough to hold 3 grid items.

    Bug (bead oqwo): .usage-power-row used a fixed 300px Power column while
    .power-grid was repeat(3, 1fr) with .power-item min-width 120px ->
    3*120 + 2*10 gaps = 380px, exceeding the 300px column and overflowing the
    card's right border. The fix expands the Power column to at least 400px
    (shrinking the Usage graph a little) and shrinks each item to 112px so the
    items stay inside the card.
    """
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Power column must be at least 400px (minmax(400px, auto)) to hold 3 items
    row_match = re.search(r'\.usage-power-row\s*\{([^}]+)\}', content, re.DOTALL)
    if not row_match:
        errors.append(".usage-power-row CSS block not found")
    else:
        row_css = row_match.group(1)
        if "minmax(400px, auto)" not in row_css:
            errors.append("Power column not expanded to minmax(400px, auto)")
        if "minmax(0, 1fr)" not in row_css:
            errors.append("Usage column not shrinkable (minmax(0, 1fr))")

    # Power items shrunk to 112px so 3 items + gaps fit within the card
    item_match = re.search(r'\.power-item\s*\{([^}]+)\}', content, re.DOTALL)
    if not item_match:
        errors.append(".power-item CSS block not found")
    elif "min-width: 112px" not in item_match.group(1):
        errors.append("power-item not shrunk to min-width: 112px")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Power column expands to hold 3 items")
    print("[PASS] Power items shrunk to 112px")
    return True


if __name__ == "__main__":
    ok1 = test_overflow_prevention()
    ok2 = test_power_card_has_room_for_items()
    sys.exit(0 if (ok1 and ok2) else 1)
