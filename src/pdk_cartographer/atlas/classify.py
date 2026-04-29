"""Conservative standard-cell classification helpers.

These helpers are fixture-oriented and intentionally generic. They recognize
common standard-cell-style names such as ``INV_X1`` or ``DFF_X1`` without
encoding real Sky130 library conventions. Classification is best-effort
metadata labeling for reports, not electrical or timing analysis.
"""

from __future__ import annotations

import re
from collections.abc import Collection, Mapping

DRIVE_SUFFIX_RE = re.compile(r"^(?P<family>.+)_(?P<drive>X[0-9]+(?:P[0-9]+)?)$")
CLOCK_PIN_NAMES = {"CLK", "CK", "CLOCK"}
SEQUENTIAL_NAME_MARKERS = ("DFF", "LATCH")


def classify_cell_family(cell_name: str) -> str:
    """Return a generic cell family name with a simple drive suffix removed.

    The rule only strips suffixes like ``_X1`` or ``_X16``. It deliberately
    avoids process- or vendor-specific naming knowledge, so unfamiliar names
    are returned unchanged.
    """

    normalized_name = cell_name.strip()
    drive_match = DRIVE_SUFFIX_RE.match(normalized_name)
    if drive_match is None:
        return normalized_name
    return drive_match.group("family")


def extract_drive_strength(cell_name: str) -> str | None:
    """Return a generic drive suffix such as ``X1`` when one is present.

    Only simple ``_X<number>`` style suffixes are recognized. More specialized
    naming schemes are intentionally left for later, fixture-backed work.
    """

    drive_match = DRIVE_SUFFIX_RE.match(cell_name.strip())
    if drive_match is None:
        return None
    return drive_match.group("drive")


def is_clock_like_pin(pin_name: str) -> bool:
    """Return whether a pin name is a conservative clock-like indicator."""

    return pin_name.strip().upper() in CLOCK_PIN_NAMES


def classify_cell_kind(
    cell_name: str,
    input_pins: Collection[str],
    output_pins: Collection[str],
    clock_pins: Collection[str],
    timing_arc_count: int,
    functions: Mapping[str, str],
) -> str:
    """Classify a cell as ``sequential``, ``combinational``, or ``unknown``.

    Sequential classification uses conservative structural hints: clock-like
    pins, explicit clock pin groups, or generic ``DFF``/``LATCH`` name markers.
    Combinational classification requires at least one output function and no
    sequential indicators. Timing arc count is accepted for future summarizer
    integration, but it is not enough by itself to classify a cell.
    """

    del timing_arc_count

    normalized_name = cell_name.upper()
    has_clock_pin = any(is_clock_like_pin(pin_name) for pin_name in input_pins)
    has_clock_pin = has_clock_pin or any(
        is_clock_like_pin(pin_name) for pin_name in clock_pins
    )
    has_sequential_name = any(
        marker in normalized_name for marker in SEQUENTIAL_NAME_MARKERS
    )
    if has_clock_pin or has_sequential_name:
        return "sequential"

    output_pin_names = set(output_pins)
    has_output_function = any(
        pin_name in output_pin_names and function.strip()
        for pin_name, function in functions.items()
    )
    if has_output_function:
        return "combinational"

    return "unknown"
