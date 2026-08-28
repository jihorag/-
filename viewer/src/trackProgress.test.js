import test from 'node:test';
import assert from 'node:assert/strict';
import { STATE, leafCoverage, leafCounts, nextPoint } from './trackProgress.js';

const leaf = { leaf_id: 'L1', points: [{ id: 'p1' }, { id: 'p2' }, { id: 'p3' }, { id: 'p4' }] };

test('기록이 없으면 coverage 0', () => {
  assert.equal(leafCoverage(leaf, {}), 0);
});

test('통과한 논점만 센다 — 설명만 본 것은 안 센다', () => {
  const prog = { L1: { p1: STATE.PASSED, p2: STATE.SEEN } };
  assert.equal(leafCoverage(leaf, prog), 0.25);
});

test('전부 통과하면 1', () => {
  const prog = { L1: { p1: 2, p2: 2, p3: 2, p4: 2 } };
  assert.equal(leafCoverage(leaf, prog), 1);
});

test('논점이 없으면 0으로 나누지 않는다', () => {
  assert.equal(leafCoverage({ leaf_id: 'X', points: [] }, {}), 0);
});

test('leafCounts는 seen에 passed를 포함한다', () => {
  const prog = { L1: { p1: STATE.PASSED, p2: STATE.SEEN } };
  assert.deepEqual(leafCounts(leaf, prog), { total: 4, seen: 2, passed: 1 });
});

test('nextPoint는 통과 못 한 첫 논점', () => {
  const prog = { L1: { p1: STATE.PASSED, p2: STATE.SEEN } };
  assert.equal(nextPoint(leaf, prog).id, 'p2');
});

test('전부 통과하면 nextPoint는 null', () => {
  const prog = { L1: { p1: 2, p2: 2, p3: 2, p4: 2 } };
  assert.equal(nextPoint(leaf, prog), null);
});

test('진도에 없는 관은 첫 논점부터', () => {
  assert.equal(nextPoint(leaf, {}).id, 'p1');
});
