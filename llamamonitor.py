#!/usr/bin/env python3
"""Main entry point for llama-monitor."""

import argparse
import logging
import math
import os
import signal
import sys
import threading
import time
from typing import Any, Dict, Optional

from aggregator import Aggregator
from config import Config, get_config, reload_config, find_config
from db import Database



def format_significant_digits(value: float, digits: int = 4) -> str:
    """Format a value with the specified number of significant digits.

    Args:
        value: The numeric value to format
        digits: Number of significant digits (default: 4)

    Returns:
        Formatted string with the specified significant digits
    """
    if value is None or value == 0 or not isinstance(value, (int, float)):
        return "0"
    if value == 0:
        return "0"

    abs_value = abs(value)
    exponent = math.floor(math.log10(abs_value))
    # Calculate decimal places needed
    decimal_places = digits - 1 - exponent
    if decimal_places < 0:
        decimal_places = 0

    # Format with the calculated decimal places
    format_str = f"{{:.{decimal_places}f}}"
    return format_str.format(value)


class MetricsCache:
    """Thread-safe cache for metrics shared between aggregator and UI."""

    def __init__(self):
        self._metrics: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def update(self, metrics: Dict[str, Any]):
        """Update metrics from aggregator."""
        with self._lock:
            self._metrics = metrics.copy()

    def get(self) -> Dict[str, Any]:
        """Get latest metrics."""
        with self._lock:
            return self._metrics.copy()


