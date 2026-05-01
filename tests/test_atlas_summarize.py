from pathlib import Path

import pytest

from pdk_cartographer.atlas import build_cell_record, build_standard_cell_atlas
from pdk_cartographer.liberty.models import Cell, Library, Pin
from pdk_cartographer.liberty.parser import parse_liberty_file

FIXTURE_DIR = Path("data/fixtures/liberty")
M3_ATLAS_FIXTURE_NAMES = (
    "multi_cell_combinational.lib",
    "parser_edge_cases.lib",
    "timing_arcs.lib",
    "tiny_combinational.lib",
    "tiny_sequential.lib",
)


def _m3_atlas_fixture_paths() -> tuple[Path, ...]:
    return tuple(FIXTURE_DIR / name for name in M3_ATLAS_FIXTURE_NAMES)


def _fixture_libraries() -> list[Library]:
    return [parse_liberty_file(path) for path in _m3_atlas_fixture_paths()]


def test_summarize_all_synthetic_fixture_libraries() -> None:
    atlas = build_standard_cell_atlas(
        _fixture_libraries(),
        source_fixture_paths=[str(path) for path in _m3_atlas_fixture_paths()],
    )

    assert atlas.summary.library_names == (
        "synthetic_multi_cell_combinational",
        "synthetic_parser_edge_cases",
        "synthetic_timing_arcs",
        "tiny_synthetic_combinational",
        "tiny_synthetic_sequential",
    )
    assert atlas.summary.cell_count == 7
    assert len(atlas.cells) == 7
    assert atlas.source_fixture_paths == tuple(
        str(path) for path in _m3_atlas_fixture_paths()
    )


def test_all_fixture_records_have_expected_deterministic_order() -> None:
    atlas = build_standard_cell_atlas(_fixture_libraries())

    assert [(cell.library_name, cell.cell_name) for cell in atlas.cells] == [
        ("synthetic_multi_cell_combinational", "INV_X1"),
        ("synthetic_multi_cell_combinational", "NAND2_X1"),
        ("synthetic_multi_cell_combinational", "NOR2_X1"),
        ("synthetic_parser_edge_cases", "EDGE_BUF_X1"),
        ("synthetic_timing_arcs", "NAND2_X1"),
        ("tiny_synthetic_combinational", "TINY_INV_X1"),
        ("tiny_synthetic_sequential", "TINY_DFF_X1"),
    ]


def test_multi_cell_fixture_produces_multiple_deterministic_records() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "multi_cell_combinational.lib")
    atlas = build_standard_cell_atlas([library])

    assert [cell.cell_name for cell in atlas.cells] == ["INV_X1", "NAND2_X1", "NOR2_X1"]
    assert atlas.cells[1].input_pins == ("A", "B")
    assert atlas.cells[1].output_pins == ("Y",)
    assert atlas.cells[1].functions == {"Y": "!(A & B)"}
    assert atlas.cells[1].pin_capacitance == {"A": 0.0022, "B": 0.0022}


def test_area_statistics_are_computed_from_available_area_values() -> None:
    atlas = build_standard_cell_atlas(_fixture_libraries())

    assert atlas.summary.area_min == 1.20
    assert atlas.summary.area_max == 4.80
    assert atlas.summary.area_mean == pytest.approx(15.10 / 7)
    assert atlas.summary.smallest_cells[:2] == ("INV_X1", "TINY_INV_X1")
    assert atlas.summary.largest_cells[:2] == ("TINY_DFF_X1", "EDGE_BUF_X1")


def test_area_rankings_are_stable_for_duplicate_cell_names() -> None:
    atlas = build_standard_cell_atlas(_fixture_libraries())

    assert atlas.summary.largest_cells == (
        "TINY_DFF_X1",
        "EDGE_BUF_X1",
        "NOR2_X1",
        "NAND2_X1",
        "NAND2_X1",
    )
    assert atlas.summary.smallest_cells == (
        "INV_X1",
        "TINY_INV_X1",
        "NAND2_X1",
        "NAND2_X1",
        "NOR2_X1",
    )


