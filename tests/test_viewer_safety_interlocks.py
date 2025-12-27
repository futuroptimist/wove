"""Safety interlock regression checks for the v1c roadmap."""

import re

from tests.viewer_utils import load_viewer_source


def test_viewer_mentions_emergency_stop_and_end_stops():
    html = load_viewer_source()

    assert "Emergency stop switch — instantly cuts power" in html

    pattern = re.compile(r"createEndStop\(.*?,\s*'([XYZ])'\)", re.DOTALL)
    axes = set(pattern.findall(html))
    assert axes == {"X", "Y", "Z"}


def test_overlay_guides_users_to_safety_interlocks():
    html = load_viewer_source()
    assert "The glowing safety interlocks mark physical end stops" in html


def test_end_stop_glow_annotations_present():
    html = load_viewer_source()

    assert "end-stop-${axisLabel.toLowerCase()}-indicator" in html
    assert "end-stop-${axisLabel.toLowerCase()}-halo" in html
