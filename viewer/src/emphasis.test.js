import test from 'node:test';
import assert from 'node:assert/strict';
import { markEmphasis, ROLES } from './emphasis.js';

// 본문에 `=` 가 들어가는 공식도 잡아야 한다 — [^=] 로 끊으면 그런 공식이 안 잡힌다.
const hilites = (s) => [...s.matchAll(/==(공식|뒤집힘):([\s\S]+?)==/g)].map((m) => [m[1], m[2]]);
const bolds = (s) => [...s.matchAll(/\*\*([^*]+)\*\*/g)].map((m) => m[1]);

test('색은 노랑·보라 둘뿐 — 역할이 두 개다', () => {
  assert.deepEqual(ROLES, ['공식', '뒤집힘']);
});

test('뒤집히는 자리에 형광펜', () => {
  const out = markEmphasis('이것은 수익이 아니라 매입원가에서 차감합니다.');
  assert.equal(hilites(out).length, 1);
  assert.equal(hilites(out)[0][0], '뒤집힘');
});

test('공식에 형광펜', () => {
  const out = markEmphasis('취득원가 = 매입원가 + 전환원가 + 기타 원가');
  assert.equal(hilites(out).length, 1);
  assert.equal(hilites(out)[0][0], '공식');
});

test('한 말풍선에 형광펜은 하나까지 — 노랑과 보라를 섞지 않는다', () => {
  const out = markEmphasis(
    "취득원가 = 매입원가 + 전환원가. 그런데 매입할인은 수익이 아니라 차감입니다.",
  );
  assert.equal(hilites(out).length, 1);
});

test('숫자가 여럿이면 하나도 굵게 하지 않는다 — 문장이 얼룩진다', () => {
  const out = markEmphasis('하위 10%가 사회 부의 10%를 가집니다.');
  assert.equal(hilites(out).length, 0, '숫자에 형광펜이 그어졌다');
  assert.deepEqual(bolds(out), []);
});

test('숫자가 하나면 그것만 굵게', () => {
  assert.deepEqual(bolds(markEmphasis('상위 계층이 부의 40%를 가집니다.')), ['40%']);
});

test('연도는 값이 아니라 날짜라 굵게 하지 않는다', () => {
  assert.deepEqual(bolds(markEmphasis('2025년 대졸 초임을 봅시다.')), []);
});

test('한 말풍선에 강조는 통틀어 둘까지', () => {
  const out = markEmphasis(
    '수익이 아니라 차감입니다. 그래서 원가가 줄어듭니다. 비중은 30%입니다.',
  );
  assert.ok(hilites(out).length + bolds(out).length <= 2);
});

test('구보다 짧으면 형광펜을 달지 않는다', () => {
  // 따옴표 안이 네 자 미만이면 규칙 자체가 잡지 않는다.
  assert.equal(hilites(markEmphasis("'가나'는 용어입니다.")).length, 0);
});

test('「따라서」 뒤 한 마디는 굵기로만', () => {
  const out = markEmphasis('구축이 커집니다. 따라서 재정정책이 약해집니다.');
  assert.equal(hilites(out).length, 0);
  assert.ok(bolds(out).some((b) => b.startsWith('따라서')));
});

test('저자 마크업은 건드리지 않는다', () => {
  const src = '이미 **굵은** 말과 ==공식:손댄 자리== 와 $x=1$ 은 그대로.';
  const out = markEmphasis(src);
  assert.ok(out.includes('**굵은**'));
  assert.ok(out.includes('==공식:손댄 자리=='));
  assert.ok(out.includes('$x=1$'));
});

test('강조할 것이 없으면 원문 그대로', () => {
  const src = '평범한 문장입니다.';
  assert.equal(markEmphasis(src), src);
});

test('빈 값은 그대로 돌려준다', () => {
  assert.equal(markEmphasis(''), '');
  assert.equal(markEmphasis(null), null);
});
