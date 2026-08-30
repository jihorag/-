import { test } from 'node:test';
import assert from 'node:assert/strict';
import { markEmphasis } from './emphasis.js';

test('따옴표로 묶인 용어에 이름 형광펜', () => {
  assert.equal(
    markEmphasis("이때 '이자율 목표제'를 시행한다."),
    "이때 ==이름:'이자율 목표제'==를 시행한다.",
  );
});

test('「~가 아니라」는 뒤집힘', () => {
  const out = markEmphasis('수요는 수량이 아니라 의도다.');
  assert.match(out, /==뒤집힘:수량이 아니라==/);
});

test('숫자와 단위는 수치', () => {
  assert.match(markEmphasis('연봉이 3천만 원에서 5% 올랐다.'), /==수치:5%==/);
});

test('결론 접속어는 뒤따르는 한 마디까지 칠한다', () => {
  const out = markEmphasis('충격을 흡수한다. 따라서 이자율이 안정된다.');
  assert.match(out, /==결론:따라서 이자율이 안정된다==/);
});

test('저자가 넣은 마크업은 건드리지 않는다', () => {
  const src = "**'핵심'**과 ==이미 그은 곳== 그리고 $x = 5%$";
  assert.equal(markEmphasis(src), src);
});

test('역할별 개수 상한을 넘지 않는다', () => {
  const src = "'수요' '공급' '균형' '탄력' 을 본다";
  const n = (markEmphasis(src).match(/==이름:/g) || []).length;
  assert.equal(n, 2);
});

test('겹치는 자리에는 두 번 긋지 않는다', () => {
  const out = markEmphasis("'수요량'이 아니라 의도다.");
  const marks = out.match(/==[^:]+:/g) || [];
  assert.equal(marks.length, 1);
});

test('빈 값은 그대로', () => {
  assert.equal(markEmphasis(''), '');
  assert.equal(markEmphasis(null), null);
});
