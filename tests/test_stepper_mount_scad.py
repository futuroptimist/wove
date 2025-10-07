from __future__ import annotations

import re
from pathlib import Path

import pytest

STEPPER_SCAD = (
    Path(__file__)
    .resolve()
    .parents[1]
    .joinpath(
        "cad",
        "stepper_mount.scad",
    )
)


@pytest.fixture(scope="module")
def stepper_source() -> str:
    return STEPPER_SCAD.read_text(encoding="utf-8")


def test_stepper_mount_exposes_mounting_hole_parameters(
    stepper_source: str,
) -> None:
    match = re.search(
        r"module\s+stepper_mount\(([^)]*)\)",
        stepper_source,
    )
    assert match, "stepper_mount module must declare parameters"
    parameters = match.group(1)
    assert "hole_spacing" in parameters, "hole_spacing parameter missing"
    assert "hole_diameter" in parameters, "hole_diameter parameter missing"


def test_stepper_mount_defines_corner_holes(stepper_source: str) -> None:
    message = "hole spacing should be used in geometry"
    assert "hole_spacing" in stepper_source, message
    assert "for (x_sign = [-1, 1])" in stepper_source
    assert "for (y_sign = [-1, 1])" in stepper_source
    assert "cylinder(d=hole_diameter" in stepper_source
    spaced = "hole_spacing / 2" in stepper_source
    unspaced = "hole_spacing/2" in stepper_source
    assert spaced or unspaced
