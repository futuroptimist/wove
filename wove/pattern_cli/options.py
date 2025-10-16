"""Argument parsing helpers for :mod:`wove.pattern_cli`."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

_DESCRIPTION = "Translate a crochet pattern into G-code-like instructions."


def build_parser() -> argparse.ArgumentParser:
    """Return an argument parser for the pattern CLI."""

    parser = argparse.ArgumentParser(description=_DESCRIPTION)
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
        choices=("gcode", "json", "planner"),
        default="gcode",
        help="Output format (default: gcode).",
    )
    parser.add_argument(
        "--machine-profile",
        type=Path,
        help=(
            "Path to a JSON or YAML machine profile containing axis limits. "
            "Generated moves are checked against those limits."
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
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse ``argv`` using the pattern CLI argument definitions."""

    parser = build_parser()
    return parser.parse_args(argv)


__all__ = ["build_parser", "parse_args"]
