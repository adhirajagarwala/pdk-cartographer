import json
from pathlib import Path

from pdk_cartographer.pdk.discovery import discover_sky130_pdk
from pdk_cartographer.pdk.reports import (
    build_parse_compatibility_payload,
    render_sky130_readonly_report_markdown,
)


def write_fake_liberty(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_readonly_report_renders_inventory_subset_and_limitations(
    tmp_path: Path,
) -> None:
    lib_dir = tmp_path / "sky130A" / "libs.ref" / "sky130_fd_sc_hd" / "lib"
    write_fake_liberty(lib_dir / "sky130_fd_sc_hd__tt_025C_1v80.lib", "library(tt) {}")
    write_fake_liberty(lib_dir / "sky130_fd_sc_hd__ff_100C_1v95.lib", "library(ff) {}")
    write_fake_liberty(lib_dir / "sky130_fd_sc_hd__ss_100C_1v40.lib", "library(ss) {}")
    pdk = discover_sky130_pdk(tmp_path)

    report = render_sky130_readonly_report_markdown(
        pdk,
        root_display="$PDK_CARTOGRAPHER_PDK_ROOT",
        root_env_var="PDK_CARTOGRAPHER_PDK_ROOT",
    )

    assert "# M5 Sky130 Read-Only Ingestion Report" in report
    assert "external Sky130 PDK installation" in report
    assert "Raw PDK files are not committed" in report
    assert "read-only exploration" in report
    assert "not production signoff" in report
    assert "sky130_fd_sc_hd__tt_025C_1v80.lib" in report
    assert "sky130_fd_sc_hd__ff_100C_1v95.lib" in report
    assert "sky130_fd_sc_hd__ss_100C_1v40.lib" in report
    assert "## M6 Handoff" in report
    assert str(tmp_path) not in report
    assert "library(tt)" not in report


def test_readonly_report_compatibility_payload_records_success_and_failure(
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

    payload_text = json.dumps(payload)
    assert payload["success_count"] == 1
    assert payload["failure_count"] == 1
    assert "full Liberty support" in payload["parser_scope_warning"]
    assert "Traceback" not in payload_text
    assert "library(ok)" not in payload_text
