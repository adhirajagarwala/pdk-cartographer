import csv
import json
from pathlib import Path

from pdk_cartographer.atlas import (
    build_standard_cell_atlas,
    render_atlas_markdown,
    write_atlas_csv,
    write_atlas_json,
)
from pdk_cartographer.liberty import Library, parse_liberty_file

FIXTURE_DIR = Path("data/fixtures/liberty")
GENERATED_MARKDOWN_PATH = Path(
    "docs/reports/generated/m3-fixture-standard-cell-atlas.md"
)
GENERATED_CSV_PATH = Path(
    "data/derived/m3_standard_cell_atlas/fixture_cell_inventory.csv"
)
GENERATED_JSON_PATH = Path(
    "data/derived/m3_standard_cell_atlas/fixture_library_summary.json"
)


def _atlas_from_multi_cell_fixture():
    path = FIXTURE_DIR / "multi_cell_combinational.lib"
    library = parse_liberty_file(path)
    return build_standard_cell_atlas([library], source_fixture_paths=[path.as_posix()])


def _atlas_from_all_fixtures():
    paths = tuple(sorted(FIXTURE_DIR.glob("*.lib")))
    libraries: tuple[Library, ...] = tuple(parse_liberty_file(path) for path in paths)
    return build_standard_cell_atlas(
        libraries,
        source_fixture_paths=[path.as_posix() for path in paths],
    )


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


def test_render_atlas_markdown_is_deterministic() -> None:
    atlas = _atlas_from_all_fixtures()

    assert render_atlas_markdown(atlas) == render_atlas_markdown(atlas)


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


def test_write_atlas_csv_is_deterministic(tmp_path: Path) -> None:
    atlas = _atlas_from_all_fixtures()
    first_path = tmp_path / "first.csv"
    second_path = tmp_path / "second.csv"

    write_atlas_csv(atlas, first_path)
    write_atlas_csv(atlas, second_path)

    assert first_path.read_text(encoding="utf-8") == second_path.read_text(
        encoding="utf-8"
    )


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


def test_write_atlas_json_is_deterministic(tmp_path: Path) -> None:
    atlas = _atlas_from_all_fixtures()
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"

    write_atlas_json(atlas, first_path)
    write_atlas_json(atlas, second_path)

    assert first_path.read_text(encoding="utf-8") == second_path.read_text(
        encoding="utf-8"
    )


def test_equivalent_generation_path_writes_expected_artifacts(tmp_path: Path) -> None:
    atlas = _atlas_from_all_fixtures()
    markdown_path = tmp_path / GENERATED_MARKDOWN_PATH
    csv_path = tmp_path / GENERATED_CSV_PATH
    json_path = tmp_path / GENERATED_JSON_PATH

    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(render_atlas_markdown(atlas), encoding="utf-8")
    write_atlas_csv(atlas, csv_path)
    write_atlas_json(atlas, json_path)

    assert markdown_path.exists()
    assert csv_path.exists()
    assert json_path.exists()
    assert "not real Sky130 data" in markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["summary"]["cell_count"] == 7
    assert payload["source_fixture_paths"] == [
        "data/fixtures/liberty/multi_cell_combinational.lib",
        "data/fixtures/liberty/parser_edge_cases.lib",
        "data/fixtures/liberty/timing_arcs.lib",
        "data/fixtures/liberty/tiny_combinational.lib",
        "data/fixtures/liberty/tiny_sequential.lib",
    ]


def test_tracked_generated_artifacts_state_synthetic_scope() -> None:
    assert GENERATED_MARKDOWN_PATH.exists()
    assert GENERATED_CSV_PATH.exists()
    assert GENERATED_JSON_PATH.exists()

    markdown = GENERATED_MARKDOWN_PATH.read_text(encoding="utf-8")
    payload = json.loads(GENERATED_JSON_PATH.read_text(encoding="utf-8"))
    csv_rows = list(
        csv.DictReader(
            GENERATED_CSV_PATH.read_text(encoding="utf-8").splitlines()
        )
    )

    assert "synthetic educational Liberty fixtures, not real Sky130 data" in markdown
    assert "synthetic educational Liberty fixtures, not real Sky130 data" in payload[
        "notice"
    ]
    assert len(csv_rows) == 7
