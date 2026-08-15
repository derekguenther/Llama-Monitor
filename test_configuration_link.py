#!/usr/bin/env python3
"""Test that a Configuration button links to the settings page."""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_configuration_link():
    """Verify a link to /settings exists in the dashboard controls."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    if 'href="/settings"' not in content:
        print("[FAIL] No link to /settings found")
        return False
    if "Configuration" not in content:
        print("[FAIL] Configuration button label missing")
        return False

    print("[PASS] Configuration link to /settings present")
    return True


if __name__ == "__main__":
    success = test_configuration_link()
    sys.exit(0 if success else 1)
