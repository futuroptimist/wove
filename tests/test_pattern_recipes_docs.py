from __future__ import annotations

from pathlib import Path

import pytest

from wove.pattern_cli import PatternTranslator

ROOT_DIR = Path(__file__).resolve().parents[1]
RECIPES_DIR = ROOT_DIR / "docs" / "learn" / "pattern-recipes"


def _extract_pattern_blocks(path: Path) -> list[str]:
    blocks: list[str] = []
    inside = False
    current: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not inside and stripped.startswith("```pattern-cli"):
            inside = True
            current = []
            continue
        if inside and stripped == "```":
            inside = False
            snippet = "\n".join(current).strip()
            if snippet:
                blocks.append(snippet)
            continue
        if inside:
            current.append(line)
    return blocks


def test_pattern_recipes_exist() -> None:
    recipe_files = sorted(RECIPES_DIR.glob("*.md"))
    assert (
        recipe_files
    ), "Add at least one pattern recipe under docs/learn/pattern-recipes/."


@pytest.mark.parametrize("recipe_path", sorted(RECIPES_DIR.glob("*.md")))
def test_pattern_recipes_compile(recipe_path: Path) -> None:
    snippets = _extract_pattern_blocks(recipe_path)
    assert snippets, f"Add a ```pattern-cli block to {recipe_path.name}."
    for snippet in snippets:
        translator = PatternTranslator()
        lines = translator.translate(snippet)
        assert len(lines) >= 4
