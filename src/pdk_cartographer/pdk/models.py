"""Typed models for read-only external PDK discovery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LibertyFile:
    """Metadata for one discovered Liberty file."""

    path: Path
    variant: str | None
    library_family: str | None
    corner: str | None
    size_bytes: int
    relative_path: str


@dataclass(frozen=True)
class Sky130Variant:
    """One discovered Sky130 variant directory and its Liberty files."""

    name: str
    path: Path
    liberty_files: tuple[LibertyFile, ...]


@dataclass(frozen=True)
class PdkRoot:
    """A read-only discovery result for one external PDK root."""

    root: Path
    variants: tuple[Sky130Variant, ...]
