from pdk_cartographer.atlas import (
    CellRecord,
    LibraryAtlasSummary,
    StandardCellAtlas,
    classify_cell_family,
    classify_cell_kind,
    extract_drive_strength,
    is_clock_like_pin,
)


def test_inv_x1_family_and_drive_strength() -> None:
    assert classify_cell_family("INV_X1") == "INV"
    assert extract_drive_strength("INV_X1") == "X1"


def test_nand2_x1_family_and_drive_strength() -> None:
    assert classify_cell_family("NAND2_X1") == "NAND2"
    assert extract_drive_strength("NAND2_X1") == "X1"


def test_family_without_simple_drive_suffix_is_preserved() -> None:
    assert classify_cell_family("CUSTOM_CELL") == "CUSTOM_CELL"
    assert extract_drive_strength("CUSTOM_CELL") is None


def test_larger_generic_drive_strength_is_extracted() -> None:
    assert classify_cell_family("BUF_X16") == "BUF"
    assert extract_drive_strength("BUF_X16") == "X16"


def test_dff_x1_classifies_as_sequential() -> None:
    assert (
        classify_cell_kind(
            "DFF_X1",
            input_pins=("D",),
            output_pins=("Q",),
            clock_pins=(),
            timing_arc_count=0,
            functions={},
        )
        == "sequential"
    )


def test_latch_name_classifies_as_sequential() -> None:
    assert (
        classify_cell_kind(
            "LATCH_X1",
            input_pins=("D",),
            output_pins=("Q",),
            clock_pins=(),
            timing_arc_count=0,
            functions={"Q": "D"},
        )
        == "sequential"
    )


def test_clock_like_input_pin_classifies_as_sequential() -> None:
    assert (
        classify_cell_kind(
            "GENERIC_STORAGE_X1",
            input_pins=("CK", "D"),
            output_pins=("Q",),
            clock_pins=(),
            timing_arc_count=0,
            functions={"Q": "D"},
        )
        == "sequential"
    )


def test_output_function_without_clock_classifies_as_combinational() -> None:
    assert (
        classify_cell_kind(
            "NAND2_X1",
            input_pins=("A", "B"),
            output_pins=("Y",),
            clock_pins=(),
            timing_arc_count=1,
            functions={"Y": "!(A & B)"},
        )
        == "combinational"
    )


def test_function_on_non_output_pin_does_not_make_combinational() -> None:
    assert (
        classify_cell_kind(
            "PARTIAL_METADATA_X1",
            input_pins=("A",),
            output_pins=("Y",),
            clock_pins=(),
            timing_arc_count=1,
            functions={"A": "Y"},
        )
        == "unknown"
    )


def test_insufficient_metadata_classifies_as_unknown() -> None:
    assert (
        classify_cell_kind(
            "CELL_WITH_UNKNOWN_ROLE",
            input_pins=("A",),
            output_pins=("Y",),
            clock_pins=(),
            timing_arc_count=0,
            functions={},
        )
        == "unknown"
    )


def test_clock_like_pin_detection() -> None:
    assert is_clock_like_pin("CLK")
    assert is_clock_like_pin("ck")
    assert is_clock_like_pin(" clock ")
    assert not is_clock_like_pin("A")


def test_public_atlas_models_import() -> None:
    cell = CellRecord(
        library_name="fixture",
        cell_name="INV_X1",
        area=1.0,
        family="INV",
        drive_strength="X1",
        cell_kind="combinational",
    )
    summary = LibraryAtlasSummary(
        library_names=("fixture",),
        cell_count=1,
        area_min=1.0,
        area_max=1.0,
        area_mean=1.0,
    )
    atlas = StandardCellAtlas(cells=(cell,), summary=summary)

    assert atlas.cells == (cell,)
    assert atlas.summary is summary
