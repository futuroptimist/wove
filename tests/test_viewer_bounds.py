"""Sanity checks for viewer bounds helpers executed via Node."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def run_node_snippet(script: str) -> dict:
    project_root = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        ["node", "-e", script],
        cwd=project_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout.strip())


def test_travel_envelope_box_includes_offsets() -> None:
    script = r'''
import { buildTravelEnvelopeBox } from './viewer/bounds.js';

const output = buildTravelEnvelopeBox(
  {
    x: { min: -10, max: 40 },
    y: { min: 5, max: 25 },
    z: { min: 2, max: 12 },
  },
  { x: 480, y: 320, z: 120 },
);

console.log(JSON.stringify(output));
'''
    result = run_node_snippet(script)
    assert result == {
        "width": 50,
        "depth": 20,
        "height": 10,
        "centerX": 15,
        "centerY": 15,
        "centerZ": 7,
    }


def test_travel_envelope_box_falls_back_to_bed_span() -> None:
    script = r'''
import { buildTravelEnvelopeBox } from './viewer/bounds.js';

const output = buildTravelEnvelopeBox(null, { x: 480, y: 320, z: 120 });

console.log(JSON.stringify(output));
'''
    result = run_node_snippet(script)
    assert result == {
        "width": 480,
        "depth": 320,
        "height": 120,
        "centerX": 0,
        "centerY": 0,
        "centerZ": 0,
    }
