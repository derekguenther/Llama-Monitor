#!/usr/bin/env python3
"""Test runner for llama-monitor - summarizes results from all test files."""

import glob
import re
import subprocess
import sys
import os

# Directory containing this test runner. Using the file location (rather than
# a hardcoded path) makes the runner cross-platform — it works both in the
# Linux docker sandbox and on Windows.
LLAMA_MONITOR_DIR = os.path.dirname(os.path.abspath(__file__))


def discover_test_files():
    """Auto-discover pytest-collectable test_*.py files alongside the runner.

    Every test_*.py file is a candidate, excluding this runner itself. Files
    that pytest cannot collect (script-style live-integration tests that need a
    running server, e.g. test_aggregator.py) are skipped, so the pre-merge
    verification gate only runs genuine unit tests. New unit test files are
    picked up automatically — no hardcoded list to keep in sync.
    """
    candidates = sorted(
        os.path.basename(f)
        for f in glob.glob(os.path.join(LLAMA_MONITOR_DIR, "test_*.py"))
        if os.path.basename(f) != "test_llama-monitor.py"
    )
    collected = []
    for name in candidates:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", name, "--collect-only", "-q"],
            cwd=LLAMA_MONITOR_DIR,
            capture_output=True,
            text=True,
        )
        output = result.stdout + result.stderr
        match = re.search(r"(\d+) tests? collected", output)
        count = int(match.group(1)) if match else 0
        if count > 0:
            collected.append(name)
    return sorted(collected)


def run_tests():
    """Run all test files and summarize results."""
    test_files = discover_test_files()
    results = []
    all_passed = True

    print("=" * 60)
    print("llama-monitor Test Suite")
    print("=" * 60)
    print()

    for test_file in test_files:
        print(f"Running {test_file}...", end=" ")
        sys.stdout.flush()

        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v"],
            cwd=LLAMA_MONITOR_DIR,
            capture_output=True,
            text=True,
        )

        # Parse output for test count and failures
        output = result.stdout + result.stderr
        passed = result.returncode == 0

        # Extract test count from output
        collected = re.search(r"collected (\d+) item", output)
        tests_run = re.search(r"(\d+) passed", output)

        item_count = collected.group(1) if collected else "?"
        run_count = tests_run.group(1) if tests_run else "0"

        results.append({
            "file": test_file,
            "passed": passed,
            "items": item_count,
            "run": run_count,
            "returncode": result.returncode,
        })

        if passed:
            print(f"PASSED ({run_count}/{item_count} tests)")
        else:
            print(f"FAILED (exit code: {result.returncode})")
            all_passed = False

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)

    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)

    print(f"Files passed: {passed_count}/{total_count}")

    if all_passed:
        print()
        print("ALL TESTS PASSED!")
        return 0
    else:
        print()
        print("Some tests failed:")
        for r in results:
            if not r["passed"]:
                print(f"  - {r['file']}")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
