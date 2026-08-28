// 논점 하나를 대화로 보여준다.
//
// 턴을 한 번에 하나씩 연다. 화면을 채워 놓고 스크롤하게 두면 그건 여전히 읽기다.
// quiz 턴에서는 고르기 전에 다음으로 못 간다 — "다음"만 눌러 통과할 수 있으면
// 이 화면의 존재 이유가 없다.
//
// turns 가 없는 옛 논점(body 만 있는 763개)은 기존 방식으로 폴백한다.
// 관 단위로 점진 갱신할 수 있게 하려는 것이다.
//
// onPassed 와 onNext 는 책임이 다르다: onPassed 는 isPassed 가 참이 되는 순간
// 진도만 기록한다(화면을 넘기지 않는다). onNext 는 atEnd 일 때 보이는
// 「다음 논점」 버튼이 부른다 — 셸이 다음 논점으로 넘기는 것은 사용자가
// 남은 턴(깐깐이·메이트·예시 문제)까지 다 보고 직접 눌렀을 때뿐이다.
import { useState, useEffect, useCallback } from 'react';
import { ChevronRight, MessageCircle, HelpCircle } from 'lucide-react';
import ParsedText from './ParsedText';
import { SpeakButton } from './Speech';
import {
  WHO, initTurnState, visibleTurns, canAdvance, advance, choose, isPassed, atEnd,
} from './conceptTurns';

// 색으로 구분하지 않는다. 이름·이모지·말풍선 위치로만 화자를 가른다.
const CAST = {
  [WHO.ask]:    { name: '묻는 이', emoji: '🙋', side: 'right' },
  [WHO.teach]:  { name: '선생',    emoji: '📖', side: 'left' },
  [WHO.gotcha]: { name: '깐깐이',  emoji: '🔍', side: 'left' },
  [WHO.mate]:   { name: '복습 메이트', emoji: '🐶', side: 'left' },
};

export default function ConceptScene({ point, onPassed, onNext, onAsk }) {
  const [state, setState] = useState(initTurnState);
  const [showSolution, setShowSolution] = useState(false);
  const [seenId, setSeenId] = useState(point?.id);

  // 논점이 바뀌면 처음부터. 렌더 도중 조정 — effect 로 하면 한 렌더를 더 써서
  // 이전 논점의 턴이 한 프레임 비친다(react-hooks/set-state-in-effect 도 이 경로를 문제 삼는다).
  if (point?.id !== seenId) {
    setSeenId(point?.id);
    setState(initTurnState());
    setShowSolution(false);
  }

  const passed = isPassed(point, state);
  useEffect(() => { if (passed && onPassed) onPassed(); }, [passed, onPassed]);

  const pick = useCallback((turnIndex, choiceIndex) => {
    setState((s) => choose(point, s, turnIndex, choiceIndex));
  }, [point]);

  const turns = visibleTurns(point, state);

  // 옛 논점 폴백 — turns 가 없으면 body 를 그대로 보여준다.
  if (!turns.length) {
    return (
      <article>
        <SceneHead point={point} />
        <ParsedText text={point?.body || ''} />
        {point?.check && (
          <CheckBox check={point.check} onDone={() => { onPassed?.(); onNext?.(); }} />
        )}
        {onAsk && <AskLink onAsk={onAsk} />}
      </article>
    );
  }

  return (
    <article>
      <SceneHead point={point} />

      {turns.map(({ turn, index, picked, solved, assisted }) => (
        turn.who === WHO.quiz
          ? (
            <QuizTurn key={index} turn={turn} picked={picked} solved={solved}
              assisted={assisted} onPick={(ci) => pick(index, ci)} />
          )
          : (
            <Bubble key={index} who={turn.who} text={turn.text} viz={turn.viz} />
          )
      ))}

      {point.example && (
        <section style={exampleBox}>
          <div style={boxLabel}>
            <HelpCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />예시 문제
          </div>
          <ParsedText text={point.example.q} />
          {showSolution
            ? <div style={{ marginTop: 10, paddingTop: 10, borderTop: '1px dashed #d1d5db' }}>
                <ParsedText text={point.example.solution} />
              </div>
            : <button onClick={() => setShowSolution(true)} style={ghostBtn}>풀이 보기</button>}
        </section>
      )}

      <div style={{ display: 'flex', gap: 6, alignItems: 'center', marginTop: 16 }}>
        {canAdvance(point, state) && (
          <button onClick={() => setState((s) => advance(point, s))} style={primaryBtn}>
            다음 <ChevronRight size={14} style={{ verticalAlign: -2 }} />
          </button>
        )}
        {atEnd(point, state) && (
          <span style={{ fontSize: '0.78rem', color: '#6b7280', fontWeight: 700 }}>
            {passed ? '이 논점 완료' : '정답을 확인했습니다'}
          </span>
        )}
        {atEnd(point, state) && onNext && (
          <button onClick={onNext} style={primaryBtn}>
            다음 논점 <ChevronRight size={14} style={{ verticalAlign: -2 }} />
          </button>
        )}
        {onAsk && <span style={{ marginLeft: 'auto' }}><AskLink onAsk={onAsk} /></span>}
      </div>
    </article>
  );
}

