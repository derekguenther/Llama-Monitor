#!/usr/bin/env python3
"""Test that debug logging is hidden by default and enabled by --verbose.

Verifies the [DEBUG] diagnostics in llamamonitor.py are routed through the
logging module (so they respect the WARNING-by-default / INFO-with-verbose
levels) rather than raw print() calls that bypass gating.
"""

import os
import re
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llamamonitor.py")


def test_debug_gated_by_verbose():
    with open(SRC, "r") as f:
        content = f.read()

    errors = []

    # No raw print debug statements (these bypass the logging level)
    if "print(f\"[DEBUG]" in content:
        errors.append("raw print(f'[DEBUG]...') still present (bypasses --verbose)")

    # Debug diagnostics must be routed through the logging module
    if "logger.info(\"[DEBUG]" not in content:
        errors.append("debug diagnostics not routed through logger.info")

    # Default (non-verbose) level must be WARNING so info-level debug is hidden
    non_verbose_match = re.search(
        r"else:\s*logging\.basicConfig\(\s*level=logging\.WARNING",
        content,
        re.DOTALL,
    )
    if not non_verbose_match:
        errors.append("non-verbose branch missing logging level WARNING")

    # Verbose branch must be at INFO (or below) so debug shows when enabled
    verbose_match = re.search(
        r"if verbose:\s*logging\.basicConfig\(\s*level=logging\.(INFO|DEBUG)",
        content,
        re.DOTALL,
    )
    if not verbose_match:
        errors.append("verbose branch missing logging level INFO/DEBUG")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] No raw print('[DEBUG]...') statements")
    print("[PASS] Debug diagnostics routed through logger.info")
    print("[PASS] Default level is WARNING (debug hidden)")
    print("[PASS] --verbose sets INFO/DEBUG (debug shown)")
    return True


if __name__ == "__main__":
    success = test_debug_gated_by_verbose()
    sys.exit(0 if success else 1)
