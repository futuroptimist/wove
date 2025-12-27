"""Ensure the electronics bay exhaust shows animated blades in the viewer."""

from __future__ import annotations

import re

from .viewer_source import load_viewer_bundle


def test_exhaust_blades_render_and_spin() -> None:
    """Exhaust fan exposes spinning blades linked to extrusion."""

    viewer_source = load_viewer_bundle()

    assert "electronics-bay-exhaust-blades" in viewer_source
    assert "Electronics bay exhaust blades" in viewer_source
    assert re.search(
        r"fanControllers\.push\(\s*\{[\s\S]*?mesh:\s*fanBlades",
        viewer_source,
        flags=re.DOTALL,
    )
    assert "linkedToExtrusion: true" in viewer_source
