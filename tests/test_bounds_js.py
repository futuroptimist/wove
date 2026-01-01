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


def test_bounds_missing_axes_messages_include_axis_lists() -> None:
    """Missing-axis status lines should name the absent planner/machine bounds."""

    script = textwrap.dedent(
        """
        import { formatMissingBoundsMessage } from './viewer/bounds.js';

        const machineText = formatMissingBoundsMessage('machine', ['x', 'e']);
        const plannerText = formatMissingBoundsMessage('planner', ['y', 'z']);
        const fallbackMachine = formatMissingBoundsMessage('machine');
        const fallbackPlanner = formatMissingBoundsMessage('planner', []);

        console.log(JSON.stringify({
          machine: machineText,
          planner: plannerText,
          fallbackMachine,
          fallbackPlanner,
        }));
        """
    )

    result = run_node(script)

    assert "missing bounds for: X, E" in result["machine"]
    assert "planner export missing bounds for: Y, Z" in result["planner"]
    assert result["fallbackMachine"].endswith("compare envelopes.")
    assert result["fallbackPlanner"].endswith("bounds metadata.")


def test_bounds_missing_axes_defaults_to_generic_message() -> None:
    """Default messages should be generic when the kind is not recognized."""

    script = textwrap.dedent(
        """
        import { formatMissingBoundsMessage } from './viewer/bounds.js';

        const unknown = formatMissingBoundsMessage('unknown', ['x']);
        const emptyKind = formatMissingBoundsMessage(undefined, ['y']);

        console.log(JSON.stringify({ unknown, emptyKind }));
        """
    )

    result = run_node(script)

    assert result["unknown"] == "Bounds check unavailable."
    assert result["emptyKind"] == "Bounds check unavailable."
