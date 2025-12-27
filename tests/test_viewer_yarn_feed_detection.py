"""Ensure the Yarn Flow overlays follow extrusion-based feed detection."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest


HTML_PATH = Path("viewer/index.html")
_UNDEFINED = object()


def extract_function_block(html: str, function_name: str) -> str:
    """Return the full function definition by slicing to the next function."""

    start_token = f"function {function_name}"
    try:
        start_index = html.index(start_token)
    except ValueError as exc:
        raise AssertionError(f"{function_name} not found in viewer HTML") from exc

    start_of_remainder = start_index + len(start_token)
    remainder_tail = html[start_of_remainder:]
    next_match = re.search(r"\n\s*function [^(]+\(", remainder_tail, flags=re.MULTILINE)
    end_index = (
        start_index + len(start_token) + next_match.start()
        if next_match is not None
        else len(html)
    )
    return html[start_index:end_index].strip()


def compute_yarn_feed_indices(
    events: list[object], baseline: object = _UNDEFINED
) -> list[int]:
    """Execute the viewer helper in Node to validate the detection behavior."""

    html = HTML_PATH.read_text(encoding="utf-8")
    coerce_fn = extract_function_block(html, "coerceFiniteNumber")
    compute_fn = extract_function_block(html, "computeYarnFeedIndices")
    baseline_js = "undefined" if baseline is _UNDEFINED else json.dumps(baseline)
    script = "\n".join(
        [
            coerce_fn,
            compute_fn,
            f"const events = {json.dumps(events)};",
            f"const baseline = {baseline_js};",
            "const result = computeYarnFeedIndices(events, baseline);",
            "console.log(JSON.stringify(result));",
        ],
    )
    completed = subprocess.run(
        ["node", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout.strip() or "[]")


def test_extrusion_deltas_trigger_feed_pulses() -> None:
    """Extrusion growth beyond tolerance should mark feed indices."""

    events = [
        {"extrusion": 0.0},
        {"extrusion": 0.00005},
        {"extrusion": 0.1},
    ]

    assert compute_yarn_feed_indices(events, baseline=0.0) == [2]


def test_constant_extrusion_does_not_feed() -> None:
    """Flat extrusion keeps the feed list empty."""

    events = [{"extrusion": 1.0}, {"extrusion": 1.0}, {"extrusion": 0.99999}]

    assert compute_yarn_feed_indices(events, baseline=1.0) == []


def test_comment_only_events_still_register_feeds() -> None:
    """Comment fallbacks catch feed pulses even without extrusion values."""

    events = [
        {"comment": "Feed yarn now"},
        {"comment": "still feed yarn", "extrusion": None},
        {"comment": "noop"},
    ]

    assert compute_yarn_feed_indices(events) == [0, 1]


def test_mixed_extrusion_and_comments() -> None:
    """Mixed scenarios should honor both extrusion jumps and textual cues."""

    events = [
        {"extrusion": 0.0, "comment": "start"},
        {"comment": "feed yarn during jump"},
        {"extrusion": 0.00005},
        {"extrusion": 0.2},
    ]

    assert compute_yarn_feed_indices(events, baseline=0.0) == [1, 3]


def test_empty_or_null_inputs_return_empty_indices() -> None:
    """Empty planner events or unparseable entries should not throw."""

    assert compute_yarn_feed_indices([], baseline=None) == []
    assert compute_yarn_feed_indices([None, {}]) == []


def test_extract_function_block_reports_missing_symbol() -> None:
    """The helper should surface a clear assertion when functions go missing."""

    html = HTML_PATH.read_text(encoding="utf-8")
    with pytest.raises(AssertionError, match="missingFunctionNotPresent"):
        extract_function_block(html, "missingFunctionNotPresent")
