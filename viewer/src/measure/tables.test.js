import test from 'node:test';
import assert from 'node:assert/strict';
import { TABLES_VERSION, HALFLIFE, SOURCE, baseWeight, capFor } from './tables.js';

test('표 버전은 1', () => {
  assert.equal(TABLES_VERSION, 1);
});

test('계산을 기계가 채점하면 가장 무겁다', () => {
  assert.equal(baseWeight('produce', 'machine'), 3.0);
});

test('서술은 기계가 채점할 수 없다 — 조합이 없으면 null', () => {
  assert.equal(baseWeight('write', 'machine'), null);
});

test('자기채점은 형식과 무관하게 가볍다', () => {
  assert.ok(baseWeight('produce', 'self') < baseWeight('recog', 'machine'));
});

test('strict 예외 — 논점 quiz는 선택지지만 2.0', () => {
  assert.equal(baseWeight('recog', 'machine'), 1.0);
  assert.equal(baseWeight('recog', 'machine', true), 2.0);
});

test('strict 예외는 recog+machine 에만 적용된다', () => {
  assert.equal(baseWeight('recog', 'self', true), 0.3);
});

test('채점하지 않은 활동은 무게 0', () => {
  assert.equal(baseWeight('recall', 'none'), 0);
});

test('상한 — 객관식만 있으면 65가 천장', () => {
  assert.equal(capFor(1.0), 65);
});

test('상한 — 무게 0이면 미측정(null)', () => {
  assert.equal(capFor(0), null);
});

test('상한은 무게에 따라 단조 증가한다', () => {
  const ws = [0.4, 0.6, 1.0, 2.0, 2.2, 2.5, 3.0];
  const caps = ws.map(capFor);
  for (let i = 1; i < caps.length; i += 1) assert.ok(caps[i] >= caps[i - 1], `${ws[i]}`);
});

test('출처 — 자체제작은 기출의 절반', () => {
  assert.equal(SOURCE.official, 1.0);
  assert.equal(SOURCE.practice, 0.5);
});

test('반감기 — 무거운 형식일수록 오래 유효하다', () => {
  assert.ok(HALFLIFE.produce > HALFLIFE.write);
  assert.ok(HALFLIFE.write > HALFLIFE.recall);
  assert.ok(HALFLIFE.recall > HALFLIFE.recog);
});
