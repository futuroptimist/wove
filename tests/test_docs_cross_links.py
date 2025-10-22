"""Regression tests for cross-track documentation cross-links."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"


def test_knitting_basics_calls_out_next_steps() -> None:
    """Knitting basics should guide readers toward deeper resources."""

    text = (DOCS_DIR / "knitting-basics.md").read_text(encoding="utf-8")

    assert "[Learning resources](learning-resources.md)" in text
    assert "sensor calibration" in text
    assert "[Pattern translation CLI](pattern-cli.md)" in text


def test_crochet_basics_links_to_materials_and_automation() -> None:
    """Crochet basics should mirror the cross-track guidance."""

    text = (DOCS_DIR / "crochet-basics.md").read_text(encoding="utf-8")

    assert "[Learning resources](learning-resources.md)" in text
    assert "sensor calibration" in text
    assert "[Pattern translation CLI](pattern-cli.md)" in text
