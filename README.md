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
where swatches land while the gantry executes calibration moves. Use the ←/→
arrow keys to cycle through roadmap milestones without leaving the keyboard.

```bash
python scripts/serve_viewer.py
# open http://127.0.0.1:8000/index.html in your browser
```

Each contribution should leave the viewer a little better—add new assets,
improve lighting, or enhance interactivity—so that future operators can preview
the entire assembly from a browser. Hover the glowing emergency stop or the axis
end stops with their pulsing halos to see the safety interlocks called out in
the v1c roadmap. Each limit switch now emits a soft indicator light so the
homing path is easy to trace from above. The translucent polycarbonate shield
now wraps the gantry to mirror the production
enclosure described in the mechanical roadmap—hover the door to read the
maintenance callout. Snap-on belt guards now clip over the CoreXY loops so stray
yarn or tools stay clear while operators inspect motion from above. Click a
product pedestal to spotlight its roadmap milestone, watch the glowing ring
pulse as it tracks which cluster is selected, and let the camera glide to frame
the scene. A teal sweep now orbits the
selected pedestal so the active milestone stays obvious from the plaza
overview. The plaza highlights these milestones today:

Mint-highlighted floor markings now extend through the open doorway with alternating, pulsing
footprints so operators can practice each step without clipping the gantry or tension hardware.
Floating step badges bob above each marker and cant toward the doorway so crews can rehearse the
left/right cadence before approaching the enclosure.

Pulsing magnetic anchor pucks now mark the removable workpiece bed so crews can
practice swapping swatch plates into position before the gantry starts tracing
calibration paths. A sequential glow now sweeps across the anchors to rehearse
the recommended swap order at a glance.

Peek through the tinted electronics bay under the work bed to see the SKR Mini
controller stack, cooling fan, and glowing status LED that route motion power up
to the gantry.

Printed cable chains now snake from the electronics bay toward the hook carriage
with sequential pulses so contributors can trace how wiring and PTFE guides ride
the gantry. Hover the glowing links to rehearse how harnesses cross the work
area without snagging tooling or yarn during maintenance walkthroughs.

Amber pulses now race through the translucent PTFE tube so you can watch yarn
flow from the spool, past the hall-effect sensor, and into the crochet hook as
the planner preview runs. Three glowing beads now chase along the same guide,
staggering their pace whenever the preview feeds yarn so the flow direction
stays obvious at a glance—even in still frames.

The source spool now spins in sync with yarn feed events so the hologram shows
fiber unwinding from the supply while the PTFE tube glows. When extrusion
pauses, the reel now coasts to a stop so idle previews keep the spool parked.
A pair of cooling fans—the electronics bay exhaust and the hook-carriage
mount—idle with a gentle spin and ramp up whenever the yarn feed engages, so the
viewer keeps thermal cues in step with spool choreography.
A shimmering Z-axis lift now hugs the hook carriage: the T8 leadscrew pulses
beside the gantry while the anti-backlash nut and printed flexures glow to show
how the carriage keeps vertical motion tight.

Color-coded axis beacons now glow beside the gantry so visitors can read the
positive X, Y, and Z directions at a glance. Their hovering arrows match the
planner coordinate system, making it easier to align CLI exports with the 3D
scene while touring the plaza.

A glowing thermistor channel now traces the reserved wiring route for the
future heated bed accessory so teams can plan sensor hookups before the upgrade
lands.

The overlay now includes a Pattern Studio preview panel that cycles through the
current `wove.pattern_cli --format planner` comment while a progress bar tracks
the hologram run. Operators can cross-reference the displayed step with the
planner animation without leaving the scene. The viewer pulls its sample from
`viewer/assets/base_chain_row.planner.json`, the same planner export produced by
the CLI fixtures, so the hologram stays aligned with the documented base chain
row recipe. Automated tests compare that asset against `PatternTranslator`
output to flag drift whenever the CLI evolves.

The overlay's Planner Defaults list calls out the safe Z height, fabric plane,
row height, and feed-rate defaults from the planner export so operators can
validate the viewer preview against CLI settings before rehearsing motion. It
also repeats the `require_home` guard and recorded `home_state` so the safety
expectations stay in view alongside the feed-rate metadata.

A Yarn Flow monitor in the overlay mirrors the hologram's yarn feed state,
calling out when the planner is actively pulling fiber and when the spool is
parked between feed events. The status flips in sync with the glowing PTFE
guide and now reports how much yarn has been fed versus the planned total,
along with the remaining feed pulses, so teams can confirm software, animation,
and spool choreography agree before running hardware. The overlay now lists the
upcoming feed pulse steps so operators can anticipate exactly when the next
yarn draws will occur during the planner loop, and it streams the live
`X`, `Y`, `Z`, and yarn-feed coordinates alongside those cues so crews can log
the precise motion snapshot in sync with the animation. Countdown timers now
quantify the seconds until the next yarn feed and highlight the following
events, translating the planner preview into a realtime pacing guide.

A translucent planner bounds frame now wraps the hologram while the overlay
lists the X/Y/Z/E limits emitted by the planner payload so teams can confirm the
motion envelope before committing the sequence to hardware.

Live coordinates now accompany each planner step so technicians can confirm the
active `X`, `Y`, `Z`, and yarn-feed positions directly from the overlay while
the hologram advances.

The overlay also surfaces a **Machine Profile** panel that lists axis
microstepping, steps-per-millimeter, and travel ranges whenever planner exports
embed machine metadata via `--machine-profile`. Verify the browser preview is
aligned with the configured gantry before rehearsing motion sequences.

A **Planner Metadata** panel now lists the export's schema version, declared
units, and total planner steps so contributors can confirm the viewer is
rendering the expected payload before rehearsing motion.

The new **Homing Guard** panel highlights whether the planner required a homed
machine and echoes the captured `home_state`. Green and amber tones flag when a
preview came from a verified homing cycle or needs attention so operators can
double-check the gantry status before executing the motion sequence. It now
echoes the live planner coordinates alongside those status lights so the safety
overlay tracks the same `X`, `Y`, `Z`, and yarn-feed snapshot as the Pattern
Studio panel.

- **v1c Crochet Robot** – anchors the mechanical platform showcased at the
  center of the plaza.
- **Tension Lab** – stages the hall-effect calibration rig that feeds future
  servo-driven yarn tensioners, complete with a prototype micro-servo adjuster
  pulsing on the bench. Watch the horn pivot and the status orb brighten
  whenever the planner preview feeds yarn so teams can rehearse programmable
  pulls.
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
  - Explore the
    [Learning resources](docs/learning-resources.md) primer for fiber science
    refreshers and curated study material.
  - Pair the stitch walkthroughs with the
    [crochet tools guide](docs/crochet-tools.md) to connect hook, yarn, and
    tension decisions with classroom labs.
- **Automation Track** – Explore the mechanical and software stack with the
  [pattern translation CLI](docs/pattern-cli.md),
  [mechanical design roadmap](docs/wove-v1c-design.md), and
  [robotic knitting specification](docs/robotic-knitting-machine.md). Pair these
  resources with the Hand-Craft Track to validate yarn handling, gauge, and
  safety considerations as the gantry evolves.
  - Review the
    [Yarn Handling benchmarks](docs/wove-v1c-design.md#yarn-handling) for hall
    sensor calibration guidance and tension profiles.
  - Run the
    [base chain row recipe](docs/learn/pattern-recipes/base-chain-row.md) to tie
    planner exports, viewer previews, and automation labs together.

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
