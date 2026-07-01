#!/usr/bin/env python3
"""Test script to verify API data integrity.

Fetches /api/metrics and checks that no values are -1 (guard values)
which indicate broken data paths or uninitialized metrics.

Usage:
    python test_api_data_integrity.py [--base-url http://localhost:8080]
"""

import argparse
import json
import sys
import urllib.request


def fetch_metrics(base_url):
    """Fetch metrics from the API."""
    url = f"{base_url}/api/metrics"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"ERROR: Failed to fetch {url}: {e}")
        sys.exit(1)


def find_negative_one_values(data, path=""):
    """Recursively find all -1 values in nested dict."""
    findings = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            findings.extend(find_negative_one_values(value, new_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            findings.extend(find_negative_one_values(item, new_path))
    elif isinstance(data, (int, float)):
        if data == -1:
            findings.append(path)
    
    return findings


def is_expected_sentinel(path):
    """Check if -1 value is an expected sentinel (not a bug)."""
    # server.slots[].task uses -1 for idle slots (expected)
    if ".task" in path:
        return True
    # server.props.default_generation_settings.params uses -1 for unset values (expected)
    if "params." in path and any(x in path for x in ["max_tokens", "n_predict", "dry_penalty_last_n"]):
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Test API data integrity")
    parser.add_argument("--base-url", default="http://localhost:8080", help="Base URL of the server")
    args = parser.parse_args()

    data = fetch_metrics(args.base_url)
    negative_ones = find_negative_one_values(data)

    print("=" * 70)
    print("API Data Integrity Test")
    print("=" * 70)
    print()

    if negative_ones:
        actual_failures = [p for p in negative_ones if not is_expected_sentinel(p)]
        if actual_failures:
            print(f"FAILED: Found {len(actual_failures)} unexpected -1 guard values in API response:")
            for path in actual_failures:
                print(f"  - {path}")
            print()
            print("These -1 values indicate broken data paths or uninitialized metrics.")
            print("The dashboard will display '-1' instead of proper values.")
            if negative_ones != actual_failures:
                print()
                print("Note: Some -1 values are expected sentinels (idle slots, unset params).")
            sys.exit(1)
        else:
            print("PASSED: All -1 values are expected sentinels (idle slots, unset params).")
            sys.exit(0)
    else:
        print("PASSED: No unexpected -1 guard values found in API response.")
        print("All data paths are functioning correctly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
