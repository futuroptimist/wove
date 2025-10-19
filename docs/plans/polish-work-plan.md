# Wove Curriculum Polish Work Plan

## Snapshot of Current Assets
- **Gauge calculators & tension analyzers**: Consolidate current scripts in `wove/` and
  calibration helpers in `scripts/` to map coverage, noting fixtures in `tests/gauge/` and
  `tests/tension/` for regression awareness.
- **`pattern_cli` pipeline**: Inventory command entrypoints in `wove/pattern_cli/` and generated
  artifacts verified by `tests/pattern_cli/` fixtures; confirm data dependencies in
  `tests/fixtures/patterns/` prior to refactors.
- **Developer tooling**: Document CLI drafting utilities under `scripts/` and calibration notebooks
  inside `docs/` to ensure automation hooks tie back to knitting workflows end-to-end.
- **CAD/STL assets**: Review printable loom upgrades stored in `/cad` and `/stl`, logging which
  classroom demos reference each fixture and how they support early robotics experiments.

## Refactor Milestones
1. **Documentation split for clarity**
   - Stage pedagogy-first content in `docs/learn/` (create subfolders for stitch theory, manual
     tooling, and classroom labs). Mirror robotics research in `docs/robotics/` with actuator tuning
     notes and motion-planning experiments.
   - Update Sphinx entrypoints: adjust `docs/index.md` and `docs/conf.py` to surface a "Learn vs.
     Robotics" choice; extend existing toctrees so navigation reflects the split.
   - Migration checklist: move assets referenced by `docs/pattern-cli.md`, `docs/robotic-knitting-machine.md`,
     and `docs/testing.md` into the appropriate track, preserving relative links.
2. **Stabilize the `pattern_cli` DSL**
   - Extract argument parsing from `wove/pattern_cli/__main__.py` into a reusable module
     (`wove/pattern_cli/options.py`) while freezing the public command set.
   - Author a JSON Schema in `docs/schema/pattern-cli.schema.json` describing primitives, units, and
     composition rules; add sample inputs under `tests/fixtures/patterns/` representing hand-written
     and auto-generated cases.
   - Leverage the `scripts/pattern_visualize.py` visualization harness to render stitch charts and
     motion timelines from fixtures, exporting static assets to `docs/_static/pattern_previews/` for
     educator review.
3. **Consolidate unit conversion utilities**
   - Move scattered conversion helpers into `wove/units/__init__.py`, expose a canonical
     `UnitRegistry`, and define APIs consumed by gauge calculators, tension analyzers, and motion
     planners.
   - Cover the registry with Hypothesis-based tests in `tests/units/test_registry.py` asserting
     round-trip accuracy across imperial, metric, and machine-native systems.
   - Replace inline conversions inside `wove/pattern_cli/`, `wove/gauge/`, and CAD scripts in
     `scripts/` to eliminate duplicated constants and align tooling.

## Docs & UX Enhancements
- Draft recipe-style guides in `docs/learn/pattern-recipes/` pairing YAML/JSON snippets with rendered
  previews from `docs/_static/pattern_previews/`; ensure samples compile via `pattern_cli` so learners
  see outcomes pre-knit. _Initial recipe available at
  `docs/learn/pattern-recipes/base-chain-row.md`, including planner JSON excerpt and links to the
  existing SVG previews._
- Expand the root `README.md` (and `docs/index.md`) with a "Choose Your Path" section contrasting the
  Hand-Craft and Automation tracks, referencing prerequisites housed in `docs/learn/` and
  `docs/robotics/`.
- Add cross-links within each track pointing to material science primers, sensor calibration steps,
  and recommended next modules to smooth transitions between manual and robotic studies.

## Testing Roadmap
- Maintain golden-motion tests in `tests/pattern_cli/test_golden_outputs.py`
  that validate motion plans emitted from curated fixtures. The focused suite
  runs via `pytest -k pattern_cli` in CI and guards the planner, JSON, and
  G-code outputs from accidental regressions.
- Extend gauge and tension acceptance coverage in `tests/gauge/test_units.py` and
  `tests/tension/test_units.py`, consuming the centralized `UnitRegistry` to verify imperial, metric,
  and SI-derived unit parity.
- Integrate the visualization harness into CI by adding a non-blocking artifact step in
  `.github/workflows/ci.yml` that publishes rendered previews while allowing educators to consume the
  latest assets without blocking merges.

## Pedagogy-First Robotics Onboarding
- Pair each robotics tutorial in `docs/robotics/` with an instructional prerequisite in
  `docs/learn/`, linking hand techniques, physics concepts, and manual lab work before automation.
- Provide facilitator kits in `docs/learn/facilitator-resources/` that include lab checklists, exit
  tickets, and reflection prompts; ensure templates reference printable mounts in `/cad` and low-cost
  actuator setups in `/stl`.
- Outline a staged robotics starter path: begin with virtual simulations using the visualization
  harness and fixtures in `tests/fixtures/patterns/`, progress to low-cost actuator assemblies from
  `/cad`, and culminate in automated runs once learners clear formative assessments.

## Sequencing Guidance
1. Execute the documentation split and navigation updates to clarify learner pathways before touching
   CLI or unit systems.
2. In parallel, scaffold the `UnitRegistry` since downstream refactors depend on stable conversions;
   gate migration of gauge and tension tools on passing Hypothesis tests.
3. Once documentation and units are stable, freeze the `pattern_cli` surface, publish the schema, and
   wire up golden tests alongside the visualization harness.
4. Close with pedagogy artifacts (recipe guides, facilitator kits, onboarding path) so they reflect
   the finalized tooling and navigation, ensuring educators can act on the updated workflows.
