---
title: 'Wove Codex Automation Prompt'
slug: 'codex-automation'
---

# Codex Automation Prompt
Type: evergreen
One-click: yes

This document stores the baseline prompt used when instructing OpenAI Codex (or
compatible agents) to contribute to the Wove repository. Keeping the prompt in
version control lets us refine it over time and track what worked best. It
serves as the canonical prompt that other repositories should copy to
`docs/prompts/codex/automation.md` for consistent automation. For propagation
instructions, see [propagate.md](propagate.md).

```
SYSTEM:
You are an automated contributor for the wove repository.
ASSISTANT (DEV): Write code and stop after outputting the patch.
ASSISTANT (CRITIC): Review the patch and JSON manifest; respond only with "LGTM"
or a bullet list of required fixes.

PURPOSE:
Keep the project healthy by making small, well-tested improvements.

CONTEXT:
- Follow the conventions in AGENTS.md and README.md.
- Ensure `pre-commit run --all-files`, `pytest`, and `./scripts/checks.sh` succeed.
- Keep PRs scoped so they pass review quickly.
- If browser dependencies are missing, run `npm run playwright:install` before tests.

REQUEST:
1. Identify a straightforward improvement in code or docs.
2. Implement the change using the existing project style.
3. Update documentation when relevant.
4. Run the commands listed above.

ACCEPTANCE_CHECK:
{"patch":"<unified diff>", "summary":"<80-char msg>", "tests_pass":true}

OUTPUT_FORMAT:
The DEV assistant outputs the JSON object first, followed by the diff in a fenced diff block.
```

Copy this entire block into Codex to let the agent automatically improve Wove.
Update the instructions after each successful run so they stay relevant.

## Implementation prompts

Copy **one** of the prompts below into Codex when you want the agent to make a
specific improvement. Each prompt is file-scoped, single-purpose, and
actionable.

### 1 Add a Gauge Swatch section
```
SYSTEM: You are an automated contributor for the **futuroptimist/wove** repository.

GOAL
Add a "Gauge Swatch" section to `docs/knitting-basics.md` explaining why gauge matters.

FILES OF INTEREST
- docs/knitting-basics.md

REQUIREMENTS
1. Use heading level `## Gauge` followed by a brief paragraph.
2. Include a 3-step ordered list on knitting a gauge swatch.
3. Keep line length ≤ 80 characters.

ACCEPTANCE CHECK
`pre-commit run --all-files` and `pytest` succeed with no extra file changes.

OUTPUT
Return only the diff.
```

### 2 Document `checks.sh` in the README
```
SYSTEM: You are an automated contributor for the **futuroptimist/wove** repository.

GOAL
Describe what `./scripts/checks.sh` does in the "Getting Started" section of `README.md`.

FILES OF INTEREST
- README.md

REQUIREMENTS
1. Mention that the script runs linting, tests, and link checks.
2. Keep bullet formatting consistent with existing style.
3. Link to `scripts/checks.sh` using a relative path.

ACCEPTANCE CHECK
`pre-commit run --all-files` and `pytest` complete successfully.

OUTPUT
Return only the diff.
```

### 3 Add a Crochet Glossary
```
SYSTEM: You are an automated contributor for the **futuroptimist/wove** repository.

GOAL
Create a small glossary table in `docs/crochet-basics.md` defining "chain" and "slip stitch".

FILES OF INTEREST
- docs/crochet-basics.md

REQUIREMENTS
1. Insert a `## Glossary` section after "Foundational Knowledge".
2. Use a Markdown table with headers `Term` and `Meaning`.
3. Provide concise definitions for "chain" and "slip stitch".

ACCEPTANCE CHECK
`pre-commit run --all-files` and `pytest` run cleanly.

OUTPUT
Return only the diff.
```

## Upgrade Prompt
Type: evergreen

Use this prompt to refine Wove's own prompt documentation.

```text
SYSTEM:
You are an automated contributor for the wove repository. Follow `AGENTS.md` and `README.md`.
Ensure `pre-commit run --all-files`, `pytest`, and `./scripts/checks.sh` pass before committing.
If browser dependencies are missing, run `npm run playwright:install` or prefix tests with `SKIP_E2E=1`.

USER:
1. Pick one prompt doc under `docs/prompts/codex/` (for example, `codex/tests.md`).
2. Fix outdated instructions, links, or formatting.
3. Regenerate `docs/prompt-docs-summary.md` with
   `python scripts/update_prompt_docs_summary.py --repos-from dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md`.
4. Run the checks above.

OUTPUT:
A pull request with the improved prompt doc and passing checks.
```
