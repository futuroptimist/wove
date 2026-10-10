# Viewer artifact and owner handoff

Wove's Site scope is its existing assembly viewer and planner playback. There is
no Python compiler, hardware connection or service port in this browser artifact.
Planner JSON uploads stay in the browser. The included planner sample is copied
unchanged from `viewer/assets`.

```sh
npm ci
npm run build
npm test
npx playwright install chromium
npm run test:browser
```

Use Node 22 or later. The build bundles pinned Three.js 0.161.0 and OrbitControls
locally, removing the broken CDN bare import and the runtime CDN dependency.
It copies the existing viewer modules, CSS and assets to `dist/`, includes the
Wove and Three.js MIT notices, and writes `dist/SHA256SUMS`. The browser smoke
test blocks external requests and checks sample loading, pause/resume, planner
upload and keyboard interaction. A screenshot is saved in `test-results/`.

For the existing source preview workflow:

```sh
npm ci
npm run viewer:prepare
python scripts/serve_viewer.py --host 127.0.0.1 --port 8000
```

Both `viewer/vendor/` and `dist/` are generated and ignored. No container path is
introduced; the Python tooling and preview server remain available.

The PR-only Site artifact workflow uploads the validated `dist/`, named by PR
head SHA. After review and final-head CI, an owner can copy it into a separate
private Sites checkout and follow the current Sites registration/publication
workflow with `static: {"directory": "dist"}`. The owner supplies the real Site
identity there. No project IDs or credentials belong in this public repository.
This build and its CI do not register, publish or deploy a Site. Verify hosting
headers and the browser controls on the final origin before sharing its URL.
