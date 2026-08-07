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


def _value_or_zero(val, sentinel=-1.0):
    """Return val if not None and not sentinel, else 0."""
    if val is None or val == sentinel:
        return 0
    return val


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
        prompt_tokens = _value_or_zero(server.get("prompt_tokens_total"))
        prompt_rate = _value_or_zero(server.get("prompt_tokens_seconds"))
        generated = _value_or_zero(server.get("tokens_predicted_total"))
        gen_rate = _value_or_zero(server.get("predicted_tokens_seconds"))
        processing = _value_or_zero(server.get("requests_processing"))
        deferred = _value_or_zero(server.get("requests_deferred"))

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
        cpu = _value_or_zero(system.get("cpu_percent"))
        gpu = _value_or_zero(system.get("gpu_usage"))
        mem = _value_or_zero(system.get("memory_percent"))
        gpu_mem = _value_or_zero(system.get("gpu_memory_used"))
        gpu_total = _value_or_zero(system.get("gpu_memory_total"))
        gpu_power = _value_or_zero(system.get("gpu_power_w"))
        cpu_power = _value_or_zero(system.get("cpu_power_w"))
        system_power = _value_or_zero(system.get("system_power_w"))

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
                gpu_util = _value_or_zero(proc.get("gpu_utilization"))
                gpu_mem = _value_or_zero(proc.get("gpu_memory_mb"))
                lines.append(f"  {name[:15]:15s} (PID: {pid})")
                lines.append(f"    GPU: {gpu_util:.1f}%  Memory: {gpu_mem:,}MB")

    # Cost stats
    cost = metrics.get("cost", {})
    if cost:
        # Use today's energy if available, otherwise fall back to session energy
        total_wh = _value_or_zero(cost.get("today_wh")) or _value_or_zero(cost.get("total_wh"))
        cost_rate = _value_or_zero(cost.get("cost_rate"))
        session_cost = total_wh / 1000 * cost_rate

        lines.append("")
        lines.append("Cost:")
        lines.append(f"  Today's cost: ${session_cost:.4f}")
        lines.append(f"  Today's energy: {total_wh:.2f} Wh")
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