def test_family_counts_are_computed_for_fixture_cells() -> None:
    atlas = build_standard_cell_atlas(_fixture_libraries())

    assert atlas.summary.family_counts == {
        "EDGE_BUF": 1,
        "INV": 1,
        "NAND2": 2,
        "NOR2": 1,
        "TINY_DFF": 1,
        "TINY_INV": 1,
    }


def test_classification_counts_include_combinational_and_sequential() -> None:
    atlas = build_standard_cell_atlas(_fixture_libraries())

    assert atlas.summary.cell_kind_counts == {
        "combinational": 6,
        "sequential": 1,
    }
    sequential_record = next(
        cell for cell in atlas.cells if cell.cell_name == "TINY_DFF_X1"
    )
    assert sequential_record.clock_pins == ("CLK",)
    assert sequential_record.cell_kind == "sequential"
    assert sequential_record.timing_arc_count == 2


def test_pin_categories_and_timing_arc_counts_are_summarized() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "tiny_sequential.lib")
    atlas = build_standard_cell_atlas([library])
    record = atlas.cells[0]

    assert record.input_pins == ("CLK", "D")
    assert record.output_pins == ("Q",)
    assert record.clock_pins == ("CLK",)
    assert record.other_pins == ()
    assert len(record.input_pins) == 2
    assert len(record.output_pins) == 1
    assert len(record.clock_pins) == 1
    assert record.functions == {"Q": "IQ"}
    assert record.pin_capacitance == {"CLK": 0.003, "D": 0.0024}
    assert record.timing_arc_count == 2


def test_missing_area_does_not_crash_summary() -> None:
    library = Library(
        name="missing_area_fixture",
        cells={
            "UNKNOWN_CELL": Cell(
                name="UNKNOWN_CELL",
                pins={"Y": Pin(name="Y", direction="output")},
            )
        },
    )

    atlas = build_standard_cell_atlas([library])

    assert atlas.summary.cell_count == 1
    assert atlas.summary.area_min is None
    assert atlas.summary.area_max is None
    assert atlas.summary.area_mean is None
    assert atlas.summary.largest_cells == ()
    assert atlas.summary.smallest_cells == ()
    assert atlas.cells[0].cell_kind == "unknown"


def test_records_are_sorted_by_library_name_then_cell_name() -> None:
    first = Library(
        name="z_fixture",
        cells={"BUF_X1": Cell(name="BUF_X1")},
    )
    second = Library(
        name="a_fixture",
        cells={
            "INV_X1": Cell(name="INV_X1"),
            "AND2_X1": Cell(name="AND2_X1"),
        },
    )

    atlas = build_standard_cell_atlas([first, second])

    assert [(cell.library_name, cell.cell_name) for cell in atlas.cells] == [
        ("a_fixture", "AND2_X1"),
        ("a_fixture", "INV_X1"),
        ("z_fixture", "BUF_X1"),
    ]


def test_build_standard_cell_atlas_is_repeatable() -> None:
    libraries = _fixture_libraries()

    first = build_standard_cell_atlas(libraries)
    second = build_standard_cell_atlas(reversed(libraries))

    assert first.cells == second.cells
    assert first.summary == second.summary


def test_build_cell_record_extracts_pin_groups_and_counts() -> None:
    cell = Cell(
        name="CUSTOM_X2",
        area=3.0,
        pins={
            "Y": Pin(name="Y", direction="output", function="A", capacitance=0.004),
            "A": Pin(name="A", direction="input", capacitance=0.002),
            "VPWR": Pin(name="VPWR", direction="inout"),
        },
    )

    record = build_cell_record("unit", cell)

    assert record.library_name == "unit"
    assert record.family == "CUSTOM"
    assert record.drive_strength == "X2"
    assert record.input_pins == ("A",)
    assert record.output_pins == ("Y",)
    assert record.other_pins == ("VPWR",)
    assert record.functions == {"Y": "A"}
    assert record.pin_capacitance == {"A": 0.002, "Y": 0.004}
