"""Configuration management for llama-monitor."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Config:
    """Manages configuration for llama-monitor."""

    DEFAULT_CONFIG = {
        "server": {
            "url": "http://localhost:8000",
            "model_id": "llama-model",
            "metrics_endpoint": "/metrics",
        },
        "data": {
            "polling_interval": 1,
            "compression_level_1": {
                "interval": 1,
                "start_after": 1,
                "unit": "week",
            },
            "compression_level_2": {
                "interval": 1,
                "start_after": 1,
                "unit": "month",
            },
            "retention": {
                "raw_forever": False,
                "archive_path": "archive/",
            },
        },
        "display": {
            "tui_refresh_rate": 2.0,
            "web_refresh_rate": 1.0,
            "show_cost": True,
            "show_temps": True,
            "cost_rate": 0.12,
        },
        "database": {
            "path": "llama_monitor.db",
            "compression_enabled": True,
            "auto_vacuum": True,
        },
        "tracking": {
            "tracked_processes": ["llama-server.exe"],
            "min_gpu_utilization": 1,
        },
        "web": {
            "https_port": 2633,
            "http_port": 2634,
            "https_enabled": True,
        },
        "logging": {
            "level": "INFO",
            "file": "llama_monitor.log",
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration from file or use defaults.

        Args:
            config_path: Path to config.yaml file. If None, uses default config.
        """
        self.config_path = config_path
        self._config = self.DEFAULT_CONFIG.copy()

        if config_path and os.path.exists(config_path):
            self._load_config(config_path)

    def _load_config(self, config_path: str) -> None:
        """Load configuration from YAML file."""
        with open(config_path, "r") as f:
            user_config = yaml.safe_load(f)

        if user_config:
            self._config = self._deep_merge(self._config, user_config)

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """Recursively merge dictionaries."""
        result = base.copy()

        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.

        Args:
            key: Dot-notation key (e.g., "server.url")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        parts = key.split(".")
        value = self._config

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation.

        Args:
            key: Dot-notation key (e.g., "server.url")
            value: Value to set
        """
        parts = key.split(".")
        config = self._config

        for part in parts[:-1]:
            if part not in config or not isinstance(config[part], dict):
                config[part] = {}
            config = config[part]

        config[parts[-1]] = value

    @property
    def server_url(self) -> str:
        """Get server URL."""
        return self.get("server.url", "http://localhost:8000")

    @property
    def server_model_id(self) -> str:
        """Get model ID for display."""
        return self.get("server.model_id", "llama-model")

    @property
    def server_metrics_endpoint(self) -> str:
        """Get metrics endpoint path."""
        return self.get("server.metrics_endpoint", "/metrics")

    @property
    def polling_interval(self) -> int:
        """Get polling interval in seconds."""
        return self.get("data.polling_interval", 1)

    @property
    def tui_refresh_rate(self) -> float:
        """Get TUI refresh rate in seconds."""
        return self.get("display.tui_refresh_rate", 2.0)

    @property
    def web_refresh_rate(self) -> float:
        """Get web dashboard refresh rate in seconds."""
        return self.get("display.web_refresh_rate", 1.0)

    @property
    def show_cost(self) -> bool:
        """Whether to show cost in displays."""
        return self.get("display.show_cost", True)

    @property
    def show_temps(self) -> bool:
        """Whether to show temperatures."""
        return self.get("display.show_temps", True)

    @property
    def cost_rate(self) -> float:
        """Electricity cost in USD per kWh."""
        return self.get("display.cost_rate", 0.12)

    @property
    def database_path(self) -> str:
        """Path to SQLite database."""
        return self.get("database.path", "llama_monitor.db")

    @property
    def compression_enabled(self) -> bool:
        """Whether compression is enabled."""
        return self.get("database.compression_enabled", True)

    @property
    def auto_vacuum(self) -> bool:
        """Whether to run auto vacuum."""
        return self.get("database.auto_vacuum", True)

    @property
    def tracked_processes(self) -> list:
        """List of processes to track."""
        return self.get("tracking.tracked_processes", ["llama-server.exe"])

    @property
    def min_gpu_utilization(self) -> int:
        """Minimum GPU utilization to track."""
        return self.get("tracking.min_gpu_utilization", 1)

    @property
    def web_https_port(self) -> int:
        """HTTPS port for web server."""
        return self.get("web.https_port", 2633)

    @property
    def web_http_port(self) -> int:
        """HTTP port for web server."""
        return self.get("web.http_port", 2634)

    @property
    def web_https_enabled(self) -> bool:
        """Whether HTTPS is enabled."""
        return self.get("web.https_enabled", True)

    @property
    def log_level(self) -> str:
        """Log level."""
        return self.get("logging.level", "INFO")

    @property
    def log_file(self) -> str:
        """Log file path."""
        return self.get("logging.file", "llama_monitor.log")

    def to_dict(self) -> Dict:
        """Return full configuration as dictionary."""
        return self._config.copy()


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file or use defaults.

    Args:
        config_path: Path to config.yaml file. If None, uses default config.

    Returns:
        Config instance
    """
    return Config(config_path)


def find_config() -> Optional[str]:
    """Find config file in common locations.

    Returns:
        Path to config file if found, None otherwise
    """
    possible_paths = [
        "config.yaml",
        "llama-monitor/config.yaml",
        os.path.expanduser("~/.config/llama-monitor/config.yaml"),
        os.path.expanduser("~/llama-monitor/config.yaml"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return os.path.abspath(path)

    return None
