#!/usr/bin/env python3
"""Main entry point for llama-monitor.

Supports TUI dashboard, web dashboard, and CLI stats modes.
"""

import argparse
import os
import sys
import time

from config import load_config, find_config
from database import Database
from aggregator import DataAggregator


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="llama-monitor - Real-time monitoring for llama.cpp servers"
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="Path to config file (default: config.yaml)",
    )

    parser.add_argument(
        "--server",
        type=str,
        help="Override server URL",
    )

    parser.add_argument(
        "--rate",
        type=float,
        help="Override electricity cost rate ($/kWh)",
    )

    parser.add_argument(
        "--tui",
        action="store_true",
        help="Run TUI dashboard (default)",
    )

    parser.add_argument(
        "--web",
        action="store_true",
        help="Run web dashboard",
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show one-time stats and exit",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit",
    )

    return parser.parse_args()


def get_config(args):
    """Load configuration from file and apply CLI overrides."""
    # Find config file
    config_path = args.config or find_config()

    # Load config
    config = load_config(config_path)

    # Apply CLI overrides
    if args.server:
        config.set("server.url", args.server)

    if args.rate is not None:
        config.set("display.cost_rate", args.rate)

    return config


def run_tui(config: dict):
    """Run the TUI dashboard."""
    from tui import TUIDashboard

    db = Database(config.database_path)
    with db:
        aggregator = DataAggregator(
            database=db,
            server_url=config.server_url,
            tracked_processes=config.tracked_processes,
            cost_rate=config.cost_rate,
        )

        dashboard = TUIDashboard(aggregator, config)
        dashboard.run()


def run_web(config: dict):
    """Run the web dashboard."""
    from web_server import WebDashboard

    db = Database(config.database_path)
    with db:
        aggregator = DataAggregator(
            database=db,
            server_url=config.server_url,
            tracked_processes=config.tracked_processes,
            cost_rate=config.cost_rate,
        )

        dashboard = WebDashboard(aggregator, config)
        dashboard.run()


def run_stats(config: dict):
    """Show one-time stats and exit."""
    db = Database(config.database_path)
    with db:
        aggregator = DataAggregator(
            database=db,
            server_url=config.server_url,
            tracked_processes=config.tracked_processes,
            cost_rate=config.cost_rate,
        )

        from aggregator import format_metrics_display
        print(format_metrics_display(aggregator))


def main():
    """Main entry point."""
    args = parse_args()

    # Show version
    if args.version:
        print("llama-monitor v1.0.0")
        return 0

    # Load configuration
    config = get_config(args)

    # Run appropriate mode
    if args.stats:
        run_stats(config)
    elif args.web:
        run_web(config)
    else:
        # Default to TUI
        run_tui(config)

    return 0


if __name__ == "__main__":
    sys.exit(main())
