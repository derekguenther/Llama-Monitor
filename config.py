#!/usr/bin/env python3
"""Configuration loader for llama-monitor."""

import os
import yaml
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for llama-monitor."""

    DEFAULT_CONFIG = {
        "idle_baseline": {
            "minimum_time_seconds": 5,
            "power_w": 150.0,
        },
        "compression": {
            "raw_to_1m_interval_seconds": 60,
            "raw_to_1m_start_after_seconds": 60,
            "1m_to_1h_interval_seconds": 3600,
            "1m_to_1h_start_after_seconds": 120,
        },
        "server": {
            "port": 8000,
        },
        "electricity": {
            "cost_rate": 0.12,
        },
        "metrics_collection": {
            "interval_seconds": 1.0,
            "collect_metrics": True,
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.

        Args:
            config_path: Path to YAML config file. If None, uses default config.
        """
        self.config_path = config_path
        self._config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()

        if config_path and os.path.exists(config_path):
            self._load_config(config_path)

    def _load_config(self, config_path: str) -> None:
        """Load configuration from YAML file.

        Args:
            config_path: Path to YAML config file.
        """
        with open(config_path, "r") as f:
            user_config = yaml.safe_load(f) or {}

        # Merge user config with defaults (deep merge)
        self._config = self._deep_merge(self.DEFAULT_CONFIG, user_config)

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """Deep merge update into base dict.

        Args:
            base: Base dictionary.
            update: Dictionary with values to merge in.

        Returns:
            Merged dictionary.
        """
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key.

        Args:
            key: Dot-notation key (e.g., "idle_baseline.minimum_time_seconds").
            default: Default value if key not found.

        Returns:
            Configuration value or default.
        """
        parts = key.split(".")
        value = self._config
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        return value

    def get_idle_baseline_config(self) -> Dict[str, Any]:
        """Get idle baseline configuration.

        Returns:
            Dictionary with idle baseline settings.
        """
        return self._config.get("idle_baseline", {})

    def get_compression_config(self) -> Dict[str, Any]:
        """Get compression configuration.

        Returns:
            Dictionary with compression settings.
        """
        return self._config.get("compression", {})

    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration.

        Returns:
            Dictionary with server settings.
        """
        return self._config.get("server", {})


def find_config(default_path: str = "config.yaml") -> str:
    """Find configuration file.

    Searches in this order:
    1. Current working directory
    2. Script directory
    3. Parent directory

    Args:
        default_path: Default config filename.

    Returns:
        Path to config file.
    """
    # Check current directory
    if os.path.exists(default_path):
        return default_path

    # Check script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_config = os.path.join(script_dir, default_path)
    if os.path.exists(script_config):
        return script_config

    # Check parent directory
    parent_config = os.path.join(os.path.dirname(script_dir), default_path)
    if os.path.exists(parent_config):
        return parent_config

    # Return default path (will fail later if file doesn't exist)
    return default_path


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file.

    Args:
        config_path: Path to config file. If None, uses default.

    Returns:
        Config instance with loaded configuration.
    """
    if config_path is None:
        config_path = find_config()
    return Config(config_path)


# Global config instance
_config: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or create global config instance.

    Args:
        config_path: Path to config file (only used on first call).

    Returns:
        Config instance.
    """
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config


def reload_config(config_path: Optional[str] = None) -> Config:
    """Reload configuration from file.

    Args:
        config_path: Path to config file.

    Returns:
        New Config instance.
    """
    global _config
    _config = Config(config_path)
    return _config
