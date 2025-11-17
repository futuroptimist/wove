"""Tests for the Three.js assembly viewer scene."""

import json
from pathlib import Path

VIEWER_HTML = Path(__file__).resolve().parents[1] / "viewer" / "index.html"
PLANNER_ASSET = (
    Path(__file__).resolve().parents[1]
    / "viewer"
    / "assets"
    / "base_chain_row.planner.json"
)


def test_workpiece_support_bed_is_documented() -> None:
    """The v1c assembly should highlight the workpiece support bed."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "workpiece support bed" in html.lower()


def test_hall_effect_sensor_is_documented() -> None:
    """The viewer should surface the hall-effect yarn tension sensor."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "hall-effect tension sensor" in html.lower()


def test_pattern_planner_preview_is_documented() -> None:
    """The Pattern Studio hologram should advertise the planner preview."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "assets/base_chain_row.planner.json" in html
    assert "base chain row" in html.lower()
    assert "pattern_cli --format planner" in html


def test_pattern_preview_overlay_panel_present() -> None:
    """The overlay should expose the Pattern Studio preview panel."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Pattern Studio Preview" in html
    assert "pattern-step-index" in html
    assert "Planner preview warming up." in html


def test_base_chain_row_embeds_machine_profile_axes() -> None:
    """The sample planner asset should include machine profile metadata."""

    payload = json.loads(PLANNER_ASSET.read_text(encoding="utf-8"))

    machine_profile = payload.get("machine_profile")
    assert machine_profile is not None
    assert "axes" in machine_profile

    axes = {name.lower(): axis for name, axis in machine_profile["axes"].items()}
    for axis in ("x", "y", "z", "e"):
        assert axis in axes

    assert axes["x"]["steps_per_mm"] == 80.0
    assert axes["x"]["travel_max_mm"] == 220.0
    assert axes["z"]["steps_per_mm"] == 400.0
    assert axes["e"]["steps_per_mm"] == 95.0


def test_viewer_documents_planner_bounds_overlay() -> None:
    """The overlay should advertise the planner bounds helper."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "pattern-bounds" in html
    assert "Planner bounds warming up…" in html
    assert "Planner bounds overlay" in html


def test_homing_guard_streams_coordinates() -> None:
    """The Homing Guard panel should advertise the coordinate stream."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "homing-guard-position" in html
    assert "Coordinates: Awaiting planner coordinates…" in html


def test_viewer_mentions_cooling_fan_mount() -> None:
    """The hook carriage cooling fan mount should be called out."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "Cooling fan mount" in html
    assert "20 mm fan" in html


def test_viewer_animates_cooling_fans() -> None:
    """Cooling fans should spin alongside yarn feed events."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "const fanControllers" in html
    assert "fanControllers.push" in html
    assert "fanControllers.forEach" in html


def test_viewer_highlights_tension_post_and_ptfe_path() -> None:
    """The Three.js viewer advertises the tension post and PTFE guide tube."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "Tension Post & PTFE Guide" in html
    assert "PTFE guide tube" in html


def test_tension_lab_mentions_servo_adjuster() -> None:
    """The Tension Lab display should mention the servo tension adjuster."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "Micro-servo tension adjuster" in html
    assert "Servo Tensioner Prototype" in html


def test_viewer_animates_servo_adjuster() -> None:
    """Servo controllers should pulse in sync with yarn feed events."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "const servoActuatorControllers" in html
    assert "servoActuatorControllers.push" in html
    assert "servoSignalControllers.push" in html


def test_viewer_mentions_selection_ring_glow() -> None:
    """The viewer should document the pulsing roadmap selection ring."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    selection_ring_copy = " ".join(
        [
            "Roadmap selection ring — pulses to mark the active product",
            "cluster.",
        ]
    )
    assert selection_ring_copy in html


def test_anchor_pucks_sequence_glow() -> None:
    """Anchor pucks should document the sequential guidance animation."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "anchorPulseControllers = []" in html
    assert "phaseOffset: index / anchorOffsets.length" in html
    assert "anchorPulseControllers.forEach" in html


def test_viewer_mentions_selection_sweep() -> None:
    """Ensure the viewer copy mentions the rotating cluster sweep."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    selection_sweep_copy = " ".join(
        [
            "Roadmap sweep — rotates around the selected cluster",
            "for quick focus.",
        ]
    )
    assert selection_sweep_copy in html


def test_viewer_glides_camera_to_selected_cluster() -> None:
    """Selecting a cluster should mention the camera glide helper."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "watch the camera glide to frame it" in html
    assert "const desiredCameraTarget" in html
    assert "cameraMoveDamping" in html


def test_viewer_highlights_machine_profile_panel() -> None:
    """The Machine Profile overlay should document axis metadata."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Machine Profile" in html
    assert (
        "Machine Profile panel mirrors axis steps/mm, microstepping, and travel bounds "
        "from" in html
    )


