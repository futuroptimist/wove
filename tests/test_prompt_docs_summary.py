from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

PHRASE = "Use this prompt when verifying tests for automation scripts."


def load_module():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "update_prompt_docs_summary.py"
    )
    spec = importlib.util.spec_from_file_location(
        "update_prompt_docs_summary", script_path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def test_collect_and_render_summary(tmp_path):
    module = load_module()
    repo_root = tmp_path / "sample"
    prompt_dir = repo_root / "docs" / "prompts"
    prompt_dir.mkdir(parents=True)

    prompt_content = """---
title: 'Sample Prompt'
slug: 'sample'
---

# Sample Prompt
Type: evergreen
One-click: yes

Use this prompt when verifying tests for automation scripts.
"""
    (prompt_dir / "sample.md").write_text(prompt_content, encoding="utf-8")

    docs = module.collect_prompt_docs([repo_root])
    assert len(docs) == 1
    doc = docs[0]
    assert doc.title == "Sample Prompt"
    assert doc.type_value == "evergreen"
    expected_phrase = PHRASE
    assert doc.description == expected_phrase
    assert doc.relative_path.as_posix() == "docs/prompts/sample.md"

    summary = module.render_summary(docs)
    assert "## sample" in summary.lower()
    assert "Sample Prompt" in summary
    assert "`docs/prompts/sample.md`" in summary
    assert expected_phrase in summary

    repos_file = tmp_path / "repos.txt"
    repos_file.write_text(str(repo_root.resolve()), encoding="utf-8")
    out_path = tmp_path / "summary.md"

    module.main(
        [
            "--repos-from",
            str(repos_file),
            "--out",
            str(out_path),
        ]
    )

    assert out_path.read_text(encoding="utf-8") == summary
