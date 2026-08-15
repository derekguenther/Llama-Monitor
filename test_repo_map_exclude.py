#!/usr/bin/env python3
"""Test that DebugTools is excluded from REPO_MAP generation.

Verifies the finish-bead REPO_MAP generator excludes the DebugTools/
directory (where the llama-raw-capture-tool lives) so its files are not
listed in docs/REPO_MAP.md.
"""

import os
import re
import sys

FINISH_BEAD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finish-bead")


def test_debugtools_excluded():
    """Verify 'DebugTools' appears in the finish-bead EXCLUDE_DIRS set."""
    with open(FINISH_BEAD_PATH, "r") as f:
        content = f.read()

    errors = []

    match = re.search(r"EXCLUDE_DIRS\s*=\s*\{([^}]*)\}", content)
    if not match:
        errors.append("EXCLUDE_DIRS set not found in finish-bead")
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    exclude_set = set(x.strip().strip("'\"") for x in match.group(1).split(","))

    if "DebugTools" not in exclude_set:
        errors.append("'DebugTools' missing from EXCLUDE_DIRS")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return False

    print("[PASS] 'DebugTools' present in finish-bead EXCLUDE_DIRS")
    return True


if __name__ == "__main__":
    success = test_debugtools_excluded()
    sys.exit(0 if success else 1)
