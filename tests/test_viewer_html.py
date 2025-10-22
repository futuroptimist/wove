from pathlib import Path


def _load_viewer_html() -> str:
    viewer_path = Path(__file__).resolve().parents[1] / "viewer" / "index.html"
    return viewer_path.read_text(encoding="utf-8")


def test_viewer_exposes_roadmap_panel() -> None:
    """Ensure the viewer documents the roadmap spotlight UI."""

    viewer_html = _load_viewer_html()

    for snippet in [
        'id="roadmap-title"',
        "function selectCluster",
        "Click a pedestal to spotlight its roadmap milestone.",
    ]:
        assert snippet in viewer_html


def test_viewer_declares_product_clusters() -> None:
    """Ensure the viewer script ships the product cluster pedestals."""

    viewer_html = _load_viewer_html()

    for snippet in [
        "const productClusters = []",
        "function createPedestalCluster",
        "Tension Lab",
        "Material Prep Pod",
        "Pattern Studio",
        "v1k Research Rig",
        "function createMaterialPrepDisplay",
        "function createV1KResearchDisplay",
    ]:
        assert snippet in viewer_html


def test_viewer_includes_safety_shield() -> None:
    """Ensure the viewer documents the polycarbonate safety enclosure."""

    viewer_html = _load_viewer_html()

    assert "Polycarbonate Shield" in viewer_html


def test_viewer_mentions_extrusion_frame() -> None:
    """Ensure the new extrusion frame callouts land in the viewer copy."""

    viewer_html = _load_viewer_html()

    hover_copy = (
        "Aluminum extrusion frame — 20×20 mm perimeter with corner cubes and "
        "leveling feet."
    )
    assert hover_copy in viewer_html
    assert "Extrusion Frame" in viewer_html


def test_viewer_mentions_safe_access_path() -> None:
    """Ensure the walkway guidance text ships with the viewer."""

    viewer_html = _load_viewer_html()

    assert "Mint-lit safe access path" in viewer_html
    assert "alternating" in viewer_html.lower()


def test_viewer_spotlights_magnetic_anchors() -> None:
    """Ensure the magnetic anchor studs are documented in the viewer."""

    viewer_html = _load_viewer_html()

    assert (
        "Magnetic anchor puck — secures swap-in plates with embedded magnets."
        in viewer_html
    )
    assert "Magnetic Anchors" in viewer_html


def test_viewer_exposes_planner_controls() -> None:
    """Ensure the planner hologram controls are shipped with the viewer."""

    viewer_html = _load_viewer_html()

    for snippet in [
        'id="planner-panel"',
        "Planner Hologram Controls",
        'id="planner-toggle"',
        'id="planner-progress"',
        'id="planner-current-comment"',
    ]:
        assert snippet in viewer_html
