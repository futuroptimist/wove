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
