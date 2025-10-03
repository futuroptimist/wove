from __future__ import annotations

from pathlib import Path

import pytest

from wove import prompt_summary as ps


def test_load_repo_sources_parses_pairs(tmp_path: Path) -> None:
    repo_file = tmp_path / "repos.txt"
    repo_file.write_text(
        "\n".join(
            (
                "# comment",  # ignored
                "futuroptimist/wove .",  # repo with explicit path
                f"example/repo {tmp_path}",  # absolute path allowed
            )
        ),
        encoding="utf-8",
    )

    sources = ps.load_repo_sources(repo_file)

    assert sources[0][0] == "futuroptimist/wove"
    assert sources[0][1] == Path(".")
    assert sources[1] == ("example/repo", tmp_path)


@pytest.fixture()
def prompt_docs() -> list[ps.PromptDoc]:
    return ps.discover_prompt_docs("futuroptimist/wove", Path("."))


def test_discover_prompt_docs_extracts_metadata(
    prompt_docs: list[ps.PromptDoc],
) -> None:
    target_path = "docs/prompts/codex/automation.md"
    automation = next(
        doc
        for doc in prompt_docs
        if doc.rel_path == target_path
    )

    assert automation.title == "Wove Codex Automation Prompt"
    assert automation.doc_type == "evergreen"
    assert automation.one_click == "yes"
    assert automation.description.startswith(
        "This document stores the baseline prompt used when instructing"
    )


def test_render_summary_contains_expected_row(
    prompt_docs: list[ps.PromptDoc],
) -> None:
    summary = ps.render_summary(prompt_docs)

    expected_link = (
        "| [docs/prompts/codex/automation.md]"
        "(docs/prompts/codex/automation.md) |"
    )
    assert expected_link in summary
    assert "| File | Title | Type | One-click | Summary |" in summary
