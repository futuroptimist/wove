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
                "solo/repo",  # repo with implicit path
            )
        ),
        encoding="utf-8",
    )

    sources = ps.load_repo_sources(repo_file)

    assert sources[0][0] == "futuroptimist/wove"
    assert sources[0][1] == Path(".")
    assert sources[1] == ("example/repo", tmp_path)
    assert sources[2] == ("solo/repo", Path("solo/repo"))


@pytest.fixture()
def prompt_docs() -> list[ps.PromptDoc]:
    return ps.discover_prompt_docs("futuroptimist/wove", Path("."))


def test_discover_prompt_docs_extracts_metadata(
    prompt_docs: list[ps.PromptDoc],
) -> None:
    target_path = "prompts/codex/automation.md"
    automation = None
    for doc in prompt_docs:
        if doc.rel_path == target_path:
            automation = doc
            break

    assert automation is not None

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

    link_target = "prompts/codex/automation.md"
    expected_link = f"| [{link_target}]({link_target}) |"
    assert expected_link in summary
    assert "| File | Title | Type | One-click | Summary |" in summary


def test_prompt_doc_rel_path_strips_docs_directory() -> None:
    doc = ps.PromptDoc(
        repo="repo",
        path=Path("docs") / "section" / "file.md",
        title="Title",
        doc_type=None,
        one_click=None,
        description=None,
    )

    assert doc.rel_path == "section/file.md"


def test_prompt_doc_rel_path_falls_back_without_docs_prefix() -> None:
    doc = ps.PromptDoc(
        repo="repo",
        path=Path("README.md"),
        title="Title",
        doc_type=None,
        one_click=None,
        description=None,
    )

    assert doc.rel_path == "README.md"


def test_escape_pipes_and_render_summary_for_empty_docs(
    tmp_path: Path,
) -> None:
    escaped = ps.escape_pipes("value | with pipe")
    assert escaped == r"value \| with pipe"

    empty_summary = ps.render_summary([])
    assert "No prompt docs were discovered." in empty_summary


def test_parse_helpers_extract_expected_metadata() -> None:
    lines = (
        "---",
        "title: 'Example'",
        "---",
        "# Heading",
        "Type: evergreen",
        "One-click: yes",
        "This is the description.",
    )

    front_matter, index = ps._parse_front_matter(lines)
    assert front_matter == {"title": "Example"}
    assert index == 3

    heading = ps._first_heading(lines[index:])
    assert heading == "Heading"

    doc_type, one_click, description = ps._extract_metadata(lines[index:])
    assert doc_type == "evergreen"
    assert one_click == "yes"
    assert description == "This is the description."


def test_generate_and_write_summary(tmp_path: Path) -> None:
    repo_file = tmp_path / "repos.txt"
    repo_file.write_text("futuroptimist/wove .\n", encoding="utf-8")

    summary = ps.generate_summary(repo_file)
    output = tmp_path / "out.md"
    ps.write_summary(output, summary)

    content = output.read_text(encoding="utf-8")
    assert content.startswith("# Prompt Docs Summary")


def test_strip_quotes_handles_various_wrappers() -> None:
    assert ps._strip_quotes("'quoted'") == "quoted"
    assert ps._strip_quotes('"double"') == "double"
    assert ps._strip_quotes("plain") == "plain"


def test_parse_helpers_gracefully_handle_missing_headers() -> None:
    lines = ("Not front matter", "Type: evergreen")

    front_matter, index = ps._parse_front_matter(lines)
    assert front_matter == {}
    assert index == 0

    metadata_lines = (
        "```",
        "Type: ignored",
        "```",
        "One-click: yes",
        "Description line",
    )
    doc_type, one_click, description = ps._extract_metadata(metadata_lines)
    assert doc_type is None
    assert one_click == "yes"
    assert description == "Description line"
