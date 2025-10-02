# 🧶 wove

[![Lint & Format](https://img.shields.io/github/actions/workflow/status/futuroptimist/wove/.github/workflows/01-lint-format.yml?label=lint%20%26%20format)](https://github.com/futuroptimist/wove/actions/workflows/01-lint-format.yml)
[![Tests](https://img.shields.io/github/actions/workflow/status/futuroptimist/wove/.github/workflows/02-tests.yml?label=tests)](https://github.com/futuroptimist/wove/actions/workflows/02-tests.yml)
[![codecov](https://codecov.io/gh/futuroptimist/wove/branch/main/graph/badge.svg)](https://codecov.io/gh/futuroptimist/wove)
[![docs][docs-badge]][docs-workflow]
[![License](https://img.shields.io/github/license/futuroptimist/wove)](LICENSE)

**wove** aims to provide an open-source toolkit for learning to knit and crochet while
building toward a robotic knitting machine. Documentation in `docs/` covers hand
knitting and crochet basics, while the `cad/` directory contains OpenSCAD files for
printable hardware components.

Key features include:

- CI workflows for linting, testing, and docs previews.
- Pre-commit hooks with spell checking via `pyspelling`.
- Simple OpenSCAD scripts and STLs for hardware.
- Utility functions such as stitch and row gauge calculators for inches,
  centimeters, yards, and meters (for example, `stitches_per_yard` and
  `rows_per_meter`), width estimators from stitch counts across those units, and
  simple unit conversion helpers.
  See [docs/gauge.md](docs/gauge.md) for examples.
- LLM helpers described in [AGENTS.md](AGENTS.md).
- Sample Codex prompts in [`docs/prompts-codex.md`](docs/prompts-codex.md).

## Getting Started

This project targets Python 3.12. Ensure your virtual environment uses Python 3.12.

```bash
# clone your fork
git clone git@github.com:YOURNAME/wove.git
cd wove

# personalize badges and docs
./scripts/setup.sh YOURNAME wove

# create virtualenv and install deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# install pre-commit hooks
pre-commit install

# run checks
pre-commit run --all-files
pytest

# for documentation changes
pyspelling -c .spellcheck.yaml  # requires 'aspell'
linkchecker README.md docs/
```

The [`scripts/checks.sh`](scripts/checks.sh) script runs linting, tests, and link checks:

- linting
- tests
- link checks

See [AGENTS.md](AGENTS.md) for details on LLM helpers that keep this repo tidy. Contributions are welcome—see [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md). For AI helper context see [llms.txt](llms.txt).

[docs-badge]: https://github.com/futuroptimist/wove/actions/workflows/docs.yml/badge.svg
[docs-workflow]: https://github.com/futuroptimist/wove/actions/workflows/docs.yml
