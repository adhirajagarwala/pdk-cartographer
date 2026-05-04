"""Read-only parser compatibility reports for selected Sky130 Liberty files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pdk_cartographer.liberty import parse_liberty_file
from pdk_cartographer.liberty.models import Library
from pdk_cartographer.pdk.manifest import (
    build_liberty_manifest,
    select_target_subset,
)
from pdk_cartographer.pdk.models import LibertyFile, PdkRoot

PARSER_SCOPE_WARNING = (
    "The current parser is a fixture-first educational Liberty subset parser. "
    "These results are compatibility probes only and do not claim full Liberty "
    "support or production signoff readiness."
)
COMPATIBILITY_LIMITATIONS = (
    "The probe uses a selected max-3 real Sky130 Liberty subset, records compact "
    "success/failure diagnostics, and never copies or emits raw Liberty text."
)
MAX_ERROR_MESSAGE_CHARS = 500


@dataclass(frozen=True)
class ParseCompatibilityRecord:
    """One parser compatibility result for a selected Liberty file."""

    relative_path: str
    variant: str | None
    library_family: str | None
    corner: str | None
    size_bytes: int
    success: bool
    library_name: str | None = None
    cell_count: int | None = None
    timing_table_count: int | None = None
    error_class: str | None = None
    error_message: str | None = None


def probe_parser_compatibility(pdk: PdkRoot) -> tuple[ParseCompatibilityRecord, ...]:
    """Attempt to parse the selected Sky130 Liberty target subset."""

    return tuple(_probe_liberty_file(liberty) for liberty in select_target_subset(pdk))


def build_parse_compatibility_payload(
    pdk: PdkRoot,
    *,
    root_display: str,
    root_env_var: str,
) -> dict[str, Any]:
    """Return deterministic parser compatibility report metadata."""

    records = probe_parser_compatibility(pdk)
    success_count = sum(1 for record in records if record.success)
    failure_count = len(records) - success_count
    return {
        "parser_scope_warning": PARSER_SCOPE_WARNING,
        "limitations": COMPATIBILITY_LIMITATIONS,
        "pdk_root": {
            "display": root_display,
            "env_var": root_env_var,
        },
        "selected_files": [record.relative_path for record in records],
        "success_count": success_count,
        "failure_count": failure_count,
        "compatibility_results": [_record_json(record) for record in records],
    }


def write_parse_compatibility_json(
    pdk: PdkRoot,
    path: str | Path,
    *,
    root_display: str,
    root_env_var: str,
) -> None:
    """Write parser compatibility results without raw Liberty contents."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_parse_compatibility_payload(
        pdk,
        root_display=root_display,
        root_env_var=root_env_var,
    )
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def render_sky130_readonly_report_markdown(
    pdk: PdkRoot,
    *,
    root_display: str,
    root_env_var: str,
) -> str:
    """Return the generated M5 read-only Sky130 ingestion report."""

    manifest = build_liberty_manifest(
        pdk,
        root_display=root_display,
        root_env_var=root_env_var,
    )
    compatibility = build_parse_compatibility_payload(
        pdk,
        root_display=root_display,
        root_env_var=root_env_var,
    )
    lines = [
        "# M5 Sky130 Read-Only Ingestion Report",
        "",
        "This report is generated from an external Sky130 PDK installation. "
        "Raw PDK files are not committed to this repository.",
        "",
        "M5 is read-only exploration of Liberty metadata and parser "
        "compatibility. It is not production signoff, static timing analysis, "
        "or a claim of full Liberty support.",
        "",
        "## PDK Root Strategy",
        "",
        f"- Preferred environment variable: `{root_env_var}`",
        f"- Display root: `{root_display}`",
        "- Generated artifacts store relative paths from the configured PDK root.",
        "- Raw Liberty contents are not copied, embedded, or summarized as "
        "source text.",
        "",
        "## Variants Found",
        "",
        "| Variant | Relative Path | Liberty Files |",
        "| --- | --- | ---: |",
    ]
    lines.extend(_variant_rows(manifest["variants"]))
    lines.extend(
        [
            "",
            "## Liberty File Inventory Summary",
            "",
            f"- Total `.lib` files discovered: {manifest['liberty_file_count']}",
            "",
            "### Standard-Cell Family Counts",
            "",
            "| Family | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(_count_rows(manifest["standard_cell_family_counts"]))
    lines.extend(
        [
            "",
            "### Inferred Corner Summary",
            "",
            "| Corner | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(_count_rows(manifest["corner_counts"], limit=30))
    lines.extend(
        [
            "",
            "## Selected Target Subset",
            "",
            "| Variant | Family | Corner | Size Bytes | Relative Path |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    lines.extend(_target_subset_rows(manifest["selected_target_subset"]))
    lines.extend(
        [
            "",
            "## Parser Compatibility Table",
            "",
            "| File | Success | Library | Cells | Timing Tables | Error |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    lines.extend(_compatibility_rows(compatibility["compatibility_results"]))
    lines.extend(
        [
            "",
            "## Parser Compatibility Summary",
            "",
            f"- Parse successes: {compatibility['success_count']}",
            f"- Parse failures: {compatibility['failure_count']}",
            f"- Scope warning: {compatibility['parser_scope_warning']}",
            "",
            "## Limitations",
            "",
            "- The current parser remains a fixture-first educational subset parser.",
            "- Successful parsing of the selected subset does not imply full Liberty "
            "compliance.",
            "- The report records metadata only and does not dump raw Liberty text.",
            "- M5 does not perform timing interpolation, static timing analysis, "
            "physical layout analysis, or signoff validation.",
            "- Results depend on the external PDK version selected by the environment.",
            "",
            "## M6 Handoff",
            "",
            "- Use the M5 manifest and compatibility results as the input baseline for "
            "M6 report polishing and broader corner comparison.",
            "- Keep raw PDK files external and continue committing only small "
            "generated summary artifacts.",
            "- Treat parser extensions as bounded compatibility improvements, not a "
            "full Liberty parser rewrite.",
            "",
        ]
    )
    return "\n".join(lines)


def write_sky130_readonly_report_markdown(
    pdk: PdkRoot,
    path: str | Path,
    *,
    root_display: str,
    root_env_var: str,
) -> None:
    """Write the generated M5 read-only Sky130 ingestion Markdown report."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_sky130_readonly_report_markdown(
            pdk,
            root_display=root_display,
            root_env_var=root_env_var,
        ),
        encoding="utf-8",
    )


def _probe_liberty_file(liberty: LibertyFile) -> ParseCompatibilityRecord:
    try:
        library = parse_liberty_file(liberty.path)
    except Exception as error:  # noqa: BLE001 - report compatibility failures.
        return ParseCompatibilityRecord(
            relative_path=liberty.relative_path,
            variant=liberty.variant,
            library_family=liberty.library_family,
            corner=liberty.corner,
            size_bytes=liberty.size_bytes,
            success=False,
            error_class=type(error).__name__,
            error_message=_compact_error_message(error),
        )

    return ParseCompatibilityRecord(
        relative_path=liberty.relative_path,
        variant=liberty.variant,
        library_family=liberty.library_family,
        corner=liberty.corner,
        size_bytes=liberty.size_bytes,
        success=True,
        library_name=library.name,
        cell_count=len(library.cells),
        timing_table_count=_timing_table_count(library),
    )


def _timing_table_count(library: Library) -> int:
    return sum(
        len(arc.timing_tables)
        for cell in library.cells.values()
        for pin in cell.pins.values()
        for arc in pin.timing_arcs
    )


def _compact_error_message(error: Exception) -> str:
    message = " ".join(str(error).split())
    if len(message) <= MAX_ERROR_MESSAGE_CHARS:
        return message
    return message[: MAX_ERROR_MESSAGE_CHARS - 3] + "..."


def _record_json(record: ParseCompatibilityRecord) -> dict[str, Any]:
    return {
        "relative_path": record.relative_path,
        "variant": record.variant,
        "library_family": record.library_family,
        "corner": record.corner,
        "size_bytes": record.size_bytes,
        "success": record.success,
        "library_name": record.library_name,
        "cell_count": record.cell_count,
        "timing_table_count": record.timing_table_count,
        "error_class": record.error_class,
        "error_message": record.error_message,
    }


def _variant_rows(variants: list[dict[str, Any]]) -> list[str]:
    if not variants:
        return ["| None |  | 0 |"]
    return [
        "| "
        + " | ".join(
            [
                _escape_markdown(str(variant["name"])),
                f"`{variant['relative_path']}`",
                str(variant["liberty_file_count"]),
            ]
        )
        + " |"
        for variant in variants
    ]


def _count_rows(counts: dict[str, int], *, limit: int | None = None) -> list[str]:
    if not counts:
        return ["| None | 0 |"]
    items = sorted(counts.items())
    visible_items = items if limit is None else items[:limit]
    rows = [
        f"| {_escape_markdown(name)} | {count} |"
        for name, count in visible_items
    ]
    if limit is not None and len(items) > limit:
        remaining_count = sum(count for _, count in items[limit:])
        rows.append(f"| Other inferred corners | {remaining_count} |")
    return rows


def _target_subset_rows(records: list[dict[str, Any]]) -> list[str]:
    if not records:
        return ["| None |  |  | 0 |  |"]
    return [
        "| "
        + " | ".join(
            [
                _optional(record["variant"]),
                _optional(record["library_family"]),
                _optional(record["corner"]),
                str(record["size_bytes"]),
                f"`{record['relative_path']}`",
            ]
        )
        + " |"
        for record in records
    ]


def _compatibility_rows(records: list[dict[str, Any]]) -> list[str]:
    if not records:
        return ["| None | no |  | 0 | 0 |  |"]
    return [
        "| "
        + " | ".join(
            [
                f"`{record['relative_path']}`",
                "yes" if record["success"] else "no",
                _optional(record["library_name"]),
                _optional_int(record["cell_count"]),
                _optional_int(record["timing_table_count"]),
                _optional(record["error_class"] or record["error_message"]),
            ]
        )
        + " |"
        for record in records
    ]


def _optional(value: Any) -> str:
    if value is None:
        return ""
    return _escape_markdown(str(value))


def _optional_int(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _escape_markdown(value: str) -> str:
    return value.replace("|", "\\|")
