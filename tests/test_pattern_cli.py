# isort: skip_file

from __future__ import annotations

import io
import json
import subprocess
import sys

import pytest

from wove.machine_profile import AxisProfile, MachineProfile
from wove.pattern_cli import (
    DEFAULT_ROW_HEIGHT,
    SAFE_Z_MM,
    YARN_FEED_RATE,
    GCodeLine,
    PatternTranslator,
    _load_pattern,
    _parse_points_attribute,
    _pattern_from_svg,
    _planner_payload,
    _points_from_svg,
    _strip_namespace,
    _write_output,
    main,
    parse_args,
    translate_pattern,
)


def _as_text(lines):
    return [line.as_text() for line in lines]


def _sample_machine_profile(
    *,
    x_max: float = 120.0,
    y_max: float = 120.0,
    z_min: float = -10.0,
    z_max: float = 15.0,
) -> MachineProfile:
    return MachineProfile(
        axes={
            "X": AxisProfile("X", 16, 80.0, 0.0, x_max),
            "Y": AxisProfile("Y", 16, 80.0, 0.0, y_max),
            "Z": AxisProfile("Z", 16, 400.0, z_min, z_max),
        }
    )


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


def test_pattern_translator_records_planner_events():
    translator = PatternTranslator()
    lines = translator.translate("CHAIN 1")

    events = translator.planner_events

    assert len(events) == len(lines)
    assert events[0].command == "G21"
    last_event = events[-1]
    assert last_event.command.startswith("G0 X5.00")
    assert last_event.x_mm == pytest.approx(5.0)
    assert last_event.y_mm == pytest.approx(0.0)
    assert last_event.z_mm == pytest.approx(SAFE_Z_MM)
    assert last_event.extrusion_mm == pytest.approx(0.5)


def test_planner_payload_includes_metadata():
    translator = PatternTranslator()
    translator.translate("CHAIN 1")

    payload = _planner_payload(translator.planner_events)

    assert payload["version"] == 1
    assert payload["defaults"]["safe_z_mm"] == pytest.approx(SAFE_Z_MM)
    assert payload["defaults"]["yarn_feed_rate_mm_min"] == YARN_FEED_RATE
    bounds = payload["bounds"]
    assert bounds["x_mm"]["max"] == pytest.approx(5.0)
    assert payload["commands"][0]["command"] == "G21"
    last_entry = payload["commands"][-1]
    assert last_entry["state"]["extrusion_mm"] == pytest.approx(0.5)


def test_translate_pattern_slip_stitches():
    lines = translate_pattern("SLIP 2")
    text = _as_text(lines)
    assert "G1 Z-1.00 F600 ; slip stitch 1 of 2: plunge" in text
    assert "G1 E0.30 F300 ; slip stitch 1 of 2: feed yarn" in text
    assert "G0 X3.50 Y0.00 F1200 ; slip stitch 1 of 2: advance" in text
    assert text[-1] == "G0 X7.00 Y0.00 F1200 ; slip stitch 2 of 2: advance"


def test_translate_pattern_ignores_comments_and_blank_lines():
    pattern = "\n".join(["", "# comment", "CHAIN 1"])
    translator = PatternTranslator()
    lines = translator.translate(pattern)
    target_comment = "chain stitch 1 of 1: advance"
    assert any(target_comment in line.as_text() for line in lines)


def test_translate_pattern_respects_axis_limits():
    profile = _sample_machine_profile(x_max=9.0)
    translator = PatternTranslator(machine_profile=profile)
    with pytest.raises(ValueError) as excinfo:
        translator.translate("CHAIN 2")
    assert "Axis X position" in str(excinfo.value)


def test_translate_pattern_respects_z_limits():
    profile = _sample_machine_profile(z_min=-1.0)
    translator = PatternTranslator(machine_profile=profile)
    with pytest.raises(ValueError) as excinfo:
        translator.translate("DOUBLE 1")
    assert "Axis Z position" in str(excinfo.value)


def test_translate_pattern_with_profile_argument():
    profile = _sample_machine_profile()
    lines = translate_pattern("CHAIN 1", machine_profile=profile)
    found = False
    for comment in (line.comment for line in lines):
        if comment and "chain stitch" in comment:
            found = True
            break
    assert found


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


