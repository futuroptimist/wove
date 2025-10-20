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
        "Pattern Studio",
        "v1k Research Rig",
    ]:
        assert snippet in viewer_html


def test_viewer_highlights_lab_and_studio_details() -> None:
    """Check that the viewer narrates the new lab and studio displays."""

    viewer_html = (
        Path(__file__).resolve().parents[1] / "viewer" / "index.html"
    ).read_text(encoding="utf-8")

    # fmt: off
    expected_snippets = (
        (
            "Calibration bench — stages load cells and fixture rails for yarn "
            "testing."
        ),
        (
            "Tension lab pedestal — stage load cells and spool "
            "fixtures before gantry trials."
        ),
        (
            "Tension spool rig — calibrates hall-effect sensors before "
            "they reach production cells."
        ),
        (
            "Planner console — previews pattern_cli exports with motion "
            "overlays."
        ),
        (
            "Holographic planner table — projects stitch simulations for "
            "operator dry runs."
        ),
    )
    # fmt: on

    for snippet in expected_snippets:
        assert snippet in viewer_html
