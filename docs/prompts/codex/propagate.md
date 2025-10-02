---
title: 'Wove Codex Prompt Propagation Guide'
slug: 'codex-propagate'
---

# Codex Prompt Propagation Guide
Type: evergreen
One-click: no

Use this guide when copying Wove's Codex prompt catalog into another repository or
rotating a fresh automation setup. It documents the lightweight checklist for
keeping prompt docs synchronized with downstream projects.

## Before you copy
- Confirm the prompt docs in this repository are up to date. Run
  `python scripts/update_prompt_docs_summary.py --repos-from dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md`
  to rebuild the catalog summary.
- Run `pre-commit run --all-files` and `pytest` so the source of truth is
  healthy before exporting anything.

## Propagation steps
1. Copy the desired prompt(s) from `docs/prompts/codex/` into the target
   repository, preserving front matter and headings.
2. Include `docs/prompts/codex/automation.md` in the destination so future
   automation runs use the canonical instructions.
3. Update the destination repository's README and AGENTS (or equivalent) to link
   back to the canonical prompt catalog in Wove.
4. Open a pull request in the destination repository that references the source
   commit hash from Wove.

## After propagation
- Leave a short note in Wove's change log or team channel pointing to the
  destination PR.
- Schedule a follow-up check to rerun the propagation process whenever the
  prompt docs materially change.
