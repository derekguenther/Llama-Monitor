#!/usr/bin/env python3
"""Test runner for llama-monitor - summarizes results from all test files."""

import subprocess
import sys
import os

TEST_FILES = [
    "test_config.py",
    "test_database.py",
    "test_server_metrics.py",
    "test_system_metrics.py",
    "test_aggregator_integration.py",
    "test_imports.py",
]

LLAMA_MONITOR_DIR = "C:/Users/ClaudeCode/Documents/llama-monitor"


def run_tests():
    """Run all test files and summarize results."""
    results = []
    all_passed = True

    print("=" * 60)
    print("llama-monitor Test Suite")
    print("=" * 60)
    print()

    for test_file in TEST_FILES:
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
        import re
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
