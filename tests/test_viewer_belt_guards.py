"""Regression tests for belt guard visuals in the Three.js viewer."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIEWER_HTML = PROJECT_ROOT / "viewer" / "index.html"


def test_viewer_mentions_snap_on_belt_guards() -> None:
    """Ensure the viewer describes the new snap-on belt guard elements."""
    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Snap-on belt guard — shields CoreXY belts" in html
    assert "Snap-On Belt Guards" in html
