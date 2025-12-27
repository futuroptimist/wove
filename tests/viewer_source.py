"""Shared helpers for loading the viewer source code during tests."""

from __future__ import annotations

from pathlib import Path

VIEWER_DIR = Path(__file__).resolve().parents[1] / "viewer"


def load_viewer_bundle() -> str:
    """Return a concatenated view of the viewer HTML, main module, and constants."""

    html = (VIEWER_DIR / "index.html").read_text(encoding="utf-8")
    script = (VIEWER_DIR / "src" / "main.js").read_text(encoding="utf-8")
    constants = (VIEWER_DIR / "src" / "constants.js").read_text(encoding="utf-8")
    return html + script + constants
