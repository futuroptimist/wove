import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFile, readdir, lstat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { artifactName, validateRef } from './resolve-preview.mjs';

const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const git = (root, ...args) => execFileSync('git', args, { cwd: root, encoding: 'utf8' }).trim();
export async function inventory(directory, prefix = '') {
  const result = {};
  for (const name of (await readdir(path.join(directory, prefix))).sort()) {
    assert(!name.startsWith('.') && !name.endsWith('.map'), `Forbidden artifact path: ${name}`);
    const relative = prefix ? `${prefix}/${name}` : name;
    const file = path.join(directory, relative);
    const stat = await lstat(file);
    assert(!stat.isSymbolicLink(), `Symlink is not allowed: ${relative}`);
    if (stat.isDirectory()) Object.assign(result, await inventory(directory, relative));
    else {
      assert(stat.isFile() && !(stat.mode & 0o111), `Unexpected executable or special file: ${relative}`);
      result[relative] = hash(await readFile(file));
    }
  }
  return result;
}

export function assertIdentity(identity, head, tree) {
  assert.match(tree, /^[a-f0-9]{40}$/);
  assert.deepEqual(Object.keys(identity).sort(), ['artifactName', 'commit', 'pr', 'repository', 'requestedRef', 'tree'].sort());
  assert.match(identity.repository, /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/);
  validateRef(identity.requestedRef);
  assert(identity.pr === null || (Number.isSafeInteger(identity.pr) && identity.pr > 0));
  assert.equal(identity.commit, head, 'Checkout differs from resolved source');
  assert.equal(identity.tree, tree, 'Checkout tree differs from resolved source');
  assert.equal(identity.artifactName, artifactName(head));
}

export function verifyChecksums(files, sums, excluded = []) {
  const entries = sums.trimEnd().split('\n').map(line => {
    assert.match(line, /^[a-f0-9]{64}  [^\r\n]+$/);
    return [line.slice(66), line.slice(0, 64)];
  });
  assert.equal(new Set(entries.map(([name]) => name)).size, entries.length, 'Duplicate checksum');
  const expected = Object.fromEntries(Object.entries(files).filter(([name]) => name !== 'SHA256SUMS' && !excluded.includes(name)));
  assert.deepEqual(Object.fromEntries(entries), expected, 'Incomplete or incorrect checksums');
}

export async function sourceFiles(root) {
  const files = {};
  const tracked = git(root, 'ls-files', '-z', '--', 'viewer/index.html', 'viewer/bounds.js', 'viewer/src', 'viewer/styles', 'viewer/assets').split('\0').filter(Boolean);
  for (const name of tracked) files[name.slice('viewer/'.length)] = hash(await readFile(path.join(root, name)));
  for (const name of ['three.js', 'three-MIT.txt']) files[`vendor/${name}`] = hash(await readFile(path.join(root, 'viewer/vendor', name)));
  files['wove-MIT.txt'] = hash(await readFile(path.join(root, 'LICENSE')));
  return files;
}

export function validateReceipt(receipt, expected) {
  assert.deepEqual(Object.keys(receipt).sort(), ['schemaVersion', 'source', 'capturedAt', 'recipe', 'lockfile', 'tools', 'buildInputs', 'commands', 'checks', 'artifact', 'ci', 'publication'].sort(), 'Unexpected receipt fields');
  assert.equal(receipt.schemaVersion, 1);
  assert.equal(new Date(receipt.capturedAt).toISOString(), receipt.capturedAt);
  for (const item of [receipt.recipe, receipt.lockfile]) assert.match(item.sha256, /^[a-f0-9]{64}$/);
  assert.equal(receipt.recipe.path, '.sites/preview.json');
  assert.equal(receipt.lockfile.path, 'package-lock.json');
  assert(Number.isSafeInteger(receipt.recipe.revision) && receipt.recipe.revision > 0);
  assertIdentity(receipt.source, expected.source.commit, expected.source.tree);
  assert.equal(receipt.artifact.name, artifactName(receipt.source.commit));
  assert(Object.keys(receipt.artifact.files).length > 0);
  for (const [name, digest] of Object.entries(receipt.artifact.files)) {
    assert(!name.startsWith('/') && !name.split('/').some(part => part.startsWith('.') || !part));
    assert.match(digest, /^[a-f0-9]{64}$/);
  }
  // Compare all nested values against independently captured source/build evidence.
  assert.deepEqual(receipt, expected, 'Receipt schema or provenance mismatch');
  assert.equal(receipt.publication, null);
}

export function verifyCheckout(root, identity) {
  assertIdentity(identity, git(root, 'rev-parse', 'HEAD'), git(root, 'rev-parse', 'HEAD^{tree}'));
  assert.equal(git(root, 'status', '--porcelain', '--untracked-files=normal'), '', 'Packaging requires a clean checkout');
  assert.equal(git(root, 'branch', '--show-current'), '', 'Packaging requires a detached checkout');
}

