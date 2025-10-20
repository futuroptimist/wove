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


def test_viewer_populates_product_clusters() -> None:
    """The viewer should describe each roadmap pedestal."""

    viewer_html = (
        Path(__file__).resolve().parents[1] / "viewer" / "index.html"
    ).read_text(encoding="utf-8")

    for snippet in [
        "const clustersData = ",
        "v1c Crochet Robot",
        "Tension Lab",
        "Pattern Studio",
    ]:
        assert snippet in viewer_html
