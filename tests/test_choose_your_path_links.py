"""Regression checks for Choose Your Path cross-links."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
README = PROJECT_ROOT / "README.md"
DOCS_INDEX = PROJECT_ROOT / "docs" / "index.md"


def test_readme_tracks_link_to_supporting_material() -> None:
    """Ensure the README cross-links reinforce the curriculum tracks."""

    content = README.read_text(encoding="utf-8")
    expected_links = [
        "[Learning resources](docs/learning-resources.md)",
        "[crochet tools guide](docs/crochet-tools.md)",
        ("[Yarn Handling benchmarks]" "(docs/wove-v1c-design.md#yarn-handling)"),
        ("[base chain row recipe]" "(docs/learn/pattern-recipes/base-chain-row.md)"),
    ]

    for link in expected_links:
        assert link in content


def test_docs_index_tracks_link_to_supporting_material() -> None:
    """Ensure the Sphinx index mirrors the same cross-links."""

    content = DOCS_INDEX.read_text(encoding="utf-8")
    expected_links = [
        "[Learning resources](learning-resources.md)",
        "[Crochet tools](crochet-tools.md)",
        "{ref}`Yarn Handling benchmarks <yarn-handling>`",
        "[base chain row recipe](learn/pattern-recipes/base-chain-row.md)",
    ]

    for link in expected_links:
        assert link in content
