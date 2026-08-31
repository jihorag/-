// 논점 하나를 대화로 보여준다 — 위로 쌓이는 대화, 아래에 고정된 조작부.
//
// 2026-08-31 개편(DECISIONS.md). 예전 화면은 층이 넷이었다 — 무대·대사·조작 줄이
// 각각 높이를 고정하고, 대사는 **한 번에 하나만** 두고 교체했다. 그렇게 만든 이유는
// 그전 화면이 말풍선을 쌓다가 「다음」 버튼을 화면 밖으로 밀어냈기 때문이다.
//
// Figma 시안은 같은 문제를 다르게 푼다: 대화는 쌓되 **조작부를 바닥에 고정**한다.
// 그래서 버튼은 절대 도망가지 않고, 방금 읽은 설명도 화면에 남는다. 쌓기만 가져오고
// 바닥 고정을 빼면 예전 결함이 그대로 되살아난다 — 둘은 한 몸이다.
//
// 층은 둘이다:
//   .cs-stream  — 논점 머리 + 말풍선 + 그림 카드. 넘치면 이것만 스크롤된다.
//   .cs-dock    — 선택지 · 다음 버튼 · 입력줄. 높이가 내용에 따라 변해도 바닥에 붙는다.
//
// 진행 규칙(언제 넘어갈 수 있는가·무엇이 통과인가)은 conceptTurns.js 가 갖는다.
// onPassed 와 onNext 는 책임이 다르다: onPassed 는 isPassed 가 참이 되는 순간
// 진도만 기록한다(화면을 넘기지 않는다). onNext 는 끝까지 본 뒤 사용자가 직접 누른다.
import { useState, useEffect, useRef, useMemo } from 'react';
import {
  ChevronRight, HelpCircle, BookOpen, AlertTriangle, Bookmark,
  FlaskConical, X, RotateCcw, SendHorizontal, CornerDownLeft,
} from 'lucide-react';
import ParsedText from './ParsedText';
import Avatar from './ConceptCast';
import { markEmphasis } from './emphasis';
import { SpeakButton } from './Speech';
import VizRouter from './viz/VizRouter';
import {
  WHO, initTurnState, visibleTurns, canAdvance, advance, choose, retry,
  isPassed, atEnd, passDetail, choicesOf, isChoiceTurn,
  submitRecall, gradeRecall,
} from './conceptTurns';
import { loadSide, appendSide, clearSide } from './sideThread';

// 색으로 구분하지 않는다. 이름·아이콘·좌우 위치로만 화자를 가른다.
// 이모지는 쓰지 않는다 — 이 앱은 lucide 아이콘 체계라 이모지만 튄다.
const CAST = {
  [WHO.ask]:    { name: '나',      Icon: HelpCircle,    side: 'right' },
  [WHO.teach]:  { name: '선생',    Icon: BookOpen,      side: 'left' },
  [WHO.gotcha]: { name: '깐깐이',  Icon: AlertTriangle, side: 'left' },
  [WHO.mate]:   { name: '복습 메이트', Icon: Bookmark,  side: 'left' },
};
const castOf = (who) => CAST[who] || CAST[WHO.teach];

const vizJson = (viz) => JSON.stringify({ ...(viz.params || {}), steps: viz.steps });

/** 입력줄의 슬래시 명령. 데이터로 두는 이유는 팔레트와 실행이 같은 목록을 보게 하려고. */
export const SLASH = [
  { cmd: '/이어서', desc: '중단한 논점부터 계속' },
  { cmd: '/쉽게',   desc: '방금 설명을 더 쉬운 말로' },
  { cmd: '/정리',   desc: '이 관에서 배운 것 요약' },
  { cmd: '/진단',   desc: '확인 문제로 실력 확인' },
  { cmd: '/교재',   desc: '교재 패널 열기' },
  { cmd: '/시작',   desc: '이 관 처음부터' },
];

