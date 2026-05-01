from pathlib import Path

import pytest

from pdk_cartographer.liberty import (
    LibertyParseError,
    LookupTableTemplate,
    TimingTable,
    parse_liberty_file,
    parse_liberty_groups,
    parse_liberty_text,
)

FIXTURE_DIR = Path("data/fixtures/liberty")


def test_parse_complex_attributes_into_group_tree() -> None:
    groups = parse_liberty_groups(
        """
        library(unit) {
          lu_table_template(timing_2x2) {
            index_1("0.01, 0.10");
            index_2("0.001, 0.010");
          }
        }
        """
    )

    template = groups[0].child_groups("lu_table_template")[0]

    assert template.attributes["index_1"].value == "0.01, 0.10"
    assert template.attributes["index_2"].value == "0.001, 0.010"


def test_parse_lu_table_template_axes() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "timing_table_2x2.lib")
    template = library.lookup_table_templates["timing_2x2"]

    assert template == LookupTableTemplate(
        name="timing_2x2",
        variable_1="input_net_transition",
        variable_2="total_output_net_capacitance",
        index_1=(0.01, 0.10),
        index_2=(0.001, 0.010),
    )
    assert template.variable_1 == "input_net_transition"
    assert template.variable_2 == "total_output_net_capacitance"


def test_parse_2x2_timing_values_and_attach_to_arc() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "timing_table_2x2.lib")
    arc = library.get_cell("INV_X1").get_pin("Y").timing_arcs[0]

    assert arc.related_pin == "A"
    assert [table.table_kind for table in arc.timing_tables] == [
        "cell_rise",
        "cell_fall",
        "rise_transition",
        "fall_transition",
    ]
    assert arc.timing_tables[0] == TimingTable(
        table_kind="cell_rise",
        template_name="timing_2x2",
        index_1=(0.01, 0.10),
        index_2=(0.001, 0.010),
        values=((0.012, 0.018), (0.026, 0.041)),
    )


def test_parse_3x3_timing_values_from_multiple_related_pins() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "timing_table_3x3.lib")
    arcs = library.get_cell("NAND2_X1").get_pin("Y").timing_arcs

    assert [arc.related_pin for arc in arcs] == ["A", "B"]
    assert len(arcs[0].timing_tables[0].values) == 3
    assert arcs[0].timing_tables[0].values[2] == (0.045, 0.061, 0.083)
    assert arcs[1].timing_tables[0].values[2] == (0.047, 0.064, 0.086)
    assert all(table.template_name == "timing_3x3" for table in arcs[0].timing_tables)


def test_parse_all_four_timing_table_kinds() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "timing_table_2x2.lib")
    arc = library.get_cell("INV_X1").get_pin("Y").timing_arcs[0]

    assert {table.table_kind for table in arc.timing_tables} == {
        "cell_rise",
        "cell_fall",
        "rise_transition",
        "fall_transition",
    }


def test_local_table_indices_override_template_indices() -> None:
    library = parse_liberty_file(FIXTURE_DIR / "timing_table_edge_cases.lib")
    arc = library.get_cell("BUF_X2").get_pin("Y").timing_arcs[0]
    table = arc.timing_tables[0]

    assert table.index_1 == (0.02, 0.08)
    assert table.index_2 == (0.002, 0.020)
    assert table.values == ((0.011, 0.019), (0.026, 0.044))


def test_malformed_table_dimensions_raise_useful_error() -> None:
    with pytest.raises(LibertyParseError) as exc_info:
        parse_liberty_text(
            """
            library(bad_table) {
              lu_table_template(timing_2x2) {
                variable_1 : input_net_transition;
                variable_2 : total_output_net_capacitance;
                index_1("0.01, 0.10");
                index_2("0.001, 0.010");
              }

              cell(INV_X1) {
                pin(Y) {
                  direction : output;
                  function : "A";

                  timing() {
                    related_pin : "A";
                    cell_rise(timing_2x2) {
                      values("0.1, 0.2, 0.3", "0.4, 0.5, 0.6");
                    }
                  }
                }
              }
            }
            """
        )

    assert "cell_rise values row 1 length 3" in str(exc_info.value)
    assert "index_2 length 2" in str(exc_info.value)
