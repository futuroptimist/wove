from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIEWER_HTML = PROJECT_ROOT / "viewer" / "index.html"


def test_viewer_falls_back_to_feed_rate_when_tension_uncalibrated() -> None:
    """Yarn Flow should explain the feed-rate fallback when calibration is missing."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Uncalibrated hall sensor" in html
    assert "falling back to feed-rate estimate" in html
    assert "tension_sensor_calibration" in html