/** quiz 턴의 응답 상태 → 그 뒤에 이어 붙일 대사 한 덩이. */
function quizSay(turn, ans) {
  const choices = choicesOf(turn);
  const ok = choices.find((c) => c.ok);
  if (ans.solved && !ans.assisted) {
    return { who: WHO.teach, text: ok?.reply || '맞았습니다.', mood: 'right' };
  }
  if (ans.assisted) {
    return {
      who: WHO.teach,
      text: `정답은 「${ok?.text || ''}」예요. ${ok?.reply || ''}`,
      mood: 'wrong',
    };
  }
  const wrong = ans.picked.filter((i) => !choices[i]?.ok);
  if (wrong.length) {
    const c = choices[wrong[wrong.length - 1]];
    return { who: c.who || WHO.gotcha, text: c.reply || '', mood: 'wrong' };
  }
  return null;   // 아직 아무것도 안 골랐으면 붙일 대사가 없다
}

export default function ConceptScene({
  point, seq, total, onPassed, onDone, onNext, onAsk, onCommand, leafId, onAskSide,
}) {
  const [state, setState] = useState(initTurnState);
  const [panel, setPanel] = useState(null);   // 'example' | null
  const [draft, setDraft] = useState('');
  // 샛길 — 트랙의 cursor 를 건드리지 않는다. 그래야 돌아갈 자리가 정확하다.
  const [side, setSide] = useState([]);
  const [asking, setAsking] = useState(false);
  useEffect(() => {
    setSide(leafId && point?.id ? loadSide(leafId, point.id) : []);
  }, [leafId, point?.id]);

  const [seenId, setSeenId] = useState(point?.id);
  // 논점이 바뀌면 처음부터. 렌더 도중 조정 — effect 로 하면 한 렌더를 더 써서
  // 이전 논점의 턴이 한 프레임 비친다.
  if (point?.id !== seenId) {
    setSeenId(point?.id);
    setState(initTurnState());
    setPanel(null);
    setDraft('');
  }

  const passed = isPassed(point, state);
  useEffect(() => { if (passed && onPassed) onPassed(); }, [passed, onPassed]);

  // 측정 계약 기록 — 통과 여부와 무관하게 "quiz 를 다 끝냈는가"가 기준이다.
  // 두 번 틀려 답을 연 경우(assisted)도 증거이므로 남긴다.
  // 논점 하나당 한 번만 부른다.
  const detail = passDetail(point, state);
  const doneRef = useRef(null);
  // useRef(Date.now()) 는 렌더 중 불순 함수 호출이라 react-hooks/purity 에러다.
  const shownAtRef = useRef(0);
  useEffect(() => {
    shownAtRef.current = Date.now();
    // 논점이 바뀌면 발화 가드도 푼다. 안 풀면 A→B→A 로 돌아와 다시 푼 것이
    // 에러 없이 기록되지 않는다 — 조용한 유실이 이 제품의 최악 결함이다.
    doneRef.current = null;
  }, [point?.id]);
  useEffect(() => {
    if (!detail.done) return;
    if (doneRef.current === point?.id) return;
    doneRef.current = point?.id;
    if (onDone) onDone({ ...detail, ms: shownAtRef.current ? Date.now() - shownAtRef.current : undefined });
  }, [detail.done, point?.id, onDone, detail]);

  const turns = visibleTurns(point, state);
  const hasTurns = turns.length > 0;
  const last = turns[turns.length - 1] || null;
  const openQuiz = last && isChoiceTurn(last.turn) ? last : null;
  const openRecall = last && last.turn.who === WHO.recall ? last : null;

  const stuck = hasTurns && !canAdvance(point, state) && !atEnd(point, state);
  const finished = hasTurns && atEnd(point, state) && !stuck;

  // 새 턴이 열리면 그 턴이 보이도록 아래로. 사용자가 위를 읽는 중이면 방해하지 않는다.
  //
  // 「따라가는 중인가」는 **스크롤할 때** 재어 둔다. 렌더 뒤에 재면 안 된다 —
  // 선택지가 바닥에 깔리는 순간 조작부가 커지고 스트림이 그만큼 줄어드는데,
  // 그 뒤에 재면 방금까지 맨 아래에 있던 사람도 「위를 읽는 중」으로 잘못 읽힌다.
  // 실제로 채점 직후의 반박 대사가 화면 밖에 남았다.
  const streamRef = useRef(null);
  const bottomRef = useRef(null);
  const following = useRef(true);
  const onStreamScroll = (e) => {
    const el = e.currentTarget;
    following.current = el.scrollHeight - el.scrollTop - el.clientHeight < 120;
  };
  useEffect(() => {
    if (following.current) bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [turns.length, openQuiz?.picked.length, openQuiz?.solved]);
  // 논점이 바뀌면 다시 따라가기 시작한다.
  useEffect(() => { following.current = true; }, [point?.id]);

  const goForward = () => {
    if (canAdvance(point, state)) { setState((s) => advance(point, s)); return; }
    if (atEnd(point, state)) onNext?.();
  };

  // Space·→ 로 다음. 버튼·입력창에 포커스가 있으면 그쪽 몫이다.
  // 핸들러는 ref 로 최신값만 읽는다 — 렌더마다 리스너를 다시 걸지 않기 위해서다.
  const keys = useRef(null);
  useEffect(() => { keys.current = { goForward }; });
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
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const pick = (choiceIndex) => {
    if (!openQuiz) return;
    setState((s) => choose(point, s, openQuiz.index, choiceIndex));
  };
  const again = () => {
    if (!openQuiz) return;
    setState((s) => retry(point, s, openQuiz.index));
  };

  // 끼어들어 묻기. 답이 오든 안 오든 트랙은 그대로다.
  const askSide = async (text) => {
    if (!leafId || !point?.id) return;
    const mine = { who: 'me', text, ts: Date.now() };
    setSide(appendSide(leafId, point.id, mine));
    if (!onAskSide) {
      setSide(appendSide(leafId, point.id, {
        who: 'ai', ts: Date.now(),
        text: '물어보려면 API 키가 필요합니다. 설정에서 키를 넣어 주세요. 키 없이도 논점 대화와 기출 풀이는 끝까지 진행됩니다.',
      }));
      return;
    }
    setAsking(true);
    try {
      const answer = await onAskSide(text, { point, turns });
      setSide(appendSide(leafId, point.id, { who: 'ai', text: answer, ts: Date.now() }));
    } catch (e) {
      setSide(appendSide(leafId, point.id, {
        who: 'ai', ts: Date.now(),
        text: `답을 가져오지 못했습니다. ${e?.message || ''}`.trim(),
      }));
    } finally {
      setAsking(false);
    }
  };

  const head = (
    <div className="cs-pointhead">
      <span className="cs-pointhead-label">
        {seq ? `논점 ${seq}${total ? ` / ${total}` : ''} · ` : ''}{point?.title || ''}
      </span>
    </div>
  );

  const inputRow = (
    <SlashInput
      value={draft} onChange={setDraft}
      onRun={(cmd) => { setDraft(''); onCommand?.(cmd); }}
      onSend={(text) => { setDraft(''); askSide(text); }}
      canAsk
    />
  );

  // ── 옛 논점 폴백 — turns 가 없는 논점은 body 를 그대로 편다. ──────────────
  if (!hasTurns) {
    return (
      <div className="cs-room">
        <div className="cs-stream" ref={streamRef} onScroll={onStreamScroll}>
          {head}
          {point?.viz && (
            <FigureCard viz={point.viz}>
              <VizRouter name={point.viz.template} rawJson={vizJson(point.viz)} />
            </FigureCard>
          )}
          <div className="cs-doc">
            <ParsedText text={markEmphasis(point?.body || point?.gist || point?.title || '')} />
            {point?.check && (
              <div className="cs-check">
                <div className="cs-check-label">확인</div>
                <ParsedText text={point.check.q} />
                <details className="cs-details">
                  <summary>답 확인</summary>
                  <ParsedText text={point.check.a} />
                </details>
              </div>
            )}
          </div>
          <div ref={bottomRef} />
        </div>
        <div className="cs-dock">
          <button type="button" className="cs-primary"
            onClick={() => { onPassed?.(); onNext?.(); }}>
            이해했어요 · 다음 <ChevronRight size={16} strokeWidth={1.75} />
          </button>
          {inputRow}
        </div>
      </div>
    );
  }

  const nextLabel = finished ? '다음 논점' : '다음';

  return (
    <div className="cs-room">
      <div className="cs-stream" ref={streamRef} onScroll={onStreamScroll}>
        {head}
        <Stream turns={turns} />
        {side.length > 0 && (
          <div className="cs-side">
            {side.map((m, i) => (
              <Bubble key={i} who={m.who === 'me' ? WHO.ask : WHO.teach}
                text={m.text} sideTag={m.who === 'ai'} />
            ))}
            {asking && <p className="cs-side-note">답을 가져오는 중…</p>}
            <button type="button" className="cs-side-back"
              onClick={() => { clearSide(leafId, point.id); setSide([]); }}>
              <CornerDownLeft size={14} strokeWidth={1.75} />돌아가기
            </button>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="cs-dock">
        {openQuiz
          ? (
            <ChoiceDock item={openQuiz} onPick={pick} onAgain={again}
              onNext={goForward} nextLabel={nextLabel} />
          )
          : openRecall
            ? (
              <RecallDock key={openRecall.index} item={openRecall}
                onSubmit={(t) => setState((s) => submitRecall(point, s, openRecall.index, t))}
                onGrade={(v) => setState((s) => gradeRecall(point, s, openRecall.index, v))}
                onNext={goForward} nextLabel={nextLabel} />
            )
            : (
              // 시안은 파란 면 버튼을 「다시 풀어보기」·「이 관 문제 풀기」 같은 매듭에만
              // 쓴다. 매 턴 넘기는 버튼까지 파랗게 하면 그 무게가 사라진다.
              <button type="button"
                className={finished ? 'cs-primary' : 'cs-secondary'}
                onClick={goForward}
                disabled={stuck} aria-keyshortcuts="Space ArrowRight">
                {nextLabel} <ChevronRight size={16} strokeWidth={1.75} />
              </button>
            )}

        <div className="cs-tools">
          <SpeakButton text={last?.turn?.text || point?.gist || ''} />
          {point?.example && (
            <button type="button" className="cs-tool"
              aria-pressed={panel === 'example'}
              onClick={() => setPanel((p) => (p === 'example' ? null : 'example'))}>
              <FlaskConical size={14} strokeWidth={1.75} />예시
            </button>
          )}
        </div>

        {inputRow}
      </div>

      {panel === 'example' && (
        <div className="cs-panel" role="dialog" aria-label="예시 문제">
          <div className="cs-panel-head">
            <span className="cs-panel-label">예시 문제</span>
            <button type="button" className="cs-tool" onClick={() => setPanel(null)} aria-label="닫기">
              <X size={15} strokeWidth={1.75} />
            </button>
          </div>
          <div className="cs-panel-body">
            <ParsedText text={point.example.q} />
            <details className="cs-details">
              <summary>풀이 보기</summary>
              <ParsedText text={point.example.solution} />
            </details>
          </div>
        </div>
      )}
    </div>
  );
}

// ── 스트림 ───────────────────────────────────────────────────────────────
// 턴을 그대로 그리지 않고 「말풍선·그림」 목록으로 한 번 편다. 그래야 앞 항목의
// 화자를 알 수 있고, 같은 화자가 연달아 말할 때 아바타와 이름표를 첫 말풍선에만
// 달 수 있다. 턴 안에서만 보면 그 판단이 안 선다.
//
// quiz 턴은 물음만 말풍선으로 올리고 선택지는 바닥으로 내려보낸다. 답한 뒤에는
// 그 결과 대사가 바로 뒤에 이어 붙는다.
function streamItems(turns) {
  const out = [];
  turns.forEach((item) => {
    const { turn } = item;
    const isQuiz = isChoiceTurn(turn);
    const text = (isQuiz || turn.who === WHO.recall) ? turn.prompt : turn.text;
    if (text) out.push({ kind: 'bubble', who: isQuiz ? WHO.teach : turn.who, text, mood: 'idle' });
    if (turn.viz) out.push({ kind: 'figure', viz: turn.viz });
    if (isQuiz) {
      const reply = quizSay(turn, item);
      if (reply?.text) out.push({ kind: 'bubble', who: reply.who, text: reply.text, mood: reply.mood });
    }
  });
  return out;
}

function Stream({ turns }) {
  const items = streamItems(turns);
  return items.map((it, i) => {
    if (it.kind === 'figure') {
      return (
        <FigureCard key={i} viz={it.viz}>
          <VizRouter name={it.viz.template} rawJson={vizJson(it.viz)} />
        </FigureCard>
      );
    }
    // 바로 앞 항목이 같은 화자의 말풍선이면 이어지는 말풍선이다.
    const prev = items[i - 1];
    const cont = prev?.kind === 'bubble' && prev.who === it.who;
    return <Bubble key={i} who={it.who} text={it.text} mood={it.mood} cont={cont} />;
  });
}

/**
 * 말풍선 하나.
 *
 * 꼬리는 삼각형이 아니라 화자 쪽 위 모서리를 4px 로 각지게 해서 낸다. 그 꼬리는
 * **첫 말풍선에만** 준다 — 이어지는 말풍선까지 각지면 한 사람이 여러 번 말을 건
 * 것처럼 보인다. 이어지는 것은 네 모서리 모두 14px 이다.
 */
function Bubble({ who, text, mood = 'idle', cont = false, sideTag = false }) {
  const c = castOf(who);
  const right = c.side === 'right';
  if (!text) return null;
  const cls = [
    'cs-line',
    right ? 'is-right' : '',
    cont ? 'is-cont' : '',
  ].filter(Boolean).join(' ');
  return (
    <div className={cls}>
      {!right && (
        <div className="cs-avatar">
          {!cont && <Avatar who={who} mood={mood} size={28} />}
        </div>
      )}
      <div className="cs-linebody">
        {!cont && (
          <span className="cs-who">
            {c.name}
            {sideTag && <span className="cs-side-tag">AI</span>}
          </span>
        )}
        <div className={`cs-bubble cs-bubble--${who}${mood === 'wrong' ? ' is-wrong' : ''}`}>
          <ParsedText text={markEmphasis(text)} />
        </div>
      </div>
      {right && (
        <div className="cs-avatar">
          {!cont && <Avatar who={who} mood={mood} size={28} />}
        </div>
      )}
    </div>
  );
}

// 카드 라벨은 **내용의 형식**을 말한다. 표가 들어가면 「표」, 그래프면 「그림」,
// 사례면 「예시」다. 표를 담고 「그림」이라 쓰지 않는다.
const TABLE_TEMPLATES = /table|matrix|compare|classify|payoff|checklist|steps|flow|timeline/i;
const CASE_TEMPLATES = /case|example|scenario/i;
export function figureKind(template) {
  if (CASE_TEMPLATES.test(template || '')) return '예시';
  if (TABLE_TEMPLATES.test(template || '')) return '표';
  return '그림';
}

/** 그림 카드 — 스트림 안에 흐름대로 놓인다. 단계 조작은 VizRouter 가 갖는다. */
function FigureCard({ viz, children }) {
  const title = viz?.caption || viz?.params?.caption || '';
  return (
    <figure className="cs-figure">
      <figcaption className="cs-figure-cap">
        {figureKind(viz?.template)}{title ? ` · ${title}` : ''}
      </figcaption>
      <div className="cs-figure-body">{children}</div>
    </figure>
  );
}

// ── 바닥의 선택지 ────────────────────────────────────────────────────────
// 채점 전에는 고르는 자리, 채점 후에는 정답·내 답을 나란히 보여주는 자리.
function ChoiceDock({ item, onPick, onAgain, onNext, nextLabel }) {
  const choices = choicesOf(item.turn);
  const isOx = item.turn.who === WHO.ox;
  const solved = item.solved;
  return (
    <div className={`cs-choices${isOx ? ' is-ox' : ''}`} role="group" aria-label="선택지">
      {choices.map((c, i) => {
        const mine = item.picked.includes(i);
        const right = solved && c.ok;
        const wrong = solved && mine && !c.ok;
        const dimmed = solved && !right && !mine;
        const cls = right ? ' is-right' : wrong ? ' is-wrong' : dimmed ? ' is-dim' : '';
        return (
          <button type="button" key={i} className={`cs-choice${cls}`}
            onClick={() => onPick(i)} disabled={solved || mine}>
            {!isOx && <span className="cs-choice-no">{'①②③④⑤⑥'[i] || i + 1}</span>}
            <span className="cs-choice-text">{c.text}</span>
            {right && <span className="cs-choice-tag">정답</span>}
            {wrong && <span className="cs-choice-tag is-mine">내 답</span>}
          </button>
        );
      })}
      {solved
        ? (
          <div className="cs-choice-ops">
            <button type="button" className="cs-secondary" onClick={onAgain}>
              <RotateCcw size={14} strokeWidth={1.75} />다시 풀어보기
            </button>
            <button type="button" className="cs-primary" onClick={onNext}>
              {nextLabel} <ChevronRight size={16} strokeWidth={1.75} />
            </button>
          </div>
        )
        : <p className="cs-choice-hint">답을 고르면 넘어갈 수 있어요</p>}
    </div>
  );
}

// ── 서술 인출 도크 — 시안 330:309 ────────────────────────────────
// 쓰기 전에는 정답을 보여 주지 않는다. 보고 쓰면 인출이 아니다.
//
// 도크의 초안은 턴마다 새로 시작해야 한다 — 호출부에서 key={턴 인덱스} 로 리마운트한다.
// key 가 없으면 연속된 인출 턴에서 앞 답이 새 백지에 남아, 「백지에서 꺼내 쓰기」가 무너진다.
function RecallDock({ item, onSubmit, onGrade, onNext, nextLabel }) {
  const [text, setText] = useState('');
  const written = item.written;
  if (!written) {
    return (
      <div className="cs-recall">
        <textarea className="cs-recall-input" rows={3} value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="여기에 써보세요" aria-label="인출 답안" />
        <button type="button" className="cs-primary"
          onClick={() => onSubmit(text)} disabled={!text.trim()}>답 제출</button>
      </div>
    );
  }
  if (!item.solved) {
    return (
      <div className="cs-recall">
        <div className="cs-recall-answer">
          <span className="cs-recall-label">정답</span>
          <ParsedText text={markEmphasis(item.turn.answer || '')} />
        </div>
        <div className="cs-recall-grade">
          <button type="button" className="cs-secondary" onClick={() => onGrade('wrong')}>못 썼음</button>
          <button type="button" className="cs-secondary" onClick={() => onGrade('partial')}>일부만</button>
          <button type="button" className="cs-primary" onClick={() => onGrade('right')}>다 썼음</button>
        </div>
      </div>
    );
  }
  return (
    <button type="button" className="cs-primary" onClick={onNext}>
      {nextLabel} <ChevronRight size={16} strokeWidth={1.75} />
    </button>
  );
}

// ── 입력줄 + 슬래시 팔레트 ───────────────────────────────────────────────
// 「/」로 시작하면 팔레트가 뜨고, Tab·Enter 로 첫 항목을 넣는다.
function SlashInput({ value, onChange, onRun, onSend, canAsk }) {
  const open = value.startsWith('/');
  const hits = useMemo(() => {
    if (!open) return [];
    const q = value.slice(1);
    return SLASH.filter((s) => s.cmd.slice(1).startsWith(q));
  }, [open, value]);

  const submit = () => {
    const t = value.trim();
    if (!t) return;
    if (t.startsWith('/')) {
      const hit = hits[0] || SLASH.find((s) => s.cmd === t);
      if (hit) onRun(hit.cmd);
      return;
    }
    onSend(t);
  };

  return (
    <div className="cs-inputwrap">
      {open && hits.length > 0 && (
        <ul className="cs-palette" role="listbox" aria-label="명령어">
          {hits.map((s, i) => (
            <li key={s.cmd}>
              <button type="button" className={`cs-palette-row${i === 0 ? ' is-on' : ''}`}
                onClick={() => onRun(s.cmd)}>
                <span className="cs-palette-cmd">{s.cmd}</span>
                <span className="cs-palette-desc">{s.desc}</span>
                {i === 0 && <span className="cs-palette-key">Tab ↹</span>}
              </button>
            </li>
          ))}
        </ul>
      )}
      <div className="cs-input">
        <input
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') { e.preventDefault(); submit(); }
            else if (e.key === 'Tab' && open && hits[0]) { e.preventDefault(); onChange(hits[0].cmd); }
            else if (e.key === 'Escape' && open) { e.preventDefault(); onChange(''); }
          }}
          placeholder={canAsk ? '메시지를 입력하거나 / 로 명령어' : '/ 로 명령어'}
          aria-label="메시지 또는 명령어"
        />
        <button type="button" className="cs-send" onClick={submit}
          disabled={!value.trim()} aria-label="보내기">
          <SendHorizontal size={17} strokeWidth={1.75} />
        </button>
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
    // OX 도 되짚기에 넣는다. 빼면 관에 OX 를 넣는 순간 그 문항들이 되짚기에서
    // 조용히 사라지고, 관 완료 화면의 확인 문제 수도 실제보다 적게 센다.
    .filter((t) => isChoiceTurn(t) && choicesOf(t).length)
    .map((t) => ({ turn: t, seq: p.seq, title: p.title })));
  if (all.length <= RECAP_MAX) return all;
  const stride = all.length / RECAP_MAX;
  return Array.from({ length: RECAP_MAX }, (_, i) => all[Math.floor(i * stride)]);
}

export function ConceptRecap({ track, onExit, onFinish }) {
  const items = useMemo(() => recapQuizzes(track), [track]);
  const [i, setI] = useState(0);
  const [picked, setPicked] = useState([]);
  const [score, setScore] = useState({ right: 0, total: 0 });
  const [done, setDone] = useState(false);

  const item = items[i];
  const choices = choicesOf(item?.turn);
  // 진행 규칙은 conceptTurns 의 choose() 와 같아야 한다. OX 는 선지가 둘뿐이라
  // 한 번 틀리면 남는 것이 정답 하나다 — 두 번째 시도를 「스스로 맞힘」으로 세면
  // 되짚기 점수가 실력이 아니라 찍기 횟수를 재게 된다.
  const maxTries = item?.turn?.who === WHO.ox ? 1 : 2;
  const solved = picked.some((n) => choices[n]?.ok) || picked.length >= maxTries;
  const assisted = solved && !picked.some((n) => choices[n]?.ok);
  const ans = { picked, solved, assisted, turn: item?.turn, index: 0 };

  const next = () => {
    if (!solved) return;
    const s2 = { right: score.right + (assisted ? 0 : 1), total: score.total + 1 };
    setScore(s2);
    setPicked([]);
    if (i + 1 >= items.length) {
      // 완료 화면이 있으면 그쪽이 마무리를 맡는다 — 여기서 또 결과를 그리면 두 번 끝난다.
      if (onFinish) { onFinish(s2); return; }
      setDone(true);
    } else setI(i + 1);
  };

  const restart = () => { setI(0); setPicked([]); setScore({ right: 0, total: 0 }); setDone(false); };

  if (!items.length) {
    return (
      <div className="cs-room">
        <div className="cs-stream">
          <div className="cs-doc">되짚을 문제가 없는 관입니다.</div>
        </div>
        <div className="cs-dock">
          <button type="button" className="cs-primary" onClick={onExit}>목록으로</button>
        </div>
      </div>
    );
  }

  if (done) {
    const all = score.right === score.total;
    return (
      <div className="cs-room">
        <div className="cs-stream">
          <div className="cs-pointhead"><span className="cs-pointhead-label">되짚기</span></div>
          <div className="cs-verdict">
            <p className="cs-verdict-title">되짚기 {score.right} / {score.total}</p>
          </div>
          <Bubble who={WHO.mate} mood={all ? 'right' : 'idle'}
            text={all
              ? '전부 스스로 맞혔습니다. 이 관은 여기서 접어도 됩니다.'
              : '틀린 자리가 이 관에서 다시 볼 곳입니다. 해당 논점을 한 번 더 열어 보세요.'} />
        </div>
        <div className="cs-dock">
          <button type="button" className="cs-primary" onClick={onExit}>목록으로</button>
          <div className="cs-tools">
            <button type="button" className="cs-tool" onClick={restart}>
              <RotateCcw size={14} strokeWidth={1.75} />다시
            </button>
          </div>
        </div>
      </div>
    );
  }

  const say = quizSay(item.turn, ans);
  return (
    <div className="cs-room">
      <div className="cs-stream">
        <div className="cs-pointhead">
          <span className="cs-pointhead-label">되짚기 {i + 1} / {items.length} · {item.title || ''}</span>
        </div>
        <Bubble who={WHO.teach} text={item.turn.prompt} />
        {say && <Bubble who={say.who} text={say.text} mood={say.mood} />}
      </div>
      <div className="cs-dock">
        <ChoiceDock item={ans}
          onPick={(n) => setPicked((p) => (p.includes(n) || solved ? p : p.concat(n)))}
          onAgain={() => setPicked([])}
          onNext={next}
          nextLabel={i + 1 >= items.length ? '되짚기 마치기' : '다음'} />
        <div className="cs-tools">
          <button type="button" className="cs-tool" onClick={onExit}>그만하기</button>
        </div>
      </div>
    </div>
  );
}

// ── 관을 다 익힌 뒤 ──────────────────────────────────────────────────────
// 시안(250:365). 관의 끝이 「목록으로」 한 줄로 끝나면 방금 한 일이 무엇이었는지
// 남지 않는다. 챙길 것 셋 · 확인 문제 성적 · 걸린 시간을 보여 주고, 다음 행동
// 두 개(이 관 문제 풀기 · 다음 관으로)를 준다.

/** 「챙길 것」 세 줄. 관 전체를 고르게 훑는다 — 앞 세 개만 뽑으면 뒤쪽이 안 보인다. */
export function keyTakeaways(track, max = 3) {
  const gists = (track?.points || []).map((p) => p.gist).filter(Boolean);
  if (gists.length <= max) return gists;
  const stride = gists.length / max;
  return Array.from({ length: max }, (_, i) => gists[Math.floor(i * stride)]);
}

export function ConceptDone({
  track, score, elapsedMs, quizCount, onSolve, onNextLeaf, onExit,
}) {
  const total = track?.points?.length || 0;
  const takeaways = useMemo(() => keyTakeaways(track), [track]);
  const minutes = elapsedMs ? Math.max(1, Math.round(elapsedMs / 60000)) : null;

  return (
    <div className="cs-room">
      <div className="cs-stream">
        <div className="cs-done-head">
          <p className="cs-done-leaf">{track?.title || ''}</p>
          <p className="cs-done-title">이 관을 다 익혔습니다</p>
          <p className="cs-done-sub">논점 {total}개를 모두 마쳤어요</p>
        </div>

        {takeaways.length > 0 && (
          <section className="cs-take">
            <h3 className="cs-take-label">이 관에서 챙길 것</h3>
            <ul className="cs-take-list">
              {takeaways.map((g, i) => (
                <li key={i}><ParsedText text={markEmphasis(g)} /></li>
              ))}
            </ul>
          </section>
        )}

        <div className="cs-done-stat">
          <span>
            {score && score.total > 0
              ? `확인 문제 ${score.total}문제 중 ${score.right}개 정답`
              : '확인 문제를 풀지 않았습니다'}
          </span>
          {minutes && <span className="cs-done-time">{minutes}분</span>}
        </div>
      </div>

      <div className="cs-dock">
        {onSolve && (
          <button type="button" className="cs-primary" onClick={onSolve}>
            이 관 문제 풀기{quizCount ? ` · 기출 ${quizCount}문제` : ''}
          </button>
        )}
        {onNextLeaf
          ? (
            <button type="button" className="cs-secondary" onClick={onNextLeaf}>
              다음 관으로 <ChevronRight size={16} strokeWidth={1.75} />
            </button>
          )
          : (
            <button type="button" className="cs-secondary" onClick={onExit}>
              단원 목록으로
            </button>
          )}
      </div>
    </div>
  );
}
