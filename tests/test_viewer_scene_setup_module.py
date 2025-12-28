from __future__ import annotations

from pathlib import Path


def test_scene_setup_module_exports_bootstrap_factory() -> None:
    """Renderer, scene, camera, and controls bootstrap should live in setup.js."""

    setup_path = (
        Path(__file__).resolve().parents[1] / "viewer" / "src" / "scene" / "setup.js"
    )
    source = setup_path.read_text(encoding="utf-8")

    assert "export function createViewerScene" in source
    assert "WebGLRenderer" in source
    assert "PerspectiveCamera" in source
    assert "OrbitControls" in source
    assert "outputColorSpace = THREE.SRGBColorSpace" in source
    assert "DEFAULT_CAMERA_POSITION = new THREE.Vector3(12, 8, 18)" in source
    assert "controlsConfig = {}" in source
    assert "maxPolarAngle: Math.PI * 0.49" in source
    assert "controlsTarget = null" in source
    assert "export { THREE }" in source
