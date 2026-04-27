from pathlib import Path

import pdk_cartographer.liberty.parser as liberty_parser
from pdk_cartographer.liberty.models import TimingArc
from pdk_cartographer.liberty.parser import parse_liberty_file

FIXTURE_DIR = Path("data/fixtures/liberty")


def test_parse_tiny_combinational_fixture() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "tiny_combinational.lib")

    assert library.name == "tiny_synthetic_combinational"
    cell = library.get_cell("TINY_INV_X1")
    assert cell.area == 1.40

    input_pin = cell.get_pin("A")
    assert input_pin.direction == "input"
    assert input_pin.capacitance == 0.0021
    assert input_pin.function is None

    output_pin = cell.get_pin("Y")
    assert output_pin.direction == "output"
    assert output_pin.function == "!A"
    assert output_pin.capacitance is None
    assert output_pin.timing_arcs == (
        TimingArc(
            related_pin="A",
            timing_sense="negative_unate",
            timing_type="combinational",
        ),
    )


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
    assert output_pin.timing_arcs == (
        TimingArc(related_pin="CLK", timing_sense=None, timing_type="rising_edge"),
        TimingArc(
            related_pin="D",
            timing_sense="non_unate",
            timing_type="setup_rising",
        ),
    )


def test_parser_scope_is_documented() -> None:
    assert liberty_parser.__doc__ is not None
    assert "not a complete Liberty parser" in liberty_parser.__doc__
    assert "lookup table parsing" in liberty_parser.__doc__
