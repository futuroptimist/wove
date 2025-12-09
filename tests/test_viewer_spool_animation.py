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
    assert "rotationDelta = delta * currentSpeed" in html


def test_spool_progress_billboard_tracks_planner_totals() -> None:
    """The yarn-feed billboard should mirror spool progress updates."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "spoolProgressLabelController.update" in html
    assert "header: spoolProgressHeader" in html
    assert "formatBillboardFeedCountdown" in html
    assert "Next feeds: Awaiting Yarn Flow timing…" in html


def test_spool_progress_ring_pre_pulses_for_upcoming_feed() -> None:
    """The spool progress ring should glow ahead of the next feed pulse."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "feedPulseHighlight" in html
    assert "cableChainNextFeedSeconds" in html
    assert "feedPulseWave" in html


def test_spool_progress_countdown_ribbon_stays_pinned() -> None:
    """The spool billboard should keep a countdown ribbon above the reel."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "createSpoolCountdownLabel" in html
    assert "spoolCountdownLabelController" in html
    assert "Countdown ribbon" in html
