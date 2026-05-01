"""Summarize fixture Liberty timing-table structure.

The timing explorer reports table shape, axis metadata, arc metadata, and value
ranges. It deliberately does not interpolate values or perform static timing
analysis.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from pdk_cartographer.liberty.models import Library, TimingArc, TimingTable
from pdk_cartographer.timing.models import (
    TimingExplorerSummary,
    TimingTableExplorer,
    TimingTableRecord,
)


def build_timing_table_explorer(
    libraries: Iterable[Library],
    source_fixture_paths: Iterable[str] = (),
) -> TimingTableExplorer:
    """Return a deterministic timing-table explorer for parsed libraries."""

    sorted_libraries = sorted(libraries, key=lambda library: library.name)
    records = tuple(
        _build_table_record(
            library=library,
            cell_name=cell_name,
            pin_name=pin_name,
            arc=arc,
            table=table,
        )
        for library in sorted_libraries
        for cell_name, cell in sorted(library.cells.items())
        for pin_name, pin in sorted(cell.pins.items())
        for arc in pin.timing_arcs
        for table in arc.timing_tables
    )
    return TimingTableExplorer(
        records=records,
        summary=_build_summary(records),
        source_fixture_paths=tuple(sorted(source_fixture_paths)),
    )


def _build_table_record(
    *,
    library: Library,
    cell_name: str,
    pin_name: str,
    arc: TimingArc,
    table: TimingTable,
) -> TimingTableRecord:
    template = (
        library.lookup_table_templates.get(table.template_name)
        if table.template_name is not None
        else None
    )
    flattened_values = tuple(value for row in table.values for value in row)
    column_count = max((len(row) for row in table.values), default=0)

    return TimingTableRecord(
        library_name=library.name,
        cell_name=cell_name,
        pin_name=pin_name,
        related_pin=arc.related_pin,
        timing_type=arc.timing_type,
        timing_sense=arc.timing_sense,
        table_kind=table.table_kind,
        template_name=table.template_name,
        variable_1=template.variable_1 if template is not None else None,
        variable_2=template.variable_2 if template is not None else None,
        index_1_count=len(table.index_1),
        index_2_count=len(table.index_2),
        row_count=len(table.values),
        column_count=column_count,
        value_min=min(flattened_values) if flattened_values else None,
        value_max=max(flattened_values) if flattened_values else None,
    )


def _build_summary(records: Iterable[TimingTableRecord]) -> TimingExplorerSummary:
    table_records = tuple(records)
    table_kind_counts = Counter(record.table_kind for record in table_records)
    timing_type_counts = Counter(
        record.timing_type for record in table_records if record.timing_type is not None
    )
    timing_sense_counts = Counter(
        record.timing_sense
        for record in table_records
        if record.timing_sense is not None
    )
    dimension_counts = Counter(_dimension_label(record) for record in table_records)

    return TimingExplorerSummary(
        table_count=len(table_records),
        table_kind_counts=dict(sorted(table_kind_counts.items())),
        timing_type_counts=dict(sorted(timing_type_counts.items())),
        timing_sense_counts=dict(sorted(timing_sense_counts.items())),
        dimension_counts=dict(sorted(dimension_counts.items())),
        libraries=tuple(sorted({record.library_name for record in table_records})),
        cells=tuple(
            sorted(
                {
                    f"{record.library_name}/{record.cell_name}"
                    for record in table_records
                }
            )
        ),
    )


def _dimension_label(record: TimingTableRecord) -> str:
    return f"{record.row_count}x{record.column_count}"
