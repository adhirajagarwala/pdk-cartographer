"""Generate M5 read-only Sky130 Liberty manifest artifacts."""

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
from pdk_cartographer.pdk.manifest import (  # noqa: E402
    select_target_subset,
    write_liberty_files_csv,
    write_liberty_manifest_json,
)

OUTPUT_DIR = REPO_ROOT / "data" / "derived" / "m5_sky130_readonly"
CSV_OUTPUT = OUTPUT_DIR / "sky130_liberty_files.csv"
JSON_OUTPUT = OUTPUT_DIR / "sky130_liberty_manifest.json"


def main() -> int:
    """Discover an external Sky130 PDK and write small manifest artifacts."""

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
    write_liberty_files_csv(pdk, CSV_OUTPUT)
    write_liberty_manifest_json(
        pdk,
        JSON_OUTPUT,
        root_display=root_display,
        root_env_var=root_env_var,
    )

    print(CSV_OUTPUT.relative_to(REPO_ROOT).as_posix())
    print(JSON_OUTPUT.relative_to(REPO_ROOT).as_posix())
    print(f"variants: {', '.join(variant.name for variant in pdk.variants)}")
    print(f"liberty_files: {liberty_file_count}")
    print("selected_target_subset:")
    for liberty in select_target_subset(pdk):
        print(f"- {liberty.relative_path}")
    return 0


def _configured_root_env_var() -> str | None:
    return get_configured_pdk_root_env_var(os.environ)


if __name__ == "__main__":
    raise SystemExit(main())
