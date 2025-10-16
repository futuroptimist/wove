"""Generate SVG previews for pattern CLI fixtures."""

from __future__ import annotations

import argparse
import html
import math
import sys
from pathlib import Path
from typing import Iterable, List, Sequence


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from wove.pattern_cli import PatternTranslator, PlannerEvent
DEFAULT_PATTERN_DIR = REPO_ROOT / "tests" / "fixtures" / "patterns"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs" / "_static" / "pattern_previews"


def _ensure_range(values: Iterable[float]) -> tuple[float, float]:
    series = list(values)
    if not series:
        return 0.0, 1.0
    minimum = min(series)
    maximum = max(series)
    if math.isclose(minimum, maximum):
        padding = 1.0 if math.isclose(maximum, 0.0) else abs(maximum) * 0.05
        minimum -= padding
        maximum += padding
    return minimum, maximum


def _scale_linear(
    value: float, *, source: tuple[float, float], target: tuple[float, float]
) -> float:
    start, end = source
    target_start, target_end = target
    span = end - start
    if math.isclose(span, 0.0):
        return (target_start + target_end) / 2.0
    ratio = (value - start) / span
    return target_start + ratio * (target_end - target_start)


def _xy_chart(events: Sequence[PlannerEvent], name: str) -> str:
    width = 420
    height = 420
    margin = 32
    points = [(event.x_mm, event.y_mm) for event in events]
    if not points:
        points = [(0.0, 0.0)]
    min_x, max_x = _ensure_range(point[0] for point in points)
    min_y, max_y = _ensure_range(point[1] for point in points)
    scaled: list[tuple[float, float]] = []
    for x_mm, y_mm in points:
        x_px = _scale_linear(
            x_mm,
            source=(min_x, max_x),
            target=(margin, width - margin),
        )
        y_px = _scale_linear(
            y_mm,
            source=(min_y, max_y),
            target=(height - margin, margin),
        )
        scaled.append((x_px, y_px))
    path_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in scaled)
    start_x, start_y = scaled[0]
    end_x, end_y = scaled[-1]
    escaped_name = html.escape(name)
    return (
        "<svg xmlns=\"http://www.w3.org/2000/svg\" "
        f"width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">"
        f"<title>{escaped_name} XY path</title>"
        "<desc>Scaled XY motion path generated from planner events.</desc>"
        f"<rect x=\"{margin}\" y=\"{margin}\" width=\"{width - 2 * margin}\" "
        f"height=\"{height - 2 * margin}\" fill=\"#f6f8fb\" stroke=\"#cdd5e0\" "
        "stroke-width=\"1\"/>"
        f"<polyline data-role=\"xy-path\" fill=\"none\" stroke=\"#0069ff\" "
        f"stroke-width=\"2\" points=\"{path_points}\"/>"
        f"<circle cx=\"{start_x:.1f}\" cy=\"{start_y:.1f}\" r=\"5\" fill=\"#2a9d8f\"/>"
        f"<circle cx=\"{end_x:.1f}\" cy=\"{end_y:.1f}\" r=\"5\" fill=\"#e76f51\"/>"
        f"<text x=\"{margin}\" y=\"{margin - 10}\" "
        "font-family=\"sans-serif\" font-size=\"14\" fill=\"#1f2933\">"
        f"{escaped_name} XY motion</text>"
        "</svg>"
    )


