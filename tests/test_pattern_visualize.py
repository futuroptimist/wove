"""Tests for the pattern visualization harness."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


MODULE_PATH = (
    Path(__file__).resolve().parent.parent / "scripts" / "pattern_visualize.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "pattern_visualize",
        MODULE_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def test_generate_previews_creates_svgs(tmp_path):
    module = _load_module()
    pattern_dir = Path(__file__).resolve().parent / "fixtures" / "patterns"
    pattern_path = pattern_dir / "handwritten.txt"
    outputs = module.generate_previews([pattern_path], tmp_path, force=True)
    assert len(outputs) == 2
    chart, timeline = outputs
    assert chart.exists()
    assert timeline.exists()
    chart_text = chart.read_text(encoding="utf-8")
    timeline_text = timeline.read_text(encoding="utf-8")
    assert chart_text.startswith("<svg")
    assert "data-role=\"xy-path\"" in chart_text
    assert "handwritten" in chart_text
    assert timeline_text.startswith("<svg")
    assert "data-series=\"z_mm\"" in timeline_text
    assert "data-series=\"extrusion_mm\"" in timeline_text


def test_main_invocation_creates_files(tmp_path, capsys):
    module = _load_module()
    pattern_dir = Path(__file__).resolve().parent / "fixtures" / "patterns"
    args = [
        "--pattern-dir",
        str(pattern_dir),
        "--output-dir",
        str(tmp_path),
        "--pattern",
        "handwritten",
        "--force",
    ]
    exit_code = module.main(args)
    assert exit_code == 0
    chart_path = tmp_path / "handwritten-chart.svg"
    timeline_path = tmp_path / "handwritten-timeline.svg"
    assert chart_path.exists()
    assert timeline_path.exists()
    captured = capsys.readouterr()
    assert "handwritten-chart.svg" in captured.out
    assert "handwritten-timeline.svg" in captured.out


def test_helper_functions_cover_edge_cases(tmp_path):
    module = _load_module()

    # _ensure_range returns a default window when it receives no values.
    assert module._ensure_range([]) == (0.0, 1.0)

    # When the range collapses to a single value the helper expands it a bit.
    minimum, maximum = module._ensure_range([2.0, 2.0, 2.0])
    assert minimum < 2.0 < maximum

    # _scale_linear falls back to the midpoint when the source span is zero.
    midpoint = module._scale_linear(
        5.0,
        source=(1.0, 1.0),
        target=(0.0, 10.0),
    )
    assert midpoint == 5.0

    # _load_patterns raises when a requested pattern cannot be found.
    with pytest.raises(FileNotFoundError):
        module._load_patterns(tmp_path, ["does-not-exist"])


def test_module_inserts_repo_root_into_sys_path(monkeypatch):
    module = _load_module()
    repo_root = module.REPO_ROOT
    sanitized_path = [
        entry
        for entry in sys.path
        if Path(entry).resolve() != repo_root
    ]
    monkeypatch.setattr(sys, "path", sanitized_path, raising=False)

    module = _load_module()

    assert str(repo_root) in sys.path


def test_chart_helpers_cover_edge_branches():
    module = _load_module()

    empty_chart = module._xy_chart([], "empty")
    assert "data-role=\"xy-path\"" in empty_chart

    single_event = module.PlannerEvent(
        command="KNIT",
        comment=None,
        x_mm=1.0,
        y_mm=2.0,
        z_mm=3.0,
        extrusion_mm=0.0,
    )
    single_timeline = module._timeline_chart([single_event], "single")
    assert "data-series=\"z_mm\"" in single_timeline


def test_load_patterns_defaults_to_directory_listing(tmp_path):
    module = _load_module()
    (tmp_path / "first.txt").write_text("KNIT 0 0 0", encoding="utf-8")
    (tmp_path / "second.txt").write_text("KNIT 0 0 0", encoding="utf-8")

    loaded = module._load_patterns(tmp_path, None)

    assert [path.name for path in loaded] == ["first.txt", "second.txt"]


def test_main_reports_errors_and_empty_directories(tmp_path, capsys):
    module = _load_module()

    exit_code = module.main([
        "--pattern-dir",
        str(tmp_path),
        "--pattern",
        "missing",
    ])

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "does not exist" in captured.out

    exit_code = module.main([
        "--pattern-dir",
        str(tmp_path),
        "--output-dir",
        str(tmp_path / "out"),
    ])

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "nothing to render" in captured.out
