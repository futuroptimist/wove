from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VIEWER_HTML = PROJECT_ROOT / "viewer" / "index.html"
VIEWER_MAIN = PROJECT_ROOT / "viewer" / "src" / "main.js"


def load_viewer_source() -> str:
    """Return combined viewer HTML and entry module source."""

    html = VIEWER_HTML.read_text(encoding="utf-8")
    main = VIEWER_MAIN.read_text(encoding="utf-8")
    return f"{html}\n{main}"
