"""Safety interlock regression checks for the v1c roadmap."""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIEWER_HTML = PROJECT_ROOT / "viewer" / "index.html"


def test_viewer_mentions_emergency_stop_and_end_stops():
    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "Emergency stop switch — instantly cuts power" in html

    pattern = re.compile(r"createEndStop\(.*?,\s*'([XYZ])'\)", re.DOTALL)
    axes = set(pattern.findall(html))
    assert axes == {"X", "Y", "Z"}


def test_overlay_guides_users_to_safety_interlocks():
    html = VIEWER_HTML.read_text(encoding="utf-8")
    assert "The glowing safety interlocks mark physical end stops" in html


def test_end_stop_glow_annotations_present():
    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "end-stop-${axisLabel.toLowerCase()}-indicator" in html
    assert "end-stop-${axisLabel.toLowerCase()}-halo" in html
