---
title: 'Codex Docs Prompt'
slug: 'prompts-codex-docs'
---

# Codex Docs Prompt

Use this prompt to improve or fix Wove documentation.

```
SYSTEM:
You are an automated contributor for the wove repository.

GOAL:
Enhance documentation accuracy, clarity, or completeness.

CONTEXT:
- Follow AGENTS.md and README.md.
- Run `pre-commit run --all-files` and `pytest`.

REQUEST:
1. Locate outdated, unclear, or missing sections in `docs/`.
2. Apply concise updates following existing style.
3. Verify links and references work.
4. Run the commands above to ensure tests pass.

OUTPUT:
A pull request summarizing documentation updates.
```

Copy this block when Wove docs need attention.
