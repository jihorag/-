// 논점 하나를 대화로 보여준다 — 「칠판이 주인공, 대사는 자막」.
//
// 층이 네 개다: 머리(ConceptTrack) · 무대 · 대사 · 조작 줄. 무대와 대사는 높이가
// 고정이라 내용이 길어져도 조작 줄이 움직이지 않는다. 예전 화면은 말풍선을 아래로
// 쌓아서 「다음」 버튼이 누를 때마다 도망갔다 — 그게 이 화면의 가장 큰 결함이었다.
//
// 대사는 한 번에 하나만 두고 교체한다. 지난 대사는 조작 줄의 「지난 대사」로 편다.
// 무대는 절대 비지 않는다: viz 가 있으면 그림, 없으면 그 논점의 gist 를 큰 활자로.
// 논점 878개 중 504개가 그림이 없으므로 이 폴백이 절반의 경험을 좌우한다.
//
// quiz 턴이 오면 선택지가 무대에 올라간다 — 스크롤 맨 끝의 곁다리가 아니다.
// 진행 규칙(언제 넘어갈 수 있는가·무엇이 통과인가)은 conceptTurns.js 가 갖는다.
//
// onPassed 와 onNext 는 책임이 다르다: onPassed 는 isPassed 가 참이 되는 순간
// 진도만 기록한다(화면을 넘기지 않는다). onNext 는 끝까지 본 뒤 사용자가 직접 누른다.
import { useState, useEffect, useRef, useMemo } from 'react';
import {
  ChevronRight, ChevronLeft, HelpCircle, BookOpen, AlertTriangle, Bookmark,
  MessageCircle, History, FlaskConical, X, RotateCcw,
} from 'lucide-react';
import ParsedText from './ParsedText';
import { SpeakButton } from './Speech';
import VizRouter from './viz/VizRouter';
import {
  WHO, initTurnState, visibleTurns, canAdvance, advance, choose, isPassed, atEnd,
} from './conceptTurns';

// 색으로 구분하지 않는다. 이름·아이콘·좌우 위치로만 화자를 가른다.
// 이모지는 쓰지 않는다 — 이 앱은 lucide 아이콘 체계라 이모지만 튄다.
const CAST = {
  [WHO.ask]:    { name: '묻는 이', Icon: HelpCircle,    side: 'right' },
  [WHO.teach]:  { name: '선생',    Icon: BookOpen,      side: 'left' },
  [WHO.gotcha]: { name: '깐깐이',  Icon: AlertTriangle, side: 'left' },
  [WHO.mate]:   { name: '복습 메이트', Icon: Bookmark,  side: 'left' },
};
const castOf = (who) => CAST[who] || CAST[WHO.teach];

const vizJson = (viz) => JSON.stringify({ ...(viz.params || {}), steps: viz.steps });

/** quiz 턴의 응답 상태 → 지금 화면에 세울 대사 한 덩이. */
function quizSay(turn, ans) {
  const choices = turn.choices || [];
  const ok = choices.find((c) => c.ok);
  if (ans.solved && !ans.assisted) return { who: WHO.teach, text: ok?.reply || '맞았습니다.' };
  if (ans.assisted) {
    return {
      who: WHO.teach,
      text: `정답은 「${ok?.text || ''}」예요. ${ok?.reply || ''}`,
    };
  }
  const wrong = ans.picked.filter((i) => !choices[i]?.ok);
  if (wrong.length) {
    const c = choices[wrong[wrong.length - 1]];
    return { who: c.who || WHO.gotcha, text: c.reply || '' };
  }
  return { who: WHO.teach, text: '생각한 답을 하나 골라 보세요.' };
}

