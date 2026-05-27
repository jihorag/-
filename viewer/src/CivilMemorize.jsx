// 통암기 — 감정평가사 1차 교재 기반 cloze + SRS
// 다과목 지원: SUBJECTS 메타 + /data/<subject>/{civil_total,civil_cards,civil_curated}.json
// (민법은 기존 /data/civil/ 경로 유지)
//
// SRS: localStorage 'mem-srs:<cardId>' — 기출과 분리된 자체 박스
// localStorage keys:
//   mem-srs          : { [cardId]: { box, due, reps, lapses, last } }
//   mem-howto-seen   : '1' (가이드 본 이력)
//   mem-session-size : 10|20|30|50 (기본 20)
//   mem-fs           : 0.9|1|1.15|1.3 (글자 배율)
//   mem-haptic       : '1'|'0' (햅틱 토글)
//   mem-daily        : { [YYYY-MM-DD]: { correct, wrong, mastered } }
//   mem-bookmarks    : { [cardId]: true } — 어려운 카드 모음
//   mem-theme        : 'auto'|'light'|'dark'
//   mem-mode         : 'simple'|'sm2'|'type'|'choice' (응답 모드, 기본 simple)
//   mem-interleave   : '1'|'0' (단원 잠금 해제, 책 전체 셔플)
//   mem-notes        : { [cardId]: text } — 자기 설명 노트
//   mem-exam-date    : 'YYYY-MM-DD' — D-DAY 시험일
//   mem-daily-goal   : 10|20|30|50|null — 일일 목표(없으면 D-DAY로 자동)
//   mem-hidden       : { [cardId]: true } — 신고로 숨긴 카드
//   mem-freeze       : { lastFreezeKey: 'YYYY-MM-DD', tokens: N } — 스트릭 보호
//   mem-byok         : string — Claude API 키 (BYOK)

import { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

// ─── 과목 메타 ────────────────────────────────────────────────
// 다과목 확장: 새 과목 추가 시 entry만 늘리면 됨. dataDir 안에 동일한 파일명 규약.
const SUBJECTS = [
  { id: 'civil', title: '민법', subtitle: '민법총칙 + 물권법', icon: '⚖️',
    dataDir: '/data/civil',
    files: { total: 'civil_total.json', cards: 'civil_cards.json', curated: 'civil_curated.json' },
    color: { primary: '#4f46e5', light: '#eef2ff', dark: '#3730a3', accent: '#818cf8' },
    comingSoon: false },
  { id: 'accounting', title: '회계학', subtitle: '재무회계 + 원가회계', icon: '💰',
    dataDir: '/data/accounting',
    files: { total: 'total.json', cards: 'cards.json', curated: 'curated.json' },
    color: { primary: '#f59e0b', light: '#fffbeb', dark: '#b45309', accent: '#fbbf24' },
    comingSoon: false },
  { id: 'realestate', title: '부동산학원론', subtitle: '국승옥 강의 기반', icon: '🏘️',
    dataDir: '/data/realestate',
    files: { total: 'total.json', cards: 'cards.json', curated: 'curated.json' },
    color: { primary: '#10b981', light: '#ecfdf5', dark: '#047857', accent: '#34d399' },
    comingSoon: false },
  { id: 'law', title: '감정평가관계법규', subtitle: '관련 법령 통암기', icon: '📜',
    dataDir: '/data/law',
    files: { total: 'total.json', cards: 'cards.json', curated: 'curated.json' },
    color: { primary: '#dc2626', light: '#fef2f2', dark: '#991b1b', accent: '#f87171' },
    comingSoon: true },
];

// ─── SRS ─────────────────────────────────────────────────────
const SRS_KEY = 'mem-srs';
const HOWTO_KEY = 'mem-howto-seen';
const SIZE_KEY = 'mem-session-size';
const FS_KEY = 'mem-fs';
const HAPTIC_KEY = 'mem-haptic';
const DAILY_KEY = 'mem-daily';
const BOOKMARK_KEY = 'mem-bookmarks';
const THEME_KEY = 'mem-theme';
const MODE_KEY = 'mem-mode';
const INTERLEAVE_KEY = 'mem-interleave';
const NOTES_KEY = 'mem-notes';
const EXAM_DATE_KEY = 'mem-exam-date';
const DAILY_GOAL_KEY = 'mem-daily-goal';
const HIDDEN_KEY = 'mem-hidden';
const FREEZE_KEY = 'mem-freeze';
const BYOK_KEY = 'mem-byok';

const EASE_DEFAULT = 2.5;
const EASE_MIN = 1.3;
const EASE_MAX = 2.7;
// 4버튼 등급: 0=다시, 1=어려움, 2=좋음, 3=쉬움
const GRADE_LABELS = ['다시', '어려움', '좋음', '쉬움'];
const GRADE_COLORS = ['#dc2626', '#ea580c', '#16a34a', '#0891b2'];
const LADDER = [1, 3, 7, 16, 35, 70]; // 일
const DAY_MS = 86400000;
const SPARKLINE_DAYS = 30;

const TYPE_META = {
  statute:    { label: '조문',  color: '#2563eb', bg: '#eff6ff' },
  definition: { label: '정의',  color: '#7c3aed', bg: '#f5f3ff' },
  bold:       { label: '핵심어', color: '#0891b2', bg: '#ecfeff' },
  mnemonic:   { label: '두문자', color: '#ea580c', bg: '#fff7ed' },
  curated:    { label: '핵심',  color: '#16a34a', bg: '#f0fdf4' },
};

// 모듈 레벨 — React Compiler가 렌더 중 setState/Math.random을 막아서 swipe transient는 여기에
const swipeState = { startX: 0, startY: 0, active: false, sid: null };

function lsLoad(key, def) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return def;
    if (typeof def === 'object') return JSON.parse(raw);
    if (typeof def === 'number') return parseFloat(raw) || def;
    return raw;
  } catch { return def; }
}
function lsSave(key, v) {
  try {
    localStorage.setItem(key, typeof v === 'object' ? JSON.stringify(v) : String(v));
  } catch { /* SSR */ }
}

