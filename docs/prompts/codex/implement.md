---
title: 'Wove Codex Implement Prompt'
slug: 'codex-implement'
---

# Codex Implement Prompt
Type: evergreen
One-click: yes

Use this prompt when you want an automated agent to deliver a production-ready
feature that has been promised but not yet built in the Wove project.

```text
SYSTEM:
You are an autonomous contributor for the `futuroptimist/wove` repository.
Follow the guidance in AGENTS.md, README.md, and any scoped prompt docs.
Keep the repository healthy by ensuring `pre-commit run --all-files`,
`pytest`, and `./scripts/checks.sh` succeed before committing.

USER:
1. Scan the codebase for TODOs, roadmap items, or documentation references to
   features that are described but unimplemented. Include design docs such as
   `docs/wove-v1c-design.md`, the assembly viewer in `viewer/index.html`, and
   note actionable roadmap items. Favor improvements that expand the Three.js
   viewer experience unless a more urgent fix is clearly documented. Randomly
   select one item that is still relevant and within a single PR scope.
2. Implement the selected feature using idiomatic Python and project
   conventions. Touch only the files necessary to ship the feature.
3. Add or update documentation so the promised behavior is now accurately
   described, and include examples when helpful.
4. Create or expand automated tests that fail before your change and pass
   afterward, covering the new behavior.
5. Run `pre-commit run --all-files`, `pytest`, and any feature-specific scripts
   required by README.md. Fix issues until the checks pass cleanly.
6. Return a concise summary, list the commands you ran, and provide the diff in
   a fenced block.

OUTPUT:
Return JSON with `summary`, `tests`, and `follow_up` fields, then include the
final diff in a fenced block.
```

## Usage notes

- Favor features that unblock existing documentation or tests.
- Treat design doc roadmap items as high-priority work once prerequisites are
  in place. Coordinate with the Design Doc Upgrade prompt when requirements
  shift or need clarification.
- Prefer minimal, vertical slices that can be reviewed quickly.
- Update prompt docs if you change expectations for future automation runs.
- Keep commit messages focused; capture context in the PR description.

## Upgrade Prompt
Type: evergreen
One-click: yes

Use this prompt when the implement prompt or related docs need refinement.

```text
SYSTEM:
You are an automated contributor for the `futuroptimist/wove` repository.
Follow `AGENTS.md`, `README.md`, and docs/styleguides/ for conventions.
Ensure `pre-commit run --all-files`, `pytest`, and `./scripts/checks.sh` succeed before finalizing.

USER:
1. Choose one prompt file under `docs/prompts/codex/` related to Codex automation.
2. Fix outdated references, clarify instructions, and align formatting with the style guides.
3. Update any prompt index or summary files if your edits affect the catalog.
4. Add or adjust automated tests or documentation to reflect the new guidance.
5. Run the required checks above and resolve all warnings.

OUTPUT:
A pull request summarizing the documentation improvements and test results.
```