def test_viewer_supports_keyboard_cluster_navigation() -> None:
    """Arrow keys should cycle roadmap milestones."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Press ←/→ to cycle roadmap milestones without leaving the keyboard." in html
    assert "window.addEventListener('keydown'" in html
    assert "event.key === 'ArrowRight'" in html


def test_viewer_mentions_thermistor_channel() -> None:
    """Ensure the overlay documents the heated-bed thermistor channel."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert (
        "Thermistor channel — reserved wiring path for the future heated bed "
        "accessory." in html
    )
    assert "Thermistor Channel" in html


def test_viewer_highlights_cable_chain() -> None:
    """Ensure the viewer documents the cable chain wiring route."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Cable Chain" in html
    assert (
        "Cable chain — routes gantry wiring from the electronics bay to "
        "the hook carriage." in html
    )


def test_viewer_uses_trio_of_yarn_pulses() -> None:
    """The yarn pulse animation should emit three glowing trails."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "const pulseCount = 3" in html


def test_viewer_limits_yarn_beads_to_trio() -> None:
    """Ensure the yarn bead queue renders exactly three glowing orbs."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "const beadCount = 3" in html


def test_yarn_flow_panel_includes_totals() -> None:
    """The Yarn Flow overlay should advertise cumulative feed guidance."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "yarn-flow-total" in html
    assert "Total yarn fed: Awaiting planner preview…" in html
    assert "yarn-flow-queue" in html
    assert "Remaining feed pulses: Awaiting planner preview…" in html
    assert "yarn-flow-upcoming" in html
    assert "Next feed pulses: Awaiting planner preview…" in html
    assert "yarn-flow-timing" in html
    assert "Feed timing: Awaiting planner preview…" in html
    assert "yarn-flow-position" in html
    assert "Coordinates: Awaiting yarn flow coordinates…" in html
    assert "yarnFlowPositionElement" in html
    assert "Coordinates: ${positionSegments.join(' · ')}" in html
    assert "yarnFlowTimingElement" in html
    assert "Feed timing: No additional feed pulses in this preview." in html
    assert "Next in ${next.delta.toFixed(1)} s (#${next.step + 1})" in html


def test_yarn_flow_panel_interpolates_coordinates() -> None:
    """Live yarn flow coordinates should interpolate between planner points."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "function interpolatePlannerEventCoordinates" in html
    assert "interpolatedPosition?.x ?? event.x" in html
    assert "interpolatedPosition?.extrusion ?? event.extrusion" in html


def test_yarn_flow_panel_mentions_spool_progress() -> None:
    """Ensure the Yarn Flow overlay calls out spool progress guidance."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "yarn-flow-progress" in html
    assert "Spool progress: Awaiting planner preview…" in html


def test_yarn_flow_panel_reports_cycle_timing() -> None:
    """Ensure the Yarn Flow overlay surfaces cycle timing cues."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "yarn-flow-cycle" in html
    assert "Cycle timing: Awaiting planner preview…" in html
    assert (
        "Cycle timing: ${elapsedSeconds.toFixed(1)} s elapsed · "
        "${remainingSeconds.toFixed(1)} s remaining." in html
    )


def test_viewer_builds_spool_progress_ring() -> None:
    """The 3D scene should describe the spool progress indicator."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "const spoolProgressSegments" in html
    assert "spoolProgressSegments.push" in html
    assert "spoolProgressSegments.forEach" in html
    progress_copy = " ".join(
        [
            "Spool progress ring — fills as the planner feeds yarn",
            "around the supply reel.",
        ]
    )
    assert progress_copy in html


def test_viewer_attaches_yarn_feed_billboard() -> None:
    """The spool should host the yarn feed progress billboard."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert (
        "Yarn feed progress display — projects live feed vs planned yarn totals."
        in html
    )
    assert "spoolProgressLabelController = spoolProgressBillboard" in html


def test_viewer_mentions_z_axis_leadscrew() -> None:
    """The scene should describe the Z-axis leadscrew lift assembly."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "Z-axis T8 leadscrew" in html
    assert "Anti-backlash nut — preloads the Z carriage" in html
    assert "Compact Z stepper" in html


def test_viewer_highlights_axis_orientation_beacons() -> None:
    """Axis orientation beacons should be documented for navigation."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "axis-orientation-beacons" in html
    x_beacon_copy = " ".join(
        (
            "X-axis beacon — points toward positive X travel along the",
            "gantry.",
        )
    )
    assert x_beacon_copy in html
    assert "Axis Orientation Beacons" in html
