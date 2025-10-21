"""Tests for the Three.js assembly viewer scene."""

from pathlib import Path

VIEWER_HTML = Path(__file__).resolve().parents[1] / "viewer" / "index.html"


def test_workpiece_support_bed_is_documented():
    """The v1c assembly should highlight the workpiece support bed."""
    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "workpiece support bed" in html.lower()


def test_hall_effect_sensor_is_documented():
    """The viewer should surface the hall-effect yarn tension sensor."""
    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "hall-effect tension sensor" in html.lower()


def test_pattern_planner_preview_is_documented():
    """The Pattern Studio hologram should advertise the planner preview."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "patternPlannerEvents" in html
    assert "base chain row" in html.lower()
    assert "pattern_cli --format planner" in html


def test_viewer_mentions_cooling_fan_mount() -> None:
    """The hook carriage cooling fan mount should be called out."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Cooling fan mount" in html
    assert "20 mm fan" in html