def test_translate_pattern_rejects_non_finite_values():
    translator = PatternTranslator()
    for command in (
        "MOVE nan 5",
        "MOVE 5 nan",
        "MOVE inf 5",
        "PAUSE nan",
        "PAUSE inf",
        "TURN nan",
        "TURN inf",
    ):
        with pytest.raises(ValueError):
            translator.translate(command)


def test_move_requires_positive_coordinates():
    translator = PatternTranslator()
    with pytest.raises(ValueError):
        translator.translate("MOVE -1 5")
    with pytest.raises(ValueError):
        translator.translate("MOVE 5 0")


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


def test_write_output_planner(tmp_path):
    translator = PatternTranslator()
    lines = translator.translate("CHAIN 1")
    planner_path = tmp_path / "pattern.planner.json"

    _write_output(
        lines,
        planner_path,
        "planner",
        planner_events=translator.planner_events,
    )

    payload = json.loads(planner_path.read_text(encoding="utf-8"))
    assert payload["commands"][0]["command"] == "G21"
    assert payload["bounds"]["x_mm"]["max"] == pytest.approx(5.0)


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


def test_load_pattern_rejects_multiple_sources(tmp_path):
    svg_path = tmp_path / "shape.svg"
    svg_path.write_text("<svg></svg>", encoding="utf-8")
    with pytest.raises(ValueError):
        _load_pattern(tmp_path / "pattern.txt", "CHAIN 1", svg=svg_path)


def test_load_pattern_uses_svg_source(monkeypatch, tmp_path):
    svg_path = tmp_path / "shape.svg"
    svg_path.write_text("<svg></svg>", encoding="utf-8")
    recorded_args: list[tuple] = []

    def fake_pattern_from_svg(path, scale, offset_x, offset_y):
        recorded_args.append((path, scale, offset_x, offset_y))
        return "MOVE 0.000 0.000"

    monkeypatch.setattr(
        "wove.pattern_cli._pattern_from_svg",
        fake_pattern_from_svg,
    )
    result = _load_pattern(
        path=None,
        pattern=None,
        svg=svg_path,
        svg_scale=2.0,
        svg_offset_x=1.5,
        svg_offset_y=-3.0,
    )
    assert result == "MOVE 0.000 0.000"
    assert recorded_args == [(svg_path, 2.0, 1.5, -3.0)]


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
            "--machine-profile",
            "profile.yaml",
            "--home-state",
            "homed",
            "--require-home",
        ]
    )
    assert str(args.pattern) == "pattern.txt"
    assert args.format == "json"
    assert str(args.output).endswith("out.gcode")
    assert str(args.machine_profile).endswith("profile.yaml")
    assert args.home_state == "homed"
    assert args.require_home is True
    planner_args = parse_args(["--format", "planner"])
    assert planner_args.format == "planner"


def test_main_stdout_json(capsys):
    exit_code = main(["--text", "CHAIN 1", "--format", "json"])
    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["command"] == "G21"


def test_main_stdout_planner(capsys):
    exit_code = main(["--text", "CHAIN 1", "--format", "planner"])
    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["commands"][0]["command"] == "G21"
    assert payload["defaults"]["safe_z_mm"] == pytest.approx(SAFE_Z_MM)


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


