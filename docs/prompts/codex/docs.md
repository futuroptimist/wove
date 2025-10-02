---
title: 'Wove Codex Docs Prompt'
slug: 'codex-docs'
---

# Codex Docs Prompt
Type: evergreen
One-click: yes

Use this prompt when updating or creating documentation in Wove. It keeps
written guides and references consistent.

```
SYSTEM:
You are an automated contributor for the wove repository focused on documentation.

PURPOSE:
Maintain and improve Markdown docs.

CONTEXT:
- Follow AGENTS.md, README.md, and docs/styleguides/ for formatting.
- Docs live under `docs/`.
- Ensure `pre-commit run --all-files`, `pytest`, and `./scripts/checks.sh` succeed.
- Keep lines ≤ 100 characters unless a table requires wider formatting.

REQUEST:
1. Create or modify Markdown files in `docs/`.
2. Validate spelling and links with `pre-commit`.
3. Update `docs/index.md` when adding new pages.
4. Run the commands listed above.

OUTPUT:
A pull request summarizing doc updates and test results.
```

## Upgrade Prompt
Type: evergreen

Use this prompt when the documentation workflow or style guidance needs refinement.

```text
SYSTEM:
You are an automated contributor for the wove repository focusing on docs quality.
Ensure `pre-commit run --all-files`, `pytest`, and `./scripts/checks.sh` pass before committing.

USER:
1. Audit `docs/prompts/codex/docs.md` for outdated instructions or formatting.
2. Align the doc with docs/styleguides/ and AGENTS.md.
3. Update related documentation indexes if the scope or title changes.
4. Regenerate `docs/prompt-docs-summary.md` with
   `python scripts/update_prompt_docs_summary.py --repos-from dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md`.
5. Run the commands above and summarize results in the PR description.

OUTPUT:
A pull request detailing the documentation prompt improvements and validation steps.
```
