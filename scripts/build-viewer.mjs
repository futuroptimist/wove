import './prepare-viewer.mjs';
import { build } from 'esbuild';
import { cp, mkdir, rm, readFile, readdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const dist = path.join(root, 'dist');
// Parse and resolve the full module graph before exporting the existing files.
await build({ absWorkingDir: root, entryPoints: ['viewer/src/main.js'], bundle: true, format: 'esm', write: false });
// This fixed generated directory is the only path removed by this build.
await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });
for (const name of ['index.html', 'bounds.js', 'src', 'styles', 'assets', 'vendor']) {
  await cp(path.join(root, 'viewer', name), path.join(dist, name), { recursive: true });
}
await cp(path.join(root, 'LICENSE'), path.join(dist, 'wove-MIT.txt'));
const hashes = [];
async function inventory(dir) {
  for (const entry of (await readdir(dir, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) await inventory(file);
    else hashes.push(`${createHash('sha256').update(await readFile(file)).digest('hex')}  ${path.relative(dist, file).split(path.sep).join('/')}`);
  }
}
await inventory(dist);
await writeFile(path.join(dist, 'SHA256SUMS'), hashes.join('\n') + '\n');
console.log(`Built ${hashes.length} viewer files in ${dist}`);
