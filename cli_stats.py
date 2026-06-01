#!/usr/bin/env python3
"""CLI stats command for llama-monitor.

Provides on-demand stats output similar to `kubectl top`.
Fetches metrics from the aggregator daemon's HTTP API.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Any, Dict, Optional


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
        "--host",
        type=str,
        default="localhost",
        help="Aggregator daemon host (default: localhost)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Aggregator daemon port (default: 8080)",
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


def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
    """Fetch latest metrics from aggregator daemon.

    Args:
        host: Aggregator daemon host
        port: Aggregator daemon port

    Returns:
        Metrics data dictionary or None if fetch failed
    """
    try:
        url = f"http://{host}:{port}/api/metrics/latest"
        with urllib.request.urlopen(url, timeout=5) as response:
            return json.loads(response.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
        return None


def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:
    """Format stats for display.

    Args:
        metrics: Metrics data dictionary
        verbose: Show detailed output

    Returns:
        Formatted string
    """
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append(f"llama-monitor stats ({timestamp})")
    lines.append("=" * 40)

    # Server stats
    server = metrics.get("server", {})
    lines.append("")
    lines.append("Server:")
    if server:
        prompt_tokens = server.get("prompt_tokens_total", 0) or 0
        prompt_rate = server.get("prompt_tokens_seconds", 0) or 0
        generated = server.get("tokens_predicted_total", 0) or 0
        gen_rate = server.get("predicted_tokens_seconds", 0) or 0
        processing = server.get("requests_processing", 0) or 0
        deferred = server.get("requests_deferred", 0) or 0

        lines.append(f"  Prompt tokens:    {prompt_tokens:,} ({prompt_rate:,.0f}/s)")
        lines.append(f"  Generated:        {generated:,} ({gen_rate:,.0f}/s)")
        lines.append(f"  Processing:       {processing}")
        lines.append(f"  Deferred:         {deferred}")
    else:
        lines.append("  No server metrics available")

    # System stats
    system = metrics.get("system", {})
    lines.append("")
    lines.append("System:")
    if system:
        cpu = system.get("cpu_percent", 0) or 0
        gpu = system.get("gpu_usage", 0) or 0
        mem = system.get("memory_percent", 0) or 0
        gpu_mem = system.get("gpu_memory_used", 0) or 0
        gpu_total = system.get("gpu_memory_total", 0) or 0
        gpu_power = system.get("gpu_power_w", 0) or 0
        cpu_power = system.get("cpu_power_w", 0) or 0
        system_power = system.get("system_power_w", 0) or 0

        lines.append(f"  CPU:         {cpu:.1f}%")
        lines.append(f"  GPU:         {gpu:.1f}%")
        lines.append(f"  Memory:      {mem:.1f}%")
        if gpu_mem and gpu_total:
            lines.append(f"  GPU Mem:     {gpu_mem:,}MB / {gpu_total:,}MB")
        if gpu_power:
            lines.append(f"  GPU Power:   {gpu_power:.0f}W")
        if cpu_power:
            lines.append(f"  CPU Power:   {cpu_power:.0f}W")
        if system_power:
            lines.append(f"  System Power:{system_power:.0f}W")
    else:
        lines.append("  No system metrics available")

    # Per-process GPU stats (verbose only)
    if verbose:
        process_gpu = metrics.get("process_gpu", {})
        if process_gpu:
            lines.append("")
            lines.append("Process GPU:")
            for name, proc in list(process_gpu.items())[:5]:
                pid = proc.get("pid", "?")
                gpu_util = proc.get("gpu_utilization", 0) or 0
                gpu_mem = proc.get("gpu_memory_mb", 0) or 0
                lines.append(f"  {name[:15]:15s} (PID: {pid})")
                lines.append(f"    GPU: {gpu_util:.1f}%  Memory: {gpu_mem:,}MB")

    # Cost stats
    cost = metrics.get("cost", {})
    if cost:
        total_wh = cost.get("total_wh", 0) or 0
        cost_rate = cost.get("cost_rate", 0) or 0
        session_cost = total_wh / 1000 * cost_rate

        lines.append("")
        lines.append("Cost:")
        lines.append(f"  Session cost: ${session_cost:.4f}")
        lines.append(f"  Total energy: {total_wh:.2f} Wh")
        lines.append(f"  Cost rate:    ${cost_rate:.2f}/kWh")

    return "\n".join(lines)


def format_stats_json(metrics: Dict[str, Any]) -> str:
    """Format stats as JSON.

    Args:
        metrics: Metrics data dictionary

    Returns:
        JSON string
    """
    # Clean up the metrics for JSON output
    output = {
        "timestamp": datetime.now().isoformat(),
        "server": metrics.get("server"),
        "system": metrics.get("system"),
        "process_gpu": metrics.get("process_gpu"),
        "cost": metrics.get("cost"),
    }

    return json.dumps(output, indent=2)


def main():
    """Main entry point."""
    args = parse_args()

    try:
        metrics = fetch_metrics(args.host, args.port)

        if metrics is None:
            print("Error: Could not connect to aggregator daemon", file=sys.stderr)
            print(f"  Host: {args.host}, Port: {args.port}", file=sys.stderr)
            return 1

        if args.json:
            print(format_stats_json(metrics))
        else:
            print(format_stats(metrics, args.verbose))

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
