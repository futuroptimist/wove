"""Tests for the Three.js assembly viewer scene."""

import re
from pathlib import Path

VIEWER_HTML = Path(__file__).resolve().parents[1] / "viewer" / "index.html"


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


def test_viewer_mentions_cooling_fan_mount() -> None:
    """The hook carriage cooling fan mount should be called out."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "Cooling fan mount" in html
    assert "20 mm fan" in html


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


def test_source_spool_rest_state_when_idle() -> None:
    """Ensure the supply spool stops rotating whenever extrusion pauses."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    position = html.find("linkedToExtrusion: true")
    assert position != -1

    block_start = html.rfind("spoolControllers.push({", 0, position)
    assert block_start != -1
    block_end = html.find("});", position)
    assert block_end != -1

    config_block = html[block_start:block_end]
    assert re.search(r"idleSpeed:\s*0(?:\.0+)?", config_block)