export default function ConceptScene({ point, onPassed, onNext, onAsk }) {
  const [state, setState] = useState(initTurnState);
  const [peek, setPeek] = useState(0);        // 0 = 지금 대사, n = n칸 전 대사 다시 보기
  const [panel, setPanel] = useState(null);   // 'log' | 'example' | null

  const [seenId, setSeenId] = useState(point?.id);
  // 논점이 바뀌면 처음부터. 렌더 도중 조정 — effect 로 하면 한 렌더를 더 써서
  // 이전 논점의 턴이 한 프레임 비친다.
  if (point?.id !== seenId) {
    setSeenId(point?.id);
    setState(initTurnState());
    setPeek(0);
    setPanel(null);
  }

  const passed = isPassed(point, state);
  useEffect(() => { if (passed && onPassed) onPassed(); }, [passed, onPassed]);

  const turns = visibleTurns(point, state);
  const hasTurns = turns.length > 0;
  const dispIdx = Math.max(0, turns.length - 1 - peek);
  const cur = turns[dispIdx] || null;
  const isQuiz = cur?.turn?.who === WHO.quiz;

  const stuck = hasTurns && !canAdvance(point, state) && !atEnd(point, state);
  const finished = hasTurns && atEnd(point, state) && !stuck;

  // 수동 메모이제이션은 걸지 않는다 — turns 가 렌더마다 새로 만들어지는 배열이라
  // React Compiler 가 useCallback 을 보존하지 못한다. 컴파일러에게 맡긴다.
  const goForward = () => {
    if (peek > 0) { setPeek((p) => p - 1); return; }
    if (canAdvance(point, state)) { setState((s) => advance(point, s)); return; }
    if (atEnd(point, state)) onNext?.();
  };

  const goBack = () => {
    setPeek((p) => Math.min(Math.max(0, turns.length - 1), p + 1));
  };

  // Space·→ 로 다음, ← 로 지난 대사. 버튼에 포커스가 있으면 Space 는 그 버튼 몫이다.
  // 핸들러는 ref 로 최신값만 읽는다 — 렌더마다 리스너를 다시 걸지 않기 위해서다.
  const keys = useRef(null);
  useEffect(() => { keys.current = { goForward, goBack }; });
  useEffect(() => {
    const onKey = (e) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target;
      const tag = t?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || t?.isContentEditable) return;
      if (e.key === ' ') {
        if (tag === 'BUTTON' || tag === 'A') return;
        e.preventDefault();
        keys.current?.goForward();
      } else if (e.key === 'ArrowRight') {
        e.preventDefault(); keys.current?.goForward();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault(); keys.current?.goBack();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const pick = (choiceIndex) => {
    setState((s) => choose(point, s, dispIdx, choiceIndex));
  };

  // 그림은 한 번 올라오면 다음 턴에도 무대에 남는다. 턴마다 그림이 사라졌다
  // 나타나면 무대가 깜빡이고, 대사는 대개 그 그림을 가리키며 이어진다.
  let stickyViz = null;
  for (let i = 0; i <= dispIdx; i += 1) if (turns[i]?.turn?.viz) stickyViz = turns[i].turn.viz;

  const say = cur && (isQuiz ? quizSay(cur.turn, cur) : { who: cur.turn.who, text: cur.turn.text });
  const sayKey = cur ? `${dispIdx}:${cur.picked.length}:${cur.solved}` : 'none';

  // ── 옛 논점 폴백 — turns 가 없는 140개는 body 를 자막 자리에 그대로 편다.
  if (!hasTurns) {
    return (
      <>
        {point?.viz
          ? (
            <div className="concept-stage">
              <div className="concept-viz">
                <VizRouter name={point.viz.template} rawJson={vizJson(point.viz)} />
              </div>
            </div>
          )
          : (
            <div className="concept-stage concept-stage--doc">
              <div className="concept-gist">{point?.gist || point?.title || ''}</div>
            </div>
          )}
        <div className="concept-say concept-say--doc">
          <ParsedText text={point?.body || ''} />
          {point?.check && (
            <div className="concept-check">
              <div className="concept-panel-label">확인</div>
              <ParsedText text={point.check.q} />
              <details className="concept-details">
                <summary>답 확인</summary>
                <ParsedText text={point.check.a} />
              </details>
            </div>
          )}
        </div>
        <div className="concept-ops">
          <button type="button" className="concept-next"
            onClick={() => { onPassed?.(); onNext?.(); }}>
            이해했어요 · 다음 <ChevronRight size={15} strokeWidth={1.75} />
          </button>
          <div className="concept-ops-side">
            {onAsk && (
              <button type="button" className="concept-op" onClick={onAsk}>
                <MessageCircle size={14} strokeWidth={1.75} />더 묻기
              </button>
            )}
          </div>
        </div>
      </>
    );
  }

  const nextLabel = peek > 0 ? '돌아오기' : finished ? '다음 논점' : '다음';

  return (
    <>
      <div className="concept-stage">
        {isQuiz
          ? <QuizStage turn={cur.turn} ans={cur} onPick={pick} />
          : stickyViz
            ? (
              <div className="concept-viz" key={stickyViz.template + dispIdx}>
                <VizRouter name={stickyViz.template} rawJson={vizJson(stickyViz)} />
              </div>
            )
            : <div className="concept-gist">{point?.gist || point?.title || ''}</div>}
      </div>

      <div className="concept-say">
        <SayLine who={say.who} text={say.text} revealKey={sayKey}
          stale={peek > 0} staleNote={`지난 대사 ${dispIdx + 1}/${turns.length}`} />
      </div>

      <div className="concept-ops">
        <button type="button" className="concept-next" onClick={goForward}
          disabled={stuck && peek === 0}
          aria-keyshortcuts="Space ArrowRight">
          {nextLabel} <ChevronRight size={15} strokeWidth={1.75} />
        </button>
        <div className="concept-ops-side">
          <button type="button" className="concept-op" onClick={goBack}
            disabled={peek >= turns.length - 1} aria-label="이전 대사">
            <ChevronLeft size={14} strokeWidth={1.75} />
          </button>
          <SpeakButton text={say.text} />
          {point?.example && (
            <button type="button" className="concept-op"
              aria-pressed={panel === 'example'}
              onClick={() => setPanel((p) => (p === 'example' ? null : 'example'))}>
              <FlaskConical size={14} strokeWidth={1.75} />예시
            </button>
          )}
          <button type="button" className="concept-op"
            aria-pressed={panel === 'log'}
            onClick={() => setPanel((p) => (p === 'log' ? null : 'log'))}>
            <History size={14} strokeWidth={1.75} />지난 대사
          </button>
          {onAsk && (
            <button type="button" className="concept-op" onClick={onAsk}>
              <MessageCircle size={14} strokeWidth={1.75} />더 묻기
            </button>
          )}
        </div>
      </div>

      {panel && (
        <div className="concept-panel" role="dialog" aria-label={panel === 'log' ? '지난 대사' : '예시 문제'}>
          <div className="concept-panel-head">
            <span className="concept-panel-label">{panel === 'log' ? '지난 대사' : '예시 문제'}</span>
            <button type="button" className="concept-op" onClick={() => setPanel(null)} aria-label="닫기">
              <X size={15} strokeWidth={1.75} />
            </button>
          </div>
          <div className="concept-panel-body">
            {panel === 'log'
              ? turns.map(({ turn, index }) => (
                <LogLine key={index} turn={turn} />
              ))
              : (
                <>
                  <ParsedText text={point.example.q} />
                  <details className="concept-details">
                    <summary>풀이 보기</summary>
                    <ParsedText text={point.example.solution} />
                  </details>
                </>
              )}
          </div>
        </div>
      )}
    </>
  );
}

function SayLine({ who, text, revealKey, stale, staleNote }) {
  const c = castOf(who);
  const right = c.side === 'right';
  return (
    <div className={`concept-sayline${right ? ' is-right' : ''}`}>
      <div className="concept-who">
        <c.Icon size={14} strokeWidth={1.75} />
        <span>{c.name}</span>
        {stale && <span className="concept-stale">{staleNote}</span>}
      </div>
      <div className="concept-saytext" key={revealKey}>
        <ParsedText text={text || ''} />
      </div>
    </div>
  );
}

function LogLine({ turn }) {
  const isQuiz = turn.who === WHO.quiz;
  const c = castOf(isQuiz ? WHO.teach : turn.who);
  return (
    <div className="concept-logline">
      <div className="concept-who">
        <c.Icon size={13} strokeWidth={1.75} />
        <span>{c.name}</span>
      </div>
      <ParsedText text={isQuiz ? turn.prompt : turn.text} />
    </div>
  );
}

/** 선택지를 무대에 올린다. 데스크톱 2×2 · 모바일 세로 스택은 CSS 가 맡는다. */
function QuizStage({ turn, ans, onPick }) {
  const choices = turn.choices || [];
  return (
    <div className="concept-quiz">
      <p className="concept-prompt">{turn.prompt}</p>
      <div className="concept-choices">
        {choices.map((c, i) => {
          const chosen = ans.picked.includes(i);
          const reveal = ans.solved && c.ok;
          const cls = reveal ? ' is-right' : chosen ? ' is-wrong' : '';
          return (
            <button type="button" key={i} className={`concept-choice${cls}`}
              onClick={() => onPick(i)} disabled={ans.solved || chosen}>
              {c.text}
            </button>
          );
        })}
      </div>
    </div>
  );
}

// ── 되짚기 ──────────────────────────────────────────────────────────────
// 관을 마치면 그 관의 quiz 중 다섯을 다시 묻는다. 새 데이터를 만들지 않는다 —
// 이미 있는 quiz 턴을 재사용한다. 마지막이 곁다리로 끝나지 않게 하는 장치다.

const RECAP_MAX = 5;

/** 관 전체 quiz 를 고르게 훑어 최대 다섯 문항. 순서는 논점 순서 그대로. */
function recapQuizzes(track) {
  const all = (track?.points || []).flatMap((p) => (p.turns || [])
    .filter((t) => t.who === WHO.quiz && (t.choices || []).length)
    .map((t) => ({ turn: t, seq: p.seq, title: p.title })));
  if (all.length <= RECAP_MAX) return all;
  const stride = all.length / RECAP_MAX;
  return Array.from({ length: RECAP_MAX }, (_, i) => all[Math.floor(i * stride)]);
}

export function ConceptRecap({ track, onExit }) {
  const items = useMemo(() => recapQuizzes(track), [track]);
  const [i, setI] = useState(0);
  const [picked, setPicked] = useState([]);
  const [score, setScore] = useState({ right: 0, total: 0 });
  const [done, setDone] = useState(false);

  const item = items[i];
  const choices = item?.turn?.choices || [];
  const solved = picked.some((n) => choices[n]?.ok) || picked.length >= 2;
  const assisted = solved && !picked.some((n) => choices[n]?.ok);
  const ans = { picked, solved, assisted };

  const next = () => {
    if (!solved) return;
    setScore((s) => ({ right: s.right + (assisted ? 0 : 1), total: s.total + 1 }));
    setPicked([]);
    if (i + 1 >= items.length) setDone(true); else setI(i + 1);
  };

  const restart = () => { setI(0); setPicked([]); setScore({ right: 0, total: 0 }); setDone(false); };

  if (!items.length) {
    return (
      <>
        <div className="concept-stage">
          <div className="concept-gist">되짚을 문제가 없는 관입니다.</div>
        </div>
        <div className="concept-say" />
        <div className="concept-ops">
          <button type="button" className="concept-next" onClick={onExit}>목록으로</button>
        </div>
      </>
    );
  }

  if (done) {
    return (
      <>
        <div className="concept-stage">
          <div className="concept-gist">
            되짚기 {score.right} / {score.total}
          </div>
        </div>
        <div className="concept-say">
          <SayLine who={WHO.mate} revealKey="recap-done"
            text={score.right === score.total
              ? '전부 스스로 맞혔습니다. 이 관은 여기서 접어도 됩니다.'
              : '틀린 자리가 이 관에서 다시 볼 곳입니다. 해당 논점을 한 번 더 열어 보세요.'} />
        </div>
        <div className="concept-ops">
          <button type="button" className="concept-next" onClick={onExit}>목록으로</button>
          <div className="concept-ops-side">
            <button type="button" className="concept-op" onClick={restart}>
              <RotateCcw size={14} strokeWidth={1.75} />다시
            </button>
          </div>
        </div>
      </>
    );
  }

  const say = quizSay(item.turn, ans);
  return (
    <>
      <div className="concept-stage">
        <QuizStage turn={item.turn} ans={ans}
          onPick={(n) => setPicked((p) => (p.includes(n) || solved ? p : p.concat(n)))} />
      </div>
      <div className="concept-say">
        <SayLine who={say.who} text={say.text} revealKey={`${i}:${picked.length}:${solved}`} />
      </div>
      <div className="concept-ops">
        <button type="button" className="concept-next" onClick={next} disabled={!solved}>
          {i + 1 >= items.length ? '되짚기 마치기' : '다음'} <ChevronRight size={15} strokeWidth={1.75} />
        </button>
        <div className="concept-ops-side">
          <span className="concept-op is-static">되짚기 {i + 1} / {items.length}</span>
          <button type="button" className="concept-op" onClick={onExit}>그만하기</button>
        </div>
      </div>
    </>
  );
}
