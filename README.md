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
- A shared unit registry (`wove.units.UNIT_REGISTRY`) that keeps conversions
  between imperial and metric measurements consistent across gauge tools,
  tension analyzers, and motion planners.
- A pattern translation CLI (`python -m wove.pattern_cli`) that turns a simple
  stitch description into G-code-like motion for early crochet experiments. Use
  `--format planner` to export per-command position snapshots, bounds, and (when
  `--machine-profile` is provided) the axis metadata consumed by the
  browser-based planner roadmap. The planner defaults also surface the homing
  guard (`require_home`) and `home_state` captured during translation so
  downstream tools can prompt builders before running motion.
- Yarn tension profile helpers (`wove.tension`) that document tested pull
  forces, trial durations, and feed rates for lace through super bulky yarns.
  Use `find_tension_profile_for_wpi` to map wraps-per-inch measurements to the
  catalog, `find_tension_profile_for_force` to match measured pull force data,
  and the interpolation helpers `estimate_profile_for_wpi`,
  `estimate_profile_for_force`, and `estimate_profile_for_sensor_reading` to
  guide in-between yarn choices and translate hall-effect sensor readings into
  the same feed-rate and variation context. Call
  `estimate_sensor_reading_for_tension` to compute the hall-effect reading a
  servo-driven tensioner should target for a desired pull force.
- LLM helpers described in [AGENTS.md](AGENTS.md).
- Sample Codex prompts in [`docs/prompts/codex/automation.md`](docs/prompts/codex/automation.md).

## Visualize the Product Assembly

Kick the tires on the new Three.js assembly viewer to see how our product lines
fit together as the roadmap grows. The scene currently spotlights `v1c`, the
first crochet robot, and is designed for incremental upgrades as new Codex
tasks expand the experience. Hover the translucent workpiece support bed to see
where swatches land while the gantry executes calibration moves.

```bash
python scripts/serve_viewer.py
# open http://127.0.0.1:8000/index.html in your browser
```

Each contribution should leave the viewer a little better—add new assets,
improve lighting, or enhance interactivity—so that future operators can preview
the entire assembly from a browser. Hover the glowing emergency stop or axis
end stops to see the safety interlocks called out in the v1c roadmap. The
translucent polycarbonate shield now wraps the gantry to mirror the production
enclosure described in the mechanical roadmap—hover the door to read the
maintenance callout. Snap-on belt guards now clip over the CoreXY loops so stray
yarn or tools stay clear while operators inspect motion from above. Click a
product pedestal to spotlight its roadmap milestone and watch the glowing ring
track which cluster is selected. The plaza highlights these milestones today:

Peek through the tinted electronics bay under the work bed to see the SKR Mini
controller stack, cooling fan, and glowing status LED that route motion power up
to the gantry.

- **v1c Crochet Robot** – anchors the mechanical platform showcased at the
  center of the plaza.
- **Tension Lab** – stages the hall-effect calibration rig that feeds future
  servo-driven yarn tensioners.
- **Material Prep Pod** – organizes yarn cones, prep bins, and inspection
  checklists so dye lots and weights are verified before automation runs.
- **Pattern Studio** – previews the planner workspace that visualizes
  `wove.pattern_cli --format planner` exports directly in the browser and
  replays the base chain row hologram for pattern dry runs.
- **v1k Research Rig** – teases the knitting successor with prototype rails,
  a modular carriage sled, and telemetry pods collecting load data for future
  toolheads.

## Choose Your Path

Wove supports two complementary learning tracks. Start where your goals align,
then cross over as projects grow.

- **Hand-Craft Track** – Learn core techniques with
  [knitting basics](docs/knitting-basics.md),
  [crochet primers](docs/crochet-basics.md), and
  [gauge calculators](docs/gauge.md). These guides build the vocabulary and
  measurement skills needed before automating motion.
- **Automation Track** – Explore the mechanical and software stack with the
  [pattern translation CLI](docs/pattern-cli.md),
  [mechanical design roadmap](docs/wove-v1c-design.md), and
  [robotic knitting specification](docs/robotic-knitting-machine.md). Pair these
  resources with the Hand-Craft Track to validate yarn handling, gauge, and
  safety considerations as the gantry evolves.

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
tools. Export the planner-oriented JSON format with `--format planner` and
validate it against [`docs/schema/pattern-cli.schema.json`](docs/schema/pattern-cli.schema.json)
to integrate with browser tooling or downstream automation.
