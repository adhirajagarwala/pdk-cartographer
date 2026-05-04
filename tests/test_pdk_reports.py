import json
from pathlib import Path

from pdk_cartographer.pdk.discovery import discover_sky130_pdk
from pdk_cartographer.pdk.reports import (
    build_parse_compatibility_payload,
    probe_parser_compatibility,
    write_parse_compatibility_json,
)


def write_fake_liberty(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_probe_parser_compatibility_records_success(tmp_path: Path) -> None:
    lib_path = (
        tmp_path
        / "sky130A"
        / "libs.ref"
        / "sky130_fd_sc_hd"
        / "lib"
        / "sky130_fd_sc_hd__tt_025C_1v80.lib"
    )
    write_fake_liberty(
        lib_path,
        """
        library(fake_tt) {
          cell(INV_X1) {
            pin(Y) {
              direction : output;
              timing() {
                related_pin : "A";
              }
            }
          }
        }
        """,
    )

    results = probe_parser_compatibility(discover_sky130_pdk(tmp_path))

    assert len(results) == 1
    assert results[0].success is True
    assert results[0].library_name == "fake_tt"
    assert results[0].cell_count == 1
    assert results[0].timing_table_count == 0
    assert results[0].error_class is None


def test_probe_parser_compatibility_records_failure_without_stack_trace(
    tmp_path: Path,
) -> None:
    lib_path = (
        tmp_path
        / "sky130A"
        / "libs.ref"
        / "sky130_fd_sc_hd"
        / "lib"
        / "sky130_fd_sc_hd__tt_025C_1v80.lib"
    )
    write_fake_liberty(lib_path, "library(fake) { cell(BROKEN) {")

    results = probe_parser_compatibility(discover_sky130_pdk(tmp_path))

    assert len(results) == 1
    assert results[0].success is False
    assert results[0].library_name is None
    assert results[0].error_class is not None
    assert results[0].error_message is not None
    assert "\n" not in results[0].error_message
    assert "Traceback" not in results[0].error_message


def test_write_parse_compatibility_json_omits_raw_liberty_text(tmp_path: Path) -> None:
    lib_path = (
        tmp_path
        / "sky130A"
        / "libs.ref"
        / "sky130_fd_sc_hd"
        / "lib"
        / "sky130_fd_sc_hd__tt_025C_1v80.lib"
    )
    write_fake_liberty(lib_path, "library(secret_raw_text) {}\n")
    pdk = discover_sky130_pdk(tmp_path)
    output_path = tmp_path / "out" / "compatibility.json"

    write_parse_compatibility_json(
        pdk,
        output_path,
        root_display="$PDK_CARTOGRAPHER_PDK_ROOT",
        root_env_var="PDK_CARTOGRAPHER_PDK_ROOT",
    )

    payload = json.loads(output_path.read_text())
    output_text = output_path.read_text()
    assert payload["success_count"] == 1
    assert payload["failure_count"] == 0
    assert payload["selected_files"] == [
        "sky130A/libs.ref/sky130_fd_sc_hd/lib/"
        "sky130_fd_sc_hd__tt_025C_1v80.lib"
    ]
    assert "secret_raw_text" in payload["compatibility_results"][0]["library_name"]
    assert "library(secret_raw_text)" not in output_text


def test_build_parse_compatibility_payload_counts_success_and_failure(
    tmp_path: Path,
) -> None:
    lib_dir = tmp_path / "sky130A" / "libs.ref" / "sky130_fd_sc_hd" / "lib"
    write_fake_liberty(lib_dir / "sky130_fd_sc_hd__tt_025C_1v80.lib", "library(ok) {}")
    write_fake_liberty(lib_dir / "sky130_fd_sc_hd__ff_100C_1v95.lib", "library(bad) {")
    pdk = discover_sky130_pdk(tmp_path)

    payload = build_parse_compatibility_payload(
        pdk,
        root_display="$PDK_CARTOGRAPHER_PDK_ROOT",
        root_env_var="PDK_CARTOGRAPHER_PDK_ROOT",
    )

    assert payload["success_count"] == 1
    assert payload["failure_count"] == 1
    assert "full Liberty support" in payload["parser_scope_warning"]
    assert len(payload["compatibility_results"]) == 2
