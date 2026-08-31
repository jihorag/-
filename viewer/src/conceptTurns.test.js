import test from 'node:test';
import assert from 'node:assert/strict';
import {
  WHO, initTurnState, visibleTurns, canAdvance, advance, choose, isPassed, atEnd, passDetail, retry,
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

// ── passDetail — 측정 계약에 넘길 상세 (스펙 §1-2)

test('passDetail — 아직 안 풀었으면 done 이 아니다', () => {
  const s = initTurnState();
  const d = passDetail(POINT, s);
  assert.equal(d.quizCount, 1);
  assert.equal(d.done, false);
});

test('passDetail — 스스로 맞히면 score 1, 도움 없음', () => {
  let s = initTurnState();
  s = advance(POINT, s); s = advance(POINT, s);   // quiz 턴까지
  s = choose(POINT, s, 2, 0);                      // 정답
  const d = passDetail(POINT, s);
  assert.equal(d.done, true);
  assert.equal(d.score, 1);
  assert.equal(d.assistedCount, 0);
  assert.equal(d.tries, 1);
});

test('passDetail — 두 번 틀려 답을 연 경우도 done 이다. 지금은 이 시도가 통째로 사라진다', () => {
  let s = initTurnState();
  s = advance(POINT, s); s = advance(POINT, s);
  s = choose(POINT, s, 2, 1);                      // 오답
  s = choose(POINT, s, 2, 2);                      // 오답 → 열어 줌(assisted)
  const d = passDetail(POINT, s);
  assert.equal(d.done, true);
  assert.equal(d.score, 0);                        // 스스로 맞힌 게 없다
  assert.equal(d.assistedCount, 1);
  assert.equal(d.tries, 2);
});

test('passDetail — quiz 가 없는 옛 논점은 채점 결과가 없다', () => {
  const bare = { id: 'p0', turns: [{ who: 'teach', text: '설명만' }] };
  const d = passDetail(bare, initTurnState());
  assert.equal(d.quizCount, 0);
  assert.equal(d.done, false);
  assert.equal(d.score, null);
});

// ── 다시 풀어보기 — 시안의 「다시 풀어보기」 ────────────────────────────────
// 지키려는 것 하나: 도움받아 푼 것을 다시 눌러 「스스로 맞힘」으로 바꿀 수 없어야 한다.

const toQuiz = () => advance(POINT, advance(POINT, initTurnState()));

test('retry — 고른 것을 지우고 다시 고를 수 있다', () => {
  let s = choose(POINT, toQuiz(), 2, 0);       // 스스로 정답
  assert.equal(visibleTurns(POINT, s)[2].solved, true);
  s = retry(POINT, s, 2);
  assert.deepEqual(visibleTurns(POINT, s)[2].picked, []);
  assert.equal(visibleTurns(POINT, s)[2].solved, false);
  assert.equal(canAdvance(POINT, s), false);   // 다시 풀기 전에는 못 넘어간다
});

test('retry — 스스로 맞힌 것을 다시 풀어도 통과는 유지된다', () => {
  let s = choose(POINT, toQuiz(), 2, 0);
  s = retry(POINT, s, 2);
  s = choose(POINT, s, 2, 0);
  assert.equal(isPassed(POINT, s), true);
  assert.equal(passDetail(POINT, s).selfCount, 1);
});

test('retry — 도움받은 이력은 다시 풀어도 지워지지 않는다', () => {
  let s = toQuiz();
  s = choose(POINT, s, 2, 1);                  // 오답
  s = choose(POINT, s, 2, 2);                  // 두 번째 오답 → 답이 열린다
  assert.equal(visibleTurns(POINT, s)[2].assisted, true);

  s = retry(POINT, s, 2);
  assert.equal(visibleTurns(POINT, s)[2].everAssisted, true);
  s = choose(POINT, s, 2, 0);                  // 이제 정답을 골라도
  assert.equal(isPassed(POINT, s), false);     // 통과로 바뀌지 않는다
  assert.equal(passDetail(POINT, s).assistedCount, 1);
  assert.equal(passDetail(POINT, s).selfCount, 0);
});

test('retry — 아직 안 푼 턴이나 quiz 가 아닌 턴에는 아무 일도 없다', () => {
  const s = toQuiz();
  assert.equal(retry(POINT, s, 2), s);         // 아직 안 풂
  assert.equal(retry(POINT, s, 1), s);         // quiz 가 아님
});

// ── OX 턴 — 지문 하나를 O/X 로 묻는다 ──────────────────────────────
const OX_POINT = {
  id: 'ox1',
  turns: [
    { who: 'teach', text: '취득원가는 셋의 합입니다.' },
    { who: 'ox', prompt: '「매입할인은 수익으로 잡는다」', answer: false, reply: '차감합니다.' },
    { who: 'mate', text: '이 자리는 자주 뒤집힙니다.' },
  ],
};

test('OX 도 quiz 처럼 풀어야 넘어간다', () => {
  let s = advance(OX_POINT, initTurnState());     // ox 턴으로
  assert.equal(canAdvance(OX_POINT, s), false);
  s = choose(OX_POINT, s, 1, 1);                  // 1 = X (오답 아님: answer=false 니 X 가 정답)
  assert.equal(canAdvance(OX_POINT, s), true);
});

test('OX 를 맞히면 통과다', () => {
  let s = advance(OX_POINT, initTurnState());
  s = choose(OX_POINT, s, 1, 1);
  s = advance(OX_POINT, s);
  assert.equal(isPassed(OX_POINT, s), true);
});

test('OX 를 틀리면 한 번에 답이 열리고 도움받은 것으로 남는다', () => {
  let s = advance(OX_POINT, initTurnState());
  s = choose(OX_POINT, s, 1, 0);                  // 0 = O (틀림)
  const a = visibleTurns(OX_POINT, s)[1];
  assert.equal(a.solved, true, 'OX 는 두 번 고를 것이 없다 — 한 번에 열린다');
  assert.equal(a.assisted, true);
  assert.equal(isPassed(OX_POINT, advance(OX_POINT, s)), false);
});
