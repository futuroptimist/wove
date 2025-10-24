"""Tests for the Three.js pattern preview data used by the viewer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from wove.pattern_cli import PatternTranslator

PATTERN_TEXT = "CHAIN 3\nPAUSE 0.4\nMOVE 18 5\nTURN 7\nSINGLE 1\n"


def load_viewer_events() -> list[dict[str, object]]:
    root = Path(__file__).resolve().parents[1]
    data_path = root / "viewer" / "assets" / "base_chain_row.planner.json"
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    commands = payload.get("commands", [])
    events: list[dict[str, object]] = []
    for entry in commands:
        state = entry.get("state") or {}
        events.append(
            {
                "comment": entry.get("comment"),
                "command": entry.get("command", ""),
                "x": float(state.get("x_mm", 0.0) or 0.0),
                "y": float(state.get("y_mm", 0.0) or 0.0),
                "z": float(state.get("z_mm", 0.0) or 0.0),
                "extrusion": float(state.get("extrusion_mm", 0.0) or 0.0),
            }
        )
    return events


def normalize_event(event) -> dict[str, object]:
    """Return a simplified snapshot used for viewer assertions."""

    return {
        "comment": event.comment,
        "command": event.command,
        "x": event.x_mm,
        "y": event.y_mm,
        "z": event.z_mm,
        "extrusion": event.extrusion_mm,
    }


def test_viewer_planner_preview_matches_translator() -> None:
    viewer_events = load_viewer_events()

    translator = PatternTranslator()
    translator.translate(PATTERN_TEXT)
    translated_events = list(map(normalize_event, translator.planner_events))

    assert len(viewer_events) == len(translated_events)

    for viewer_entry, translated_entry in zip(
        viewer_events, translated_events, strict=True
    ):
        assert viewer_entry["comment"] == translated_entry["comment"]
        assert viewer_entry["command"] == translated_entry["command"]
        assert viewer_entry["x"] == pytest.approx(
            translated_entry["x"],
            abs=1e-6,
        )
        assert viewer_entry["y"] == pytest.approx(
            translated_entry["y"],
            abs=1e-6,
        )
        assert viewer_entry["z"] == pytest.approx(
            translated_entry["z"],
            abs=1e-6,
        )
        assert viewer_entry["extrusion"] == pytest.approx(
            translated_entry["extrusion"],
            abs=1e-6,
        )
