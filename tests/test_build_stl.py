from __future__ import annotations

import os
from pathlib import Path
from typing import List, Sequence, Tuple

import pytest

import wove.build_stl as build_stl

Call = Tuple[str, Path, Path, Tuple[build_stl.Definition, ...]]


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

    def fake_run(
        openscad: str,
        scad_path: Path,
        stl_path: Path,
        defines: Sequence[build_stl.Definition] | None = None,
    ) -> None:
        calls.append((openscad, scad_path, stl_path, tuple(defines or ())))
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
    assert calls == [
        (
            "openscad",
            target,
            stl_dir / "alpha.stl",
            (),
        )
    ]


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
            (),
        )
    ]


def test_resolve_targets_raises_when_scad_dir_missing(tmp_path: Path) -> None:
    missing_dir = tmp_path / "cad"

    with pytest.raises(FileNotFoundError):
        build_stl._resolve_targets(missing_dir, ())


def test_resolve_targets_with_directory_argument(scad_project: Path) -> None:
    targets = build_stl._resolve_targets(scad_project, [str(scad_project)])

    assert targets == [
        scad_project / "alpha.scad",
        scad_project / "nested" / "beta.scad",
    ]


def test_resolve_targets_rejects_non_scad(scad_project: Path) -> None:
    with pytest.raises(ValueError):
        build_stl._resolve_targets(scad_project, ["not_a_scad.txt"])


def test_resolve_targets_missing_file(scad_project: Path) -> None:
    target = scad_project / "missing.scad"
    with pytest.raises(FileNotFoundError):
        build_stl._resolve_targets(scad_project, [str(target)])


def test_stl_path_for_outside_scad_dir(
    tmp_path: Path,
    scad_project: Path,
) -> None:
    stl_dir = tmp_path / "stl"
    outside = scad_project.parent / "external.scad"
    outside.write_text("// ext", encoding="utf-8")

    result = build_stl._stl_path_for(
        scad_project,
        stl_dir,
        outside,
    )

    assert result == stl_dir / "external.stl"


def test_should_skip_force_overrides(
    scad_project: Path,
    tmp_path: Path,
) -> None:
    stale = scad_project / "alpha.scad"
    stl = tmp_path / "alpha.stl"
    stl.write_text("existing", encoding="utf-8")

    skip = build_stl._should_skip(
        stale,
        stl,
        force=True,
    )

    assert skip is False


def test_should_skip_without_output(
    scad_project: Path,
    tmp_path: Path,
) -> None:
    stale = scad_project / "alpha.scad"
    stl = tmp_path / "alpha.stl"

    skip = build_stl._should_skip(
        stale,
        stl,
        force=False,
    )

    assert skip is False


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("", '""'),
        ("   ", '""'),
        ("'quoted'", "'quoted'"),
        ('"quoted"', '"quoted"'),
        ("true", "true"),
        ("FALSE", "false"),
        ("42", "42"),
        ("3.14", "3.14"),
        (
            'needs "escaping" \\ backslash',
            '"needs \\"escaping\\" \\\\ backslash"',
        ),
    ],
)
def test_format_define_value_handles_types(raw: str, expected: str) -> None:
    assert build_stl._format_define_value(raw) == expected


def test_format_define_value_trims_whitespace() -> None:
    assert build_stl._format_define_value("  name  ") == '"name"'


def test_run_openscad_invocation(
    monkeypatch: pytest.MonkeyPatch,
    scad_project: Path,
    tmp_path: Path,
) -> None:
    called_with: List[List[str]] = []

    def fake_run(
        args: List[str],
        check: bool,
    ) -> None:  # type: ignore[override]
        called_with.append(args)

    monkeypatch.setattr(
        build_stl.subprocess,
        "run",
        fake_run,
    )  # type: ignore[arg-type]

    scad = scad_project / "alpha.scad"
    stl = tmp_path / "alpha.stl"

    build_stl._run_openscad("openscad", scad, stl)

    assert called_with == [
        [
            "openscad",
            "-o",
            str(stl),
            str(scad),
        ]
    ]
    assert stl.parent.exists()


def test_run_openscad_with_defines(
    monkeypatch: pytest.MonkeyPatch,
    scad_project: Path,
    tmp_path: Path,
) -> None:
    called_with: List[List[str]] = []

    def fake_run(args: List[str], check: bool) -> None:
        # type: ignore[override]
        called_with.append(args)

    # type: ignore[arg-type]
    monkeypatch.setattr(build_stl.subprocess, "run", fake_run)

    scad = scad_project / "alpha.scad"
    stl = tmp_path / "alpha.stl"

    build_stl._run_openscad(
        "openscad",
        scad,
        stl,
        defines=[
            ("STANDOFF_MODE", "printed"),
            ("HEIGHT_MM", "12.5"),
        ],
    )

    assert called_with == [
        [
            "openscad",
            "-D",
            'STANDOFF_MODE="printed"',
            "-D",
            "HEIGHT_MM=12.5",
            "-o",
            str(stl),
            str(scad),
        ]
    ]


def test_render_stls_handles_skips(
    monkeypatch: pytest.MonkeyPatch,
    scad_project: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    calls = _recorded_calls(monkeypatch)
    stl_dir = tmp_path / "out"
    stl_dir.mkdir()

    up_to_date = stl_dir / "nested" / "beta.stl"
    up_to_date.parent.mkdir(parents=True, exist_ok=True)
    up_to_date.write_text("fresh", encoding="utf-8")

    mtime = (scad_project / "nested" / "beta.scad").stat().st_mtime
    os.utime(up_to_date, (mtime + 50, mtime + 50))

    build_stl.render_stls(
        scad_project,
        stl_dir,
        [
            scad_project / "alpha.scad",
            scad_project / "nested" / "beta.scad",
        ],
        "openscad",
        defines=[("STANDOFF_MODE", "printed")],
    )

    captured = capsys.readouterr()
    assert "Skipping" in captured.out
    assert calls == [
        (
            "openscad",
            scad_project / "alpha.scad",
            stl_dir / "alpha.stl",
            (("STANDOFF_MODE", "printed"),),
        )
    ]


def test_main_handles_errors(
    scad_project: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    bad_target = scad_project / "missing.scad"

    exit_code = build_stl.main(
        [
            "--scad-dir",
            str(scad_project),
            str(bad_target),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "does not exist" in captured.out


def test_main_rejects_bad_define(
    scad_project: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = build_stl.main(
        [
            "--scad-dir",
            str(scad_project),
            "--define",
            "invalid",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "KEY=VALUE" in captured.out


def test_main_reports_no_targets(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    empty_scad = tmp_path / "cad"
    empty_scad.mkdir()

    exit_code = build_stl.main(
        [
            "--scad-dir",
            str(empty_scad),
            "--stl-dir",
            str(tmp_path / "stl"),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "No .scad files found" in captured.out
