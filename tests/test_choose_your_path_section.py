"""Ensure docs highlight the Hand-Craft and Automation tracks."""

from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "path",
    [
        Path("README.md"),
        Path("docs/index.md"),
    ],
)
def test_choose_your_path_section_present(path: Path) -> None:
    """Each entry point should mention the Choose Your Path navigation."""

    text = path.read_text(encoding="utf-8")
    assert "## Choose Your Path" in text
