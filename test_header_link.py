#!/usr/bin/env python3
"""Test that the header does not contain a clickable server link."""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_no_server_link():
    """Verify the server URL is not rendered as a clickable link in the header."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # The header should NOT contain an anchor tag for the server URL
    if '<a href="{{ server_url }}"' in content:
        errors.append("Found <a> link for server_url in header — should be plain text")

    # The server URL should still be displayed as text
    if "{{ server_url }}" not in content:
        errors.append("server_url placeholder removed entirely — should still display as text")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Server URL is not a clickable link")
    print("[PASS] Server URL still displayed as text")
    return True


if __name__ == "__main__":
    success = test_no_server_link()
    sys.exit(0 if success else 1)
