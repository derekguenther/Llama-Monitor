"""Shared helpers for llama-raw-capture-tool.

Small, self-contained utilities used by both ``capture.py`` and
``postprocess.py``. Kept separate from the main Llama Monitor project.

The two wall-clock stamp formats defined here are the canonical capture-side
timestamps described in the spec:

- ``wallclock_iso``: ISO 8601 extended, local + TZ offset, ms precision.
- ``wallclock_epoch_us``: Unix-epoch microseconds from ``time.time_ns() // 1000``.
"""

from __future__ import annotations

import time
from typing import Any, Dict


def wallclock_stamp() -> Dict[str, Any]:
    """Return a dict with the canonical capture-side wall-clock stamps.

    Both stamps derive from the same ``system_clock`` family as the log's
    ``t_us()``, giving a lossless, deterministic input for the post-processor.

    Returns:
        {"wallclock_iso": ..., "wallclock_epoch_us": ...}
    """
    now_us = time.time_ns() // 1000
    return {
        "wallclock_iso": iso_from_epoch_us(now_us),
        "wallclock_epoch_us": now_us,
    }


def iso_from_epoch_us(epoch_us: int) -> str:
    """Convert a Unix-epoch microsecond value to an ISO 8601 local + TZ string.

    Uses the local timezone offset and millisecond precision.
    """
    epoch_s = epoch_us // 1_000_000
    ms = (epoch_us % 1_000_000) // 1000
    t = time.localtime(epoch_s)
    offset_sec = time.timezone if not time.daylight else time.altzone
    # Python's timezone values are seconds WEST of UTC; negate for ISO offset.
    offset_min = -offset_sec // 60
    sign = "+" if offset_min >= 0 else "-"
    offset_min = abs(offset_min)
    tz = f"{sign}{offset_min // 60:02d}:{offset_min % 60:02d}"
    return time.strftime("%Y-%m-%dT%H:%M:%S", t) + f".{ms:03d}{tz}"


def iso_from_epoch_s(epoch_s: float) -> str:
    """Convert a Unix-epoch (seconds, may be fractional) to ISO 8601 string."""
    return iso_from_epoch_us(int(epoch_s * 1_000_000))