def _timeline_chart(events: Sequence[PlannerEvent], name: str) -> str:
    width = 640
    height = 360
    margin_left = 56
    margin_right = 20
    margin_top = 36
    margin_bottom = 48
    indices = list(range(len(events))) or [0]
    z_series = [event.z_mm for event in events] or [0.0]
    extrusion_series = [event.extrusion_mm for event in events] or [0.0]
    z_min, z_max = _ensure_range(z_series)
    e_min, e_max = _ensure_range(extrusion_series)
    plot_width = width - margin_left - margin_right
    if len(indices) > 1:
        step = plot_width / (len(indices) - 1)
    else:
        step = 0
    x_coords = [margin_left + index * step for index in range(len(indices))]
    top_band = (margin_top, (height / 2) - 16)
    bottom_band = ((height / 2) + 16, height - margin_bottom)

    def series_points(series: Sequence[float], source_range: tuple[float, float], band):
        start_px, end_px = band
        return " ".join(
            f"{x:.1f},{_scale_linear(value, source=source_range, target=(end_px, start_px)):.1f}"
            for x, value in zip(x_coords, series)
        )

    z_points = series_points(z_series, (z_min, z_max), top_band)
    e_points = series_points(extrusion_series, (e_min, e_max), bottom_band)
    escaped_name = html.escape(name)
    return (
        "<svg xmlns=\"http://www.w3.org/2000/svg\" "
        f"width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">"
        f"<title>{escaped_name} timeline</title>"
        "<desc>Z height and yarn feed plotted across emitted commands.</desc>"
        f"<rect x=\"{margin_left}\" y=\"{margin_top}\" "
        f"width=\"{plot_width}\" height=\"{height - margin_top - margin_bottom}\" "
        "fill=\"#f6f8fb\" stroke=\"#cdd5e0\" stroke-width=\"1\"/>"
        f"<line x1=\"{margin_left}\" y1=\"{height/2}\" x2=\"{width - margin_right}\" "
        f"y2=\"{height/2}\" stroke=\"#cdd5e0\" stroke-dasharray=\"4 4\"/>"
        f"<polyline data-series=\"z_mm\" fill=\"none\" stroke=\"#264653\" "
        f"stroke-width=\"2\" points=\"{z_points}\"/>"
        f"<polyline data-series=\"extrusion_mm\" fill=\"none\" stroke=\"#e9c46a\" "
        f"stroke-width=\"2\" points=\"{e_points}\"/>"
        f"<text x=\"{margin_left}\" y=\"{margin_top - 10}\" "
        "font-family=\"sans-serif\" font-size=\"14\" fill=\"#1f2933\">"
        f"{escaped_name} motion timeline</text>"
        f"<text x=\"{margin_left}\" y=\"{height/2 - 8}\" "
        "font-family=\"sans-serif\" font-size=\"12\" fill=\"#264653\">Z (mm)</text>"
        f"<text x=\"{margin_left}\" y=\"{height/2 + 24}\" "
        "font-family=\"sans-serif\" font-size=\"12\" fill=\"#946c00\">Extrusion (mm)</text>"
        f"<text x=\"{width - margin_right - 4}\" y=\"{height - margin_bottom + 24}\" "
        "font-family=\"sans-serif\" font-size=\"12\" fill=\"#1f2933\" text-anchor=\"end\">"
        "Command index</text>"
        "</svg>"
    )


def _load_patterns(pattern_dir: Path, names: Sequence[str] | None) -> List[Path]:
    if names:
        resolved: list[Path] = []
        for raw in names:
            candidate = Path(raw)
            if not candidate.suffix:
                candidate = candidate.with_suffix(".txt")
            if not candidate.is_absolute():
                candidate = pattern_dir / candidate
            if not candidate.exists():
                raise FileNotFoundError(f"Pattern file {candidate} does not exist")
            resolved.append(candidate)
        return sorted(resolved)
    return sorted(pattern_dir.glob("*.txt"))


def generate_previews(
    pattern_paths: Sequence[Path],
    output_dir: Path,
    *,
    force: bool = False,
) -> List[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []
    for pattern_path in pattern_paths:
        translator = PatternTranslator()
        pattern_text = pattern_path.read_text(encoding="utf-8")
        translator.translate(pattern_text)
        events = translator.planner_events
        base_name = pattern_path.stem
        chart_path = output_dir / f"{base_name}-chart.svg"
        timeline_path = output_dir / f"{base_name}-timeline.svg"
        if force or not chart_path.exists():
            chart_path.write_text(
                _xy_chart(events, base_name),
                encoding="utf-8",
            )
        if force or not timeline_path.exists():
            timeline_path.write_text(
                _timeline_chart(events, base_name),
                encoding="utf-8",
            )
        generated.extend([chart_path, timeline_path])
    return generated


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render SVG stitch charts and motion timelines from pattern fixtures."
        )
    )
    parser.add_argument(
        "--pattern-dir",
        type=Path,
        default=DEFAULT_PATTERN_DIR,
        help="Directory containing pattern .txt fixtures (default: %(default)s).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated SVG previews (default: %(default)s).",
    )
    parser.add_argument(
        "--pattern",
        action="append",
        help=(
            "Specific pattern files or basenames to render. Repeat for multiple "
            "patterns. Defaults to all .txt files in --pattern-dir."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate previews even when output files already exist.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        pattern_paths = _load_patterns(args.pattern_dir, args.pattern)
    except FileNotFoundError as error:
        print(f"[ERROR] {error}")
        return 1
    if not pattern_paths:
        print("[INFO] No pattern fixtures found; nothing to render.")
        return 0
    generated = generate_previews(
        pattern_paths,
        args.output_dir,
        force=args.force,
    )
    for path in generated:
        print(f"[INFO] Wrote {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