export async function packagePreview(root, identity, { run = null } = {}) {
  verifyCheckout(root, identity);
  const recipeBytes = await readFile(path.join(root, '.sites/preview.json'));
  const recipe = JSON.parse(recipeBytes);
  assert.equal(recipe.schemaVersion, 1);
  assert.equal(recipe.project.repository, 'futuroptimist/wove');
  assert.equal(recipe.build.node, process.versions.node, 'Use the recipe Node version');
  const npm = execFileSync('npm', ['--version'], { encoding: 'utf8' }).trim();
  assert.equal(recipe.build.npm, npm, 'Use the recipe npm version');
  const commands = [['npm', 'ci'], ['npm', 'test'], ['npm', 'run', 'build'], ['npm', 'run', 'test:browser']];
  assert.deepEqual(recipe.build.commands, commands);
  assert.equal(recipe.build.workingDirectory, '.');
  assert.equal(recipe.build.lockfile, 'package-lock.json');
  assert.equal(recipe.artifact.directory, 'dist');
  assert.deepEqual(recipe.preview.allowedExternalOrigins, []);
  assert.equal(recipe.preview.dataMode, 'synthetic');
  assert.deepEqual(recipe.preview.fixtureInputs, ['viewer/assets/base_chain_row.planner.json']);
  const lockBytes = await readFile(path.join(root, 'package-lock.json'));
  const lock = JSON.parse(lockBytes);
  const versions = {};
  for (const name of ['three', 'esbuild', '@playwright/test', 'playwright', 'playwright-core']) {
    versions[name] = JSON.parse(await readFile(path.join(root, 'node_modules', name, 'package.json'))).version;
    assert.equal(versions[name], lock.packages[`node_modules/${name}`].version);
  }
  // Use fixed commands, never execute arbitrary recipe text or interpolate a ref.
  for (const args of [['test'], ['run', 'build']]) execFileSync('npm', args, { cwd: root, stdio: 'inherit' });
  const dist = path.join(root, 'dist');
  const before = await inventory(dist);
  verifyChecksums(before, await readFile(path.join(dist, 'SHA256SUMS'), 'utf8'));
  const expectedFiles = await sourceFiles(root);
  assert.deepEqual(Object.fromEntries(Object.entries(before).filter(([name]) => name !== 'SHA256SUMS')), expectedFiles, 'Export differs from source');
  execFileSync('npm', ['run', 'test:browser'], { cwd: root, stdio: 'inherit' });
  assert.deepEqual(await inventory(dist), before, 'Artifact changed during browser checks');
  assert.equal(git(root, 'status', '--porcelain', '--untracked-files=normal'), '', 'Source changed during checks');
  if (run !== null) {
    assert.deepEqual(Object.keys(run).sort(), ['attempt', 'id', 'repository', 'workflowRef', 'workflowSha'].sort());
    assert.match(run.id, /^\d+$/);
    assert.match(run.attempt, /^\d+$/);
    assert.equal(run.repository, 'futuroptimist/wove');
    assert.match(run.workflowSha, /^[a-f0-9]{40}$/);
    assert.match(run.workflowRef, /^futuroptimist\/wove\/\.github\/workflows\/site-artifact.yml@refs\/[A-Za-z0-9._/-]+$/);
  }
  const { chromium } = await import('@playwright/test');
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  let chromiumVersion;
  try { chromiumVersion = browser.version(); } finally { await browser.close(); }
  const receipt = {
    schemaVersion: 1,
    source: identity,
    capturedAt: new Date().toISOString(),
    recipe: { path: '.sites/preview.json', sha256: hash(recipeBytes), revision: recipe.project.recipeRevision },
    lockfile: { path: 'package-lock.json', sha256: hash(lockBytes) },
    tools: { node: process.versions.node, npm, platform: process.platform, arch: process.arch, packages: versions, chromium: chromiumVersion },
    buildInputs: { browser: { viewport: { width: 960, height: 720 }, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }, dataMode: 'synthetic', externalOrigins: [], fixtures: { 'viewer/assets/base_chain_row.planner.json': hash(await readFile(path.join(root, 'viewer/assets/base_chain_row.planner.json'))) } },
    commands,
    checks: { unit: 'passed', build: 'passed', browser: 'passed', sourceCorrespondence: 'passed' },
    artifact: { name: identity.artifactName, files: expectedFiles },
    ci: run,
    publication: null,
  };
  await writeFile(path.join(dist, 'preview-provenance.json'), JSON.stringify(receipt, null, 2) + '\n');
  validateReceipt(JSON.parse(await readFile(path.join(dist, 'preview-provenance.json'), 'utf8')), receipt);
  const finalFiles = await inventory(dist);
  await writeFile(path.join(dist, 'SHA256SUMS'), Object.keys(finalFiles).filter(name => name !== 'SHA256SUMS').sort().map(name => `${finalFiles[name]}  ${name}\n`).join(''));
  verifyChecksums(await inventory(dist), await readFile(path.join(dist, 'SHA256SUMS'), 'utf8'));
  return receipt;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const identity = JSON.parse(await readFile(process.argv[2], 'utf8'));
  const run = process.env.GITHUB_ACTIONS === 'true' ? {
    repository: process.env.GITHUB_REPOSITORY,
    id: process.env.GITHUB_RUN_ID,
    attempt: process.env.GITHUB_RUN_ATTEMPT,
    workflowRef: process.env.GITHUB_WORKFLOW_REF,
    workflowSha: process.env.GITHUB_WORKFLOW_SHA,
  } : null;
  await packagePreview(process.cwd(), identity, { run });
}
