"""Read-only parser compatibility reports for selected Sky130 Liberty files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pdk_cartographer.liberty import parse_liberty_file
from pdk_cartographer.liberty.models import Library
from pdk_cartographer.pdk.manifest import select_target_subset
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

