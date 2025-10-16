"""Tests for the pattern visualization harness."""

from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "pattern_visualize.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("pattern_visualize", MODULE_PATH)
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
