"""Render timing-table explorer artifacts with the Python standard library."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from pdk_cartographer.timing.models import TimingTableExplorer, TimingTableRecord

CSV_COLUMNS = (
    "library_name",
    "cell_name",
    "pin_name",
    "related_pin",
    "timing_type",
    "timing_sense",
    "table_kind",
    "template_name",
    "variable_1",
    "variable_2",
    "index_1_count",
    "index_2_count",
    "row_count",
    "column_count",
    "value_min",
    "value_max",
)
SYNTHETIC_TIMING_NOTICE = (
    "This report is generated from synthetic educational Liberty fixtures, "
    "not real Sky130 data."
)


def render_timing_explorer_markdown(explorer: TimingTableExplorer) -> str:
    """Return a deterministic Markdown timing-table explorer report."""

    lines: list[str] = [
        "# M4 Fixture Timing Table Explorer",
        "",
        SYNTHETIC_TIMING_NOTICE,
        "",
        "## Overview",
        "",
        f"- Libraries: {len(explorer.summary.libraries)}",
        f"- Cells: {len(explorer.summary.cells)}",
        f"- Timing tables: {explorer.summary.table_count}",
        "",
        "## Source Fixtures",
        "",
    ]
    if explorer.source_fixture_paths:
        lines.extend(f"- `{path}`" for path in explorer.source_fixture_paths)
    else:
        lines.append("- None recorded")

    lines.extend(
        [
            "",
            "## Timing Table Inventory",
            "",
            "| Library | Cell | Pin | Related Pin | Type | Sense | Table | "
            "Template | Axis 1 | Axis 2 | Rows | Columns | Min | Max |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | "
            "---: | ---: | ---: | ---: |",
        ]
    )
    lines.extend(_record_rows(explorer.records))
    lines.extend(
        [
            "",
            "## Table Kind Summary",
            "",
            "| Table Kind | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(_count_rows(explorer.summary.table_kind_counts))
    lines.extend(
        [
            "",
            "## Axis and Dimension Summary",
            "",
            "| Dimension | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(_count_rows(explorer.summary.dimension_counts))
    lines.extend(
        [
            "",
            "## Timing Arc Summary",
            "",
            "### Timing Types",
            "",
            "| Timing Type | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(_count_rows(explorer.summary.timing_type_counts))
    lines.extend(
        [
            "",
            "### Timing Senses",
            "",
            "| Timing Sense | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(_count_rows(explorer.summary.timing_sense_counts))
    lines.extend(
        [
            "",
            "## What This Does Not Do",
            "",
            "- M4 does not perform static timing analysis.",
            "- M4 does not interpolate timing values.",
            "- M4 does not model physical layout, routing, parasitics, "
            "or signoff timing.",
            "",
            "## Limitations",
            "",
            "- This report uses synthetic educational Liberty fixtures only.",
            "- It does not contain or analyze real Sky130 Liberty files.",
            "- Values are reported as table-shape metadata, not validated delays.",
            "- Only the small fixture-backed timing-table subset is supported.",
            "",
        ]
    )
    return "\n".join(lines)


def write_timing_tables_csv(explorer: TimingTableExplorer, path: str | Path) -> None:
    """Write one deterministic CSV row per timing-table record."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=CSV_COLUMNS,
            lineterminator="\n",
        )
        writer.writeheader()
        for record in _sorted_records(explorer.records):
            writer.writerow(_record_csv_row(record))


def write_timing_summary_json(
    explorer: TimingTableExplorer,
    path: str | Path,
) -> None:
    """Write deterministic timing-table summary metadata as JSON."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "notice": SYNTHETIC_TIMING_NOTICE,
        "source_fixture_paths": list(explorer.source_fixture_paths),
        "summary": {
            "table_count": explorer.summary.table_count,
            "table_kind_counts": explorer.summary.table_kind_counts,
            "timing_type_counts": explorer.summary.timing_type_counts,
            "timing_sense_counts": explorer.summary.timing_sense_counts,
            "dimension_counts": explorer.summary.dimension_counts,
            "libraries": list(explorer.summary.libraries),
            "cells": list(explorer.summary.cells),
        },
        "records": [
            _record_json(record) for record in _sorted_records(explorer.records)
        ],
    }
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _record_rows(records: tuple[TimingTableRecord, ...]) -> list[str]:
    return [
        "| "
        + " | ".join(
            [
                _escape_markdown(record.library_name),
                _escape_markdown(record.cell_name),
                _escape_markdown(record.pin_name),
                _escape_markdown(record.related_pin or ""),
                _escape_markdown(record.timing_type or ""),
                _escape_markdown(record.timing_sense or ""),
                _escape_markdown(record.table_kind),
                _escape_markdown(record.template_name or ""),
                _escape_markdown(record.variable_1 or ""),
                _escape_markdown(record.variable_2 or ""),
                str(record.row_count),
                str(record.column_count),
                _format_optional_float(record.value_min),
                _format_optional_float(record.value_max),
            ]
        )
        + " |"
        for record in _sorted_records(records)
    ]


def _count_rows(counts: dict[str, int]) -> list[str]:
    if not counts:
        return ["| None | 0 |"]
    return [
        f"| {_escape_markdown(name)} | {count} |"
        for name, count in sorted(counts.items())
    ]


def _record_csv_row(record: TimingTableRecord) -> dict[str, Any]:
    return {
        "library_name": record.library_name,
        "cell_name": record.cell_name,
        "pin_name": record.pin_name,
        "related_pin": record.related_pin or "",
        "timing_type": record.timing_type or "",
        "timing_sense": record.timing_sense or "",
        "table_kind": record.table_kind,
        "template_name": record.template_name or "",
        "variable_1": record.variable_1 or "",
        "variable_2": record.variable_2 or "",
        "index_1_count": record.index_1_count,
        "index_2_count": record.index_2_count,
        "row_count": record.row_count,
        "column_count": record.column_count,
        "value_min": _format_optional_float(record.value_min),
        "value_max": _format_optional_float(record.value_max),
    }


def _record_json(record: TimingTableRecord) -> dict[str, Any]:
    return {
        "library_name": record.library_name,
        "cell_name": record.cell_name,
        "pin_name": record.pin_name,
        "related_pin": record.related_pin,
        "timing_type": record.timing_type,
        "timing_sense": record.timing_sense,
        "table_kind": record.table_kind,
        "template_name": record.template_name,
        "variable_1": record.variable_1,
        "variable_2": record.variable_2,
        "index_1_count": record.index_1_count,
        "index_2_count": record.index_2_count,
        "row_count": record.row_count,
        "column_count": record.column_count,
        "value_min": record.value_min,
        "value_max": record.value_max,
    }


def _sorted_records(
    records: tuple[TimingTableRecord, ...],
) -> tuple[TimingTableRecord, ...]:
    return tuple(
        sorted(
            records,
            key=lambda record: (
                record.library_name,
                record.cell_name,
                record.pin_name,
                record.related_pin or "",
                record.table_kind,
                record.template_name or "",
            ),
        )
    )


def _format_optional_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6g}"


def _escape_markdown(value: str) -> str:
    return value.replace("|", "\\|")
