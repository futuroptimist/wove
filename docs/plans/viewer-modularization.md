# W1C viewer modularization plan

The current `viewer/index.html` hosts styling, markup, scene setup, UI wiring, and animation logic
in a single module. This plan proposes a multi-phase refactor that splits the Pattern Studio viewer
into focused files, keeps future additions incremental, and keeps the experience shippable after
each step.

## Objectives

- Improve readability by isolating rendering, UI, data parsing, and state management concerns.
- Enable iterative enhancements to the Three.js scene without touching unrelated planner logic.
- Reduce regression risk through tighter module boundaries and targeted tests.
- Keep the viewer runnable via `python scripts/serve_viewer.py` throughout the refactor.

## Target architecture

- `viewer/index.html`: markup, theme styles, module imports, and bootstrap only.
- `viewer/src/ui-elements.js`: DOM lookup helpers and UI element registries.
- `viewer/src/viewer-config.js`: shared defaults, fallback copy, and constant palettes.
- `viewer/src/state.js`: central state container for controller collections and runtime flags.
- `viewer/src/scene/`: mesh creation, lighting, materials, and geometry utilities.
- `viewer/src/interactions/`: input handling (orbit, keyboard, drag-and-drop).
- `viewer/src/pattern/`: planner parsing, playback clocks, bounds comparison, and yarn flow cues.
- `viewer/src/ui/`: overlay rendering, status copy updates, progress bars, and upload flows.
- `viewer/src/services/`: data loading, caching, and validation helpers.
- `viewer/src/animation-loop.js`: render loop orchestration and controller tick routing.

## Phased migration

### Phase 1: Bootstrap separation (highest impact)

- Extract shared configuration (fallback text, palette values, default planner settings) to a
  module.
- Extract DOM element lookups into a helper so rendering code no longer touches `document` directly.
- Introduce a minimal state container that tracks controller arrays and runtime flags.
- Wire `index.html` to import these modules while keeping functional parity.

### Phase 2: Scene and UI segmentation

- Move mesh/material construction into `scene` utilities (e.g., bed, pedestals, holograms).
- Move overlay copy + formatting into `ui` helpers and keep strings centralized in config.
- Separate planner parsing/loading from the render loop; expose pure utilities for tests.
- Add lightweight unit tests for parsing helpers (bounds comparison, planner metadata).

### Phase 3: Interaction and animation decoupling

- Split animation controllers into individual modules (e.g., spool halo, cable chain pulses).
- Route all per-frame updates through a central `animation-loop` dispatcher.
- Isolate input handlers (drag, scroll, keyboard shortcuts) from rendering concerns.

### Phase 4: Hardening and follow-ups

- Add docs to `docs/plans/` as modules land; keep a changelog of moved responsibilities.
- Expand tests to cover pause/resume logic, upload validation, and bounds warnings.
- Consider bundling (Vite/ESM) once modules are established to simplify CDN pinning.

## Testing expectations

- Keep `pre-commit run --all-files`, `pytest`, and
  `python scripts/serve_viewer.py --host 127.0.0.1 --port 0` green after each incremental merge.
- Prefer small, atomic PRs that migrate one responsibility at a time.

## Notes for future Codex sessions

- Favor extraction over rewrites; move code verbatim into modules before refactoring internals.
- Maintain feature flags for new visuals so the viewer stays stable during multi-step migrations.
- Update this plan with completed phases and new follow-ups to keep continuity across sessions.
