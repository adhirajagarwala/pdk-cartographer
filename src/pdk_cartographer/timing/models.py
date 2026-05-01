"""Typed models for the fixture timing-table explorer.

These records describe timing-table structure from synthetic Liberty fixtures.
They are metadata summaries only; they do not imply static timing analysis,
interpolation, or real Sky130 characterization.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TimingTableRecord:
    """One flattened timing-table record for report generation."""

    library_name: str
    cell_name: str
    pin_name: str
    related_pin: str | None
    timing_type: str | None
    timing_sense: str | None
    table_kind: str
    template_name: str | None
    variable_1: str | None
    variable_2: str | None
    index_1_count: int
    index_2_count: int
    row_count: int
    column_count: int
    value_min: float | None
    value_max: float | None


@dataclass(frozen=True)
class TimingExplorerSummary:
    """Aggregate counts for a timing-table explorer snapshot."""

    table_count: int
    table_kind_counts: dict[str, int] = field(default_factory=dict)
    timing_type_counts: dict[str, int] = field(default_factory=dict)
    timing_sense_counts: dict[str, int] = field(default_factory=dict)
    dimension_counts: dict[str, int] = field(default_factory=dict)
    libraries: tuple[str, ...] = ()
    cells: tuple[str, ...] = ()


@dataclass(frozen=True)
class TimingTableExplorer:
    """Deterministic timing-table explorer output."""

    records: tuple[TimingTableRecord, ...]
    summary: TimingExplorerSummary
    source_fixture_paths: tuple[str, ...] = ()
