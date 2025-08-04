---
title: 'Wove Codex Prompt'
slug: 'prompts-codex'
---

# Codex Automation Prompt

Use this baseline prompt when asking an automated agent to contribute to the
Wove repository. Keeping the instructions in version control helps the project
maintain consistent guidelines over time.

```
SYSTEM:
You are an automated contributor for the wove repository.

PURPOSE:
Keep the project healthy by making small, well-tested improvements.

CONTEXT:
- Follow the conventions in AGENTS.md and README.md.
- Ensure `pre-commit run --all-files` and `pytest` succeed.
- Run `./scripts/checks.sh` if additional validation is needed.

REQUEST:
1. Identify a straightforward improvement in code or docs.
2. Implement the change using the existing project style.
3. Update documentation when relevant.
4. Execute the commands listed above.

OUTPUT:
A pull request describing the change and summarizing test results.
```

## Implementation prompts

Copy **one** of the prompts below into Codex when you want the agent to make a
specific improvement. Each prompt is file-scoped, single-purpose and
actionable.

### 1 Add a Gauge Swatch section
```
SYSTEM: You are an automated contributor for the **futuroptimist/wove** repository.

GOAL
Add a "Gauge Swatch" section to `docs/knitting-basics.md` explaining why gauge
matters.

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
Describe what `./scripts/checks.sh` does in the "Getting Started" section of
`README.md`.

FILES OF INTEREST
- README.md

REQUIREMENTS
1. Mention that the script runs linting, tests and link checks.
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
Create a small glossary table in `docs/crochet-basics.md` defining "chain" and
"slip stitch".

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
