"""Typed output models for the standard-cell atlas layer.

The atlas models describe summaries derived from parsed Liberty fixture data.
They are intentionally small and deterministic, and they do not imply coverage
of a real PDK or full Liberty semantics.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CellRecord:
    """Flattened metadata for one parsed standard-cell-style Liberty cell."""

    library_name: str
    cell_name: str
    area: float | None
    family: str
    drive_strength: str | None
    cell_kind: str
    input_pins: tuple[str, ...] = ()
    output_pins: tuple[str, ...] = ()
    clock_pins: tuple[str, ...] = ()
    other_pins: tuple[str, ...] = ()
    functions: dict[str, str] = field(default_factory=dict)
    pin_capacitance: dict[str, float] = field(default_factory=dict)
    timing_arc_count: int = 0


@dataclass(frozen=True)
class LibraryAtlasSummary:
    """Aggregate metadata for one or more parsed Liberty libraries."""

    library_names: tuple[str, ...]
    cell_count: int
    area_min: float | None
    area_max: float | None
    area_mean: float | None
    family_counts: dict[str, int] = field(default_factory=dict)
    cell_kind_counts: dict[str, int] = field(default_factory=dict)
    largest_cells: tuple[str, ...] = ()
    smallest_cells: tuple[str, ...] = ()


@dataclass(frozen=True)
class StandardCellAtlas:
    """A deterministic atlas snapshot produced from fixture Liberty inputs."""

    cells: tuple[CellRecord, ...]
    summary: LibraryAtlasSummary
    source_fixture_paths: tuple[str, ...] = ()
