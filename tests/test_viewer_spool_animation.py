"""Regression tests for spool animation cues in the viewer."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIEWER_HTML = PROJECT_ROOT / "viewer" / "index.html"


def test_viewer_animates_spools_during_yarn_feed() -> None:
    """The viewer should animate spools with extrusion-aware speed changes."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "const spoolControllers" in html
    assert "spoolControllers.push" in html
    assert "linkedToExtrusion" in html
    assert "rotationDelta = delta * speed" in html
