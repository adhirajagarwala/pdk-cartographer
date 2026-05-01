from pathlib import Path

from pdk_cartographer.liberty.parser import parse_liberty_file
from pdk_cartographer.timing import build_timing_table_explorer

FIXTURE_DIR = Path("data/fixtures/liberty")
M4_TIMING_FIXTURE_NAMES = (
    "timing_table_2x2.lib",
    "timing_table_3x3.lib",
    "timing_table_edge_cases.lib",
)


def _m4_timing_fixture_paths() -> tuple[Path, ...]:
    return tuple(FIXTURE_DIR / name for name in M4_TIMING_FIXTURE_NAMES)


def _m4_timing_libraries():
    return [parse_liberty_file(path) for path in _m4_timing_fixture_paths()]


def test_summarize_all_m4_timing_table_fixtures() -> None:
    explorer = build_timing_table_explorer(
        _m4_timing_libraries(),
        source_fixture_paths=[path.as_posix() for path in _m4_timing_fixture_paths()],
    )

    assert explorer.summary.table_count == 12
    assert len(explorer.records) == 12
    assert explorer.summary.libraries == (
        "synthetic_timing_table_2x2",
        "synthetic_timing_table_3x3",
        "synthetic_timing_table_edge_cases",
    )
    assert explorer.source_fixture_paths == tuple(
        path.as_posix() for path in _m4_timing_fixture_paths()
    )


def test_table_kind_counts_cover_fixture_table_kinds() -> None:
    explorer = build_timing_table_explorer(_m4_timing_libraries())

    assert explorer.summary.table_kind_counts == {
        "cell_fall": 3,
        "cell_rise": 5,
        "fall_transition": 2,
        "rise_transition": 2,
    }


def test_dimension_counts_include_2x2_and_3x3_tables() -> None:
    explorer = build_timing_table_explorer(_m4_timing_libraries())

    assert explorer.summary.dimension_counts == {
        "2x2": 6,
        "3x3": 6,
    }


def test_records_include_related_pin_timing_metadata_and_template_variables() -> None:
    explorer = build_timing_table_explorer(_m4_timing_libraries())

    first_record = explorer.records[0]

    assert first_record.library_name == "synthetic_timing_table_2x2"
    assert first_record.cell_name == "INV_X1"
    assert first_record.pin_name == "Y"
    assert first_record.related_pin == "A"
    assert first_record.timing_type == "combinational"
    assert first_record.timing_sense == "negative_unate"
    assert first_record.table_kind == "cell_rise"
    assert first_record.template_name == "timing_2x2"
    assert first_record.variable_1 == "input_net_transition"
    assert first_record.variable_2 == "total_output_net_capacitance"
    assert first_record.index_1_count == 2
    assert first_record.index_2_count == 2
    assert first_record.row_count == 2
    assert first_record.column_count == 2


def test_value_min_and_max_are_structural_ranges() -> None:
    explorer = build_timing_table_explorer(_m4_timing_libraries())
    first_record = explorer.records[0]

    assert first_record.value_min == 0.012
    assert first_record.value_max == 0.041


def test_timing_type_and_sense_counts_are_summarized() -> None:
    explorer = build_timing_table_explorer(_m4_timing_libraries())

    assert explorer.summary.timing_type_counts == {
        "combinational": 11,
        "rising_edge": 1,
    }
    assert explorer.summary.timing_sense_counts == {
        "negative_unate": 10,
        "positive_unate": 1,
    }


def test_records_are_deterministically_ordered() -> None:
    libraries = _m4_timing_libraries()
    first = build_timing_table_explorer(libraries)
    second = build_timing_table_explorer(reversed(libraries))

    assert first.records == second.records
    first_three_record_names = [
        (record.library_name, record.cell_name) for record in first.records[:3]
    ]

    assert first_three_record_names == [
        ("synthetic_timing_table_2x2", "INV_X1"),
        ("synthetic_timing_table_2x2", "INV_X1"),
        ("synthetic_timing_table_2x2", "INV_X1"),
    ]
