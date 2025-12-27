# W1C viewer refactor plan

## Goals
- Reduce monolithic `viewer/index.html` into well-scoped modules for styling, scene logic, data
  adapters, and UI orchestration.
- Preserve current functionality while creating clear seams for iterative improvements during
  future Codex sessions.
- Keep the viewer runnable via `python scripts/serve_viewer.py` without introducing a build step.

## Target file layout
- `viewer/index.html`: minimal shell that wires CSS and the main module entrypoint.
- `viewer/styles/`: visual concerns only (base theme, layout, component-specific styles).
- `viewer/src/` JavaScript modules
  - `main.js`: bootstraps the renderer, loads supporting modules, and owns lifecycle wiring.
  - `scene/`: Three.js scene setup, lighting, camera, controls, and animation loop helpers.
  - `ui/`: overlay panels, status billboards, tooltip interactions, and accessibility affordances.
  - `data/`: parser utilities for planner exports, machine profiles, and derived metadata such as
    bounds comparison.
  - `systems/`: reusable controllers (pulses, glows, timelines) that animate meshes based on data.
  - `assets/`: static JSON samples, geometry configs, and palette constants.
- `tests/viewer/`: add browserless unit tests for pure utilities plus Playwright smoke for critical
  flows when feasible.

## Migration phases
1. **Scaffolding (current step)**
   - Move inline CSS to `viewer/styles/viewer.css`.
   - Move inline JS to `viewer/src/main.js` and import via `<script type="module" src=...>`.
   - Document the refactor plan to guide future sessions.
2. **Module seams**
   - Extract DOM queries and overlay updates into `ui/panels.js` and `ui/status.js`.
   - Split planner parsing and bounds comparison into `data/planner.js` and `data/machine.js`.
   - Create a `scene/bootstrap.js` responsible for renderer, camera, and controls configuration.
3. **Controller isolation**
   - Group recurring animation patterns (pulses, halos, timelines) under `systems/` with unit tests.
   - Move geometry/material builders into `scene/geometries.js` and `scene/materials.js`.
   - Centralize event routing (pointer events, keyboard shortcuts, upload handling) in
     `ui/interactions.js`.
4. **Testing and tooling**
   - Add Jest/Playwright coverage for parsing utilities and a smoke check that loads the viewer and
     asserts key DOM/text markers.
   - Wire linting/formatting to pre-commit hooks so viewer files follow the same guardrails.
5. **Progressive enhancements**
   - Introduce lazy loading for heavy assets and progressive disclosure for dense overlays.
   - Add per-module docs (`docs/viewer/*.md`) capturing data contracts and rendering conventions.

## Execution notes
- Maintain ES modules without bundling; prefer small files with clear exports.
- Keep line length under 100 characters and favor descriptive names over comments.
- Validate changes with `pre-commit run --all-files`, `pytest`, and a quick
  `python scripts/serve_viewer.py --host 127.0.0.1 --port 0` smoke before opening a PR.
- Capture before/after screenshots for visual adjustments using the provided browser tooling.
