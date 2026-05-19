import { useState, useMemo, useEffect, useCallback, useRef } from 'react';
import { ArrowLeft, House, Compass, RotateCcw, ChartColumn } from 'lucide-react';
import { cloudEnabled, supabase, pullState, pushState } from './cloud';
import katex from 'katex';
import 'katex/dist/katex.min.css';

// ===== 사용자 데이터 관리 (백업/복원/초기화) =====
// 모든 학습 상태는 localStorage 의 quiz-* 키에 저장됨. 계정 동기화의 단일 레이어.
const collectUserData = () => {
  const data = {};
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    if (k && k.startsWith('quiz-')) data[k] = localStorage.getItem(k);
  }
  return { version: 1, exportedAt: new Date().toISOString(), data };
};
const loadProfile = () => {
  try { return JSON.parse(localStorage.getItem('quiz-profile') || '{}') || {}; }
  catch { return {}; }
};
const saveProfile = (p) => {
  try { localStorage.setItem('quiz-profile', JSON.stringify(p)); } catch { /* SSR */ }
};
const exportUserData = () => {
  // 백업 시각 기록(백업 후 수집되도록 먼저 저장)
  saveProfile({ ...loadProfile(), lastBackup: new Date().toISOString() });
  const blob = new Blob([JSON.stringify(collectUserData(), null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `gampyeong-backup-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
};
const importUserData = (text) => {
  const parsed = JSON.parse(text);
  const data = parsed && parsed.data;
  if (!data || typeof data !== 'object') throw new Error('형식이 올바르지 않은 백업 파일입니다.');
  for (let i = localStorage.length - 1; i >= 0; i--) {
    const k = localStorage.key(i);
    if (k && k.startsWith('quiz-')) localStorage.removeItem(k);
  }
  for (const k in data) {
    if (k.startsWith('quiz-') && typeof data[k] === 'string') localStorage.setItem(k, data[k]);
  }
};
const resetUserData = () => {
  for (let i = localStorage.length - 1; i >= 0; i--) {
    const k = localStorage.key(i);
    if (k && k.startsWith('quiz-')) localStorage.removeItem(k);
  }
};

// v4 난이도(1~5) 배지 메타: 색/라벨
const DIFFICULTY_META = {
  1: { label: '난이도 1 · 매우쉬움', bg: '#ecfdf5', fg: '#047857' },
  2: { label: '난이도 2 · 쉬움', bg: '#f0fdf4', fg: '#15803d' },
  3: { label: '난이도 3 · 보통', bg: '#fefce8', fg: '#a16207' },
  4: { label: '난이도 4 · 어려움', bg: '#fff7ed', fg: '#c2410c' },
  5: { label: '난이도 5 · 매우어려움', bg: '#fef2f2', fg: '#b91c1c' },
};

// 정답 정규화: 원문자/공백 처리 후 1..optCount 범위의 숫자 문자열만 유효, 아니면 null
const CIRCLED = { '①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5', '⑥': '6', '⑦': '7', '⑧': '8', '⑨': '9', '⑩': '10' };
const normAnswer = (raw, optCount) => {
  if (raw == null) return null;
  let s = String(raw).trim();
  if (CIRCLED[s]) s = CIRCLED[s];
  if (!/^\d+$/.test(s)) return null;            // 빈값·'정답없음'·서술형 센티넬 등
  const n = parseInt(s, 10);
  if (n < 1) return null;                        // '0' 등
  if (optCount && n > optCount) return null;     // 범위 초과
  return String(n);
};

// ===== 학습 진행률 (localStorage) =====
const PROGRESS_KEY = 'quiz-progress-v1';
const qid = (q) => q.id || `${q.exam}_${q.year}_${q.number}`;

const loadProgress = () => {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}') || {};
  } catch {
    return {};
  }
};

// 검색·필터 영속화 (새로고침/딥링크 시 유지)
const FILTERS_KEY = 'quiz-filters-v1';

// 가이드 학습 세션 이어풀기: 개념별 마지막 위치(localStorage)
const POS_KEY = 'quiz-pos-v1';
const loadPos = () => {
  try { return JSON.parse(localStorage.getItem(POS_KEY) || '{}') || {}; }
  catch { return {}; }
};
const savePos = (map) => {
  try { localStorage.setItem(POS_KEY, JSON.stringify(map)); } catch { /* quota/SSR */ }
};
const EMPTY_FILTERS = { exams: [], subjects: [], years: [], diffs: [], kw: '', cleanOnly: false };
const loadFilters = () => {
  try {
    const f = JSON.parse(localStorage.getItem(FILTERS_KEY) || 'null');
    return f && typeof f === 'object' ? { ...EMPTY_FILTERS, ...f } : { ...EMPTY_FILTERS };
  } catch {
    return { ...EMPTY_FILTERS };
  }
};

// ===== 기억 곡선(간격 반복) =====
// Leitner 간격(일): 맞히면 다음 칸으로, 틀리면 1칸으로. 끝까지 가면 graduated.
const SRS_LADDER = [1, 3, 7, 16, 35, 70];
const DAY = 86400000;
const dayStart = (t) => { const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); };
// 복습 강도: 간격 배율 + 하루 복습 상한
// 배열에서 무작위 n개(Fisher-Yates 부분 셔플). 모듈 레벨이라 렌더 순수성 규칙 밖.
const sampleN = (arr, n) => {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a.slice(0, n);
};

// B4: 스와이프 추적(렌더와 무관한 전역 트랜션트 상태)
const swipe = { x: 0, y: 0 };
// C2: 문항 목록 스크롤 위치 기억(목록↔학습 왕복 시 복원)
const scrollMem = { qlist: 0 };

// A4: 컨페티 조각(모듈 로드 시 1회 생성 — 렌더 순수성 규칙 밖)
const CONFETTI_COLORS = ['#2563eb', '#16a34a', '#ea580c', '#eab308', '#ec4899', '#06b6d4'];
const CONFETTI_PIECES = Array.from({ length: 90 }, () => ({
  left: Math.random() * 100,
  delay: Math.random() * 0.5,
  dur: 2 + Math.random() * 1.6,
  color: CONFETTI_COLORS[Math.floor(Math.random() * CONFETTI_COLORS.length)],
  rot: Math.random() * 360,
}));
const Confetti = () => (
  <div className="confetti-layer" aria-hidden="true">
    {CONFETTI_PIECES.map((p, i) => (
      <span key={i} className="confetti-pc" style={{
        left: `${p.left}%`, background: p.color,
        animationDelay: `${p.delay}s`, animationDuration: `${p.dur}s`,
        transform: `rotate(${p.rot}deg)`,
      }} />
    ))}
  </div>
);

// 첫 화면 가치 설명(모달 아님 — 빈 상태 히어로에 인라인)
const ONB_BULLETS = [
  { emoji: '✍️', t: '풀면서 이해', d: '해설로 개념까지' },
  { emoji: '🔁', t: '틀린 건 기억곡선', d: '복습일 자동 배정' },
  { emoji: '📊', t: '약점 한눈에', d: '현황·추천으로 보강' },
];

const SRS_MODES = {
  hard:   { label: '빡세게', factor: 0.6, cap: Infinity },
  normal: { label: '보통',   factor: 1,   cap: 40 },
  easy:   { label: '여유',   factor: 1.7, cap: 20 },
};
const SRS_MODE_KEY = 'quiz-srs-mode';
const ladderFor = (mode) => {
  const f = (SRS_MODES[mode] || SRS_MODES.normal).factor;
  return SRS_LADDER.map(d => Math.max(1, Math.round(d * f)));
};
// prevSrs + 정오답 → 다음 srs. due는 해당 날짜 0시(ms). graduated면 due=null.
const nextSrs = (prevSrs, correct, mode = 'normal') => {
  const ladder = ladderFor(mode);
  const lapses = (prevSrs && prevSrs.lapses) || 0;
  const reps = (prevSrs && prevSrs.reps) || 0;
  if (!correct) {
    return { box: 0, reps: reps + 1, lapses: lapses + 1,
             due: dayStart(Date.now()) + ladder[0] * DAY };
  }
  const box = ((prevSrs && typeof prevSrs.box === 'number') ? prevSrs.box : -1) + 1;
  if (box >= ladder.length) {
    return { box, reps: reps + 1, lapses, due: null, graduated: true };
  }
  return { box, reps: reps + 1, lapses, due: dayStart(Date.now()) + ladder[box] * DAY };
};

// 진행률 상태 + 영속화 훅. record(q,sel,correct) 최초기록, update() 복습 재채점.
const saveProgress = (next) => {
  try { localStorage.setItem(PROGRESS_KEY, JSON.stringify(next)); } catch { /* quota/SSR */ }
  return next;
};

const useProgress = () => {
  const [progress, setProgress] = useState(loadProgress);
  const [srsMode, setSrsModeState] = useState(() => {
    try { return SRS_MODES[localStorage.getItem(SRS_MODE_KEY)] ? localStorage.getItem(SRS_MODE_KEY) : 'normal'; }
    catch { return 'normal'; }
  });
  const setSrsMode = (m) => {
    setSrsModeState(m);
    try { localStorage.setItem(SRS_MODE_KEY, m); } catch { /* SSR */ }
  };
  // 함수형 업데이트로 직전 상태 기준 병합 → 빠른 연속 응답에도 기록 유실 없음.
  // 최초 응답이 오답(채점됨)이면 즉시 복습 스케줄(srs) 부여.
  const record = (q, sel, correct) => {
    const id = qid(q);
    setProgress(prev => {
      if (prev[id]) return prev;
      const entry = { sel, correct, ts: Date.now() };
      if (correct === false) entry.srs = nextSrs(null, false, srsMode);
      return saveProgress({ ...prev, [id]: entry });
    });
  };
  // 복습 재채점: 기존 기록 덮어씀 + 기억곡선 재스케줄. reviewed 누적.
  const update = (q, sel, correct) => {
    const id = qid(q);
    setProgress(prev => {
      const p = prev[id] || {};
      const srs = (correct === null || correct === undefined)
        ? p.srs                                   // 채점불가는 스케줄 변경 안 함
        : nextSrs(p.srs, correct === true, srsMode);
      return saveProgress({
        ...prev,
        [id]: { sel, correct, ts: Date.now(), reviewed: (p.reviewed || 0) + 1, srs },
      });
    });
  };
  const reset = () => setProgress(saveProgress({}));
  const clearMany = (ids) => {
    const set = new Set(ids);
    setProgress(prev => {
      const next = {};
      for (const k in prev) if (!set.has(k)) next[k] = prev[k];
      return saveProgress(next);
    });
  };
  return { progress, record, update, reset, clearMany, srsMode, setSrsMode };
};

// 문항 북마크 — 사유 태그(중요/헷갈림/실수). 정오답과 무관, 별도 영속
const BM_KEY = 'quiz-bookmarks-v1';
// 탭 시 사유 순환: 없음→중요→헷갈림→실수→없음
const BM_REASONS = ['important', 'confusing', 'mistake'];
const BM_META = {
  important: { label: '중요', icon: '★', color: '#f59e0b' },
  confusing: { label: '헷갈림', icon: '★', color: '#8b5cf6' },
  mistake:   { label: '실수', icon: '★', color: '#ef4444' },
};
const bmReasonOf = (v) => (typeof v === 'string' && BM_META[v]) ? v : (v ? 'important' : null); // 레거시(1)→중요
const loadBookmarks = () => {
  try { return JSON.parse(localStorage.getItem(BM_KEY) || '{}') || {}; }
  catch { return {}; }
};
const useBookmarks = () => {
  const [bm, setBm] = useState(loadBookmarks);
  const cycleBookmark = (q) => {
    const id = qid(q);
    setBm(prev => {
      const cur = bmReasonOf(prev[id]);
      const i = cur ? BM_REASONS.indexOf(cur) : -1;
      const nextReason = BM_REASONS[i + 1]; // 마지막 다음은 undefined → 해제
      const next = { ...prev };
      if (nextReason) next[id] = nextReason; else delete next[id];
      try { localStorage.setItem(BM_KEY, JSON.stringify(next)); } catch { /* quota/SSR */ }
      return next;
    });
  };
  return { bm, cycleBookmark };
};

// 문항 배열에 대한 진행 통계
const progressStats = (questions, progress) => {
  let answered = 0, correct = 0, scored = 0, dSum = 0, dCnt = 0;
  for (const q of questions) {
    if (typeof q.difficulty === 'number') { dSum += q.difficulty; dCnt++; }
    const p = progress[qid(q)];
    if (p) {
      answered++;
      if (p.correct === true) correct++;
      if (p.correct !== null && p.correct !== undefined) scored++; // 정답 정보 있는 채점 대상
    }
  }
  const avgDiff = dCnt ? dSum / dCnt : null;
  // accuracy: 채점 가능한(scored) 문항 기준 정답률
  return {
    answered, correct, scored, total: questions.length,
    accuracy: scored ? Math.round((correct / scored) * 100) : null,
    avgDiff, level: avgDiff ? Math.round(avgDiff) : null,
  };
};

// ===== URL 라우팅 (해시 동기화) =====
// 네비게이션 계층을 #/seg/seg.. 로 직렬화. 빈 값은 '-'.
const NAV_KEYS = ['viewMode', 'currentView', 'scope', 'taxSubject', 'taxSubSubject', 'taxChapter', 'taxSection'];
const enc = (v) => (v == null || v === '' ? '-' : encodeURIComponent(v));
const dec = (v) => (v == null || v === '-' ? null : decodeURIComponent(v));

const serializeNav = (s) => {
  const scope = s.taxScope ? `${s.taxScope.kind}~${s.taxScope.value}` : null;
  const parts = [s.viewMode, s.currentView, scope, s.taxSubject, s.taxSubSubject, s.taxChapter, s.taxSection];
  return '#/' + parts.map(enc).join('/');
};

const parseNav = (hash) => {
  if (!hash || !hash.startsWith('#/')) return null;
  const segs = hash.slice(2).split('/');
  if (segs.length < 2) return null;
  const obj = {};
  NAV_KEYS.forEach((k, i) => { obj[k] = dec(segs[i]); });
  let taxScope = null;
  if (obj.scope) {
    const [kind, ...rest] = obj.scope.split('~');
    const value = rest.join('~');
    if (kind === 'exam' || kind === 'year') {
      taxScope = { kind, value, label: kind === 'year' ? `${value}년` : value };
    }
  }
  return {
    viewMode: obj.viewMode || 'exam',
    currentView: obj.currentView || 'home',
    taxScope,
    taxSubject: obj.taxSubject,
    taxSubSubject: obj.taxSubSubject,
    taxChapter: obj.taxChapter,
    taxSection: obj.taxSection,
  };
};

// 소실 이미지를 깨진 아이콘 대신 안내로 표시 (React 상태로 안전 처리)
const SafeImage = ({ src }) => {
  const [errored, setErrored] = useState(false);
  const [zoom, setZoom] = useState(false);
  if (errored) {
    return <span style={{ display: 'inline-block', color: '#9ca3af', fontSize: '0.85rem', padding: '8px 0' }}>[이미지 없음]</span>;
  }
  return (
    <>
      <img
        src={src}
        alt="content"
        loading="lazy"
        decoding="async"
        className="q-img"
        onClick={() => setZoom(true)}
        onError={() => setErrored(true)}
        style={{ maxWidth: '100%', display: 'block', margin: '12px auto', borderRadius: '4px' }}
      />
      {zoom && (
        <div className="lightbox" role="dialog" aria-label="이미지 확대" onClick={() => setZoom(false)}>
          <button className="lightbox-close" aria-label="닫기" onClick={() => setZoom(false)}>✕</button>
          <img src={src} alt="확대 이미지" onClick={(e) => e.stopPropagation()} />
        </div>
      )}
    </>
  );
};

// Component to parse and render text with inline images and math
const ParsedText = ({ text }) => {
  if (!text) return null;
  const parts = text.split(/(\[IMAGE:\s*.*?\])/g);
  return (
    <>
      {parts.map((part, i) => {
        const imgMatch = part.match(/\[IMAGE:\s*(.*?)\]/);
        if (imgMatch) {
          const rawName = imgMatch[1].split('/').pop();
          // PNG/GIF는 빌드 시 동일 파일명의 WebP로 변환됨(확장자만 교체).
          const imageName = rawName.replace(/\.(png|gif)$/i, '.webp');
          return <SafeImage key={i} src={`/images/${imageName}`} />;
        }
        
        // Render math in the text part
        const mathParts = part.split(/(\$[\s\S]*?\$)/g);
        return mathParts.map((mathPart, j) => {
          if (mathPart.startsWith('$') && mathPart.endsWith('$')) {
            const math = mathPart.slice(1, -1);
            try {
              const html = katex.renderToString(math, { 
                throwOnError: false,
                output: 'html' // Only output HTML to prevent duplicate text when copy-pasting
              });
              return <span key={`${i}-${j}`} dangerouslySetInnerHTML={{ __html: html }} />;
            } catch {
              return <span key={`${i}-${j}`}>{mathPart}</span>;
            }
          }
          return <span key={`${i}-${j}`}>{mathPart}</span>;
        });
      })}
    </>
  );
};

// Interactive Question Component
const QuestionItem = ({ q, prior, onAnswer, bmReason, onToggleBookmark, keyboard }) => {
  const [selectedOpt, setSelectedOpt] = useState(prior ? (prior.sel ?? null) : null);
  const isRevealed = selectedOpt !== null;
  const hasAnswer = !!q.answerNorm;          // 정답 정보가 유효한 문항인가
  const noOptions = !q.options || q.options.length === 0;

  const handleOptionClick = (optIdx) => {
    if (isRevealed) return; // 응답 후 변경 방지
    const sel = String(optIdx + 1);
    setSelectedOpt(sel);
    const correct = hasAnswer ? sel === q.answerNorm : null;
    // 햅틱: 정답 짧게, 오답 패턴 진동 (지원 기기에서만)
    try {
      if (correct === true && navigator.vibrate) navigator.vibrate(18);
      else if (correct === false && navigator.vibrate) navigator.vibrate([35, 30, 35]);
    } catch { /* 미지원 */ }
    // correct: 정답 있으면 boolean, 없으면 null(채점 제외)
    if (onAnswer) onAnswer(q, sel, correct);
  };

  // 가이드 학습: 숫자키 1~9로 보기 선택(단일 문항 표시 화면에서만)
  useEffect(() => {
    if (!keyboard || isRevealed || noOptions) return;
    const onKey = (e) => {
      const tag = e.target && e.target.tagName;
      if (tag && /^(INPUT|TEXTAREA|SELECT)$/.test(tag)) return;
      const n = parseInt(e.key, 10);
      if (n >= 1 && n <= q.options.length) handleOptionClick(n - 1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [keyboard, isRevealed, noOptions, q]);

  return (
    <div style={{ background: '#fff', borderRadius: '12px', padding: '24px', marginBottom: '24px', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', gap: '8px' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontWeight: '700', fontSize: '1.125rem', color: '#2563eb' }}>Q. {q.number}</span>
          {typeof q.difficulty === 'number' && (() => {
            const m = DIFFICULTY_META[q.difficulty] || DIFFICULTY_META[3];
            return (
              <span style={{
                fontSize: '0.75rem', fontWeight: 700, padding: '2px 8px', borderRadius: '999px',
                background: m.bg, color: m.fg
              }}>
                {m.label}
              </span>
            );
          })()}
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '0.875rem', color: '#9ca3af' }}>
            {q.exam} {q.year}년 {q.number}번
          </span>
          {onToggleBookmark && (() => {
            const m = bmReason ? BM_META[bmReason] : null;
            return (
              <button
                onClick={() => onToggleBookmark(q)}
                aria-label="북마크"
                title={m ? `북마크: ${m.label} (탭하여 변경)` : '북마크 (중요→헷갈림→실수)'}
                style={{ border: 'none', background: 'none', cursor: 'pointer', display: 'flex',
                  alignItems: 'center', gap: '3px', padding: 0, lineHeight: 1,
                  color: m ? m.color : '#d1d5db' }}
              >
                <span style={{ fontSize: '1.2rem' }}>{m ? m.icon : '☆'}</span>
                {m && <span style={{ fontSize: '0.7rem', fontWeight: 700 }}>{m.label}</span>}
              </button>
            );
          })()}
        </span>
      </div>
      
      <h3 className="q-text" style={{ lineHeight: '1.6', marginBottom: '20px', fontWeight: '600' }}>
        <ParsedText text={q.question} />
      </h3>
      
      {noOptions && (
        <div style={{ padding: '16px', background: '#fff7ed', border: '1px solid #fed7aa', borderRadius: '8px', color: '#9a3412', fontSize: '0.9rem', marginBottom: '24px' }}>
          이 문항은 보기가 공개되지 않아 지문·해설 위주로 학습해요.
        </div>
      )}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
        {!noOptions && q.options.map((opt, optIdx) => {
          const optNumber = String(optIdx + 1);
          const isCorrectAnswer = hasAnswer && q.answerNorm === optNumber;
          const isSelected = selectedOpt === optNumber;

          const showCorrect = isRevealed && isCorrectAnswer;
          const showWrong = isRevealed && isSelected && !isCorrectAnswer;

          let bgColor, borderColor, badgeBg = '#fff', badgeColor = '#4b5563', badgeBorder = '1.5px solid #d1d5db';
          let anim = '';
          if (showCorrect) {
            bgColor = '#eff6ff'; borderColor = '#93c5fd'; badgeBg = '#2563eb'; badgeColor = '#fff'; badgeBorder = 'none';
            anim = 'opt-correct';
          } else if (showWrong) {
            bgColor = '#fef2f2'; borderColor = '#fca5a5'; badgeBg = '#dc2626'; badgeColor = '#fff'; badgeBorder = 'none';
            anim = 'opt-wrong';
          } else {
            bgColor = '#f9fafb'; borderColor = '#e5e7eb';
            if (isRevealed) { bgColor = '#fff'; }
          }

          return (
            <button
              key={optIdx}
              type="button"
              className={`opt-btn ${anim}`.trim()}
              onClick={() => handleOptionClick(optIdx)}
              disabled={isRevealed}
              aria-pressed={isSelected}
              aria-label={`${optIdx + 1}번 보기${showCorrect ? ' (정답)' : showWrong ? ' (오답·내 선택)' : ''}`}
              style={{ background: bgColor, borderColor }}
            >
              <span style={{
                display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                width: '26px', height: '26px', borderRadius: '50%',
                background: badgeBg, color: badgeColor, border: badgeBorder,
                fontSize: '0.875rem', fontWeight: '700', flexShrink: 0
              }}>
                {showCorrect ? '✓' : showWrong ? '✕' : optIdx + 1}
              </span>
              <span className="q-opt" style={{ lineHeight: '1.5', color: '#1f2937' }}>
                <ParsedText text={opt} />
              </span>
            </button>
          );
        })}
      </div>
      
      {isRevealed && (() => {
        // 채점 결과: 정답 정보 없으면 중립 안내, 있으면 정/오답
        const correct = hasAnswer && selectedOpt === q.answerNorm;
        const accent = !hasAnswer ? '#6b7280' : (correct ? '#16a34a' : '#ef4444');
        return (
          <div className="result-box" style={{ padding: '16px', background: '#f3f4f6', borderRadius: '8px', borderLeft: `4px solid ${accent}` }}>
            <div style={{ fontWeight: '700', marginBottom: q.explanation ? '8px' : '0', fontSize: '0.95rem', display: 'flex', justifyContent: 'space-between' }}>
              <span>{q.explanation ? '해설' : '결과'}</span>
              <span style={{ color: accent }}>
                {!hasAnswer ? 'ℹ 공식 정답 미공개 · 해설로 학습' : (correct ? '✓ 정답입니다!' : '✕ 오답입니다.')}
              </span>
            </div>
            {q.explanation
              ? <div className="q-exp" style={{ lineHeight: '1.6', color: '#4b5563' }}><ParsedText text={q.explanation} /></div>
              : (hasAnswer && <div style={{ fontSize: '0.9rem', color: '#6b7280' }}>정답: {q.answerNorm}번</div>)}
          </div>
        );
      })()}
    </div>
  );
};

const App = () => {
  const [questionsData, setQuestionsData] = useState([]);
  const [taxonomyData, setTaxonomyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadPct, setLoadPct] = useState(0);
  const [loadError, setLoadError] = useState(false);
  // 새로고침/딥링크 복원: 최초 렌더에서 URL 해시를 1회 파싱해 초기 상태로 사용
  const [bootNav] = useState(() => parseNav(typeof window !== 'undefined' ? window.location.hash : ''));
  const bootView = (() => {
    if (!bootNav) return 'home';
    let cv = bootNav.currentView;
    if (cv === 'question_list' || cv === 'study') {
      if (bootNav.taxSection) cv = 'tax_items';
      else if (bootNav.taxChapter) cv = 'tax_sections';
      else if (bootNav.taxSubSubject) cv = 'tax_chapters';
      else if (bootNav.taxSubject) cv = 'tax_sub_subjects';
      else if (bootNav.taxScope) cv = 'tax_subjects';
      else cv = 'dashboard';
    }
    return cv;
  })();

  const [viewMode, setViewMode] = useState(bootNav?.viewMode || 'exam'); // 'exam' | 'subject' | 'year' | 'chapter'
  const [currentView, setCurrentView] = useState(bootView);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [studyIdx, setStudyIdx] = useState(0); // 가이드 학습 모드 현재 문항 인덱스
  const [studyNonce, setStudyNonce] = useState(0); // 재학습 시 문항 카드 강제 리마운트
  const [autoNext, setAutoNextState] = useState(() => {
    try { return localStorage.getItem('quiz-autonext') === '1'; } catch { return false; }
  });
  const setAutoNext = (v) => {
    setAutoNextState(v);
    try { localStorage.setItem('quiz-autonext', v ? '1' : '0'); } catch { /* SSR */ }
  };
  const [autoSec, setAutoSecState] = useState(() => {
    try { const n = parseInt(localStorage.getItem('quiz-autosec'), 10); return [3, 5, 8].includes(n) ? n : 5; }
    catch { return 5; }
  });
  const setAutoSec = (n) => {
    setAutoSecState(n);
    try { localStorage.setItem('quiz-autosec', String(n)); } catch { /* SSR */ }
  };
  const autoTimerRef = useRef(null);
  const fileRef = useRef(null);
  const onImportFile = (e) => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    const r = new FileReader();
    r.onload = () => {
      try { importUserData(String(r.result)); alert('가져오기 완료. 새로고침합니다.'); window.location.reload(); }
      catch (err) { alert('가져오기 실패: ' + err.message); }
    };
    r.readAsText(f);
  };
  const clearAutoTimer = () => { if (autoTimerRef.current) { clearTimeout(autoTimerRef.current); autoTimerRef.current = null; } };
  const [autoPending, setAutoPending] = useState(false); // 자동 다음 대기 표시
  const [studyOrder, setStudyOrderState] = useState(() => {
    try { return localStorage.getItem('quiz-study-order') === 'random' ? 'random' : 'difficulty'; }
    catch { return 'difficulty'; }
  });
  const setStudyOrder = (o) => {
    setStudyOrderState(o);
    try { localStorage.setItem('quiz-study-order', o); } catch { /* SSR */ }
  };
  const [reviewSubject, setReviewSubject] = useState(null); // 오답 복습 2단계 드릴(과목 선택)
  const [nowTs] = useState(() => Date.now()); // 세션 기준 현재시각(렌더 순수성)
  const [trendDays, setTrendDays] = useState(7); // 학습 추이 기간(7|30)
  const [dailyGoal, setDailyGoalState] = useState(() => {
    try { const n = parseInt(localStorage.getItem('quiz-daily-goal'), 10); return [10, 20, 30, 50].includes(n) ? n : 20; }
    catch { return 20; }
  });
  const setDailyGoal = (n) => {
    setDailyGoalState(n);
    try { localStorage.setItem('quiz-daily-goal', String(n)); } catch { /* SSR */ }
  };
  const [nickname, setNicknameState] = useState(() => loadProfile().nickname || '');
  const setNickname = (v) => {
    setNicknameState(v);
    saveProfile({ ...loadProfile(), nickname: v });
  };

  // 클라우드 동기화(선택)
  const [authUser, setAuthUser] = useState(null);
  const [cloudMsg, setCloudMsg] = useState('');
  const [cloudEmail, setCloudEmail] = useState('');
  const [cloudPw, setCloudPw] = useState('');
  const cloudAuth = async (mode) => {
    setCloudMsg('처리 중…');
    try {
      const creds = { email: cloudEmail.trim(), password: cloudPw };
      const { error } = mode === 'signup'
        ? await supabase.auth.signUp(creds)
        : await supabase.auth.signInWithPassword(creds);
      if (error) throw error;
      setCloudPw('');
      setCloudMsg(mode === 'signup' ? '가입 완료. 로그인되었어요.' : '로그인되었어요.');
    } catch (e) { setCloudMsg((e.message || String(e))); }
  };
  useEffect(() => {
    if (!supabase) return;
    supabase.auth.getSession().then(({ data }) => setAuthUser(data?.session?.user || null));
    const { data: sub } = supabase.auth.onAuthStateChange((_e, session) => setAuthUser(session?.user || null));
    return () => sub?.subscription?.unsubscribe();
  }, []);
  const cloudPush = useCallback(async (silent) => {
    try {
      const at = await pushState(collectUserData());
      saveProfile({ ...loadProfile(), lastCloud: at });
      if (!silent) setCloudMsg('클라우드에 백업했어요.');
    } catch (e) { if (!silent) setCloudMsg('백업 실패: ' + (e.message || e)); }
  }, []);
  const cloudPull = useCallback(async () => {
    try {
      const row = await pullState();
      if (!row || !row.data) { setCloudMsg('클라우드에 저장된 기록이 없어요.'); return; }
      if (!window.confirm('클라우드 기록으로 이 기기를 덮어쓸까요? 현재 진행은 사라집니다.')) return;
      importUserData(JSON.stringify(row.data));
      window.location.reload();
    } catch (e) { setCloudMsg('불러오기 실패: ' + (e.message || e)); }
  }, []);
  // 로그인 중이면 앱이 백그라운드로 갈 때 자동 백업
  useEffect(() => {
    if (!supabase || !authUser) return;
    const onHide = () => { if (document.visibilityState === 'hidden') cloudPush(true); };
    document.addEventListener('visibilitychange', onHide);
    return () => document.removeEventListener('visibilitychange', onHide);
  }, [authUser, cloudPush]);
  const [notifPref, setNotifPref] = useState(() => {
    try { return localStorage.getItem('quiz-notif') === '1' && typeof Notification !== 'undefined' && Notification.permission === 'granted'; }
    catch { return false; }
  });
  useEffect(() => {
    try { localStorage.setItem('quiz-notif', notifPref ? '1' : '0'); } catch { /* SSR */ }
  }, [notifPref]);
  // B1: 본문 글자 크기(작게 0.9 / 보통 1 / 크게 1.18). --q-fs CSS 변수로 반영.
  const [fontScale, setFontScaleState] = useState(() => {
    try { const n = parseFloat(localStorage.getItem('quiz-fontscale')); return [0.9, 1, 1.18].includes(n) ? n : 1; }
    catch { return 1; }
  });
  const setFontScale = (n) => {
    setFontScaleState(n);
    try { localStorage.setItem('quiz-fontscale', String(n)); } catch { /* SSR */ }
  };
  useEffect(() => {
    try { document.documentElement.style.setProperty('--q-fs', String(fontScale)); } catch { /* SSR */ }
  }, [fontScale]);
  // C2: 문항 목록으로 돌아오면 직전 스크롤 위치 복원
  useEffect(() => {
    if (currentView !== 'question_list') return;
    const y = scrollMem.qlist;
    if (y > 0) requestAnimationFrame(() => window.scrollTo(0, y));
  }, [currentView]);
  // A4: 목표 달성 컨페티(하루 1회)
  const [confetti, setConfetti] = useState(false);

  const { progress, record: recordAnswer, update: updateAnswer, reset: resetProgress, clearMany, srsMode, setSrsMode } = useProgress();
  const { bm, cycleBookmark } = useBookmarks();
  // 복합 검색·필터 상태
  const [filters, setFilters] = useState(loadFilters);

  // taxonomy states
  const [taxSubject, setTaxSubject] = useState(bootNav?.taxSubject || null);
  const [taxSubSubject, setTaxSubSubject] = useState(bootNav?.taxSubSubject || null);
  const [taxChapter, setTaxChapter] = useState(bootNav?.taxChapter || null);
  const [taxSection, setTaxSection] = useState(bootNav?.taxSection || null);
  // 시험별/연도별 진입 시 적용되는 분류 스코프: null | {kind:'exam'|'year', value, label}
  const [taxScope, setTaxScope] = useState(bootNav?.taxScope || null);

  // 데이터 불러오기 — 큰 questions_db는 스트리밍해 실제 진행률 표시
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [qRes, tData] = await Promise.all([
          fetch('/data/questions_db.json'),
          fetch('/data/taxonomy.json').then(r => r.json()),
        ]);
        if (!qRes.ok) throw new Error('questions_db ' + qRes.status);
        const total = parseInt(qRes.headers.get('content-length') || '0', 10);
        let qData;
        if (qRes.body && total > 0) {
          const reader = qRes.body.getReader();
          const chunks = [];
          let received = 0;
          for (;;) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            received += value.length;
            if (!cancelled) setLoadPct(Math.min(99, Math.round((received / total) * 100)));
          }
          const buf = new Uint8Array(received);
          let off = 0;
          for (const c of chunks) { buf.set(c, off); off += c.length; }
          qData = JSON.parse(new TextDecoder().decode(buf));
        } else {
          qData = await qRes.json(); // content-length 없으면(캐시/압축) 일반 파싱
        }
        if (cancelled) return;
        setLoadPct(100);
        setQuestionsData(qData);
        setTaxonomyData(tData);
        setLoading(false);
      } catch (err) {
        console.error('데이터 로딩 실패:', err);
        if (cancelled) return;
        setLoadError(true);
        setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, []);

  // ----- URL 라우팅: 해시 ↔ 네비게이션 상태 동기 -----
  const hydratedRef = useRef(false);

  const applyNav = useCallback((n) => {
    if (!n) return;
    setViewMode(n.viewMode);
    setTaxScope(n.taxScope);
    setTaxSubject(n.taxSubject);
    setTaxSubSubject(n.taxSubSubject);
    setTaxChapter(n.taxChapter);
    setTaxSection(n.taxSection);
    setSelectedGroup(null);
    // 문제목록은 filterFn 직렬화가 불가 → 가장 가까운 상위 목록으로 복원
    let cv = n.currentView;
    if (cv === 'question_list' || cv === 'study') {
      if (n.taxSection) cv = 'tax_items';
      else if (n.taxChapter) cv = 'tax_sections';
      else if (n.taxSubSubject) cv = 'tax_chapters';
      else if (n.taxSubject) cv = 'tax_sub_subjects';
      else if (n.taxScope) cv = 'tax_subjects';
      else cv = 'dashboard';
    }
    setCurrentView(cv);
  }, []);

  // popstate(브라우저 뒤로/앞으로) 구독. 초기 상태는 이미 해시에서 복원됨.
  useEffect(() => {
    hydratedRef.current = true;
    const onPop = () => applyNav(parseNav(window.location.hash));
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, [applyNav]);

  // 네비게이션 상태 변경 → 해시 push (딥링크/뒤로가기 지원)
  useEffect(() => {
    if (!hydratedRef.current) return;
    const hash = serializeNav({ viewMode, currentView, taxScope, taxSubject, taxSubSubject, taxChapter, taxSection });
    if (hash !== window.location.hash) {
      window.history.pushState(null, '', hash);
    }
  }, [viewMode, currentView, taxScope, taxSubject, taxSubSubject, taxChapter, taxSection]);

  // 검색·필터 영속화: 변경 시 localStorage 저장 (새로고침 후 복원)
  useEffect(() => {
    try { localStorage.setItem(FILTERS_KEY, JSON.stringify(filters)); } catch { /* quota/SSR */ }
  }, [filters]);

  // Process data
  const processedData = useMemo(() => {
    if (loading || !questionsData) return [];
    return questionsData.map(q => {
      // V4 분류 정보: Gemini 또는 Claude로 분류되어 mapped_taxonomy가 있고
      // in_scope!==false 인 문제만 전 탭(시험/과목/단원/연도)에 노출.
      const iv = q.indexing_v4;
      const mt = iv && iv.mapped_taxonomy;
      const isClassified = !!(
        iv && mt && mt.subject &&
        (iv.processed_by === 'gemini-2.5-flash' || iv.processed_by === 'claude-sonnet-4-6') &&
        iv.in_scope !== false
      );

      const opts = q.options || q.choices || [];
      return {
        ...q,
        year: q.year || '2025',
        exam: q.exam || '감정평가사',
        options: opts, // options / choices 통일
        // 정답 정규화: 원문자(①②③..)→숫자, 1..보기수 범위만 유효, 그 외(빈/센티넬)는 null
        answerNorm: normAnswer(q.answer, opts.length),
        // 실제 v4 난이도(1~5). 분류 전이면 null. 4 이상을 '취약'으로 간주.
        difficulty: (iv && typeof iv.difficulty === 'number') ? iv.difficulty : null,
        isWeak: !!(iv && typeof iv.difficulty === 'number' && iv.difficulty >= 4),
        // v4 mapped_taxonomy 기반 분류 필드 (모든 탭이 공유하는 단일 분류축)
        isClassified,
        taxSubjectName: isClassified ? mt.subject : null,
        taxSubSubjectName: isClassified ? (mt.sub_subject || null) : null,
        taxChapterName: isClassified ? (mt.chapter || null) : null,
        taxSectionName: isClassified ? (mt.section || null) : null,
        taxItemName: isClassified ? (mt.item || null) : null,
      };
    });
  }, [loading, questionsData]);

  // 가이드 학습: 키보드 ← 이전 / → · Enter 다음
  useEffect(() => {
    if (currentView !== 'study' || !selectedGroup) return;
    const onKey = (e) => {
      const tag = e.target && e.target.tagName;
      if (tag && /^(INPUT|TEXTAREA|SELECT)$/.test(tag)) return;
      if (e.key === 'ArrowLeft') {
        setStudyIdx(i => Math.max(0, i - 1)); window.scrollTo(0, 0);
      } else if (e.key === 'ArrowRight' || e.key === 'Enter') {
        const n = processedData.filter(selectedGroup.filterFn).length;
        setStudyIdx(i => Math.min(Math.max(0, n - 1), i + 1)); window.scrollTo(0, 0);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [currentView, selectedGroup, processedData]);

  // 가이드 학습 위치 영속화(비복습 세션만) → 이어풀기
  useEffect(() => {
    if (currentView !== 'study' || !selectedGroup || selectedGroup.review || !selectedGroup.posKey) return;
    const map = loadPos();
    if (studyIdx > 0) map[selectedGroup.posKey] = studyIdx;
    else delete map[selectedGroup.posKey];
    savePos(map);
  }, [currentView, selectedGroup, studyIdx]);

  // ===== 단일 v4 분류축 엔진 =====
  // 모든 탭(시험별/과목별/단원별/연도별)이 동일한 mapped_taxonomy 분류축을 공유한다.
  // taxScope: null(과목별/단원별) | {kind:'exam'|'year', value, label} (시험별/연도별 진입 시)
  const baseFilter = useCallback((item) => {
    if (!item.isClassified) return false;
    if (!taxScope) return true;
    if (taxScope.kind === 'exam') return item.exam === taxScope.value;
    if (taxScope.kind === 'year') return String(item.year) === String(taxScope.value);
    return true;
  }, [taxScope]);

  const scopedClassified = useMemo(
    () => processedData.filter(baseFilter),
    [processedData, baseFilter]
  );

  // Level 0: 연도 목록 (연도별 탭) — 분류 완료 문항만 집계
  const yearGroups = useMemo(() => {
    const groups = {};
    processedData.forEach(q => {
      if (!q.isClassified) return;
      const key = q.year;
      if (!groups[key]) {
        groups[key] = {
          type: 'year_group',
          title: `${q.year}년`,
          subtitle: '기출연도',
          total: 0,
          weak: false,
          tag: '기출',
          rawValue: q.year
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    return Object.values(groups).sort((a, b) => parseInt(b.rawValue) - parseInt(a.rawValue));
  }, [processedData]);

  // Level 0: 시험 목록 (시험별 탭) — 분류 완료 문항만 집계
  const examGroups = useMemo(() => {
    const groups = {};
    processedData.forEach(q => {
      if (!q.isClassified) return;
      const key = q.exam;
      if (!groups[key]) {
        groups[key] = {
          type: 'exam',
          title: q.exam,
          subtitle: '자격시험',
          total: 0,
          weak: false,
          tag: '기출문제'
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    return Object.values(groups).sort((a, b) => b.total - a.total);
  }, [processedData]);

  // 과목(taxonomy subject) 목록 — 시험별/과목별/단원별/연도별 공용 (scope 반영)
  const taxSubjectGroups = useMemo(() => {
    if (!taxonomyData) return [];
    return Object.keys(taxonomyData).map(subj => {
      const filtered = scopedClassified.filter(q => q.taxSubjectName === subj);
      return {
        type: 'tax_subject',
        title: subj,
        subtitle: taxScope ? taxScope.label : '단원별 학습',
        total: filtered.length,
        weak: filtered.some(q => q.isWeak),
        tag: '과목'
      };
    }).filter(g => g.total > 0);
  }, [taxonomyData, scopedClassified, taxScope]);

  // 세부과목 또는 장(Chapter) 목록 (scope 반영)
  const taxSubSubjectGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject) return [];
    const subjData = taxonomyData[taxSubject];
    const filtered = scopedClassified.filter(q => q.taxSubjectName === taxSubject);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSubject} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject
    });

    if (subjData.has_subjects) {
      Object.keys(subjData.subjects).forEach(subSubj => {
        const sub = filtered.filter(q => q.taxSubSubjectName === subSubj);
        if (sub.length === 0) return;
        groups.push({
          type: 'tax_sub_subject',
          title: subSubj,
          subtitle: taxSubject,
          total: sub.length,
          weak: sub.some(q => q.isWeak),
          tag: '세부과목'
        });
      });
    } else {
      subjData.chapters.forEach(ch => {
        const chFiltered = filtered.filter(q => q.taxChapterName === ch.name);
        if (chFiltered.length === 0) return;
        groups.push({
          type: 'tax_chapter',
          title: ch.name,
          subtitle: taxSubject,
          total: chFiltered.length,
          weak: chFiltered.some(q => q.isWeak),
          tag: 'PART/장',
          filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxChapterName === ch.name
        });
      });
    }
    return groups;
  }, [taxonomyData, taxSubject, scopedClassified, baseFilter]);

  // 장(Chapter) 목록 (세부과목이 있는 경우, scope 반영)
  const taxChapterGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxSubSubject) return [];
    const subjData = taxonomyData[taxSubject];
    const chapters = subjData.subjects[taxSubSubject] || [];
    const filtered = scopedClassified.filter(q =>
      q.taxSubjectName === taxSubject && q.taxSubSubjectName === taxSubSubject);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSubSubject} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSubSubjectName === taxSubSubject
    });
    chapters.forEach(ch => {
      const chFiltered = filtered.filter(q => q.taxChapterName === ch.name);
      if (chFiltered.length === 0) return;
      groups.push({
        type: 'tax_chapter',
        title: ch.name,
        subtitle: taxSubSubject,
        total: chFiltered.length,
        weak: chFiltered.some(q => q.isWeak),
        tag: 'PART/장',
        filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxChapterName === ch.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, scopedClassified, baseFilter]);

  // 절(Section) 목록 — 절은 클릭 시 관(item) 목록으로 진입 (scope 반영)
  const taxSectionGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxChapter) return [];
    const subjData = taxonomyData[taxSubject];
    let chapters = [];
    if (subjData.has_subjects && taxSubSubject) {
      chapters = subjData.subjects[taxSubSubject];
    } else if (!subjData.has_subjects) {
      chapters = subjData.chapters;
    }
    const chapterData = chapters.find(c => c.name === taxChapter);
    if (!chapterData || !chapterData.sections) return [];

    const filtered = scopedClassified.filter(q =>
      q.taxSubjectName === taxSubject && q.taxChapterName === taxChapter);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxChapter} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxChapterName === taxChapter
    });

    chapterData.sections.forEach(sec => {
      const secQs = filtered.filter(q => q.taxSectionName === sec.name);
      if (secQs.length === 0) return;
      const hasItems = (sec.items || []).some(it =>
        secQs.some(q => q.taxItemName === it.name));
      groups.push({
        // 관(item) 단위 분류가 있으면 진입형(tax_section), 없으면 바로 풀기(play_all_tax)
        type: hasItems ? 'tax_section' : 'play_all_tax',
        title: sec.name,
        subtitle: taxChapter,
        total: secQs.length,
        weak: secQs.some(q => q.isWeak),
        tag: '절',
        filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSectionName === sec.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, taxChapter, scopedClassified, baseFilter]);

  // 관(item) 목록 — 최저 분류 단위 (scope 반영)
  const taxItemGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxChapter || !taxSection) return [];
    const subjData = taxonomyData[taxSubject];
    let chapters = [];
    if (subjData.has_subjects && taxSubSubject) {
      chapters = subjData.subjects[taxSubSubject];
    } else if (!subjData.has_subjects) {
      chapters = subjData.chapters;
    }
    const chapterData = chapters.find(c => c.name === taxChapter);
    const sectionData = chapterData && (chapterData.sections || []).find(s => s.name === taxSection);
    if (!sectionData) return [];

    const filtered = scopedClassified.filter(q =>
      q.taxSubjectName === taxSubject && q.taxSectionName === taxSection);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSection} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSectionName === taxSection
    });

    (sectionData.items || []).forEach(it => {
      const itQs = filtered.filter(q => q.taxItemName === it.name);
      if (itQs.length === 0) return;
      groups.push({
        type: 'play_all_tax',
        title: it.name,
        subtitle: taxSection,
        total: itQs.length,
        weak: itQs.some(q => q.isWeak),
        tag: '관',
        filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSectionName === taxSection && item.taxItemName === it.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, taxChapter, taxSection, scopedClassified, baseFilter]);

  // 4개 탭 모두 동일 v4 분류축 사용. 시험별/연도별은 picker → 스코프 설정 후 동일 엔진.
  let activeGroups = [];
  if (viewMode === 'subject' || viewMode === 'chapter') activeGroups = taxSubjectGroups;
  else if (viewMode === 'year') activeGroups = yearGroups;
  else if (viewMode === 'exam') activeGroups = examGroups;

  const classifiedList = useMemo(
    () => processedData.filter(q => q.isClassified),
    [processedData]
  );

  const bookmarkedList = useMemo(
    () => classifiedList.filter(q => bm[qid(q)]),
    [classifiedList, bm]
  );

  // 오답(채점 결과 false) 집합 + 과목별 그룹
  const wrongList = useMemo(
    () => classifiedList.filter(q => { const p = progress[qid(q)]; return p && p.correct === false; }),
    [classifiedList, progress]
  );
  const reviewGroups = useMemo(() => {
    const by = {};
    for (const q of wrongList) {
      const k = q.taxSubjectName || '기타';
      (by[k] || (by[k] = [])).push(q);
    }
    return Object.entries(by)
      .map(([subj, qs]) => ({ subj, ids: qs.map(qid), count: qs.length }))
      .sort((a, b) => b.count - a.count);
  }, [wrongList]);

  // 기억곡선 스케줄: 오늘(이전 포함) 복습 도래분 + 다음 예정일
  const srs = useMemo(() => {
    const now = nowTs;
    const dueAllPairs = [];   // [{q, dueAt}]
    let next = null;          // 가장 이른 미래 복습일(ms)
    for (const q of classifiedList) {
      const p = progress[qid(q)];
      if (!p) continue;
      // 레거시: 오답인데 srs 없으면 즉시 복습 대상으로 간주
      const s = p.srs || (p.correct === false ? { due: 0 } : null);
      if (!s || s.graduated) continue;
      if (s.due == null) continue;
      if (s.due <= now) dueAllPairs.push({ q, dueAt: s.due });
      else if (next == null || s.due < next) next = s.due;
    }
    // 하루 상한: 가장 오래 밀린 것부터 cap개, 초과분은 다음 기회로 이월
    dueAllPairs.sort((a, b) => a.dueAt - b.dueAt);
    const cap = (SRS_MODES[srsMode] || SRS_MODES.normal).cap;
    const dueTotal = dueAllPairs.length;
    const due = dueAllPairs.slice(0, cap === Infinity ? dueTotal : cap).map(x => x.q);
    const bysubj = {};
    for (const q of due) {
      const k = q.taxSubjectName || '기타';
      (bysubj[k] || (bysubj[k] = [])).push(q);
    }
    return {
      due, dueTotal, capped: dueTotal > due.length,
      groups: Object.entries(bysubj)
        .map(([subj, qs]) => ({ subj, ids: qs.map(qid), count: qs.length }))
        .sort((a, b) => b.count - a.count),
      nextDue: next,
    };
  }, [classifiedList, progress, nowTs, srsMode]);

  // 앱 열 때 알림: 권한 허용 + 옵트인 + 오늘 도래분 있음 + 당일 1회만.
  // (앱이 닫힌 상태의 백그라운드 푸시는 별도 서버/푸시 인프라 필요 → 범위 밖)
  useEffect(() => {
    if (!notifPref || loading || srs.due.length === 0) return;
    if (typeof Notification === 'undefined' || Notification.permission !== 'granted') return;
    const today = new Date().toDateString();
    try {
      if (localStorage.getItem('quiz-notif-last') === today) return;
      localStorage.setItem('quiz-notif-last', today);
    } catch { /* SSR */ }
    try {
      new Notification('오늘의 복습', { body: `기억 곡선에 따라 복습할 ${srs.due.length}문제가 있어요.` });
    } catch { /* 일부 브라우저는 SW 필요 */ }
  }, [notifPref, loading, srs.due.length]);

  // 복합 필터 선택지
  const filterOptions = useMemo(() => {
    const exams = new Set(), subjects = new Set(), years = new Set();
    for (const q of classifiedList) {
      exams.add(q.exam);
      if (q.taxSubjectName) subjects.add(q.taxSubjectName);
      years.add(String(q.year));
    }
    return {
      exams: [...exams].sort(),
      subjects: [...subjects].sort(),
      years: [...years].sort((a, b) => Number(b) - Number(a)),
      diffs: [1, 2, 3, 4, 5],
    };
  }, [classifiedList]);

  // 복합 필터 결과 (AND 결합, 키워드는 문제/보기/해설 OR 매칭)
  const filteredResults = useMemo(() => {
    const { exams, subjects, years, diffs, kw, cleanOnly } = filters;
    const active = exams.length || subjects.length || years.length || diffs.length || kw.trim() || cleanOnly;
    if (!active) return [];
    const k = kw.trim().toLowerCase();
    return classifiedList.filter(q => {
      if (exams.length && !exams.includes(q.exam)) return false;
      if (subjects.length && !subjects.includes(q.taxSubjectName)) return false;
      if (years.length && !years.includes(String(q.year))) return false;
      if (diffs.length && !diffs.includes(q.difficulty)) return false;
      if (cleanOnly) {
        const dq = q.data_quality || {};
        if (dq.no_answer || dq.no_options) return false;   // 채점 가능 문항만
      }
      if (k) {
        const hay = `${q.question || ''} ${(q.options || []).join(' ')} ${q.explanation || ''}`.toLowerCase();
        if (!hay.includes(k)) return false;
      }
      return true;
    });
  }, [classifiedList, filters]);

  const toggleFilter = (key, val) => setFilters(f => {
    const arr = f[key];
    return { ...f, [key]: arr.includes(val) ? arr.filter(x => x !== val) : [...arr, val] };
  });
  const clearFilters = () => setFilters({ ...EMPTY_FILTERS });
  const totalQuestions = classifiedList.length;
  const overall = useMemo(
    () => progressStats(classifiedList, progress),
    [classifiedList, progress]
  );

  // 학습 분석: 과목·절별 성취도, 난이도별 정답률, 연속 학습일, 약점 도출
  const analytics = useMemo(() => {
    const subj = {};   // subjectName -> {total,scored,correct, sec:{secName:{scored,correct,ids[]}}}
    const diff = {};   // 1..5 -> {scored,correct}
    const days = new Set();
    const dayAgg = {};  // dateString -> {count, scored, correct}
    let todayCount = 0;
    const todayStr = new Date().toDateString();
    for (const q of classifiedList) {
      const sName = q.taxSubjectName || '기타';
      const s = subj[sName] || (subj[sName] = { total: 0, scored: 0, correct: 0, sec: {} });
      s.total++;
      const p = progress[qid(q)];
      if (!p) continue;
      if (p.ts) {
        const ds = new Date(p.ts).toDateString();
        days.add(ds);
        if (ds === todayStr) todayCount++;
        const da = dayAgg[ds] || (dayAgg[ds] = { count: 0, scored: 0, correct: 0 });
        da.count++;
        if (p.correct === true || p.correct === false) { da.scored++; if (p.correct === true) da.correct++; }
      }
      if (p.correct === true || p.correct === false) {
        s.scored++; if (p.correct === true) s.correct++;
        const secName = q.taxSectionName || q.taxChapterName || '기타';
        const sc = s.sec[secName] || (s.sec[secName] = { scored: 0, correct: 0, ids: [] });
        sc.scored++; if (p.correct === true) sc.correct++; sc.ids.push(qid(q));
        if (typeof q.difficulty === 'number') {
          const d = diff[q.difficulty] || (diff[q.difficulty] = { scored: 0, correct: 0 });
          d.scored++; if (p.correct === true) d.correct++;
        }
      }
    }
    // 연속 학습일(오늘 또는 어제부터 역순으로 끊김 없이)
    let streak = 0;
    const cur = new Date(); cur.setHours(0, 0, 0, 0);
    if (!days.has(cur.toDateString())) cur.setDate(cur.getDate() - 1); // 오늘 안 했으면 어제부터
    while (days.has(cur.toDateString())) { streak++; cur.setDate(cur.getDate() - 1); }

    // 목표 달성: 일별 count >= dailyGoal
    const metDay = (d) => ((dayAgg[d.toDateString()] || {}).count || 0) >= dailyGoal;
    let goalStreak = 0;
    const gc = new Date(); gc.setHours(0, 0, 0, 0);
    if (!metDay(gc)) gc.setDate(gc.getDate() - 1);   // 오늘 미달이면 어제까지로 연속 판정
    while (metDay(gc)) { goalStreak++; gc.setDate(gc.getDate() - 1); }
    const weekMet = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - i);
      weekMet.push({ label: ['일', '월', '화', '수', '목', '금', '토'][d.getDay()], met: metDay(d), isToday: i === 0 });
    }

    const subjects = Object.entries(subj).map(([name, v]) => ({
      name, total: v.total, scored: v.scored, correct: v.correct,
      acc: v.scored ? Math.round((v.correct / v.scored) * 100) : null,
      // 가장 약한 절(채점 3+ & 정답률 최저)
      weakSection: Object.entries(v.sec)
        .filter(([, c]) => c.scored >= 3)
        .map(([nm, c]) => ({ nm, acc: c.correct / c.scored, ids: c.ids }))
        .sort((a, b) => a.acc - b.acc)[0] || null,
      allWrongUnseenIds: [], // 채워짐(아래)
    }));
    // 약점 과목: 채점 5+ 중 정답률 낮은 순
    const weak = subjects.filter(s => s.scored >= 5 && s.acc != null)
      .sort((a, b) => a.acc - b.acc).slice(0, 3);
    const diffAcc = [1, 2, 3, 4, 5].map(d => {
      const v = diff[d];
      return { d, scored: v ? v.scored : 0, acc: v && v.scored ? Math.round((v.correct / v.scored) * 100) : null };
    });
    // 최근 N일 학습 추이(문항의 최신 활동일 기준)
    const trend = [];
    for (let i = trendDays - 1; i >= 0; i--) {
      const dt = new Date(); dt.setHours(0, 0, 0, 0); dt.setDate(dt.getDate() - i);
      const a = dayAgg[dt.toDateString()] || { count: 0, scored: 0, correct: 0 };
      trend.push({
        // 7일이면 요일, 30일이면 라벨 생략(범위는 별도 표기)
        label: trendDays <= 7 ? ['일', '월', '화', '수', '목', '금', '토'][dt.getDay()] : '',
        isToday: i === 0,
        count: a.count,
        acc: a.scored ? Math.round((a.correct / a.scored) * 100) : null,
      });
    }
    const trendMax = Math.max(1, ...trend.map(t => t.count));
    const trendSum = trend.reduce((n, t) => n + t.count, 0);
    return { subjects, weak, diffAcc, streak, goalStreak, weekMet, todayCount, studiedDays: days.size, trend, trendMax, trendSum };
  }, [classifiedList, progress, trendDays, dailyGoal]);

  // A4: 오늘 목표 도달 시 컨페티 1회(하루 1번만)
  useEffect(() => {
    if (analytics.todayCount < dailyGoal) return;
    const today = new Date().toDateString();
    let last = null;
    try { last = localStorage.getItem('quiz-confetti-date'); } catch { /* SSR */ }
    if (last === today) return;
    try { localStorage.setItem('quiz-confetti-date', today); } catch { /* SSR */ }
    const t1 = setTimeout(() => setConfetti(true), 60);
    const t2 = setTimeout(() => setConfetti(false), 2700);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [analytics.todayCount, dailyGoal]);

  // 커버리지: 전체 대비 미응답/정답/복습필요/마스터 + 시험별 진척
  const coverage = useMemo(() => {
    let unseen = 0, learned = 0, review = 0, mastered = 0;
    const byExam = {};
    for (const q of classifiedList) {
      const ex = q.exam || '기타';
      const e = byExam[ex] || (byExam[ex] = { total: 0, answered: 0, scored: 0, correct: 0, mastered: 0 });
      e.total++;
      const p = progress[qid(q)];
      if (!p) { unseen++; continue; }
      e.answered++;
      const grad = p.srs && p.srs.graduated;
      if (grad) { mastered++; e.mastered++; }
      else if (p.correct === false) review++;
      else learned++;                     // 정답 또는 채점불가 응답(=학습함)
      if (p.correct === true || p.correct === false) { e.scored++; if (p.correct === true) e.correct++; }
    }
    const total = classifiedList.length || 1;
    const exams = Object.entries(byExam)
      .map(([name, v]) => ({
        name, ...v,
        coverPct: Math.round((v.answered / (v.total || 1)) * 100),
        acc: v.scored ? Math.round((v.correct / v.scored) * 100) : null,
      }))
      .sort((a, b) => b.total - a.total);
    return {
      total: classifiedList.length, unseen, learned, review, mastered,
      pct: (n) => Math.round((n / total) * 100),
      exams,
    };
  }, [classifiedList, progress]);

  // 한 과목을 집중 연습: 오답·미응답 우선(없으면 전체) 가이드 학습
  const startConcept = (subjectName, title) => {
    const ids = [];
    for (const q of classifiedList) {
      if ((q.taxSubjectName || '기타') !== subjectName) continue;
      const p = progress[qid(q)];
      if (!p || p.correct === false) ids.push(qid(q));   // 미응답 또는 오답 우선
    }
    const finalIds = ids.length ? ids
      : classifiedList.filter(q => (q.taxSubjectName || '기타') === subjectName).map(qid);
    startReview(finalIds, title, 'home');
  };

  // 오늘의 추천: 오답 → 미응답 순, 약점 과목 가중, 일일 목표 수만큼
  const startRecommended = () => {
    const weakNames = new Set(analytics.weak.map(w => w.name));
    const w = (q) => (weakNames.has(q.taxSubjectName || '기타') ? 0 : 1);
    const wrong = [], unseen = [];
    for (const q of classifiedList) {
      const p = progress[qid(q)];
      if (!p) unseen.push(q);
      else if (p.correct === false) wrong.push(q);
    }
    wrong.sort((a, b) => w(a) - w(b));
    unseen.sort((a, b) => w(a) - w(b));
    const ids = [...wrong, ...unseen].slice(0, dailyGoal).map(qid);
    if (ids.length) startReview(ids, '오늘의 추천 학습', 'home');
  };

  // 무작위 N문제 (셔플은 모듈 레벨 sampleN — 렌더 순수성 규칙 회피)
  const startRandom = (n = 20) => {
    const ids = sampleN(classifiedList, n).map(qid);
    if (ids.length) startReview(ids, `랜덤 ${ids.length}문제`, 'home');
  };

  // 카드 한 장이 대표하는 문항 집합 (filterFn 없으면 타입별 추론)
  const cardQuestions = (group) => {
    if (group.filterFn) return processedData.filter(group.filterFn);
    if (group.type === 'exam') return classifiedList.filter(q => q.exam === group.title);
    if (group.type === 'year_group') return classifiedList.filter(q => String(q.year) === String(group.rawValue));
    if (group.type === 'tax_subject') return scopedClassified.filter(q => q.taxSubjectName === group.title);
    if (group.type === 'tax_sub_subject') return scopedClassified.filter(q => q.taxSubjectName === taxSubject && q.taxSubSubjectName === group.title);
    return [];
  };

  const enterTaxScope = (scope) => {
    setTaxScope(scope);
    setTaxSubject(null);
    setTaxSubSubject(null);
    setTaxChapter(null);
    setTaxSection(null);
    setCurrentView('tax_subjects');
    window.scrollTo(0, 0);
  };

  // 오답 복습 시작: 진입 시점의 오답 id를 스냅샷 → 세션 중 목록 안정, 가이드 학습 재사용
  const startReview = (ids, title, backView = 'review') => {
    const set = new Set(ids);
    setSelectedGroup({
      type: 'play_all_review',
      review: true,
      backView,                       // 학습 종료 후 복귀할 화면(review | today)
      title,
      subtitle: backView === 'today' ? '오늘 복습' : backView === 'search' ? '검색 학습' : backView === 'status' ? '북마크 복습' : '오답 복습',
      filterFn: (q) => set.has(qid(q)),
    });
    setStudyIdx(0);
    setStudyNonce(n => n + 1);
    setCurrentView('study');
    window.scrollTo(0, 0);
  };

  const handleGroupClick = (group) => {
    if (group.type === 'exam') {
      enterTaxScope({ kind: 'exam', value: group.title, label: group.title });
    } else if (group.type === 'year_group') {
      enterTaxScope({ kind: 'year', value: group.rawValue, label: `${group.rawValue}년` });
    } else if (group.type === 'tax_subject') {
      setTaxSubject(group.title);
      setCurrentView('tax_sub_subjects');
      window.scrollTo(0, 0);
    } else if (group.type === 'tax_sub_subject') {
      setTaxSubSubject(group.title);
      setCurrentView('tax_chapters');
      window.scrollTo(0, 0);
    } else if (group.type === 'tax_chapter') {
      setTaxChapter(group.title);
      setCurrentView('tax_sections');
      window.scrollTo(0, 0);
    } else if (group.type === 'tax_section') {
      setTaxSection(group.title);
      setCurrentView('tax_items');
      window.scrollTo(0, 0);
    } else {
      // 개념 단위 안정 키 → 이어풀기 위치 복원
      const posKey = [taxScope && taxScope.kind, taxScope && taxScope.value,
        taxSubject, taxSubSubject, taxChapter, taxSection, group.type, group.title]
        .map(x => x || '').join('|');
      const saved = loadPos()[posKey];
      const resumeIdx = Number.isInteger(saved) && saved > 0 ? saved : 0;
      setSelectedGroup({ ...group, posKey, resumeIdx });
      setStudyIdx(resumeIdx);
      setStudyNonce(n => n + 1);
      setCurrentView('study');
      window.scrollTo(0, 0);
    }
  };

  const handleBack = () => {
    clearAutoTimer();
    if (currentView === 'question_list' || currentView === 'study') {
      // 오답 복습에서 진입한 경우 복습 화면으로 복귀
      if (selectedGroup && selectedGroup.review) {
        setCurrentView(selectedGroup.backView || 'review');
        setSelectedGroup(null);
        return;
      }
      // play_all_tax: 진입했던 가장 깊은 tax 레벨로 복귀
      if (taxSection) setCurrentView('tax_items');
      else if (taxChapter) setCurrentView('tax_sections');
      else if (taxSubSubject) setCurrentView('tax_chapters');
      else if (taxSubject) setCurrentView('tax_sub_subjects');
      else if (taxScope) setCurrentView('tax_subjects');
      else setCurrentView('dashboard');
      setSelectedGroup(null);
    } else if (currentView === 'tax_items') {
      setCurrentView('tax_sections');
      setTaxSection(null);
    } else if (currentView === 'tax_sections') {
      setCurrentView('tax_chapters');
      setTaxChapter(null);
    } else if (currentView === 'tax_chapters') {
      setCurrentView('tax_sub_subjects');
      setTaxSubSubject(null);
    } else if (currentView === 'tax_sub_subjects') {
      setCurrentView(taxScope ? 'tax_subjects' : 'dashboard');
      setTaxSubject(null);
    } else if (currentView === 'tax_subjects') {
      setCurrentView('dashboard');
      setTaxScope(null);
    } else {
      setCurrentView('dashboard');
    }
  };

  // 탭 전환: 모든 드릴다운 상태를 초기화하고 대시보드로
  const switchTab = (mode) => {
    setViewMode(mode);
    setCurrentView('dashboard');
    setTaxScope(null);
    setTaxSubject(null);
    setTaxSubSubject(null);
    setTaxChapter(null);
    setTaxSection(null);
    setSelectedGroup(null);
    window.scrollTo(0, 0);
  };

  // 하단 탭바: 루트 화면에서만 노출(드릴/풀이는 전체화면)
  const navTab =
    (currentView === 'home' || currentView === 'profile' || currentView === 'settings') ? 'home'
    : (currentView === 'reviewHome' || currentView === 'review' || currentView === 'today') ? 'review'
    : currentView === 'status' ? 'status'
    : 'browse'; // dashboard + tax_* + search(둘러보기 흡수)
  const goTab = (t) => {
    clearAutoTimer();
    if (t === 'home') setCurrentView('home');
    else if (t === 'browse') setCurrentView('dashboard');
    else if (t === 'review') { setReviewSubject(null); setCurrentView('reviewHome'); }
    else if (t === 'status') setCurrentView('status');
    window.scrollTo(0, 0);
  };
  const NAV_ITEMS = [
    ['home', House, '홈'],
    ['browse', Compass, '둘러보기'],
    ['review', RotateCcw, '복습'],
    ['status', ChartColumn, '현황'],
  ];
  const bottomNav = (
    <nav className="bottom-nav">
      {NAV_ITEMS.map(([t, Ico, label]) => {
        const active = navTab === t;
        return (
          <button key={t} className={active ? 'active' : ''} onClick={() => goTab(t)}>
            <span className="nav-ico" style={{ position: 'relative' }}>
              <Ico size={22} strokeWidth={active ? 2.4 : 1.9} />
              {t === 'review' && srs.due.length > 0 && (
                <span className="nav-badge">{srs.due.length > 99 ? '99+' : srs.due.length}</span>
              )}
            </span>
            {label}
          </button>
        );
      })}
    </nav>
  );
  // 첫 사용자는 모달 대신 빈 상태 히어로로 가치를 먼저 보여준다(아래 home 분기).
  const startFirstTaste = () => {
    try { localStorage.setItem('quiz-onboarded', '1'); } catch { /* SSR */ }
    const ids = sampleN(classifiedList, 10).map(qid);
    if (ids.length) startReview(ids, '맛보기 10문제', 'home');
  };
  // 전역 오버레이(컨페티) — 루트/드릴 양쪽에 삽입
  const overlays = <>{confetti && <Confetti />}</>;
  const shell = (content) => (
    <div className="app-shell with-nav">
      {content}
      {bottomNav}
      {overlays}
    </div>
  );

  // 드릴 화면 공통 상단바: 좌측 뒤로가기 + 우측 액션(옵션)
  const drillHeader = (rightAction = null) => (
    <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', display: 'flex', justifyContent: 'space-between' }}>
      <button className="back-btn" onClick={handleBack}>
        <ArrowLeft size={24} style={{ marginRight: '8px' }} />
        <span style={{ fontSize: '1rem', fontWeight: '600' }}>뒤로가기</span>
      </button>
      {rightAction}
    </header>
  );

  // 가이드 학습 모드: 한 개념의 문제를 난이도↑ 순으로 한 문제씩, 해설로 누적 학습
  if (currentView === 'study' && selectedGroup) {
    const shuffleMode = !selectedGroup.review && studyOrder === 'random';
    // 세션 내 안정 셔플: qid+studyNonce 해시 → 같은 세션에선 순서 고정
    const seededRank = (q) => {
      let h = studyNonce * 2654435761 >>> 0;
      const id = qid(q);
      for (let i = 0; i < id.length; i++) h = (h * 31 + id.charCodeAt(i)) >>> 0;
      return h;
    };
    const ordered = processedData
      .filter(selectedGroup.filterFn)
      .sort((a, b) => {
        if (shuffleMode) return seededRank(a) - seededRank(b);
        if (selectedGroup.review) {
          // 복습: 여러 번 틀린 것 먼저, 그다음 어려운 것 먼저
          const ra = (progress[qid(a)] && progress[qid(a)].reviewed) || 0;
          const rb = (progress[qid(b)] && progress[qid(b)].reviewed) || 0;
          if (ra !== rb) return rb - ra;
          const dda = a.difficulty ?? 0, ddb = b.difficulty ?? 0;
          if (dda !== ddb) return ddb - dda;
        } else {
          const da = a.difficulty ?? 99, db = b.difficulty ?? 99;
          if (da !== db) return da - db;               // 학습: 쉬운 문제부터
        }
        const ya = parseInt(a.year, 10), yb = parseInt(b.year, 10);
        if (ya !== yb) return yb - ya;                  // 최신 연도
        return parseInt(a.number, 10) - parseInt(b.number, 10);
      });
    const total = ordered.length;
    const idx = Math.min(studyIdx, Math.max(0, total - 1));
    const q = ordered[idx];
    const s = progressStats(ordered, progress);
    const pathParts = q ? [q.taxSubjectName, q.taxSubSubjectName, q.taxChapterName, q.taxSectionName, q.taxItemName].filter(Boolean) : [];
    const done = total > 0 && s.answered >= total;
    const goPrev = () => { clearAutoTimer(); setAutoPending(false); setStudyIdx(Math.max(0, idx - 1)); window.scrollTo(0, 0); };
    const goNext = () => { clearAutoTimer(); setAutoPending(false); setStudyIdx(Math.min(total - 1, idx + 1)); window.scrollTo(0, 0); };
    const baseAnswer = selectedGroup.review ? updateAnswer : recordAnswer;
    const handleAnswer = (qq, sel, correct) => {
      baseAnswer(qq, sel, correct);
      if (autoNext && idx < total - 1) {
        clearAutoTimer();
        setAutoPending(true);
        autoTimerRef.current = setTimeout(() => {
          autoTimerRef.current = null;
          setAutoPending(false);
          setStudyIdx(i => Math.min(total - 1, i + 1));
          window.scrollTo(0, 0);
        }, autoSec * 1000);
      }
    };
    return (
      <div className="app-container">
        {drillHeader(
          <button className="drill-action" onClick={() => setCurrentView('question_list')}>
            ▦ 목록
          </button>
        )}

        <div className="drill-head sticky">
          <div style={{ fontSize: '0.8rem', color: '#6b7280' }}>{selectedGroup.title}</div>
          {pathParts.length > 0 && (
            <div style={{ fontSize: '0.85rem', color: '#374151', margin: '6px 0', fontWeight: 600 }}>
              {pathParts.join(' ▸ ')}
            </div>
          )}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '8px' }}>
            <div style={{ flex: 1, height: '8px', background: '#e5e7eb', borderRadius: '999px', overflow: 'hidden' }}>
              <div style={{ width: `${total ? Math.round((s.answered / total) * 100) : 0}%`, height: '100%', background: 'var(--primary)', transition: 'width .3s' }} />
            </div>
            <span style={{ fontSize: '0.8rem', color: '#6b7280', whiteSpace: 'nowrap' }}>
              {idx + 1} / {total} · 정답 <b style={{ color: '#16a34a' }}>{s.correct}</b>
            </span>
          </div>
          <div style={{ display: 'flex', gap: '8px', marginTop: '10px', flexWrap: 'wrap' }}>
            {!selectedGroup.review && (
              <button
                onClick={() => { setStudyOrder(studyOrder === 'random' ? 'difficulty' : 'random'); setStudyIdx(0); setStudyNonce(n => n + 1); window.scrollTo(0, 0); }}
                style={{ border: '1px solid #d1d5db', background: '#fff', color: '#374151',
                  borderRadius: '999px', padding: '6px 12px', fontSize: '0.78rem', fontWeight: 700, cursor: 'pointer' }}
              >
                {studyOrder === 'random' ? '🔀 무작위 순서' : '↕ 난이도순'}
              </button>
            )}
            <button
              onClick={() => { const v = !autoNext; setAutoNext(v); if (!v) { clearAutoTimer(); setAutoPending(false); } }}
              style={{ border: `1px solid ${autoNext ? 'var(--primary)' : '#d1d5db'}`,
                background: autoNext ? 'var(--primary)' : '#fff', color: autoNext ? '#fff' : '#374151',
                borderRadius: '999px', padding: '6px 12px', fontSize: '0.78rem', fontWeight: 700, cursor: 'pointer' }}
            >
              ⏩ 자동 다음 {autoNext ? 'ON' : 'OFF'}
            </button>
            {autoNext && [3, 5, 8].map(sec => (
              <button key={sec} onClick={() => setAutoSec(sec)}
                style={{ border: `1px solid ${autoSec === sec ? 'var(--primary)' : '#d1d5db'}`,
                  background: autoSec === sec ? '#eff6ff' : '#fff', color: autoSec === sec ? 'var(--primary)' : '#6b7280',
                  borderRadius: '999px', padding: '6px 10px', fontSize: '0.74rem', fontWeight: 700, cursor: 'pointer' }}>
                {sec}초
              </button>
            ))}
          </div>
        </div>

        <main
          style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}
          onTouchStart={(e) => { const t = e.changedTouches[0]; swipe.x = t.clientX; swipe.y = t.clientY; }}
          onTouchEnd={(e) => {
            const t = e.changedTouches[0];
            const dx = t.clientX - swipe.x, dy = t.clientY - swipe.y;
            if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return; // 가로 스와이프만
            if (dx < 0 && idx < total - 1) goNext();
            else if (dx > 0 && idx > 0) goPrev();
          }}
        >
          {q ? (
            <>
              {selectedGroup.resumeIdx > 0 && studyIdx === selectedGroup.resumeIdx && (
                <div style={{ background: '#eff6ff', border: '1px solid #bfdbfe', color: '#1d4ed8',
                  borderRadius: '10px', padding: '10px 14px', marginBottom: '12px', fontSize: '0.85rem', fontWeight: 600 }}>
                  ⏯️ 이어서 풀기 — {studyIdx + 1}번째 문제부터
                </div>
              )}
              <QuestionItem
                key={`${qid(q)}-${studyNonce}`}
                q={q}
                prior={selectedGroup.review ? undefined : progress[qid(q)]}
                onAnswer={handleAnswer}
                bmReason={bmReasonOf(bm[qid(q)])}
                onToggleBookmark={cycleBookmark}
                keyboard
              />
              {autoPending && (
                <div onClick={() => { clearAutoTimer(); setAutoPending(false); }}
                  style={{ marginTop: '10px', padding: '10px 14px', borderRadius: '10px', cursor: 'pointer',
                    background: '#eff6ff', border: '1px solid #bfdbfe', color: '#1d4ed8', fontSize: '0.85rem', fontWeight: 600, textAlign: 'center' }}>
                  ⏩ 잠시 후 다음 문제로… (탭하여 멈춤)
                </div>
              )}
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', marginTop: '8px' }}>
                <button
                  onClick={goPrev}
                  disabled={idx === 0}
                  style={{ flex: 1, padding: '14px', minHeight: '48px', borderRadius: '10px', border: '1px solid #d1d5db', background: '#fff', cursor: idx === 0 ? 'default' : 'pointer', color: idx === 0 ? '#d1d5db' : '#374151', fontWeight: 600 }}
                >← 이전</button>
                <button
                  onClick={goNext}
                  disabled={idx >= total - 1}
                  style={{ flex: 2, padding: '14px', minHeight: '48px', borderRadius: '10px', border: 'none', background: idx >= total - 1 ? '#e5e7eb' : 'var(--primary)', color: idx >= total - 1 ? '#9ca3af' : '#fff', cursor: idx >= total - 1 ? 'default' : 'pointer', fontWeight: 700 }}
                >다음 문제 →</button>
              </div>
              <div className="kbd-hint" style={{ textAlign: 'center', fontSize: '0.75rem', color: '#9ca3af', marginTop: '8px' }}>
                키보드 <b>1~5</b> 보기 · <b>←</b> 이전 · <b>→</b>·<b>Enter</b> 다음
              </div>
              <div className="swipe-hint" style={{ textAlign: 'center', fontSize: '0.75rem', color: '#9ca3af', marginTop: '8px' }}>
                ← 좌우로 밀어 이전·다음 →
              </div>
              {done && selectedGroup.review && (() => {
                const stillWrong = ordered.filter(x => { const p = progress[qid(x)]; return p && p.correct === false; });
                const cleared = total - stillWrong.length;
                return (
                  <div style={{ marginTop: '20px', padding: '20px', background: stillWrong.length ? '#fef2f2' : '#ecfdf5', border: `1px solid ${stillWrong.length ? '#fecaca' : '#a7f3d0'}`, borderRadius: '12px', textAlign: 'center' }}>
                    <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: '6px' }}>
                      {stillWrong.length ? '복습 1회전 완료' : '오답 전부 해결 🎉'}
                    </div>
                    <div style={{ color: '#374151', marginBottom: '14px' }}>
                      복습 {total}개 · 해결 <b style={{ color: '#16a34a' }}>{cleared}</b> · 여전히 오답 <b style={{ color: '#dc2626' }}>{stillWrong.length}</b>
                    </div>
                    {stillWrong.length > 0 ? (
                      <button onClick={() => startReview(stillWrong.map(qid), selectedGroup.title, selectedGroup.backView)}
                        style={{ padding: '12px 20px', borderRadius: '10px', border: 'none', background: '#ef4444', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>
                        여전히 틀린 {stillWrong.length}개 다시 풀기
                      </button>
                    ) : (
                      <button onClick={() => { const bv = selectedGroup.backView || 'review'; setSelectedGroup(null); setReviewSubject(null); setCurrentView(bv); window.scrollTo(0, 0); }}
                        style={{ padding: '12px 20px', borderRadius: '10px', border: 'none', background: '#16a34a', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>
                        {/* today면 오늘 복습으로 */}목록으로
                      </button>
                    )}
                  </div>
                );
              })()}
              {done && !selectedGroup.review && (
                <div style={{ marginTop: '20px', padding: '20px', background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '12px', textAlign: 'center' }}>
                  <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: '6px' }}>이 개념 학습 완료 🎉</div>
                  <div style={{ color: '#374151', marginBottom: '14px' }}>
                    {total}문제 중 정답 <b style={{ color: '#16a34a' }}>{s.correct}</b> · 오답 <b style={{ color: '#dc2626' }}>{s.scored - s.correct}</b>
                    {s.answered > s.scored && <> · 채점제외 <b style={{ color: '#6b7280' }}>{s.answered - s.scored}</b></>}
                    {s.accuracy !== null && <> · 정답률 <b>{s.accuracy}%</b></>}
                  </div>
                  {(() => {
                    const wrongNow = ordered.filter(x => { const p = progress[qid(x)]; return p && p.correct === false; });
                    return (
                      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', flexWrap: 'wrap' }}>
                        {wrongNow.length > 0 && (
                          <button onClick={() => startReview(wrongNow.map(qid), `${selectedGroup.title} 오답`, 'dashboard')}
                            style={{ padding: '12px 20px', borderRadius: '10px', border: 'none', background: '#ef4444', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>
                            틀린 {wrongNow.length}개만 다시
                          </button>
                        )}
                        <button onClick={() => {
                            clearMany(ordered.map(qid));   // 이 개념 진행 초기화 → 재측정
                            setStudyIdx(0);
                            setStudyNonce(n => n + 1);     // 카드 강제 리마운트(이전 응답 표시 제거)
                            window.scrollTo(0, 0);
                          }}
                          style={{ padding: '12px 20px', borderRadius: '10px', border: '1px solid #bfdbfe', background: '#fff', color: '#1d4ed8', fontWeight: 700, cursor: 'pointer' }}>
                          처음부터 다시
                        </button>
                      </div>
                    );
                  })()}
                </div>
              )}
            </>
          ) : (
            <div className="empty-state"><span className="emoji">📭</span><div className="title">문제가 없습니다</div></div>
          )}
        </main>
        {overlays}
      </div>
    );
  }

  if (currentView === 'question_list' && selectedGroup) {
    // 필터링된 문제를 연도 내림차순, 문제 번호 오름차순으로 정렬
    const filteredQuestions = processedData
      .filter(selectedGroup.filterFn)
      .sort((a, b) => {
        const yearA = parseInt(a.year, 10);
        const yearB = parseInt(b.year, 10);
        if (yearA !== yearB) return yearB - yearA; // 연도 내림차순
        return parseInt(a.number, 10) - parseInt(b.number, 10); // 번호 오름차순
      });
    
    return (
      <div className="app-container">
        {drillHeader(
          <button className="drill-action" onClick={() => { scrollMem.qlist = window.scrollY; setStudyIdx(0); setCurrentView('study'); window.scrollTo(0, 0); }}>
            📚 학습
          </button>
        )}

        <div className="drill-head">
          <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '4px' }}>{selectedGroup.subtitle}</div>
          <h1 className="screen-title">{selectedGroup.title} ({filteredQuestions.length}문제)</h1>
          {(() => {
            const s = progressStats(filteredQuestions, progress);
            const pct = s.total ? Math.round((s.answered / s.total) * 100) : 0;
            return (
              <div style={{ marginTop: '12px' }}>
                <div style={{ height: '8px', background: '#e5e7eb', borderRadius: '999px', overflow: 'hidden' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: 'var(--primary)', transition: 'width .3s' }} />
                </div>
                <div style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: '6px' }}>
                  푼 문제 <b>{s.answered}/{s.total}</b> · 정답 <b style={{ color: '#16a34a' }}>{s.correct}</b>
                </div>
              </div>
            );
          })()}
        </div>

        <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
          {filteredQuestions.map((q) => (
            <QuestionItem
              key={qid(q)}
              q={q}
              prior={progress[qid(q)]}
              onAnswer={recordAnswer}
              bmReason={bmReasonOf(bm[qid(q)])}
              onToggleBookmark={cycleBookmark}
            />
          ))}
        </main>
      </div>
    );
  }


  const renderStudyGrid = (title, subtitle, groups) => (
    <div className="app-container">
      {drillHeader()}

      <div className="drill-head">
        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '4px' }}>{subtitle}</div>
        <h1 className="screen-title">{title}</h1>
      </div>
      
      <main className="main-content" style={{ marginTop: '20px' }}>
        <div className="study-grid">
          {groups.map((group, idx) => {
            const isAll = group.type && group.type.startsWith('play_all');
            const s = progressStats(cardQuestions(group), progress);
            const pct = s.total ? Math.round((s.answered / s.total) * 100) : 0;
            const dm = s.level ? (DIFFICULTY_META[s.level] || null) : null;
            return (
              <div key={idx} className="study-card" onClick={() => handleGroupClick(group)} style={isAll ? { background: '#eff6ff', borderColor: '#bfdbfe' } : {}}>
                <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                  <div className="card-badge" style={isAll ? { background: 'var(--primary)', color: '#fff', border: 'none' } : {}}>{group.tag}</div>
                  {dm && (
                    <span style={{ fontSize: '0.72rem', fontWeight: 700, padding: '2px 8px', borderRadius: '999px', background: dm.bg, color: dm.fg }}>
                      난이도 {s.avgDiff.toFixed(1)}
                    </span>
                  )}
                </div>
                <div className="card-subtitle">{group.subtitle}</div>
                <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{group.title}</h3>
                <div className="card-total">총 {group.total} 문제 {s.answered > 0 && <span style={{ color: 'var(--primary)', fontWeight: 700 }}>· {pct}%</span>}</div>
                <div className="card-progress-container">
                  <div className="card-progress-fill" style={{ width: `${pct}%` }}></div>
                </div>
                <div className="play-btn" style={isAll ? { background: 'var(--primary)', color: '#fff' } : {}}>선택</div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );

  // ===== 단일 v4 분류축 뷰 (시험별/과목별/단원별/연도별 공용) =====
  const scopePrefix = taxScope ? `${taxScope.label} · ` : '';
  if (currentView === 'tax_subjects') return renderStudyGrid(taxScope ? taxScope.label : '과목 선택', taxScope ? `${taxScope.label} 과목별` : '단원별 학습', taxSubjectGroups);
  if (currentView === 'tax_sub_subjects' && taxSubject) return renderStudyGrid(`${scopePrefix}${taxSubject}`, '세부과목 / 장 선택', taxSubSubjectGroups);
  if (currentView === 'tax_chapters' && taxSubSubject) return renderStudyGrid(`${scopePrefix}${taxSubSubject}`, '장(Chapter) 선택', taxChapterGroups);
  if (currentView === 'tax_sections' && taxChapter) return renderStudyGrid(`${scopePrefix}${taxChapter}`, '절(Section) 선택', taxSectionGroups);
  if (currentView === 'tax_items' && taxSection) return renderStudyGrid(`${scopePrefix}${taxSection}`, '관(Item) 선택', taxItemGroups);

  // Dashboard View

  if (loading) {
    return (
      <div className="boot">
        <div className="boot-mark">감정평가사 기출</div>
        <div className="boot-title">1차 기출 12,000+ 문제</div>
        <div className="boot-bar"><div className="boot-fill" style={{ width: `${Math.max(4, loadPct)}%` }} /></div>
        <div className="boot-pct">{loadPct < 100 ? `${loadPct}%` : '거의 다 됐어요…'}</div>
        <div className="boot-note">최초 1회만 받으면 다음부터 오프라인에서도 바로 열려요</div>
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="boot">
        <div className="boot-mark">감정평가사 기출</div>
        <div className="boot-title" style={{ marginBottom: 8 }}>잠깐 연결이 끊겼어요</div>
        <div className="boot-note" style={{ marginBottom: 22 }}>
          네트워크를 확인하고 다시 시도해 주세요. 데이터는 안전합니다.
        </div>
        <button onClick={() => window.location.reload()} className="boot-retry">
          다시 시도
        </button>
      </div>
    );
  }

  if (totalQuestions === 0) {
    return (
      <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#f8fafc', color: '#6b7280', padding: '24px', textAlign: 'center' }}>
        <div style={{ fontWeight: 700, fontSize: '1.2rem', color: '#374151', marginBottom: '8px' }}>표시할 분류된 문제가 없습니다</div>
        <div>데이터가 비어 있거나 분류가 아직 반영되지 않았습니다.</div>
      </div>
    );
  }

  if (currentView === 'search') {
    const activeCount = filters.exams.length + filters.subjects.length + filters.years.length + filters.diffs.length + (filters.kw.trim() ? 1 : 0) + (filters.cleanOnly ? 1 : 0);
    const shown = filteredResults.slice(0, 200);
    const chip = (on) => ({
      padding: '6px 12px', borderRadius: '999px', fontSize: '0.85rem', cursor: 'pointer',
      border: on ? '1px solid var(--primary)' : '1px solid #d1d5db',
      background: on ? 'var(--primary)' : '#fff', color: on ? '#fff' : '#374151',
    });
    const groupChips = (label, items, sel, k, fmt) => (
      <div style={{ marginBottom: '14px' }}>
        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#6b7280', marginBottom: '6px' }}>{label}</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          {items.map(it => (
            <span key={String(it)} style={chip(sel.includes(it))} onClick={() => toggleFilter(k, it)}>
              {fmt ? fmt(it) : it}
            </span>
          ))}
        </div>
      </div>
    );
    return shell(
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => setCurrentView('dashboard')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>둘러보기</span>
          </button>
        </header>
        <div className="screen-head">
          <h1 className="screen-title">🔍 검색</h1>
        </div>
        <div style={{ padding: '20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <input
            value={filters.kw}
            onChange={(e) => setFilters(f => ({ ...f, kw: e.target.value }))}
            placeholder="문제·보기·해설 키워드 검색"
            style={{ width: '100%', padding: '12px 14px', fontSize: '1rem', border: '1px solid #d1d5db', borderRadius: '10px', marginBottom: '16px', boxSizing: 'border-box' }}
          />
          {groupChips('시험', filterOptions.exams, filters.exams, 'exams')}
          {groupChips('과목', filterOptions.subjects, filters.subjects, 'subjects')}
          {groupChips('연도', filterOptions.years, filters.years, 'years', (y) => `${y}년`)}
          {groupChips('난이도', filterOptions.diffs, filters.diffs, 'diffs', (d) => `난이도 ${d}`)}
          <div style={{ marginBottom: '10px' }}>
            <span
              style={chip(filters.cleanOnly)}
              onClick={() => setFilters(f => ({ ...f, cleanOnly: !f.cleanOnly }))}
            >
              ✓ 정답·보기 있는 문항만
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '6px' }}>
            <span style={{ fontWeight: 700 }}>{activeCount ? `${filteredResults.length}문제` : '필터를 선택하세요'}</span>
            {activeCount > 0 && (
              <button onClick={clearFilters} style={{ border: 'none', background: '#f3f4f6', padding: '6px 12px', borderRadius: '8px', cursor: 'pointer', fontSize: '0.85rem' }}>필터 초기화</button>
            )}
          </div>
          {filteredResults.length > 0 && (
            <button
              onClick={() => startReview(filteredResults.map(qid), `검색 결과 학습 (${filteredResults.length})`, 'search')}
              style={{ width: '100%', marginTop: '14px', padding: '14px', border: 'none', borderRadius: '12px',
                background: 'var(--primary)', color: '#fff', fontWeight: 800, fontSize: '0.95rem', cursor: 'pointer' }}
            >
              ▶ 이 결과로 가이드 학습 시작 ({filteredResults.length}문제)
            </button>
          )}
        </div>
        <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
          {shown.map(q => (
            <QuestionItem key={qid(q)} q={q} prior={progress[qid(q)]} onAnswer={recordAnswer} bmReason={bmReasonOf(bm[qid(q)])} onToggleBookmark={cycleBookmark} />
          ))}
          {filteredResults.length > shown.length && (
            <div style={{ textAlign: 'center', color: '#6b7280', padding: '16px' }}>
              상위 {shown.length}개만 표시 중 (총 {filteredResults.length}개) — 필터를 좁혀주세요
            </div>
          )}
        </main>
      </div>
    );
  }

  if (currentView === 'profile') {
    const prof = loadProfile();
    let firstTs = null;
    for (const k in progress) { const t = progress[k] && progress[k].ts; if (t && (firstTs == null || t < firstTs)) firstTs = t; }
    const fmt = (iso) => { const d = new Date(iso); return `${d.getFullYear()}.${d.getMonth() + 1}.${d.getDate()}`; };
    const daysAgo = prof.lastBackup ? Math.floor((nowTs - new Date(prof.lastBackup).getTime()) / 86400000) : null;
    const stale = overall.answered > 0 && (daysAgo == null || daysAgo >= 7);
    return shell(
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => setCurrentView('home')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>홈</span>
          </button>
        </header>
        <div className="screen-head"><h1 className="screen-title">👤 내 프로필</h1></div>
        <main className="main-content" style={{ marginTop: '16px' }}>
          <section style={{ background: '#fff', borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
            <label style={{ fontSize: '0.8rem', fontWeight: 700, color: '#6b7280' }}>닉네임</label>
            <input
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              placeholder="학습자 이름"
              style={{ width: '100%', padding: '11px 14px', marginTop: '6px', fontSize: '1rem',
                border: '1px solid #d1d5db', borderRadius: '10px', boxSizing: 'border-box' }}
            />
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginTop: '16px' }}>
              {[
                ['학습 시작', firstTs ? fmt(firstTs) : '–'],
                ['총 학습', `${overall.answered}문제`],
                ['정답률', overall.accuracy == null ? '–' : `${overall.accuracy}%`],
                ['연속 학습', `${analytics.streak}일`],
              ].map(([k, v]) => (
                <div key={k} style={{ background: '#f8fafc', borderRadius: '10px', padding: '12px', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.05rem', fontWeight: 800 }}>{v}</div>
                  <div style={{ fontSize: '0.72rem', color: '#6b7280', marginTop: '2px' }}>{k}</div>
                </div>
              ))}
            </div>
          </section>

          <section style={{ background: stale ? '#fffbeb' : '#fff', border: `1px solid ${stale ? '#fde68a' : '#e5e7eb'}`,
            borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
            <div style={{ fontWeight: 800, marginBottom: '4px' }}>데이터 백업</div>
            <div style={{ fontSize: '0.82rem', color: '#6b7280', marginBottom: '12px' }}>
              학습 기록은 이 기기에만 저장돼요. 백업 파일을 보관하면 기기를 바꿔도 그대로 복원할 수 있어요.
              {prof.lastBackup
                ? <> 마지막 백업: <b>{daysAgo === 0 ? '오늘' : `${daysAgo}일 전`}</b>.</>
                : <> <b>아직 백업한 적 없어요.</b></>}
              {stale && <span style={{ color: '#b45309' }}> 백업을 권장합니다.</span>}
            </div>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              <button onClick={exportUserData}
                style={{ flex: 1, minWidth: 110, padding: '12px', borderRadius: '10px', border: 'none',
                  background: 'var(--primary)', color: '#fff', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                ⬇ 백업 내보내기
              </button>
              <button onClick={() => fileRef.current && fileRef.current.click()}
                style={{ flex: 1, minWidth: 110, padding: '12px', borderRadius: '10px', border: '1px solid #d1d5db',
                  background: '#fff', color: '#374151', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                ⬆ 백업 가져오기
              </button>
            </div>
            <button onClick={() => { if (window.confirm('모든 학습 기록을 삭제할까요? 되돌릴 수 없습니다.')) { resetUserData(); window.location.reload(); } }}
              style={{ width: '100%', marginTop: '8px', padding: '11px', borderRadius: '10px', border: '1px solid #fecaca',
                background: '#fef2f2', color: '#b91c1c', fontWeight: 700, fontSize: '0.85rem', cursor: 'pointer' }}>
              전체 초기화
            </button>
            <input ref={fileRef} type="file" accept="application/json,.json" onChange={onImportFile} style={{ display: 'none' }} />
          </section>

          <section style={{ background: '#fff', borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '12px' }}>
            <div style={{ fontWeight: 800, marginBottom: '4px' }}>☁ 클라우드 동기화</div>
            {!cloudEnabled ? (
              <div style={{ fontSize: '0.82rem', color: '#9ca3af' }}>설정되지 않음 (파일 백업만 사용)</div>
            ) : authUser ? (
              <>
                <div style={{ fontSize: '0.82rem', color: '#6b7280', marginBottom: '12px' }}>
                  로그인: <b>{authUser.email}</b>
                  {loadProfile().lastCloud && <> · 마지막 동기화 {new Date(loadProfile().lastCloud).toLocaleString('ko-KR')}</>}
                  <br />다른 기기에서도 같은 계정으로 로그인하면 이어집니다. (앱을 닫을 때 자동 백업)
                </div>
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  <button onClick={() => cloudPush(false)}
                    style={{ flex: 1, minWidth: 120, padding: '12px', borderRadius: '10px', border: 'none', background: 'var(--primary)', color: '#fff', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                    ☁⬆ 클라우드에 백업
                  </button>
                  <button onClick={cloudPull}
                    style={{ flex: 1, minWidth: 120, padding: '12px', borderRadius: '10px', border: '1px solid #d1d5db', background: '#fff', color: '#374151', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                    ☁⬇ 클라우드에서 복원
                  </button>
                </div>
                <button onClick={async () => { await supabase.auth.signOut(); setCloudMsg('로그아웃되었어요.'); }}
                  style={{ width: '100%', marginTop: '8px', padding: '10px', borderRadius: '10px', border: '1px solid #d1d5db', background: '#fff', color: '#6b7280', fontWeight: 700, fontSize: '0.82rem', cursor: 'pointer' }}>
                  로그아웃
                </button>
              </>
            ) : (
              <>
                <div style={{ fontSize: '0.82rem', color: '#6b7280', marginBottom: '12px' }}>
                  이메일로 로그인하면 여러 기기에서 학습 기록이 자동으로 이어져요.
                </div>
                <input value={cloudEmail} onChange={(e) => setCloudEmail(e.target.value)} placeholder="이메일" type="email"
                  style={{ width: '100%', padding: '11px 14px', marginBottom: '8px', border: '1px solid #d1d5db', borderRadius: '10px', boxSizing: 'border-box' }} />
                <input value={cloudPw} onChange={(e) => setCloudPw(e.target.value)} placeholder="비밀번호(6자 이상)" type="password"
                  style={{ width: '100%', padding: '11px 14px', marginBottom: '10px', border: '1px solid #d1d5db', borderRadius: '10px', boxSizing: 'border-box' }} />
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button onClick={() => cloudAuth('signin')}
                    style={{ flex: 1, padding: '12px', borderRadius: '10px', border: 'none', background: 'var(--primary)', color: '#fff', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                    로그인
                  </button>
                  <button onClick={() => cloudAuth('signup')}
                    style={{ flex: 1, padding: '12px', borderRadius: '10px', border: '1px solid #d1d5db', background: '#fff', color: '#374151', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                    회원가입
                  </button>
                </div>
              </>
            )}
            {cloudMsg && <div style={{ fontSize: '0.8rem', color: '#1d4ed8', marginTop: '10px' }}>{cloudMsg}</div>}
          </section>

          <div style={{ fontSize: '0.75rem', color: '#9ca3af', textAlign: 'center', padding: '0 8px' }}>
            파일 백업도 함께 쓰면 가장 안전해요.
          </div>
        </main>
      </div>
    );
  }

  if (currentView === 'status') {
    const cv = coverage;
    const segs = [
      { k: 'learned', label: '정답·학습', n: cv.learned, c: 'var(--primary)' },
      { k: 'mastered', label: '마스터', n: cv.mastered, c: '#16a34a' },
      { k: 'review', label: '복습필요', n: cv.review, c: '#ef4444' },
      { k: 'unseen', label: '미응답', n: cv.unseen, c: '#e5e7eb' },
    ];
    const learnedPct = cv.total ? Math.round(((cv.learned + cv.mastered + cv.review) / cv.total) * 100) : 0;
    const backlog = Math.max(0, srs.dueTotal - srs.due.length);
    const kpi = (v, sub, color) => (
      <div style={{ flex: 1, background: '#fff', borderRadius: '12px', padding: '14px 10px', textAlign: 'center', boxShadow: 'var(--shadow-sm)' }}>
        <div style={{ fontSize: '1.25rem', fontWeight: 800, color: color || '#111827' }}>{v}</div>
        <div style={{ fontSize: '0.72rem', color: '#6b7280', marginTop: '2px' }}>{sub}</div>
      </div>
    );
    return shell(
      <div className="app-container">
        <div className="screen-head"><h1 className="screen-title">📊 학습 현황</h1></div>
        <main className="main-content" style={{ marginTop: '16px' }}>
          {/* 핵심 KPI */}
          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
            {kpi(`${learnedPct}%`, `학습 ${cv.total - cv.unseen}/${cv.total}`, '#2563eb')}
            {kpi(overall.accuracy == null ? '–' : `${overall.accuracy}%`, '정답률', '#16a34a')}
            {kpi(`${analytics.streak}일`, '연속 학습', '#ea580c')}
            {kpi(srs.due.length, '오늘 복습', '#7c3aed')}
          </div>

          {/* 오늘 학습 목표 */}
          {(() => {
            const done = analytics.todayCount;
            const pct = Math.min(100, Math.round((done / dailyGoal) * 100));
            const met = done >= dailyGoal;
            return (
              <section style={{ background: met ? '#ecfdf5' : '#fff', border: `1px solid ${met ? '#a7f3d0' : '#e5e7eb'}`,
                borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <span style={{ fontWeight: 800 }}>🎯 오늘 목표 {met && <span style={{ color: '#16a34a' }}>달성!</span>}</span>
                  <span style={{ fontSize: '0.9rem', color: '#374151' }}><b>{done}</b> / {dailyGoal}문제</span>
                </div>
                <div style={{ height: '10px', background: '#f1f5f9', borderRadius: '999px', overflow: 'hidden', marginBottom: '12px' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: met ? '#16a34a' : 'var(--primary)', transition: 'width .3s' }} />
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <span style={{ fontSize: '0.85rem', color: '#374151' }}>
                    🔥 목표 연속 <b style={{ color: '#ea580c' }}>{analytics.goalStreak}일</b>
                  </span>
                  <span style={{ display: 'flex', gap: '5px' }}>
                    {analytics.weekMet.map((w, i) => (
                      <span key={i} title={w.label} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2px' }}>
                        <span style={{ width: 14, height: 14, borderRadius: '50%',
                          background: w.met ? '#16a34a' : '#e5e7eb',
                          outline: w.isToday ? '2px solid var(--primary)' : 'none', outlineOffset: '1px' }} />
                        <span style={{ fontSize: '0.55rem', color: '#9ca3af' }}>{w.label}</span>
                      </span>
                    ))}
                  </span>
                </div>
                <div style={{ display: 'flex', gap: '6px' }}>
                  {[10, 20, 30, 50].map(g => (
                    <button key={g} onClick={() => setDailyGoal(g)}
                      style={{ flex: 1, padding: '7px', borderRadius: '8px', fontSize: '0.78rem', fontWeight: 700, cursor: 'pointer',
                        border: dailyGoal === g ? '1px solid var(--primary)' : '1px solid #d1d5db',
                        background: dailyGoal === g ? 'var(--primary)' : '#fff', color: dailyGoal === g ? '#fff' : '#6b7280' }}>
                      {g}문제
                    </button>
                  ))}
                </div>
              </section>
            );
          })()}

          {/* 커버리지 스택바 */}
          <section style={{ background: '#fff', borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
            <div style={{ fontWeight: 800, marginBottom: '12px' }}>전체 커버리지 ({cv.total}문항)</div>
            <div style={{ display: 'flex', height: '14px', borderRadius: '999px', overflow: 'hidden', marginBottom: '12px' }}>
              {segs.map(s => s.n > 0 && (
                <div key={s.k} title={`${s.label} ${s.n}`} style={{ width: `${(s.n / cv.total) * 100}%`, background: s.c }} />
              ))}
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px 14px' }}>
              {segs.map(s => (
                <div key={s.k} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.82rem', color: '#374151' }}>
                  <span style={{ width: 10, height: 10, borderRadius: 3, background: s.c, flexShrink: 0 }} />
                  {s.label} <b style={{ marginLeft: 'auto' }}>{s.n}</b>
                  <span style={{ color: '#9ca3af', minWidth: 38, textAlign: 'right' }}>{cv.pct(s.n)}%</span>
                </div>
              ))}
            </div>
          </section>

          {/* 복습 현황 */}
          <section onClick={() => srs.due.length && setCurrentView('today')}
            style={{ background: srs.due.length ? '#eff6ff' : '#fff', border: `1px solid ${srs.due.length ? '#bfdbfe' : '#e5e7eb'}`,
              borderRadius: '16px', padding: '18px', marginBottom: '16px', cursor: srs.due.length ? 'pointer' : 'default' }}>
            <div style={{ fontWeight: 800, marginBottom: '8px' }}>🔁 복습 현황</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '14px', fontSize: '0.85rem', color: '#374151' }}>
              <span>오늘 <b style={{ color: '#1d4ed8' }}>{srs.due.length}</b></span>
              <span>밀림 <b style={{ color: backlog ? '#dc2626' : '#374151' }}>{backlog}</b></span>
              <span>마스터 <b style={{ color: '#16a34a' }}>{cv.mastered}</b></span>
              <span style={{ color: '#6b7280' }}>
                다음 예정 {srs.nextDue != null ? `${new Date(srs.nextDue).getMonth() + 1}/${new Date(srs.nextDue).getDate()}` : '–'}
              </span>
            </div>
            {srs.due.length > 0 && <div style={{ fontSize: '0.8rem', color: '#1d4ed8', marginTop: '8px' }}>오늘 복습 시작 →</div>}
          </section>

          {/* 추세 */}
          <section style={{ background: '#fff', borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
              <span style={{ fontWeight: 800 }}>최근 {trendDays}일 · {analytics.trendSum}문제</span>
              <span style={{ display: 'flex', gap: '4px' }}>
                {[7, 30].map(d => (
                  <button key={d} onClick={() => setTrendDays(d)}
                    style={{ border: 'none', borderRadius: '6px', padding: '4px 10px', fontSize: '0.72rem', fontWeight: 700, cursor: 'pointer',
                      background: trendDays === d ? 'var(--primary)' : '#f1f5f9', color: trendDays === d ? '#fff' : '#6b7280' }}>{d}일</button>
                ))}
              </span>
            </div>
            <div style={{ display: 'flex', gap: trendDays > 7 ? '2px' : '6px', alignItems: 'flex-end', height: '64px' }}>
              {analytics.trend.map((t, i) => (
                <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-end', height: '100%' }}>
                  <div title={`${t.count}문제${t.acc != null ? ` · ${t.acc}%` : ''}`} style={{
                    width: '100%', borderRadius: '3px 3px 0 0',
                    height: `${t.count ? Math.max(4, (t.count / analytics.trendMax) * 44) : 3}px`,
                    background: t.count ? (t.isToday ? 'var(--primary)' : '#93c5fd') : '#eee',
                  }} />
                  <div style={{ fontSize: '0.6rem', marginTop: '3px', color: t.isToday ? 'var(--primary)' : '#9ca3af', fontWeight: t.isToday ? 700 : 500 }}>{t.label}</div>
                </div>
              ))}
            </div>
          </section>

          {/* 약점 */}
          <section style={{ background: '#fff', borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
            <div style={{ fontWeight: 800, marginBottom: '10px' }}>약점 진단</div>
            <div style={{ fontSize: '0.78rem', fontWeight: 700, color: '#6b7280', marginBottom: '6px' }}>난이도별 정답률</div>
            <div style={{ display: 'flex', gap: '6px', marginBottom: '14px' }}>
              {analytics.diffAcc.map(({ d, acc }) => {
                const m = DIFFICULTY_META[d] || {};
                return (
                  <div key={d} style={{ flex: 1, textAlign: 'center' }}>
                    <div style={{ height: '40px', display: 'flex', alignItems: 'flex-end', justifyContent: 'center' }}>
                      <div style={{ width: '64%', borderRadius: '3px 3px 0 0', height: `${acc == null ? 3 : Math.max(4, acc * 0.38)}px`, background: acc == null ? '#e5e7eb' : (m.fg || 'var(--primary)') }} />
                    </div>
                    <div style={{ fontSize: '0.62rem', color: '#9ca3af', marginTop: '3px' }}>난{d}</div>
                    <div style={{ fontSize: '0.68rem', fontWeight: 700, color: acc == null ? '#9ca3af' : '#374151' }}>{acc == null ? '–' : `${acc}%`}</div>
                  </div>
                );
              })}
            </div>
            {analytics.weak.length === 0 ? (
              <div style={{ fontSize: '0.85rem', color: '#9ca3af' }}>과목당 5문제 이상 풀면 약점이 분석돼요</div>
            ) : analytics.weak.map(w => (
              <div key={w.name} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                border: '1px solid #fecaca', background: '#fef2f2', borderRadius: '10px', padding: '10px 12px', marginBottom: '6px',
                cursor: 'pointer' }} onClick={() => startConcept(w.name, `${w.name} 집중 학습`)}>
                <span style={{ color: '#7f1d1d', fontSize: '0.88rem' }}><b>{w.name}</b>{w.weakSection && <span style={{ fontSize: '0.75rem', color: '#9a3412' }}> · {w.weakSection.nm}</span>}</span>
                <span style={{ fontWeight: 800, color: '#dc2626' }}>{w.acc}%</span>
              </div>
            ))}
          </section>

          {/* 시험별 진척 */}
          <section style={{ background: '#fff', borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
            <div style={{ fontWeight: 800, marginBottom: '10px' }}>시험별 진척</div>
            {cv.exams.map(e => (
              <div key={e.name} style={{ marginBottom: '10px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '4px' }}>
                  <span style={{ fontWeight: 600 }}>{e.name}</span>
                  <span style={{ color: '#6b7280' }}>{e.answered}/{e.total} · {e.acc == null ? '–' : `정답 ${e.acc}%`}</span>
                </div>
                <div style={{ height: '7px', background: '#f1f5f9', borderRadius: '999px', overflow: 'hidden' }}>
                  <div style={{ width: `${e.coverPct}%`, height: '100%', background: 'var(--primary)' }} />
                </div>
              </div>
            ))}
          </section>

          {/* 북마크 요약 */}
          {bookmarkedList.length > 0 && (
            <section style={{ background: '#fffbeb', border: '1px solid #fde68a', borderRadius: '16px', padding: '18px', marginBottom: '8px' }}>
              <div style={{ fontWeight: 800, marginBottom: '10px', color: '#b45309' }}>★ 북마크 {bookmarkedList.length}</div>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {BM_REASONS.map(r => {
                  const ids = bookmarkedList.filter(q => bmReasonOf(bm[qid(q)]) === r).map(qid);
                  if (!ids.length) return null;
                  const m = BM_META[r];
                  return (
                    <button key={r} onClick={() => startReview(ids, `북마크 · ${m.label}`, 'status')}
                      style={{ border: `1px solid ${m.color}`, background: '#fff', color: m.color, borderRadius: '999px',
                        padding: '7px 13px', fontSize: '0.82rem', fontWeight: 700, cursor: 'pointer' }}>
                      {m.icon} {m.label} {ids.length}
                    </button>
                  );
                })}
              </div>
            </section>
          )}

          <button onClick={() => setCurrentView('profile')}
            style={{ width: '100%', textAlign: 'left', padding: '14px 16px', borderRadius: '12px', marginBottom: '8px',
              border: '1px solid #d1d5db', background: '#fff', color: '#374151', cursor: 'pointer',
              display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: 700 }}>👤 프로필 · 데이터 백업</span>
            <span style={{ fontSize: '0.8rem', color: '#9ca3af' }}>관리 →</span>
          </button>
        </main>
      </div>
    );
  }

  if (currentView === 'today') {
    const fmtDate = (ms) => {
      const d = new Date(ms), t = new Date(); t.setHours(0, 0, 0, 0);
      const diff = Math.round((new Date(ms).setHours(0, 0, 0, 0) - t.getTime()) / DAY);
      const label = diff <= 0 ? '오늘' : diff === 1 ? '내일' : `${diff}일 후`;
      return `${d.getMonth() + 1}/${d.getDate()} (${label})`;
    };
    return shell(
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => setCurrentView('reviewHome')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>복습 홈</span>
          </button>
        </header>
        <div style={{ padding: '24px 20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700 }}>📅 오늘 복습</h1>
          <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>
            오늘 복습 {srs.due.length}문제
            {srs.capped && <> · 전체 {srs.dueTotal}개 중 (나머지는 다음에)</>}
            · 맞히면 간격이 늘어 더 나중에 나와요
          </div>
          <div style={{ display: 'flex', gap: '6px', marginTop: '12px' }}>
            {Object.entries(SRS_MODES).map(([m, cfg]) => (
              <button key={m} onClick={() => setSrsMode(m)}
                style={{ flex: 1, padding: '8px', borderRadius: '8px', cursor: 'pointer', fontSize: '0.82rem', fontWeight: 700,
                  border: srsMode === m ? '1px solid var(--primary)' : '1px solid #d1d5db',
                  background: srsMode === m ? 'var(--primary)' : '#fff',
                  color: srsMode === m ? '#fff' : '#374151' }}>
                {cfg.label}
                <span style={{ display: 'block', fontWeight: 500, fontSize: '0.68rem', opacity: 0.8 }}>
                  하루 {cfg.cap === Infinity ? '무제한' : `${cfg.cap}개`}
                </span>
              </button>
            ))}
          </div>
        </div>
        <main className="main-content" style={{ marginTop: '20px' }}>
          {srs.due.length === 0 ? (
            <div className="empty-state">
              <span className="emoji">🎉</span>
              <div className="title">오늘 복습할 문제가 없어요</div>
              <div className="sub">
                {srs.nextDue != null
                  ? <>다음 복습 예정: <b>{fmtDate(srs.nextDue)}</b></>
                  : '문제를 풀다 틀리면 복습 일정이 생겨요'}
              </div>
            </div>
          ) : (
            <div className="study-grid">
              <div className="study-card"
                onClick={() => startReview(srs.due.map(qid), '오늘 복습 전체', 'today')}
                style={{ background: '#eff6ff', borderColor: '#bfdbfe', cursor: 'pointer' }}>
                <div className="card-badge" style={{ background: 'var(--primary)', color: '#fff', border: 'none' }}>전체</div>
                <h3 className="card-title" style={{ fontSize: '1.1rem' }}>오늘 복습 전체</h3>
                <div className="card-total">총 {srs.due.length} 문제</div>
                <div className="play-btn" style={{ background: 'var(--primary)', color: '#fff' }}>시작</div>
              </div>
              {srs.groups.map((g) => (
                <div key={g.subj} className="study-card"
                  onClick={() => startReview(g.ids, `${g.subj} 오늘 복습`, 'today')}
                  style={{ cursor: 'pointer' }}>
                  <div className="card-badge">과목</div>
                  <div className="card-subtitle">오늘 복습</div>
                  <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{g.subj}</h3>
                  <div className="card-total">{g.count} 문제</div>
                  <div className="play-btn">시작</div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    );
  }

  if (currentView === 'review') {
    // 현재 스코프(전체 또는 선택 과목)의 오답 집합
    const scopeWrong = reviewSubject
      ? wrongList.filter(q => (q.taxSubjectName || '기타') === reviewSubject)
      : wrongList;
    // 난이도 오답 분포 (1~5)
    const dist = [1, 2, 3, 4, 5].map(d => scopeWrong.filter(q => q.difficulty === d).length);
    const distMax = Math.max(1, ...dist);
    // 과목 선택 시 절(section) 단위 그룹
    const sectionGroups = (() => {
      if (!reviewSubject) return [];
      const by = {};
      for (const q of scopeWrong) {
        const k = q.taxSectionName || q.taxChapterName || q.taxSubSubjectName || '기타';
        (by[k] || (by[k] = [])).push(q);
      }
      return Object.entries(by).map(([sec, qs]) => ({ sec, ids: qs.map(qid), count: qs.length }))
        .sort((a, b) => b.count - a.count);
    })();
    return shell(
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => reviewSubject ? setReviewSubject(null) : setCurrentView('reviewHome')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>{reviewSubject ? '뒤로가기' : '복습 홈'}</span>
          </button>
        </header>
        <div style={{ padding: '24px 20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700 }}>
            {reviewSubject ? `${reviewSubject} 오답` : '오답 복습'}
          </h1>
          <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>
            {reviewSubject ? '절 단위로 약점을 좁혀 복습하세요' : '여러 번 틀린·어려운 문제부터 우선 출제됩니다'}
          </div>
          {scopeWrong.length > 0 && (
            <div style={{ display: 'flex', gap: '6px', alignItems: 'flex-end', marginTop: '14px', height: '44px' }}>
              {dist.map((c, i) => (
                <div key={i} style={{ flex: 1, textAlign: 'center' }}>
                  <div style={{ height: `${Math.round((c / distMax) * 32)}px`, background: (DIFFICULTY_META[i + 1] || {}).fg || '#9ca3af', borderRadius: '3px 3px 0 0', minHeight: c ? '3px' : '0' }} />
                  <div style={{ fontSize: '0.65rem', color: '#9ca3af', marginTop: '3px' }}>난{i + 1}·{c}</div>
                </div>
              ))}
            </div>
          )}
        </div>
        <main className="main-content" style={{ marginTop: '20px' }}>
          {scopeWrong.length === 0 ? (
            <div className="empty-state">
              <span className="emoji">🎉</span>
              <div className="title">{reviewSubject ? '이 과목 오답을 모두 해결했어요' : '복습할 오답이 없어요'}</div>
              <div className="sub">{reviewSubject ? '다른 과목도 확인해 보세요' : '잘하고 있어요! 계속 풀어볼까요?'}</div>
            </div>
          ) : (
            <div className="study-grid">
              <div className="study-card"
                onClick={() => startReview(scopeWrong.map(qid), reviewSubject ? `${reviewSubject} 오답` : '전체 오답 복습')}
                style={{ background: '#fef2f2', borderColor: '#fecaca', cursor: 'pointer' }}>
                <div className="card-badge" style={{ background: '#ef4444', color: '#fff', border: 'none' }}>{reviewSubject ? '과목 전체' : '전체'}</div>
                <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{reviewSubject ? `${reviewSubject} 전체 오답` : '전체 오답 복습'}</h3>
                <div className="card-total">총 {scopeWrong.length} 문제</div>
                <div className="play-btn" style={{ background: '#ef4444', color: '#fff' }}>복습</div>
              </div>
              {!reviewSubject && reviewGroups.map((g) => (
                <div key={g.subj} className="study-card" onClick={() => setReviewSubject(g.subj)} style={{ cursor: 'pointer' }}>
                  <div className="card-badge">과목</div>
                  <div className="card-subtitle">절 단위로 좁히기 →</div>
                  <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{g.subj}</h3>
                  <div className="card-total">오답 {g.count} 문제</div>
                  <div className="play-btn">선택</div>
                </div>
              ))}
              {reviewSubject && sectionGroups.map((g) => (
                <div key={g.sec} className="study-card" onClick={() => startReview(g.ids, `${g.sec} 오답`)} style={{ cursor: 'pointer' }}>
                  <div className="card-badge">절</div>
                  <div className="card-subtitle">{reviewSubject}</div>
                  <h3 className="card-title" style={{ fontSize: '1.05rem' }}>{g.sec}</h3>
                  <div className="card-total">오답 {g.count} 문제</div>
                  <div className="play-btn">복습</div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    );
  }

  // ===== 홈 탭: 학습 통계 + 오늘 복습 배너 =====
  if (currentView === 'home' && overall.answered === 0) {
    // 첫 사용자: 0의 벽 대신 단일 가치 행동으로 착지
    return shell(
      <div className="app-container">
        <div style={{ position: 'absolute', right: 16, top: 'calc(env(safe-area-inset-top,0px) + 14px)',
          zIndex: 10, display: 'flex', gap: 10 }}>
          <button aria-label="설정" onClick={() => setCurrentView('settings')}
            style={{ width: 38, height: 38, borderRadius: '50%', border: '1px solid #e5e7eb',
              background: '#fff', color: '#6b7280', cursor: 'pointer' }}>⚙️</button>
        </div>
        <main className="welcome">
          <div className="welcome-mark">감정평가사 1차 기출</div>
          <h1 className="welcome-title">기출 12,000제,<br />풀면서 개념까지.</h1>
          <p className="welcome-sub">시험에 나온 문제로 바로 시작하세요. 가입 없이.</p>
          <button className="welcome-cta" onClick={startFirstTaste}>
            30초 안에 첫 문제 풀어보기
          </button>
          <button className="welcome-2nd" onClick={() => setCurrentView('dashboard')}>
            시험·과목별로 골라 보기 →
          </button>
          <div className="welcome-bullets">
            {ONB_BULLETS.map((b, i) => (
              <div key={i} className="welcome-bullet">
                <span style={{ fontSize: '1.3rem' }}>{b.emoji}</span>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#374151' }}>{b.t}</div>
                  <div style={{ fontSize: '0.78rem', color: '#9ca3af' }}>{b.d}</div>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    );
  }

  if (currentView === 'home') {
    return shell(
    <div className="app-container">
      <div className="banner">
        <div style={{ position: 'absolute', right: '16px',
          top: 'calc(env(safe-area-inset-top, 0px) + 14px)', zIndex: 10,
          display: 'flex', gap: '10px' }}>
          <button aria-label="프로필" onClick={() => setCurrentView('profile')}
            style={{ width: 40, height: 40, borderRadius: '50%', border: 'none', cursor: 'pointer',
              background: 'rgba(255,255,255,0.18)', color: '#fff', fontSize: '1.1rem',
              display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            👤
          </button>
          <button aria-label="설정" onClick={() => setCurrentView('settings')}
            style={{ width: 40, height: 40, borderRadius: '50%', border: 'none', cursor: 'pointer',
              background: 'rgba(255,255,255,0.18)', color: '#fff', fontSize: '1.1rem',
              display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            ⚙️
          </button>
        </div>
        <div className="banner-content">
          <div className="banner-title">감정평가사 1차 기출</div>
          <p style={{ marginTop: '6px', opacity: 0.85, fontSize: '0.9rem', fontWeight: 500 }}>
            {nickname ? `${nickname}님, 오늘도 한 걸음 더` : '오늘도 한 걸음 더'}
          </p>
        </div>
      </div>

      <main className="main-content">
        {/* 오늘 할 일 — 단일 다음 행동(선택 부담 제거: Duolingo path 원칙) */}
        {(() => {
          const w0 = analytics.weak[0];
          let act;
          if (srs.due.length > 0) {
            act = { tag: '복습', title: `오늘 복습 ${srs.due.length}문제`,
              desc: '기억 곡선이 도래했어요 · 지금이 가장 잘 외워질 때',
              go: () => setCurrentView('today') };
          } else if (w0) {
            act = { tag: '약점 보강', title: `${w0.name} 집중`,
              desc: `현재 정답률 ${w0.acc}% — 약한 곳부터 끌어올려요`,
              go: () => startConcept(w0.name, `${w0.name} 집중 학습`) };
          } else {
            act = { tag: '추천', title: `오늘의 추천 ${dailyGoal}문제`,
              desc: '미학습 위주로 골라 담았어요 · 한 번에 시작',
              go: startRecommended };
          }
          return (
            <button onClick={act.go} className="todo-hero">
              <span className="todo-tag">{act.tag}</span>
              <span className="todo-title">{act.title}</span>
              <span className="todo-desc">{act.desc}</span>
              <span className="todo-cta">바로 시작하기 →</span>
            </button>
          );
        })()}

        {/* 다음 목표(마일스톤) — 단일 진행 지표 */}
        {(() => {
          const ms = [50, 100, 300, 500, 1000, 2000, 3000, 5000];
          const next = ms.find(m => overall.answered < m);
          if (!next) return null;
          const prev = ms[ms.indexOf(next) - 1] || 0;
          const p = Math.round(((overall.answered - prev) / (next - prev)) * 100);
          return (
            <div className="milestone">
              <div className="milestone-row">
                <span>🏁 다음 목표 <b>{next}문제</b></span>
                <span style={{ color: 'var(--text-sub)' }}>{next - overall.answered}문제 남음</span>
              </div>
              <div className="progress-bar-container" style={{ marginTop: 8, height: 6 }}>
                <div className="progress-bar-fill" style={{ width: `${p}%` }} />
              </div>
            </div>
          );
        })()}

        {/* 오늘의 목표 */}
        {(() => {
          const goal = dailyGoal;
          const done = analytics.todayCount;
          const gpct = Math.min(100, Math.round((done / (goal || 1)) * 100));
          const reached = done >= goal;
          return (
            <section style={{ background: '#fff', borderRadius: '16px', padding: '18px',
              boxShadow: 'var(--shadow-md)', marginBottom: '14px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                <div style={{ fontWeight: 800, fontSize: '1.05rem', color: '#111827' }}>
                  {reached ? '🎉 오늘 목표 달성!' : '🎯 오늘의 목표'}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#6b7280', fontWeight: 600 }}>
                  <span style={{ color: reached ? '#16a34a' : '#1d4ed8', fontWeight: 800 }}>{done}</span> / {goal}문제
                </div>
              </div>
              <div className="progress-bar-container" style={{ marginTop: '12px' }}>
                <div className="progress-bar-fill" style={{ width: `${gpct}%`,
                  background: reached ? '#16a34a' : undefined }}></div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '14px' }}>
                <div style={{ display: 'flex', gap: '6px' }}>
                  {analytics.weekMet.map((w, i) => (
                    <div key={i} title={w.label} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                      <div style={{ width: 22, height: 22, borderRadius: '50%',
                        background: w.met ? '#16a34a' : '#e5e7eb',
                        color: w.met ? '#fff' : '#9ca3af', fontSize: '0.7rem',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        outline: w.isToday ? '2px solid #1d4ed8' : 'none', outlineOffset: '1px' }}>
                        {w.met ? '✓' : ''}
                      </div>
                      <span style={{ fontSize: '0.68rem', color: '#9ca3af' }}>{w.label}</span>
                    </div>
                  ))}
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#ea580c' }}>
                    🔥 {analytics.streak}일
                  </div>
                  <div style={{ fontSize: '0.7rem', color: '#9ca3af' }}>연속 학습</div>
                </div>
              </div>
            </section>
          );
        })()}

        {/* 다른 방법으로 — 보조 경로(시각 비중↓, 선택 부담 분산 방지) */}
        <section style={{ marginBottom: '14px' }}>
          <div style={{ display: 'flex', gap: '8px' }}>
            {[
              { t: '둘러보기', on: () => setCurrentView('dashboard') },
              { t: '랜덤 20', on: () => startRandom(20) },
              { t: '검색', on: () => setCurrentView('search') },
            ].map((b, i) => (
              <button key={i} onClick={b.on}
                style={{ flex: 1, padding: '11px 8px', borderRadius: '10px', cursor: 'pointer',
                  border: '1px solid #e5e7eb', background: '#fff', color: '#374151',
                  fontSize: '0.85rem', fontWeight: 600 }}>
                {b.t}
              </button>
            ))}
          </div>
        </section>

        {/* 약점 집중 */}
        {analytics.weak.length > 0 && (
          <section style={{ marginBottom: '14px' }}>
            <div style={{ fontWeight: 800, fontSize: '0.95rem', color: '#374151', margin: '0 2px 10px' }}>
              📉 약점 집중
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {analytics.weak.map((w) => (
                <button key={w.name} onClick={() => startConcept(w.name, `${w.name} 집중 학습`)}
                  style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '10px',
                    padding: '13px 15px', borderRadius: '12px', cursor: 'pointer',
                    border: '1px solid #fecaca', background: '#fef2f2', textAlign: 'left' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.9rem', color: '#374151' }}>{w.name}</span>
                  <span style={{ fontSize: '0.82rem', color: '#dc2626', fontWeight: 700, flexShrink: 0 }}>
                    정답률 {w.acc}% · 보강 →
                  </span>
                </button>
              ))}
            </div>
          </section>
        )}

        {/* 학습 진행 요약 */}
        <section className="overview-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <h2 className="overview-title">나의 학습 진행</h2>
              <p className="overview-subtitle">전체 {totalQuestions}개 문항 중 현재 진행 현황</p>
            </div>
            {overall.answered > 0 && (
              <button
                onClick={() => { if (window.confirm('학습 진행률을 모두 초기화할까요?')) resetProgress(); }}
                style={{ background: 'var(--primary-light)', padding: '8px 16px', borderRadius: '12px', color: 'var(--primary)', fontWeight: '700', fontSize: '0.9rem', border: 'none', cursor: 'pointer' }}
              >
                초기화
              </button>
            )}
          </div>

          {(() => {
            const pct = totalQuestions ? Math.round((overall.answered / totalQuestions) * 100) : 0;
            const acc = overall.accuracy;
            return (
              <>
                <div className="progress-bar-container">
                  <div className="progress-bar-fill" style={{ width: `${pct}%` }}></div>
                </div>
                <div className="progress-stats">
                  <div>
                    <span className="stat-dot"></span>
                    학습한 문제 <span className="stat-bold">{overall.answered}/{totalQuestions}</span>
                    {acc !== null && <> · 정답률 <span className="stat-bold" style={{ color: '#16a34a' }}>{acc}%</span></>}
                  </div>
                  <div>{pct}%</div>
                </div>
              </>
            );
          })()}

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '8px', marginTop: '16px' }}>
            {[
              ['미응답', coverage.unseen, '#6b7280', '#f3f4f6'],
              ['학습', coverage.learned, '#1d4ed8', '#eff6ff'],
              ['복습필요', coverage.review, '#dc2626', '#fef2f2'],
              ['마스터', coverage.mastered, '#16a34a', '#f0fdf4'],
            ].map(([lbl, n, c, bg]) => (
              <div key={lbl} style={{ background: bg, borderRadius: '10px', padding: '10px 6px', textAlign: 'center' }}>
                <div style={{ fontSize: '1.05rem', fontWeight: 800, color: c }}>{n}</div>
                <div style={{ fontSize: '0.7rem', color: '#6b7280', marginTop: '2px' }}>{lbl}</div>
              </div>
            ))}
          </div>

          {overall.answered > 0 && (
            <button
              onClick={() => setCurrentView('status')}
              style={{ width: '100%', textAlign: 'center', padding: '12px', marginTop: '14px', borderRadius: '12px',
                border: '1px solid #bfdbfe', background: '#eff6ff', color: '#1d4ed8', cursor: 'pointer',
                fontWeight: 700, fontSize: '0.9rem' }}
            >
              📊 학습 현황 자세히 보기 →
            </button>
          )}
        </section>

        {/* 시험별 진척 */}
        {coverage.exams.length > 0 && (
          <section style={{ marginBottom: '14px' }}>
            <div style={{ fontWeight: 800, fontSize: '0.95rem', color: '#374151', margin: '0 2px 10px' }}>
              📋 시험별 진척
            </div>
            <div style={{ background: '#fff', borderRadius: '14px', padding: '14px', boxShadow: 'var(--shadow-sm)',
              display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {coverage.exams.slice(0, 4).map((e) => (
                <button key={e.name} onClick={() => enterTaxScope({ kind: 'exam', value: e.name, label: e.name })}
                  style={{ border: 'none', background: 'transparent', cursor: 'pointer', textAlign: 'left', padding: 0 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '5px' }}>
                    <span style={{ fontWeight: 700, color: '#374151' }}>{e.name}</span>
                    <span style={{ color: '#6b7280' }}>
                      {e.coverPct}%{e.acc != null && <> · 정답 {e.acc}%</>}
                    </span>
                  </div>
                  <div className="progress-bar-container" style={{ height: '7px' }}>
                    <div className="progress-bar-fill" style={{ width: `${e.coverPct}%` }}></div>
                  </div>
                </button>
              ))}
            </div>
          </section>
        )}

        {/* 복습 알림 */}
        <div style={{ width: '100%', padding: '14px 16px', marginBottom: '8px', borderRadius: '12px',
          border: '1px solid #e5e7eb', background: '#fff',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px' }}>
          <div>
            <div style={{ fontWeight: 700, fontSize: '0.92rem', color: '#374151' }}>🔔 복습 알림</div>
            <div style={{ fontSize: '0.78rem', color: '#9ca3af', marginTop: '2px' }}>
              {srs.nextDue != null && !srs.due.length
                ? `다음 복습 ${new Date(srs.nextDue).getMonth() + 1}/${new Date(srs.nextDue).getDate()}`
                : '복습할 게 생기면 알려드려요'}
            </div>
          </div>
          <button
            onClick={() => {
              if (typeof Notification === 'undefined') return;
              if (Notification.permission === 'granted') setNotifPref(p => !p);
              else Notification.requestPermission().then(r => setNotifPref(r === 'granted'));
            }}
            style={{ flexShrink: 0, border: notifPref ? '1px solid #2563eb' : '1px solid #d1d5db',
              background: notifPref ? '#eff6ff' : '#fff', borderRadius: '8px',
              padding: '8px 14px', fontSize: '0.8rem', cursor: 'pointer',
              color: notifPref ? '#1d4ed8' : '#6b7280', fontWeight: 600 }}
          >
            {notifPref ? '켜짐' : '받기'}
          </button>
        </div>

      </main>
    </div>
    );
  }

  // ===== 설정 =====
  if (currentView === 'settings') {
    const segRow = (title, desc, opts, cur, onPick) => (
      <section style={{ background: '#fff', borderRadius: '14px', padding: '16px', boxShadow: 'var(--shadow-sm)', marginBottom: '12px' }}>
        <div style={{ fontWeight: 700, fontSize: '0.95rem', color: '#374151' }}>{title}</div>
        {desc && <div style={{ fontSize: '0.78rem', color: '#9ca3af', marginTop: '3px' }}>{desc}</div>}
        <div style={{ display: 'flex', gap: '8px', marginTop: '12px', flexWrap: 'wrap' }}>
          {opts.map(([val, lbl]) => {
            const on = cur === val;
            return (
              <button key={String(val)} onClick={() => onPick(val)}
                style={{ flex: '1 1 auto', minWidth: '64px', padding: '9px 10px', borderRadius: '9px', cursor: 'pointer',
                  fontSize: '0.85rem', fontWeight: 600,
                  border: on ? '1px solid #2563eb' : '1px solid #d1d5db',
                  background: on ? '#eff6ff' : '#fff', color: on ? '#1d4ed8' : '#6b7280' }}>
                {lbl}
              </button>
            );
          })}
        </div>
      </section>
    );
    return shell(
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => setCurrentView('home')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>홈</span>
          </button>
        </header>
        <div className="screen-head"><h1 className="screen-title">⚙️ 설정</h1></div>
        <main className="main-content" style={{ marginTop: '16px' }}>
          {segRow('복습 강도', '간격 반복 일정의 빡셈 정도를 정해요.',
            Object.entries(SRS_MODES).map(([k, v]) => [k, v.label]), srsMode, setSrsMode)}
          {segRow('일일 학습 목표', '하루에 풀 문제 수 목표예요.',
            [[10, '10문제'], [20, '20문제'], [30, '30문제'], [50, '50문제']], dailyGoal, setDailyGoal)}
          {segRow('학습 순서', '가이드 학습에서 문제가 나오는 순서예요.',
            [['difficulty', '난이도순'], ['random', '무작위']], studyOrder, setStudyOrder)}
          {segRow('글자 크기', '문제·보기·해설 본문 크기예요.',
            [[0.9, '작게'], [1, '보통'], [1.18, '크게']], fontScale, setFontScale)}
          {segRow('자동 다음', '정답 확인 후 다음 문제로 자동 이동할지 정해요.',
            [[true, '켜기'], [false, '끄기']], autoNext, setAutoNext)}
          {autoNext && segRow('자동 다음 대기', '자동 이동 전 해설을 볼 시간이에요.',
            [[3, '3초'], [5, '5초'], [8, '8초']], autoSec, setAutoSec)}
          {segRow('학습 추세 기간', '현황 화면 추세 그래프의 기간이에요.',
            [[7, '7일'], [30, '30일']], trendDays, setTrendDays)}
          <section style={{ background: '#fff', borderRadius: '14px', padding: '16px', boxShadow: 'var(--shadow-sm)', marginBottom: '12px',
            display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px' }}>
            <div>
              <div style={{ fontWeight: 700, fontSize: '0.95rem', color: '#374151' }}>복습 알림</div>
              <div style={{ fontSize: '0.78rem', color: '#9ca3af', marginTop: '3px' }}>
                오늘 복습할 문제가 있으면 앱을 열 때 하루 한 번 알려줘요.
              </div>
            </div>
            <button
              onClick={() => {
                if (typeof Notification === 'undefined') return;
                if (Notification.permission === 'granted') setNotifPref(p => !p);
                else Notification.requestPermission().then(r => setNotifPref(r === 'granted'));
              }}
              style={{ flexShrink: 0, border: notifPref ? '1px solid #2563eb' : '1px solid #d1d5db',
                background: notifPref ? '#eff6ff' : '#fff', borderRadius: '9px', padding: '9px 14px',
                fontSize: '0.85rem', cursor: 'pointer', fontWeight: 600,
                color: notifPref ? '#1d4ed8' : '#6b7280' }}>
              {notifPref ? '🔔 켜짐' : '🔕 꺼짐'}
            </button>
          </section>
          <button onClick={() => setCurrentView('profile')}
            style={{ width: '100%', textAlign: 'left', padding: '14px 16px', borderRadius: '12px',
              border: '1px solid #d1d5db', background: '#fff', color: '#374151', cursor: 'pointer',
              display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: 700 }}>👤 내 프로필 · 백업·데이터 관리</span>
            <span style={{ fontSize: '0.8rem', color: '#9ca3af' }}>→</span>
          </button>
        </main>
      </div>
    );
  }

  // ===== 복습 탭: 오늘 복습 / 오답 복습 진입 =====
  if (currentView === 'reviewHome') {
    return shell(
    <div className="app-container">
      <div className="screen-head">
        <h1 className="screen-title">🔁 복습</h1>
        <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>기억 곡선 복습과 누적 오답을 한곳에서</p>
      </div>
      <main className="main-content" style={{ marginTop: '16px' }}>
        <div
          onClick={() => srs.due.length && setCurrentView('today')}
          style={{ padding: '18px', marginBottom: '12px', borderRadius: '12px',
            border: `1px solid ${srs.due.length ? '#bfdbfe' : '#e5e7eb'}`,
            background: srs.due.length ? '#eff6ff' : '#fff',
            cursor: srs.due.length ? 'pointer' : 'default' }}
        >
          <div style={{ fontWeight: 700, fontSize: '1.05rem', color: srs.due.length ? '#1d4ed8' : '#6b7280' }}>
            📅 오늘 복습 {srs.due.length > 0 ? `${srs.due.length}문제` : '없음'}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: '4px' }}>
            {srs.due.length > 0
              ? '기억 곡선에 따라 오늘 풀 차례예요 →'
              : (srs.nextDue != null
                  ? `다음 복습 예정: ${new Date(srs.nextDue).getMonth() + 1}/${new Date(srs.nextDue).getDate()}`
                  : '틀린 문제가 쌓이면 복습 일정이 생겨요')}
          </div>
        </div>
        <div
          onClick={() => wrongList.length && (setReviewSubject(null), setCurrentView('review'))}
          style={{ padding: '18px', borderRadius: '12px',
            border: `1px solid ${wrongList.length ? '#fecaca' : '#e5e7eb'}`,
            background: wrongList.length ? '#fef2f2' : '#fff',
            cursor: wrongList.length ? 'pointer' : 'default' }}
        >
          <div style={{ fontWeight: 700, fontSize: '1.05rem', color: wrongList.length ? '#b91c1c' : '#9ca3af' }}>
            🔁 오답 복습 {wrongList.length > 0 ? `${wrongList.length}문제` : '없음'}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: '4px' }}>
            {wrongList.length > 0 ? '틀린 문제를 과목·절별로 다시 풀기 →' : '아직 틀린 문제가 없어요'}
          </div>
        </div>
        <div style={{ padding: '18px', marginTop: '12px', borderRadius: '12px',
          border: `1px solid ${bookmarkedList.length ? '#fde68a' : '#e5e7eb'}`,
          background: bookmarkedList.length ? '#fffbeb' : '#fff' }}>
          <div
            onClick={() => bookmarkedList.length && startReview(bookmarkedList.map(qid), '북마크 전체', 'reviewHome')}
            style={{ cursor: bookmarkedList.length ? 'pointer' : 'default' }}
          >
            <div style={{ fontWeight: 700, fontSize: '1.05rem', color: bookmarkedList.length ? '#b45309' : '#9ca3af' }}>
              ★ 북마크 {bookmarkedList.length > 0 ? `${bookmarkedList.length}문제` : '없음'}
            </div>
            <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: '4px' }}>
              {bookmarkedList.length > 0 ? '전체 모아 학습 →' : '문제 풀 때 ☆를 눌러 북마크(중요·헷갈림·실수)'}
            </div>
          </div>
          {bookmarkedList.length > 0 && (
            <div style={{ display: 'flex', gap: '8px', marginTop: '12px', flexWrap: 'wrap' }}>
              {BM_REASONS.map(r => {
                const ids = bookmarkedList.filter(q => bmReasonOf(bm[qid(q)]) === r).map(qid);
                if (ids.length === 0) return null;
                const m = BM_META[r];
                return (
                  <button key={r} onClick={() => startReview(ids, `북마크 · ${m.label}`, 'reviewHome')}
                    style={{ border: `1px solid ${m.color}`, background: '#fff', color: m.color,
                      borderRadius: '999px', padding: '7px 13px', fontSize: '0.82rem', fontWeight: 700, cursor: 'pointer' }}>
                    {m.icon} {m.label} {ids.length}
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </main>
    </div>
    );
  }

  // ===== 둘러보기 탭: 시험/과목/단원/연도 =====
  return shell(
    <div className="app-container">
      <div className="screen-head">
        <h1 className="screen-title">📚 둘러보기</h1>
      </div>
      <main className="main-content" style={{ marginTop: '16px' }}>
        <button
          onClick={() => setCurrentView('search')}
          style={{ width: '100%', textAlign: 'left', padding: '14px 16px', marginBottom: '20px',
            border: '1px solid #d1d5db', borderRadius: '12px', background: '#fff', color: '#6b7280',
            fontSize: '0.95rem', cursor: 'pointer' }}
        >
          🔍 통합 검색·필터 (시험·과목·연도·난이도·키워드)
        </button>
        <div className="section-header">
          <h3 className="section-title">학습 목록</h3>
          <div className="view-toggle">
            {[['exam','시험별'],['subject','과목별'],['chapter','단원별'],['year','연도별']].map(([mode,label]) => (
              <button
                key={mode}
                className={viewMode === mode ? 'active' : ''}
                onClick={() => switchTab(mode)}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <div className="study-grid">
          {activeGroups.map((group, idx) => {
            const s = progressStats(cardQuestions(group), progress);
            const pct = s.total ? Math.round((s.answered / s.total) * 100) : 0;
            const dm = s.level ? (DIFFICULTY_META[s.level] || null) : null;
            return (
            <div key={idx} className="study-card" onClick={() => handleGroupClick(group)}>
              {dm && (
                <div className="card-badge" style={{ background: dm.bg, color: dm.fg, border: 'none' }}>
                  난이도 {s.avgDiff.toFixed(1)}
                </div>
              )}
              <h3 className="card-title">{group.title}</h3>
              <div className="card-total">
                {group.total}문제{s.answered > 0 && <> · 학습 {s.answered}<span style={{ color: '#9ca3af' }}>/{s.total}</span></>}
              </div>

              <div className="card-progress-container">
                <div className="card-progress-fill" style={{ width: `${pct}%` }}></div>
              </div>

              <div className="play-btn">풀기</div>
            </div>
            );
          })}
        </div>
      </main>
    </div>
  );
};

export default App;
