#!/usr/bin/env python3
"""Test that dollar sign is on Monthly Cost chart, not Tokens/s chart."""

import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def test_dollar_sign_placement():
    """Verify dollar sign is on Monthly Cost chart, not Tokens/s chart."""
    with open(TEMPLATE_PATH, "r") as f:
        content = f.read()

    errors = []

    # Find the tokens chart config
    tokens_match = re.search(r'tokensChart = new Chart\((.*?)\}\s*\}\s*\}\s*\}\s*\}\s*\)', content, re.DOTALL)
    if tokens_match:
        tokens_config = tokens_match.group(1)
        if "callback: function(value)" in tokens_config and "'$'" in tokens_config:
            errors.append("Tokens/s chart still has dollar sign callback")

    # Find the monthly cost chart config
    monthly_match = re.search(r'monthlyCostChart = new Chart\((.*?)\}\s*\}\s*\}\s*\}\s*\}\s*\)', content, re.DOTALL)
    if monthly_match:
        monthly_config = monthly_match.group(1)
        if "callback: function(value)" not in monthly_config or "'$'" not in monthly_config:
            errors.append("Monthly Cost chart missing dollar sign callback")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] Tokens/s chart has no dollar sign")
    print("[PASS] Monthly Cost chart has dollar sign")
    return True


if __name__ == "__main__":
    success = test_dollar_sign_placement()
    sys.exit(0 if success else 1)
