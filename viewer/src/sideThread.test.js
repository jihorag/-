import test from 'node:test';
import assert from 'node:assert/strict';
import { sideKey, loadSide, appendSide, clearSide, sideCount, SIDE_MAX } from './sideThread.js';

// node 에는 localStorage 가 없다. 최소 구현을 심는다.
function fakeStorage() {
  const m = new Map();
  return {
    getItem: (k) => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => m.set(k, String(v)),
    removeItem: (k) => m.delete(k),
  };
}
test.beforeEach(() => { globalThis.localStorage = fakeStorage(); });

test('키는 관과 논점을 함께 담는다 — 심화 탭의 관 단위 키와 겹치지 않는다', () => {
  assert.equal(sideKey('leaf-1', 'p-3'), 'ailearn-side:leaf-1:p-3');
});

test('아무것도 없으면 빈 배열', () => {
  assert.deepEqual(loadSide('leaf-1', 'p-3'), []);
  assert.equal(sideCount('leaf-1', 'p-3'), 0);
});

test('붙이면 쌓이고 다시 읽힌다', () => {
  appendSide('leaf-1', 'p-3', { who: 'me', text: '왜요?', ts: 1 });
  const after = appendSide('leaf-1', 'p-3', { who: 'ai', text: '이래서요', ts: 2 });
  assert.equal(after.length, 2);
  assert.deepEqual(loadSide('leaf-1', 'p-3').map((m) => m.who), ['me', 'ai']);
  assert.equal(sideCount('leaf-1', 'p-3'), 2);
});

test('논점이 다르면 따로 쌓인다', () => {
  appendSide('leaf-1', 'p-3', { who: 'me', text: 'A', ts: 1 });
  appendSide('leaf-1', 'p-4', { who: 'me', text: 'B', ts: 2 });
  assert.equal(sideCount('leaf-1', 'p-3'), 1);
  assert.equal(sideCount('leaf-1', 'p-4'), 1);
});

test('상한을 넘으면 오래된 것부터 버린다', () => {
  for (let i = 0; i < SIDE_MAX + 5; i += 1) {
    appendSide('leaf-1', 'p-3', { who: 'me', text: `m${i}`, ts: i });
  }
  const all = loadSide('leaf-1', 'p-3');
  assert.equal(all.length, SIDE_MAX);
  assert.equal(all[0].text, 'm5', '오래된 다섯이 밀려나야 한다');
});

test('지우면 비워진다', () => {
  appendSide('leaf-1', 'p-3', { who: 'me', text: 'A', ts: 1 });
  clearSide('leaf-1', 'p-3');
  assert.deepEqual(loadSide('leaf-1', 'p-3'), []);
});

test('저장소가 깨져 있어도 던지지 않는다', () => {
  localStorage.setItem(sideKey('leaf-1', 'p-3'), '{망가진 json');
  assert.deepEqual(loadSide('leaf-1', 'p-3'), []);
});
