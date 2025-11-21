"""Translate simple crochet stitch descriptions into G-code-like motion."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple
from xml.etree import ElementTree as ET

from ..machine_profile import MachineProfile, load_machine_profile
from .options import build_parser, parse_args

SAFE_Z_MM = 4.0
FABRIC_PLANE_Z_MM = 0.0
TRAVEL_FEED_RATE = 1200
PLUNGE_FEED_RATE = 600
YARN_FEED_RATE = 300
DEFAULT_ROW_HEIGHT = 6.0
MIN_MOVE_COORD_MM = 1e-3
PLANNER_LOOP_SECONDS = 14.0
PLANNER_METADATA_SOURCE = "pattern_cli preview"


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
class PlannerEvent:
    """State snapshot for planner integrations after emitting a command."""

    command: str
    comment: str | None
    x_mm: float
    y_mm: float
    z_mm: float
    extrusion_mm: float


@dataclass(frozen=True)
class StitchProfile:
    """Describe how to render a stitch in the generated motion sequence."""

    name: str
    spacing_mm: float
    plunge_depth_mm: float
    yarn_feed_mm: float


STITCH_PROFILES = {
    "SLIP": StitchProfile(
        "SLIP",
        spacing_mm=3.5,
        plunge_depth_mm=1.0,
        yarn_feed_mm=0.3,
    ),
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


class PatternTranslator:
    """Translate pattern lines into a list of :class:`GCodeLine` objects."""

    def __init__(self, machine_profile: MachineProfile | None = None) -> None:
        self._lines: List[GCodeLine] = []
        self._x_mm = 0.0
        self._y_mm = 0.0
        self._z_mm = SAFE_Z_MM
        self._extrusion_mm = 0.0
        self._machine_profile = machine_profile
        self._planner_events: List[PlannerEvent] = []

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
                self._emit_stitches(profile, count, line_number)
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

    @property
    def planner_events(self) -> List[PlannerEvent]:
        """Return planner-oriented command snapshots for the translation."""

        return list(self._planner_events)

    # Internal helpers -------------------------------------------------

    def _reset_state(self) -> None:
        self._lines = []
        self._planner_events = []
        self._x_mm = 0.0
        self._y_mm = 0.0
        self._z_mm = SAFE_Z_MM
        self._extrusion_mm = 0.0
        self._emit("G21", "use millimeters")
        self._emit("G90", "absolute positioning")
        self._emit(
            f"G92 X{self._x_mm:.2f} Y{self._y_mm:.2f} Z{SAFE_Z_MM:.2f} E0",
            "zero axes",
        )

    def _emit(self, command: str, comment: str | None = None) -> None:
        self._lines.append(GCodeLine(command, comment))
        self._planner_events.append(
            PlannerEvent(
                command=command,
                comment=comment,
                x_mm=self._x_mm,
                y_mm=self._y_mm,
                z_mm=self._z_mm,
                extrusion_mm=self._extrusion_mm,
            )
        )

    def _ensure_within_limits(
        self, axis: str, position: float, *, line_number: int | None = None
    ) -> None:
        if self._machine_profile is None:
            return
        self._machine_profile.ensure_within(
            axis,
            position,
            line_number=line_number,
        )

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
            number = float(value)
        except ValueError as error:
            message = "{} on line {} expects numeric values".format(
                command,
                line_number,
            )
            raise ValueError(message) from error
        if math.isnan(number) or math.isinf(number):
            message = "{} on line {} expects finite values".format(
                command,
                line_number,
            )
            raise ValueError(message)
        return number

    def _ensure_safe_height(self) -> None:
        if self._z_mm != SAFE_Z_MM:
            self._ensure_within_limits("Z", SAFE_Z_MM)
            self._z_mm = SAFE_Z_MM
            command = f"G1 Z{SAFE_Z_MM:.2f} F{PLUNGE_FEED_RATE}"
            self._emit(command, "raise to safe height")

    def _emit_stitches(
        self, profile: StitchProfile, count: int, line_number: int
    ) -> None:
        for index in range(1, count + 1):
            stitch_label = f"{profile.name.lower()} stitch {index} of {count}"
            plunge_z = FABRIC_PLANE_Z_MM - profile.plunge_depth_mm
            self._ensure_within_limits("Z", plunge_z, line_number=line_number)
            self._z_mm = plunge_z
            self._emit(
                f"G1 Z{plunge_z:.2f} F{PLUNGE_FEED_RATE}",
                f"{stitch_label}: plunge",
            )
            self._extrusion_mm += profile.yarn_feed_mm
            self._emit(
                f"G1 E{self._extrusion_mm:.2f} F{YARN_FEED_RATE}",
                f"{stitch_label}: feed yarn",
            )
            self._z_mm = SAFE_Z_MM
            self._emit(
                f"G1 Z{SAFE_Z_MM:.2f} F{PLUNGE_FEED_RATE}",
                f"{stitch_label}: raise",
            )
            self._ensure_within_limits("Z", SAFE_Z_MM, line_number=line_number)
            new_x = self._x_mm + profile.spacing_mm
            self._ensure_within_limits("X", new_x, line_number=line_number)
            self._x_mm = new_x
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
        if x_value <= 0 or y_value <= 0:
            message = "MOVE on line {} requires positive coordinates".format(
                line_number
            )
            raise ValueError(message)
        self._ensure_within_limits("X", x_value, line_number=line_number)
        self._ensure_within_limits("Y", y_value, line_number=line_number)
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
        self._ensure_within_limits("X", 0.0, line_number=line_number)
        self._x_mm = 0.0
        new_y = self._y_mm + step
        self._ensure_within_limits("Y", new_y, line_number=line_number)
        self._y_mm = new_y
        self._emit(
            f"G0 X{self._x_mm:.2f} Y{self._y_mm:.2f} F{TRAVEL_FEED_RATE}",
            "turn to next row",
        )


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
    scaled_points: List[Tuple[float, float]] = []
    for x_value, y_value in points:
        x_mm = x_value * scale + offset_x
        y_mm = y_value * scale + offset_y
        scaled_points.append((x_mm, y_mm))
    min_x = min(x for x, _ in scaled_points)
    min_y = min(y for _, y in scaled_points)
    shift_x = 0.0
    shift_y = 0.0
    if min_x <= 0:
        shift_x = MIN_MOVE_COORD_MM - min_x
    if min_y <= 0:
        shift_y = MIN_MOVE_COORD_MM - min_y
    commands = []
    for x_mm, y_mm in scaled_points:
        adjusted_x = x_mm + shift_x
        adjusted_y = y_mm + shift_y
        commands.append(f"MOVE {adjusted_x:.3f} {adjusted_y:.3f}")
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


def _planner_payload(
    events: Sequence[PlannerEvent],
    *,
    machine_profile: MachineProfile | None = None,
    require_home: bool = False,
    home_state: str = "unknown",
) -> dict[str, object]:
    """Return a planner-friendly payload summarizing motion commands."""

    def bounds(values: Iterable[float]) -> dict[str, float]:
        series = list(values)
        return {"min": min(series), "max": max(series)}

    commands = []
    for index, event in enumerate(events):
        entry: dict[str, object] = {
            "index": index,
            "command": event.command,
            "state": {
                "x_mm": event.x_mm,
                "y_mm": event.y_mm,
                "z_mm": event.z_mm,
                "extrusion_mm": event.extrusion_mm,
            },
        }
        if event.comment is not None:
            entry["comment"] = event.comment
        commands.append(entry)

    payload: dict[str, object] = {
        "version": 1,
        "units": "millimeters",
        "metadata": {
            "duration_seconds": PLANNER_LOOP_SECONDS,
            "source": PLANNER_METADATA_SOURCE,
        },
        "defaults": {
            "safe_z_mm": SAFE_Z_MM,
            "fabric_plane_z_mm": FABRIC_PLANE_Z_MM,
            "travel_feed_rate_mm_min": TRAVEL_FEED_RATE,
            "plunge_feed_rate_mm_min": PLUNGE_FEED_RATE,
            "yarn_feed_rate_mm_min": YARN_FEED_RATE,
            "default_row_height_mm": DEFAULT_ROW_HEIGHT,
            "require_home": bool(require_home),
            "home_state": home_state,
        },
        "bounds": {
            "x_mm": bounds(event.x_mm for event in events),
            "y_mm": bounds(event.y_mm for event in events),
            "z_mm": bounds(event.z_mm for event in events),
            "extrusion_mm": bounds(event.extrusion_mm for event in events),
        },
        "commands": commands,
    }

    if machine_profile is not None:
        axes_payload: dict[str, dict[str, float]] = {}
        for name in sorted(machine_profile.axes):
            axis = machine_profile.axes[name]
            axes_payload[name] = {
                "microstepping": axis.microstepping,
                "steps_per_mm": axis.steps_per_mm,
                "travel_min_mm": axis.travel_min_mm,
                "travel_max_mm": axis.travel_max_mm,
            }
        payload["machine_profile"] = {"axes": axes_payload}

    return payload


def _write_output(
    lines: Iterable[GCodeLine],
    output_path: Path | None,
    fmt: str,
    *,
    planner_events: Sequence[PlannerEvent] | None = None,
    machine_profile: MachineProfile | None = None,
    require_home: bool = False,
    home_state: str = "unknown",
) -> None:
    if fmt == "gcode":
        text = "\n".join(line.as_text() for line in lines) + "\n"
    elif fmt == "json":
        payload = [line.as_dict() for line in lines]
        text = json.dumps(payload, indent=2)
    else:
        if planner_events is None:
            raise ValueError("Planner format requires planner events")
        payload = _planner_payload(
            planner_events,
            machine_profile=machine_profile,
            require_home=require_home,
            home_state=home_state,
        )
        text = json.dumps(payload, indent=2)
    if output_path is None:
        sys.stdout.write(text)
    else:
        output_path.write_text(text, encoding="utf-8")


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
    machine_profile: MachineProfile | None = None
    if args.machine_profile is not None:
        try:
            machine_profile = load_machine_profile(args.machine_profile)
        except ValueError as error:
            sys.stderr.write(f"{error}\n")
            return 1
    if args.require_home and args.home_state != "homed":
        message = (
            "Refusing to generate motion: home state is "
            f"'{args.home_state}' (expected 'homed').\n"
        )
        sys.stderr.write(message)
        guidance = "Run the machine homing sequence or omit --require-home.\n"
        sys.stderr.write(guidance)
        return 1
    translator = PatternTranslator(machine_profile=machine_profile)
    try:
        lines = translator.translate(pattern_text)
    except ValueError as error:
        sys.stderr.write(f"{error}\n")
        return 1
    _write_output(
        lines,
        args.output,
        args.format,
        planner_events=translator.planner_events,
        machine_profile=machine_profile,
        require_home=args.require_home,
        home_state=args.home_state,
    )
    return 0


__all__ = [
    "SAFE_Z_MM",
    "FABRIC_PLANE_Z_MM",
    "TRAVEL_FEED_RATE",
    "PLUNGE_FEED_RATE",
    "YARN_FEED_RATE",
    "DEFAULT_ROW_HEIGHT",
    "MIN_MOVE_COORD_MM",
    "GCodeLine",
    "PlannerEvent",
    "StitchProfile",
    "STITCH_PROFILES",
    "PatternTranslator",
    "translate_pattern",
    "_strip_namespace",
    "_parse_points_attribute",
    "_points_from_svg",
    "_pattern_from_svg",
    "_planner_payload",
    "_write_output",
    "_load_pattern",
    "build_parser",
    "parse_args",
    "main",
]


if __name__ == "__main__":  # pragma: no cover - exercised via CLI tests
    raise SystemExit(main())
