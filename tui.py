"""Terminal UI for llama-monitor.

This module provides a curses-based terminal dashboard that:
- Displays real-time metrics from the aggregator daemon
- Shows server status, system resources, power consumption, and costs
- Updates automatically at configurable intervals
- Handles graceful shutdown

The TUI connects to the aggregator daemon's HTTP API for data.
"""

import curses
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from typing import Any, Dict, List, Optional

from config import load_config, find_config

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class TUI:
    """Terminal UI for llama-monitor."""

    def __init__(self, aggregator_host: str = "localhost", aggregator_port: int = 8080):
        """Initialize the TUI.

        Args:
            aggregator_host: Host of the aggregator daemon
            aggregator_port: Port of the aggregator daemon
        """
        self.aggregator_host = aggregator_host
        self.aggregator_port = aggregator_port
        self.config = load_config(find_config())

        self.running = False
        self.last_update = None
        self.metrics = {}
        self.history: List[Dict[str, Any]] = []
        self.max_history = 60  # Keep last 60 data points (60 seconds)

        # Color scheme
        self.colors = {}

    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:
        """Fetch latest metrics from aggregator daemon.

        Returns:
            Metrics data dictionary or None if fetch failed
        """
        try:
            url = f"http://{self.aggregator_host}:{self.aggregator_port}/api/metrics/latest"
            with urllib.request.urlopen(url, timeout=5) as response:
                return json.loads(response.read().decode())
        except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
            return None

    def _init_colors(self) -> None:
        """Initialize color pairs for curses."""
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()

            # Define color pairs
            curses.init_pair(1, curses.COLOR_CYAN, -1)      # Header/Title
            curses.init_pair(2, curses.COLOR_GREEN, -1)     # Good/Connected
            curses.init_pair(3, curses.COLOR_RED, -1)       # Bad/Disconnected
            curses.init_pair(4, curses.COLOR_YELLOW, -1)    # Warning
            curses.init_pair(5, curses.COLOR_WHITE, -1)     # Normal text
            curses.init_pair(6, curses.COLOR_BLUE, -1)      # Secondary info
            curses.init_pair(7, curses.COLOR_MAGENTA, -1)   # Cost/Power
            curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Inverted

            self.colors = {
                "header": curses.color_pair(1) | curses.A_BOLD,
                "good": curses.color_pair(2),
                "bad": curses.color_pair(3) | curses.A_BOLD,
                "warning": curses.color_pair(4),
                "normal": curses.color_pair(5),
                "secondary": curses.color_pair(6),
                "cost": curses.color_pair(7) | curses.A_BOLD,
                "inverted": curses.color_pair(8),
            }
        else:
            self.colors = {
                "header": curses.A_BOLD,
                "good": curses.A_NORMAL,
                "bad": curses.A_BOLD,
                "warning": curses.A_NORMAL,
                "normal": curses.A_NORMAL,
                "secondary": curses.A_NORMAL,
                "cost": curses.A_BOLD,
                "inverted": curses.A_REVERSE,
            }

    def _draw_header(self, stdscr) -> None:
        """Draw the header section."""
        height, width = stdscr.getmaxyx()

        # Title
        title = " llama-monitor Dashboard "
        stdscr.attron(self.colors.get("header", curses.A_BOLD))
        stdscr.addstr(0, 0, title.center(width)[:width-1])
        stdscr.attroff(self.colors.get("header", curses.A_BOLD))

        # Status line
        status = " Connected " if self.metrics else " Disconnected "
        status_color = self.colors.get("good") if self.metrics else self.colors.get("bad")

        status_str = f" {status} "
        stdscr.attron(status_color)
        stdscr.addstr(1, 0, status_str.center(width)[:width-1])
        stdscr.attroff(status_color)

        # Timestamp
        if self.last_update:
            timestamp = f" Last update: {self.last_update.strftime('%H:%M:%S')} "
            stdscr.addstr(2, 0, timestamp.center(width)[:width-1], curses.A_DIM)

    def _draw_cost_section(self, stdscr, start_row: int) -> int:
        """Draw the cost display section.

        Args:
            start_row: Starting row for this section

        Returns:
            Next available row
        """
        height, width = stdscr.getmaxyx()
        section_width = min(40, width - 2)

        # Cost card
        row = start_row
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(row, 0, " Today's Energy Cost ".center(section_width)[:section_width])
        stdscr.attroff(curses.A_REVERSE)

        row += 1
        if self.metrics and self.metrics.get("cost"):
            cost = self.metrics["cost"]
            # Use today's energy if available, otherwise fall back to session energy
            total_wh = cost.get("today_wh") or cost.get("total_wh", 0)
            cost_rate = getattr(self.config, "cost_rate", 0.12)
            cost_usd = total_wh / 1000 * cost_rate

            cost_str = f" ${cost_usd:.4f} "
            stdscr.attron(self.colors.get("cost", curses.A_BOLD))
            stdscr.addstr(row, 2, cost_str)
            stdscr.attroff(self.colors.get("cost", curses.A_BOLD))

            row += 1
            sub_str = f" Energy: {total_wh:.1f} Wh @ ${cost_rate:.2f}/kWh "
            stdscr.addstr(row, 2, sub_str[:section_width-4], curses.A_DIM)
        else:
            stdscr.addstr(row, 2, " No cost data available ", curses.A_DIM)

        return row + 2

    def _draw_server_section(self, stdscr, start_row: int) -> int:
        """Draw the server status section.

        Args:
            start_row: Starting row for this section

        Returns:
            Next available row
        """
        height, width = stdscr.getmaxyx()
        section_width = min(45, (width - 4) // 2)

        row = start_row

        # Card header
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(row, 2, " Server Status ".center(section_width-4)[:section_width-4])
        stdscr.attroff(curses.A_REVERSE)
        row += 1

        if self.metrics and self.metrics.get("server"):
            server = self.metrics["server"]

            # Prompt tokens
            prompt_tokens = server.get("prompt_tokens_total", 0) or 0
            prompt_rate = server.get("prompt_tokens_seconds", 0) or 0
            stdscr.addstr(row, 4, f"Prompt tokens:  {prompt_tokens:,}", self.colors.get("normal"))
            stdscr.addstr(row, 25, f"({prompt_rate:,.0f}/s)", self.colors.get("secondary"))
            row += 1

            # Generated tokens
            gen_tokens = server.get("tokens_predicted_total", 0) or 0
            gen_rate = server.get("predicted_tokens_seconds", 0) or 0
            stdscr.addstr(row, 4, f"Generated:      {gen_tokens:,}", self.colors.get("normal"))
            stdscr.addstr(row, 25, f"({gen_rate:,.0f}/s)", self.colors.get("secondary"))
            row += 1

            # Requests
            processing = server.get("requests_processing", 0) or 0
            deferred = server.get("requests_deferred", 0) or 0
            stdscr.addstr(row, 4, f"Requests:       {processing} processing", self.colors.get("normal"))
            if deferred > 0:
                stdscr.addstr(row, 25, f"{deferred} deferred", self.colors.get("warning"))
            row += 2
        else:
            stdscr.addstr(row, 4, " No server data available ", curses.A_DIM)
            row += 4

        return row

    def _draw_system_section(self, stdscr, start_row: int) -> int:
        """Draw the system resources section.

        Args:
            start_row: Starting row for this section

        Returns:
            Next available row
        """
        height, width = stdscr.getmaxyx()
        section_width = min(45, (width - 4) // 2)

        row = start_row

        # Card header
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(row, 2, " System Resources ".center(section_width-4)[:section_width-4])
        stdscr.attroff(curses.A_REVERSE)
        row += 1

        if self.metrics and self.metrics.get("system"):
            system = self.metrics["system"]

            # CPU usage
            cpu_percent = system.get("cpu_percent", 0) or 0
            stdscr.addstr(row, 4, f"CPU Usage:  {cpu_percent:5.1f}%", self.colors.get("normal"))
            self._draw_progress_bar(stdscr, row, 18, cpu_percent, section_width - 22)
            row += 1

            # GPU usage
            gpu_percent = system.get("gpu_usage", 0) or 0
            stdscr.addstr(row, 4, f"GPU Usage:  {gpu_percent:5.1f}%", self.colors.get("cost"))
            self._draw_progress_bar(stdscr, row, 18, gpu_percent, section_width - 22)
            row += 1

            # Memory usage
            memory_percent = system.get("memory_percent", 0) or 0
            stdscr.addstr(row, 4, f"Memory:     {memory_percent:5.1f}%", self.colors.get("normal"))
            self._draw_progress_bar(stdscr, row, 18, memory_percent, section_width - 22)
            row += 2

            # GPU memory
            gpu_mem_used = system.get("gpu_memory_used", 0) or 0
            gpu_mem_total = system.get("gpu_memory_total", 0) or 1
            stdscr.addstr(row, 4, f"GPU Memory: {gpu_mem_used:,} / {gpu_mem_total:,} MB", self.colors.get("normal"))
            row += 1
        else:
            stdscr.addstr(row, 4, " No system data available ", curses.A_DIM)
            row += 5

        return row

    def _draw_power_section(self, stdscr, start_row: int) -> int:
        """Draw the power and energy section.

        Args:
            start_row: Starting row for this section

        Returns:
            Next available row
        """
        height, width = stdscr.getmaxyx()
        section_width = min(45, (width - 4) // 2)

        row = start_row

        # Card header
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(row, 2, " Power & Energy ".center(section_width-4)[:section_width-4])
        stdscr.attroff(curses.A_REVERSE)
        row += 1

        if self.metrics and self.metrics.get("system"):
            system = self.metrics["system"]

            # GPU power
            gpu_power = system.get("gpu_power_w", 0) or 0
            stdscr.addstr(row, 4, f"GPU Power:    {gpu_power:6.1f} W", self.colors.get("cost"))
            row += 1

            # CPU power
            cpu_power = system.get("cpu_power_w", 0) or 0
            stdscr.addstr(row, 4, f"CPU Power:    {cpu_power:6.1f} W", self.colors.get("normal"))
            row += 1

            # System power
            system_power = system.get("system_power_w", 0) or 0
            stdscr.addstr(row, 4, f"System Power: {system_power:6.1f} W", self.colors.get("normal"))
            row += 2

            # Session energy
            if self.metrics.get("cost"):
                total_wh = self.metrics["cost"].get("total_wh", 0) or 0
                stdscr.addstr(row, 4, f"Session Energy: {total_wh:.1f} Wh", self.colors.get("secondary"))
                row += 1
        else:
            stdscr.addstr(row, 4, " No power data available ", curses.A_DIM)
            row += 4

        return row

    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:
        """Draw the per-process GPU section.

        Args:
            start_row: Starting row for this section

        Returns:
            Next available row
        """
        height, width = stdscr.getmaxyx()
        section_width = min(45, (width - 4) // 2)

        row = start_row

        # Card header
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(row, 2, " Process GPU ".center(section_width-4)[:section_width-4])
        stdscr.attroff(curses.A_REVERSE)
        row += 1

        if self.metrics and self.metrics.get("process_gpu"):
            process_gpu = self.metrics["process_gpu"]
            process_names = list(process_gpu.keys())

            if not process_names:
                stdscr.addstr(row, 4, " No tracked processes ", curses.A_DIM)
                row += 2
            else:
                # Show first 3 processes
                for i, name in enumerate(process_names[:3]):
                    proc = process_gpu[name]
                    pid = proc.get("pid", "?")
                    gpu_util = proc.get("gpu_utilization", 0) or 0
                    gpu_mem = proc.get("gpu_memory_mb", 0) or 0

                    stdscr.addstr(row, 4, f"{name[:15]:15s} (PID: {pid})", self.colors.get("normal"))
                    stdscr.addstr(row, 30, f"{gpu_util:5.1f}% {gpu_mem:6,} MB", self.colors.get("cost"))
                    row += 1
                row += 1
        else:
            stdscr.addstr(row, 4, " No process data available ", curses.A_DIM)
            row += 2

        return row

    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:
        """Draw a progress bar.

        Args:
            stdscr: Curses screen
            row: Row position
            col: Column position
            value: Value (0-100)
            width: Width of the progress bar
        """
        filled = int(width * value / 100)
        empty = width - filled

        stdscr.addstr(row, col, "[" + "#" * filled + "-" * empty + "]")

    def _draw_history_chart(self, stdscr, start_row: int) -> int:
        """Draw the history chart section.

        Args:
            start_row: Starting row for this section

        Returns:
            Next available row
        """
        height, width = stdscr.getmaxyx()
        chart_width = width - 4
        chart_height = 8

        row = start_row

        # Card header
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(row, 0, " Recent History (GPU/CPU/Power) ".center(width)[:width-1])
        stdscr.attroff(curses.A_REVERSE)
        row += 1

        if len(self.history) < 2:
            stdscr.addstr(row + 2, 4, " Collecting history data... ", curses.A_DIM)
            return row + chart_height + 1

        # Get data ranges
        gpu_values = [m.get("system", {}).get("gpu_usage", 0) or 0 for m in self.history]
        cpu_values = [m.get("system", {}).get("cpu_percent", 0) or 0 for m in self.history]
        power_values = [(m.get("system", {}).get("gpu_power_w", 0) or 0) + (m.get("system", {}).get("cpu_power_w", 0) or 0) for m in self.history]

        max_gpu = max(gpu_values) if gpu_values else 100
        max_cpu = max(cpu_values) if cpu_values else 100
        max_power = max(power_values) if power_values else 100

        # Draw GPU chart
        stdscr.addstr(row, 2, "GPU:", self.colors.get("cost"))
        for i in range(chart_height):
            row_idx = chart_height - 1 - i
            if row_idx < len(gpu_values):
                value = gpu_values[row_idx]
                bar_width = int(chart_width * value / max(max_gpu, 1))
                stdscr.addstr(row + 1 + i, 7, "=" * bar_width, self.colors.get("cost"))

        # Draw CPU chart
        stdscr.addstr(row + 5, 2, "CPU:", self.colors.get("good"))
        for i in range(3):
            row_idx = chart_height - 1 - i
            if row_idx < len(cpu_values):
                value = cpu_values[row_idx]
                bar_width = int(chart_width * value / max(max_cpu, 1))
                stdscr.addstr(row + 6 + i, 7, "=" * bar_width, self.colors.get("good"))

        # Legend
        row += chart_height + 1
        stdscr.addstr(row, 2, "Legend: GPU = green, CPU = blue, Power = magenta", curses.A_DIM)

        return row + 2

    def _draw_footer(self, stdscr) -> None:
        """Draw the footer with controls."""
        height, width = stdscr.getmaxyx()
        footer_row = height - 1

        footer_text = " Q:Quit | R:Refresh "
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(footer_row, 0, footer_text.center(width)[:width-1])
        stdscr.attroff(curses.A_REVERSE)

    def _main_loop(self, stdscr) -> None:
        """Main TUI loop.

        Args:
            stdscr: Curses screen
        """
        # Initialize colors
        self._init_colors()

        # Hide cursor
        curses.curs_set(0)

        # Set refresh rate
        refresh_interval = self.config.polling_interval if hasattr(self.config, "polling_interval") else 1

        # Main loop
        while self.running:
            # Fetch metrics
            metrics = self._fetch_metrics()
            if metrics:
                self.metrics = metrics
                self.last_update = datetime.now()

                # Add to history
                self.history.append(metrics)
                if len(self.history) > self.max_history:
                    self.history.pop(0)

            # Clear screen
            stdscr.clear()

            # Draw sections
            self._draw_header(stdscr)

            row = 4
            row = self._draw_cost_section(stdscr, row)
            row = self._draw_server_section(stdscr, row)
            row = self._draw_system_section(stdscr, row)
            row = self._draw_power_section(stdscr, row)
            row = self._draw_process_gpu_section(stdscr, row)
            row = self._draw_history_chart(stdscr, row)

            self._draw_footer(stdscr)

            # Refresh screen
            stdscr.refresh()

            # Wait for next update or key press
            stdscr.timeout(100)
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord('r') or key == ord('R'):
                # Force refresh
                continue

            # Sleep for remaining time
            time.sleep(refresh_interval)

    def run(self) -> None:
        """Run the TUI."""
        self.running = True

        try:
            curses.wrapper(self._main_loop)
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False

    def stop(self) -> None:
        """Stop the TUI."""
        self.running = False


def main() -> int:
    """Main entry point for the TUI."""
    import argparse

    parser = argparse.ArgumentParser(description="llama-monitor terminal UI")
    parser.add_argument(
        "--host",
        "-H",
        default="localhost",
        help="Aggregator host (default: localhost)",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8080,
        help="Aggregator port (default: 8080)",
    )
    parser.add_argument(
        "--config",
        "-c",
        help="Path to config.yaml file",
    )

    args = parser.parse_args()

    # Override config path if specified
    if args.config:
        os.environ["LLAMA_MONITOR_CONFIG"] = args.config

    tui = TUI(aggregator_host=args.host, aggregator_port=args.port)
    tui.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
