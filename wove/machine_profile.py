"""Load motion-system profiles with axis limits for pattern planning."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping

import yaml


@dataclass(frozen=True)
class AxisProfile:
    """Describe controller parameters for a single axis."""

    name: str
    microstepping: int
    steps_per_mm: float
    travel_min_mm: float
    travel_max_mm: float

    def ensure_within(
        self, position_mm: float, *, line_number: int | None = None
    ) -> None:
        """Raise ``ValueError`` when ``position_mm`` exceeds travel limits."""

        if self.travel_min_mm <= position_mm <= self.travel_max_mm:
            return
        if line_number is None:
            location = "generated command"
        else:
            location = f"line {line_number}"
        message_parts = [
            (
                "Axis {} position {:.2f} mm exceeds travel range".format(
                    self.name,
                    position_mm,
                )
            ),
            f"{self.travel_min_mm:.2f}\u2013{self.travel_max_mm:.2f} mm",
            f"({location})",
        ]
        message = " ".join(message_parts)
        raise ValueError(message)


@dataclass(frozen=True)
class MachineProfile:
    """Axis definitions for a motion system."""

    axes: Dict[str, AxisProfile]

    def ensure_within(
        self, axis: str, position_mm: float, *, line_number: int | None = None
    ) -> None:
        """Ensure ``axis`` stays inside its configured travel range."""

        key = axis.upper()
        try:
            profile = self.axes[key]
        except KeyError as error:
            message = f"Machine profile is missing axis '{key}'"
            raise ValueError(message) from error
        profile.ensure_within(position_mm, line_number=line_number)


def _coerce_float(data: Mapping[str, Any], *keys: str) -> float:
    for key in keys:
        if key in data:
            value = data[key]
            break
    else:  # pragma: no cover - defensive
        raise KeyError(f"Missing one of keys: {', '.join(keys)}")
    try:
        return float(value)
    except (TypeError, ValueError) as error:  # pragma: no cover - defensive
        message = f"Expected a numeric value for {keys[0]}"
        raise ValueError(message) from error


def _coerce_int(data: Mapping[str, Any], key: str) -> int:
    if key not in data:  # pragma: no cover - defensive
        raise KeyError(f"Missing key: {key}")
    try:
        return int(data[key])
    except (TypeError, ValueError) as error:  # pragma: no cover - defensive
        message = f"Expected an integer value for {key}"
        raise ValueError(message) from error


def _axis_from_mapping(name: str, payload: Mapping[str, Any]) -> AxisProfile:
    microstepping = _coerce_int(payload, "microstepping")
    steps_per_mm = _coerce_float(payload, "steps_per_mm")
    travel_min_mm = _coerce_float(payload, "travel_min_mm", "min_mm", "min")
    travel_max_mm = _coerce_float(payload, "travel_max_mm", "max_mm", "max")
    if travel_max_mm <= travel_min_mm:
        message = "Axis {} has invalid travel range {} to {}".format(
            name,
            travel_min_mm,
            travel_max_mm,
        )
        raise ValueError(message)
    return AxisProfile(
        name=name,
        microstepping=microstepping,
        steps_per_mm=steps_per_mm,
        travel_min_mm=travel_min_mm,
        travel_max_mm=travel_max_mm,
    )


def _machine_profile_from_mapping(
    payload: Mapping[str, Any],
) -> MachineProfile:
    axes_payload = payload.get("axes")
    if not isinstance(axes_payload, Mapping):
        raise ValueError("Machine profile must contain an 'axes' mapping")
    axes: Dict[str, AxisProfile] = {}
    for raw_name, axis_data in axes_payload.items():
        if not isinstance(axis_data, Mapping):
            message = f"Axis '{raw_name}' must map to an object"
            raise ValueError(message)
        name = str(raw_name).upper()
        axes[name] = _axis_from_mapping(name, axis_data)
    if not axes:
        raise ValueError("Machine profile must define at least one axis")
    return MachineProfile(axes=axes)


def load_machine_profile(path: str | Path) -> MachineProfile:
    """Load a machine profile from JSON or YAML at ``path``."""

    profile_path = Path(path)
    try:
        raw_text = profile_path.read_text(encoding="utf-8")
    except OSError as error:  # pragma: no cover - exercised in CLI tests
        message = "Unable to read machine profile: {}".format(error)
        raise ValueError(message) from error

    suffix = profile_path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        payload = yaml.safe_load(raw_text) or {}
    else:
        payload = json.loads(raw_text)
    if not isinstance(payload, Mapping):
        message_parts = [
            "Machine profile file must contain an object",
            "at the top level",
        ]
        raise ValueError(" ".join(message_parts))
    return _machine_profile_from_mapping(payload)


__all__ = ["AxisProfile", "MachineProfile", "load_machine_profile"]
