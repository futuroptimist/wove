import { chromium, expect } from '@playwright/test';
import { createServer } from 'node:http';
import { readFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';

const dist = path.resolve(fileURLToPath(new URL('../dist/', import.meta.url)));
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.txt': 'text/plain' };
// Loopback-only test server for the exported artifact.
const server = createServer(async (req, res) => {
  const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  const file = path.resolve(dist, '.' + (pathname === '/' ? '/index.html' : pathname));
  if (!file.startsWith(dist + path.sep)) { res.writeHead(404).end(); return; }
  try {
    const bytes = await readFile(file);
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] ?? 'application/octet-stream' }).end(bytes);
  } catch { res.writeHead(404).end(); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
let browser;
try {
  browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  // The full assembly is expensive on CI's software GPU. Keep real playback and
  // actionability checks, but give that renderer a smaller canvas and more time.
  const page = await browser.newPage({ viewport: { width: 960, height: 720 } });
  page.setDefaultTimeout(90000);
  const errors = [], external = [];
  page.on('pageerror', error => { errors.push(error.message); console.error(error.message); });
  page.on('console', message => { if (message.type() === 'error') console.error(message.text()); });
  await page.route('**/*', route => {
    if (new URL(route.request().url()).origin !== origin) {
      external.push(route.request().url());
      return route.abort();
    }
    return route.continue();
  });
  assert.equal((await page.goto(origin)).status(), 200);
  await expect(page.locator('canvas').first()).toBeVisible();
  await expect(page.locator('#planner-file-name')).toContainText('base_chain_row.planner.json');
  await page.getByRole('button', { name: 'Pause preview', exact: true }).click();
  await expect(page.locator('#pattern-playback-status')).toContainText('Paused');
  await page.getByRole('button', { name: 'Resume preview', exact: true }).click();
  await expect(page.locator('#pattern-playback-status')).toContainText('Running');
  await page.locator('#planner-upload').setInputFiles(path.join(dist, 'assets/base_chain_row.planner.json'));
  await expect(page.locator('#status')).toContainText('Planner upload loaded: base_chain_row.planner.json');
  await page.locator('#planner-upload').blur();
  await page.locator('#pattern-pause-toggle').blur();
  const previousMilestone = await page.locator('#roadmap-title').textContent();
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('#roadmap-title')).not.toHaveText(previousMilestone);
  await mkdir(new URL('../test-results/', import.meta.url), { recursive: true });
  await page.screenshot({ path: fileURLToPath(new URL('../test-results/viewer.png', import.meta.url)) });
  assert.deepEqual(errors, []);
  assert.deepEqual(external, [], 'The viewer must work without a CDN or backend');
} finally {
  await browser?.close();
  await new Promise(resolve => server.close(resolve));
}
