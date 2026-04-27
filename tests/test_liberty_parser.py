from pathlib import Path

import pdk_cartographer.liberty.parser as liberty_parser
from pdk_cartographer.liberty.models import TimingArc
from pdk_cartographer.liberty.parser import (
    parse_liberty_file,
    parse_liberty_groups,
    parse_liberty_text,
)

FIXTURE_DIR = Path("data/fixtures/liberty")


def test_parse_simple_library_group_tree() -> None:
    groups = parse_liberty_groups(
        """
        library(tiny) {
          time_unit : "1ns";
        }
        """
    )

    assert len(groups) == 1
    library = groups[0]
    assert library.name == "library"
    assert library.args == ("tiny",)
    assert library.attributes["time_unit"].value == "1ns"


def test_parse_nested_cell_and_pin_groups() -> None:
    groups = parse_liberty_groups(
        """
        library(tiny) {
          cell(TINY_BUF_X1) {
            area : 2.5;
            pin(A) {
              direction : input;
            }
          }
        }
        """
    )

    library = groups[0]
    cell = library.child_groups("cell")[0]
    pin = cell.child_groups("pin")[0]
    assert cell.first_arg_as_string() == "TINY_BUF_X1"
    assert cell.attributes["area"].value == 2.5
    assert pin.first_arg_as_string() == "A"
    assert pin.attributes["direction"].value == "input"


def test_parse_multiple_groups_with_same_name() -> None:
    groups = parse_liberty_groups(
        """
        library(tiny) {
          cell(A_X1) {
          }
          cell(B_X1) {
          }
        }
        """
    )

    cells = groups[0].child_groups("cell")
    assert [cell.first_arg_as_string() for cell in cells] == ["A_X1", "B_X1"]


def test_parse_tiny_combinational_fixture() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "tiny_combinational.lib")

    assert library.name == "tiny_synthetic_combinational"
    assert "TINY_INV_X1" in library.cells
    assert library.attributes["time_unit"] == "1ns"
    cell = library.get_cell("TINY_INV_X1")
    assert cell.area == 1.40
    assert cell.attributes["area"] == 1.40
    assert "A" in cell.pins

    input_pin = cell.get_pin("A")
    assert input_pin.direction == "input"
    assert input_pin.capacitance == 0.0021
    assert input_pin.function is None
    assert input_pin.timing_arcs == []

    output_pin = cell.get_pin("Y")
    assert output_pin.direction == "output"
    assert output_pin.function == "!A"
    assert output_pin.capacitance is None
    assert output_pin.timing_arcs == [
        TimingArc(
            related_pin="A",
            timing_sense="negative_unate",
            timing_type="combinational",
            attributes={
                "related_pin": "A",
                "timing_sense": "negative_unate",
                "timing_type": "combinational",
            },
        ),
    ]


def test_parse_tiny_sequential_fixture() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "tiny_sequential.lib")

    assert library.name == "tiny_synthetic_sequential"
    cell = library.get_cell("TINY_DFF_X1")
    assert cell.area == 4.80

    clock_pin = cell.get_pin("CLK")
    assert clock_pin.direction == "input"
    assert clock_pin.capacitance == 0.0030

    data_pin = cell.get_pin("D")
    assert data_pin.direction == "input"
    assert data_pin.capacitance == 0.0024

    output_pin = cell.get_pin("Q")
    assert output_pin.direction == "output"
    assert output_pin.function == "IQ"
    assert output_pin.timing_arcs == [
        TimingArc(
            related_pin="CLK",
            timing_sense=None,
            timing_type="rising_edge",
            attributes={"related_pin": "CLK", "timing_type": "rising_edge"},
        ),
        TimingArc(
            related_pin="D",
            timing_sense="non_unate",
            timing_type="setup_rising",
            attributes={
                "related_pin": "D",
                "timing_sense": "non_unate",
                "timing_type": "setup_rising",
            },
        ),
    ]


def test_parse_liberty_text_returns_library() -> None:
    library = parse_liberty_text(
        """
        library(unit_api) {
          cell(TINY_EMPTY_X1) {
          }
        }
        """
    )

    assert library.name == "unit_api"
    assert library.cells["TINY_EMPTY_X1"].area is None


def test_parse_multi_cell_combinational_fixture() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "multi_cell_combinational.lib")

    assert library.name == "synthetic_multi_cell_combinational"
    assert set(library.cells) == {"INV_X1", "NAND2_X1", "NOR2_X1"}
    assert library.get_cell("INV_X1").area == 1.20
    assert library.get_cell("NAND2_X1").get_pin("A").capacitance == 0.0022
    assert library.get_cell("NAND2_X1").get_pin("Y").function == "!(A & B)"
    assert library.get_cell("NOR2_X1").get_pin("Y").function == "!(A | B)"


def test_parse_timing_arcs_fixture() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "timing_arcs.lib")
    output_pin = library.get_cell("NAND2_X1").get_pin("Y")

    assert [arc.related_pin for arc in output_pin.timing_arcs] == ["A", "B"]
    assert [arc.timing_sense for arc in output_pin.timing_arcs] == [
        "negative_unate",
        "negative_unate",
    ]
    assert [arc.timing_type for arc in output_pin.timing_arcs] == [
        "combinational",
        "combinational",
    ]
    assert output_pin.timing_arcs[0].attributes["related_pin"] == "A"


def test_parse_edge_cases_fixture_preserves_attributes() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "parser_edge_cases.lib")
    cell = library.get_cell("EDGE_BUF_X1")
    input_pin = cell.get_pin("A")

    assert library.attributes["comment_label"] == "quoted metadata survives"
    assert cell.attributes["pdk_cartographer_note"] == "synthetic only"
    assert input_pin.attributes["custom_index"] == 3.0
    assert cell.get_pin("Y").timing_arcs[0].related_pin == "A"


def test_parser_scope_is_documented() -> None:
    assert liberty_parser.__doc__ is not None
    assert "not a complete Liberty parser" in liberty_parser.__doc__
    assert "lookup table parsing" in liberty_parser.__doc__
