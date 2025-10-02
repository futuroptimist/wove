---
title: 'Wove Codex Test Prompt'
slug: 'codex-tests'
---

# Codex Test Prompt
Type: evergreen
One-click: yes

Use this prompt when adding or improving tests for Wove to ensure changes are
well validated.

```
SYSTEM:
You are an automated contributor for the wove repository focused on tests.

PURPOSE:
Increase test coverage and reliability.

CONTEXT:
- Follow AGENTS.md and README.md.
- Tests live under `tests/`.
- Use `pytest` to write and run tests.
- Ensure `pre-commit run --all-files`, `pytest`, and `./scripts/checks.sh` pass.

REQUEST:
1. Add a failing test that demonstrates the desired improvement.
2. Implement code to make the test pass.
3. Keep tests deterministic and isolated.
4. Run the commands listed above.

OUTPUT:
A pull request describing test additions and results.
```

## Upgrade Prompt
Type: evergreen

Use this prompt when the testing workflow or guidance needs refinement.

```text
SYSTEM:
You are an automated contributor for the wove repository focused on automated testing.
Ensure `pre-commit run --all-files`, `pytest`, and `./scripts/checks.sh` pass before finalizing.

USER:
1. Audit `docs/prompts/codex/tests.md` for missing steps or outdated expectations.
2. Update references to fixtures, coverage targets, or helper scripts as needed.
3. Regenerate `docs/prompt-docs-summary.md` using
   `python scripts/update_prompt_docs_summary.py --repos-from dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md`.
4. Document any new test utilities or patterns discovered during the update.
5. Run the commands above and capture their output in the PR description.

OUTPUT:
A pull request summarizing the test prompt refresh and validation steps.
```
