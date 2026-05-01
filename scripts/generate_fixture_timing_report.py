"""Generate M4 timing-table explorer artifacts from synthetic Liberty fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pdk_cartographer.liberty import parse_liberty_file  # noqa: E402
from pdk_cartographer.timing import (  # noqa: E402
    build_timing_table_explorer,
    render_timing_explorer_markdown,
    write_timing_summary_json,
    write_timing_tables_csv,
)

FIXTURE_DIR = REPO_ROOT / "data" / "fixtures" / "liberty"
MARKDOWN_OUTPUT = (
    REPO_ROOT
    / "docs"
    / "reports"
    / "generated"
    / "m4-fixture-timing-table-explorer.md"
)
CSV_OUTPUT = (
    REPO_ROOT
    / "data"
    / "derived"
    / "m4_timing_table_explorer"
    / "fixture_timing_tables.csv"
)
JSON_OUTPUT = (
    REPO_ROOT
    / "data"
    / "derived"
    / "m4_timing_table_explorer"
    / "fixture_timing_summary.json"
)


def main() -> int:
    """Generate Markdown, CSV, and JSON timing-table artifacts."""

    fixture_paths = tuple(sorted(FIXTURE_DIR.glob("*.lib")))
    libraries = tuple(parse_liberty_file(path) for path in fixture_paths)
    source_fixture_paths = tuple(
        path.relative_to(REPO_ROOT).as_posix() for path in fixture_paths
    )
    explorer = build_timing_table_explorer(
        libraries,
        source_fixture_paths=source_fixture_paths,
    )

    MARKDOWN_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    MARKDOWN_OUTPUT.write_text(
        render_timing_explorer_markdown(explorer),
        encoding="utf-8",
    )
    write_timing_tables_csv(explorer, CSV_OUTPUT)
    write_timing_summary_json(explorer, JSON_OUTPUT)

    for path in (MARKDOWN_OUTPUT, CSV_OUTPUT, JSON_OUTPUT):
        print(_display_path(path))
    return 0


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
