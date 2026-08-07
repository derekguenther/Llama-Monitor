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
        # Previous cumulative values for instantaneous rate calculation
        self._prev_prompt_tokens_total = None
        self._prev_prompt_seconds_total = None
        self._prev_tokens_predicted_total = None
        self._prev_tokens_predicted_seconds_total = None
        self._prev_timestamp = None

    def _make_request(self, endpoint: str) -> Optional[Any]:
        """Make HTTP request to server endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Response data (dict or text), or None if request failed
        """
        url = f"{self.server_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            # Prometheus format returns text/plain, JSON endpoints return application/json
            if 'text/plain' in content_type or 'text/plain' in content_type.lower():
                return response.text
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
                # Calculate instantaneous token rates from cumulative deltas
                self._compute_instant_rates(result["server"])
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
            # Strip out the massive chat_template (Jinja2 template) — not used by frontend
            if isinstance(props, dict):
                props = {k: v for k, v in props.items() if k != "chat_template"}
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
                    # Strip llamacpp: prefix if present
                    clean_key = key.replace("llamacpp:", "")
                    result[clean_key] = value
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
                        # Strip llamacpp: prefix if present
                        clean_name = name.replace("llamacpp:", "")
                        # Strip labels from metric name (e.g., requests_processing{foo="bar"} -> requests_processing)
                        if "{" in clean_name:
                            clean_name = clean_name.split("{")[0]
                        result[clean_name] = float(value)
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

        # Normalize input: wrap single dict in a list so all paths use the same loop
        slot_list = slots if isinstance(slots, list) else ([slots] if isinstance(slots, dict) else [])

        for slot in slot_list:
            if not isinstance(slot, dict):
                continue

            # Convert None to 0/default for numeric fields
            def _v(key, default=0):
                val = slot.get(key, default)
                return val if val is not None else default

            slot_state = slot.get("state")
            progress = slot.get("progress")
            n_prompt_tokens = _v("n_prompt_tokens")
            n_prompt_tokens_processed = _v("n_prompt_tokens_processed")
            n_gen_tokens = _v("n_gen_tokens")

            # Normalize state: None (from JSON null) means idle
            if slot_state is None:
                slot_state = "idle"

            # Calculate progress when actively processing
            if progress is None:
                if slot_state == "processing" and n_prompt_tokens > 0:
                    progress = n_prompt_tokens_processed / n_prompt_tokens
                else:
                    progress = 0.0

            n_cache = _v("n_prompt_tokens_cache")
            n_tokens = n_cache + n_prompt_tokens_processed + n_gen_tokens

            result.append(
                {
                    "id": _v("id"),
                    "task": max(-1, _v("task", -1)),
                    "n_tokens": max(0, n_tokens),
                    "n_prompt_tokens": max(0, n_prompt_tokens),
                    "n_gen_tokens": max(0, n_gen_tokens),
                    "n_prompt_tokens_processed": max(0, n_prompt_tokens_processed),
                    "progress": max(0.0, min(1.0, progress)),
                    "state": slot_state,
                    "prompt": slot.get("prompt", ""),
                    "generated": slot.get("generated", ""),
                    "next_token": slot.get("next_token", []),
                }
            )

        return result

    def _compute_instant_rates(self, server: Dict[str, Any]) -> None:
        """Calculate instantaneous token rates from cumulative delta.

        The /metrics endpoint provides cumulative averages (total/seconds).
        This method tracks deltas between consecutive poll cycles to compute
        instantaneous rates that reflect current activity.

        Adds prompt_tokens_seconds_instant and predicted_tokens_seconds_instant
        to the server dict in-place.
        """
        now = time.time()
        pt = server.get("prompt_tokens_total")
        pst = server.get("prompt_seconds_total")
        tt = server.get("tokens_predicted_total")
        tst = server.get("tokens_predicted_seconds_total")

        if None in (pt, pst, tt, tst) or self._prev_timestamp is None:
            # First call or missing data — store baseline, no rate yet
            self._prev_prompt_tokens_total = pt
            self._prev_prompt_seconds_total = pst
            self._prev_tokens_predicted_total = tt
            self._prev_tokens_predicted_seconds_total = tst
            self._prev_timestamp = now
            server["prompt_tokens_seconds_instant"] = 0.0
            server["predicted_tokens_seconds_instant"] = 0.0
            return

        dt = now - self._prev_timestamp
        dpt = pt - self._prev_prompt_tokens_total
        dpst = pst - self._prev_prompt_seconds_total
        dtt = tt - self._prev_tokens_predicted_total
        dtst = tst - self._prev_tokens_predicted_seconds_total

        # Update stored prev values for next cycle
        self._prev_prompt_tokens_total = pt
        self._prev_prompt_seconds_total = pst
        self._prev_tokens_predicted_total = tt
        self._prev_tokens_predicted_seconds_total = tst
        self._prev_timestamp = now

        prompt_rate = dpt / dt if dt > 0 and dpt >= 0 else 0.0
        gen_rate = dtt / dt if dt > 0 and dtt >= 0 else 0.0

        server["prompt_tokens_seconds_instant"] = round(prompt_rate, 2)
        server["predicted_tokens_seconds_instant"] = round(gen_rate, 2)


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
