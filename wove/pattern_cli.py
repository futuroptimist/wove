"""Translate simple crochet stitch descriptions into G-code-like motion."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple
from xml.etree import ElementTree as ET

import yaml

SAFE_Z_MM = 4.0
FABRIC_PLANE_Z_MM = 0.0
TRAVEL_FEED_RATE = 1200
PLUNGE_FEED_RATE = 600
YARN_FEED_RATE = 300
DEFAULT_ROW_HEIGHT = 6.0


@dataclass(frozen=True)
class GCodeLine:
    """A single G-code-like instruction with an optional trailing comment."""

    command: str
    comment: str | None = None

    def as_text(self) -> str:
        if self.comment:
            return f"{self.command} ; {self.comment}"
        return self.command

    def as_dict(self) -> dict[str, str]:
        data = {"command": self.command}
        if self.comment:
            data["comment"] = self.comment
        return data


@dataclass(frozen=True)
class StitchProfile:
    """Describe how to render a stitch in the generated motion sequence."""

    name: str
    spacing_mm: float
    plunge_depth_mm: float
    yarn_feed_mm: float


@dataclass(frozen=True)
class AxisProfile:
    """Travel and calibration data for a single axis."""

    min_mm: float
    max_mm: float
    microstepping: int
    steps_per_mm: float

    def ensure_within(self, axis_label: str, value: float) -> None:
        if value < self.min_mm or value > self.max_mm:
            message = (
                f"{axis_label} value {value:.2f} mm exceeds allowed range "
                f"{self.min_mm:.2f}–{self.max_mm:.2f} mm from machine profile"
            )
            raise ValueError(message)

    def as_dict(self) -> Dict[str, float | int]:
        return {
            "min_mm": self.min_mm,
            "max_mm": self.max_mm,
            "microstepping": self.microstepping,
            "steps_per_mm": self.steps_per_mm,
        }


@dataclass(frozen=True)
class MachineProfile:
    """Machine calibration profile describing each axis."""

    axes: Dict[str, AxisProfile]

    def axis(self, name: str) -> AxisProfile | None:
        return self.axes.get(name.lower())

    def as_dict(self) -> Dict[str, Dict[str, float | int]]:
        result: Dict[str, Dict[str, float | int]] = {}
        for axis, profile in sorted(self.axes.items()):
            result[axis] = profile.as_dict()
        return result


STITCH_PROFILES = {
    "CHAIN": StitchProfile(
        "CHAIN",
        spacing_mm=5.0,
        plunge_depth_mm=1.5,
        yarn_feed_mm=0.5,
    ),
    "SINGLE": StitchProfile(
        "SINGLE",
        spacing_mm=4.5,
        plunge_depth_mm=2.0,
        yarn_feed_mm=0.6,
    ),
    "DOUBLE": StitchProfile(
        "DOUBLE",
        spacing_mm=5.5,
        plunge_depth_mm=2.5,
        yarn_feed_mm=0.7,
    ),
}


def load_machine_profile(path: Path) -> MachineProfile:
    """Load a machine profile from JSON or YAML."""

    raw_mapping = _read_machine_profile_mapping(path)
    axes_data = raw_mapping.get("axes")
    if not isinstance(axes_data, dict) or not axes_data:
        message = f"Machine profile {path} must define an 'axes' mapping"
        raise ValueError(message)
    axes: Dict[str, AxisProfile] = {}
    for axis_name, raw_axis in axes_data.items():
        if not isinstance(raw_axis, dict):
            message = f"Axis '{axis_name}' in {path} must be a mapping"
            raise ValueError(message)
        min_raw = raw_axis.get("min_mm", 0.0)
        try:
            max_raw = raw_axis["max_mm"]
            microstepping_raw = raw_axis["microstepping"]
            steps_per_mm_raw = raw_axis["steps_per_mm"]
        except KeyError as error:
            missing = error.args[0]
            message = "Axis '{}' in {} is missing '{}'".format(
                axis_name,
                path,
                missing,
            )
            raise ValueError(message) from error
        try:
            min_mm = float(min_raw)
            max_mm = float(max_raw)
            steps_per_mm = float(steps_per_mm_raw)
        except (TypeError, ValueError) as error:
            message = (
                f"Axis '{axis_name}' in {path} must provide numeric limits "
                "and steps_per_mm"
            )
            raise ValueError(message) from error
        try:
            microstepping = int(microstepping_raw)
        except (TypeError, ValueError) as error:
            message = (
                f"Axis '{axis_name}' in {path} must provide an integer "
                "microstepping value"
            )
            raise ValueError(message) from error
        if microstepping <= 0:
            template = "Axis '{}' in {} must declare positive microstepping"
            message = template.format(axis_name, path)
            raise ValueError(message)
        if steps_per_mm <= 0:
            template = "Axis '{}' in {} must declare positive steps_per_mm"
            message = template.format(axis_name, path)
            raise ValueError(message)
        if max_mm <= min_mm:
            template = "Axis '{}' in {} must have max_mm greater than min_mm"
            message = template.format(axis_name, path)
            raise ValueError(message)
        axes[axis_name.lower()] = AxisProfile(
            min_mm=min_mm,
            max_mm=max_mm,
            microstepping=microstepping,
            steps_per_mm=steps_per_mm,
        )
    return MachineProfile(axes=axes)


def _read_machine_profile_mapping(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as error:  # pragma: no cover
            message = f"Failed to parse YAML machine profile {path}"
            raise ValueError(message) from error
    else:
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            try:
                data = yaml.safe_load(text)
            except yaml.YAMLError as yaml_error:
                message = f"Machine profile {path} is not valid JSON or YAML"
                raise ValueError(message) from yaml_error
            else:
                if data is None:
                    message = f"Machine profile {path} is empty"
                    raise ValueError(message)
        else:
            if data is None:
                message = f"Machine profile {path} is empty"
                raise ValueError(message)
    if not isinstance(data, dict):
        message = f"Machine profile {path} must decode to a mapping"
        raise ValueError(message)
    return data


def _format_machine_profile_comment(machine_profile: MachineProfile) -> str:
    parts = []
    for axis_name, axis_profile in sorted(machine_profile.axes.items()):
        span = f"{axis_profile.min_mm:.2f}–{axis_profile.max_mm:.2f} mm"
        calibration = (
            f"{axis_profile.steps_per_mm:g} steps/mm @ "
            f"{axis_profile.microstepping}x"
        )
        parts.append(f"{axis_name.upper()}: {span}, {calibration}")
    return "; machine profile: " + "; ".join(parts)


class PatternTranslator:
    """Translate pattern lines into a list of :class:`GCodeLine` objects."""

    def __init__(self, machine_profile: MachineProfile | None = None) -> None:
        self._lines: List[GCodeLine] = []
        self._x_mm = 0.0
        self._y_mm = 0.0
        self._z_mm = SAFE_Z_MM
        self._extrusion_mm = 0.0
        self._machine_profile = machine_profile

    def translate(self, source: str) -> List[GCodeLine]:
        """Translate a stitch description into motion commands."""

        self._reset_state()
        for line_number, raw_line in enumerate(source.splitlines(), start=1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            tokens = stripped.split()
            command = tokens[0].upper()
            arguments = tokens[1:]
            if command in STITCH_PROFILES:
                count = self._parse_positive_int(
                    arguments,
                    line_number,
                    command,
                )
                profile = STITCH_PROFILES[command]
                self._emit_stitches(profile, count)
            elif command == "MOVE":
                self._handle_move(arguments, line_number)
            elif command == "PAUSE":
                self._handle_pause(arguments, line_number)
            elif command == "TURN":
                self._handle_turn(arguments, line_number)
            else:
                message = f"Unknown command '{command}' on line {line_number}"
                raise ValueError(message)
        return list(self._lines)

    # Internal helpers -------------------------------------------------

    def _reset_state(self) -> None:
        self._x_mm = 0.0
        self._y_mm = 0.0
        self._z_mm = SAFE_Z_MM
        self._extrusion_mm = 0.0
        self._validate_position()
        self._lines = [
            GCodeLine("G21", "use millimeters"),
            GCodeLine("G90", "absolute positioning"),
            GCodeLine(
                f"G92 X{self._x_mm:.2f} Y{self._y_mm:.2f} Z{SAFE_Z_MM:.2f} E0",
                "zero axes",
            ),
        ]

    def _emit(self, command: str, comment: str | None = None) -> None:
        self._lines.append(GCodeLine(command, comment))

    def _parse_positive_int(
        self, arguments: Sequence[str], line_number: int, command: str
    ) -> int:
        if not arguments:
            message = f"{command} on line {line_number} requires a count"
            raise ValueError(message)
        try:
            count = int(arguments[0])
        except ValueError as error:
            message = "{} on line {} requires an integer count".format(
                command,
                line_number,
            )
            raise ValueError(message) from error
        if count <= 0:
            message = "{} on line {} requires a positive count".format(
                command,
                line_number,
            )
            raise ValueError(message)
        return count

    def _parse_float(
        self,
        value: str,
        line_number: int,
        command: str,
    ) -> float:
        try:
            return float(value)
        except ValueError as error:
            message = "{} on line {} expects numeric values".format(
                command,
                line_number,
            )
            raise ValueError(message) from error

    def _ensure_safe_height(self) -> None:
        self._check_axis("z", SAFE_Z_MM)
        if self._z_mm != SAFE_Z_MM:
            command = f"G1 Z{SAFE_Z_MM:.2f} F{PLUNGE_FEED_RATE}"
            self._emit(command, "raise to safe height")
            self._z_mm = SAFE_Z_MM

    def _emit_stitches(self, profile: StitchProfile, count: int) -> None:
        for index in range(1, count + 1):
            stitch_label = f"{profile.name.lower()} stitch {index} of {count}"
            plunge_z = FABRIC_PLANE_Z_MM - profile.plunge_depth_mm
            self._check_axis("z", plunge_z)
            self._emit(
                f"G1 Z{plunge_z:.2f} F{PLUNGE_FEED_RATE}",
                f"{stitch_label}: plunge",
            )
            self._z_mm = plunge_z
            self._extrusion_mm += profile.yarn_feed_mm
            self._emit(
                f"G1 E{self._extrusion_mm:.2f} F{YARN_FEED_RATE}",
                f"{stitch_label}: feed yarn",
            )
            self._emit(
                f"G1 Z{SAFE_Z_MM:.2f} F{PLUNGE_FEED_RATE}",
                f"{stitch_label}: raise",
            )
            self._z_mm = SAFE_Z_MM
            self._x_mm += profile.spacing_mm
            self._check_axis("x", self._x_mm)
            self._emit(
                f"G0 X{self._x_mm:.2f} Y{self._y_mm:.2f} F{TRAVEL_FEED_RATE}",
                f"{stitch_label}: advance",
            )

    def _handle_move(self, arguments: Sequence[str], line_number: int) -> None:
        if len(arguments) < 2:
            message = f"MOVE on line {line_number} requires X and Y values"
            raise ValueError(message)
        self._ensure_safe_height()
        x_value = self._parse_float(arguments[0], line_number, "MOVE")
        y_value = self._parse_float(arguments[1], line_number, "MOVE")
        self._check_axis("x", x_value)
        self._check_axis("y", y_value)
        self._x_mm = x_value
        self._y_mm = y_value
        self._emit(
            f"G0 X{self._x_mm:.2f} Y{self._y_mm:.2f} F{TRAVEL_FEED_RATE}",
            "reposition",
        )

    def _handle_pause(
        self,
        arguments: Sequence[str],
        line_number: int,
    ) -> None:
        if len(arguments) != 1:
            message = "PAUSE on line {} requires exactly one value".format(
                line_number,
            )
            raise ValueError(message)
        seconds = self._parse_float(arguments[0], line_number, "PAUSE")
        if seconds <= 0:
            message = "PAUSE on line {} requires a positive duration".format(
                line_number
            )
            raise ValueError(message)
        milliseconds = int(round(seconds * 1000))
        comment = f"pause for {seconds:.3f} s"
        self._emit(f"G4 P{milliseconds}", comment)

    def _handle_turn(self, arguments: Sequence[str], line_number: int) -> None:
        if len(arguments) > 1:
            message = "TURN on line {} accepts at most one value".format(
                line_number,
            )
            raise ValueError(message)
        self._ensure_safe_height()
        if arguments:
            step = self._parse_float(arguments[0], line_number, "TURN")
        else:
            step = DEFAULT_ROW_HEIGHT
        if step <= 0:
            message = "TURN on line {} requires a positive row height".format(
                line_number
            )
            raise ValueError(message)
        new_y = self._y_mm + step
        self._check_axis("x", 0.0)
        self._check_axis("y", new_y)
        self._x_mm = 0.0
        self._y_mm = new_y
        self._emit(
            f"G0 X{self._x_mm:.2f} Y{self._y_mm:.2f} F{TRAVEL_FEED_RATE}",
            "turn to next row",
        )

    def _check_axis(self, axis: str, value: float) -> None:
        if self._machine_profile is None:
            return
        axis_profile = self._machine_profile.axis(axis)
        if axis_profile is None:
            return
        axis_profile.ensure_within(axis.upper(), value)

    def _validate_position(self) -> None:
        self._check_axis("x", self._x_mm)
        self._check_axis("y", self._y_mm)
        self._check_axis("z", self._z_mm)


def translate_pattern(
    source: str, machine_profile: MachineProfile | None = None
) -> List[GCodeLine]:
    """Convenience wrapper for :class:`PatternTranslator`."""

    translator = PatternTranslator(machine_profile=machine_profile)
    return translator.translate(source)


def _strip_namespace(tag: str) -> str:
    """Return the local element name without any XML namespace."""

    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _parse_points_attribute(raw: str) -> List[Tuple[float, float]]:
    """Parse an SVG ``points`` attribute into coordinate tuples."""

    tokens = raw.replace(",", " ").split()
    if len(tokens) % 2 != 0:
        message = "SVG points attribute must contain coordinate pairs"
        raise ValueError(message)
    points: List[Tuple[float, float]] = []
    for index in range(0, len(tokens), 2):
        try:
            x_value = float(tokens[index])
            y_value = float(tokens[index + 1])
        except ValueError as error:  # pragma: no cover - defensive
            message = "Invalid numeric value in SVG points attribute"
            raise ValueError(message) from error
        points.append((x_value, y_value))
    return points


def _points_from_svg(svg_path: Path) -> List[Tuple[float, float]]:
    """Extract polyline or polygon coordinates from an SVG file."""

    document = ET.parse(svg_path)
    root = document.getroot()
    for element in root.iter():
        if _strip_namespace(element.tag) not in {"polyline", "polygon"}:
            continue
        points_attr = element.get("points")
        if not points_attr:
            continue
        points = _parse_points_attribute(points_attr)
        if _strip_namespace(element.tag) == "polygon" and len(points) > 1:
            first_point = points[0]
            last_point = points[-1]
            if first_point == last_point:
                points = points[:-1]
        if points:
            return points
    message = "SVG file does not contain a polyline or polygon with points"
    raise ValueError(message)


def _pattern_from_svg(
    svg_path: Path,
    scale: float,
    offset_x: float,
    offset_y: float,
) -> str:
    """Convert SVG polyline coordinates into MOVE commands."""

    points = _points_from_svg(svg_path)
    if not points:
        raise ValueError("SVG source did not provide any coordinates")
    commands = []
    for x_value, y_value in points:
        x_mm = x_value * scale + offset_x
        y_mm = y_value * scale + offset_y
        commands.append(f"MOVE {x_mm:.3f} {y_mm:.3f}")
    return "\n".join(commands)


def _load_pattern(
    path: Path | None,
    pattern: str | None,
    svg: Path | None = None,
    svg_scale: float = 1.0,
    svg_offset_x: float = 0.0,
    svg_offset_y: float = 0.0,
) -> str:
    if svg is not None and (pattern is not None or path is not None):
        message = "Provide SVG input without additional pattern text or files"
        raise ValueError(message)
    if pattern is not None:
        return pattern
    if svg is not None:
        return _pattern_from_svg(svg, svg_scale, svg_offset_x, svg_offset_y)
    if path is not None:
        return path.read_text(encoding="utf-8")
    return sys.stdin.read()


def _write_output(
    lines: Iterable[GCodeLine],
    output_path: Path | None,
    fmt: str,
    machine_profile: MachineProfile | None = None,
) -> None:
    materialized = list(lines)
    if fmt == "gcode":
        output_lines = [line.as_text() for line in materialized]
        if machine_profile is not None:
            output_lines.insert(
                0,
                _format_machine_profile_comment(machine_profile),
            )
        text = "\n".join(output_lines) + "\n"
    else:
        commands = [line.as_dict() for line in materialized]
        payload: Dict[str, Any] = {"commands": commands}
        if machine_profile is not None:
            payload["machine_profile"] = machine_profile.as_dict()
        text = json.dumps(payload, indent=2)
    if output_path is None:
        sys.stdout.write(text)
    else:
        output_path.write_text(text, encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    description = "Translate a crochet pattern into G-code-like instructions."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "pattern",
        nargs="?",
        help="Path to a pattern file (defaults to stdin).",
    )
    parser.add_argument(
        "--text",
        help="Inline pattern text. Overrides the positional file if provided.",
    )
    parser.add_argument(
        "--svg",
        type=Path,
        help=" ".join(
            [
                "Path to an SVG polyline or polygon to convert into MOVE",
                "commands.",
            ]
        ),
    )
    parser.add_argument(
        "--svg-scale",
        type=float,
        default=1.0,
        help="Scale factor applied to SVG coordinates before conversion.",
    )
    parser.add_argument(
        "--svg-offset-x",
        type=float,
        default=0.0,
        help="X offset (mm) applied after scaling SVG coordinates.",
    )
    parser.add_argument(
        "--svg-offset-y",
        type=float,
        default=0.0,
        help="Y offset (mm) applied after scaling SVG coordinates.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Optional file to write output. Defaults to stdout.",
    )
    parser.add_argument(
        "--format",
        choices=("gcode", "json"),
        default="gcode",
        help="Output format (default: gcode).",
    )
    parser.add_argument(
        "--machine-profile",
        type=Path,
        help=(
            "Path to a JSON or YAML machine profile describing axis travel "
            "limits, microstepping, and steps-per-mm."
        ),
    )
    parser.add_argument(
        "--home-state",
        choices=("unknown", "homed"),
        default="unknown",
        help=(
            "Reported homing state of the motion system (default: unknown). "
            "Set to 'homed' after completing a homing cycle."
        ),
    )
    parser.add_argument(
        "--require-home",
        action="store_true",
        help=(
            "Abort translation if the reported homing state is not 'homed'. "
            "Enforces the home-before-run guard from the design docs."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    pattern_path = Path(args.pattern) if args.pattern else None
    pattern_text = _load_pattern(
        pattern_path,
        args.text,
        args.svg,
        args.svg_scale,
        args.svg_offset_x,
        args.svg_offset_y,
    )
    if args.require_home and args.home_state != "homed":
        message = (
            "Refusing to generate motion: home state is "
            f"'{args.home_state}' (expected 'homed').\n"
        )
        sys.stderr.write(message)
        guidance = "Run the machine homing sequence or omit --require-home.\n"
        sys.stderr.write(guidance)
        return 1
    machine_profile = None
    if args.machine_profile is not None:
        machine_profile = load_machine_profile(args.machine_profile)
    lines = translate_pattern(pattern_text, machine_profile=machine_profile)
    _write_output(
        lines,
        args.output,
        args.format,
        machine_profile=machine_profile,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised via CLI tests
    raise SystemExit(main())