class Monitor:
    """Main monitor orchestrator."""

    def __init__(
        self,
        server_url: str = "http://localhost:8000",
        config_path: str = "llama-monitor/config.yaml",
        polling_interval: float = 1.0,
        enable_web: bool = True,
        enable_tui: bool = False,
        port: int = 8080,
        show_stats: bool = False,
        verbose: bool = False,
        debug: bool = False,
    ):
        """Initialize the monitor.

        Args:
            server_url: URL of the llama.cpp server.
            config_path: Path to config file.
            polling_interval: Metrics collection interval in seconds.
            enable_web: Enable web server mode.
            enable_tui: Enable TUI mode.
            show_stats: Show stats and exit.
            verbose: Enable verbose logging.
        """
        self.server_url = server_url
        self.config_path = config_path
        self.polling_interval = polling_interval
        self.enable_web = enable_web
        self.enable_tui = enable_tui
        self.port = port
        self.show_stats = show_stats
        self.verbose = verbose
        self.debug = debug

        # Configure logging based on verbose flag
        if verbose:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            logging.getLogger('werkzeug').setLevel(logging.INFO)
            logging.getLogger('socketio').setLevel(logging.INFO)
            logging.getLogger('engineio').setLevel(logging.INFO)
        else:
            logging.basicConfig(
                level=logging.WARNING,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            logging.getLogger('werkzeug').setLevel(logging.WARNING)
            logging.getLogger('socketio').setLevel(logging.WARNING)
            logging.getLogger('engineio').setLevel(logging.WARNING)

        # Load config first - fall back to find_config if path doesn't exist
        if config_path and not os.path.exists(config_path):
            config_path = find_config()
        self.config = get_config(config_path)

        # Override server_url from config if specified
        config_server_url = self.config.get("server.url")
        if config_server_url:
            self.server_url = config_server_url

        # Shared metrics cache
        self.metrics_cache = MetricsCache()

        # Aggregator
        self.aggregator: Optional[Aggregator] = None

        # Threads
        self.aggregator_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()

        # Mode-specific components
        self.web_server_thread: Optional[threading.Thread] = None
        self.tui: Optional[Any] = None

    def initialize(self):
        """Initialize the monitor components."""
        # Initialize database - use absolute path
        db_path = self.config.get("database.path", "llama-monitor.db")
        if not os.path.isabs(db_path):
            # Resolve relative paths relative to the script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, db_path)
        self.db = Database(db_path)
        self.db.connect()

        # Initialize aggregator
        cost_rate = self.config.get("electricity.cost_rate", 0.12)
        idle_baseline = self.config.get("idle_baseline.power_w", 40.0)
        collect_metrics = self.config.get("metrics_collection.collect_metrics", True)
        tracked_processes = self.config.get("metrics_collection.tracked_processes", ["llama.cpp"])

        self.aggregator = Aggregator(
            server_url=self.server_url,
            db_path=db_path,
            idle_baseline_w=idle_baseline,
            cost_rate=cost_rate,
            collect_metrics=collect_metrics,
        )
        # Override tracked_processes if specified in config
        if tracked_processes:
            self.aggregator.system_collector.tracked_processes = tracked_processes

        # Set polling interval from config
        self.polling_interval = self.config.get(
            "metrics_collection.interval_seconds", self.polling_interval
        )

    def run_aggregator_loop(self):
        """Background thread to run the aggregator collection loop."""
        iteration = 0
        while not self._shutdown_event.is_set():
            loop_start = time.monotonic()
            try:
                # Collect and store metrics
                metrics = self.aggregator.collect_all_metrics()
                print(f"[DEBUG] iter {iteration}: collect_all_metrics keys={list(metrics.keys())}")
                if iteration == 0:
                    sys = metrics.get("system", {})
                    print(f"[DEBUG]   system keys={list(sys.keys())}")
                    print(f"[DEBUG]   cpu_percent={sys.get('cpu_percent')}, gpu_usage={sys.get('gpu_usage')}")
                    print(f"[DEBUG]   nested cpu={sys.get('cpu', {})}, gpu={sys.get('gpu', {})}")
                    svr = metrics.get("server", {})
                    print(f"[DEBUG]   server keys={list(svr.keys())}")

                self.aggregator.store_raw_metrics(metrics)
                self.aggregator.compress_if_needed()
                cost = self.aggregator.calculate_cost()
                metrics["cost"] = cost

                if iteration == 0:
                    print(f"[DEBUG]   cost keys={list(cost.keys())}")
                    print(f"[DEBUG]   session_cost_usd={cost.get('session_cost_usd')}, today_cost={cost.get('today_cost')}")

                # Update shared cache
                self.metrics_cache.update(metrics)

                if iteration == 0:
                    # Verify cache has cost
                    cached = self.metrics_cache.get()
                    print(f"[DEBUG]   cache keys={list(cached.keys())}")
                    print(f"[DEBUG]   cache has cost={'cost' in cached}, cost type={type(cached.get('cost'))}")

                # Wait for next interval, accounting for time already spent on work
                elapsed = time.monotonic() - loop_start
                wait_time = max(0.0, self.polling_interval - elapsed)
                self._shutdown_event.wait(wait_time)
                iteration += 1
            except Exception as e:
                # Log error but continue loop
                import traceback
                import sqlite3
                print(f"Error in aggregator loop: {e}")
                traceback.print_exc()
                # If the database is corrupt, rebuild it so the monitor recovers
                # automatically instead of failing every iteration.
                if isinstance(e, sqlite3.DatabaseError):
                    print("Database corruption detected; attempting automatic recovery...")
                    if self.aggregator and hasattr(self.aggregator, "db"):
                        if self.aggregator.db.recover_from_corruption():
                            print("Database recovered successfully; resuming normal operation.")
                        else:
                            print("Database recovery FAILED; will retry.")
                self._shutdown_event.wait(1)

    def shutdown(self):
        """Gracefully shutdown the monitor."""
        print("Shutting down...")
        self._shutdown_event.set()

        # Wait for aggregator thread to finish
        if self.aggregator_thread:
            self.aggregator_thread.join(timeout=2)

        # Stop web server if running
        if self.web_server_thread:
            from web_server import stop_server as stop_web_server
            stop_web_server()

        # Stop TUI if running
        if self.tui:
            self.tui.running = False

        # Close aggregator
        if self.aggregator:
            self.aggregator.close()

        # Close database
        if hasattr(self, "db") and self.db:
            self.db.close()

        print("Shutdown complete.")

    def run_web_mode(self):
        """Run in web server mode."""
        from web_server import start_server as start_web_server

        print(f"Starting web server on port {self.port}")

        # Start web server in background thread
        self.web_server_thread = threading.Thread(
            target=lambda: start_web_server(host="0.0.0.0", port=self.port, metrics_cache=self.metrics_cache, verbose=self.verbose, debug=self.debug),
            daemon=True,
        )
        self.web_server_thread.start()

        # Wait for shutdown
        while not self._shutdown_event.is_set():
            time.sleep(0.1)

    def run_tui_mode(self):
        """Run in TUI mode."""
        # Check for Windows + cmd.exe (no curses support)
        import sys
        import os

        if os.name == 'nt':
            # Windows detected - check if running in cmd.exe
            terminal = os.environ.get('TERM', '')
            if 'cmd' in terminal.lower() or not terminal:
                print("ERROR: TUI mode is not supported in cmd.exe on Windows.")
                print("")
                print("The TUI uses curses which requires a proper terminal emulator.")
                print("")
                print("Options:")
                print("  1. Use the web interface (default): python main.py")
                print("  2. Use Windows Terminal or PowerShell")
                print("  3. Use Git Bash or MSYS2")
                print("")
                sys.exit(1)

        try:
            import curses
        except ImportError:
            print("ERROR: curses module not found.")
            print("")
            print("On Windows, install: pip install windows-curses")
            print("")
            sys.exit(1)

        from tui import TUI

        print("Starting TUI dashboard...")

        # TUI connects to the aggregator daemon via HTTP API
        # When running via main.py, pass metrics_cache for in-process data sharing
        self.tui = TUI(
            aggregator_host="localhost",
            aggregator_port=self.port,
            metrics_cache=self.metrics_cache,
        )

        try:
            self.tui.run()
        except KeyboardInterrupt:
            pass
        finally:
            self.tui.running = False

    def show_statistics(self):
        """Show system statistics and exit."""
        self.initialize()

        # Collect one sample
        metrics = self.aggregator.collect_all_metrics()
        cost = self.aggregator.calculate_cost()

        # Aggregator already returns nested system structure
        system = metrics.get("system", {})

        print("\n=== Llama Monitor Statistics ===\n")

        # Server metrics
        server = metrics.get("server", {})
        print("Server:")
        print(f"  Prompt tokens:    {server.get('prompt_tokens_total', 0):,}")
        print(f"  Generated:        {server.get('tokens_predicted_total', 0):,}")
        print(f"  Requests:         {server.get('requests_processing', 0)} processing")

        # System metrics
        cpu = system.get("cpu", {})
        gpu = system.get("gpu", {})
        mem = system.get("memory", {})
        sys_power = system.get("system", {})

        print("\nSystem:")
        print(f"  CPU:              {format_significant_digits(cpu.get('percent', 0))}%")
        print(f"  GPU Usage:        {format_significant_digits(gpu.get('usage', 0))}%")
        print(f"  GPU Memory:       {format_significant_digits(gpu.get('memory_used', 0))} MB / {format_significant_digits(gpu.get('memory_total', 0))} MB")
        print(f"  Memory:           {format_significant_digits(mem.get('used', 0))} MB / {format_significant_digits(mem.get('total', 0))} MB")
        print(f"  GPU Temp:         {format_significant_digits(gpu.get('temperature_c', 0))}°C")
        print(f"  System Power:     {format_significant_digits(sys_power.get('system_power_w', 0))} W")
        print(f"  GPU Power:        {format_significant_digits(gpu.get('power_w', 0))} W")

        # Cost - show today's energy
        print("\nCost:")
        if cost:
            today_wh = cost.get('today_wh') or cost.get('total_wh', 0)
            print(f"  Today's Cost:     ${format_significant_digits(cost.get('total_cost', 0))}")
            print(f"  Today's Energy:   {format_significant_digits(today_wh)} Wh")
        else:
            print("  No cost data available (no active session)")

        print("\n" + "=" * 36)

        self.shutdown()
        sys.exit(0)

    def run(self):
        """Run the monitor in the specified mode(s)."""
        try:
            if self.show_stats:
                self.show_statistics()

            self.initialize()

            # Start aggregator loop in background thread
            self.aggregator_thread = threading.Thread(
                target=self.run_aggregator_loop,
                daemon=True,
            )
            self.aggregator_thread.start()

            # Run selected modes
            if self.enable_web:
                self.run_web_mode()

            if self.enable_tui:
                self.run_tui_mode()

            # If neither mode enabled, just run aggregator and wait
            if not self.enable_web and not self.enable_tui:
                print("No UI mode enabled. Aggregator running in background.")
                while not self._shutdown_event.is_set():
                    time.sleep(0.1)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            self.shutdown()


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Llama Monitor - Real-time GPU/CPU metrics and cost tracking"
    )

    parser.add_argument(
        "--server",
        type=str,
        default="http://localhost:8000",
        help="URL of the llama.cpp server (default: http://localhost:8000)",
    )

    parser.add_argument(
        "--config",
        type=str,
        default="llama-monitor/config.yaml",
        help="Path to config file (default: llama-monitor/config.yaml)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Web server port (default: 8080)",
    )
    parser.add_argument(
        "--polling-interval",
        type=float,
        default=1.0,
        help="Metrics collection interval in seconds (default: 1.0)",
    )

    parser.add_argument(
        "--no-web",
        action="store_true",
        help="Disable web server (default: web server is enabled)",
    )

    parser.add_argument(
        "--tui",
        action="store_true",
        help="Enable TUI mode (default: disabled)",
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show system statistics and exit",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging (INFO level for werkzeug, socketio, engineio)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable Flask debug mode (auto-reload on code changes, detailed error pages)",
    )

    return parser.parse_args()


