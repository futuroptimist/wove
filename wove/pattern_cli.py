"""Translate simple crochet stitch descriptions into G-code-like motion."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

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


class PatternTranslator:
    """Translate pattern lines into a list of :class:`GCodeLine` objects."""

    def __init__(self) -> None:
        self._lines: List[GCodeLine] = []
        self._x_mm = 0.0
        self._y_mm = 0.0
        self._z_mm = SAFE_Z_MM
        self._extrusion_mm = 0.0

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
        self._lines = [
            GCodeLine("G21", "use millimeters"),
            GCodeLine("G90", "absolute positioning"),
            GCodeLine(
                f"G92 X{self._x_mm:.2f} Y{self._y_mm:.2f} Z{SAFE_Z_MM:.2f} E0",
                "zero axes",
            ),
        ]
        self._x_mm = 0.0
        self._y_mm = 0.0
        self._z_mm = SAFE_Z_MM
        self._extrusion_mm = 0.0

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
        if self._z_mm != SAFE_Z_MM:
            command = f"G1 Z{SAFE_Z_MM:.2f} F{PLUNGE_FEED_RATE}"
            self._emit(command, "raise to safe height")
            self._z_mm = SAFE_Z_MM

    def _emit_stitches(self, profile: StitchProfile, count: int) -> None:
        for index in range(1, count + 1):
            stitch_label = f"{profile.name.lower()} stitch {index} of {count}"
            plunge_z = FABRIC_PLANE_Z_MM - profile.plunge_depth_mm
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
        self._x_mm = 0.0
        self._y_mm += step
        self._emit(
            f"G0 X{self._x_mm:.2f} Y{self._y_mm:.2f} F{TRAVEL_FEED_RATE}",
            "turn to next row",
        )


def translate_pattern(source: str) -> List[GCodeLine]:
    """Convenience wrapper for :class:`PatternTranslator`."""

    translator = PatternTranslator()
    return translator.translate(source)


def _load_pattern(path: Path | None, pattern: str | None) -> str:
    if pattern is not None:
        return pattern
    if path is not None:
        return path.read_text(encoding="utf-8")
    return sys.stdin.read()


def _write_output(
    lines: Iterable[GCodeLine],
    output_path: Path | None,
    fmt: str,
) -> None:
    if fmt == "gcode":
        text = "\n".join(line.as_text() for line in lines) + "\n"
    else:
        payload = [line.as_dict() for line in lines]
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
    pattern_text = _load_pattern(pattern_path, args.text)
    if args.require_home and args.home_state != "homed":
        message = (
            "Refusing to generate motion: home state is "
            f"'{args.home_state}' (expected 'homed').\n"
        )
        sys.stderr.write(message)
        guidance = "Run the machine homing sequence or omit --require-home.\n"
        sys.stderr.write(guidance)
        return 1
    lines = translate_pattern(pattern_text)
    _write_output(lines, args.output, args.format)
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised via CLI tests
    raise SystemExit(main())
