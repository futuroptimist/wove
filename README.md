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
- A pattern translation CLI (`python -m wove.pattern_cli`) that turns a simple
  stitch description into G-code-like motion for early crochet experiments.
- Yarn tension profile helpers (`wove.tension`) that document tested pull
  forces, trial durations, and feed rates for lace through super bulky yarns.
  Use `find_tension_profile_for_wpi` to map wraps-per-inch measurements to the
  catalog, `find_tension_profile_for_force` to match measured pull force data,
  and the interpolation helpers `estimate_profile_for_wpi`,
  `estimate_profile_for_force`, and `estimate_profile_for_sensor_reading` to
  guide in-between yarn choices and translate hall-effect sensor readings into
  the same feed-rate and variation context.
- LLM helpers described in [AGENTS.md](AGENTS.md).
- Sample Codex prompts in [`docs/prompts/codex/automation.md`](docs/prompts/codex/automation.md).

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
# Pattern translation CLI

Use the companion CLI to convert a lightweight stitch description into
G-code-like motion suitable for early gantry experiments. Feed the CLI either a
file path or inline text:

```bash
python -m wove.pattern_cli pattern.txt
# or
python -m wove.pattern_cli --text "CHAIN 2\nSINGLE 1" --format json
```

Trace simple SVG sketches by passing a polyline or polygon. Adjust scale and offsets to fit your
workspace:

```bash
python -m wove.pattern_cli --svg sketch.svg --svg-scale 2 --svg-offset-x 10 --svg-offset-y 5
```

The DSL accepts commands such as `SLIP <count>`, `CHAIN <count>`, `SINGLE <count>`, `DOUBLE
<count>`, `MOVE <x> <y>`, `TURN [height]`, and `PAUSE <seconds>`. The output is
G-code-inspired: each stitch generates plunge, yarn-feed, raise, and travel
moves with comments so you can import the sequence into firmware or simulation
tools.
