import test from 'node:test';
import assert from 'node:assert/strict';
import { applyScope } from './trackScope.js';

const LEAVES = [
  { id: 'a', path: ['미시경제학', '제1장', '제1절', '제1관'] },
  { id: 'b', path: ['재정학', '제1장', '제1절', '제1관'] },
  { id: 'c', path: ['거시경제학', '제1장', '제1절', '제1관'] },
];

test('제외 목록의 세부과목이 빠진다', () => {
  const out = applyScope(LEAVES, { exclude_divisions: ['재정학'] });
  assert.deepEqual(out.map((l) => l.id), ['a', 'c']);
});

test('scope 가 없으면 원본 그대로', () => {
  assert.equal(applyScope(LEAVES, null).length, 3);
  assert.equal(applyScope(LEAVES, {}).length, 3);
});

test('원본 배열을 변형하지 않는다 — 순서가 곧 커리큘럼이다', () => {
  const copy = LEAVES.slice();
  applyScope(LEAVES, { exclude_divisions: ['재정학'] });
  assert.deepEqual(LEAVES, copy);
});

test('path 가 없는 leaf 는 버리지 않는다 — 조용한 유실 금지', () => {
  const out = applyScope([{ id: 'x' }], { exclude_divisions: ['재정학'] });
  assert.deepEqual(out.map((l) => l.id), ['x']);
});

test('제외 목록이 빈 배열이면 아무것도 안 뺀다', () => {
  assert.equal(applyScope(LEAVES, { exclude_divisions: [] }).length, 3);
});
