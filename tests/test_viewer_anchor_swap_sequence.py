"""Verify the anchor swap choreography described in the viewer roadmap."""

from __future__ import annotations

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIEWER_HTML = PROJECT_ROOT / "viewer" / "index.html"


def test_anchor_sweep_starts_from_rear_left_and_moves_clockwise() -> None:
    """The anchor halos should start at the rear-left puck and sweep clockwise."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    match = re.search(r"const anchorOffsets = \[(.*?)\];", html, re.DOTALL)

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

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert (
        "rear-left puck kicks off the clockwise halo" in html
    ), "anchor hover text should highlight sweep starting point"
