"""Dataclasses for the M1 Liberty fixture subset."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TimingArc:
    """Minimal timing arc metadata captured from fixture timing groups."""

    related_pin: str | None = None
    timing_sense: str | None = None
    timing_type: str | None = None


@dataclass(frozen=True)
class Pin:
    """A Liberty pin with simple scalar attributes."""

    name: str
    direction: str | None = None
    function: str | None = None
    capacitance: float | None = None
    timing_arcs: tuple[TimingArc, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Cell:
    """A Liberty cell with area and pins."""

    name: str
    area: float | None = None
    pins: tuple[Pin, ...] = field(default_factory=tuple)

    def get_pin(self, name: str) -> Pin:
        """Return a pin by name or raise KeyError."""

        for pin in self.pins:
            if pin.name == name:
                return pin
        raise KeyError(name)


@dataclass(frozen=True)
class Library:
    """A parsed Liberty library from the M1 fixture subset."""

    name: str
    cells: tuple[Cell, ...] = field(default_factory=tuple)

    def get_cell(self, name: str) -> Cell:
        """Return a cell by name or raise KeyError."""

        for cell in self.cells:
            if cell.name == name:
                return cell
        raise KeyError(name)
