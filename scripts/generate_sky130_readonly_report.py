"""Generate M5 read-only Sky130 parser compatibility artifacts."""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pdk_cartographer.pdk.config import (  # noqa: E402
    get_configured_pdk_root_env_var,
    get_pdk_root_from_env,
)
from pdk_cartographer.pdk.discovery import discover_sky130_pdk  # noqa: E402
from pdk_cartographer.pdk.reports import (  # noqa: E402
    build_parse_compatibility_payload,
    write_parse_compatibility_json,
    write_sky130_readonly_report_markdown,
)

OUTPUT_DIR = REPO_ROOT / "data" / "derived" / "m5_sky130_readonly"
COMPATIBILITY_OUTPUT = OUTPUT_DIR / "sky130_parse_compatibility.json"
MARKDOWN_OUTPUT = (
    REPO_ROOT
    / "docs"
    / "reports"
    / "generated"
    / "m5-sky130-readonly-ingestion.md"
)


def main() -> int:
    """Generate parser compatibility JSON for selected real Sky130 Liberty files."""

    root_env_var = _configured_root_env_var()
    pdk_root = get_pdk_root_from_env()
    if pdk_root is None or root_env_var is None:
        print(
            "No PDK root configured. Set PDK_CARTOGRAPHER_PDK_ROOT or PDK_ROOT.",
            file=sys.stderr,
        )
        return 2
    if not pdk_root.is_dir():
        print(
            f"Configured PDK root ${root_env_var} does not exist or is not a "
            "directory.",
            file=sys.stderr,
        )
        return 2

    pdk = discover_sky130_pdk(pdk_root)
    liberty_file_count = sum(len(variant.liberty_files) for variant in pdk.variants)
    if not pdk.variants:
        print(
            f"No sky130A or sky130B directories found below ${root_env_var}.",
            file=sys.stderr,
        )
        return 3
    if liberty_file_count == 0:
        print(f"No Liberty .lib files found below ${root_env_var}.", file=sys.stderr)
        return 3

    root_display = f"${root_env_var}"
    write_sky130_readonly_report_markdown(
        pdk,
        MARKDOWN_OUTPUT,
        root_display=root_display,
        root_env_var=root_env_var,
    )
    write_parse_compatibility_json(
        pdk,
        COMPATIBILITY_OUTPUT,
        root_display=root_display,
        root_env_var=root_env_var,
    )
    payload = build_parse_compatibility_payload(
        pdk,
        root_display=root_display,
        root_env_var=root_env_var,
    )

    print(MARKDOWN_OUTPUT.relative_to(REPO_ROOT).as_posix())
    print(COMPATIBILITY_OUTPUT.relative_to(REPO_ROOT).as_posix())
    print(f"selected_files: {len(payload['selected_files'])}")
    print(f"parse_successes: {payload['success_count']}")
    print(f"parse_failures: {payload['failure_count']}")
    for relative_path in payload["selected_files"]:
        print(f"- {relative_path}")
    return 0


def _configured_root_env_var() -> str | None:
    return get_configured_pdk_root_env_var(os.environ)


if __name__ == "__main__":
    raise SystemExit(main())
