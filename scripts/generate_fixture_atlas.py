"""Generate M3 atlas artifacts from synthetic Liberty fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pdk_cartographer.atlas import (  # noqa: E402
    build_standard_cell_atlas,
    render_atlas_markdown,
    write_atlas_csv,
    write_atlas_json,
)
from pdk_cartographer.liberty import parse_liberty_file  # noqa: E402

FIXTURE_DIR = REPO_ROOT / "data" / "fixtures" / "liberty"
MARKDOWN_OUTPUT = (
    REPO_ROOT / "docs" / "reports" / "generated" / "m3-fixture-standard-cell-atlas.md"
)
CSV_OUTPUT = (
    REPO_ROOT
    / "data"
    / "derived"
    / "m3_standard_cell_atlas"
    / "fixture_cell_inventory.csv"
)
JSON_OUTPUT = (
    REPO_ROOT
    / "data"
    / "derived"
    / "m3_standard_cell_atlas"
    / "fixture_library_summary.json"
)


def main() -> int:
    """Generate Markdown, CSV, and JSON atlas artifacts."""

    fixture_paths = tuple(sorted(FIXTURE_DIR.glob("*.lib")))
    libraries = tuple(parse_liberty_file(path) for path in fixture_paths)
    source_fixture_paths = tuple(
        path.relative_to(REPO_ROOT).as_posix() for path in fixture_paths
    )
    atlas = build_standard_cell_atlas(
        libraries,
        source_fixture_paths=source_fixture_paths,
    )

    MARKDOWN_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    MARKDOWN_OUTPUT.write_text(render_atlas_markdown(atlas), encoding="utf-8")
    write_atlas_csv(atlas, CSV_OUTPUT)
    write_atlas_json(atlas, JSON_OUTPUT)

    for path in (MARKDOWN_OUTPUT, CSV_OUTPUT, JSON_OUTPUT):
        print(path.relative_to(REPO_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
