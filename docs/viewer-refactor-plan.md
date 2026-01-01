# W1C Viewer Modularization Plan

This plan outlines how to break the current monolithic `viewer/index.html` into smaller, focused
modules so future Codex sessions can ship incremental improvements without re-reading a giant file.
The steps prioritize minimizing merge risk while keeping the viewer runnable at every phase.

## Goals
- Reduce `index.html` to a lean HTML shell that references external style and script bundles.
- Split viewer responsibilities into focused modules: data loading, UI overlays, scene objects,
  animation controllers, and utilities.
- Preserve the current experience while enabling quick iteration on the Pattern Studio preview,
  roadmap pedestals, and yarn flow instrumentation.
- Keep the structure compatible with static hosting (no build step required for now).

## Target structure
```
viewer/
├── index.html              # Thin shell with semantic markup and module/script tags
├── styles/
│   └── main.css            # Shared styling for overlay panels and status banners
├── src/
│   ├── constants.js        # Shared constants, fallbacks, palette definitions
│   ├── dom.js              # DOM lookups, event wiring helpers (planned)
│   ├── loaders/
│   │   ├── planner.js      # Fetch/parse planner exports, defaults, metadata (planned)
│   │   └── assets.js       # Static asset loading: textures, models, fonts (planned)
│   ├── scene/
│   │   ├── setup.js        # Renderer, camera, controls bootstrap (planned)
│   │   ├── components.js   # Geometry builders for frames, pedestals, anchors (planned)
│   │   └── effects.js      # Billboards, glows, pulses, sweep rings (planned)
│   ├── ui/
│   │   ├── overlay.js      # Overlay text updates and tone helpers (planned)
│   │   └── uploads.js      # Planner upload/drag-drop handling (planned)
│   └── main.js             # Entry point orchestrating loaders, scene, UI (planned)
└── main.js                 # Temporary host for legacy logic while modules land
```

## Progress
- Renderer, scene, camera, and control bootstrap now live in `viewer/src/scene/setup.js`, returning
  `{ renderer, scene, camera, controls }` so future refactors can import the shared defaults instead
  of rebuilding the config inline.
- Overlay tone helpers now live in `viewer/src/ui/tones.js`, keeping panel tone updates reusable
  while `main.js` continues to shrink.

## Migration phases
1. **Extract shared assets (done)**
   - Move inline CSS into `viewer/styles/main.css` and load it from `index.html`.
   - Move the inline `<script>` into `viewer/main.js` to shrink the HTML shell.
   - Hoist global constants and fallback strings into `viewer/src/constants.js` so other modules
     can reuse them without scrolling a single mega file.

2. **Stabilize entry points**
   - Create `viewer/src/dom.js` to centralize all `getElementById` lookups and reusable event
     wiring helpers (e.g., drag-drop, file input change listeners).
   - Move renderer/camera/control setup into `viewer/src/scene/setup.js`, exporting a factory that
     returns `{ renderer, scene, camera, controls }` while keeping configuration in one place.

3. **Module boundaries for logic**
   - Split planner parsing, default application, and bounds comparisons into `viewer/src/loaders/`.
   - Extract UI overlay updates (roadmap panel, pattern progress, yarn flow text) into
     `viewer/src/ui/overlay.js`, with small helpers for tone application and value formatting.
   - Extract billboard/halo/anchor builders into `viewer/src/scene/components.js`, returning
     grouped meshes plus controller callbacks to keep animation code separate from geometry setup.

4. **Animation controllers and state machines**
   - Introduce a light-weight state container for playback timing, yarn feed queues, and selection
     state. Keep it in a dedicated module so animation loops consume a clean API instead of reading
     global variables.
   - Migrate periodic updates (e.g., spool countdowns, tracer sweeps, insert grid pulses) into
     distinct controller classes or factory functions that accept the state container.

5. **Progressive cleanup**
   - Once modules exist, slim `viewer/main.js` to a small coordinator that wires modules together
     and hosts the animation loop.
   - Remove deprecated globals from the legacy script as the corresponding modules replace them.
   - Add targeted unit or snapshot tests where possible (e.g., bounds comparison helpers) to keep
     future refactors safe.

## Immediate next steps
- Carve out DOM lookups into `viewer/src/dom.js` and import them in `viewer/main.js`.
- Reuse the shared bootstrap in `viewer/src/scene/setup.js` while the animation loop lives in
  `viewer/main.js` temporarily.
- Extract formatter utilities so panel updates no longer depend on globals and keep slim tone usage
  alongside the shared helper.
- Align directory naming with the target structure above to minimize diff churn in future sessions.

## Testing expectations
- `pre-commit run --all-files`
- `pytest`
- `python scripts/serve_viewer.py --host 127.0.0.1 --port 0` (start/stop check)

Keep the viewer runnable after every phase so future Codex runs can pick up from a green baseline.
