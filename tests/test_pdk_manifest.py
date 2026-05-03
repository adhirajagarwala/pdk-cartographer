import csv
import json
from pathlib import Path

from pdk_cartographer.pdk.discovery import discover_sky130_pdk
from pdk_cartographer.pdk.manifest import (
    build_liberty_manifest,
    select_target_subset,
    write_liberty_files_csv,
    write_liberty_manifest_json,
)


def write_fake_liberty(path: Path, text: str = "library(fake) {}\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_select_target_subset_prefers_sky130a_hd_tt_ff_ss(tmp_path: Path) -> None:
    hd_lib = tmp_path / "sky130A" / "libs.ref" / "sky130_fd_sc_hd" / "lib"
    hvl_lib = tmp_path / "sky130A" / "libs.ref" / "sky130_fd_sc_hvl" / "lib"
    write_fake_liberty(hd_lib / "sky130_fd_sc_hd__ss_100C_1v40.lib")
    write_fake_liberty(hd_lib / "sky130_fd_sc_hd__ff_100C_1v65.lib")
    write_fake_liberty(hd_lib / "sky130_fd_sc_hd__ff_100C_1v95.lib")
    write_fake_liberty(hd_lib / "sky130_fd_sc_hd__tt_025C_1v80.lib")
    write_fake_liberty(hvl_lib / "sky130_fd_sc_hvl__tt_025C_3v30.lib")

    pdk = discover_sky130_pdk(tmp_path)
    selected = select_target_subset(pdk)

    assert [Path(liberty.relative_path).name for liberty in selected] == [
        "sky130_fd_sc_hd__tt_025C_1v80.lib",
        "sky130_fd_sc_hd__ff_100C_1v95.lib",
        "sky130_fd_sc_hd__ss_100C_1v40.lib",
    ]


def test_manifest_uses_env_label_and_relative_paths(tmp_path: Path) -> None:
    lib_path = (
        tmp_path
        / "ciel"
        / "sky130"
        / "versions"
        / "hash"
        / "sky130A"
        / "libs.ref"
        / "sky130_fd_sc_hd"
        / "lib"
        / "sky130_fd_sc_hd__tt_025C_1v80.lib"
    )
    write_fake_liberty(lib_path)

    pdk = discover_sky130_pdk(tmp_path)
    manifest = build_liberty_manifest(
        pdk,
        root_display="$PDK_CARTOGRAPHER_PDK_ROOT",
        root_env_var="PDK_CARTOGRAPHER_PDK_ROOT",
    )

    assert manifest["pdk_root"] == {
        "display": "$PDK_CARTOGRAPHER_PDK_ROOT",
        "env_var": "PDK_CARTOGRAPHER_PDK_ROOT",
    }
    assert manifest["liberty_file_count"] == 1
    file_record = manifest["liberty_files"][0]
    assert file_record["relative_path"].startswith("ciel/sky130/versions/hash/")
    assert str(tmp_path) not in json.dumps(manifest)
    assert manifest["standard_cell_family_counts"] == {"sky130_fd_sc_hd": 1}
    assert manifest["corner_counts"] == {"tt_025C_1v80": 1}


def test_manifest_writers_create_small_csv_and_json(tmp_path: Path) -> None:
    lib_path = (
        tmp_path
        / "sky130A"
        / "libs.ref"
        / "sky130_fd_sc_hd"
        / "lib"
        / "sky130_fd_sc_hd__ff_100C_1v95.lib"
    )
    write_fake_liberty(lib_path, text="library(fake_ff) {}\n")
    pdk = discover_sky130_pdk(tmp_path)
    csv_path = tmp_path / "out" / "sky130_liberty_files.csv"
    json_path = tmp_path / "out" / "sky130_liberty_manifest.json"

    write_liberty_files_csv(pdk, csv_path)
    write_liberty_manifest_json(
        pdk,
        json_path,
        root_display="$PDK_CARTOGRAPHER_PDK_ROOT",
        root_env_var="PDK_CARTOGRAPHER_PDK_ROOT",
    )

    rows = list(csv.DictReader(csv_path.read_text().splitlines()))
    payload = json.loads(json_path.read_text())
    assert rows == [
        {
            "variant": "sky130A",
            "library_family": "sky130_fd_sc_hd",
            "corner": "ff_100C_1v95",
            "size_bytes": str(len("library(fake_ff) {}\n")),
            "relative_path": (
                "sky130A/libs.ref/sky130_fd_sc_hd/lib/"
                "sky130_fd_sc_hd__ff_100C_1v95.lib"
            ),
            "selected_target": "yes",
        }
    ]
    assert payload["selected_target_subset"][0]["selected_target"] is True
    assert "library(fake_ff)" not in json_path.read_text()
