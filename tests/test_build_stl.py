from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

import pytest

import wove.build_stl as build_stl

Call = Tuple[str, Path, Path]


@pytest.fixture()
def scad_project(tmp_path: Path) -> Path:
    scad_dir = tmp_path / "cad"
    nested = scad_dir / "nested"
    nested.mkdir(parents=True)
    (scad_dir / "alpha.scad").write_text("// alpha", encoding="utf-8")
    (nested / "beta.scad").write_text("// beta", encoding="utf-8")
    return scad_dir


def _recorded_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> List[Call]:
    calls: List[Call] = []

    def fake_run(openscad: str, scad_path: Path, stl_path: Path) -> None:
        calls.append((openscad, scad_path, stl_path))
        stl_path.parent.mkdir(parents=True, exist_ok=True)
        stl_path.write_text("rendered", encoding="utf-8")

    monkeypatch.setattr(build_stl, "_run_openscad", fake_run)
    return calls


def test_render_specific_file(
    monkeypatch: pytest.MonkeyPatch,
    scad_project: Path,
    tmp_path: Path,
) -> None:
    calls = _recorded_calls(monkeypatch)
    target = scad_project / "alpha.scad"
    stl_dir = tmp_path / "out"

    exit_code = build_stl.main(
        [
            "--scad-dir",
            str(scad_project),
            "--stl-dir",
            str(stl_dir),
            str(target),
        ]
    )

    assert exit_code == 0
    assert calls == [("openscad", target, stl_dir / "alpha.stl")]


def test_skip_up_to_date_file(
    monkeypatch: pytest.MonkeyPatch,
    scad_project: Path,
    tmp_path: Path,
) -> None:
    calls = _recorded_calls(monkeypatch)
    stl_dir = tmp_path / "stl"
    stl_dir.mkdir()

    stale = scad_project / "nested" / "beta.scad"
    output = stl_dir / "nested" / "beta.stl"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("older", encoding="utf-8")

    mtime = stale.stat().st_mtime
    os.utime(output, (mtime + 100, mtime + 100))

    build_stl.main(
        [
            "--scad-dir",
            str(scad_project),
            "--stl-dir",
            str(stl_dir),
        ]
    )

    # alpha.scad renders; beta.scad is skipped because its STL is newer.
    assert calls == [
        (
            "openscad",
            scad_project / "alpha.scad",
            stl_dir / "alpha.stl",
        )
    ]
