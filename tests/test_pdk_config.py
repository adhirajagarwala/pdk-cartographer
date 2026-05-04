from pathlib import Path

from pdk_cartographer.pdk.config import get_pdk_root_from_env


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


def test_get_pdk_root_returns_none_when_unset() -> None:
    assert get_pdk_root_from_env({}) is None
