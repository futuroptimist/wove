from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_node(script: str) -> dict:
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        check=True,
    )
    return json.loads(result.stdout)


def test_bounds_comparison_accepts_uppercase_axes() -> None:
    """Machine profile bounds should be case-insensitive."""

    script = textwrap.dedent(
        """
        import { comparePlannerToMachineBounds } from './viewer/bounds.js';

        const planner = {
          X: { min: 0, max: 120 },
          y: { min: -5, max: 55 },
          Z: { min: 0, max: 40 },
          extrusion: { min: 0, max: 30 },
        };

        const machine = {
          x: { min: -10, max: 130 },
          Y: { min: -10, max: 60 },
          z: { min: -2, max: 42 },
          E: { min_mm: 0, max_mm: 35 },
        };

        const comparison = comparePlannerToMachineBounds(planner, machine);

        console.log(JSON.stringify({
          missingPlanner: comparison.missingPlanner,
          missingMachine: comparison.missingMachine,
          fits: comparison.fits,
          exceeding: comparison.exceedingAxes,
        }));
        """
    )

    result = run_node(script)

    assert result["missingPlanner"] is False
    assert result["missingMachine"] is False
    assert result["fits"] is True
    assert result["exceeding"] == []
