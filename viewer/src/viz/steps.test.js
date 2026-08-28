import test from 'node:test';
import assert from 'node:assert/strict';
import { mergeStep, stepParamsList } from './steps.js';

test('mergeStep은 label을 빼고 얕게 덮어쓴다', () => {
  const base = { scenario: 'A', shifts: [], axes: { x_label: 'Q' } };
  const out = mergeStep(base, { label: '2단계', shifts: [{ curve: 'D' }] });
  assert.equal(out.label, undefined);
  assert.equal(out.scenario, 'A');
  assert.deepEqual(out.shifts, [{ curve: 'D' }]);
  assert.deepEqual(out.axes, { x_label: 'Q' });
});

test('mergeStep은 base를 변형하지 않는다', () => {
  const base = { shifts: [] };
  mergeStep(base, { shifts: [{ curve: 'S' }] });
  assert.deepEqual(base.shifts, []);
});

test('steps가 없으면 단일 항목', () => {
  const p = { scenario: 'A' };
  assert.deepEqual(stepParamsList(p), [{ scenario: 'A' }]);
});

test('steps는 순서대로 병합된다', () => {
  const p = {
    scenario: 'A',
    steps: [{ label: '1', shifts: [] }, { label: '2', shifts: [{ curve: 'D' }] }],
  };
  const list = stepParamsList(p);
  assert.equal(list.length, 2);
  assert.equal(list[0].scenario, 'A');
  assert.deepEqual(list[1].shifts, [{ curve: 'D' }]);
  assert.equal(list[1].steps, undefined);
});

test('steps가 빈 배열이면 단일 항목으로 폴백', () => {
  assert.deepEqual(stepParamsList({ scenario: 'A', steps: [] }), [{ scenario: 'A' }]);
});
