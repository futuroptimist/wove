"""Ensure CAD documentation covers all modules."""
from __future__ import annotations

from pathlib import Path

CAD_DIR = Path(__file__).resolve().parents[1] / "cad"
CAD_README = CAD_DIR / "README.md"


def test_cad_readme_exists() -> None:
    assert CAD_README.exists(), "cad/README.md should describe hardware modules"


def test_cad_readme_lists_all_modules() -> None:
    content = CAD_README.read_text(encoding="utf-8")
    scad_files = sorted(CAD_DIR.glob("*.scad"))
    missing = [path.name for path in scad_files if path.stem not in content]
    assert not missing, f"Missing module entries in CAD README: {missing}"
