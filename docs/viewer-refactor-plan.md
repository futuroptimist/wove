# W1C Viewer Refactor Plan

This plan captures how to break the monolithic `viewer/index.html` into modular, testable pieces.
It prioritizes changes that unblock future work while keeping the viewer shippable between steps.

## Goals
- **Maintain current behavior** while improving readability and debuggability.
- **Modularize by concern** (scene setup, data loading, animation systems, UI panels).
- **Enable incremental commits** so future Codex sessions can continue without large rebases.
- **Prepare for testing** by isolating logic that can be unit-tested without WebGL.

## Target structure
- `viewer/src/core/` — renderer + scene bootstrapping, lights, resize/orbit controls.
- `viewer/src/data/` — loader utilities for planner payloads, machine profiles, bounds.
- `viewer/src/systems/` — reusable animation + visualization controllers (yarn flow, bounds cage,
  cable chains, travel envelopes).
- `viewer/src/ui/` — DOM queries, overlay rendering, interaction helpers.
- `viewer/src/config/` — shared constants, fallback copy, defaults for planner playback.
- `viewer/main.js` — small entry point that wires modules together (type="module" import in
  `index.html`).

## Refactor phases
1. **Foundation (current step)**
   - Extract shared constants and DOM lookup helpers into modules to reduce `index.html` churn.
   - Keep entry point in `index.html` but move toward a `main.js` module.
2. **Scene + UI separation**
   - Move renderer/scene/camera setup (and resize/orbit controls) into `src/core/scene.js`.
   - Move overlay state management (status/pattern/panels) into `src/ui/overlays.js`.
3. **Data + parsing isolation**
   - Split planner/machine profile parsing into `src/data/planner.js` and
     `src/data/machine-profile.js` with pure functions for bounds and metadata extraction.
4. **Systems extraction**
   - Carve out animation controllers (yarn flow, cable chain, automation sweep) into
     `src/systems/*` modules with small public APIs.
   - Introduce a thin registry to update systems each frame.
5. **Entry-point cleanup**
   - Replace inline script with `viewer/main.js` that imports core/ui/data/systems modules and
     wires them together.
6. **Testing + linting**
   - Add targeted unit tests for pure helpers (parsing, formatting, bounds comparison) using
     Jest or Vitest.
   - Wire a minimal lint/format step and document dev workflow in `docs/`.

## Rollout notes
- Keep each phase shippable; ensure the fallback planner preview still runs after every step.
- Favor named exports and small modules to make future merges low-risk.
- Update `docs/` alongside code to keep new module boundaries discoverable.
- Continue capturing screenshots when visual behavior changes.

## Immediate next steps (started now)
- Land shared config + DOM helper modules and switch `index.html` to import them.
- Next sessions should move scene bootstrapping out of `index.html` per Phase 2.
