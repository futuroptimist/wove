from __future__ import annotations

from .viewer_source import VIEWER_DIR


def test_viewer_tone_helper_module_exists() -> None:
    """Shared tone helpers should live in the ui module for reuse."""

    tone_helper = VIEWER_DIR / "src" / "ui" / "tones.js"

    assert tone_helper.exists()

    content = tone_helper.read_text(encoding="utf-8")
    assert "export function setTone" in content


def test_viewer_imports_shared_tone_helper() -> None:
    """The main viewer module should import the shared tone helper."""

    main_module = (VIEWER_DIR / "src" / "main.js").read_text(encoding="utf-8")

    assert "from './ui/tones.js'" in main_module
    assert "function setTone" not in main_module
