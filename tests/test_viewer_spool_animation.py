"""Regression tests for spool animation cues in the viewer."""

from __future__ import annotations

from .viewer_source import load_viewer_bundle


def test_viewer_animates_spools_during_yarn_feed() -> None:
    """The viewer should animate spools with extrusion-aware speed changes."""

    viewer_source = load_viewer_bundle()

    assert "const spoolControllers" in viewer_source
    assert "spoolControllers.push" in viewer_source
    assert "linkedToExtrusion" in viewer_source
    assert "rotationDelta = delta * currentSpeed" in viewer_source


def test_spool_progress_billboard_tracks_planner_totals() -> None:
    """The yarn-feed billboard should mirror spool progress updates."""

    viewer_source = load_viewer_bundle()

    assert "spoolProgressLabelController.update" in viewer_source
    assert "header: spoolProgressHeader" in viewer_source
    assert "formatBillboardFeedCountdown" in viewer_source
    assert "Next feeds: Awaiting Yarn Flow timing…" in viewer_source


def test_spool_progress_ring_pre_pulses_for_upcoming_feed() -> None:
    """The spool progress ring should glow ahead of the next feed pulse."""

    viewer_source = load_viewer_bundle()

    assert "feedPulseHighlight" in viewer_source
    assert "cableChainNextFeedSeconds" in viewer_source
    assert "feedPulseWave" in viewer_source


def test_spool_progress_countdown_ribbon_stays_pinned() -> None:
    """The spool billboard should keep a countdown ribbon above the reel."""

    viewer_source = load_viewer_bundle()

    assert "createSpoolCountdownLabel" in viewer_source
    assert "spoolCountdownLabelController" in viewer_source
    assert "Countdown ribbon" in viewer_source
