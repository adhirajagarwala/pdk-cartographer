"""Manifest generation for read-only Sky130 Liberty discovery."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from pdk_cartographer.pdk.models import LibertyFile, PdkRoot

CSV_COLUMNS = (
    "variant",
    "library_family",
    "corner",
    "size_bytes",
    "relative_path",
    "selected_target",
)
M5_READONLY_NOTICE = (
    "Generated from an external read-only Sky130 PDK root. Raw Liberty "
    "contents are not copied into this repository."
)
PREFERRED_TARGET_FAMILY = "sky130_fd_sc_hd"
PREFERRED_TARGET_CORNERS = frozenset(
    {
        "tt_025C_1v80",
        "ff_100C_1v95",
        "ss_100C_1v40",
    }
)


def build_liberty_manifest(
    pdk: PdkRoot,
    *,
    root_display: str,
    root_env_var: str,
    max_target_files: int = 3,
) -> dict[str, Any]:
    """Return deterministic manifest metadata for discovered Liberty files."""

    liberty_files = _all_liberty_files(pdk)
    target_subset = select_target_subset(pdk, max_files=max_target_files)
    selected_paths = {liberty.relative_path for liberty in target_subset}

    return {
        "notice": M5_READONLY_NOTICE,
        "pdk_root": {
            "display": root_display,
            "env_var": root_env_var,
        },
        "variants": [
            {
                "name": variant.name,
                "relative_path": _relative_variant_path(variant.path, pdk.root),
                "liberty_file_count": len(variant.liberty_files),
            }
            for variant in pdk.variants
        ],
        "liberty_file_count": len(liberty_files),
        "standard_cell_family_counts": _count_nonempty(
            liberty.library_family for liberty in liberty_files
        ),
        "corner_counts": _count_nonempty(liberty.corner for liberty in liberty_files),
        "selected_target_subset": [
            _liberty_file_json(liberty, selected_paths=selected_paths)
            for liberty in target_subset
        ],
        "liberty_files": [
            _liberty_file_json(liberty, selected_paths=selected_paths)
            for liberty in sorted(liberty_files, key=lambda item: item.relative_path)
        ],
    }


def write_liberty_files_csv(pdk: PdkRoot, path: str | Path) -> None:
    """Write one deterministic CSV row per discovered Liberty file."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    target_subset = select_target_subset(pdk)
    selected_paths = {liberty.relative_path for liberty in target_subset}

    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=CSV_COLUMNS,
            lineterminator="\n",
        )
        writer.writeheader()
        for liberty in sorted(
            _all_liberty_files(pdk),
            key=lambda item: item.relative_path,
        ):
            writer.writerow(
                _liberty_file_csv_row(liberty, selected_paths=selected_paths)
            )


def write_liberty_manifest_json(
    pdk: PdkRoot,
    path: str | Path,
    *,
    root_display: str,
    root_env_var: str,
) -> None:
    """Write deterministic Sky130 Liberty manifest metadata as JSON."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_liberty_manifest(
        pdk,
        root_display=root_display,
        root_env_var=root_env_var,
    )
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def select_target_subset(
    pdk: PdkRoot,
    *,
    max_files: int = 3,
) -> tuple[LibertyFile, ...]:
    """Select a small first-pass Sky130 Liberty target subset."""

    if max_files <= 0:
        return ()

    liberty_files = tuple(sorted(_all_liberty_files(pdk), key=_target_sort_key))
    selected: list[LibertyFile] = []
    for category in (_is_typical_corner, _is_fast_corner, _is_slow_corner):
        match = _first_match(liberty_files, category, excluded=selected)
        if match is not None:
            selected.append(match)
        if len(selected) >= max_files:
            return tuple(selected)

    for liberty in liberty_files:
        if liberty in selected:
            continue
        selected.append(liberty)
        if len(selected) >= max_files:
            break
    return tuple(selected)


def _all_liberty_files(pdk: PdkRoot) -> tuple[LibertyFile, ...]:
    return tuple(
        liberty
        for variant in pdk.variants
        for liberty in variant.liberty_files
    )


def _first_match(
    liberty_files: tuple[LibertyFile, ...],
    predicate: Any,
    *,
    excluded: list[LibertyFile],
) -> LibertyFile | None:
    for liberty in liberty_files:
        if liberty not in excluded and predicate(liberty):
            return liberty
    return None


def _target_sort_key(liberty: LibertyFile) -> tuple[int, int, int, str]:
    variant_rank = 0 if liberty.variant == "sky130A" else 1
    family_rank = 0 if liberty.library_family == PREFERRED_TARGET_FAMILY else 1
    corner_rank = 0 if liberty.corner in PREFERRED_TARGET_CORNERS else 1
    return (variant_rank, family_rank, corner_rank, liberty.relative_path)


def _is_typical_corner(liberty: LibertyFile) -> bool:
    return (liberty.corner or "").startswith("tt_")


def _is_fast_corner(liberty: LibertyFile) -> bool:
    return (liberty.corner or "").startswith("ff_")


def _is_slow_corner(liberty: LibertyFile) -> bool:
    return (liberty.corner or "").startswith("ss_")


def _count_nonempty(values: Any) -> dict[str, int]:
    counts = Counter(value for value in values if value)
    return dict(sorted(counts.items()))


def _relative_variant_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def _liberty_file_json(
    liberty: LibertyFile,
    *,
    selected_paths: set[str],
) -> dict[str, Any]:
    return {
        "variant": liberty.variant,
        "library_family": liberty.library_family,
        "corner": liberty.corner,
        "size_bytes": liberty.size_bytes,
        "relative_path": liberty.relative_path,
        "selected_target": liberty.relative_path in selected_paths,
    }


def _liberty_file_csv_row(
    liberty: LibertyFile,
    *,
    selected_paths: set[str],
) -> dict[str, Any]:
    return {
        "variant": liberty.variant or "",
        "library_family": liberty.library_family or "",
        "corner": liberty.corner or "",
        "size_bytes": liberty.size_bytes,
        "relative_path": liberty.relative_path,
        "selected_target": "yes" if liberty.relative_path in selected_paths else "no",
    }
