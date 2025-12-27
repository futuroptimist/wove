import test from 'node:test';
import assert from 'node:assert/strict';

import { computeYarnFeedIndices } from '../src/feeds.js';

test('returns no feeds when no events provided', () => {
  assert.deepEqual(computeYarnFeedIndices([]), []);
  assert.deepEqual(computeYarnFeedIndices(null), []);
});

test('detects yarn feed comments and extrusion deltas', () => {
  const events = [
    { comment: 'travel move', extrusion: 0 },
    { comment: 'feed yarn', extrusion: 0 },
    { comment: 'plunge', extrusion: 0.15 },
    { comment: 'advance', extrusion: 0.18 },
  ];

  assert.deepEqual(computeYarnFeedIndices(events), [1, 2, 3]);
});

test('uses baseline extrusion when spotting feed pulses', () => {
  const events = [
    { comment: 'start', extrusion: 5.0 },
    { comment: 'move', extrusion: 5.005 },
    { comment: 'move', extrusion: 5.02 },
    { comment: 'move', extrusion: 4.98 },
  ];

  const baseline = 5.0;
  assert.deepEqual(computeYarnFeedIndices(events, baseline), [2]);
});
