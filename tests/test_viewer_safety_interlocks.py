"""Safety interlock regression checks for the v1c roadmap."""

import re

from .viewer_source import load_viewer_bundle


def test_viewer_mentions_emergency_stop_and_end_stops():
    viewer_source = load_viewer_bundle()

    assert "Emergency stop switch — instantly cuts power" in viewer_source

    pattern = re.compile(r"createEndStop\(.*?,\s*'([XYZ])'\)", re.DOTALL)
    axes = set(pattern.findall(viewer_source))
    assert axes == {"X", "Y", "Z"}


def test_overlay_guides_users_to_safety_interlocks():
    viewer_source = load_viewer_bundle()
    assert "The glowing safety interlocks mark physical end stops" in viewer_source


def test_end_stop_glow_annotations_present():
    viewer_source = load_viewer_bundle()

    assert "end-stop-${axisLabel.toLowerCase()}-indicator" in viewer_source
    assert "end-stop-${axisLabel.toLowerCase()}-halo" in viewer_source
