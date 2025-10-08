from __future__ import annotations

import json
import subprocess
import sys

import pytest

from wove.pattern_cli import PatternTranslator, translate_pattern


def _as_text(lines):
    return [line.as_text() for line in lines]


def test_translate_pattern_basic():
    pattern = "\n".join(
        [
            "CHAIN 2",
            "PAUSE 0.5",
            "MOVE 10 5",
            "TURN 6",
            "SINGLE 1",
        ]
    )
    lines = translate_pattern(pattern)
    text = _as_text(lines)
    assert text[:3] == [
        "G21 ; use millimeters",
        "G90 ; absolute positioning",
        "G92 X0.00 Y0.00 Z4.00 E0 ; zero axes",
    ]
    assert text[3] == "G1 Z-1.50 F600 ; chain stitch 1 of 2: plunge"
    assert text[4] == "G1 E0.50 F300 ; chain stitch 1 of 2: feed yarn"
    assert text[5] == "G1 Z4.00 F600 ; chain stitch 1 of 2: raise"
    assert text[6] == "G0 X5.00 Y0.00 F1200 ; chain stitch 1 of 2: advance"
    assert text[7] == "G1 Z-1.50 F600 ; chain stitch 2 of 2: plunge"
    assert text[10] == "G0 X10.00 Y0.00 F1200 ; chain stitch 2 of 2: advance"
    assert "G4 P500 ; pause for 0.500 s" in text
    assert "G0 X10.00 Y5.00 F1200 ; reposition" in text
    turn_index = text.index("G0 X0.00 Y11.00 F1200 ; turn to next row")
    expected_plunge = "G1 Z-2.00 F600 ; single stitch 1 of 1: plunge"
    assert text[turn_index + 1] == expected_plunge
    assert text[-1] == "G0 X4.50 Y11.00 F1200 ; single stitch 1 of 1: advance"


@pytest.mark.parametrize(
    "pattern",
    [
        "UNKNOWN 3",
        "CHAIN 0",
        "PAUSE 0",
        "MOVE 3",
        "TURN -1",
    ],
)
def test_translate_pattern_errors(pattern):
    translator = PatternTranslator()
    with pytest.raises(ValueError):
        translator.translate(pattern)


@pytest.mark.parametrize("fmt", ["json", "gcode"])
def test_pattern_cli_formats(tmp_path, fmt):
    pattern_path = tmp_path / "pattern.txt"
    pattern_path.write_text("CHAIN 1\n", encoding="utf-8")
    command = [
        sys.executable,
        "-m",
        "wove.pattern_cli",
        str(pattern_path),
        "--format",
        fmt,
    ]
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    if fmt == "json":
        payload = json.loads(completed.stdout)
        assert payload[0]["command"] == "G21"
        assert payload[-1]["comment"].startswith("chain")
    else:
        output_lines = completed.stdout.strip().splitlines()
        assert output_lines[0] == "G21 ; use millimeters"
        assert output_lines[-1].startswith("G0 X5.00 Y0.00 F1200")


def test_pattern_cli_text_input():
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "wove.pattern_cli",
            "--text",
            "CHAIN 1\nPAUSE 0.25",
            "--format",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    pause = next(line for line in payload if line["command"].startswith("G4"))
    assert pause["comment"] == "pause for 0.250 s"
