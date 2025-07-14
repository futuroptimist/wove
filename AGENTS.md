# 🤖 Agents

This repository uses lightweight LLM assistants to automate common chores. Conventions are borrowed from [flywheel](https://github.com/futuroptimist/flywheel).

## Docs Agent
- Spell-checks and checks links for Markdown files on each PR.

## Code Agent
- Suggests formatting fixes if linting fails.

## CAD Agent
- Helps generate new OpenSCAD modules from text prompts.

Run `pre-commit run --all-files` before pushing changes to keep the wheel spinning.
