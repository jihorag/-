import test from 'node:test';
import assert from 'node:assert/strict';
import {
  WHO, initTurnState, visibleTurns, canAdvance, advance, choose, isPassed, atEnd,
} from './conceptTurns.js';

// 대사 5턴 중 3번째가 quiz — 정답은 0번 선택지.
const POINT = {
  id: 'p1',
  turns: [
    { who: 'ask', text: '이거 왜 배워요?' },
    { who: 'teach', text: '쉽게 말하면…' },
    { who: 'quiz', prompt: '가격이 오르면 공급량은?', choices: [
      { text: '늘어난다', ok: true, reply: '맞아요.' },
      { text: '줄어든다', ok: false, who: 'gotcha', reply: '그건 사는 쪽 얘기예요.' },
      { text: '안 변한다', ok: false, who: 'gotcha', reply: '그건 아주 특수한 경우예요.' },
    ] },
    { who: 'gotcha', text: '공급량 변화와 공급 변화는 다릅니다.' },
    { who: 'mate', text: '이 절은 그 구분 하나만 외우면 됩니다.' },
  ],
};

test('처음에는 첫 턴 하나만 보인다', () => {
  const s = initTurnState();
  assert.equal(visibleTurns(POINT, s).length, 1);
  assert.equal(visibleTurns(POINT, s)[0].turn.who, WHO.ask);
});

test('quiz 가 아닌 턴은 그냥 넘어간다', () => {
  let s = initTurnState();
  assert.equal(canAdvance(POINT, s), true);
  s = advance(POINT, s);
  assert.equal(visibleTurns(POINT, s).length, 2);
});

test('quiz 턴에서는 고르기 전에 못 넘어간다', () => {
  let s = advance(POINT, advance(POINT, initTurnState())); // cursor=2 (quiz)
  assert.equal(canAdvance(POINT, s), false);
});

test('정답을 고르면 넘어갈 수 있다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 0);
  assert.equal(canAdvance(POINT, s), true);
  assert.equal(visibleTurns(POINT, s)[2].solved, true);
  assert.equal(visibleTurns(POINT, s)[2].assisted, false);
});

test('오답 한 번은 기록되지만 여전히 못 넘어간다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 1);
  assert.equal(canAdvance(POINT, s), false);
  assert.deepEqual(visibleTurns(POINT, s)[2].picked, [1]);
  assert.equal(visibleTurns(POINT, s)[2].solved, false);
});

test('두 번 틀리면 정답을 알려주고 넘어가게 한다 — 막히면 학습이 멈춘다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 1);
  s = choose(POINT, s, 2, 2);
  const v = visibleTurns(POINT, s)[2];
  assert.equal(v.solved, true);
  assert.equal(v.assisted, true);       // 도움받아 넘어간 것을 기록한다
  assert.equal(canAdvance(POINT, s), true);
});

test('같은 오답을 다시 골라도 시도 수가 늘지 않는다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 1);
  s = choose(POINT, s, 2, 1);
  assert.deepEqual(visibleTurns(POINT, s)[2].picked, [1]);
  assert.equal(visibleTurns(POINT, s)[2].solved, false);
});

test('정답을 맞힌 뒤에는 선택이 바뀌지 않는다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 0);
  s = choose(POINT, s, 2, 1);
  assert.equal(visibleTurns(POINT, s)[2].solved, true);
  assert.equal(visibleTurns(POINT, s)[2].assisted, false);
});

test('마지막 턴에서 atEnd 가 참이고 더 못 넘어간다', () => {
  let s = initTurnState();
  s = advance(POINT, s); s = advance(POINT, s);
  s = choose(POINT, s, 2, 0);
  s = advance(POINT, s); s = advance(POINT, s);
  assert.equal(atEnd(POINT, s), true);
  assert.equal(canAdvance(POINT, s), false);
});

test('quiz 를 스스로 맞히면 통과', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 0);
  assert.equal(isPassed(POINT, s), true);
});

test('도움받아 넘어간 것은 통과가 아니다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 1);
  s = choose(POINT, s, 2, 2);
  assert.equal(isPassed(POINT, s), false);
});

test('quiz 가 없는 논점은 끝까지 가면 통과 — 옛 데이터 폴백', () => {
  const old = { id: 'p0', turns: [{ who: 'teach', text: 'a' }, { who: 'mate', text: 'b' }] };
  let s = initTurnState();
  assert.equal(isPassed(old, s), false);
  s = advance(old, s);
  assert.equal(atEnd(old, s), true);
  assert.equal(isPassed(old, s), true);
});

test('turns 가 없는 옛 논점은 빈 배열을 돌려주고 터지지 않는다', () => {
  const legacy = { id: 'p9', body: '옛 교재체 서술' };
  const s = initTurnState();
  assert.deepEqual(visibleTurns(legacy, s), []);
  assert.equal(atEnd(legacy, s), true);
  assert.equal(canAdvance(legacy, s), false);
});