def ensure_dependencies(check_tui: bool = False):
    """Check for and install missing dependencies from requirements.txt.

    Args:
        check_tui: If True, also check for windows-curses even if not on Windows.
    """
    import os
    import sys
    import subprocess

    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(script_dir, 'requirements.txt')

    if not os.path.exists(requirements_path):
        return

    # Check for required dependencies
    missing_required = []
    try:
        import flask
        import flask_socketio
        import psutil
        import yaml
        import requests
    except ImportError as e:
        missing_required = [e.name] if hasattr(e, 'name') else ['unknown']

    # Check for optional windows-curses (only needed for TUI on Windows)
    missing_optional = []
    if os.name == 'nt' or check_tui:
        try:
            import curses
        except ImportError:
            missing_optional = ['windows-curses']

    # If nothing is missing, we're done
    if not missing_required and not missing_optional:
        return

    # Ask user if they want to install dependencies
    print("=" * 60)
    if missing_required:
        print("Missing dependencies detected.")
        print(f"Missing required: {', '.join(missing_required)}")
    if missing_optional:
        print(f"Missing optional (for TUI on Windows): {', '.join(missing_optional)}")
    print("=" * 60)
    print("")

    try:
        response = input("Install missing dependencies now? [Y/n] ").strip().lower()
        if response in ('', 'y', 'yes'):
            print("")
            print("Installing dependencies...")
            print("")

            # Run pip install
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', requirements_path],
                cwd=script_dir,
                capture_output=False
            )

            if result.returncode == 0:
                print("")
                print("Dependencies installed successfully!")
                print("Please run the command again.")
            else:
                print("")
                print("ERROR: Failed to install dependencies.")
                print("You may need to install them manually:")
                print(f"  pip install -r {requirements_path}")
            sys.exit(result.returncode)
        else:
            print("")
            print("Please install dependencies manually:")
            print(f"  pip install -r {requirements_path}")
            sys.exit(1)
    except KeyboardInterrupt:
        print("")
        print("Installation cancelled.")
        sys.exit(1)


