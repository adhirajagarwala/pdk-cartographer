from pathlib import Path

from pdk_cartographer.pdk.discovery import discover_sky130_pdk


def write_fake_liberty(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("library(fake) {}\n")


def test_discover_direct_sky130_variant_root(tmp_path: Path) -> None:
    variant = tmp_path / "sky130A"
    liberty = variant / "libs.ref" / "sky130_fd_sc_hd" / "lib"
    write_fake_liberty(liberty / "sky130_fd_sc_hd__tt_025C_1v80.lib")

    pdk = discover_sky130_pdk(variant)

    assert pdk.root == variant
    assert [item.name for item in pdk.variants] == ["sky130A"]
    assert len(pdk.variants[0].liberty_files) == 1


def test_discover_nested_ciel_style_variants(tmp_path: Path) -> None:
    sky130_root = tmp_path / "ciel" / "sky130" / "versions" / "hash"
    hd_lib = sky130_root / "sky130A" / "libs.ref" / "sky130_fd_sc_hd" / "lib"
    hvl_lib = sky130_root / "sky130B" / "libs.ref" / "sky130_fd_sc_hvl" / "lib"
    write_fake_liberty(hd_lib / "sky130_fd_sc_hd__tt_025C_1v80.lib")
    write_fake_liberty(hvl_lib / "sky130_fd_sc_hvl__ff_100C_5v50.lib")

    pdk = discover_sky130_pdk(tmp_path)

    assert [variant.name for variant in pdk.variants] == ["sky130A", "sky130B"]
    assert [len(variant.liberty_files) for variant in pdk.variants] == [1, 1]


def test_liberty_file_metadata_is_inferred_from_path(tmp_path: Path) -> None:
    lib_path = (
        tmp_path
        / "sky130A"
        / "libs.ref"
        / "sky130_fd_sc_hd"
        / "lib"
        / "sky130_fd_sc_hd__ss_100C_1v40.lib"
    )
    write_fake_liberty(lib_path)

    pdk = discover_sky130_pdk(tmp_path)
    liberty = pdk.variants[0].liberty_files[0]

    assert liberty.path == lib_path
    assert liberty.variant == "sky130A"
    assert liberty.library_family == "sky130_fd_sc_hd"
    assert liberty.corner == "ss_100C_1v40"
    assert liberty.size_bytes == len("library(fake) {}\n")
    assert liberty.relative_path == (
        "sky130A/libs.ref/sky130_fd_sc_hd/lib/"
        "sky130_fd_sc_hd__ss_100C_1v40.lib"
    )


def test_discovery_is_bounded(tmp_path: Path) -> None:
    shallow = tmp_path / "level1" / "sky130A"
    deep = tmp_path / "level1" / "level2" / "sky130B"
    write_fake_liberty(shallow / "libs.ref" / "sky130_fd_sc_hd" / "lib" / "a.lib")
    write_fake_liberty(deep / "libs.ref" / "sky130_fd_sc_hd" / "lib" / "b.lib")

    pdk = discover_sky130_pdk(tmp_path, max_variant_depth=2)

    assert [variant.name for variant in pdk.variants] == ["sky130A"]


def test_missing_root_returns_empty_result(tmp_path: Path) -> None:
    pdk = discover_sky130_pdk(tmp_path / "missing")

    assert pdk.variants == ()


def test_discovery_normalizes_paths_relative_to_configured_root(
    tmp_path: Path,
) -> None:
    root = tmp_path / "external" / "pdks"
    lib_path = (
        root
        / "ciel"
        / "sky130"
        / "versions"
        / "fake_hash"
        / "sky130A"
        / "libs.ref"
        / "sky130_fd_sc_hd"
        / "lib"
        / "sky130_fd_sc_hd__ff_100C_1v95.lib"
    )
    write_fake_liberty(lib_path)

    pdk = discover_sky130_pdk(root)
    liberty = pdk.variants[0].liberty_files[0]

    assert liberty.relative_path == (
        "ciel/sky130/versions/fake_hash/sky130A/libs.ref/"
        "sky130_fd_sc_hd/lib/sky130_fd_sc_hd__ff_100C_1v95.lib"
    )
    assert str(tmp_path) not in liberty.relative_path
