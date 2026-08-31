import test from 'node:test';
import assert from 'node:assert/strict';
import { weakSpots, WEAK_MIN_MISS } from './weakSpots.js';

const TRACK = {
  points: [
    { id: 'p1', seq: 1, title: '취득원가의 범위' },
    { id: 'p2', seq: 2, title: '매입할인의 처리' },
    { id: 'p3', seq: 3, title: '저가법 적용 단위' },
  ],
};

test('두 번 넘게 틀린 논점만 뽑는다', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [
      { leafId: 'L', pointId: 'p2', attempted: 3, correct: 0, kind: 'ox' },
      { leafId: 'L', pointId: 'p1', attempted: 3, correct: 3, kind: 'ox' },
    ],
  });
  assert.equal(out.length, 1);
  assert.equal(out[0].pointId, 'p2');
});

test('why 가 숫자로 근거를 댄다', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [{ leafId: 'L', pointId: 'p2', attempted: 3, correct: 0, kind: 'ox' }],
  });
  assert.equal(out[0].why, '확인 문제 3회 중 3개 오답 · 논점 2');
});

test('기출 오답은 「기출」로 적는다', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [{ leafId: 'L', pointId: 'p3', attempted: 2, correct: 0, kind: 'exam' }],
  });
  assert.ok(out[0].why.startsWith('기출 2문제 중 2개 오답'));
});

test('더 많이 틀린 것이 앞', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [
      { leafId: 'L', pointId: 'p1', attempted: 3, correct: 1, kind: 'ox' },
      { leafId: 'L', pointId: 'p2', attempted: 4, correct: 0, kind: 'ox' },
    ],
  });
  assert.deepEqual(out.map((w) => w.pointId), ['p2', 'p1']);
});

test('다섯 개를 넘지 않는다', () => {
  const many = Array.from({ length: 9 }, (_, i) => ({
    leafId: 'L', pointId: `p${i}`, attempted: 3, correct: 0, kind: 'ox',
  }));
  const track = { points: many.map((m, i) => ({ id: m.pointId, seq: i + 1, title: `T${i}` })) };
  assert.equal(weakSpots({ leafId: 'L', track, items: many }).length, 5);
});

test('다른 관의 기록은 섞지 않는다', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [{ leafId: '다른관', pointId: 'p2', attempted: 3, correct: 0, kind: 'ox' }],
  });
  assert.deepEqual(out, []);
});

test('상수는 2다 — 「두 번 이상 틀린 곳」', () => {
  assert.equal(WEAK_MIN_MISS, 2);
});

test('입력이 비어도 던지지 않는다', () => {
  assert.deepEqual(weakSpots({}), []);
});
