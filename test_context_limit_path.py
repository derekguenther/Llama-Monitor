#!/usr/bin/env python3
"""Test that the Context Used chart reads props from the correct data path."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_context_limit_data_path():
    """Verify the context limit is read from data.props, not data.server.props."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Should read from data.props (top-level)
    if "data.props" not in content:
        errors.append("Context limit not reading from data.props")

    # Should NOT read from data.server?.props (wrong path)
    if "data.server?.props" in content:
        errors.append("Context limit still reading from wrong path data.server?.props")

    # Should still have the fallback default
    if "4096" not in content:
        errors.append("Missing 4096 fallback default")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Context limit reads from data.props (correct path)")
    print("[PASS] No longer reads from data.server?.props (wrong path)")
    print("[PASS] 4096 fallback default intact")
    return True


if __name__ == "__main__":
    success = test_context_limit_data_path()
    sys.exit(0 if success else 1)
