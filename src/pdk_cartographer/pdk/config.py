"""Configuration helpers for external PDK discovery."""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

PREFERRED_PDK_ROOT_ENV = "PDK_CARTOGRAPHER_PDK_ROOT"
FALLBACK_PDK_ROOT_ENV = "PDK_ROOT"


def get_pdk_root_from_env(env: Mapping[str, str] | None = None) -> Path | None:
    """Return the configured external PDK root, if one is set."""

    values = os.environ if env is None else env
    variable_name = get_configured_pdk_root_env_var(values)
    if variable_name is None:
        return None
    return Path(values[variable_name].strip()).expanduser()


def get_configured_pdk_root_env_var(
    env: Mapping[str, str] | None = None,
) -> str | None:
    """Return the env var name that provides the external PDK root."""

    values = os.environ if env is None else env
    for variable_name in (PREFERRED_PDK_ROOT_ENV, FALLBACK_PDK_ROOT_ENV):
        value = values.get(variable_name)
        if value and value.strip():
            return variable_name
    return None
