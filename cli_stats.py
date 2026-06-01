#!/usr/bin/env python3
"""CLI stats command for llama-monitor.

Provides on-demand stats output similar to `kubectl top`.
"""

import argparse
import sys
from datetime import datetime

from config import load_config, find_config
from database import Database
from aggregator import DataAggregator, format_metrics_display


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="llama-monitor stats - Display current monitoring statistics"
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
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output",
    )

    return parser.parse_args()


def get_config(args):
    """Load configuration from file and apply CLI overrides."""
    config_path = args.config or find_config()
    config = load_config(config_path)

    if args.server:
        config.set("server.url", args.server)

    if args.rate is not None:
        config.set("display.cost_rate", args.rate)

    return config


def format_stats(aggregator, verbose: bool = False) -> str:
    """Format stats for display.

    Args:
        aggregator: DataAggregator instance
        verbose: Show detailed output

    Returns:
        Formatted string
    """
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append(f"llama-monitor stats ({timestamp})")
    lines.append("=" * 40)

    # Server stats
    server_metrics = aggregator.get_recent_server_metrics(limit=1)
    lines.append("")
    lines.append("Server:")
    if server_metrics:
        m = server_metrics[0]
        prompt_tokens = m.get("prompt_tokens_total", 0)
        prompt_rate = m.get("prompt_tokens_seconds", 0)
        generated = m.get("tokens_predicted_total", 0)
        gen_rate = m.get("predicted_tokens_seconds", 0)
        processing = m.get("requests_processing", 0)
        deferred = m.get("requests_deferred", 0)

        lines.append(f"  Prompt tokens:    {prompt_tokens:,} ({prompt_rate:,.0f}/s)")
        lines.append(f"  Generated:        {generated:,} ({gen_rate:,.0f}/s)")
        lines.append(f"  Processing:       {processing}")
        lines.append(f"  Deferred:         {deferred}")
    else:
        lines.append("  No server metrics available")

    # System stats
    system_metrics = aggregator.get_recent_system_metrics(limit=1)
    lines.append("")
    lines.append("System:")
    if system_metrics:
        m = system_metrics[0]
        cpu = m.get("cpu_percent", 0)
        gpu = m.get("gpu_usage", 0)
        mem = m.get("memory_percent", 0)
        gpu_mem = m.get("gpu_memory_used", 0)
        gpu_total = m.get("gpu_memory_total", 0)
        gpu_power = m.get("gpu_power_w", 0)
        cpu_power = m.get("cpu_power_w", 0)

        lines.append(f"  CPU:     {cpu:.1f}%")
        lines.append(f"  GPU:     {gpu:.1f}%")
        lines.append(f"  Memory:  {mem:.1f}%")
        if gpu_mem and gpu_total:
            lines.append(f"  GPU Mem: {gpu_mem:,}MB / {gpu_total:,}MB")
        if gpu_power:
            lines.append(f"  GPU Power: {gpu_power:.0f}W")
        if cpu_power:
            lines.append(f"  CPU Power: {cpu_power:.0f}W")
    else:
        lines.append("  No system metrics available")

    # Cost stats
    energy = aggregator.get_cumulative_energy()
    if energy and energy.get("session_cost_usd") is not None:
        lines.append("")
        lines.append("Cost:")
        lines.append(f"  Session cost: ${energy['session_cost_usd']:.4f}")
        lines.append(f"  Total energy: {energy['total_wh']:.2f} Wh")

    return "\n".join(lines)


def format_stats_json(aggregator) -> str:
    """Format stats as JSON.

    Args:
        aggregator: DataAggregator instance

    Returns:
        JSON string
    """
    server_metrics = aggregator.get_recent_server_metrics(limit=1)
    system_metrics = aggregator.get_recent_system_metrics(limit=1)
    energy = aggregator.get_cumulative_energy()

    stats = {
        "timestamp": datetime.now().isoformat(),
        "server": server_metrics[0] if server_metrics else None,
        "system": system_metrics[0] if system_metrics else None,
        "cost": {
            "session_cost_usd": energy.get("session_cost_usd") if energy else None,
            "total_wh": energy.get("total_wh") if energy else None,
        },
    }

    return json.dumps(stats, indent=2)


def main():
    """Main entry point."""
    args = parse_args()

    try:
        config = get_config(args)

        db = Database(config.database_path)
        with db:
            aggregator = DataAggregator(
                database=db,
                server_url=config.server_url,
                tracked_processes=config.tracked_processes,
                cost_rate=config.cost_rate,
            )

            if args.json:
                print(format_stats_json(aggregator))
            else:
                print(format_stats(aggregator, args.verbose))

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
