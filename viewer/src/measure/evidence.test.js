import test from 'node:test';
import assert from 'node:assert/strict';
import { guessAdj, sourceAdj, repeatFactor, decayFactor, effectiveWeight } from './evidence.js';

const near = (a, b, eps = 1e-6) => assert.ok(Math.abs(a - b) < eps, `${a} != ${b}`);

// ── 찍기 하한 보정 (§4-4)
test('5지선다를 1.0 으로 정규화한다', () => {
  near(guessAdj('recog', 5), 1.0);
});

test('OX 는 찍기 하한이 50% 라 크게 깎인다', () => {
  near(guessAdj('recog', 2), 0.625);
});

test('4지선다', () => {
  near(guessAdj('recog', 4), 0.9375);
});

test('선택지 수를 모르면 깎지 않는다', () => {
  near(guessAdj('recog', undefined), 1.0);
});

test('선택지가 없는 형식은 찍기 보정을 하지 않는다', () => {
  near(guessAdj('produce', 2), 1.0);
  near(guessAdj('write', 2), 1.0);
  near(guessAdj('recall', 2), 1.0);
});

// ── 출처 (§4-5)
test('모르는 출처는 자체제작만큼 보수적으로 본다', () => {
  near(sourceAdj('없는출처'), 0.5);
});

// ── 반복 감쇠 (§4-6)
test('처음 푸는 문항은 감쇠하지 않는다', () => {
  near(repeatFactor(1, 0, 'recog'), 1.0);
});

test('방금 또 푼 2회차는 0.6', () => {
  near(repeatFactor(2, 0, 'recog'), 0.6);
});

test('간격이 아주 길면 반복이어도 완전히 회복한다', () => {
  assert.ok(repeatFactor(2, 3650, 'recog') > 0.999);
});

test('회차가 쌓일수록 즉시 재응답의 값은 급격히 떨어진다', () => {
  assert.ok(repeatFactor(5, 0, 'recog') < 0.14);
  assert.ok(repeatFactor(5, 0, 'recog') < repeatFactor(3, 0, 'recog'));
});

test('rep 이 없거나 0이면 1회차로 본다', () => {
  near(repeatFactor(0, 0, 'recog'), 1.0);
  near(repeatFactor(undefined, 0, 'recog'), 1.0);
});

// ── 시간 감쇠 (§4-7)
test('방금 한 응답은 감쇠하지 않는다', () => {
  near(decayFactor(0, 'produce', 'machine'), 1.0);
});

test('자기채점은 같은 기간에 더 많이 감쇠한다', () => {
  assert.ok(decayFactor(30, 'recall', 'self') < decayFactor(30, 'recall', 'machine'));
});

test('무거운 형식일수록 천천히 감쇠한다', () => {
  assert.ok(decayFactor(60, 'produce', 'machine') > decayFactor(60, 'recog', 'machine'));
});

// ── 합성 (§4-2)
test('처음 푼 기출 객관식의 유효 무게는 1.0', () => {
  const now = 1_700_000_000_000;
  const rec = { f: 'recog', g: 'machine', nopt: 5, src: 'official', rep: 1, ts: now };
  near(effectiveWeight(rec, now), 1.0);
});

test('자체제작 OX 를 세 번째 즉시 다시 푼 것은 거의 증거가 되지 않는다', () => {
  const now = 1_700_000_000_000;
  const rec = {
    f: 'recog', g: 'self', nopt: 2, src: 'practice',
    rep: 3, ts: now, prevTs: now,
  };
  assert.ok(effectiveWeight(rec, now) < 0.05);
});

test('존재할 수 없는 조합은 무게 0', () => {
  const now = 1_700_000_000_000;
  near(effectiveWeight({ f: 'write', g: 'machine', src: 'official', rep: 1, ts: now }, now), 0);
});

test('채점하지 않은 활동은 무게 0', () => {
  const now = 1_700_000_000_000;
  near(effectiveWeight({ f: 'recall', g: 'none', src: 'internal', rep: 1, ts: now }, now), 0);
});

test('간격을 모르는 반복은 페널티를 면제하지 않는다 — 즉시 재응답과 같게 본다', () => {
  const now = 1_700_000_000_000;
  const rec = { f: 'recog', g: 'machine', nopt: 5, src: 'official', rep: 3, ts: now };
  const same = { ...rec, prevTs: now };
  near(effectiveWeight(rec, now), effectiveWeight(same, now));
});

test('rep 이 1이면 prevTs 가 없어도 무게가 온전하다', () => {
  const now = 1_700_000_000_000;
  const rec = { f: 'recog', g: 'machine', nopt: 5, src: 'official', rep: 1, ts: now };
  near(effectiveWeight(rec, now), 1.0);
});