function SceneHead({ point }) {
  return (
    <header style={{ marginBottom: 14 }}>
      <h3 style={{ fontSize: '1.02rem', margin: '0 0 2px' }}>
        {point?.seq}. {point?.title}
      </h3>
      <p style={{ color: '#6b7280', fontSize: '0.83rem', margin: 0 }}>{point?.gist}</p>
      {point?.source === 'textbook' && (
        <span style={{ fontSize: '0.7rem', color: '#9ca3af', fontWeight: 700 }}>교재 기반</span>
      )}
    </header>
  );
}

function Bubble({ who, text, viz }) {
  const c = CAST[who] || CAST[WHO.teach];
  const right = c.side === 'right';
  return (
    <div style={{ display: 'flex', justifyContent: right ? 'flex-end' : 'flex-start', marginBottom: 12 }}>
      <div style={{ maxWidth: '92%' }}>
        <div style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700, marginBottom: 3,
          textAlign: right ? 'right' : 'left' }}>
          {c.emoji} {c.name}
        </div>
        <div style={{
          background: right ? '#f3f4f6' : '#fafafa',
          border: '1px solid #e5e7eb', borderRadius: 10, padding: '10px 12px',
        }}>
          <ParsedText text={text} />
          {viz && (
            <ParsedText text={'```viz ' + viz.template + '\n'
              + JSON.stringify({ ...viz.params, steps: viz.steps }, null, 1) + '\n```'} />
          )}
          <SpeakButton text={text} />
        </div>
      </div>
    </div>
  );
}

function QuizTurn({ turn, picked, solved, assisted, onPick }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700, marginBottom: 3 }}>
        {CAST[WHO.teach].emoji} {CAST[WHO.teach].name}
      </div>
      <div style={{ background: '#fafafa', border: '1px solid #e5e7eb', borderRadius: 10, padding: '10px 12px' }}>
        <ParsedText text={turn.prompt} />
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 10 }}>
          {(turn.choices || []).map((c, i) => {
            const chosen = picked.includes(i);
            const reveal = solved && c.ok;
            return (
              <button key={i} onClick={() => onPick(i)} disabled={solved || chosen}
                style={{
                  padding: '7px 12px', borderRadius: 7, cursor: solved || chosen ? 'default' : 'pointer',
                  fontSize: '0.82rem', fontWeight: 700,
                  border: reveal ? '1.5px solid #374151' : '1px solid #d1d5db',
                  background: reveal ? '#374151' : chosen ? '#f3f4f6' : '#fff',
                  color: reveal ? '#fff' : chosen ? '#9ca3af' : '#374151',
                }}>{c.text}</button>
            );
          })}
        </div>
      </div>

      {/* 고른 오답마다 그 오답 전용 반박이 붙는다. "틀렸습니다" 가 아니다. */}
      {picked.filter((i) => !(turn.choices || [])[i]?.ok).map((i) => (
        <div key={'w' + i} style={{ marginTop: 8 }}>
          <Bubble who={(turn.choices[i].who) || WHO.gotcha} text={turn.choices[i].reply} />
        </div>
      ))}
      {solved && !assisted && (turn.choices || []).some((c) => c.ok) && (
        <div style={{ marginTop: 8 }}>
          <Bubble who={WHO.teach} text={(turn.choices.find((c) => c.ok) || {}).reply || ''} />
        </div>
      )}
      {assisted && (
        <div style={{ marginTop: 8 }}>
          <Bubble who={WHO.teach}
            text={'정답은 「' + ((turn.choices || []).find((c) => c.ok) || {}).text + '」예요. '
              + (((turn.choices || []).find((c) => c.ok) || {}).reply || '')} />
        </div>
      )}
    </div>
  );
}

function CheckBox({ check, onDone }) {
  const [open, setOpen] = useState(false);
  return (
    <section style={exampleBox}>
      <div style={boxLabel}>
        <HelpCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />확인
      </div>
      <ParsedText text={check.q} />
      {open
        ? (
          <>
            <div style={{ marginTop: 10, paddingTop: 10, borderTop: '1px dashed #d1d5db' }}>
              <ParsedText text={check.a} />
            </div>
            <button onClick={onDone} style={{ ...primaryBtn, marginTop: 12 }}>이해했어요 · 다음</button>
          </>
        )
        : <button onClick={() => setOpen(true)} style={{ ...ghostBtn, marginTop: 10 }}>답 확인</button>}
    </section>
  );
}

function AskLink({ onAsk }) {
  return (
    <button onClick={onAsk} style={linkBtn}>
      <MessageCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />이 논점 더 묻기
    </button>
  );
}

const exampleBox = {
  marginTop: 16, padding: '12px 14px',
  border: '1px solid #e5e7eb', borderRadius: 8, background: '#fafafa',
};
const boxLabel = { fontSize: '0.76rem', color: '#6b7280', fontWeight: 700, marginBottom: 6 };
const primaryBtn = {
  padding: '7px 12px', borderRadius: 7, border: 'none', cursor: 'pointer',
  background: '#374151', color: '#fff', fontSize: '0.82rem', fontWeight: 700,
};
const ghostBtn = {
  padding: '7px 12px', borderRadius: 7, border: '1px solid #d1d5db', cursor: 'pointer',
  background: '#fff', color: '#374151', fontSize: '0.82rem', fontWeight: 700,
};
const linkBtn = {
  background: 'none', border: 'none', padding: 0, cursor: 'pointer',
  color: '#4b5563', fontSize: '0.8rem', fontWeight: 700,
};
