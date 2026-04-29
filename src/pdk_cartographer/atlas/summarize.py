"""Build deterministic standard-cell atlas summaries from parsed Liberty data.

The summarizer flattens the small M2 Liberty model into portfolio-friendly
metadata records. It counts pins, functions, areas, and timing arc metadata, but
it deliberately does not perform static timing analysis or interpret Liberty
lookup tables.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from pdk_cartographer.atlas.classify import (
    classify_cell_family,
    classify_cell_kind,
    extract_drive_strength,
    is_clock_like_pin,
)
from pdk_cartographer.atlas.models import (
    CellRecord,
    LibraryAtlasSummary,
    StandardCellAtlas,
)
from pdk_cartographer.liberty.models import Cell, Library, Pin

AREA_RANK_LIMIT = 5


def build_cell_record(library_name: str, cell: Cell) -> CellRecord:
    """Return one deterministic atlas record for a parsed Liberty cell."""

    pins = tuple(pin for _, pin in sorted(cell.pins.items()))
    input_pins = _pin_names_by_direction(pins, "input")
    output_pins = _pin_names_by_direction(pins, "output")
    clock_pins = tuple(pin.name for pin in pins if is_clock_like_pin(pin.name))
    known_pin_names = set(input_pins) | set(output_pins) | set(clock_pins)
    other_pins = tuple(pin.name for pin in pins if pin.name not in known_pin_names)
    functions = {
        pin.name: pin.function
        for pin in pins
        if pin.direction == "output" and pin.function is not None
    }
    pin_capacitance = {
        pin.name: pin.capacitance for pin in pins if pin.capacitance is not None
    }
    timing_arc_count = sum(len(pin.timing_arcs) for pin in pins)
    family = classify_cell_family(cell.name)
    drive_strength = extract_drive_strength(cell.name)
    cell_kind = classify_cell_kind(
        cell.name,
        input_pins=input_pins,
        output_pins=output_pins,
        clock_pins=clock_pins,
        timing_arc_count=timing_arc_count,
        functions=functions,
    )

    return CellRecord(
        library_name=library_name,
        cell_name=cell.name,
        area=cell.area,
        family=family,
        drive_strength=drive_strength,
        cell_kind=cell_kind,
        input_pins=input_pins,
        output_pins=output_pins,
        clock_pins=clock_pins,
        other_pins=other_pins,
        functions=functions,
        pin_capacitance=pin_capacitance,
        timing_arc_count=timing_arc_count,
    )


def build_standard_cell_atlas(
    libraries: Iterable[Library],
    source_fixture_paths: Iterable[str] = (),
) -> StandardCellAtlas:
    """Return a deterministic atlas for one or more parsed Liberty libraries."""

    sorted_libraries = sorted(libraries, key=lambda library: library.name)
    cells = tuple(
        build_cell_record(library.name, cell)
        for library in sorted_libraries
        for _, cell in sorted(library.cells.items())
    )
    return StandardCellAtlas(
        cells=cells,
        summary=build_library_atlas_summary(cells),
        source_fixture_paths=tuple(sorted(source_fixture_paths)),
    )


def build_library_atlas_summary(
    cells: Iterable[CellRecord],
) -> LibraryAtlasSummary:
    """Return aggregate atlas metadata for deterministic report generation."""

    cell_records = tuple(cells)
    area_records = tuple(cell for cell in cell_records if cell.area is not None)
    areas = tuple(cell.area for cell in area_records if cell.area is not None)
    family_counts = Counter(cell.family for cell in cell_records)
    cell_kind_counts = Counter(cell.cell_kind for cell in cell_records)

    return LibraryAtlasSummary(
        library_names=tuple(sorted({cell.library_name for cell in cell_records})),
        cell_count=len(cell_records),
        area_min=min(areas) if areas else None,
        area_max=max(areas) if areas else None,
        area_mean=(sum(areas) / len(areas)) if areas else None,
        family_counts=dict(sorted(family_counts.items())),
        cell_kind_counts=dict(sorted(cell_kind_counts.items())),
        largest_cells=_rank_cells_by_area(area_records, reverse=True),
        smallest_cells=_rank_cells_by_area(area_records, reverse=False),
    )


def _pin_names_by_direction(pins: Iterable[Pin], direction: str) -> tuple[str, ...]:
    return tuple(pin.name for pin in pins if pin.direction == direction)


def _rank_cells_by_area(
    cells: Iterable[CellRecord],
    *,
    reverse: bool,
) -> tuple[str, ...]:
    ranked = sorted(
        cells,
        key=lambda cell: (
            -(cell.area or 0.0) if reverse else cell.area or 0.0,
            cell.library_name,
            cell.cell_name,
        ),
    )
    return tuple(cell.cell_name for cell in ranked[:AREA_RANK_LIMIT])
