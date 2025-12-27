from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VIEWER_INDEX = PROJECT_ROOT / "viewer" / "index.html"
VIEWER_CONFIG = PROJECT_ROOT / "viewer" / "src" / "viewer-config.js"


def load_viewer_sources() -> str:
    """Return the concatenated viewer HTML and supporting config module."""

    sources = [VIEWER_INDEX.read_text(encoding="utf-8")]
    if VIEWER_CONFIG.exists():
        sources.append(VIEWER_CONFIG.read_text(encoding="utf-8"))
    return "\n".join(sources)
