"""Ensure the Three.js viewer ships the base chain row planner preview."""

from __future__ import annotations

import json
from pathlib import Path

from .viewer_source import load_viewer_bundle

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PREVIEW_NAME = "base_chain_row.planner.json"
VIEWER_PREVIEW_ROOT = PROJECT_ROOT / "viewer" / "assets"
FIXTURE_PREVIEW_ROOT = PROJECT_ROOT / "tests" / "fixtures" / "patterns"
VIEWER_PREVIEW = VIEWER_PREVIEW_ROOT / PREVIEW_NAME
FIXTURE_PREVIEW = FIXTURE_PREVIEW_ROOT / PREVIEW_NAME


def test_viewer_planner_preview_matches_fixture() -> None:
    """The viewer asset should mirror the base chain row planner fixture."""

    assert VIEWER_PREVIEW.exists()
    assert FIXTURE_PREVIEW.exists()
    viewer_preview = VIEWER_PREVIEW.read_text(encoding="utf-8")
    fixture_preview = FIXTURE_PREVIEW.read_text(encoding="utf-8")

    assert viewer_preview == fixture_preview


def test_viewer_planner_preview_includes_duration_metadata() -> None:
    """The base chain row preview should publish loop duration metadata."""

    payload = json.loads(VIEWER_PREVIEW.read_text(encoding="utf-8"))

    metadata = payload.get("metadata") or {}
    assert metadata.get("duration_seconds") == 14.0
    assert metadata.get("source") == "pattern_cli preview"


def test_viewer_planner_preview_includes_tension_calibration() -> None:
    """Tension telemetry should ship with hall sensor calibration hints."""

    payload = json.loads(VIEWER_PREVIEW.read_text(encoding="utf-8"))

    defaults = payload.get("defaults") or {}
    calibration = defaults.get("tension_sensor_calibration")
    assert calibration
    assert calibration.get("pairs") == [
        [102.0, 20.0],
        [168.5, 55.0],
        [220.0, 85.0],
    ]

    readings = [
        entry.get("state", {}).get("tension_sensor_reading")
        for entry in payload.get("commands", [])
        if isinstance(entry, dict)
    ]

    assert any(readings)
    assert min(readings) >= 0


def test_viewer_planner_preview_includes_heated_bed_conduit() -> None:
    """Heated bed conduit metadata should ride alongside planner defaults."""

    payload = json.loads(VIEWER_PREVIEW.read_text(encoding="utf-8"))

    defaults = payload.get("defaults") or {}
    conduit = defaults.get("heated_bed_conduit") or {}

    assert (
        conduit.get("status")
        == "Ready — thermistor conduit illuminated for the bay-to-bed wiring run"
    )
    assert (
        conduit.get("route")
        == "Bay-to-bed thermistor channel glows when planner metadata is ready."
    )


def test_viewer_exposes_planner_defaults_panel() -> None:
    """The overlay should advertise the planner defaults list."""

    html = load_viewer_bundle()

    assert "pattern-defaults-status" in html
    assert "Loading planner defaults…" in html
    assert "Planner defaults unavailable." in html


def test_viewer_ships_fallback_pattern_defaults() -> None:
    """Ensure fallback planner defaults include feed rate metadata."""

    html = load_viewer_bundle()

    assert "fallbackPatternDefaults" in html
    assert "travel_feed_rate_mm_min" in html
    assert "default_row_height_mm" in html
    assert "yarnFlowStatusFallbackMessage" in html
    assert "yarnFlowSpoolFallbackMessage" in html
    assert "plannerMetadataFallbackMessage" in html


def test_planner_defaults_panel_mentions_homing_guard() -> None:
    """The planner defaults overlay should echo homing guard metadata."""

    html = load_viewer_bundle()

    assert "Homing guard" in html
    assert "Optional for this planner preview" in html
    assert "Recorded home state" in html


def test_planner_defaults_panel_highlights_row_spacing() -> None:
    """Row spacing should appear alongside other planner defaults."""

    html = load_viewer_bundle()

    assert "Row spacing" in html
    assert "row_spacing_mm" in html


def test_yarn_flow_panel_mentions_spool_progress() -> None:
    """Ensure the Yarn Flow overlay advertises spool progress guidance."""

    html = load_viewer_bundle()

    assert "yarn-flow-progress" in html
    assert "Spool progress: Awaiting planner preview…" in html
    assert "yarnFlowProgressFallbackMessage" in html
    assert "Spool progress:" in html


def test_yarn_flow_panel_surfaces_calibration_hint() -> None:
    """Hall sensor calibration guidance should ride alongside yarn flow cues."""

    html = load_viewer_bundle()

    assert "yarn-flow-calibration" in html
    assert "Calibration: Awaiting tension sensor calibration metadata." in html
    assert "tension_sensor_calibration" in html


def test_planner_metadata_panel_mentions_duration() -> None:
    """The metadata overlay should surface preview duration guidance."""

    html = load_viewer_bundle()

    assert "Preview duration" in html


def test_planner_bounds_cage_highlights_z_span() -> None:
    """The planner overlay should expose the 3D bounds cage for Z coverage."""

    html = load_viewer_bundle()

    assert "planner-bounds-cage" in html
    assert "displayZMin" in html


def test_homing_guard_coordinates_follow_progress() -> None:
    """The homing guard panel should track interpolated coordinates."""

    html = load_viewer_bundle()

    assert "homing-guard-position" in html
    assert (
        "shouldUpdatePosition && (patternPositionElement || homingGuardPositionElement)"
        in html
    )


def test_spool_progress_ring_pauses_without_target() -> None:
    """When no target is supplied, the progress ring should pause and warn viewers."""

    html = load_viewer_bundle()

    assert "progress ring paused until planner target provided" in html


def test_spool_countdown_ribbon_surfaces_cycle_pacing() -> None:
    """The countdown ribbon should stack cycle pacing beneath feed timing."""

    html = load_viewer_bundle()

    assert "spoolProgressCountdownFallbackMessage" in html
    assert "yarnFlowCycleFallbackMessage" in html
    assert "const countdownLines = [lastSpoolCountdownSummary];" in html
    assert "countdownLines.push(lastSpoolCycleTimingDetail);" in html
    assert "lastSpoolCycleTimingDetail = yarnFlowCycleFallbackMessage;" in html
