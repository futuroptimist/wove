import { build } from 'esbuild';
import { mkdir, copyFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
await mkdir(new URL('../viewer/vendor/', import.meta.url), { recursive: true });
await build({
  absWorkingDir: root,
  stdin: {
    contents: `import * as THREE from 'three';
export { THREE };
export { OrbitControls } from 'three/addons/controls/OrbitControls.js';`,
    resolveDir: root,
  },
  bundle: true,
  format: 'esm',
  platform: 'browser',
  minify: true,
  outfile: 'viewer/vendor/three.js',
});
await copyFile(new URL('../node_modules/three/LICENSE', import.meta.url), new URL('../viewer/vendor/three-MIT.txt', import.meta.url));