function startOfDayMs(ts = Date.now()) {
  const d = new Date(ts); d.setHours(0, 0, 0, 0); return d.getTime();
}
function dateKey(d) {
  const y = d.getFullYear(), m = String(d.getMonth() + 1).padStart(2, '0'), dd = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${dd}`;
}
function todayKey() { return dateKey(new Date()); }

// 연속 학습일 (오늘부터 거꾸로 셈) — freeze 토큰 적용
// freeze 토큰: 주 1회 자동 회복. 1일 결석을 메워 streak 유지.
function computeStreak(daily, freezeData) {
  if (!daily) return { streak: 0, freezeUsedToday: false };
  let streak = 0;
  let freezeUsedToday = false;
  let availableFreezes = freezeData?.tokens || 0;
  const d = new Date();
  for (let i = 0; i < 365; i++) {
    const k = dateKey(d);
    const slot = daily[k];
    const hasStudy = slot && (slot.correct + slot.wrong) > 0;
    if (hasStudy) {
      streak++;
    } else if (i === 0) {
      // 오늘 — 그냥 건너뛰기 (어제부터 카운트)
    } else if (availableFreezes > 0) {
      // freeze 사용 — streak 유지
      availableFreezes--;
      if (i === 1) freezeUsedToday = true;
      streak++;
    } else {
      break;
    }
    d.setDate(d.getDate() - 1);
  }
  return { streak, freezeUsedToday };
}

// 주 1회 freeze 토큰 회복 (월요일 마다 +1, 최대 2개)
function refreshFreezeTokens(prev) {
  const today = new Date();
  const todayK = dateKey(today);
  if (prev?.lastCheck === todayK) return prev || { tokens: 1, lastCheck: todayK };
  // 마지막 회복 후 7일+ 지났으면 토큰 +1
  let tokens = prev?.tokens ?? 1;
  const last = prev?.lastRefresh ? new Date(prev.lastRefresh) : null;
  if (!last || (today - last) / DAY_MS >= 7) {
    tokens = Math.min(2, tokens + 1);
    return { tokens, lastRefresh: todayK, lastCheck: todayK };
  }
  return { ...prev, tokens, lastCheck: todayK };
}

// D-DAY 계산
function daysToExam(examDate) {
  if (!examDate) return null;
  const ex = new Date(examDate);
  if (isNaN(ex)) return null;
  ex.setHours(0, 0, 0, 0);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return Math.round((ex - today) / DAY_MS);
}

// 자동 일일 권장량 = (미학습 + 학습중) ÷ (D-DAY 1일 전까지 남은 일수, 최소 14일)
function computeDailyGoal(totalCards, srs, examDate, manualGoal) {
  if (manualGoal != null && manualGoal > 0) return manualGoal;
  if (!examDate) return 20;
  const days = daysToExam(examDate);
  if (days == null) return 20;
  const usable = Math.max(14, days - 7); // 시험 1주 전부턴 복습만
  const learning = totalCards - Object.values(srs).filter(s => s.box >= LADDER.length).length;
  const goal = Math.ceil(learning / usable);
  return Math.max(10, Math.min(100, goal));
}

// 트리에서 leafId로 노드 찾기
function findNodeById(root, id) {
  if (!root) return null;
  if (root.id === id) return root;
  if (!root.children) return null;
  for (const c of root.children) {
    const f = findNodeById(c, id);
    if (f) return f;
  }
  return null;
}

function nextSrs(prev, correct, now = Date.now()) {
  const cur = prev || { box: -1, due: 0, reps: 0, lapses: 0, last: 0, ease: EASE_DEFAULT };
  if (correct) {
    const nb = Math.min(LADDER.length, cur.box + 1);
    if (nb >= LADDER.length) {
      return { ...cur, box: LADDER.length, due: null, reps: cur.reps + 1, last: now };
    }
    return {
      ...cur, box: nb, due: startOfDayMs(now) + LADDER[nb] * DAY_MS,
      reps: cur.reps + 1, last: now,
    };
  }
  return {
    ...cur, box: 0, due: startOfDayMs(now) + LADDER[0] * DAY_MS,
    reps: cur.reps, lapses: cur.lapses + 1, last: now,
  };
}

// SM-2 변형: 4등급 + ease factor. interval은 box 사다리 + ease 곱.
// grade 0=다시, 1=어려움, 2=좋음, 3=쉬움
function nextSrsSm2(prev, grade, now = Date.now()) {
  const cur = prev || { box: -1, due: 0, reps: 0, lapses: 0, last: 0, ease: EASE_DEFAULT };
  const ease = Math.max(EASE_MIN, Math.min(EASE_MAX, (cur.ease ?? EASE_DEFAULT)
    + (grade === 0 ? -0.20 : grade === 1 ? -0.15 : grade === 3 ? +0.15 : 0)));

  if (grade === 0) {
    // 다시: 박스 리셋, 내일 다시
    return {
      box: 0, due: startOfDayMs(now) + LADDER[0] * DAY_MS,
      reps: cur.reps, lapses: cur.lapses + 1, last: now, ease,
    };
  }

  let nb = cur.box + (grade === 3 ? 2 : 1);
  nb = Math.min(LADDER.length, Math.max(0, nb));
  if (nb >= LADDER.length) {
    return { box: LADDER.length, due: null, reps: cur.reps + 1, lapses: cur.lapses, last: now, ease };
  }
  // 어려움이면 사다리 간격을 0.6배(다음 단계 너무 멀어지지 않게)
  const baseDays = LADDER[nb];
  const mult = grade === 1 ? 0.6 : grade === 3 ? 1.3 : 1.0;
  const days = Math.max(1, Math.round(baseDays * mult * (ease / EASE_DEFAULT)));
  return {
    box: nb, due: startOfDayMs(now) + days * DAY_MS,
    reps: cur.reps + 1, lapses: cur.lapses, last: now, ease,
  };
}

// 등급별 예상 다음 도래 일수 (UI 미리보기용, 실제 적용 없이 시뮬레이션)
function previewDays(prev, grade) {
  const ns = nextSrsSm2(prev, grade);
  if (ns.due == null) return null;
  return Math.max(1, Math.round((ns.due - startOfDayMs()) / DAY_MS));
}

// 셔플은 모듈 레벨 (React Compiler 회피)
function shuffleArr(arr) {
  const o = arr.slice();
  for (let i = o.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [o[i], o[j]] = [o[j], o[i]];
  }
  return o;
}

function buildQueue(pool, srs, size) {
  const now = Date.now();
  const due = [], fresh = [], inProg = [];
  for (const c of pool) {
    const s = srs[c.id];
    if (!s) fresh.push(c);
    else if (s.box >= LADDER.length) continue;
    else if (s.due == null || s.due <= now) due.push(c);
    else inProg.push(c);
  }
  let q = shuffleArr(due).slice(0, size);
  if (q.length < size) q = q.concat(shuffleArr(fresh).slice(0, size - q.length));
  if (q.length < size) q = q.concat(shuffleArr(inProg).slice(0, size - q.length));
  return q;
}

// ─── 메인 ─────────────────────────────────────────────────────
// 모드별 관련 과목 — 3시험 동시 준비 시 추천 과목 강조 + 비추천 dim
const EXAM_SUBJECT_RELEVANCE = {
  '감정평가사': ['civil', 'accounting', 'realestate', 'law'],
  '세무사': ['civil', 'accounting'],
  '공인중개사': ['civil', 'realestate'],
};

export default function MemorizeApp({ isTabRoot = false, onBack, browseExam = '' }) {
  // ── 상태
  const [view, setView] = useState('subjects');         // 과목 picker
  const [subjectId, setSubjectId] = useState(null);
  const subject = useMemo(() => SUBJECTS.find(s => s.id === subjectId), [subjectId]);

  const [data, setData] = useState(null);
  const [autoCards, setAutoCards] = useState(null);
  const [curated, setCurated] = useState([]);
  const [loadErr, setLoadErr] = useState(null);
  const [loading, setLoading] = useState(false);

  const [srs, setSrs] = useState(() => lsLoad(SRS_KEY, {}));
  const [daily, setDaily] = useState(() => lsLoad(DAILY_KEY, {}));
  const [howtoSeen, setHowtoSeen] = useState(() => lsLoad(HOWTO_KEY, '') === '1');
  const [sessionSize, setSessionSize] = useState(() => {
    const n = lsLoad(SIZE_KEY, 20);
    return [10, 20, 30, 50].includes(n) ? n : 20;
  });
  const [fs, setFs] = useState(() => {
    const n = lsLoad(FS_KEY, 1);
    return [0.9, 1, 1.15, 1.3].includes(n) ? n : 1;
  });
  const [haptic, setHaptic] = useState(() => lsLoad(HAPTIC_KEY, '1') === '1');
  const [bookmarks, setBookmarks] = useState(() => lsLoad(BOOKMARK_KEY, {}));
  const [theme, setTheme] = useState(() => {
    const t = lsLoad(THEME_KEY, 'auto');
    return ['auto', 'light', 'dark'].includes(t) ? t : 'auto';
  });
  const [expandSource, setExpandSource] = useState(false);
  const [respMode, setRespMode] = useState(() => {
    const m = lsLoad(MODE_KEY, 'simple');
    return ['simple', 'sm2', 'type', 'choice'].includes(m) ? m : 'simple';
  });
  const [interleave, setInterleave] = useState(() => lsLoad(INTERLEAVE_KEY, '0') === '1');
  const [notes, setNotes] = useState(() => lsLoad(NOTES_KEY, {}));

  // 세션 내 타이핑 input / 4지선다 선택 transient
  const [typedAnswer, setTypedAnswer] = useState('');
  const [choicePicked, setChoicePicked] = useState(null); // 'A'|'B'|'C'|'D'|null
  const [showNote, setShowNote] = useState(false);
  const [noteDraft, setNoteDraft] = useState('');
  const [examDate, setExamDate] = useState(() => lsLoad(EXAM_DATE_KEY, ''));
  const [dailyGoal, setDailyGoal] = useState(() => {
    const v = lsLoad(DAILY_GOAL_KEY, null);
    return v && !isNaN(parseInt(v)) ? parseInt(v) : null;
  });
  const [hidden, setHidden] = useState(() => lsLoad(HIDDEN_KEY, {}));
  const [freeze, setFreeze] = useState(() => refreshFreezeTokens(lsLoad(FREEZE_KEY, null)));
  const [byok, setByok] = useState(() => lsLoad(BYOK_KEY, ''));

  // book / chapter / filter
  const [bookId, setBookId] = useState(null);
  const [chapterTitle, setChapterTitle] = useState(null);
  const [filterType, setFilterType] = useState('all');  // 'all' | type id

  // session
  const [queue, setQueue] = useState([]);
  const [idx, setIdx] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [combo, setCombo] = useState(0);
  const [sessionStats, setSessionStats] = useState({ correct: 0, wrong: 0, mastered: 0 });

  // swipe transient (렌더용 offset만 state)
  const [swipeOff, setSwipeOff] = useState(0);
  const [swipeOut, setSwipeOut] = useState(null); // 'left'|'right'|null
  const cardRef = useRef(null);

  // ── 데이터 로드 (과목 선택 시)
  useEffect(() => {
    if (!subject) return;
    let alive = true;
    setLoading(true);
    setLoadErr(null);
    setData(null); setAutoCards(null); setCurated([]);
    (async () => {
      try {
        const [r1, r2] = await Promise.all([
          fetch(`${subject.dataDir}/${subject.files.total}`),
          fetch(`${subject.dataDir}/${subject.files.cards}`),
        ]);
        if (!alive) return;
        if (!r1.ok || !r2.ok) throw new Error(`fetch ${r1.status}/${r2.status}`);
        const tot = await r1.json();
        const crd = await r2.json();
        if (!alive) return;
        setData(tot);
        setAutoCards(crd.cards || []);
      } catch (e) {
        if (alive) setLoadErr(e.message || String(e));
      } finally {
        if (alive) setLoading(false);
      }
      try {
        const r = await fetch(`${subject.dataDir}/${subject.files.curated}`);
        if (r.ok) {
          const j = await r.json();
          if (alive) setCurated((j.cards || []).map(c => ({ ...c, type: c.type || 'curated' })));
        }
      } catch { /* optional */ }
    })();
    return () => { alive = false; };
  }, [subject]);

  const allCards = useMemo(() => {
    const merged = (autoCards || []).concat(curated);
    return merged.filter(c => !hidden[c.id]);
  }, [autoCards, curated, hidden]);

  const hideCard = (cardId) => {
    const next = { ...hidden, [cardId]: true };
    setHidden(next);
    lsSave(HIDDEN_KEY, next);
  };
  const restoreAllHidden = () => {
    setHidden({});
    lsSave(HIDDEN_KEY, {});
  };

  // 과목 진척 (picker에 표시)
  const subjectProgress = useMemo(() => {
    const map = {};
    for (const c of allCards) {
      const sid = subjectId;
      if (!map[sid]) map[sid] = { total: 0, mastered: 0, due: 0 };
      map[sid].total++;
      const s = srs[c.id];
      if (s && s.box >= LADDER.length) map[sid].mastered++;
      else if (s && (s.due == null || s.due <= Date.now())) map[sid].due++;
    }
    return map;
  }, [allCards, subjectId, srs]);

  // 책별 진척
  const bookProgress = useMemo(() => {
    if (!data || !data.books) return [];
    const now = Date.now();
    return data.books.map(b => {
      const pool = allCards.filter(c => c.bookId === b.id);
      let learned = 0, mastered = 0, due = 0;
      const boxDist = Array.from({ length: LADDER.length + 1 }, () => 0); // 0..6
      let unseen = 0;
      for (const c of pool) {
        const s = srs[c.id];
        if (!s) { unseen++; continue; }
        if (s.box >= LADDER.length) { mastered++; boxDist[LADDER.length]++; }
        else {
          learned++;
          boxDist[Math.max(0, s.box)]++;
          if (s.due == null || s.due <= now) due++;
        }
      }
      return {
        id: b.id, title: b.title,
        total: pool.length, unseen, learned, mastered, due, boxDist,
        chapters: (b.tree?.children || []).map(ch => {
          const cPool = pool.filter(c => c.chapterTitle.includes(ch.title));
          let cMast = 0, cLearn = 0, cDue = 0;
          for (const c of cPool) {
            const s = srs[c.id];
            if (s && s.box >= LADDER.length) cMast++;
            else if (s) {
              cLearn++;
              if (s.due == null || s.due <= now) cDue++;
            }
          }
          return { id: ch.id, title: ch.title, total: cPool.length, learned: cLearn, mastered: cMast, due: cDue };
        }),
      };
    });
  }, [data, allCards, srs]);

  // 현재 풀
  const currentPool = useMemo(() => {
    if (!bookId) return [];
    let p = allCards.filter(c => c.bookId === bookId);
    // 인터리빙 ON이면 단원 잠금 해제 — 책 전체에서 셔플
    if (chapterTitle && !interleave) p = p.filter(c => c.chapterTitle.includes(chapterTitle));
    if (filterType === 'bookmark') p = p.filter(c => bookmarks[c.id]);
    else if (filterType !== 'all') p = p.filter(c => c.type === filterType);
    return p;
  }, [allCards, bookId, chapterTitle, filterType, bookmarks, interleave]);

  // ── 세션 시작
  const startSession = useCallback((overridePool = null) => {
    const pool = overridePool || currentPool;
    const q = buildQueue(pool, srs, sessionSize);
    if (!q.length) return;
    setQueue(q);
    setIdx(0);
    setRevealed(false);
    setCombo(0);
    setSwipeOff(0); setSwipeOut(null);
    setSessionStats({ correct: 0, wrong: 0, mastered: 0 });
    setView('session');
  }, [currentPool, srs, sessionSize]);

  // ── 답 처리 (모든 응답 모드 통합)
  // grade: 0=다시, 1=어려움, 2=좋음, 3=쉬움 (simple은 X→0 / O→2로 매핑)
  const commitGrade = useCallback((grade) => {
    const card = queue[idx];
    if (!card) return;
    const correct = grade >= 1;
    const prev = srs[card.id];
    const ns = (respMode === 'sm2' || respMode === 'type' || respMode === 'choice')
      ? nextSrsSm2(prev, grade)
      : nextSrs(prev, correct);
    const newlyMastered = ns.box >= LADDER.length && (!prev || prev.box < LADDER.length);
    const updated = { ...srs, [card.id]: ns };
    setSrs(updated);
    lsSave(SRS_KEY, updated);

    const today = todayKey();
    const d = { ...daily };
    const slot = d[today] || { correct: 0, wrong: 0, mastered: 0 };
    if (correct) slot.correct++; else slot.wrong++;
    if (newlyMastered) slot.mastered++;
    d[today] = slot;
    setDaily(d);
    lsSave(DAILY_KEY, d);

    // 노트 draft 자동 저장
    if (noteDraft.trim()) {
      const nx = { ...notes, [card.id]: noteDraft.trim() };
      setNotes(nx);
      lsSave(NOTES_KEY, nx);
    }

    if (haptic && typeof navigator !== 'undefined' && navigator.vibrate) {
      navigator.vibrate(correct ? 18 : [10, 30, 10]);
    }
    setSessionStats(s => ({
      correct: s.correct + (correct ? 1 : 0),
      wrong: s.wrong + (correct ? 0 : 1),
      mastered: s.mastered + (newlyMastered ? 1 : 0),
    }));
    setCombo(prev => correct ? prev + 1 : 0);
    setRevealed(false);
    setSwipeOff(0); setSwipeOut(null);
    setExpandSource(false);
    setTypedAnswer(''); setChoicePicked(null);
    setShowNote(false); setNoteDraft('');
    if (idx + 1 >= queue.length) setView('done');
    else setIdx(idx + 1);
  }, [queue, idx, srs, daily, haptic, respMode, notes, noteDraft]);

  // 스와이프 → 슬라이드 아웃 → 채점 (simple/sm2에서 좌(X=다시) 우(O=좋음))
  const handleSwipeJudge = (correct) => {
    setSwipeOut(correct ? 'right' : 'left');
    setTimeout(() => commitGrade(correct ? 2 : 0), 220);
  };

  // 카드 전환 시 노트 초기 로드
  useEffect(() => {
    const c = queue[idx];
    if (c && notes[c.id]) {
      setNoteDraft(notes[c.id]);
    } else {
      setNoteDraft('');
    }
  }, [idx, queue, notes]);

  // ── AI 해설 (BYOK)
  const [aiExplain, setAiExplain] = useState({}); // {cardId: text|null|'loading'|'error'}
  const requestAiExplain = useCallback(async (card) => {
    if (!byok || !card) return;
    setAiExplain(s => ({ ...s, [card.id]: 'loading' }));
    try {
      const res = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': byok,
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true',
        },
        body: JSON.stringify({
          model: 'claude-haiku-4-5-20251001',
          max_tokens: 400,
          messages: [{
            role: 'user',
            content: `감정평가사 1차 ${subject?.title || ''} 학습 카드입니다. 정답이 왜 이렇게 되는지 3~5문장으로 간결히 해설해 주세요. 출처는 김묘엽 「위패스 마이」.\n\n[문제]\n${card.q}\n\n[정답]\n${card.a}\n\n[단원]\n${card.chapterTitle}`,
          }],
        }),
      });
      if (!res.ok) throw new Error(`API ${res.status}`);
      const j = await res.json();
      const text = j?.content?.[0]?.text || '응답이 비어 있습니다.';
      setAiExplain(s => ({ ...s, [card.id]: text }));
    } catch (e) {
      setAiExplain(s => ({ ...s, [card.id]: `오류: ${e.message || e}` }));
    }
  }, [byok, subject]);

  // ── 스와이프 핸들러 (revealed일 때만)
  const onTouchStart = (e) => {
    if (!revealed) return;
    const t = e.touches[0];
    swipeState.active = true;
    swipeState.startX = t.clientX;
    swipeState.startY = t.clientY;
  };
  const onTouchMove = (e) => {
    if (!revealed || !swipeState.active) return;
    const t = e.touches[0];
    const dx = t.clientX - swipeState.startX;
    const dy = t.clientY - swipeState.startY;
    if (Math.abs(dy) > Math.abs(dx) * 1.5) return; // 수직 스크롤
    setSwipeOff(dx);
  };
  const onTouchEnd = () => {
    if (!swipeState.active) return;
    swipeState.active = false;
    const off = swipeOff;
    if (Math.abs(off) > 80) {
      handleSwipeJudge(off > 0);
    } else {
      setSwipeOff(0);
    }
  };

  // 키보드 — 모드별 다른 단축키
  useEffect(() => {
    if (view !== 'session') return;
    const onKey = (e) => {
      // 타이핑 모드에서 input 안에 있으면 인터셉트하지 않음 (Enter 제외)
      const tgt = e.target;
      const inInput = tgt && (tgt.tagName === 'INPUT' || tgt.tagName === 'TEXTAREA');
      if (inInput && e.key !== 'Escape') return;

      if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        if (!revealed) setRevealed(true);
      } else if (revealed) {
        if (respMode === 'simple') {
          if (e.key === 'o' || e.key === 'O') handleSwipeJudge(true);
          else if (e.key === 'x' || e.key === 'X') handleSwipeJudge(false);
        } else {
          // sm2/type/choice → 1~4
          const map = { '1': 0, '2': 1, '3': 2, '4': 3 };
          if (map[e.key] != null) commitGrade(map[e.key]);
        }
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [view, revealed, queue, idx, respMode]); // eslint-disable-line

  // ── 글자 배율 CSS 변수
  useEffect(() => { document.documentElement.style.setProperty('--mem-fs', fs); }, [fs]);

  // ── 테마: auto면 OS prefers-color-scheme 반응, 아니면 강제
  useEffect(() => {
    const apply = () => {
      let effective = theme;
      if (theme === 'auto') {
        effective = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      if (effective === 'dark') document.documentElement.setAttribute('data-mem-theme', 'dark');
      else document.documentElement.removeAttribute('data-mem-theme');
    };
    apply();
    if (theme === 'auto' && window.matchMedia) {
      const mq = window.matchMedia('(prefers-color-scheme: dark)');
      const onChange = () => apply();
      mq.addEventListener?.('change', onChange);
      return () => mq.removeEventListener?.('change', onChange);
    }
  }, [theme]);

  // ── 북마크 토글
  const toggleBookmark = (cardId) => {
    const next = { ...bookmarks };
    if (next[cardId]) delete next[cardId]; else next[cardId] = true;
    setBookmarks(next);
    lsSave(BOOKMARK_KEY, next);
  };

  // 일별 학습량 (sparkline용) — 지난 N일
  const sparkData = useMemo(() => {
    const arr = [];
    const d = new Date();
    for (let i = SPARKLINE_DAYS - 1; i >= 0; i--) {
      const day = new Date(d); day.setDate(d.getDate() - i);
      const k = dateKey(day);
      const slot = daily[k] || { correct: 0, wrong: 0, mastered: 0 };
      arr.push({ k, total: slot.correct + slot.wrong, correct: slot.correct, mastered: slot.mastered });
    }
    return arr;
  }, [daily]);

  const streakInfo = useMemo(() => computeStreak(daily, freeze), [daily, freeze]);
  const streak = streakInfo.streak;
  const bookmarkCount = useMemo(() => Object.keys(bookmarks).length, [bookmarks]);
  const hiddenCount = useMemo(() => Object.keys(hidden).length, [hidden]);
  const ddays = useMemo(() => daysToExam(examDate), [examDate]);
  const autoGoal = useMemo(() => {
    const total = (autoCards || []).length + curated.length;
    return computeDailyGoal(total, srs, examDate, dailyGoal);
  }, [autoCards, curated, srs, examDate, dailyGoal]);

  // freeze 토큰 1일 1회 자동 갱신
  useEffect(() => {
    const refreshed = refreshFreezeTokens(freeze);
    if (refreshed.lastCheck !== freeze?.lastCheck || refreshed.tokens !== freeze?.tokens) {
      setFreeze(refreshed);
      lsSave(FREEZE_KEY, refreshed);
    }
    // eslint-disable-next-line
  }, []);

  // 4지선다 옵션: 카드 id 기반 안정적 — 같은 카드에서 매 렌더 reshuffle 방지
  const choiceData = useMemo(() => {
    if (respMode !== 'choice') return null;
    const card = queue[idx];
    if (!card) return null;
    const sameSection = card.chapterTitle.split(' > ').slice(-2)[0];
    let others = allCards.filter(c =>
      c.id !== card.id && c.bookId === card.bookId && c.a && c.a.length > 4 &&
      c.chapterTitle.split(' > ').slice(-2)[0] === sameSection);
    if (others.length < 3) {
      others = allCards.filter(c =>
        c.id !== card.id && c.bookId === card.bookId && c.a && c.a.length > 4 && c.a !== card.a);
    }
    const distractors = shuffleArr(others).slice(0, 3);
    const opts = shuffleArr([card.a, ...distractors.map(d => d.a)]);
    return { opts, correctIdx: opts.indexOf(card.a) };
  }, [respMode, queue, idx, allCards]);

  // ── 헤더 빌더
  const memHeader = (title, backHandler) => (
    <header className="mem-header">
      {backHandler
        ? <button className="mem-icon-btn" onClick={backHandler} aria-label="뒤로">‹</button>
        : <div className="mem-icon-btn" />}
      <div className="mem-header-title">{title}</div>
      <button className="mem-icon-btn" onClick={() => setView('options')} aria-label="옵션">⚙</button>
    </header>
  );

  // ─── VIEW: subjects (과목 picker) ────────────────────────────
  if (view === 'subjects') {
    const relevant = browseExam ? EXAM_SUBJECT_RELEVANCE[browseExam] || [] : null;
    return (
      <div className="mem-root">
        {memHeader('통암기', isTabRoot ? null : onBack)}
        <main className="mem-main">
          <div className="mem-hero-min">
            <div className="mem-hero-eyebrow">
              {browseExam || '감정평가사'} 1차 · 교재 통째 외우기
            </div>
            <h1 className="mem-hero-h1">어떤 과목부터?</h1>
            {browseExam && (
              <div style={{ fontSize: '0.78rem', color: '#6b7280', marginTop: 6 }}>
                {browseExam} 모드 — 시험 출제 과목 강조 표시
              </div>
            )}
          </div>

          <div className="mem-subject-grid">
            {SUBJECTS.map(sub => {
              const enabled = !sub.comingSoon;
              const inMode = !relevant || relevant.includes(sub.id);
              return (
                <button
                  key={sub.id}
                  className={`mem-subject-card ${enabled ? '' : 'is-soon'}`}
                  disabled={!enabled}
                  onClick={() => { if (enabled) { setSubjectId(sub.id); setView('home'); } }}
                  style={{
                    '--c-primary': sub.color.primary,
                    '--c-light': sub.color.light,
                    '--c-dark': sub.color.dark,
                    '--c-accent': sub.color.accent,
                    opacity: inMode ? 1 : 0.45,
                  }}
                >
                  <div className="mem-subject-icon">{sub.icon}</div>
                  <div className="mem-subject-info">
                    <div className="mem-subject-title">
                      {sub.title}
                      {browseExam && !inMode && (
                        <span style={{ marginLeft: 6, fontSize: '0.7rem',
                          color: '#9ca3af', fontWeight: 500 }}>
                          (출제 없음)
                        </span>
                      )}
                    </div>
                    <div className="mem-subject-sub">{sub.subtitle}</div>
                  </div>
                  {enabled
                    ? <div className="mem-subject-arrow">→</div>
                    : <div className="mem-subject-soon">곧 출시</div>}
                </button>
              );
            })}
          </div>

          {!howtoSeen && (
            <div className="mem-section">
              <div className="mem-section-title">통암기란?</div>
              <ul className="mem-howto">
                <li><b>스페이스</b>·탭 → 정답 공개</li>
                <li>좌/우 스와이프, <b>O</b>·<b>X</b> 키, 버튼 → 자가 채점</li>
                <li>맞히면 <b>1·3·7·16·35·70일</b> 간격으로 재출제 (Leitner 6박스)</li>
                <li>6번 연속 정답 = <b>마스터</b>, 더 이상 안 나옴</li>
              </ul>
              <button className="mem-text-btn"
                onClick={() => { setHowtoSeen(true); lsSave(HOWTO_KEY, '1'); }}>
                알겠어요 — 이 안내 숨기기
              </button>
            </div>
          )}
        </main>
      </div>
    );
  }

  if (loadErr) {
    return (
      <div className="mem-root">
        {memHeader(subject?.title || '통암기', () => setView('subjects'))}
        <div style={{ padding: 24, color: 'var(--danger)' }}>데이터 로드 실패: {loadErr}</div>
      </div>
    );
  }
  if (loading || !data || !autoCards) {
    return (
      <div className="mem-root">
        {memHeader(subject?.title || '통암기', () => setView('subjects'))}
        <div style={{ padding: 24, color: 'var(--text-sub)' }}>불러오는 중…</div>
      </div>
    );
  }

  // ─── VIEW: home (책 선택) ─────────────────────────────────────
  if (view === 'home') {
    const sp = subjectProgress[subjectId] || { total: 0, mastered: 0, due: 0 };
    const pct = sp.total ? Math.round((sp.mastered / sp.total) * 100) : 0;
    return (
      <div className="mem-root" style={{ '--c-primary': subject.color.primary, '--c-light': subject.color.light, '--c-dark': subject.color.dark, '--c-accent': subject.color.accent }}>
        {memHeader(subject.title, () => setView('subjects'))}
        <main className="mem-main">
          <div className="mem-summary">
            <div className="mem-summary-row">
              <span className="mem-summary-icon">{subject.icon}</span>
              <span className="mem-summary-meta">
                전체 <b>{sp.total.toLocaleString()}</b>장
                {sp.mastered > 0 && <> · 마스터 <b style={{ color: '#16a34a' }}>{sp.mastered}</b></>}
                {sp.due > 0 && <> · <span style={{ color: '#b45309', fontWeight: 700 }}>오늘 복습 {sp.due}</span></>}
              </span>
            </div>
            <div className="mem-summary-bar">
              <div className="mem-summary-bar-fill" style={{ width: `${pct}%` }} />
            </div>
            <div className="mem-summary-pct">마스터 {pct}%</div>
          </div>

          {/* D-DAY + 일일 권장 (시험일 설정된 경우) */}
          {ddays != null && ddays >= 0 && (
            <div className="mem-dday-card">
              <div className="mem-dday-num">D-{ddays}</div>
              <div className="mem-dday-body">
                <div className="mem-dday-label">시험까지</div>
                <div className="mem-dday-goal">오늘 권장 <b>{autoGoal}</b>장</div>
              </div>
              <button className="mem-dday-edit" onClick={() => setView('options')}>설정</button>
            </div>
          )}

          {/* 스트릭 + 주간 히트맵 */}
          <div className="mem-streak-card">
            <div className="mem-streak-icon">{streak > 0 ? '🔥' : '🌱'}</div>
            <div className="mem-streak-body">
              <div className="mem-streak-num">{streak}<span>일</span></div>
              <div className="mem-streak-label">
                {streak > 0 ? '연속 학습 중' : '오늘 시작!'}
                {streakInfo.freezeUsedToday && <span className="mem-freeze-tag" title="결석한 어제를 freeze 토큰으로 메웠어요">❄️ freeze</span>}
              </div>
              {freeze?.tokens > 0 && (
                <div className="mem-freeze-stock">❄️ {freeze.tokens}장 보유</div>
              )}
            </div>
            <Sparkline data={sparkData} />
          </div>

          {/* 주간 히트맵 (28일) */}
          <WeekHeatmap daily={daily} />


          {/* 북마크 빠른 진입 */}
          {bookmarkCount > 0 && (
            <button className="mem-bookmark-row"
              onClick={() => {
                const ids = Object.keys(bookmarks);
                const pool = allCards.filter(c => ids.includes(c.id));
                if (pool.length) startSession(pool);
              }}>
              <span className="mem-bookmark-ico">⭐</span>
              <span className="mem-bookmark-text">북마크 <b>{bookmarkCount}</b>장 풀기</span>
              <span className="mem-bookmark-arrow">→</span>
            </button>
          )}

          <div className="mem-section-title">교재 선택</div>
          <div className="mem-book-grid">
            {bookProgress.map(b => {
              const bpct = b.total ? Math.round((b.mastered / b.total) * 100) : 0;
              return (
                <button key={b.id} className="mem-book-card"
                  onClick={() => { setBookId(b.id); setChapterTitle(null); setFilterType('all'); setView('browse'); }}>
                  <div className="mem-book-title">{b.title}</div>
                  <div className="mem-book-meta">
                    {b.total}장
                    <span className="mem-divider">·</span>
                    {b.learned > 0 && <>학습중 {b.learned}</>}
                    {b.mastered > 0 && <span className="mem-pill mem-pill-mast">⭐ {b.mastered}</span>}
                    {b.due > 0 && <span className="mem-pill mem-pill-due">오늘 {b.due}</span>}
                  </div>
                  <BoxDistChart dist={b.boxDist} unseen={b.unseen} primary={subject.color.primary} />
                  <div className="mem-book-pct">마스터 {bpct}%</div>
                </button>
              );
            })}
          </div>
        </main>
      </div>
    );
  }

  // ─── VIEW: browse (단원 선택) ─────────────────────────────────
  if (view === 'browse') {
    const book = bookProgress.find(b => b.id === bookId);
    if (!book) return null;
    const filterChips = ['all', 'bookmark', 'statute', 'definition', 'mnemonic', 'curated'];
    return (
      <div className="mem-root" style={{ '--c-primary': subject.color.primary, '--c-light': subject.color.light, '--c-dark': subject.color.dark, '--c-accent': subject.color.accent }}>
        {memHeader(book.title, () => setView('home'))}
        <main className="mem-main">
          <div className="mem-quick">
            <button className="mem-btn-primary"
              disabled={book.total === 0}
              onClick={() => { setChapterTitle(null); setTimeout(() => startSession(), 0); }}>
              <span>📚 전 단원 통째로</span>
              <span className="mem-btn-sub">{sessionSize}장 셔플</span>
            </button>
            {book.due > 0 && (
              <button className="mem-btn-secondary"
                onClick={() => {
                  setChapterTitle(null);
                  const now = Date.now();
                  const duePool = allCards.filter(c => c.bookId === book.id).filter(c => {
                    const s = srs[c.id]; return s && s.due != null && s.due <= now && s.box < LADDER.length;
                  });
                  if (duePool.length) startSession(duePool);
                }}>
                <span>🔁 오늘 복습</span>
                <span className="mem-btn-sub">{book.due}장 도래</span>
              </button>
            )}
          </div>

          <div className="mem-section-title">카드 유형</div>
          <div className="mem-chips">
            {filterChips.map(t => {
              const label = t === 'all' ? '전체'
                : t === 'bookmark' ? `⭐ 북마크${bookmarkCount > 0 ? ` ${bookmarkCount}` : ''}`
                : (TYPE_META[t]?.label || t);
              const disabled = t === 'bookmark' && bookmarkCount === 0;
              return (
                <button key={t}
                  className={`mem-chip ${filterType === t ? 'is-active' : ''}`}
                  disabled={disabled}
                  onClick={() => setFilterType(t)}>
                  {label}
                </button>
              );
            })}
          </div>

          <div className="mem-section-title" style={{ marginTop: 28 }}>단원별</div>
          <div className="mem-ch-list">
            {book.chapters.map(ch => {
              const pct = ch.total ? Math.round((ch.mastered / ch.total) * 100) : 0;
              const tone = pct >= 80 ? 'mast' : pct >= 40 ? 'mid' : ch.learned > 0 ? 'low' : 'fresh';
              return (
                <button key={ch.id} className={`mem-ch-row tone-${tone}`}
                  disabled={ch.total === 0}
                  onClick={() => { setChapterTitle(ch.title); setTimeout(() => startSession(), 0); }}>
                  <div className="mem-ch-name">{ch.title}</div>
                  <div className="mem-ch-meta">
                    {ch.total}장
                    {ch.due > 0 && <span className="mem-pill mem-pill-due">{ch.due}</span>}
                    {ch.mastered > 0 && <span className="mem-pill mem-pill-mast">⭐ {ch.mastered}</span>}
                  </div>
                  <div className="mem-ch-bar"><div className="mem-ch-bar-fill" style={{ width: `${pct}%` }} /></div>
                </button>
              );
            })}
          </div>
        </main>
      </div>
    );
  }

  // ─── VIEW: session (카드 큐) ──────────────────────────────────
  if (view === 'session') {
    const card = queue[idx];
    if (!card) {
      return (
        <div className="mem-root">
          {memHeader('통암기', () => setView('browse'))}
          <div style={{ padding: 24 }}>카드가 없습니다.</div>
        </div>
      );
    }
    const meta = TYPE_META[card.type] || { label: card.type, color: '#6b7280', bg: '#f3f4f6' };
    const sCur = srs[card.id];
    const curBox = sCur ? sCur.box : -1;
    const nextBoxIfO = curBox < 0 ? 0 : Math.min(LADDER.length, curBox + 1);
    const dueInDays = nextBoxIfO < LADDER.length ? LADDER[nextBoxIfO] : null;
    const sessionAcc = sessionStats.correct + sessionStats.wrong > 0
      ? Math.round((sessionStats.correct / (sessionStats.correct + sessionStats.wrong)) * 100) : 0;

    const choiceOpts = choiceData?.opts || null;
    const correctChoiceIdx = choiceData?.correctIdx ?? -1;

    let transform;
    if (swipeOut === 'right') transform = 'translateX(120%) rotate(8deg)';
    else if (swipeOut === 'left') transform = 'translateX(-120%) rotate(-8deg)';
    else transform = `translateX(${swipeOff}px) rotate(${swipeOff / 50}deg)`;

    return (
      <div className="mem-root" style={{ '--c-primary': subject.color.primary, '--c-light': subject.color.light, '--c-dark': subject.color.dark, '--c-accent': subject.color.accent }}>
        <header className="mem-header">
          <button className="mem-icon-btn" onClick={() => {
            if (sessionStats.correct + sessionStats.wrong > 0 && !window.confirm('세션 종료할까요? 진행은 저장됐어요.')) return;
            setView('browse');
          }} aria-label="뒤로">‹</button>
          <div className="mem-header-title">
            <span>{idx + 1} / {queue.length}</span>
            {combo >= 3 && <span className="mem-streak">🔥 {combo}</span>}
          </div>
          <div className="mem-icon-btn" />
        </header>
        <div className="mem-progress-bar">
          <div className="mem-progress-fill" style={{ width: `${((idx) / queue.length) * 100}%` }} />
        </div>

        <main className="mem-main mem-session">
          <div className="mem-card-meta">
            <span className="mem-type-tag" style={{ color: meta.color, background: meta.bg }}>{meta.label}</span>
            <BoxDots box={curBox} />
            <div className="mem-card-actions">
              <button className={`mem-card-action ${bookmarks[card.id] ? 'is-active' : ''}`}
                onClick={(e) => { e.stopPropagation(); toggleBookmark(card.id); }}
                aria-label="북마크">
                {bookmarks[card.id] ? '★' : '☆'}
              </button>
              <button className={`mem-card-action ${expandSource ? 'is-active' : ''}`}
                onClick={(e) => { e.stopPropagation(); setExpandSource(v => !v); }}
                aria-label="출처 본문 보기">
                📖
              </button>
              <button className="mem-card-action"
                onClick={(e) => {
                  e.stopPropagation();
                  if (window.confirm('이 카드를 숨길까요? (이상한 카드 신고용 — 옵션에서 복원 가능)')) {
                    hideCard(card.id);
                    // 즉시 다음 카드로
                    if (idx + 1 >= queue.length) setView('done');
                    else setIdx(idx + 1);
                  }
                }}
                aria-label="카드 신고/숨김">
                ⚠
              </button>
            </div>
            <span className="mem-card-path">{card.chapterTitle}</span>
          </div>

          <div
            ref={cardRef}
            className={`mem-card ${revealed ? 'is-revealed' : ''}`}
            style={{ transform, transition: swipeState.active ? 'none' : 'transform 0.2s ease' }}
            onTouchStart={respMode === 'simple' || respMode === 'sm2' ? onTouchStart : undefined}
            onTouchMove={respMode === 'simple' || respMode === 'sm2' ? onTouchMove : undefined}
            onTouchEnd={respMode === 'simple' || respMode === 'sm2' ? onTouchEnd : undefined}
            onClick={(e) => {
              // 입력 모드에선 카드 탭으로 reveal 막기 (input 사용 유도)
              if (revealed) return;
              if (respMode === 'type' || respMode === 'choice') return;
              setRevealed(true);
            }}
          >
            <div className="mem-q"><CardText text={card.q} /></div>

            {/* 타이핑 모드 입력 영역 */}
            {!revealed && respMode === 'type' && (
              <div className="mem-type-area">
                <input
                  className="mem-type-input"
                  type="text"
                  value={typedAnswer}
                  onChange={(e) => setTypedAnswer(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); setRevealed(true); } }}
                  placeholder="답을 직접 입력하세요 — Enter로 확인"
                  autoFocus
                />
                <button className="mem-type-confirm" onClick={() => setRevealed(true)}>
                  확인
                </button>
              </div>
            )}

            {/* 4지선다 옵션 */}
            {!revealed && respMode === 'choice' && choiceOpts && (
              <div className="mem-choice-list">
                {choiceOpts.map((opt, i) => (
                  <button key={i}
                    className={`mem-choice-opt ${choicePicked === i ? 'is-picked' : ''}`}
                    onClick={(e) => { e.stopPropagation(); setChoicePicked(i); setRevealed(true); }}>
                    <span className="mem-choice-label">{String.fromCharCode(65 + i)}</span>
                    <span className="mem-choice-text"><CardText text={opt} /></span>
                  </button>
                ))}
              </div>
            )}

            <div className={`mem-reveal-zone ${revealed ? '' : 'is-hidden'}`}>
              <div className="mem-divider-line" />

              {/* 타이핑 결과: 내가 적은 것 vs 정답 */}
              {respMode === 'type' && typedAnswer && (
                <div className="mem-type-result">
                  <div className="mem-type-yours"><span>내가 적은 답</span><b>{typedAnswer}</b></div>
                </div>
              )}

              {/* 4지선다 결과 */}
              {respMode === 'choice' && choicePicked != null && (
                <div className={`mem-choice-result ${choicePicked === correctChoiceIdx ? 'ok' : 'no'}`}>
                  {choicePicked === correctChoiceIdx
                    ? <span>✓ 정답! ({String.fromCharCode(65 + correctChoiceIdx)})</span>
                    : <span>✗ 정답은 <b>{String.fromCharCode(65 + correctChoiceIdx)}</b></span>}
                </div>
              )}

              <div className="mem-a"><CardText text={card.a} /></div>
              {card.note && <div className="mem-note">💡 {card.note}</div>}

              {/* AI 해설 (BYOK) */}
              {byok && (
                <div className="mem-ai-area">
                  {!aiExplain[card.id] && (
                    <button className="mem-ai-btn" onClick={(e) => { e.stopPropagation(); requestAiExplain(card); }}>
                      ✨ AI 해설 요청
                    </button>
                  )}
                  {aiExplain[card.id] === 'loading' && (
                    <div className="mem-ai-loading">AI 응답 생성 중…</div>
                  )}
                  {typeof aiExplain[card.id] === 'string' && aiExplain[card.id] !== 'loading' && (
                    <div className={`mem-ai-result ${aiExplain[card.id].startsWith('오류') ? 'is-error' : ''}`}>
                      <div className="mem-ai-head">✨ AI 해설</div>
                      <div className="mem-ai-body">{aiExplain[card.id]}</div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {!revealed && respMode !== 'type' && respMode !== 'choice' && (
              <div className="mem-card-hint">
                <span>탭 또는 <kbd>Space</kbd> → 정답</span>
              </div>
            )}

            {/* 스와이프 인디케이터 (drag 중) */}
            {Math.abs(swipeOff) > 30 && (
              <div className={`mem-swipe-ind ${swipeOff > 0 ? 'right' : 'left'}`}>
                {swipeOff > 0 ? '✓ 맞춤' : '✗ 틀림'}
              </div>
            )}
          </div>

          {/* 출처 본문 패널 */}
          {expandSource && (
            <SourcePanel
              card={card}
              data={data}
              onClose={() => setExpandSource(false)}
            />
          )}

          {revealed && (
            <>
              {respMode === 'simple' ? (
                <div className="mem-judge">
                  <button className="mem-judge-x" onClick={() => handleSwipeJudge(false)}>
                    <span className="mem-judge-emoji">✗</span>
                    <span className="mem-judge-label">틀림</span>
                    <span className="mem-judge-hint">내일 다시</span>
                  </button>
                  <button className="mem-judge-o" onClick={() => handleSwipeJudge(true)}>
                    <span className="mem-judge-emoji">✓</span>
                    <span className="mem-judge-label">맞춤</span>
                    <span className="mem-judge-hint">
                      {dueInDays ? `+${dueInDays}일 후` : '⭐ 마스터'}
                    </span>
                  </button>
                </div>
              ) : (
                <div className="mem-grade">
                  {GRADE_LABELS.map((label, g) => {
                    const d = previewDays(sCur, g);
                    return (
                      <button key={g}
                        className={`mem-grade-btn grade-${g}`}
                        style={{ '--g-color': GRADE_COLORS[g] }}
                        onClick={() => commitGrade(g)}>
                        <span className="mem-grade-label">{label}</span>
                        <span className="mem-grade-hint">
                          {d == null ? '⭐' : `+${d}일`}
                        </span>
                      </button>
                    );
                  })}
                </div>
              )}

              {/* 자기 설명 노트 */}
              <div className="mem-note-area">
                {!showNote ? (
                  <button className="mem-note-toggle" onClick={() => setShowNote(true)}>
                    📝 자기 설명 메모 {notes[card.id] ? '(저장됨 — 수정)' : '추가'}
                  </button>
                ) : (
                  <>
                    <textarea
                      className="mem-note-input"
                      value={noteDraft}
                      onChange={(e) => setNoteDraft(e.target.value)}
                      placeholder="왜 그런지 한 줄로 적어보세요 — 다음 카드에서 자동 저장"
                      rows={2}
                      autoFocus
                    />
                    <div className="mem-note-actions">
                      <button className="mem-text-btn" onClick={() => { setShowNote(false); }}>접기</button>
                      {notes[card.id] && (
                        <button className="mem-text-btn"
                          onClick={() => { const n = { ...notes }; delete n[card.id]; setNotes(n); lsSave(NOTES_KEY, n); setNoteDraft(''); }}>
                          삭제
                        </button>
                      )}
                    </div>
                  </>
                )}
              </div>

              <div className="mem-kbd-hint">
                {respMode === 'simple'
                  ? <><kbd>O</kbd> 맞춤 · <kbd>X</kbd> 틀림 · 좌/우 스와이프</>
                  : <><kbd>1</kbd> 다시 · <kbd>2</kbd> 어려움 · <kbd>3</kbd> 좋음 · <kbd>4</kbd> 쉬움</>}
              </div>
            </>
          )}

          <div className="mem-session-stats">
            세션 {idx + 1}/{queue.length} · 맞춤 {sessionStats.correct} · 틀림 {sessionStats.wrong}
            {sessionStats.correct + sessionStats.wrong > 0 && <> · {sessionAcc}%</>}
          </div>
        </main>
      </div>
    );
  }

  // ─── VIEW: done (세션 완료 미니 리포트) ────────────────────────
  if (view === 'done') {
    const total = sessionStats.correct + sessionStats.wrong;
    const acc = total > 0 ? Math.round((sessionStats.correct / total) * 100) : 0;
    const tier = acc >= 90 ? { emoji: '🏆', t: '완벽!' } : acc >= 70 ? { emoji: '🎯', t: '잘했어요' } : acc >= 50 ? { emoji: '💪', t: '계속 가요' } : { emoji: '🌱', t: '한 번 더!' };
    return (
      <div className="mem-root" style={{ '--c-primary': subject.color.primary, '--c-light': subject.color.light, '--c-dark': subject.color.dark, '--c-accent': subject.color.accent }}>
        {memHeader('세션 완료', () => setView('browse'))}
        <main className="mem-main mem-done">
          <div className="mem-done-emoji">{tier.emoji}</div>
          <div className="mem-done-title">{tier.t}</div>
          <div className="mem-done-sub">{queue.length}장 끝!</div>

          <div className="mem-report">
            <div className="mem-report-row">
              <div className="mem-report-cell"><span>맞춤</span><b style={{ color: '#16a34a' }}>{sessionStats.correct}</b></div>
              <div className="mem-report-cell"><span>틀림</span><b style={{ color: '#dc2626' }}>{sessionStats.wrong}</b></div>
              <div className="mem-report-cell"><span>정답률</span><b>{acc}%</b></div>
            </div>
            {sessionStats.mastered > 0 && (
              <div className="mem-report-mast">⭐ <b>{sessionStats.mastered}</b>장 마스터 도달!</div>
            )}
          </div>

          <div className="mem-quick">
            <button className="mem-btn-primary" onClick={() => startSession()}>한 세션 더</button>
            <button className="mem-btn-secondary" onClick={() => setView('browse')}>단원 선택</button>
          </div>
        </main>
      </div>
    );
  }

  // ─── VIEW: options ───────────────────────────────────────────
  if (view === 'options') {
    return (
      <div className="mem-root" style={subject ? { '--c-primary': subject.color.primary, '--c-light': subject.color.light, '--c-dark': subject.color.dark, '--c-accent': subject.color.accent } : undefined}>
        {memHeader('통암기 옵션', () => setView(subjectId ? 'home' : 'subjects'))}
        <main className="mem-main">
          <div className="mem-opt-section">
            <div className="mem-opt-label">응답 모드 <span className="mem-opt-hint">— 학습 깊이 조절</span></div>
            <div className="mem-opt-row">
              {[
                ['simple', '간단 (O/X)', '가장 빠름 · 기본'],
                ['sm2', '4등급', '카드별 간격 자동 조정 (SM-2)'],
                ['type', '직접 적기', '능동 회상 — 효과 강력'],
                ['choice', '4지선다', '시험 시뮬레이션'],
              ].map(([v, l, d]) => (
                <button key={v}
                  className={`mem-chip mem-mode-chip ${respMode === v ? 'is-active' : ''}`}
                  onClick={() => { setRespMode(v); lsSave(MODE_KEY, v); }}
                  title={d}>
                  {l}
                </button>
              ))}
            </div>
            <div className="mem-opt-desc">
              {respMode === 'simple' && '맞췄으면 O, 틀렸으면 X. 가장 빠른 흐름.'}
              {respMode === 'sm2' && '다시/어려움/좋음/쉬움 4단계로 카드별 망각 곡선을 정밀하게 학습.'}
              {respMode === 'type' && '답을 직접 입력 → 정답 확인 → 자가 채점. 능동 회상이 강력합니다.'}
              {respMode === 'choice' && '같은 절 다른 카드 답에서 오답 3개를 자동 추출 → 시험장 변별력 훈련.'}
            </div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">인터리빙</div>
            <div className="mem-opt-row">
              <button className={`mem-chip ${!interleave ? 'is-active' : ''}`}
                onClick={() => { setInterleave(false); lsSave(INTERLEAVE_KEY, '0'); }}>단원 잠금</button>
              <button className={`mem-chip ${interleave ? 'is-active' : ''}`}
                onClick={() => { setInterleave(true); lsSave(INTERLEAVE_KEY, '1'); }}>전체 셔플</button>
            </div>
            <div className="mem-opt-desc">
              전체 셔플은 한 단원 안에서만 풀지 않고 책 전체 카드를 섞어 출제 — 변별력 강화 (Bjork 인터리빙 효과).
            </div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">시험일 (D-DAY) <span className="mem-opt-hint">— 일일 권장량 자동 계산</span></div>
            <div className="mem-opt-row" style={{ alignItems: 'center', gap: 10 }}>
              <input
                type="date"
                className="mem-date-input"
                value={examDate}
                onChange={(e) => { setExamDate(e.target.value); lsSave(EXAM_DATE_KEY, e.target.value); }}
              />
              {examDate && (
                <button className="mem-text-btn"
                  onClick={() => { setExamDate(''); lsSave(EXAM_DATE_KEY, ''); }}>해제</button>
              )}
              {ddays != null && <span className="mem-opt-desc" style={{ background: 'transparent', padding: 0, color: 'var(--c-primary)', fontWeight: 700 }}>
                D-{ddays} · 권장 {autoGoal}장/일
              </span>}
            </div>
            <div className="mem-opt-desc">시험일 입력 시 잔여 카드 ÷ 남은 일수로 매일 권장량 자동 계산. (시험 1주 전부터는 복습 위주로 가정)</div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">일일 목표 수동 설정 <span className="mem-opt-hint">— 자동 계산 무시</span></div>
            <div className="mem-opt-row">
              <button className={`mem-chip ${dailyGoal == null ? 'is-active' : ''}`}
                onClick={() => { setDailyGoal(null); lsSave(DAILY_GOAL_KEY, ''); }}>자동</button>
              {[10, 20, 30, 50, 100].map(n => (
                <button key={n} className={`mem-chip ${dailyGoal === n ? 'is-active' : ''}`}
                  onClick={() => { setDailyGoal(n); lsSave(DAILY_GOAL_KEY, n); }}>
                  {n}
                </button>
              ))}
            </div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">한 세션 카드 수</div>
            <div className="mem-opt-row">
              {[10, 20, 30, 50].map(n => (
                <button key={n}
                  className={`mem-chip ${sessionSize === n ? 'is-active' : ''}`}
                  onClick={() => { setSessionSize(n); lsSave(SIZE_KEY, n); }}>
                  {n}장
                </button>
              ))}
            </div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">글자 크기</div>
            <div className="mem-opt-row">
              {[[0.9, '작게'], [1, '보통'], [1.15, '크게'], [1.3, '매우 크게']].map(([v, l]) => (
                <button key={v}
                  className={`mem-chip ${fs === v ? 'is-active' : ''}`}
                  onClick={() => { setFs(v); lsSave(FS_KEY, v); }}>
                  {l}
                </button>
              ))}
            </div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">테마</div>
            <div className="mem-opt-row">
              {[['auto', '시스템'], ['light', '라이트'], ['dark', '다크']].map(([v, l]) => (
                <button key={v}
                  className={`mem-chip ${theme === v ? 'is-active' : ''}`}
                  onClick={() => { setTheme(v); lsSave(THEME_KEY, v); }}>
                  {l}
                </button>
              ))}
            </div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">햅틱 (모바일 진동)</div>
            <div className="mem-opt-row">
              <button className={`mem-chip ${haptic ? 'is-active' : ''}`}
                onClick={() => { setHaptic(true); lsSave(HAPTIC_KEY, '1'); }}>켜기</button>
              <button className={`mem-chip ${!haptic ? 'is-active' : ''}`}
                onClick={() => { setHaptic(false); lsSave(HAPTIC_KEY, '0'); }}>끄기</button>
            </div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">북마크 ({bookmarkCount}장)</div>
            <button className="mem-chip"
              disabled={bookmarkCount === 0}
              onClick={() => {
                if (window.confirm(`북마크 ${bookmarkCount}장을 모두 해제할까요?`)) {
                  setBookmarks({}); lsSave(BOOKMARK_KEY, {});
                }
              }}>
              모두 해제
            </button>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">숨김 카드 ({hiddenCount}장) <span className="mem-opt-hint">— ⚠로 신고한 카드</span></div>
            <button className="mem-chip"
              disabled={hiddenCount === 0}
              onClick={() => {
                if (window.confirm(`숨김 ${hiddenCount}장을 모두 복원할까요?`)) restoreAllHidden();
              }}>
              모두 복원
            </button>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">AI 해설 (BYOK) <span className="mem-opt-hint">— Anthropic API 키 직접 입력</span></div>
            <input type="password"
              className="mem-date-input"
              style={{ width: '100%', maxWidth: 360 }}
              placeholder="sk-ant-..."
              value={byok}
              onChange={(e) => { setByok(e.target.value); lsSave(BYOK_KEY, e.target.value); }}
            />
            <div className="mem-opt-desc">
              사용자의 API 키로 직접 Anthropic Claude 호출. 키는 브라우저에만 저장 (서버 송신 X). 카드의 ✨ 아이콘으로 해설 요청.
              {byok && <> · 현재 키 입력됨</>}
            </div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">스트릭 보호 토큰</div>
            <div className="mem-opt-desc">
              현재 ❄️ <b>{freeze?.tokens || 0}</b>장 보유 · 7일마다 1장 회복(최대 2장). 결석한 어제를 자동으로 메워 연속 학습일 유지.
            </div>
          </div>
          <div className="mem-opt-section">
            <div className="mem-opt-label">가이드</div>
            <button className="mem-chip" onClick={() => { setHowtoSeen(false); lsSave(HOWTO_KEY, ''); }}>
              사용법 다시 보기
            </button>
          </div>
        </main>
      </div>
    );
  }

  return null;
}

// ─── 작은 부품 ───────────────────────────────────────────────

// 박스 분포 가로 막대 (책 카드용)
function BoxDistChart({ dist, unseen, primary }) {
  // dist[0..6], 6 = mastered
  const total = unseen + dist.reduce((a, b) => a + b, 0);
  if (total === 0) return null;
  const seg = (n, color) => n > 0 && (
    <div className="mem-bdc-seg" style={{ width: `${(n / total) * 100}%`, background: color }} />
  );
  // 색: unseen=회색, box 0~5=primary alpha 그라데, mastered=초록
  const stops = ['rgba(0,0,0,0.10)', '#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa', '#3b82f6'];
  return (
    <div className="mem-bdc" title={`미학습 ${unseen} / 박스별 ${dist.slice(0, 6).join('·')} / 마스터 ${dist[6]}`}>
      {seg(unseen, '#e5e7eb')}
      {dist.slice(0, 6).map((n, i) => (
        <div key={i} className="mem-bdc-seg"
          style={{ width: `${(n / total) * 100}%`, background: stops[i] || primary }} />
      ))}
      {seg(dist[6] || 0, '#16a34a')}
    </div>
  );
}

// 카드 상단 박스 도트 (현재 박스 진행 시각화)
function BoxDots({ box }) {
  const dots = [];
  for (let i = 0; i < 6; i++) {
    dots.push(<span key={i} className={`mem-dot ${i <= box ? 'on' : ''}`} />);
  }
  if (box >= 6) {
    return <span className="mem-box-graduated">⭐ 졸업</span>;
  }
  return <span className="mem-dots">{dots}</span>;
}

// 본문 라이트 마크다운 (**bold**, ___, 줄바꿈)
function CardText({ text }) {
  if (!text) return null;
  const parts = text.split(/(\n)/);
  return (
    <>
      {parts.map((p, i) => p === '\n' ? <br key={i} /> : <span key={i}>{renderInline(p)}</span>)}
    </>
  );
}
// 4주(28일) 학습 히트맵 — GitHub contribution 스타일
function WeekHeatmap({ daily }) {
  // 오늘 포함 28일을 4주 × 7일 그리드 (가로축 = 요일)
  const today = new Date();
  const cells = [];
  const max = Math.max(1, ...Object.values(daily || {}).map(s => (s.correct || 0) + (s.wrong || 0)));
  for (let w = 3; w >= 0; w--) {
    for (let dow = 0; dow < 7; dow++) {
      const d = new Date(today);
      d.setDate(today.getDate() - (w * 7 + (6 - dow)));
      const k = dateKey(d);
      const slot = (daily || {})[k] || { correct: 0, wrong: 0 };
      const total = (slot.correct || 0) + (slot.wrong || 0);
      const level = total === 0 ? 0
        : total < max * 0.25 ? 1
        : total < max * 0.5 ? 2
        : total < max * 0.75 ? 3 : 4;
      const isToday = k === dateKey(today);
      cells.push({ k, total, level, isToday, dow });
    }
  }
  const dowLabels = ['일', '월', '화', '수', '목', '금', '토'];
  return (
    <div className="mem-heatmap">
      <div className="mem-heatmap-title">최근 4주 학습</div>
      <div className="mem-heatmap-grid">
        {dowLabels.map((l, i) => <div key={`h-${i}`} className="mem-heatmap-dow">{l}</div>)}
        {cells.map((c, i) => (
          <div key={c.k}
            className={`mem-heatmap-cell level-${c.level} ${c.isToday ? 'is-today' : ''}`}
            title={`${c.k}: ${c.total}장`} />
        ))}
      </div>
      <div className="mem-heatmap-legend">
        적음 <span className="mem-heatmap-cell level-0" />
        <span className="mem-heatmap-cell level-1" />
        <span className="mem-heatmap-cell level-2" />
        <span className="mem-heatmap-cell level-3" />
        <span className="mem-heatmap-cell level-4" /> 많음
      </div>
    </div>
  );
}

// 30일 학습량 sparkline
function Sparkline({ data }) {
  if (!data || !data.length) return null;
  const max = Math.max(1, ...data.map(d => d.total));
  return (
    <div className="mem-spark" title="지난 30일 학습량">
      {data.map((d, i) => {
        const h = d.total === 0 ? 6 : 6 + Math.round((d.total / max) * 30);
        const isToday = i === data.length - 1;
        const cls = d.total === 0 ? 'is-zero' : isToday ? 'is-today' : '';
        return (
          <div key={d.k} className={`mem-spark-bar ${cls}`}
            style={{ height: `${h}px` }}
            title={`${d.k}: ${d.total}장${d.mastered ? ` · ⭐${d.mastered}` : ''}`} />
        );
      })}
    </div>
  );
}

// 카드 출처 본문 패널 — civil_total 트리에서 leafId로 노드 찾고 본문 단락 표시
function SourcePanel({ card, data, onClose }) {
  const node = useMemo(() => {
    if (!card?.leafId || !data?.books) return null;
    for (const b of data.books) {
      const f = findNodeById(b.tree, card.leafId);
      if (f) return f;
    }
    return null;
  }, [card, data]);

  if (!node) {
    return (
      <div className="mem-source">
        <div className="mem-source-head">
          <span>📖 출처 본문</span>
          <button className="mem-icon-btn" onClick={onClose} aria-label="닫기">×</button>
        </div>
        <div className="mem-source-empty">본문을 찾을 수 없습니다. (leafId: {card.leafId})</div>
      </div>
    );
  }
  const paras = node.paragraphs || [];
  return (
    <div className="mem-source">
      <div className="mem-source-head">
        <span>📖 {node.title}</span>
        <button className="mem-icon-btn" onClick={onClose} aria-label="닫기">×</button>
      </div>
      {paras.length === 0 && <div className="mem-source-empty">이 항목엔 본문이 없습니다.</div>}
      <div className="mem-source-body">
        {paras.map((p, i) => (
          <div key={i} className={`mem-source-p ${p.kind === 'quote' ? 'is-quote' : ''}`}>
            <CardText text={p.text} />
          </div>
        ))}
      </div>
      <div className="mem-source-hint">교재 OCR 본문 그대로 — 일부 줄바꿈 오류가 있을 수 있어요.</div>
    </div>
  );
}

function renderInline(s) {
  const out = [];
  let cur = '';
  let i = 0;
  const push = () => { if (cur) { out.push(cur); cur = ''; } };
  while (i < s.length) {
    if (s.startsWith('**', i)) {
      const end = s.indexOf('**', i + 2);
      if (end > i + 2) {
        push();
        out.push(<b key={out.length}>{s.slice(i + 2, end)}</b>);
        i = end + 2;
        continue;
      }
    }
    if (s.startsWith('___', i)) {
      push();
      out.push(<span key={out.length} className="mem-blank">_ _ _ _ _</span>);
      i += 3;
      continue;
    }
    // KaTeX 인라인 수식 ($...$) — 수동 카드(formula/manual)용
    if (s[i] === '$') {
      const end = s.indexOf('$', i + 1);
      if (end > i + 1) {
        const math = s.slice(i + 1, end);
        push();
        try {
          const html = katex.renderToString(math, { throwOnError: false, output: 'html' });
          out.push(<span key={out.length} dangerouslySetInnerHTML={{ __html: html }} />);
        } catch {
          out.push(<span key={out.length}>{`$${math}$`}</span>);
        }
        i = end + 1;
        continue;
      }
    }
    cur += s[i++];
  }
  push();
  return out;
}