def main():
    """Main entry point."""
    import os
    import sys

    # Check and install dependencies first
    ensure_dependencies()

    args = parse_args()

    if args.version:
        print("llama-monitor 1.0.0")
        sys.exit(0)

    # On Windows, disable TUI by default and warn if user tries to enable it
    if os.name == 'nt':
        if args.tui:
            try:
                import curses
            except ImportError:
                print("ERROR: TUI mode requires windows-curses on Windows.")
                print("")
                print("The curses module is not installed by default on Windows.")
                print("")
                print("Options:")
                print("  1. Use the web interface (default): python main.py")
                print("  2. Install windows-curses: pip install windows-curses")
                print("  3. Use Windows Terminal, PowerShell, or MSYS2")
                print("")
                sys.exit(1)
        # On Windows, default to web-only mode if TUI not requested
        # (if user explicitly requests TUI, respect that)
        # But if TUI is requested, disable web by default (unless --no-web was NOT set)
        # Actually, let's make TUI imply --no-web for cleaner UX
        if args.tui and not args.no_web:
            args.no_web = True

    monitor = Monitor(
        server_url=args.server,
        config_path=args.config,
        polling_interval=args.polling_interval,
        enable_web=not args.no_web,
        enable_tui=args.tui,
        show_stats=args.stats,
        port=args.port,
        verbose=args.verbose,
        debug=args.debug,
    )

    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        monitor.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    monitor.run()


if __name__ == "__main__":
    main()
