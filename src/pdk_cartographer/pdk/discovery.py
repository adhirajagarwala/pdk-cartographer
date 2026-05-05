"""Bounded read-only discovery for external Sky130 PDK roots."""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

from pdk_cartographer.pdk.models import LibertyFile, PdkRoot, Sky130Variant

SKY130_VARIANT_NAMES = frozenset({"sky130A", "sky130B"})
DEFAULT_VARIANT_SEARCH_DEPTH = 8
DEFAULT_LIBERTY_SEARCH_DEPTH = 8

_STANDARD_CELL_FAMILY_RE = re.compile(r"(sky130_fd_sc_[A-Za-z0-9]+)")
_LIBERTY_CORNER_RE = re.compile(r"__(?P<corner>[^/]+)\.lib$")


def discover_sky130_pdk(
    root: Path,
    *,
    max_variant_depth: int = DEFAULT_VARIANT_SEARCH_DEPTH,
    max_liberty_depth: int = DEFAULT_LIBERTY_SEARCH_DEPTH,
) -> PdkRoot:
    """Discover Sky130 variants and Liberty files below an external root."""

    _validate_search_depth("max_variant_depth", max_variant_depth)
    _validate_search_depth("max_liberty_depth", max_liberty_depth)
    root = root.expanduser()
    variants = tuple(
        _discover_variant(path, root, max_liberty_depth=max_liberty_depth)
        for path in _find_variant_paths(root, max_depth=max_variant_depth)
    )
    return PdkRoot(root=root, variants=variants)


def _discover_variant(
    variant_path: Path,
    root: Path,
    *,
    max_liberty_depth: int,
) -> Sky130Variant:
    variant_name = variant_path.name
    liberty_files = tuple(
        _build_liberty_file(path, root=root, variant_name=variant_name)
        for path in _find_liberty_files(variant_path, max_depth=max_liberty_depth)
    )
    return Sky130Variant(
        name=variant_name,
        path=variant_path,
        liberty_files=liberty_files,
    )


def _build_liberty_file(path: Path, *, root: Path, variant_name: str) -> LibertyFile:
    return LibertyFile(
        path=path,
        variant=variant_name,
        library_family=_infer_library_family(path),
        corner=_infer_corner(path),
        size_bytes=path.stat().st_size,
        relative_path=_relative_path(path, root),
    )


def _find_variant_paths(root: Path, *, max_depth: int) -> tuple[Path, ...]:
    if root.name in SKY130_VARIANT_NAMES and root.is_dir() and not root.is_symlink():
        return (root,)

    variants = [
        path
        for path in _bounded_walk_dirs(root, max_depth=max_depth)
        if path.name in SKY130_VARIANT_NAMES
    ]
    return tuple(sorted(variants, key=lambda path: path.as_posix()))


def _find_liberty_files(variant_path: Path, *, max_depth: int) -> tuple[Path, ...]:
    liberty_files = [
        path
        for path in _bounded_walk_files(variant_path, max_depth=max_depth)
        if path.suffix == ".lib"
    ]
    return tuple(sorted(liberty_files, key=lambda path: path.as_posix()))


def _bounded_walk_dirs(root: Path, *, max_depth: int) -> Iterable[Path]:
    for path, depth in _bounded_walk(root, max_depth=max_depth):
        if depth == 0:
            continue
        if path.is_dir() and not path.is_symlink():
            yield path


def _bounded_walk_files(root: Path, *, max_depth: int) -> Iterable[Path]:
    for path, depth in _bounded_walk(root, max_depth=max_depth):
        if depth == 0:
            continue
        if path.is_file() and not path.is_symlink():
            yield path


def _bounded_walk(root: Path, *, max_depth: int) -> Iterable[tuple[Path, int]]:
    if not root.exists() or root.is_symlink():
        return

    stack = [(root, 0)]
    while stack:
        current, depth = stack.pop()
        yield current, depth
        if depth >= max_depth or not current.is_dir():
            continue

        try:
            children = sorted(current.iterdir(), key=lambda path: path.name)
        except OSError:
            continue

        for child in reversed(children):
            if child.is_symlink():
                continue
            stack.append((child, depth + 1))


def _infer_library_family(path: Path) -> str | None:
    for part in path.parts:
        match = _STANDARD_CELL_FAMILY_RE.fullmatch(part)
        if match:
            return match.group(1)

    match = _STANDARD_CELL_FAMILY_RE.search(path.name)
    if match:
        return match.group(1)
    return None


def _infer_corner(path: Path) -> str | None:
    match = _LIBERTY_CORNER_RE.search(path.name)
    if not match:
        return None

    corner = match.group("corner")
    if corner.startswith("sky130_"):
        return None
    return corner


def _relative_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def _validate_search_depth(label: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{label} must be nonnegative.")
