"""Ensure CAD documentation covers all modules."""

from __future__ import annotations

from pathlib import Path

import pytest

CAD_DIR = Path(__file__).resolve().parents[1] / "cad"
CAD_README = CAD_DIR / "README.md"
CAD_README_DESCRIPTION_MSG = "CAD README must describe hardware modules"
CAD_README_MISSING_MODULE_MSG = "Missing CAD README modules: {modules}"


def test_cad_readme_exists() -> None:
    assert CAD_README.exists(), CAD_README_DESCRIPTION_MSG


def test_cad_readme_lists_all_modules() -> None:
    content = CAD_README.read_text(encoding="utf-8")
    scad_files = sorted(CAD_DIR.glob("*.scad"))
    missing = [path.name for path in scad_files if path.stem not in content]
    if missing:
        missing_modules = ", ".join(missing)
        message = CAD_README_MISSING_MODULE_MSG.format(modules=missing_modules)
        pytest.fail(message)
