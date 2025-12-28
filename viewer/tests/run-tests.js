#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const projectRoot = resolve(fileURLToPath(new URL('../..', import.meta.url)));
const filteredArgs = process.argv.slice(2).filter((arg) => arg !== '--coverage');

const result = spawnSync(
  process.execPath,
  ['--test', ...filteredArgs],
  { stdio: 'inherit', cwd: projectRoot },
);

if (result.error) {
  console.error(result.error);
  process.exit(1);
}

process.exit(result.status ?? (result.signal ? 1 : 0));
