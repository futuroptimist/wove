"""Ensure the electronics bay exhaust shows animated blades in the viewer."""

from __future__ import annotations

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIEWER_HTML = PROJECT_ROOT / "viewer" / "index.html"


def test_exhaust_blades_render_and_spin() -> None:
    """Exhaust fan exposes spinning blades linked to extrusion."""

    html = VIEWER_HTML.read_text(encoding="utf-8")

    assert "electronics-bay-exhaust-blades" in html
    assert "Electronics bay exhaust blades" in html
    assert re.search(
        r"fanControllers\.push\(\s*\{[\s\S]*?mesh:\s*fanBlades",
        html,
        flags=re.DOTALL,
    )
    assert "linkedToExtrusion: true" in html
