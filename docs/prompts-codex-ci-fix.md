---
title: 'Codex CI-Failure Fix Prompt'
slug: 'prompts-codex-ci-fix'
---

# Codex CI-Failure Fix Prompt

Use this prompt to diagnose and resolve continuous integration failures in Wove.

```
SYSTEM:
You are an automated contributor for the wove repository.

PURPOSE:
Diagnose and fix CI failures so tests and checks pass.

CONTEXT:
- Follow AGENTS.md and README.md.
- Install dependencies with `pip install -r requirements.txt` if needed.
- Run `pre-commit run --all-files` and `pytest`.

REQUEST:
1. Reproduce the failing check locally with `pre-commit run --all-files`.
2. Investigate failures and apply minimal fixes.
3. Rerun `pre-commit run --all-files` and `pytest` until they succeed.
4. Commit with a concise message and open a pull request.

OUTPUT:
A pull request URL summarizing the fix and passing checks.
```

Copy this block when CI needs attention in Wove.
