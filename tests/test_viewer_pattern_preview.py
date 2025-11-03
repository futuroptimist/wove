"""Ensure the Three.js viewer ships the base chain row planner preview."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PREVIEW_NAME = "base_chain_row.planner.json"
VIEWER_PREVIEW_ROOT = PROJECT_ROOT / "viewer" / "assets"
FIXTURE_PREVIEW_ROOT = PROJECT_ROOT / "tests" / "fixtures" / "patterns"
VIEWER_PREVIEW = VIEWER_PREVIEW_ROOT / PREVIEW_NAME
FIXTURE_PREVIEW = FIXTURE_PREVIEW_ROOT / PREVIEW_NAME


def test_viewer_planner_preview_matches_fixture() -> None:
    """The viewer asset should mirror the base chain row planner fixture."""

    assert VIEWER_PREVIEW.exists()
    assert FIXTURE_PREVIEW.exists()
    viewer_preview = VIEWER_PREVIEW.read_text(encoding="utf-8")
    fixture_preview = FIXTURE_PREVIEW.read_text(encoding="utf-8")

    assert viewer_preview == fixture_preview


def test_viewer_exposes_planner_defaults_panel() -> None:
    """The overlay should advertise the planner defaults list."""

    html = (PROJECT_ROOT / "viewer" / "index.html").read_text(encoding="utf-8")

    assert "pattern-defaults-status" in html
    assert "Loading planner defaults…" in html
    assert "Planner defaults unavailable." in html


def test_viewer_ships_fallback_pattern_defaults() -> None:
    """Ensure fallback planner defaults include feed rate metadata."""

    html = (PROJECT_ROOT / "viewer" / "index.html").read_text(encoding="utf-8")

    assert "fallbackPatternDefaults" in html
    assert "travel_feed_rate_mm_min" in html
    assert "default_row_height_mm" in html
    assert "yarnFlowStatusFallbackMessage" in html
    assert "yarnFlowSpoolFallbackMessage" in html
    assert "plannerMetadataFallbackMessage" in html


def test_planner_defaults_panel_mentions_homing_guard() -> None:
    """The planner defaults overlay should echo homing guard metadata."""

    html = (PROJECT_ROOT / "viewer" / "index.html").read_text(encoding="utf-8")

    assert "Homing guard" in html
    assert "Optional for this planner preview" in html
    assert "Recorded home state" in html
