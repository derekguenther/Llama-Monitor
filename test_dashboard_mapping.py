#!/usr/bin/env python3
"""Test script to verify dashboard data mapping.

Fetches /api/metrics and checks that each expected DOM element
has a corresponding data source. Reports mismatches and missing values.

Usage:
    python test_dashboard_mapping.py [--base-url http://localhost:8080]
"""

import argparse
import json
import sys
import urllib.request

# Mapping of DOM element IDs to their expected data paths
# Format: dom_id: [(api_path, transform_func), ...]
# Multiple paths are tried in order; first valid value wins
DOM_MAP = {
    # Server metrics
    "prompt-tokens": [("server.prompt_tokens_total", None)],
    "generated-tokens": [("server.tokens_predicted_total", None)],
    "processing-requests": [("server.requests_processing", None)],
    "deferred-requests": [("server.requests_deferred", None)],
    "active-slots": [("server.slots", "count_active")],
    # CPU
    "cpu-percent": [("system.cpu.percent", None), ("system.cpu_percent", None)],
    "cpu-bar": [("system.cpu.percent", "width")],
    # GPU
    "gpu-percent": [("system.gpu.usage", None), ("system.gpu_usage", None)],
    "gpu-bar": [("system.gpu.usage", "width")],
    # Memory
    "mem-percent": [("system.memory.percent", None), ("system.memory_percent", None)],
    "mem-bar": [("system.memory.percent", "width")],
    # GPU Memory
    "gpu-mem": [("system.gpu.memory_used", "mem_text"), ("system.memory_used", "mem_text")],
    "gpu-mem-bar": [("system.gpu.memory_total", "mem_bar"), ("system.memory_total", "mem_bar")],
    # Power
    "gpu-power-1": [("system.gpu.power_w", None), ("system.gpu_power_w", None)],
    "cpu-power-1": [("system.cpu.power_w", None), ("system.cpu_power_w", None)],
    "sys-power-1": [("system.gpu.power_w", "sum"), ("system.cpu.power_w", "sum")],
    "gpu-power-2": [("system.gpu.power_w", None), ("system.gpu_power_w", None)],
    "cpu-power-2": [("system.cpu.power_w", None), ("system.cpu_power_w", None)],
    "sys-power-2": [("system.system_power_w", None)],
    # Cost
    "session-cost": [("cost.session_cost_usd", None), ("cost.total_cost", None)],
    "today-cost": [("cost.today_cost", None)],
    "total-energy": [("cost.today_wh", None), ("cost.total_wh", None)],
    "today-energy": [("cost.today_wh", None)],
    "monthly-total-cost": [("cost.total_cost", None)],
}


def get_nested_value(data, path):
    """Get a value from nested dict using dot-notation path."""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


def transform_value(value, transform, data=None):
    """Apply a transform to a value."""
    if value is None:
        return None
    if transform == "width":
        return f"{value}%"
    if transform == "mem_text" and data:
        used = get_nested_value(data, "system.gpu.memory_used") or get_nested_value(data, "system.memory_used")
        total = get_nested_value(data, "system.gpu.memory_total") or get_nested_value(data, "system.memory_total")
        if used is not None and total is not None:
            return f"{used}/{total} MB"
        return None
    if transform == "mem_bar" and data:
        total = get_nested_value(data, "system.gpu.memory_total") or get_nested_value(data, "system.memory_total")
        used = get_nested_value(data, "system.gpu.memory_used") or get_nested_value(data, "system.memory_used")
        if total and total > 0:
            return f"{(used / total) * 100}%"
        return "0%"
    if transform == "count_active" and data:
        slots = get_nested_value(data, "server.slots") or []
        if isinstance(slots, list):
            active = sum(1 for s in slots if isinstance(s, dict) and s.get("state") == "processing")
            return f"{active}/{len(slots)}"
        return None
    if transform == "sum":
        # Sum all numeric values found in the data for power
        gpu = get_nested_value(data, "system.gpu.power_w") or get_nested_value(data, "system.gpu_power_w") or 0
        cpu = get_nested_value(data, "system.cpu.power_w") or get_nested_value(data, "system.cpu_power_w") or 0
        return gpu + cpu
    return value


def fetch_metrics(base_url):
    """Fetch metrics from the API."""
    url = f"{base_url}/api/metrics"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"ERROR: Failed to fetch {url}: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Test dashboard data mapping")
    parser.add_argument("--base-url", default="http://localhost:8080", help="Base URL of the server")
    args = parser.parse_args()

    data = fetch_metrics(args.base_url)
    errors = []
    warnings = []
    ok_count = 0

    print("=" * 70)
    print("Dashboard Data Mapping Test")
    print("=" * 70)
    print()

    for dom_id, paths in DOM_MAP.items():
        found = False
        for path, transform in paths:
            value = get_nested_value(data, path)
            if value is not None:
                result = transform_value(value, transform, data)
                if result is not None:
                    # Check if value is a meaningful number (not 0 for power)
                    if isinstance(result, (int, float)) and dom_id.startswith("gpu-power") or dom_id.startswith("cpu-power") or dom_id.startswith("sys-power"):
                        if result == 0:
                            warnings.append(f"  {dom_id}: {path} = {result} (0 may mean no data)")
                        else:
                            ok_count += 1
                            print(f"  OK     {dom_id}: {path} = {result}")
                    else:
                        ok_count += 1
                        print(f"  OK     {dom_id}: {path} = {result}")
                    found = True
                    break

        if not found:
            errors.append(dom_id)
            print(f"  MISSING {dom_id}: no valid data path found")

    print()
    print("=" * 70)
    print(f"Results: {ok_count} OK, {len(warnings)} warnings, {len(errors)} missing")
    print("=" * 70)

    if warnings:
        print()
        print("Warnings:")
        for w in warnings:
            print(w)

    if errors:
        print()
        print(f"ERRORS: {len(errors)} elements have no data:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    elif warnings:
        print("\nNote: Some values are 0 (may indicate no data available)")
        sys.exit(0)
    else:
        print("\nAll elements have valid data!")
        sys.exit(0)


if __name__ == "__main__":
    main()
