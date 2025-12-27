"""Verify the anchor swap choreography described in the viewer roadmap."""

from __future__ import annotations

import re

from .viewer_source import load_viewer_bundle


def test_anchor_sweep_starts_from_rear_left_and_moves_clockwise() -> None:
    """The anchor halos should start at the rear-left puck and sweep clockwise."""

    viewer_source = load_viewer_bundle()
    match = re.search(r"const anchorOffsets = \[(.*?)\];", viewer_source, re.DOTALL)

    assert match, "anchorOffsets block missing"

    offsets = re.findall(r"\[\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\s*\]", match.group(1))

    assert offsets == [
        ("-1.8", "-1.0"),
        ("-1.8", "1.2"),
        ("1.8", "1.2"),
        ("1.8", "-1.0"),
    ]


def test_anchor_hover_callout_matches_sweep_story() -> None:
    """The hover text should explain the clockwise swap choreography."""

    viewer_source = load_viewer_bundle()

    assert (
        "rear-left puck kicks off the clockwise halo" in viewer_source
    ), "anchor hover text should highlight sweep starting point"
