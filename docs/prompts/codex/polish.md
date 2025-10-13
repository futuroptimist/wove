---
title: 'Wove Codex Polish Plan'
slug: 'codex-polish'
---

Copy the appropriate prompt block below into Codex.

## Primary prompt
```
SYSTEM:
You are an automation planner for the wove repository.

PURPOSE:
Coordinate polish work that keeps the pedagogy-first curriculum strong while onboarding learners
into early-stage robotics.

DELIVERABLES:
- A concise work plan covering snapshot, refactors, docs & UX, testing, and pedagogy-first robotics
  onboarding.
- Clear sequencing notes that help contributors prioritize.
- Explicit references to repository paths, fixtures, and tooling so the plan is directly actionable.

SNAPSHOT:
- Core modules: gauge calculators, tension analyzers, and the `pattern_cli` pipeline that turns
  stitch patterns into repeatable instructions.
- Developer tooling: command line utilities for pattern drafting, calibration scripts, and
  automation hooks that connect the knitting workflow end to end.
- CAD/STL assets: printable loom components and fixture upgrades maintained in `/cad` and `/stl`
  for classroom demonstrations and early robotics experiments.

REFACTORS:
1. Documentation split for clarity
   - Move pedagogy-first material into `docs/learn/` (stitch theory, manual tooling, classroom
     exercises).
   - Relocate robotics prototypes, actuator tuning notes, and motion-planning research into
     `docs/robotics/` so experimental work stays isolated from the core learning path.
   - Update navigation (including `docs/index.md` and Sphinx toctrees) to highlight the "learn vs.
     robotics" choice up front.
2. Stabilize the `pattern_cli` DSL
   - Freeze the command surface, codify argument semantics, and extract the option parser into a
     reusable module.
   - Publish a machine-readable JSON Schema documenting pattern primitives, composition rules, and
     unit expectations; add fixtures spanning hand-authored and generated patterns.
   - Provide a visualization harness that renders pattern fixtures into stitch charts and motion
     timelines so educators can validate lessons without hardware.
3. Consolidate unit conversion utilities
   - Move conversion helpers into `wove/units`, expose a canonical `UnitRegistry`, and define an API
     for gauge, tension, and motion planning.
   - Back the registry with property-based tests (Hypothesis) asserting round-trip conversions across
     imperial, metric, and machine-native unit systems.
   - Replace ad-hoc conversions inside `pattern_cli`, gauge calculators, and CAD scripts with the
     shared utilities to remove duplicated constants.

DOCS & UX:
- Author recipe-oriented pattern guides pairing YAML/JSON snippets with rendered previews (static
  charts or animated GIFs) so students see outcomes before knitting.
- Add a "Choose Your Path" README segment explaining the branching curriculum: Hand-Craft Track
  (manual looms, tactile learning, material science primers) versus Automation Track (sensor
  calibration, G-code generation, robotics integration).
- Cross-link tracks with prerequisites and recommended reading to ease transitions from pedagogy
  lessons into the robotics sandbox.

TESTING:
- Add golden tests that assert `pattern_cli` outputs the expected motion plans for curated pattern
  fixtures, guarding against regressions as the DSL evolves.
- Expand gauge/tension calculator coverage with multi-unit acceptance tests exercising the new
  `wove/units` registry across imperial, metric, and SI-derived machine units.
- Integrate the visualization harness into CI as a non-blocking artifact so rendered previews stay in
  sync with fixtures while keeping educator workflows reliable.

PEDAGOGY-FIRST ROBOTICS ONRAMP:
- Pair each robotics module with an instructional counterpart in `docs/learn/` that teaches the
  underlying physics and hand techniques before automation.
- Provide lightweight lab checklists and formative assessments (exit tickets, reflection prompts) so
  facilitators can gauge comprehension without specialized hardware.
- Offer an early robotics starter path: begin with virtual simulations using the visualization
  harness, progress to low-cost actuators with printable mounts from `/cad`, and culminate in full
  automation once students prove proficiency on the manual track.
```

## Upgrade prompt
```
SYSTEM:
You critique and improve the "Primary prompt" above for the wove repository.

INSTRUCTIONS:
1. Review the existing primary prompt and identify any gaps in clarity, sequencing, or actionable
   detail.
2. Propose concrete edits that preserve intent while increasing usability for Codex agents and human
   operators.
3. Ensure the upgraded prompt maintains the same sections (SNAPSHOT, REFACTORS, DOCS & UX, TESTING,
   PEDAGOGY-FIRST ROBOTICS ONRAMP) and continues to reference the required repository paths and
   fixtures.
4. Return your improvements as a revised prompt text and a short changelog summarizing what you
   adjusted.
```
