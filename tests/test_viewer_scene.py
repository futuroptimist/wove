"""Tests for the Three.js assembly viewer scene."""

import ast
import json
import re
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


def test_calibration_rail_sweep_is_documented() -> None:
    """The calibration rail animation should be called out in the overlay."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "dashed calibration rail sweep" in html.lower()


def test_anchor_pulse_sequence_runs_clockwise() -> None:
    """The magnetic anchor sweep should follow the clockwise swap order."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    match = re.search(r"const anchorOffsets = \[(.*?)\];", html, re.DOTALL)
    assert match is not None

    anchor_pattern = r"\[\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\s*\]"
    pairs = re.findall(anchor_pattern, match.group(1))
    offsets = [(float(x), float(z)) for x, z in pairs]

    assert offsets == [(-1.8, 1.2), (1.8, 1.2), (1.8, -1.0), (-1.8, -1.0)]


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


def test_machine_profile_envelope_mentions_extrusion_axis() -> None:
    """The machine profile envelope helper should surface the E-axis bounds."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Machine profile envelope: " in html
    assert "E ${bounds.e.min.toFixed(1)}–${bounds.e.max.toFixed(1)} mm" in html


def test_viewer_documents_planner_bounds_overlay() -> None:
    """The overlay should advertise the planner bounds helper."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "pattern-bounds" in html
    assert "Planner bounds warming up…" in html
    assert "Planner bounds overlay" in html


def test_planner_bounds_cage_highlights_z_span() -> None:
    """The bounds cage should spotlight the mint Z-span markers."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "planner-bounds-cage" in html
    assert (
        "Mint bounds cage — tracks the planner Z span above the preview plane." in html
    )
    assert "Z-span beacon — mint column spotlights the planner clearance band." in html
    assert (
        "Z-span markers — twin halos pulse at the planner min and max heights." in html
    )
    assert "boundsCageControllers" in html
    assert "boundsZMarkerControllers" in html


def test_homing_guard_streams_coordinates() -> None:
    """The Homing Guard panel should advertise the coordinate stream."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "homing-guard-position" in html
    assert "Coordinates: Awaiting planner coordinates…" in html


def test_heated_bed_conduit_panel_present() -> None:
    """Heated bed conduit status should surface alongside the overlay panels."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Heated Bed Conduit" in html
    assert "Thermistor conduit reserved for the heater upgrade" in html
    assert "bay-to-bed run" in html


def test_yarn_flow_surface_feed_rate_copy() -> None:
    """Yarn flow telemetry should include live feed-rate messaging."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "yarn-flow-rate" in html
    assert "Feed rate: Awaiting yarn feed telemetry…" in html


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


def test_controller_stack_leds_breathe_at_idle() -> None:
    """Electronics bay LEDs should pulse even when the yarn feed is idle."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert re.search(
        r"controllerStackGlowControllers\.push\(\{[^}]*idlePulseStrength",
        html,
        re.DOTALL,
    )


def test_viewer_highlights_tension_post_and_ptfe_path() -> None:
    """The Three.js viewer advertises the tension post and PTFE guide tube."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "Tension Post & PTFE Guide" in html
    assert "PTFE guide tube" in html


def test_viewer_surfaces_filament_break_sensor() -> None:
    """Optional filament break detection should be documented in the viewer."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "filamentSensorControllers" in html
    assert "Filament break sensor — optional inline detector" in html
    assert "Filament Break Sensor" in html


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


def test_servo_status_orb_tracks_yarn_feed() -> None:
    """The servo status orb should advertise its feed-synced brightness."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "Servo status orb — brightens with yarn feed pulses" in html
    assert "light: servoLight" in html


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

    swap_copy = (
        "Anchor swap order sweep — follow the clockwise halo " "to swap plates safely."
    )

    assert "anchorPulseControllers = []" in html
    assert swap_copy in html
    assert "sequenceDuration" in html
    assert "sequenceIndex" in html


def test_anchor_pucks_sequence_runs_clockwise() -> None:
    """Anchor pulses should follow the clockwise swap choreography."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    match = re.search(r"const anchorOffsets = \[(.*?)\];", html, flags=re.DOTALL)
    assert match is not None

    offsets = ast.literal_eval(f"[{match.group(1)}]")
    assert isinstance(offsets, list)
    assert len(offsets) >= 3

    area = 0.0
    for index, (x1, z1) in enumerate(offsets):
        x2, z2 = offsets[(index + 1) % len(offsets)]
        area += x1 * z2 - x2 * z1

    assert area < 0, "anchor offsets should wind clockwise"


def test_safe_access_path_drives_footstep_cadence() -> None:
    """Safe access footprints should animate a lift cadence across the path."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "const footstepControllers" in html
    assert "footstepControllers.push" in html
    assert "footprint.position.y = baseHeight + lift" in html
    assert "toe.position.y = baseToeHeight + lift * 0.82" in html


