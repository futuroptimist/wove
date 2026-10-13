import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, symlink, chmod, readFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { resolvePreview, validateRef, artifactName } from '../../scripts/resolve-preview.mjs';
import { assertIdentity, inventory, validateReceipt, verifyChecksums } from '../../scripts/package-preview.mjs';

const sha = 'a'.repeat(40), tree = 'b'.repeat(40), merge = 'c'.repeat(40);
const commit = { sha, commit: { tree: { sha: tree } } };
const repository = 'futuroptimist/wove';
const dispatch = ref => ({ repository, eventName: 'workflow_dispatch', event: {}, ref });
for (const ref of ['main', 'feature/preview', 'refs/heads/feature/preview', 'refs/tags/v1.0', sha]) {
  test(`resolves immutable identity for ${ref}`, async () => {
    const result = await resolvePreview(dispatch(ref), async (repo, requested) => {
      assert.equal(repo, repository);
      assert.equal(requested, ref);
      return commit;
    });
    assert.deepEqual(result, { repository, requestedRef: ref, pr: null, commit: sha, tree, artifactName: artifactName(sha) });
    assertIdentity(result, sha, tree);
    assert.throws(() => assertIdentity(result, merge, tree));
    assert.throws(() => assertIdentity({ ...result, tree: merge }, sha, tree));
    assert.throws(() => assertIdentity({ ...result, artifactName: artifactName(merge) }, sha, tree));
  });
}
test('deleted and missing branches never fall back to main', async () => {
  for (const ref of ['deleted-branch', 'missing-branch']) {
    let calls = 0;
    await assert.rejects(resolvePreview(dispatch(ref), async () => { calls++; throw new Error('404'); }), /404/);
    assert.equal(calls, 1);
  }
});
test('invalid input is rejected before lookup', async () => {
  for (const ref of ['', '-main', '../main', 'main..next', 'main\nother', '$(id)', 'main;id', 'a b', 'a\\b', 'refs/pull/4/merge', 'branch.lock', '.hidden', 'refs/heads/', 'a//b']) {
    assert.throws(() => validateRef(ref), undefined, ref);
    await assert.rejects(resolvePreview(dispatch(ref), async () => assert.fail('must not look up invalid ref')));
  }
});
test('PR uses explicit head repository and SHA, never synthetic merge SHA', async () => {
  const result = await resolvePreview({ repository, eventName: 'pull_request', event: {
    sha: merge,
    pull_request: { number: 42, merge_commit_sha: merge, head: { sha, repo: { full_name: 'synthetic-owner/wove' } } },
  } }, async (repo, ref) => {
    assert.equal(repo, 'synthetic-owner/wove');
    assert.equal(ref, sha);
    return commit;
  });
  assertIdentity(result, sha, tree);
  assert.equal(result.artifactName, `wove-site-${sha}`);
});
test('full SHA lookup cannot resolve a different commit', async () => {
  await assert.rejects(resolvePreview(dispatch(merge), async () => commit));
});
test('checksum inventory is complete and rejects duplicates, missing and altered files', () => {
  const digest = 'd'.repeat(64);
  const files = { 'index.html': digest, SHA256SUMS: 'unused' };
  verifyChecksums(files, `${digest}  index.html\n`);
  for (const sums of ['', `${digest}  missing.html\n`, `${digest}  index.html\n${digest}  index.html\n`, `${'e'.repeat(64)}  index.html\n`]) {
    assert.throws(() => verifyChecksums(files, sums));
  }
  assert.throws(() => verifyChecksums({ ...files, 'extra.txt': digest }, `${digest}  index.html\n`));
});
test('inventory rejects hidden files, source maps, symlinks and executable files', async () => {
  for (const type of ['hidden', 'map', 'symlink', 'executable']) {
    const dir = await mkdtemp(path.join(os.tmpdir(), 'wove-preview-'));
    const file = path.join(dir, type === 'hidden' ? '.env' : type === 'map' ? 'index.js.map' : 'index.js');
    if (type === 'symlink') await symlink('/etc/passwd', file);
    else await writeFile(file, 'synthetic');
    if (type === 'executable') await chmod(file, 0o755);
    await assert.rejects(inventory(dir));
  }
});
test('receipt rejects private/publication fields and any changed identity or digest', () => {
  const receipt = {
    schemaVersion: 1,
    source: { repository, requestedRef: 'main', pr: null, commit: sha, tree, artifactName: artifactName(sha) },
    capturedAt: '2026-01-01T00:00:00.000Z',
    recipe: { path: '.sites/preview.json', revision: 1, sha256: 'd'.repeat(64) },
    lockfile: { path: 'package-lock.json', sha256: 'e'.repeat(64) },
    tools: {}, buildInputs: {}, commands: [], checks: {}, ci: null,
    artifact: { name: artifactName(sha), files: { 'index.html': 'f'.repeat(64) } },
    publication: null,
  };
  validateReceipt(structuredClone(receipt), receipt);
  for (const changed of [
    { ...receipt, siteId: 'synthetic-site' },
    { ...receipt, privateRecords: [] },
    { ...receipt, publication: { url: 'https://example.invalid' } },
    { ...receipt, recipe: { sha256: '0'.repeat(64) } },
    { ...receipt, lockfile: { sha256: '0'.repeat(64) } },
    { ...receipt, artifact: { files: {} } },
    { ...receipt, source: { commit: merge, tree } },
  ]) assert.throws(() => validateReceipt(changed, receipt));
});
test('workflow checkout, naming and receipt share resolved identity without shell ref interpolation', async () => {
  const workflow = await readFile(new URL('../../.github/workflows/site-artifact.yml', import.meta.url), 'utf8');
  assert.match(workflow, /default: main/);
  assert.match(workflow, /contents: read/);
  assert.match(workflow, /repository: \$\{\{ steps.source.outputs.repository \}\}/);
  assert.match(workflow, /ref: \$\{\{ steps.source.outputs.commit \}\}/);
  assert.match(workflow, /name: \$\{\{ steps.source.outputs.artifactName \}\}/);
  assert(!workflow.split('\n').some(line => line.includes('run:') && line.includes('${{')));
  assert.equal((workflow.match(/persist-credentials: false/g) || []).length, 2);
});
