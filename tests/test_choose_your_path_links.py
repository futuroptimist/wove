"""Regression checks for Choose Your Path cross-links."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
README = PROJECT_ROOT / "README.md"
DOCS_INDEX = PROJECT_ROOT / "docs" / "index.md"


def test_readme_tracks_link_to_supporting_material() -> None:
    """Ensure the README cross-links reinforce the curriculum tracks."""

    content = README.read_text(encoding="utf-8")
    assert "[Learning resources](docs/learning-resources.md)" in content
    assert "[crochet tools guide](docs/crochet-tools.md)" in content
    assert "[Yarn Handling benchmarks](docs/wove-v1c-design.md#yarn-handling)" in content
    assert "[base chain row recipe](docs/learn/pattern-recipes/base-chain-row.md)" in content


def test_docs_index_tracks_link_to_supporting_material() -> None:
    """Ensure the Sphinx index mirrors the same cross-links."""

    content = DOCS_INDEX.read_text(encoding="utf-8")
    assert "[Learning resources](learning-resources.md)" in content
    assert "[Crochet tools](crochet-tools.md)" in content
    assert "[Yarn Handling benchmarks](wove-v1c-design.md#yarn-handling)" in content
    assert "[base chain row recipe](learn/pattern-recipes/base-chain-row.md)" in content
