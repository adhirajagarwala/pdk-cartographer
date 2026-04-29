import csv
import json
from pathlib import Path

from pdk_cartographer.atlas import (
    build_standard_cell_atlas,
    render_atlas_markdown,
    write_atlas_csv,
    write_atlas_json,
)
from pdk_cartographer.liberty import parse_liberty_file

FIXTURE_DIR = Path("data/fixtures/liberty")


def _atlas_from_multi_cell_fixture():
    path = FIXTURE_DIR / "multi_cell_combinational.lib"
    library = parse_liberty_file(path)
    return build_standard_cell_atlas([library], source_fixture_paths=[path.as_posix()])


def test_render_atlas_markdown_has_required_sections_and_notice() -> None:
    markdown = render_atlas_markdown(_atlas_from_multi_cell_fixture())

    assert markdown.startswith("# M3 Fixture Standard Cell Atlas")
    assert "synthetic educational Liberty fixtures, not real Sky130 data" in markdown
    assert "## Overview" in markdown
    assert "## Source Fixtures" in markdown
    assert "## Library Summary" in markdown
    assert "## Cell Inventory" in markdown
    assert "## Area Ranking" in markdown
    assert "## Family Summary" in markdown
    assert "## Cell Kind Summary" in markdown
    assert "## Limitations" in markdown
    assert (
        "| synthetic_multi_cell_combinational | INV_X1 | 1.2 | INV | X1 |"
        in markdown
    )


def test_write_atlas_csv_has_stable_columns_and_one_row_per_cell(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "atlas.csv"

    write_atlas_csv(_atlas_from_multi_cell_fixture(), output_path)

    rows = list(csv.DictReader(output_path.read_text(encoding="utf-8").splitlines()))
    assert list(rows[0]) == [
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
    ]
    assert [row["cell_name"] for row in rows] == ["INV_X1", "NAND2_X1", "NOR2_X1"]
    assert rows[1]["input_pins"] == "A;B"
    assert rows[1]["output_pins"] == "Y"


def test_write_atlas_json_includes_summary_metadata(tmp_path: Path) -> None:
    output_path = tmp_path / "atlas.json"

    write_atlas_json(_atlas_from_multi_cell_fixture(), output_path)

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert (
        "synthetic educational Liberty fixtures, not real Sky130 data"
        in payload["notice"]
    )
    assert payload["source_fixture_paths"] == [
        "data/fixtures/liberty/multi_cell_combinational.lib"
    ]
    assert payload["summary"]["cell_count"] == 3
    assert payload["summary"]["family_counts"] == {
        "INV": 1,
        "NAND2": 1,
        "NOR2": 1,
    }
    assert payload["summary"]["cell_kind_counts"] == {"combinational": 3}
