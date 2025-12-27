from __future__ import annotations

from tests.viewer_utils import load_viewer_source


def test_viewer_falls_back_to_feed_rate_when_tension_uncalibrated() -> None:
    """Yarn Flow should explain the feed-rate fallback when calibration is missing."""

    html = load_viewer_source()

    assert "Uncalibrated hall sensor" in html
    assert "falling back to feed-rate estimate" in html
    assert "tension_sensor_calibration" in html
