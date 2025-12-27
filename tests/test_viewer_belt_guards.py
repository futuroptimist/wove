"""Regression tests for belt guard visuals in the Three.js viewer."""

from .viewer_source import load_viewer_bundle


def test_viewer_mentions_snap_on_belt_guards() -> None:
    """Ensure the viewer describes the new snap-on belt guard elements."""
    viewer_source = load_viewer_bundle()

    assert "Snap-on belt guard — shields CoreXY belts" in viewer_source
    assert "Snap-On Belt Guards" in viewer_source
