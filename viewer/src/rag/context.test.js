import test from 'node:test';
import assert from 'node:assert/strict';
import { buildContext, BUDGET } from './context.js';

const chunk = (id, text) => ({ id, path: ['제3절', '취득원가'], text, terms: ['취득원가', '취득'] });

test('예산 상한이 스펙 값과 같다', () => {
  assert.deepEqual(BUDGET, { chunks: 3000, points: 600, record: 800, lecture: 800 });
});

test('찾은 청크를 본문에 넣고 출처를 돌려준다', () => {
  const r = buildContext({
    question: '취득원가가 뭐죠?',
    chunks: [chunk('G01#1', '취득원가는 매입원가와 전환원가의 합이다')],
  });
  assert.ok(r.text.includes('매입원가와 전환원가'));
  assert.equal(r.cited.length, 1);
  assert.equal(r.cited[0].id, 'G01#1');
});

test('청크 예산을 넘기지 않는다', () => {
  const big = Array.from({ length: 20 }, (_, i) => chunk(`G01#${i}`, '취득원가 '.repeat(200)));
  const r = buildContext({ question: '취득원가', chunks: big });
  const body = r.text.split('[교재]')[1] || '';
  assert.ok(body.length <= BUDGET.chunks + 400, `교재 블록이 예산을 넘었다: ${body.length}`);
});

test('찾은 것이 없으면 그렇게 적는다 — 지어내지 않게', () => {
  const r = buildContext({ question: '점심 메뉴' });
  assert.ok(r.text.includes('교재에서 찾지 못했다'));
  assert.deepEqual(r.cited, []);
});

test('논점·학습 기록·강의 필기도 각자 상한을 지킨다', () => {
  const r = buildContext({
    question: '취득원가',
    chunks: [],
    points: 'ㄱ'.repeat(5000),
    record: 'ㄴ'.repeat(5000),
    lecture: 'ㄷ'.repeat(5000),
  });
  assert.ok((r.text.match(/ㄱ/g) || []).length <= BUDGET.points);
  assert.ok((r.text.match(/ㄴ/g) || []).length <= BUDGET.record);
  assert.ok((r.text.match(/ㄷ/g) || []).length <= BUDGET.lecture);
});

test('빈 블록은 아예 넣지 않는다', () => {
  const r = buildContext({ question: '취득원가', chunks: [] });
  assert.ok(!r.text.includes('[학습 기록]'));
});
