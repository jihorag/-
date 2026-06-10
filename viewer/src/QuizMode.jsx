// ⚡ 퀴즈 탭 — 문제풀이(학습)와 독립된 검증·게임화 엔진.
// 세션 단위(짧은 판) · 해설 없이 빠른 템포 · 종료 후 일괄 리뷰 · 점수/콤보/최고기록.
// 데이터는 전부 기존 자산 재사용: classifiedList, progress, confidence, coach 약점.
import { useState, useEffect, useRef, useMemo } from 'react';
import { ArrowLeft } from 'lucide-react';
import { ParsedText } from './ParsedText';

const SESSIONS_KEY = 'quiz-sessions-v1';
const CALC_SUBJECTS = ['경제학원론', '회계학'];

// ───────────────────────── 모드 정의 ─────────────────────────
export const QUIZ_MODES = [
  { id: 'daily',      icon: '📅', label: '일일 퀴즈',   desc: '매일 같은 10문 · 모두가 같은 문제',
    color: '#0891b2', bg: '#ecfeff', border: '#a5f3fc', count: 10 },
  { id: 'random',     icon: '🎲', label: '랜덤 퀴즈',   desc: '전 과목 무작위 10문',
    color: '#3182F6', bg: '#EFF6FF', border: '#BFDBFE', count: 10 },
  { id: 'timeattack', icon: '⏱', label: '타임어택',    desc: '5분 안에 최대한 많이',
    color: '#7C3AED', bg: '#F5F3FF', border: '#DDD6FE', count: 80, timeLimitMs: 5 * 60000 },
  { id: 'sudden',     icon: '🔥', label: '서든데스',    desc: '틀리는 순간 끝 — 몇 문제까지?',
    color: '#dc2626', bg: '#fef2f2', border: '#fecaca', count: 200, suddenDeath: true },
  { id: 'weak',       icon: '🎯', label: '약점 집중',   desc: '정답률 낮은 단원만 골라서',
    color: '#059669', bg: '#ECFDF5', border: '#A7F3D0', count: 10 },
  { id: 'wrong',      icon: '🏆', label: '오답 정복',   desc: '틀렸거나 애매했던 문제 재도전',
    color: '#D97706', bg: '#FFFBEB', border: '#FDE68A', count: 10 },
  { id: 'calc',       icon: '🧮', label: '계산 스프린트', desc: '경제·회계 계산 감각 단련',
    color: '#be123c', bg: '#fff1f2', border: '#fecdd3', count: 10 },
  { id: 'subject',    icon: '📚', label: '과목 뽑기',   desc: '한 과목만 집중 10문',
    color: '#4f46e5', bg: '#eef2ff', border: '#c7d2fe', count: 10, needsSubject: true },
];

