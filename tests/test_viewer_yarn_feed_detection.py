"""Ensure the Yarn Flow overlays follow extrusion-based feed detection."""

from __future__ import annotations

from pathlib import Path


def test_viewer_computes_feed_indices_from_extrusion() -> None:
    """The viewer should derive feed pulses from extrusion deltas."""

    html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert "computeYarnFeedIndices" in html
    assert "extrusionDelta" in html
    assert "extrusionFeeds || commentFeeds" in html


def test_viewer_applies_feed_index_helper() -> None:
    """Planner loads should reuse the extrusion-aware feed helper."""

    html = Path("viewer/index.html").read_text(encoding="utf-8")

    assert "yarnFeedStepIndices = computeYarnFeedIndices(" in html
    assert "patternExtrusionBaseline" in html
