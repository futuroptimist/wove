"""Regression tests for belt guard visuals in the Three.js viewer."""

from tests.viewer_utils import load_viewer_source


def test_viewer_mentions_snap_on_belt_guards() -> None:
    """Ensure the viewer describes the new snap-on belt guard elements."""
    html = load_viewer_source()

    assert "Snap-on belt guard — shields CoreXY belts" in html
    assert "Snap-On Belt Guards" in html
