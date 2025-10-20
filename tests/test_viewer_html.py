"""Regression tests for the Three.js assembly viewer HTML."""

from __future__ import annotations

from pathlib import Path


def test_viewer_exposes_roadmap_panel() -> None:
    """Ensure the viewer documents the roadmap spotlight UI."""

    viewer_html = (
        Path(__file__).resolve().parents[1] / "viewer" / "index.html"
    ).read_text(encoding="utf-8")

    for snippet in [
        'id="roadmap-title"',
        "function selectCluster",
        "Click a pedestal to spotlight its roadmap milestone.",
    ]:
        assert snippet in viewer_html