// ───────────────────────── 문제 선정 ─────────────────────────
// 날짜 시드 PRNG (일일 퀴즈 — 같은 날 = 같은 문제)
function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const shuffleWith = (arr, rnd) => {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

// ctx: { classifiedList, progress, qid, confMap, weakIds(Set), subject }
export function selectQuizQuestions(modeId, ctx) {
  const mode = QUIZ_MODES.find(m => m.id === modeId);
  const pool = ctx.classifiedList.filter(q => q.answerNorm && Array.isArray(q.options) && q.options.length >= 4);
  const rnd = modeId === 'daily'
    ? mulberry32(parseInt(new Date().toISOString().slice(0, 10).replace(/-/g, ''), 10))
    : mulberry32((Date.now() % 2 ** 31) ^ (Math.random() * 2 ** 31));
  const shuffled = shuffleWith(pool, rnd);

  let picked;
  switch (modeId) {
    case 'daily':
      picked = shuffled; break;
    case 'random': {
      const unseen = shuffled.filter(q => !ctx.progress[ctx.qid(q)]);
      picked = [...unseen, ...shuffled.filter(q => ctx.progress[ctx.qid(q)])];
      break;
    }
    case 'timeattack':
    case 'sudden':
      picked = shuffled; break;
    case 'weak':
      picked = shuffled.filter(q => ctx.weakIds?.has(ctx.qid(q)));
      if (picked.length < mode.count) {
        // 약점 절 데이터가 부족하면 오답 과목으로 보충
        picked = [...picked, ...shuffled.filter(q => !ctx.weakIds?.has(ctx.qid(q)))];
      }
      break;
    case 'wrong': {
      const bad = shuffled.filter(q => {
        const p = ctx.progress[ctx.qid(q)];
        const conf = ctx.confMap?.[ctx.qid(q)];
        return (p && p.correct === false) || conf === 'fuzzy' || conf === 'unknown';
      });
      picked = bad; break;
    }
    case 'calc':
      picked = shuffled.filter(q => CALC_SUBJECTS.includes(q.taxSubjectName)); break;
    case 'subject':
      picked = shuffled.filter(q => q.taxSubjectName === ctx.subject); break;
    default:
      picked = shuffled;
  }
  return picked.slice(0, mode.count);
}

// ───────────────────────── 기록 저장 ─────────────────────────
export function loadQuizHistory() {
  try { return JSON.parse(localStorage.getItem(SESSIONS_KEY) || '[]') || []; } catch { return []; }
}
export function saveQuizSession(s) {
  const all = [...loadQuizHistory(), s].slice(-100);
  try { localStorage.setItem(SESSIONS_KEY, JSON.stringify(all)); } catch { /* full */ }
  return all;
}
export function bestFor(modeId, history) {
  const hs = history.filter(h => h.mode === modeId);
  if (!hs.length) return null;
  if (modeId === 'timeattack' || modeId === 'sudden') return Math.max(...hs.map(h => h.correct));
  return Math.max(...hs.map(h => h.total ? Math.round((h.correct / h.total) * 100) : 0));
}
export function dailyDoneToday(history) {
  const today = new Date().toISOString().slice(0, 10);
  return history.some(h => h.mode === 'daily' && h.date === today);
}

// ───────────────────────── 러너 ─────────────────────────
const fmtMs = (ms) => {
  const s = Math.max(0, Math.ceil(ms / 1000));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
};

export function QuizRunner({ questions, mode, onFinish, onQuit }) {
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState([]);   // [{q, sel, correct}]
  const [flash, setFlash] = useState(null);     // {sel, correct} — 0.8초 정오 플래시
  const [combo, setCombo] = useState(0);
  const [maxCombo, setMaxCombo] = useState(0);
  const [now, setNow] = useState(Date.now());
  const startRef = useRef(Date.now());
  const finishedRef = useRef(false);
  const timerRef = useRef(null);

  const q = questions[idx];
  const remainMs = mode.timeLimitMs ? mode.timeLimitMs - (now - startRef.current) : null;

  const finish = (finalAnswers) => {
    if (finishedRef.current) return;
    finishedRef.current = true;
    const corr = finalAnswers.filter(a => a.correct).length;
    onFinish({
      mode: mode.id, date: new Date().toISOString().slice(0, 10), ts: Date.now(),
      total: finalAnswers.length, correct: corr,
      durationMs: Date.now() - startRef.current,
      maxCombo: Math.max(maxCombo, combo),
      answers: finalAnswers,
    });
  };

  // 제한시간 카운트다운 (타임어택)
  useEffect(() => {
    if (!mode.timeLimitMs) return undefined;
    const iv = setInterval(() => setNow(Date.now()), 250);
    return () => clearInterval(iv);
  }, [mode.timeLimitMs]);
  useEffect(() => {
    if (remainMs != null && remainMs <= 0) finish(answers);
  }, [remainMs]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => () => clearTimeout(timerRef.current), []);

  const pick = (n) => {
    if (flash || !q) return;
    const correct = String(n) === String(q.answerNorm);
    const entry = { q, sel: String(n), correct };
    const nextAnswers = [...answers, entry];
    setAnswers(nextAnswers);
    setFlash({ sel: n, correct });
    const nextCombo = correct ? combo + 1 : 0;
    setCombo(nextCombo);
    if (correct) setMaxCombo(m => Math.max(m, nextCombo));
    timerRef.current = setTimeout(() => {
      setFlash(null);
      if (mode.suddenDeath && !correct) { finish(nextAnswers); return; }
      if (idx + 1 >= questions.length) { finish(nextAnswers); return; }
      setIdx(i => i + 1);
    }, correct ? 550 : 950);
  };

  if (!q) return null;
  const progPct = mode.timeLimitMs
    ? Math.min(100, ((now - startRef.current) / mode.timeLimitMs) * 100)
    : (idx / questions.length) * 100;

  return (
    <div className="app-container" style={{ display: 'flex', flexDirection: 'column',
      minHeight: '100dvh', background: '#f8fafc' }}>
      <header style={{ flexShrink: 0, padding: '12px 14px', display: 'flex',
        alignItems: 'center', justifyContent: 'space-between', gap: 10,
        paddingTop: 'calc(12px + env(safe-area-inset-top, 0px))' }}>
        <button onClick={() => (answers.length ? finish(answers) : onQuit())} aria-label="퀴즈 종료"
          style={{ border: '1px solid #e5e7eb', background: '#fff', borderRadius: 10,
            padding: '7px 12px', fontWeight: 700, fontSize: '0.8rem', color: '#6b7280', cursor: 'pointer' }}>
          ✕ 종료
        </button>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          {combo >= 2 && (
            <span style={{ fontWeight: 800, fontSize: '0.85rem', color: '#ea580c' }}>🔥 {combo}연속</span>
          )}
          <span style={{ fontWeight: 800, fontSize: '0.9rem',
            color: remainMs != null && remainMs < 30000 ? '#dc2626' : '#111827' }}>
            {mode.timeLimitMs ? `⏱ ${fmtMs(remainMs)}` : `${idx + 1} / ${questions.length}`}
          </span>
        </div>
      </header>
      <div style={{ height: 4, background: '#e5e7eb', flexShrink: 0 }}>
        <div style={{ width: `${progPct}%`, height: '100%', transition: 'width 0.25s',
          background: mode.color || '#3182F6' }} />
      </div>

      <main style={{ flex: 1, overflowY: 'auto', padding: '16px 16px 28px' }}>
        <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#9ca3af', marginBottom: 8 }}>
          {mode.icon} {mode.label} · {q.taxSubjectName || q.subject || ''}
        </div>
        <div style={{ background: '#fff', borderRadius: 14, padding: 16,
          boxShadow: '0 2px 8px rgba(0,0,0,0.05)', marginBottom: 12,
          fontSize: '0.98rem', lineHeight: 1.6, fontWeight: 600, color: '#111827' }}>
          <ParsedText text={q.question} />
        </div>
        {q.options.map((opt, i) => {
          const n = i + 1;
          const isAns = String(n) === String(q.answerNorm);
          const isSel = flash && flash.sel === n;
          let border = '#e5e7eb'; let bg = '#fff';
          if (flash) {
            if (isAns) { border = '#16a34a'; bg = '#f0fdf4'; }
            else if (isSel) { border = '#ef4444'; bg = '#fef2f2'; }
          }
          return (
            <button key={i} onClick={() => pick(n)} disabled={!!flash}
              style={{ display: 'flex', gap: 10, width: '100%', textAlign: 'left',
                padding: '12px 14px', marginBottom: 8, borderRadius: 12, cursor: flash ? 'default' : 'pointer',
                border: `1.5px solid ${border}`, background: bg, fontSize: '0.92rem', lineHeight: 1.55,
                color: '#1f2937', alignItems: 'flex-start' }}>
              <span style={{ flexShrink: 0, width: 24, height: 24, borderRadius: '50%',
                border: '1.5px solid #d1d5db', display: 'flex', alignItems: 'center',
                justifyContent: 'center', fontSize: '0.78rem', fontWeight: 700,
                background: flash && isAns ? '#16a34a' : flash && isSel ? '#ef4444' : '#fff',
                color: flash && (isAns || isSel) ? '#fff' : '#6b7280',
                borderColor: flash && isAns ? '#16a34a' : flash && isSel ? '#ef4444' : '#d1d5db' }}>
                {flash && isAns ? '✓' : flash && isSel && !isAns ? '✕' : n}
              </span>
              <span style={{ flex: 1 }}>{opt ? <ParsedText text={opt} /> : `${n}번`}</span>
            </button>
          );
        })}
      </main>
    </div>
  );
}

// ───────────────────────── 결과 ─────────────────────────
export function QuizResult({ result, history, onRetry, onReviewWrong, onHome }) {
  const [openIdx, setOpenIdx] = useState(null);
  const mode = QUIZ_MODES.find(m => m.id === result.mode) || QUIZ_MODES[1];
  const pct = result.total ? Math.round((result.correct / result.total) * 100) : 0;
  const prevBest = useMemo(() => {
    const prior = history.slice(0, -1); // 방금 판 제외
    return bestFor(result.mode, prior);
  }, [history, result.mode]);
  const score = (result.mode === 'timeattack' || result.mode === 'sudden') ? result.correct : pct;
  const isNewBest = score > 0 && (prevBest == null || score > prevBest);
  const wrong = result.answers.filter(a => !a.correct);
  const recent = history.filter(h => h.mode === result.mode).slice(-10);

  return (
    <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', paddingBottom: 24 }}>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
        <button className="back-btn" onClick={onHome}>
          <ArrowLeft size={24} style={{ marginRight: 8 }} />
          <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>퀴즈 홈</span>
        </button>
      </header>
      <main className="main-content" style={{ marginTop: 16 }}>
        {/* 점수 헤드라인 */}
        <section style={{ background: '#fff', borderRadius: 16, padding: 22, textAlign: 'center',
          boxShadow: '0 2px 10px rgba(0,0,0,0.06)', marginBottom: 12 }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: mode.color }}>
            {mode.icon} {mode.label}
          </div>
          <div style={{ fontSize: '2.6rem', fontWeight: 900, color: '#111827', marginTop: 6 }}>
            {result.mode === 'timeattack' || result.mode === 'sudden'
              ? <>{result.correct}<span style={{ fontSize: '1rem', color: '#9ca3af' }}> 문제</span></>
              : <>{pct}<span style={{ fontSize: '1rem', color: '#9ca3af' }}>점</span></>}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: 4 }}>
            {result.correct}/{result.total} 정답 · {fmtMs(result.durationMs)} 소요
            {result.maxCombo >= 2 && <> · 🔥 최대 {result.maxCombo}연속</>}
          </div>
          {isNewBest && result.total > 0 && (
            <div style={{ marginTop: 8, display: 'inline-block', padding: '4px 14px', borderRadius: 999,
              background: '#fffbeb', border: '1px solid #fde68a', color: '#b45309',
              fontWeight: 800, fontSize: '0.8rem' }}>
              🏅 신기록!{prevBest != null ? ` (이전 ${prevBest}${result.mode === 'timeattack' || result.mode === 'sudden' ? '문제' : '점'})` : ''}
            </div>
          )}
          {/* 최근 10판 미니 그래프 */}
          {recent.length >= 2 && (
            <div style={{ display: 'flex', gap: 3, justifyContent: 'center', alignItems: 'flex-end',
              height: 36, marginTop: 14 }}>
              {recent.map((h, i) => {
                const v = (h.mode === 'timeattack' || h.mode === 'sudden')
                  ? h.correct : (h.total ? (h.correct / h.total) * 100 : 0);
                const max = Math.max(...recent.map(x => (x.mode === 'timeattack' || x.mode === 'sudden')
                  ? x.correct : (x.total ? (x.correct / x.total) * 100 : 0))) || 1;
                return <div key={i} style={{ width: 14, borderRadius: 3,
                  height: `${Math.max(10, (v / max) * 100)}%`,
                  background: i === recent.length - 1 ? mode.color : '#e5e7eb' }} />;
              })}
            </div>
          )}
        </section>

        {/* 오답 리뷰 — 여기서만 해설 노출 */}
        {wrong.length > 0 && (
          <section style={{ marginBottom: 12 }}>
            <div style={{ fontWeight: 800, fontSize: '0.9rem', color: '#111827', marginBottom: 8 }}>
              ✕ 틀린 문제 {wrong.length}개 — 해설 확인
            </div>
            {wrong.map((a, i) => (
              <div key={i} style={{ background: '#fff', borderRadius: 12, marginBottom: 8,
                border: '1px solid #fecaca', overflow: 'hidden' }}>
                <button onClick={() => setOpenIdx(openIdx === i ? null : i)}
                  style={{ width: '100%', textAlign: 'left', padding: '11px 14px', border: 'none',
                    background: 'none', cursor: 'pointer', fontSize: '0.85rem', lineHeight: 1.5, color: '#374151' }}>
                  <span style={{ color: '#dc2626', fontWeight: 800, marginRight: 6 }}>
                    내 답 {a.sel} → 정답 {a.q.answerNorm}
                  </span>
                  {(a.q.question || '').replace(/\n/g, ' ').slice(0, 60)}…
                  <span style={{ float: 'right', color: '#9ca3af' }}>{openIdx === i ? '▲' : '▼'}</span>
                </button>
                {openIdx === i && (
                  <div style={{ padding: '0 14px 12px', fontSize: '0.85rem', lineHeight: 1.65, color: '#4b5563' }}>
                    <div style={{ padding: 10, background: '#f9fafb', borderRadius: 8 }}>
                      <ParsedText text={a.q.explanation || '해설 없음 — 정답: ' + a.q.answerNorm + '번'} />
                    </div>
                  </div>
                )}
              </div>
            ))}
          </section>
        )}

        <div style={{ display: 'flex', gap: 8 }}>
          {wrong.length > 0 && (
            <button onClick={() => onReviewWrong(wrong.map(a => a.q))}
              style={{ flex: 1, padding: '13px', borderRadius: 12, border: '1px solid #fdba74',
                background: '#fff7ed', color: '#c2410c', fontWeight: 800, cursor: 'pointer', fontSize: '0.85rem' }}>
              오답 학습모드로
            </button>
          )}
          <button onClick={onRetry}
            style={{ flex: 1.4, padding: '13px', borderRadius: 12, border: 'none',
              background: mode.color, color: '#fff', fontWeight: 800, cursor: 'pointer', fontSize: '0.9rem' }}>
            {mode.icon} 한 판 더
          </button>
        </div>
      </main>
    </div>
  );
}
