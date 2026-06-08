#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all module imports."""
    errors = []

    # Test config
    try:
        from config import load_config, find_config
        print("[PASS] config.load_config, config.find_config")
    except ImportError as e:
        errors.append(f"config: {e}")
        print(f"[FAIL] config: {e}")

    # Test db
    try:
        from db import Database
        print("[PASS] db.Database")
    except ImportError as e:
        errors.append(f"db: {e}")
        print(f"[FAIL] db: {e}")

    # Test server_metrics
    try:
        from server_metrics import ServerMetricsCollector
        print("[PASS] server_metrics.ServerMetricsCollector")
    except ImportError as e:
        errors.append(f"server_metrics: {e}")
        print(f"[FAIL] server_metrics: {e}")

    # Test system_metrics
    try:
        from system_metrics import SystemMetricsCollector
        print("[PASS] system_metrics.SystemMetricsCollector")
    except ImportError as e:
        errors.append(f"system_metrics: {e}")
        print(f"[FAIL] system_metrics: {e}")

    # Test electricity_cost
    try:
        from electricity_cost import ElectricityCostCalculator
        print("[PASS] electricity_cost.ElectricityCostCalculator")
    except ImportError as e:
        errors.append(f"electricity_cost: {e}")
        print(f"[FAIL] electricity_cost: {e}")

    # Test aggregator
    try:
        from aggregator import Aggregator
        print("[PASS] aggregator.Aggregator")
    except ImportError as e:
        errors.append(f"aggregator: {e}")
        print(f"[FAIL] aggregator: {e}")

    # Test tui
    try:
        from tui import TUI
        print("[PASS] tui.TUI")
    except ImportError as e:
        errors.append(f"tui: {e}")
        print(f"[FAIL] tui: {e}")

    # Test web_server
    try:
        from web_server import run_server
        print("[PASS] web_server.run_server")
    except ImportError as e:
        errors.append(f"web_server.run_server: {e}")
        print(f"[FAIL] web_server.run_server: {e}")

    # Test web_server start_server (what main.py needs)
    try:
        from web_server import start_server
        print("[PASS] web_server.start_server")
    except ImportError as e:
        errors.append(f"web_server.start_server: {e}")
        print(f"[FAIL] web_server.start_server: {e}")

    # Test web_server stop_server (what main.py needs)
    try:
        from web_server import stop_server
        print("[PASS] web_server.stop_server")
    except ImportError as e:
        errors.append(f"web_server.stop_server: {e}")
        print(f"[FAIL] web_server.stop_server: {e}")

    # Test main
    try:
        from main import main, ensure_dependencies, Monitor
        print("[PASS] main.main, main.ensure_dependencies, main.Monitor")
    except ImportError as e:
        errors.append(f"main: {e}")
        print(f"[FAIL] main: {e}")

    print("\n" + "=" * 50)
    if errors:
        print(f"FAILED: {len(errors)} import error(s)")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("SUCCESS: All imports work correctly!")
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
