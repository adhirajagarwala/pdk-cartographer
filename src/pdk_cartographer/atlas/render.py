"""Render standard-cell atlas artifacts with the Python standard library.

The renderers are deterministic and report-oriented. They describe metadata
derived from synthetic Liberty fixtures only; they do not claim real Sky130
coverage or perform timing analysis.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from pdk_cartographer.atlas.models import CellRecord, StandardCellAtlas

CSV_COLUMNS = (
    "library_name",
    "cell_name",
    "area",
    "family",
    "drive_strength",
    "cell_kind",
    "input_pins",
    "output_pins",
    "clock_pins",
    "other_pins",
    "timing_arc_count",
)
SYNTHETIC_FIXTURE_NOTICE = (
    "This atlas is generated from synthetic educational Liberty fixtures, "
    "not real Sky130 data."
)


def render_atlas_markdown(atlas: StandardCellAtlas) -> str:
    """Return a deterministic Markdown report for a standard-cell atlas."""

    lines: list[str] = [
        "# M3 Fixture Standard Cell Atlas",
        "",
        SYNTHETIC_FIXTURE_NOTICE,
        "",
        "## Overview",
        "",
        f"- Libraries: {len(atlas.summary.library_names)}",
        f"- Cells: {atlas.summary.cell_count}",
        f"- Area min: {_format_optional_float(atlas.summary.area_min)}",
        f"- Area max: {_format_optional_float(atlas.summary.area_max)}",
        f"- Area mean: {_format_optional_float(atlas.summary.area_mean)}",
        "",
        "## Source Fixtures",
        "",
    ]
    if atlas.source_fixture_paths:
        lines.extend(f"- `{path}`" for path in atlas.source_fixture_paths)
    else:
        lines.append("- None recorded")

    lines.extend(
        [
            "",
            "## Library Summary",
            "",
            "| Library |",
            "| --- |",
        ]
    )
    lines.extend(
        f"| {_escape_markdown(library_name)} |"
        for library_name in atlas.summary.library_names
    )
    lines.extend(
        [
            "",
            "## Cell Inventory",
            "",
            "| Library | Cell | Area | Family | Drive | Kind | Inputs | "
            "Outputs | Clocks | Other Pins | Timing Arcs |",
            "| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | ---: |",
        ]
    )
    lines.extend(_cell_inventory_rows(atlas))
    lines.extend(
        [
            "",
            "## Area Ranking",
            "",
            "### Largest Cells",
            "",
            *_name_list(atlas.summary.largest_cells),
            "",
            "### Smallest Cells",
            "",
            *_name_list(atlas.summary.smallest_cells),
            "",
            "## Family Summary",
            "",
            "| Family | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(_count_rows(atlas.summary.family_counts))
    lines.extend(
        [
            "",
            "## Cell Kind Summary",
            "",
            "| Cell Kind | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(_count_rows(atlas.summary.cell_kind_counts))
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- This report uses synthetic educational Liberty fixtures only.",
            "- It does not contain or analyze real Sky130 Liberty files.",
            "- Cell kind classification is conservative metadata labeling, not "
            "timing or functional proof.",
            "- Timing arc counts are metadata counts only; no lookup-table "
            "exploration or static timing analysis is performed.",
            "",
        ]
    )
    return "\n".join(lines)


def write_atlas_csv(atlas: StandardCellAtlas, path: str | Path) -> None:
    """Write one deterministic CSV row per atlas cell record."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=CSV_COLUMNS,
            lineterminator="\n",
        )
        writer.writeheader()
        for cell in sorted(
            atlas.cells,
            key=lambda item: (item.library_name, item.cell_name),
        ):
            writer.writerow(_cell_csv_row(cell))


def write_atlas_json(atlas: StandardCellAtlas, path: str | Path) -> None:
    """Write deterministic atlas summary metadata as JSON."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "notice": SYNTHETIC_FIXTURE_NOTICE,
        "source_fixture_paths": list(atlas.source_fixture_paths),
        "summary": {
            "library_names": list(atlas.summary.library_names),
            "cell_count": atlas.summary.cell_count,
            "area_min": atlas.summary.area_min,
            "area_max": atlas.summary.area_max,
            "area_mean": atlas.summary.area_mean,
            "family_counts": atlas.summary.family_counts,
            "cell_kind_counts": atlas.summary.cell_kind_counts,
            "largest_cells": list(atlas.summary.largest_cells),
            "smallest_cells": list(atlas.summary.smallest_cells),
        },
    }
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _cell_inventory_rows(atlas: StandardCellAtlas) -> list[str]:
    return [
        "| "
        + " | ".join(
            [
                _escape_markdown(cell.library_name),
                _escape_markdown(cell.cell_name),
                _format_optional_float(cell.area),
                _escape_markdown(cell.family),
                _escape_markdown(cell.drive_strength or ""),
                _escape_markdown(cell.cell_kind),
                _escape_markdown(_join_tuple(cell.input_pins)),
                _escape_markdown(_join_tuple(cell.output_pins)),
                _escape_markdown(_join_tuple(cell.clock_pins)),
                _escape_markdown(_join_tuple(cell.other_pins)),
                str(cell.timing_arc_count),
            ]
        )
        + " |"
        for cell in sorted(
            atlas.cells,
            key=lambda item: (item.library_name, item.cell_name),
        )
    ]


def _count_rows(counts: dict[str, int]) -> list[str]:
    if not counts:
        return ["| None | 0 |"]
    return [
        f"| {_escape_markdown(name)} | {count} |"
        for name, count in sorted(counts.items())
    ]


def _name_list(names: tuple[str, ...]) -> list[str]:
    if not names:
        return ["- None"]
    return [f"- `{name}`" for name in names]


def _cell_csv_row(cell: CellRecord) -> dict[str, Any]:
    return {
        "library_name": cell.library_name,
        "cell_name": cell.cell_name,
        "area": _format_optional_float(cell.area),
        "family": cell.family,
        "drive_strength": cell.drive_strength or "",
        "cell_kind": cell.cell_kind,
        "input_pins": _join_tuple(cell.input_pins),
        "output_pins": _join_tuple(cell.output_pins),
        "clock_pins": _join_tuple(cell.clock_pins),
        "other_pins": _join_tuple(cell.other_pins),
        "timing_arc_count": cell.timing_arc_count,
    }


def _join_tuple(values: tuple[str, ...]) -> str:
    return ";".join(values)


def _format_optional_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6g}"


def _escape_markdown(value: str) -> str:
    return value.replace("|", "\\|")
