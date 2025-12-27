"""Ensure the electronics bay exhaust shows animated blades in the viewer."""

from __future__ import annotations

import re

from tests.viewer_utils import load_viewer_source


def test_exhaust_blades_render_and_spin() -> None:
    """Exhaust fan exposes spinning blades linked to extrusion."""

    html = load_viewer_source()

    assert "electronics-bay-exhaust-blades" in html
    assert "Electronics bay exhaust blades" in html
    assert re.search(
        r"fanControllers\.push\(\s*\{[\s\S]*?mesh:\s*fanBlades",
        html,
        flags=re.DOTALL,
    )
    assert "linkedToExtrusion: true" in html
