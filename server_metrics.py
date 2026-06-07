"""Server metrics collector for llama.cpp server."""

import time
from typing import Any, Dict, Optional

import requests


class ServerMetricsCollector:
    """Collects metrics from llama.cpp server endpoints."""

    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
        """Initialize the collector.

        Args:
            server_url: Base URL of the llama.cpp server
            metrics_endpoint: Path to the metrics endpoint
            collect_metrics: Whether to attempt collecting /metrics data
        """
        self.server_url = server_url.rstrip("/")
        self.metrics_endpoint = metrics_endpoint
        self.collect_metrics = collect_metrics
        self.metrics_available = True  # Will be set to False if /metrics returns error

    def _make_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make HTTP request to server endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            JSON response as dictionary, or None if request failed
        """
        url = f"{self.server_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Check if this is a metrics endpoint error (not supported)
            if endpoint == self.metrics_endpoint:
                self.metrics_available = False
            return None

    def get_metrics(self) -> Optional[Dict[str, Any]]:
        """Fetch metrics from /metrics endpoint.

        Returns:
            Dictionary with metrics data, or None if request failed
        """
        return self._make_request(self.metrics_endpoint)

    def get_slots(self) -> Optional[Dict[str, Any]]:
        """Fetch slot information from /slots endpoint.

        Returns:
            Dictionary with slots data, or None if request failed
        """
        return self._make_request("/slots")

    def get_props(self) -> Optional[Dict[str, Any]]:
        """Fetch server properties from /props endpoint.

        Returns:
            Dictionary with props data, or None if request failed
        """
        return self._make_request("/props")

    def collect(self) -> Dict[str, Any]:
        """Collect all server metrics.

        Returns:
            Dictionary with timestamped server metrics
        """
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

        result = {
            "timestamp": timestamp,
            "server": {},
            "slots": [],
            "props": {},
            "metrics_available": True,
        }

        # Check if metrics collection is enabled
        if self.collect_metrics:
            # Get metrics
            metrics = self.get_metrics()
            if metrics:
                result["server"] = self._parse_metrics(metrics)
            else:
                # Metrics endpoint returned None (not supported)
                result["metrics_available"] = False
                result["server"] = {"error": "metrics_endpoint_not_available"}
        else:
            result["metrics_available"] = True  # Not collecting, so not an issue

        # Get slots
        slots = self.get_slots()
        if slots:
            result["slots"] = self._parse_slots(slots)

        # Get props
        props = self.get_props()
        if props:
            result["props"] = props

        return result

    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
        """Parse Prometheus-format metrics.

        Args:
            metrics: Raw metrics data (dict or string)

        Returns:
            Parsed metrics dictionary
        """
        result = {}

        if isinstance(metrics, dict):
            # Direct JSON format
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    result[key] = value
        elif isinstance(metrics, str):
            # Prometheus text format
            for line in metrics.strip().split("\n"):
                if line.startswith("#") or not line.strip():
                    continue

                # Parse metric line: metric_name value
                parts = line.rsplit(" ", 1)
                if len(parts) == 2:
                    name, value = parts
                    try:
                        result[name] = float(value)
                    except ValueError:
                        pass

        return result

    def _parse_slots(self, slots: Any) -> list:
        """Parse slot data.

        Args:
            slots: Raw slots data (list or dict)

        Returns:
            List of parsed slot dictionaries
        """
        result = []

        if isinstance(slots, list):
            for slot in slots:
                if isinstance(slot, dict):
                    result.append(
                        {
                            "id": slot.get("id", 0),
                            "task": slot.get("task", -1),
                            "n_tokens": slot.get("n_tokens", 0),
                            "n_prompt_tokens": slot.get("n_prompt_tokens", 0),
                            "n_gen_tokens": slot.get("n_gen_tokens", 0),
                            "progress": slot.get("progress", 0.0),
                            "state": slot.get("state", "idle"),
                            "prompt": slot.get("prompt", ""),
                            "generated": slot.get("generated", ""),
                        }
                    )
        elif isinstance(slots, dict):
            # Single slot format
            result.append(slots)

        return result


def format_metrics_display(metrics: Dict[str, Any]) -> str:
    """Format metrics for display.

    Args:
        metrics: Dictionary of metrics

    Returns:
        Formatted string for display
    """
    lines = []

    # Server metrics
    server = metrics.get("server", {})
    if server:
        prompt_tokens = server.get("prompt_tokens_total", 0)
        prompt_rate = server.get("prompt_tokens_seconds", 0)
        generated = server.get("tokens_predicted_total", 0)
        gen_rate = server.get("predicted_tokens_seconds", 0)

        lines.append(f"Prompt tokens:    {prompt_tokens:,} ({prompt_rate:,.0f}/s)")
        lines.append(f"Generated:        {generated:,} ({gen_rate:,.0f}/s)")
        lines.append(f"Requests:         {server.get('requests_processing', 0)} processing")

    # Slot info
    slots = metrics.get("slots", [])
    if slots:
        total_slots = len(slots)
        active_slots = sum(1 for s in slots if s.get("state") == "processing")
        avg_progress = (
            sum(s.get("progress", 0) for s in slots) / total_slots if total_slots else 0
        )

        lines.append(f"Active slots:     {active_slots}/{total_slots} ({avg_progress:.1%})")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test the collector
    collector = ServerMetricsCollector("http://localhost:8000")

    print("Collecting server metrics...")
    data = collector.collect()

    print("\nServer Metrics:")
    print(format_metrics_display(data))

    print("\nRaw Data:")
    import json

    print(json.dumps(data, indent=2))
