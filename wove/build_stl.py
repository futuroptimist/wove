"""Helpers for rendering OpenSCAD files to STL outputs."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path
from typing import Iterable, List, Sequence

DEFAULT_SCAD_DIR = Path(os.environ.get("SCAD_DIR", "cad"))
DEFAULT_STL_DIR = Path(os.environ.get("STL_DIR", "stl"))
DEFAULT_OPENSCAD = os.environ.get("OPENSCAD", "openscad")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render OpenSCAD sources to STL files",
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help=(
            "Specific .scad files or directories to render. "
            "Default is all files in --scad-dir."
        ),
    )
    parser.add_argument(
        "--scad-dir",
        type=Path,
        default=DEFAULT_SCAD_DIR,
        help="Directory containing .scad sources (default: %(default)s).",
    )
    parser.add_argument(
        "--stl-dir",
        type=Path,
        default=DEFAULT_STL_DIR,
        help="Destination directory for STL outputs (default: %(default)s).",
    )
    parser.add_argument(
        "--openscad",
        default=DEFAULT_OPENSCAD,
        help="OpenSCAD executable to invoke (default: %(default)s).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Render even if the STL appears up to date.",
    )
    return parser.parse_args(argv)


def _resolve_targets(scad_dir: Path, targets: Sequence[str]) -> List[Path]:
    if not targets:
        if not scad_dir.exists():
            message = f"SCAD directory {scad_dir} does not exist"
            raise FileNotFoundError(message)
        return sorted(scad_dir.rglob("*.scad"))

    resolved: List[Path] = []
    seen: set[Path] = set()
    for raw in targets:
        path = Path(raw)
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
        if path.is_dir():
            for scad_file in sorted(path.rglob("*.scad")):
                if scad_file not in seen:
                    resolved.append(scad_file)
                    seen.add(scad_file)
            continue
        if path.suffix.lower() != ".scad":
            raise ValueError(f"Target {raw} is not a .scad file")
        if not path.exists():
            raise FileNotFoundError(f"Target {path} does not exist")
        if path not in seen:
            resolved.append(path)
            seen.add(path)
    return resolved


def _stl_path_for(scad_dir: Path, stl_dir: Path, scad_path: Path) -> Path:
    scad_dir_resolved = scad_dir.resolve()
    try:
        relative = scad_path.resolve().relative_to(scad_dir_resolved)
    except ValueError:
        relative = Path(scad_path.name)
    return stl_dir / relative.with_suffix(".stl")


def _should_skip(scad_path: Path, stl_path: Path, force: bool) -> bool:
    if force:
        return False
    if not stl_path.exists():
        return False
    return stl_path.stat().st_mtime >= scad_path.stat().st_mtime


def _run_openscad(openscad: str, scad_path: Path, stl_path: Path) -> None:
    stl_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [openscad, "-o", str(stl_path), str(scad_path)],
        check=True,
    )


def render_stls(
    scad_dir: Path,
    stl_dir: Path,
    targets: Iterable[Path],
    openscad: str,
    force: bool = False,
) -> None:
    for scad_path in targets:
        stl_path = _stl_path_for(scad_dir, stl_dir, scad_path)
        if _should_skip(scad_path, stl_path, force):
            print(f"[INFO] Skipping {scad_path}; STL up to date")
            continue
        print(f"[INFO] Exporting {scad_path} -> {stl_path}")
        _run_openscad(openscad, scad_path, stl_path)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        targets = _resolve_targets(args.scad_dir, args.targets)
    except (FileNotFoundError, ValueError) as error:
        print(f"[ERROR] {error}")
        return 1

    if not targets:
        print("[INFO] No .scad files found to render")
        return 0

    render_stls(
        args.scad_dir,
        args.stl_dir,
        targets,
        args.openscad,
        force=args.force,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
