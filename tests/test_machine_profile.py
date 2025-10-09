# isort: skip_file

from __future__ import annotations

import json
import textwrap

import pytest

from wove.machine_profile import (
    AxisProfile,
    MachineProfile,
    load_machine_profile,
)


def _profile_payload() -> dict[str, dict[str, dict[str, float]]]:
    return {
        "axes": {
            "X": {
                "microstepping": 16,
                "steps_per_mm": 80,
                "travel_min_mm": 0,
                "travel_max_mm": 250,
            },
            "Y": {
                "microstepping": 16,
                "steps_per_mm": 80,
                "travel_min_mm": 0,
                "travel_max_mm": 200,
            },
            "Z": {
                "microstepping": 16,
                "steps_per_mm": 400,
                "travel_min_mm": -10,
                "travel_max_mm": 15,
            },
        }
    }


def test_load_machine_profile_json(tmp_path):
    profile_path = tmp_path / "machine.json"
    profile_path.write_text(
        json.dumps(_profile_payload()),
        encoding="utf-8",
    )
    profile = load_machine_profile(profile_path)
    assert isinstance(profile, MachineProfile)
    profile.ensure_within("X", 100.0)
    profile.ensure_within("Y", 150.0)
    profile.ensure_within("Z", 0.0)


def test_load_machine_profile_yaml(tmp_path):
    payload = textwrap.dedent(
        """
        axes:
          x:
            microstepping: 32
            steps_per_mm: 80
            travel_min_mm: 0
            travel_max_mm: 180
          Y:
            microstepping: 16
            steps_per_mm: 100
            min_mm: 0
            max_mm: 220
          Z:
            microstepping: 16
            steps_per_mm: 400
            travel_min_mm: -5
            travel_max_mm: 10
        """
    )
    profile_path = tmp_path / "machine.yaml"
    profile_path.write_text(payload, encoding="utf-8")
    profile = load_machine_profile(profile_path)
    assert profile.axes["X"].microstepping == 32
    assert profile.axes["Y"].steps_per_mm == 100
    profile.ensure_within("Z", -1.0)


def test_axis_profile_validate_range():
    axis = AxisProfile("X", 16, 80, 0.0, 10.0)
    axis.ensure_within(5.0)
    with pytest.raises(ValueError):
        axis.ensure_within(11.0, line_number=7)


def test_axis_profile_reports_generated_command():
    axis = AxisProfile("X", 16, 80, 0.0, 5.0)
    with pytest.raises(ValueError) as excinfo:
        axis.ensure_within(10.0)
    assert "generated command" in str(excinfo.value)


def test_load_machine_profile_rejects_invalid_range(tmp_path):
    payload = _profile_payload()
    payload["axes"]["X"]["travel_max_mm"] = -1
    profile_path = tmp_path / "machine.json"
    profile_path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_machine_profile(profile_path)


def test_load_machine_profile_requires_axes_mapping(tmp_path):
    payload = {"axes": None}
    profile_path = tmp_path / "machine.json"
    profile_path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        load_machine_profile(profile_path)
    assert "must contain an 'axes' mapping" in str(excinfo.value)


def test_machine_profile_requires_known_axis():
    profile = MachineProfile(axes={"X": AxisProfile("X", 16, 80, 0.0, 5.0)})
    with pytest.raises(ValueError) as excinfo:
        profile.ensure_within("Y", 1.0)
    assert "missing axis 'Y'" in str(excinfo.value)


def test_load_machine_profile_requires_mapping_payload(tmp_path):
    profile_path = tmp_path / "machine.json"
    profile_path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        load_machine_profile(profile_path)
    assert "top level" in str(excinfo.value)


def test_load_machine_profile_validates_axis_mappings(tmp_path):
    payload = {"axes": {"X": [1, 2, 3]}}
    profile_path = tmp_path / "machine.json"
    profile_path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        load_machine_profile(profile_path)
    assert "must map to an object" in str(excinfo.value)


def test_load_machine_profile_rejects_empty_axes(tmp_path):
    payload = {"axes": {}}
    profile_path = tmp_path / "machine.json"
    profile_path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        load_machine_profile(profile_path)
    assert "define at least one axis" in str(excinfo.value)
