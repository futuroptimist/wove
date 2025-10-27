"""Tests for the Three.js pattern preview data used by the viewer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from wove.pattern_cli import PatternTranslator

ROOT = Path(__file__).resolve().parents[1]
PATTERN_FIXTURE = ROOT / Path("tests/fixtures/patterns/base_chain_row.txt")
PATTERN_TEXT = PATTERN_FIXTURE.read_text(encoding="utf-8")


def load_viewer_events() -> list[dict[str, object]]:
    """Load the planner commands consumed by the Three.js viewer."""

    asset_path = ROOT / "viewer" / "assets" / "base_chain_row.planner.json"
    payload = json.loads(asset_path.read_text(encoding="utf-8"))
    commands: list[dict[str, object]] = []
    if isinstance(payload, dict):
        commands = payload.get("commands", [])

    events: list[dict[str, object]] = []
    for entry in commands:
        if not isinstance(entry, dict):
            continue
        state = entry.get("state") or {}
        events.append(
            {
                "comment": entry.get("comment"),
                "command": entry.get("command"),
                "x": state.get("x_mm"),
                "y": state.get("y_mm"),
                "z": state.get("z_mm"),
                "extrusion": state.get("extrusion_mm"),
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


def test_load_viewer_events_skips_non_dict_entries(monkeypatch) -> None:
    """Ensure non-dictionary command entries are ignored when loading events."""

    asset_path = ROOT / "viewer" / "assets" / "base_chain_row.planner.json"

    def patched_read_text(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        assert self == asset_path
        return json.dumps(
            {
                "commands": [
                    9,
                    {
                        "comment": "valid entry",
                        "command": "G1",
                        "state": {
                            "x_mm": 1.0,
                            "y_mm": 2.0,
                            "z_mm": 3.0,
                            "extrusion_mm": 4.0,
                        },
                    },
                ]
            }
        )

    monkeypatch.setattr(Path, "read_text", patched_read_text)

    events = load_viewer_events()

    assert events == [
        {
            "comment": "valid entry",
            "command": "G1",
            "x": 1.0,
            "y": 2.0,
            "z": 3.0,
            "extrusion": 4.0,
        }
    ]


def test_load_viewer_events_ignores_non_dict_payload(monkeypatch) -> None:
    """A planner asset that is not a dictionary should return no events."""

    asset_path = ROOT / "viewer" / "assets" / "base_chain_row.planner.json"

    def patched_read_text(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        assert self == asset_path
        return json.dumps(["unexpected", "payload"])

    monkeypatch.setattr(Path, "read_text", patched_read_text)

    assert load_viewer_events() == []
