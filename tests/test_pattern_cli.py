# isort: skip_file

from __future__ import annotations

import io
import json
import subprocess
import sys

import pytest

from wove.pattern_cli import (
    DEFAULT_ROW_HEIGHT,
    GCodeLine,
    PatternTranslator,
    _load_pattern,
    _write_output,
    main,
    parse_args,
    translate_pattern,
)


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
    final_step = "G0 X4.50 Y11.00 F1200 ; single stitch 1 of 1: advance"
    assert text[-1] == final_step


def test_translate_pattern_ignores_comments_and_blank_lines():
    pattern = "\n".join(["", "# comment", "CHAIN 1"])
    translator = PatternTranslator()
    lines = translator.translate(pattern)
    target_comment = "chain stitch 1 of 1: advance"
    assert any(target_comment in line.as_text() for line in lines)


@pytest.mark.parametrize(
    "pattern",
    [
        "UNKNOWN 3",
        "CHAIN 0",
        "CHAIN",
        "CHAIN two",
        "PAUSE 0",
        "PAUSE",
        "PAUSE 1 2",
        "MOVE 3",
        "MOVE nope 1",
        "TURN -1",
        "TURN 1 2",
    ],
)
def test_translate_pattern_errors(pattern):
    translator = PatternTranslator()
    with pytest.raises(ValueError):
        translator.translate(pattern)


def test_turn_without_argument_uses_default_height():
    pattern = "\n".join(["CHAIN 1", "TURN", "CHAIN 1"])
    lines = translate_pattern(pattern)
    text = _as_text(lines)
    default_turn = ("G0 X0.00 Y{height:.2f} F1200 ; turn to next row").format(
        height=DEFAULT_ROW_HEIGHT
    )
    assert default_turn in text
    assert text[-1].startswith("G0 X5.00 Y6.00 F1200")


def test_ensure_safe_height_emits_command():
    translator = PatternTranslator()
    translator._reset_state()
    translator._z_mm = -1.0
    translator._ensure_safe_height()
    assert translator._lines[-1].command.startswith("G1 Z4.00 F600")


def test_write_output_handles_files(tmp_path):
    gcode_lines = [GCodeLine("G21"), GCodeLine("G90", "absolute positioning")]
    gcode_path = tmp_path / "pattern.gcode"
    _write_output(gcode_lines, gcode_path, "gcode")
    expected = "G21\nG90 ; absolute positioning\n"
    assert gcode_path.read_text(encoding="utf-8") == expected

    json_path = tmp_path / "pattern.json"
    _write_output(gcode_lines, json_path, "json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload[0]["command"] == "G21"
    assert payload[1]["comment"] == "absolute positioning"


def test_load_pattern_prefers_inline(tmp_path):
    pattern_path = tmp_path / "pattern.txt"
    pattern_path.write_text("CHAIN 1", encoding="utf-8")
    inline = "CHAIN 2"
    result = _load_pattern(pattern_path, inline)
    assert result == inline


def test_load_pattern_reads_file(tmp_path):
    pattern_path = tmp_path / "pattern.txt"
    pattern_path.write_text("CHAIN 1", encoding="utf-8")
    result = _load_pattern(pattern_path, None)
    assert result == "CHAIN 1"


def test_load_pattern_reads_stdin(monkeypatch):
    fake_stdin = io.StringIO("CHAIN 1\n")
    monkeypatch.setattr(sys, "stdin", fake_stdin)
    assert _load_pattern(None, None) == "CHAIN 1\n"


def test_write_output_stdout_gcode(capsys):
    lines = [GCodeLine("G21")]
    _write_output(lines, None, "gcode")
    captured = capsys.readouterr()
    assert captured.out == "G21\n"


def test_parse_args_variants():
    defaults = parse_args([])
    assert defaults.format == "gcode"
    assert defaults.home_state == "unknown"
    assert defaults.require_home is False
    args = parse_args(
        [
            "pattern.txt",
            "--format",
            "json",
            "--output",
            "out.gcode",
            "--home-state",
            "homed",
        ]
    )
    assert str(args.pattern) == "pattern.txt"
    assert args.format == "json"
    assert str(args.output).endswith("out.gcode")
    assert args.home_state == "homed"


def test_main_stdout_json(capsys):
    exit_code = main(["--text", "CHAIN 1", "--format", "json"])
    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["command"] == "G21"


def test_main_writes_output_file(tmp_path):
    output_path = tmp_path / "pattern.gcode"
    exit_code = main(
        [
            "--text",
            "CHAIN 1",
            "--output",
            str(output_path),
        ]
    )
    assert exit_code == 0
    assert output_path.read_text(encoding="utf-8").startswith("G21")


def test_main_requires_homed_guard(capsys):
    exit_code = main(["--text", "CHAIN 1", "--require-home"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Refusing to generate motion" in captured.err


def test_main_allows_homed_guard_when_homed(capsys):
    exit_code = main(
        [
            "--text",
            "CHAIN 1",
            "--require-home",
            "--home-state",
            "homed",
        ]
    )
    assert exit_code == 0


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
