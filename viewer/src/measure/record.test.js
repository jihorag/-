import test from 'node:test';
import assert from 'node:assert/strict';
import { validate, prune, normalize, pathFromLeafId, MAX_PER_UNIT } from './record.js';

const ok = {
  id: 'q1', leaf: 'L1', subject: 'economics', stage: 1,
  axis: 'knowledge', f: 'recog', g: 'machine', src: 'official',
  correct: true, ts: 1000,
};

// ── 검증
test('제대로 된 레코드는 위반이 없다', () => {
  assert.deepEqual(validate(ok), []);
});

test('f 를 빠뜨리면 잡는다', () => {
  const v = validate({ ...ok, f: undefined });
  assert.ok(v.some((m) => m.includes('f')));
});

test('g 를 빠뜨리면 잡는다', () => {
  assert.ok(validate({ ...ok, g: undefined }).some((m) => m.includes('g')));
});

test('axis 를 빠뜨리면 잡는다 — 실력과 수행을 섞지 않기 위해 필수다', () => {
  assert.ok(validate({ ...ok, axis: undefined }).some((m) => m.includes('axis')));
});

test('모르는 f 값을 잡는다', () => {
  assert.ok(validate({ ...ok, f: 'guess' }).length > 0);
});

test('모르는 axis 값을 잡는다', () => {
  assert.ok(validate({ ...ok, axis: 'vibes' }).length > 0);
});

test('leaf 가 없으면 어디의 실력인지 알 수 없다', () => {
  assert.ok(validate({ ...ok, leaf: '' }).some((m) => m.includes('leaf')));
});

test('correct 도 score 도 없으면 채점 결과가 없는 것이다', () => {
  const v = validate({ ...ok, correct: undefined, score: undefined });
  assert.ok(v.some((m) => m.includes('score')));
});

test('g:none 은 채점 결과가 없어도 된다 — 무채점이 그 뜻이다', () => {
  assert.deepEqual(validate({ ...ok, g: 'none', correct: undefined }), []);
});

test('score 가 0~1 범위를 벗어나면 잡는다', () => {
  assert.ok(validate({ ...ok, correct: undefined, score: 85 }).length > 0);
});

test('recog 인데 nopt 가 없으면 경고로 남긴다', () => {
  const v = validate({ ...ok, nopt: undefined });
  assert.ok(v.length === 0, '경고는 위반이 아니다');
});

// ── 정규화
test('correct 를 score 로 흡수한다 — 1차와 2차가 같은 식을 쓰게 된다', () => {
  assert.equal(normalize({ ...ok, correct: true }, []).score, 1);
  assert.equal(normalize({ ...ok, correct: false }, []).score, 0);
});

test('처음 보는 채점 단위는 rep 1', () => {
  assert.equal(normalize(ok, []).rep, 1);
});

test('같은 채점 단위를 다시 풀면 rep 이 오르고 prevTs 가 붙는다', () => {
  const first = normalize(ok, []);
  const second = normalize({ ...ok, ts: 5000 }, [first]);
  assert.equal(second.rep, 2);
  assert.equal(second.prevTs, 1000);
});

test('다른 채점 단위는 rep 을 공유하지 않는다', () => {
  const first = normalize(ok, []);
  const other = normalize({ ...ok, id: 'q2', ts: 5000 }, [first]);
  assert.equal(other.rep, 1);
});

test('parent 를 안 주면 자기 id 를 쓴다', () => {
  assert.equal(normalize(ok, []).parent, 'q1');
});

test('계약 버전을 찍는다', () => {
  assert.equal(normalize(ok, []).v, 1);
});

test('rev 를 주면 레코드에 붙는다', () => {
  assert.equal(normalize(ok, [], 'build-2026-08-31').rev, 'build-2026-08-31');
});

test('rev 를 안 주면 붙이지 않는다 — 판을 모르는 기록이라는 뜻이다', () => {
  assert.equal('rev' in normalize(ok, []), false);
});

test('레코드가 자기 rev 를 들고 오면 그것을 쓴다', () => {
  assert.equal(normalize({ ...ok, rev: '내가정한판' }, [], 'build-2026-08-31').rev, '내가정한판');
});

// ── 가지치기
test('채점 단위마다 최신 N개만 남긴다', () => {
  const many = Array.from({ length: 12 }, (_, i) => ({ ...ok, ts: i, rep: i + 1 }));
  const kept = prune(many, 5);
  assert.equal(kept.length, 5);
  assert.deepEqual(kept.map((r) => r.ts), [7, 8, 9, 10, 11]);
});

test('가지치기는 채점 단위별로 따로 센다', () => {
  const a = Array.from({ length: 8 }, (_, i) => ({ ...ok, id: 'a', ts: i }));
  const b = Array.from({ length: 8 }, (_, i) => ({ ...ok, id: 'b', ts: 100 + i }));
  const kept = prune([...a, ...b], 5);
  assert.equal(kept.length, 10);
});

test('가지치기 뒤에도 시간 순서가 유지된다', () => {
  const mixed = [{ ...ok, ts: 30 }, { ...ok, id: 'b', ts: 10 }, { ...ok, ts: 20 }];
  const kept = prune(mixed, 5);
  assert.deepEqual(kept.map((r) => r.ts), [10, 20, 30]);
});

test('기본 보관 수는 5 — 반복 감쇠가 그 뒤로는 0.13 이하라 값이 거의 없다', () => {
  assert.equal(MAX_PER_UNIT, 5);
});

// ── leaf id → 계층 경로
test('leaf id 를 계층 경로로 쪼갠다 — 1차는 5단', () => {
  assert.deepEqual(
    pathFromLeafId('economics__거시경제학__제1장_국민소득__제2절_측정__제2관_GDP'),
    ['economics', '거시경제학', '제1장_국민소득', '제2절_측정', '제2관_GDP'],
  );
});

test('2차는 더 얕다 — 깊이에 상관없이 같은 함수를 쓴다', () => {
  assert.deepEqual(pathFromLeafId('appraisal_practice__1__1-1'), ['appraisal_practice', '1', '1-1']);
});

test('빈 값은 빈 경로', () => {
  assert.deepEqual(pathFromLeafId(''), []);
  assert.deepEqual(pathFromLeafId(undefined), []);
});
