#!/usr/bin/env python3
"""Tests for test_llama-monitor.py auto-discovery of test files.

IMPORTANT: discovery must NOT run at import time. The runner's discovery
function itself invokes `pytest --collect-only` on every test_*.py file
(including this one), so running discovery at module import would recurse.
We therefore load the runner source and call discovery lazily inside each
test instead.
"""

import importlib.util
import os
import pytest

_RUNNER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "test_llama-monitor.py")
_spec = importlib.util.spec_from_file_location("test_llama_monitor_runner",
                                               _RUNNER_PATH)
runner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runner)


@pytest.fixture(scope="module")
def discovered():
    """Discover test files once per module (lazily, not at import)."""
    return runner.discover_test_files()


def test_discovers_known_unit_test_files(discovered):
    """The runner must discover genuine pytest unit test files."""
    for name in [
        "test_top_bar_slots.py",
        "test_config.py",
        "test_database.py",
        "test_energy_deltas.py",
        "test_hybrid_cost_model.py",
    ]:
        assert name in discovered, f"expected {name} to be discovered"


def test_excludes_itself(discovered):
    """The runner must not include itself in the discovered list."""
    assert "test_llama-monitor.py" not in discovered


def test_excludes_script_style_integration_tests(discovered):
    """Script-style live-integration tests (need a running server) are skipped."""
    for name in [
        "test_aggregator.py",
        "test_api_data_integrity.py",
        "test_dashboard_mapping.py",
    ]:
        assert name not in discovered, (
            f"{name} is script-style and should not be in the pre-merge gate"
        )


def test_all_discovered_files_exist(discovered):
    """Every discovered file must actually exist on disk."""
    base = runner.LLAMA_MONITOR_DIR
    for name in discovered:
        assert os.path.exists(os.path.join(base, name)), f"{name} missing"


def test_discovery_is_sorted_and_nonempty(discovered):
    """Discovery returns a sorted, non-empty list."""
    assert len(discovered) > 0
    assert discovered == sorted(discovered)
