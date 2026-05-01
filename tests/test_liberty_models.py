import pdk_cartographer.liberty as liberty
from pdk_cartographer.liberty.models import (
    Cell,
    Library,
    LookupTableTemplate,
    Pin,
    TimingArc,
    TimingTable,
)


def test_model_getters_return_name_indexed_members() -> None:
    pin = Pin(name="A", direction="input")
    cell = Cell(name="TINY_BUF_X1", pins={"A": pin})
    library = Library(name="tiny", cells={"TINY_BUF_X1": cell})

    assert library.get_cell("TINY_BUF_X1") is cell
    assert cell.get_pin("A") is pin


def test_timing_arc_list_exists_even_when_empty() -> None:
    pin = Pin(name="A")

    assert pin.timing_arcs == []


def test_models_preserve_simple_attributes() -> None:
    arc = TimingArc(related_pin="A", attributes={"timing_type": "combinational"})
    pin = Pin(name="Y", attributes={"function": "A"}, timing_arcs=[arc])
    cell = Cell(name="BUF_X1", attributes={"area": 1.0}, pins={"Y": pin})
    library = Library(
        name="tiny",
        attributes={"time_unit": "1ns"},
        cells={"BUF_X1": cell},
    )

    assert library.attributes["time_unit"] == "1ns"
    assert library.get_cell("BUF_X1").attributes["area"] == 1.0
    assert library.get_cell("BUF_X1").get_pin("Y").attributes["function"] == "A"
    assert pin.timing_arcs[0].attributes["timing_type"] == "combinational"


def test_public_liberty_imports_work() -> None:
    assert liberty.Library is Library
    assert liberty.Cell is Cell
    assert liberty.Pin is Pin
    assert liberty.TimingArc is TimingArc
    assert liberty.TimingTable is TimingTable
    assert liberty.LookupTableTemplate is LookupTableTemplate
    assert callable(liberty.parse_liberty_text)
    assert callable(liberty.parse_liberty_file)
