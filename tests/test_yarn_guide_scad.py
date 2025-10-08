from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
YARN_GUIDE_SCAD = REPO_ROOT / "cad" / "yarn_guide.scad"
BASE_MARKER = "cylinder(h=base_height, d=base_diameter)"
POST_MARKER = "cylinder(h=post_height, d=post_diameter)"


@pytest.fixture(scope="module")
def yarn_guide_source() -> str:
    return YARN_GUIDE_SCAD.read_text(encoding="utf-8")


def test_yarn_guide_exposes_integrated_post_parameter(
    yarn_guide_source: str,
) -> None:
    match = re.search(r"module\s+yarn_guide\(([^)]*)\)", yarn_guide_source)
    assert match, "yarn_guide module must declare parameters"
    parameters = match.group(1)
    assert "integrated_post" in parameters
    assert "post_diameter" in parameters
    assert "post_height" in parameters
    assert "base_diameter" in parameters
    assert "base_height" in parameters


def test_yarn_guide_integration_uses_union_block(
    yarn_guide_source: str,
) -> None:
    assert "if (integrated_post)" in yarn_guide_source
    assert "union()" in yarn_guide_source
    assert BASE_MARKER in yarn_guide_source
    assert POST_MARKER in yarn_guide_source
    assert "is_undef(post_offset)" in yarn_guide_source
