"""Ensure the Three.js viewer ships the base chain row planner preview."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PREVIEW_NAME = "base_chain_row.planner.json"
VIEWER_PREVIEW = PROJECT_ROOT / "viewer" / "assets" / PREVIEW_NAME
FIXTURE_PREVIEW = PROJECT_ROOT / "tests" / "fixtures" / "patterns" / PREVIEW_NAME


def test_viewer_planner_preview_matches_fixture() -> None:
    """The viewer asset should mirror the base chain row planner fixture."""

    assert VIEWER_PREVIEW.exists()
    assert FIXTURE_PREVIEW.exists()
    assert VIEWER_PREVIEW.read_text(encoding="utf-8") == FIXTURE_PREVIEW.read_text(
        encoding="utf-8"
    )
