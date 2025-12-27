from __future__ import annotations

from .viewer_source import load_viewer_bundle


def test_viewer_falls_back_to_feed_rate_when_tension_uncalibrated() -> None:
    """Yarn Flow should explain the feed-rate fallback when calibration is missing."""

    viewer_source = load_viewer_bundle()

    assert "Uncalibrated hall sensor" in viewer_source
    assert "falling back to feed-rate estimate" in viewer_source
    assert "tension_sensor_calibration" in viewer_source