def test_main_accepts_machine_profile(tmp_path):
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(
        json.dumps(
            {
                "axes": {
                    "X": {
                        "microstepping": 16,
                        "steps_per_mm": 80,
                        "travel_min_mm": 0,
                        "travel_max_mm": 200,
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
        ),
        encoding="utf-8",
    )
    exit_code = main(
        [
            "--text",
            "CHAIN 1",
            "--machine-profile",
            str(profile_path),
        ]
    )
    assert exit_code == 0


def test_main_reports_machine_profile_limit_errors(tmp_path, capsys):
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(
        json.dumps(
            {
                "axes": {
                    "X": {
                        "microstepping": 16,
                        "steps_per_mm": 80,
                        "travel_min_mm": 0,
                        "travel_max_mm": 5,
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
        ),
        encoding="utf-8",
    )
    exit_code = main(
        [
            "--text",
            "CHAIN 2",
            "--machine-profile",
            str(profile_path),
        ]
    )
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Axis X position" in captured.err


def test_main_reports_machine_profile_load_errors(tmp_path, capsys):
    profile_path = tmp_path / "profile.json"
    profile_path.write_text("[]", encoding="utf-8")
    exit_code = main(
        [
            "--text",
            "CHAIN 1",
            "--machine-profile",
            str(profile_path),
        ]
    )
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Machine profile file must contain an object" in captured.err


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


def test_pattern_cli_svg_polyline(tmp_path):
    svg_path = tmp_path / "shape.svg"
    svg_path.write_text(
        (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<polyline points="0,0 5,0 5,5"/>'
            "</svg>"
        ),
        encoding="utf-8",
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "wove.pattern_cli",
            "--svg",
            str(svg_path),
            "--svg-scale",
            "2",
            "--svg-offset-x",
            "1",
            "--svg-offset-y",
            "0.5",
            "--format",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    repositions: list[str] = []
    for entry in payload:
        command = entry["command"]
        if command.startswith("G0 X"):
            repositions.append(command)
    assert repositions == [
        "G0 X1.00 Y0.50 F1200",
        "G0 X11.00 Y0.50 F1200",
        "G0 X11.00 Y10.50 F1200",
    ]


def test_parse_points_attribute_parses_pairs():
    points = _parse_points_attribute("0,0  5,0 5,5")
    assert points == [(0.0, 0.0), (5.0, 0.0), (5.0, 5.0)]


def test_parse_points_attribute_requires_even_values():
    with pytest.raises(ValueError):
        _parse_points_attribute("0,0 5")


def test_strip_namespace_returns_tag_when_missing_braces():
    assert _strip_namespace("polyline") == "polyline"


def test_points_from_svg_reads_polyline(tmp_path):
    svg_path = tmp_path / "shape.svg"
    svg_path.write_text(
        (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            "<g>"
            "<polygon/>"
            '<polyline points="2,2 3,2 3,3"/>'
            "</g>"
            "</svg>"
        ),
        encoding="utf-8",
    )
    assert _points_from_svg(svg_path) == [(2.0, 2.0), (3.0, 2.0), (3.0, 3.0)]


def test_points_from_svg_polygon_drops_duplicate_endpoint(tmp_path):
    svg_path = tmp_path / "shape.svg"
    svg_path.write_text(
        (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<polygon points="0,0 1,0 1,1 0,0"/>'
            "</svg>"
        ),
        encoding="utf-8",
    )
    assert _points_from_svg(svg_path) == [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]


def test_points_from_svg_requires_polyline_or_polygon(tmp_path):
    svg_path = tmp_path / "shape.svg"
    svg_path.write_text(
        (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="1" height="1"/>'
            "</svg>"
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        _points_from_svg(svg_path)


def test_pattern_from_svg_scales_and_offsets(tmp_path):
    svg_path = tmp_path / "shape.svg"
    svg_path.write_text(
        (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<polyline points="0,0 1,1"/>'
            "</svg>"
        ),
        encoding="utf-8",
    )
    result = _pattern_from_svg(
        svg_path,
        scale=2.0,
        offset_x=1.0,
        offset_y=0.5,
    )
    assert result.splitlines() == [
        "MOVE 1.000 0.500",
        "MOVE 3.000 2.500",
    ]


def test_pattern_from_svg_shifts_coordinates_to_positive_origin(tmp_path):
    svg_path = tmp_path / "shape.svg"
    svg_path.write_text(
        (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<polyline points="0,0 1,0"/>'
            "</svg>"
        ),
        encoding="utf-8",
    )
    result = _pattern_from_svg(
        svg_path,
        scale=1.0,
        offset_x=0.0,
        offset_y=0.0,
    )
    assert result.splitlines() == [
        "MOVE 0.001 0.001",
        "MOVE 1.001 0.001",
    ]


def test_pattern_from_svg_requires_coordinates(monkeypatch, tmp_path):
    svg_path = tmp_path / "shape.svg"
    svg_path.write_text("<svg></svg>", encoding="utf-8")

    def fake_points_from_svg(path):
        assert path == svg_path
        return []

    monkeypatch.setattr(
        "wove.pattern_cli._points_from_svg",
        fake_points_from_svg,
    )
    with pytest.raises(ValueError):
        _pattern_from_svg(svg_path, scale=1.0, offset_x=0.0, offset_y=0.0)
