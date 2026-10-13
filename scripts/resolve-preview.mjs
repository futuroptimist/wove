import assert from 'node:assert/strict';
import { appendFile, readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

export function validateRef(ref) {
  assert.equal(typeof ref, 'string', 'Ref must be a string');
  assert(ref.length > 0 && ref.length <= 200, 'Invalid ref length');
  assert(/^[A-Za-z0-9][A-Za-z0-9._/-]*$/.test(ref), 'Invalid ref characters');
  assert(!ref.includes('..') && !ref.includes('//') && !ref.endsWith('/'), 'Invalid ref');
  assert(ref.split('/').every(part => !part.startsWith('.') && !part.endsWith('.') && !part.endsWith('.lock')), 'Invalid ref component');
  assert(!ref.startsWith('refs/') || ref.startsWith('refs/heads/') || ref.startsWith('refs/tags/'), 'Unsupported ref namespace');
  return ref;
}

export function artifactName(sha) {
  assert.match(sha, /^[a-f0-9]{40}$/);
  return `wove-site-${sha}`;
}

export async function resolvePreview({ repository, eventName, event, ref = 'main' }, getCommit) {
  assert.equal(repository, 'futuroptimist/wove', 'Unexpected workflow repository');
  let sourceRepository = repository;
  let requestedRef = validateRef(ref);
  let pr = null;
  if (eventName === 'pull_request') {
    sourceRepository = event.pull_request.head.repo.full_name;
    requestedRef = event.pull_request.head.sha;
    assert.match(requestedRef, /^[a-f0-9]{40}$/, 'PR head must be a full SHA');
    pr = event.pull_request.number;
    assert(Number.isSafeInteger(pr) && pr > 0);
  } else {
    assert.equal(eventName, 'workflow_dispatch', 'Unsupported event');
  }
  assert.match(sourceRepository, /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/);
  const commit = await getCommit(sourceRepository, requestedRef);
  const sha = commit.sha;
  const tree = commit.commit.tree.sha;
  assert.match(sha, /^[a-f0-9]{40}$/);
  assert.match(tree, /^[a-f0-9]{40}$/);
  if (/^[a-f0-9]{40}$/.test(requestedRef)) assert.equal(sha, requestedRef);
  return { repository: sourceRepository, requestedRef, pr, commit: sha, tree, artifactName: artifactName(sha) };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const identity = await resolvePreview({
    repository: process.env.GITHUB_REPOSITORY,
    eventName: process.env.GITHUB_EVENT_NAME,
    event: JSON.parse(await readFile(process.env.GITHUB_EVENT_PATH, 'utf8')),
    ref: process.env.PREVIEW_REF || 'main',
  }, async (repository, ref) => {
    const response = await fetch(`https://api.github.com/repos/${repository}/commits/${encodeURIComponent(ref)}`, {
      headers: { Accept: 'application/vnd.github+json', Authorization: `Bearer ${process.env.GITHUB_TOKEN}` },
      signal: AbortSignal.timeout(30000),
    });
    assert(response.ok, `Ref resolution failed (${response.status}); no fallback is allowed`);
    return response.json();
  });
  await writeFile(process.env.PREVIEW_IDENTITY, JSON.stringify(identity, null, 2) + '\n');
  await appendFile(process.env.GITHUB_OUTPUT, Object.entries(identity).filter(([key]) => ['repository', 'commit', 'tree', 'artifactName'].includes(key)).map(([key, value]) => `${key}=${value}\n`).join(''));
}
