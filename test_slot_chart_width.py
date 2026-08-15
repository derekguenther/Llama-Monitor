#!/usr/bin/env python3
"""Test that Slot Progress & Context graphs fill the allotted card width.

Verifies .slot-context-card stretches children full-width and the slot
charts no longer use excessive left padding.
"""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_slot_chart_width():
    """Verify slot graphs stretch full width and left padding is reduced."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # .slot-context-card should stretch children
    card_match = re.search(r'\.slot-context-card\s*\{([^}]+)\}', content, re.DOTALL)
    if not card_match:
        errors.append(".slot-context-card CSS block not found")
    elif "align-items: stretch" not in card_match.group(1):
        errors.append(".slot-context-card does not use align-items: stretch")

    # .slot-graph should be full width
    graph_match = re.search(r'\.slot-graph\s*\{([^}]+)\}', content, re.DOTALL)
    if not graph_match:
        errors.append(".slot-graph CSS block not found")
    elif "width: 100%" not in graph_match.group(1):
        errors.append(".slot-graph missing width: 100%")

    # Left padding in the two slot charts should be reduced (not 50)
    if "left: 50" in content:
        errors.append("Slot charts still use excessive left: 50 padding")
    if "left: 10" not in content:
        errors.append("Slot charts missing reduced left: 10 padding")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] .slot-context-card uses align-items: stretch")
    print("[PASS] .slot-graph has width: 100%")
    print("[PASS] Slot chart left padding reduced")
    return True


if __name__ == "__main__":
    success = test_slot_chart_width()
    sys.exit(0 if success else 1)
