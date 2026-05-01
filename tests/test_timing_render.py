import csv
import importlib.util
import json
from pathlib import Path
from types import ModuleType

from pdk_cartographer.liberty import parse_liberty_file
from pdk_cartographer.timing import (
    build_timing_table_explorer,
    render_timing_explorer_markdown,
    write_timing_summary_json,
    write_timing_tables_csv,
)

FIXTURE_DIR = Path("data/fixtures/liberty")
GENERATED_MARKDOWN_PATH = Path(
    "docs/reports/generated/m4-fixture-timing-table-explorer.md"
)
GENERATED_CSV_PATH = Path(
    "data/derived/m4_timing_table_explorer/fixture_timing_tables.csv"
)
GENERATED_JSON_PATH = Path(
    "data/derived/m4_timing_table_explorer/fixture_timing_summary.json"
)


def _timing_explorer():
    paths = tuple(sorted(FIXTURE_DIR.glob("*.lib")))
    libraries = tuple(parse_liberty_file(path) for path in paths)
    return build_timing_table_explorer(
        libraries,
        source_fixture_paths=[path.as_posix() for path in paths],
    )


def test_render_timing_explorer_markdown_has_required_sections_and_notice() -> None:
    markdown = render_timing_explorer_markdown(_timing_explorer())

    assert markdown.startswith("# M4 Fixture Timing Table Explorer")
    assert "synthetic educational Liberty fixtures, not real Sky130 data" in markdown
    assert "## Overview" in markdown
    assert "## Source Fixtures" in markdown
    assert "## Timing Table Inventory" in markdown
    assert "## Table Kind Summary" in markdown
    assert "## Axis and Dimension Summary" in markdown
    assert "## Timing Arc Summary" in markdown
    assert "## What This Does Not Do" in markdown
    assert "## Limitations" in markdown
    assert "M4 does not perform static timing analysis" in markdown


def test_render_timing_explorer_markdown_is_deterministic() -> None:
    explorer = _timing_explorer()

    assert render_timing_explorer_markdown(explorer) == (
        render_timing_explorer_markdown(explorer)
    )


def test_write_timing_tables_csv_has_stable_columns_and_one_row_per_table(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "timing.csv"

    write_timing_tables_csv(_timing_explorer(), output_path)

    rows = list(csv.DictReader(output_path.read_text(encoding="utf-8").splitlines()))
    assert list(rows[0]) == [
        "library_name",
        "cell_name",
        "pin_name",
        "related_pin",
        "timing_type",
        "timing_sense",
        "table_kind",
        "template_name",
        "variable_1",
        "variable_2",
        "index_1_count",
        "index_2_count",
        "row_count",
        "column_count",
        "value_min",
        "value_max",
    ]
    assert len(rows) == 12
    assert rows[0]["library_name"] == "synthetic_timing_table_2x2"
    assert rows[0]["row_count"] == "2"


def test_write_timing_summary_json_includes_summary_and_records(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "timing.json"

    write_timing_summary_json(_timing_explorer(), output_path)

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert "synthetic educational Liberty fixtures, not real Sky130 data" in payload[
        "notice"
    ]
    assert payload["summary"]["table_count"] == 12
    assert payload["summary"]["dimension_counts"] == {"2x2": 6, "3x3": 6}
    assert len(payload["records"]) == 12


def test_csv_and_json_renderers_are_deterministic(tmp_path: Path) -> None:
    explorer = _timing_explorer()
    first_csv_path = tmp_path / "first.csv"
    second_csv_path = tmp_path / "second.csv"
    first_json_path = tmp_path / "first.json"
    second_json_path = tmp_path / "second.json"

    write_timing_tables_csv(explorer, first_csv_path)
    write_timing_tables_csv(explorer, second_csv_path)
    write_timing_summary_json(explorer, first_json_path)
    write_timing_summary_json(explorer, second_json_path)

    assert first_csv_path.read_text(encoding="utf-8") == second_csv_path.read_text(
        encoding="utf-8"
    )
    assert first_json_path.read_text(encoding="utf-8") == second_json_path.read_text(
        encoding="utf-8"
    )


def test_equivalent_generation_path_writes_expected_artifacts(tmp_path: Path) -> None:
    explorer = _timing_explorer()
    markdown_path = tmp_path / GENERATED_MARKDOWN_PATH
    csv_path = tmp_path / GENERATED_CSV_PATH
    json_path = tmp_path / GENERATED_JSON_PATH

    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(
        render_timing_explorer_markdown(explorer),
        encoding="utf-8",
    )
    write_timing_tables_csv(explorer, csv_path)
    write_timing_summary_json(explorer, json_path)

    assert markdown_path.exists()
    assert csv_path.exists()
    assert json_path.exists()
    assert "not real Sky130 data" in markdown_path.read_text(encoding="utf-8")
    assert len(list(csv.DictReader(csv_path.read_text().splitlines()))) == 12
    assert json.loads(json_path.read_text())["summary"]["table_count"] == 12


def test_generator_script_writes_documented_artifact_paths(
    tmp_path: Path,
    capsys,
) -> None:
    module = _load_generator_module()
    module.MARKDOWN_OUTPUT = tmp_path / GENERATED_MARKDOWN_PATH
    module.CSV_OUTPUT = tmp_path / GENERATED_CSV_PATH
    module.JSON_OUTPUT = tmp_path / GENERATED_JSON_PATH

    assert module.main() == 0

    captured = capsys.readouterr()
    assert GENERATED_MARKDOWN_PATH.as_posix() in captured.out
    assert GENERATED_CSV_PATH.as_posix() in captured.out
    assert GENERATED_JSON_PATH.as_posix() in captured.out
    assert module.MARKDOWN_OUTPUT.exists()
    assert module.CSV_OUTPUT.exists()
    assert module.JSON_OUTPUT.exists()
    assert "synthetic educational Liberty fixtures" in module.MARKDOWN_OUTPUT.read_text(
        encoding="utf-8"
    )


def _load_generator_module() -> ModuleType:
    script_path = Path("scripts/generate_fixture_timing_report.py")
    spec = importlib.util.spec_from_file_location(
        "generate_fixture_timing_report_under_test",
        script_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
