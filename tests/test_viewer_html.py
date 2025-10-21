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


def test_viewer_declares_product_clusters() -> None:
    """Ensure the viewer script ships the product cluster pedestals."""

    viewer_html = (
        Path(__file__).resolve().parents[1] / "viewer" / "index.html"
    ).read_text(encoding="utf-8")

    for snippet in [
        "const productClusters = []",
        "function createPedestalCluster",
        "Tension Lab",
        "Material Prep Pod",
        "Pattern Studio",
        "v1k Research Rig",
        "function createMaterialPrepDisplay",
        "function createV1KResearchDisplay",
    ]:
        assert snippet in viewer_html


def test_viewer_includes_safety_shield() -> None:
    """Ensure the viewer documents the polycarbonate safety enclosure."""

    viewer_html = (
        Path(__file__).resolve().parents[1] / "viewer" / "index.html"
    ).read_text(encoding="utf-8")

    assert "Polycarbonate Shield" in viewer_html
