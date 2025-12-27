from tests.viewer_utils import load_viewer_source


def test_viewer_exposes_roadmap_panel() -> None:
    """Ensure the viewer documents the roadmap spotlight UI."""

    viewer_html = load_viewer_source()

    for snippet in [
        'id="roadmap-title"',
        "function selectCluster",
        (
            "Click a pedestal to spotlight its roadmap milestone and "
            "watch the camera glide to frame it."
        ),
    ]:
        assert snippet in viewer_html


def test_viewer_declares_product_clusters() -> None:
    """Ensure the viewer script ships the product cluster pedestals."""

    viewer_html = load_viewer_source()

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

    viewer_html = load_viewer_source()

    assert "Polycarbonate Shield" in viewer_html


def test_viewer_mentions_extrusion_frame() -> None:
    """Ensure the new extrusion frame callouts land in the viewer copy."""

    viewer_html = load_viewer_source()

    hover_copy = (
        "Aluminum extrusion frame — 20×20 mm perimeter with corner cubes and "
        "leveling feet."
    )
    assert hover_copy in viewer_html
    assert "Extrusion Frame" in viewer_html


def test_viewer_mentions_safe_access_path() -> None:
    """Ensure the walkway guidance text ships with the viewer."""

    viewer_html = load_viewer_source()

    assert "Mint-lit safe access path" in viewer_html
    assert "alternating" in viewer_html.lower()


def test_viewer_spotlights_magnetic_anchors() -> None:
    """Ensure the magnetic anchor studs are documented in the viewer."""

    viewer_html = load_viewer_source()

    assert (
        "Magnetic anchor puck — secures swap-in plates with embedded magnets."
        in viewer_html
    )
    assert "Magnetic Anchors" in viewer_html


def test_viewer_mentions_servo_tension_adjuster() -> None:
    """Ensure the servo-driven tension adjuster lands in the viewer copy."""

    viewer_html = load_viewer_source()

    assert "Micro-servo tension adjuster" in viewer_html
    assert "Servo Tensioner Prototype" in viewer_html


def test_viewer_surfaces_controller_stack() -> None:
    """Ensure the electronics bay exposes the controller stack details."""

    viewer_html = load_viewer_source()

    assert "Controller stack PCB" in viewer_html
    assert "controllerStackGlowControllers" in viewer_html


def test_viewer_highlights_machine_profile_overlay() -> None:
    """Ensure the viewer advertises the machine profile metadata panel."""

    viewer_html = load_viewer_source()

    assert "Machine Profile" in viewer_html
    assert "Machine profile metadata unavailable" in viewer_html
    assert "Planner-aligned axis settings" in viewer_html


def test_viewer_surfaces_machine_profile_envelope_fallback() -> None:
    """The machine profile envelope should render a helpful fallback message."""

    viewer_html = load_viewer_source()

    assert (
        "Machine profile envelope unavailable. Include travel_min_mm and "
        in viewer_html
    )
    assert "travel_max_mm for each axis." in viewer_html


def test_viewer_surfaces_yarn_flow_monitor() -> None:
    """Ensure the yarn flow overlay ships with idle messaging."""

    viewer_html = load_viewer_source()

    assert "Yarn Flow Monitor" in viewer_html
    assert "Yarn flow monitor idle" in viewer_html
    assert "Spool status: Parked" in viewer_html


def test_viewer_surfaces_homing_guard_panel() -> None:
    """Ensure the viewer surfaces the homing guard metadata panel."""

    viewer_html = load_viewer_source()

    assert "Homing Guard" in viewer_html
    homing_guard_copy = (
        "Requires a homed machine before executing this planner preview."
    )
    assert homing_guard_copy in viewer_html


def test_viewer_surfaces_planner_metadata_panel() -> None:
    """Ensure the planner metadata overlay advertises schema details."""

    viewer_html = load_viewer_source()

    assert "Planner Metadata" in viewer_html
    assert "planner-metadata-status" in viewer_html
    assert "Planner metadata unavailable." in viewer_html


def test_viewer_patterns_surface_position_overlay() -> None:
    """Ensure the Pattern Studio panel advertises live coordinate updates."""

    viewer_html = load_viewer_source()

    assert 'id="pattern-position"' in viewer_html
    assert "Position: Loading planner coordinates" in viewer_html


def test_safe_access_step_badges_hover() -> None:
    """Hovering step signage should be animated for the safe access path."""

    viewer_html = load_viewer_source()

    assert "const stepBadgeControllers" in viewer_html
    assert "stepBadgeControllers.push" in viewer_html
    assert "badge.position.y = baseHeight + verticalOffset" in viewer_html
