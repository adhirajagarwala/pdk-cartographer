from pathlib import Path

from pdk_cartographer.pdk.config import (
    get_configured_pdk_root_env_var,
    get_pdk_root_from_env,
)


def test_get_pdk_root_prefers_project_specific_env() -> None:
    root = get_pdk_root_from_env(
        {
            "PDK_CARTOGRAPHER_PDK_ROOT": "/tmp/project-pdk",
            "PDK_ROOT": "/tmp/fallback-pdk",
        }
    )

    assert root == Path("/tmp/project-pdk")


def test_get_pdk_root_falls_back_to_pdk_root() -> None:
    root = get_pdk_root_from_env({"PDK_ROOT": "/tmp/fallback-pdk"})

    assert root == Path("/tmp/fallback-pdk")


def test_get_pdk_root_uses_fallback_when_project_specific_env_is_empty() -> None:
    root = get_pdk_root_from_env(
        {
            "PDK_CARTOGRAPHER_PDK_ROOT": "",
            "PDK_ROOT": "/tmp/fallback-pdk",
        }
    )

    assert root == Path("/tmp/fallback-pdk")


def test_get_pdk_root_treats_whitespace_only_value_as_unset() -> None:
    root = get_pdk_root_from_env(
        {
            "PDK_CARTOGRAPHER_PDK_ROOT": "   ",
            "PDK_ROOT": "/tmp/fallback-pdk",
        }
    )

    assert root == Path("/tmp/fallback-pdk")


def test_get_pdk_root_strips_surrounding_whitespace() -> None:
    root = get_pdk_root_from_env({"PDK_CARTOGRAPHER_PDK_ROOT": "  ~/pdks  "})

    assert root == Path("~/pdks").expanduser()


def test_get_configured_pdk_root_env_var_matches_root_precedence() -> None:
    variable_name = get_configured_pdk_root_env_var(
        {
            "PDK_CARTOGRAPHER_PDK_ROOT": "",
            "PDK_ROOT": "/tmp/fallback-pdk",
        }
    )

    assert variable_name == "PDK_ROOT"


def test_get_pdk_root_returns_none_when_unset() -> None:
    assert get_pdk_root_from_env({}) is None