def test_z_lift_shimmers_with_yarn_feed() -> None:
    """The Z-axis lift should glow in sync with yarn feed pulses."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "const zLiftGlowControllers" in html
    assert "zLiftGlowControllers.push" in html
    assert "zLiftGlowControllers.forEach" in html


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


def test_spool_billboard_tracks_following_feed() -> None:
    """The spool billboard should echo next and following feed countdowns."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Following in" in html


def test_spool_progress_ring_pre_pulse_documented() -> None:
    """The spool ring should call out the pre-pulse sweep before feed events."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "pre-pulse sweep wraps the ring" in html
    assert "spoolPrePulseSettings" in html


def test_viewer_supports_keyboard_cluster_navigation() -> None:
    """Arrow keys should cycle roadmap milestones."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Press ←/→ to cycle roadmap milestones without leaving the keyboard." in html
    assert "window.addEventListener('keydown'" in html
    assert "event.key === 'ArrowRight'" in html


def test_homing_guard_verifies_homed_cycles() -> None:
    """Homing Guard should acknowledge a verified homing capture."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "planner captured a verified homing cycle" in html


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
        "Cable chain — routes gantry wiring to the hook carriage with a "
        "chasing glow." in html
    )


def test_cable_chain_chases_with_feed_pulses() -> None:
    """Cable chain pulses should be controlled by a dedicated animation loop."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "const cableChainPulseControllers" in html
    assert "cableChainPulseControllers.push" in html
    assert "cableChainPulseControllers.forEach" in html


def test_cable_chain_chase_orb_tracks_feed_queue() -> None:
    """Cable chain chase orb should anticipate upcoming yarn feed pulses."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "const cableChainChaseControllers" in html
    assert (
        "Cable chain chase orb — accelerates as yarn feed pulses approach the gantry."
        in html
    )
    assert "cableChainNextFeedSeconds" in html


def test_viewer_highlights_status_led_behavior() -> None:
    """The electronics bay status LED should advertise its pulsing behavior."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Status LED — breathes at idle and brightens with yarn feed pulses." in html


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


def test_yarn_flow_panel_reports_tension_telemetry() -> None:
    """The Yarn Flow overlay should surface estimated hall-sensor grams."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "yarn-flow-tension" in html
    assert "Tension telemetry: Awaiting planner preview…" in html
    assert "tension_sensor_calibration" in html
    assert "feed-rate estimate" in html


def test_calibration_lab_pedestal_documented() -> None:
    """The roadmap should include a calibration lab pedestal."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Calibration Lab" in html
    assert (
        "Calibration lab pedestal — validates hall sensors and load-cell fixtures."
        in html
    )


def test_yarn_flow_panel_reports_cycle_timing() -> None:
    """Ensure the Yarn Flow overlay surfaces cycle timing cues."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "yarn-flow-cycle" in html
    assert "Cycle pacing: Awaiting planner preview…" in html
    assert (
        "Cycle timing: ${elapsedSeconds.toFixed(1)} s elapsed · "
        "${remainingSeconds.toFixed(1)} s remaining." in html
    )


def test_tension_lab_traces_calibration_path() -> None:
    """The Tension Lab should visualize its automation sweep."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    automation_tooltip = (
        "Automation sweep — traces the load-cell carriage path across the calibration "
        "rail."
    )

    assert automation_tooltip in html
    assert "tensionLabPathControllers" in html


def test_spool_billboard_mirrors_cycle_pacing() -> None:
    """The spool billboard should echo the Yarn Flow cycle pacing."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert (
        "Cycle pacing: ${elapsedSeconds.toFixed(1)} s elapsed · "
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


def test_cable_chain_billboard_surfaces_countdowns() -> None:
    """Cable chain billboard should mirror feed countdowns and queue size."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "createCableChainBillboard" in html
    assert "Countdown: Awaiting planner preview…" in html
    assert "Remaining feeds: Queue clear." in html
    assert "Following pulse in" in html
    assert "Cycle pacing:" in html


def test_spool_progress_ring_shifts_with_tone() -> None:
    """Spool progress segments should react to Yarn Flow tones."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "spoolProgressTonePalette" in html
    assert "applySpoolProgressTone" in html
    assert "material.color.setHex(palette.color)" in html


def test_viewer_attaches_yarn_feed_billboard() -> None:
    """The spool should host the yarn feed progress billboard."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert (
        "Yarn feed progress display — projects live feed vs planned yarn totals."
        in html
    )
    assert "spoolProgressLabelController = spoolProgressBillboard" in html


def test_billboard_highlights_next_feed_countdown() -> None:
    """The spool billboard should surface the next yarn feed countdown copy."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Next feeds: Awaiting Yarn Flow timing…" in html
    assert "Next feeds: Queue clear." in html


def test_spool_billboard_reports_remaining_feeds() -> None:
    """The spool billboard should mirror the remaining feed queue length."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Remaining feeds: Awaiting planner preview…" in html
    assert "Remaining feeds: Queue clear." in html


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
