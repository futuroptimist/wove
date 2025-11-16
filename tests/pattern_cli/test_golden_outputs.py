"""Golden motion regression snapshots for pattern_cli fixtures."""

import json
from pathlib import Path

import pytest

from wove.machine_profile import AxisProfile, MachineProfile
from wove.pattern_cli import PatternTranslator, _planner_payload

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures" / "patterns"


def _fixture_text(name: str, suffix: str) -> str:
    return (FIXTURE_DIR / f"{name}{suffix}").read_text(encoding="utf-8")


def _load_pattern(name: str) -> str:
    return _fixture_text(name, ".txt")


def _golden_machine_profile() -> MachineProfile:
    return MachineProfile(
        axes={
            "X": AxisProfile("X", 16, 80.0, 0.0, 220.0),
            "Y": AxisProfile("Y", 16, 80.0, 0.0, 220.0),
            "Z": AxisProfile("Z", 16, 400.0, -10.0, 120.0),
            "E": AxisProfile("E", 16, 95.0, 0.0, 1200.0),
        }
    )


def _generate_outputs(pattern_text: str):
    profile = _golden_machine_profile()
    translator = PatternTranslator(machine_profile=profile)
    lines = translator.translate(pattern_text)
    gcode = "\n".join(line.as_text() for line in lines) + "\n"
    json_payload = [line.as_dict() for line in lines]
    planner_payload = _planner_payload(
        translator.planner_events,
        machine_profile=profile,
    )
    return gcode, json_payload, planner_payload


def _fixture_names() -> list[str]:
    return sorted(entry.stem for entry in FIXTURE_DIR.glob("*.txt"))


@pytest.mark.parametrize("pattern_name", _fixture_names())
def test_gcode_matches_golden(pattern_name: str) -> None:
    pattern = _load_pattern(pattern_name)
    generated_gcode, _, _ = _generate_outputs(pattern)
    expected_gcode = _fixture_text(pattern_name, ".gcode")
    assert generated_gcode == expected_gcode


@pytest.mark.parametrize("pattern_name", _fixture_names())
def test_json_matches_golden(pattern_name: str) -> None:
    pattern = _load_pattern(pattern_name)
    _, json_payload, _ = _generate_outputs(pattern)
    expected_json = json.loads(_fixture_text(pattern_name, ".json"))
    assert json_payload == expected_json


@pytest.mark.parametrize("pattern_name", _fixture_names())
def test_planner_matches_golden(pattern_name: str) -> None:
    pattern = _load_pattern(pattern_name)
    _, _, planner_payload = _generate_outputs(pattern)
    expected_planner = json.loads(_fixture_text(pattern_name, ".planner.json"))
    assert planner_payload == expected_planner
