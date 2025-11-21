from __future__ import annotations

import json
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_node(script: str) -> dict:
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        check=True,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    return json.loads(result.stdout.strip())


def test_bounds_detects_overruns():
    script = "".join(
        [
            "import { comparePlannerToMachineBounds } from './viewer/bounds.js';",
            (
                "const planner = { x: { min: 0, max: 250 }, "
                "y: { min: -10, max: 200 }, z: { min: 0, max: 90 } };"
            ),
            (
                "const machine = { x: { min: 0, max: 220 }, "
                "y: { min: 0, max: 200 }, z: { min: 0, max: 120 } };"
            ),
            "const result = comparePlannerToMachineBounds(planner, machine);",
            "console.log(JSON.stringify(result));",
        ]
    )
    result = run_node(script)

    assert result["fits"] is False
    assert set(result["exceedingAxes"]) == {"x", "y"}
    x_detail = result["details"].get("x")
    assert x_detail["overrunHigh"] is True
    assert x_detail["overrunLow"] is False


def test_bounds_reports_fit_when_envelopes_match():
    script = "".join(
        [
            "import { comparePlannerToMachineBounds } from './viewer/bounds.js';",
            (
                "const planner = { x: { min: 0, max: 200 }, "
                "y: { min: 0, max: 200 }, z: { min: 0, max: 100 } };"
            ),
            (
                "const machine = { x: { min: 0, max: 220 }, "
                "y: { min: -20, max: 220 }, z: { min: 0, max: 120 } };"
            ),
            "const result = comparePlannerToMachineBounds(planner, machine);",
            "console.log(JSON.stringify(result));",
        ]
    )
    result = run_node(script)

    assert result["fits"] is True
    assert result["exceedingAxes"] == []
    assert result["missingMachine"] is False
    assert result["missingPlanner"] is False


def test_bounds_warns_when_axis_metadata_missing():
    script = "".join(
        [
            "import { comparePlannerToMachineBounds } from './viewer/bounds.js';",
            "const planner = { x: { min: 0, max: 200 }, y: { min: 0, max: 200 } };",
            "const machine = { x: { min: 0, max: 220 }, z: { min: 0, max: 120 } };",
            "const result = comparePlannerToMachineBounds(planner, machine);",
            "console.log(JSON.stringify(result));",
        ]
    )
    result = run_node(script)

    assert result["fits"] is False
    assert result["missingMachine"] is True
    assert result["missingPlanner"] is True
    assert set(result["missingPlannerAxes"]) == {"z"}
    assert set(result["missingMachineAxes"]) == {"y"}
