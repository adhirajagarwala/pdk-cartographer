"""Typed models produced by the fixture-first Liberty parser.

These dataclasses are intentionally small and atlas-oriented. They preserve the
simple Liberty metadata needed by the synthetic fixtures without claiming full
Liberty coverage or real Sky130 ingestion.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeAlias

LibertyScalarValue: TypeAlias = str | float
LibertyModelValue: TypeAlias = LibertyScalarValue | tuple[LibertyScalarValue, ...]
LibertyAttributes: TypeAlias = dict[str, LibertyModelValue]


@dataclass(frozen=True)
class LookupTableTemplate:
    """A small Liberty lookup-table template captured from fixture data."""

    name: str
    variable_1: str | None = None
    variable_2: str | None = None
    index_1: tuple[float, ...] = ()
    index_2: tuple[float, ...] = ()


@dataclass(frozen=True)
class TimingTable:
    """A parsed timing lookup table from the fixture Liberty subset."""

    table_kind: str
    template_name: str | None = None
    index_1: tuple[float, ...] = ()
    index_2: tuple[float, ...] = ()
    values: tuple[tuple[float, ...], ...] = ()


@dataclass(frozen=True)
class TimingArc:
    """Minimal timing arc metadata captured from fixture timing groups."""

    related_pin: str | None = None
    timing_sense: str | None = None
    timing_type: str | None = None
    attributes: LibertyAttributes = field(default_factory=dict)
    timing_tables: tuple[TimingTable, ...] = ()


@dataclass(frozen=True)
class Pin:
    """A Liberty pin with simple scalar attributes."""

    name: str
    direction: str | None = None
    function: str | None = None
    capacitance: float | None = None
    attributes: LibertyAttributes = field(default_factory=dict)
    timing_arcs: list[TimingArc] = field(default_factory=list)


@dataclass(frozen=True)
class Cell:
    """A Liberty cell with area and pins."""

    name: str
    area: float | None = None
    pins: dict[str, Pin] = field(default_factory=dict)
    attributes: LibertyAttributes = field(default_factory=dict)

    def get_pin(self, name: str) -> Pin:
        """Return a pin by name or raise KeyError."""

        return self.pins[name]


@dataclass(frozen=True)
class Library:
    """A parsed Liberty library from the synthetic fixture subset."""

    name: str
    cells: dict[str, Cell] = field(default_factory=dict)
    attributes: LibertyAttributes = field(default_factory=dict)
    lookup_table_templates: dict[str, LookupTableTemplate] = field(
        default_factory=dict
    )

    def get_cell(self, name: str) -> Cell:
        """Return a cell by name or raise KeyError."""

        return self.cells[name]
