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
upload and keyboard roadmap selection. A screenshot is saved in `test-results/`.

For the existing source preview workflow:

```sh
npm ci
npm run viewer:prepare
python scripts/serve_viewer.py --host 127.0.0.1 --port 8000
```

Both `viewer/vendor/` and `dist/` are generated and ignored. No container path is
introduced; the Python tooling and preview server remain available.

The Site artifact workflow uploads the validated `dist/`, named by PR
head SHA. After review and final-head CI, an owner can copy it into a separate
private Sites checkout and follow the current Sites registration/publication
workflow with `static: {"directory": "dist"}`. The owner supplies the real Site
identity there. No project IDs or credentials belong in this public repository.
This build and its CI do not register, publish or deploy a Site. Verify hosting
headers and the browser controls on the final origin before sharing its URL.

## Repeatable preview packages

`.sites/preview.json` is an identity-free recipe for this static export, not a
Sites runtime manifest. Use Node **22.19.0**, its npm **10.9.3**, and the existing
`package-lock.json`. No dependency update is needed. The original build and browser smoke
scripts remain unchanged.

The Site artifact workflow also accepts a manual `ref`, defaulting to `main`.
It accepts a branch name, `refs/heads/<branch>`, `refs/tags/<tag>`, or a full
40-character commit SHA. GitHub resolves that input once to a full commit and
tree. Missing, deleted or malformed refs fail; there is no fallback to main.
For pull requests, resolution uses the explicit head repository and head SHA,
not GitHub's synthetic merge commit. Checkout, the receipt and artifact naming
all use that resolved identity. Checkout does not persist credentials, and the
job retains only `contents: read`. The lookup token is scoped to its step.

Manual dispatch requires this workflow on the default branch. Until an owner
merges it, local resolver tests and a successful PR artifact do **not** establish
native manual-dispatch validation. Do not dispatch as a substitute for those
source and review gates. The owner can subsequently exercise default-main and
branch dispatches and retain their run identities as separate evidence.

The selected source must contain this recipe and packaging scripts. Older refs
without them fail explicitly; this workflow does not silently overlay or
cherry-pick an exporter. A tag means an explicitly selected existing tag, not a
wildcard or moving latest-tag search. Treat branch code as untrusted: run it in
an isolated checkout without production credentials or private inputs.

For a local retained package, resolve the desired ref using the exported
`resolvePreview` function in `scripts/resolve-preview.mjs`, supplying a GitHub
commit lookup. Save its returned JSON **outside** the checkout, fetch its full
commit, and check it out detached. Then run:

```sh
npm ci
npx playwright install chromium
node scripts/package-preview.mjs /absolute/path/to/resolved-source.json
```

The packager requires a clean, detached checkout matching the resolved commit
and tree. It runs `npm test`, `npm run build` and `npm run test:browser` itself.
It checks every exported file against the checked-out viewer and newly bundled
vendor files, blocks unexpected files, maps, symbolic links and executable files, and
checks that browser QA leaves the artifact bytes unchanged. The existing
external-request, actual play/pause/resume, upload and keyboard checks remain.
This establishes the existing 960-by-720 software-rendered browser scenarios;
it does not establish mobile, physical GPU, hardware or final-origin acceptance.

`dist/preview-provenance.json` records the requested ref, full source commit and
tree, recipe and `package-lock.json` hashes, runtime and dependency versions, synthetic
fixture hashes, commands, successful checks, per-file artifact hashes and CI
run/attempt/workflow identity (or `null` for a local run). Publication metadata
is `null`. It never collects arbitrary environment variables, private records,
Site IDs or credentials. `SHA256SUMS` covers every payload file and the receipt;
the receipt excludes itself and `SHA256SUMS` to avoid circular hashes.

The uploaded artifact keeps the existing `wove-site-<full-source-SHA>` name and
flat `dist/` layout, with the receipt added. GitHub's upload artifact digest and
artifact ID are external run evidence available after upload; they cannot be
embedded in that same artifact without changing its digest. Retain them with
the run URL when comparing artifacts. Hashes identify bytes, not authority or
a guarantee that two builds will be reproducible. Do not relabel a pre-merge
artifact as a main build. No source maps, Site registration, publication or
hosting configuration are added by this workflow.
