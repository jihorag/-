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
  FlaskConical, X, RotateCcw, SendHorizontal,
} from 'lucide-react';
import ParsedText from './ParsedText';
import Avatar from './ConceptCast';
import { markEmphasis } from './emphasis';
import { SpeakButton } from './Speech';
import VizRouter from './viz/VizRouter';
import {
  WHO, initTurnState, visibleTurns, canAdvance, advance, choose, retry,
  isPassed, atEnd, passDetail,
} from './conceptTurns';

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
  const choices = turn.choices || [];
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
  point, seq, total, onPassed, onDone, onNext, onAsk, onCommand,
}) {
  const [state, setState] = useState(initTurnState);
  const [panel, setPanel] = useState(null);   // 'example' | null
  const [draft, setDraft] = useState('');

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
  const openQuiz = last && last.turn.who === WHO.quiz ? last : null;

  const stuck = hasTurns && !canAdvance(point, state) && !atEnd(point, state);
  const finished = hasTurns && atEnd(point, state) && !stuck;

  // 새 턴이 열리면 그 턴이 보이도록 아래로. 사용자가 위를 읽는 중이면 방해하지 않는다.
  const streamRef = useRef(null);
  const bottomRef = useRef(null);
  useEffect(() => {
    const el = streamRef.current;
    if (!el) return;
    const nearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 220;
    if (nearBottom) bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [turns.length, openQuiz?.picked.length, openQuiz?.solved]);

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
      onSend={(text) => { setDraft(''); onAsk?.(text); }}
      canAsk={!!onAsk}
    />
  );

  // ── 옛 논점 폴백 — turns 가 없는 논점은 body 를 그대로 편다. ──────────────
  if (!hasTurns) {
    return (
      <div className="cs-room">
        <div className="cs-stream" ref={streamRef}>
          {head}
          {point?.viz && (
            <FigureCard caption={point.viz.caption || '그림'}>
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
      <div className="cs-stream" ref={streamRef}>
        {head}
        {turns.map((t) => <StreamTurn key={t.index} item={t} />)}
        <div ref={bottomRef} />
      </div>

      <div className="cs-dock">
        {openQuiz
          ? (
            <ChoiceDock item={openQuiz} onPick={pick} onAgain={again}
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

// ── 스트림의 한 턴 ───────────────────────────────────────────────────────
// quiz 턴은 물음만 말풍선으로 올리고 선택지는 바닥으로 내려보낸다. 답한 뒤에는
// 그 결과 대사가 바로 뒤에 이어 붙는다.
function StreamTurn({ item }) {
  const { turn } = item;
  const isQuiz = turn.who === WHO.quiz;
  const reply = isQuiz ? quizSay(turn, item) : null;
  return (
    <>
      <Bubble who={isQuiz ? WHO.teach : turn.who} text={isQuiz ? turn.prompt : turn.text} />
      {turn.viz && (
        <FigureCard caption={turn.viz.caption || turn.viz.params?.caption || '그림'}>
          <VizRouter name={turn.viz.template} rawJson={vizJson(turn.viz)} />
        </FigureCard>
      )}
      {reply && <Bubble who={reply.who} text={reply.text} mood={reply.mood} />}
    </>
  );
}

/** 말풍선 하나. 꼬리는 삼각형이 아니라 화자 쪽 모서리만 각지게 하는 것으로 낸다. */
function Bubble({ who, text, mood = 'idle' }) {
  const c = castOf(who);
  const right = c.side === 'right';
  if (!text) return null;
  return (
    <div className={`cs-line${right ? ' is-right' : ''}`}>
      {!right && (
        <div className="cs-avatar"><Avatar who={who} mood={mood} size={28} /></div>
      )}
      <div className="cs-linebody">
        <span className="cs-who">{c.name}</span>
        <div className={`cs-bubble cs-bubble--${who}${mood === 'wrong' ? ' is-wrong' : ''}`}>
          <ParsedText text={markEmphasis(text)} />
        </div>
      </div>
      {right && (
        <div className="cs-avatar"><Avatar who={who} mood={mood} size={28} /></div>
      )}
    </div>
  );
}

/** 그림 카드 — 스트림 안에 흐름대로 놓인다. 단계 조작은 VizRouter 가 갖는다. */
function FigureCard({ caption, children }) {
  return (
    <figure className="cs-figure">
      <figcaption className="cs-figure-cap">{caption}</figcaption>
      <div className="cs-figure-body">{children}</div>
    </figure>
  );
}

// ── 바닥의 선택지 ────────────────────────────────────────────────────────
// 채점 전에는 고르는 자리, 채점 후에는 정답·내 답을 나란히 보여주는 자리.
function ChoiceDock({ item, onPick, onAgain, onNext, nextLabel }) {
  const choices = item.turn.choices || [];
  const solved = item.solved;
  return (
    <div className="cs-choices" role="group" aria-label="선택지">
      {choices.map((c, i) => {
        const mine = item.picked.includes(i);
        const right = solved && c.ok;
        const wrong = solved && mine && !c.ok;
        const dimmed = solved && !right && !mine;
        const cls = right ? ' is-right' : wrong ? ' is-wrong' : dimmed ? ' is-dim' : '';
        return (
          <button type="button" key={i} className={`cs-choice${cls}`}
            onClick={() => onPick(i)} disabled={solved || mine}>
            <span className="cs-choice-no">{'①②③④⑤⑥'[i] || i + 1}</span>
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
  const ans = { picked, solved, assisted, turn: item?.turn, index: 0 };

  const next = () => {
    if (!solved) return;
    setScore((s) => ({ right: s.right + (assisted ? 0 : 1), total: s.total + 1 }));
    setPicked([]);
    if (i + 1 >= items.length) setDone(true); else setI(i + 1);
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
