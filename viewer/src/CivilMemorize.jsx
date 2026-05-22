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

import { useState, useEffect, useMemo, useCallback, useRef } from 'react';

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
    comingSoon: true },
  { id: 'realestate', title: '부동산학원론', subtitle: '국승옥 강의 기반', icon: '🏘️',
    dataDir: '/data/realestate',
    files: { total: 'total.json', cards: 'cards.json', curated: 'curated.json' },
    color: { primary: '#10b981', light: '#ecfdf5', dark: '#047857', accent: '#34d399' },
    comingSoon: true },
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

// 연속 학습일 (오늘부터 거꾸로 셈)
function computeStreak(daily) {
  if (!daily) return 0;
  let streak = 0;
  const d = new Date();
  for (let i = 0; i < 365; i++) {
    const k = dateKey(d);
    const slot = daily[k];
    if (slot && (slot.correct + slot.wrong) > 0) {
      streak++;
    } else if (i === 0) {
      // 오늘 학습 안 했음 → 어제까지의 streak 보존 (=어제 streak 유지)
      // 다만 어제도 안 했으면 끊김. 어제부터 보자.
    } else {
      break;
    }
    d.setDate(d.getDate() - 1);
  }
  // 보정: 어제까지만 학습했고 오늘 안 했으면 streak는 어제까지 카운트.
  // 위 알고리즘: 오늘 0, 어제 1, 그제 1 → streak=2. 오늘 안 한 만큼 break는 어제 끝까지 갈 때.
  return streak;
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
  const cur = prev || { box: -1, due: 0, reps: 0, lapses: 0, last: 0 };
  if (correct) {
    const nb = Math.min(LADDER.length, cur.box + 1);
    if (nb >= LADDER.length) {
      return { box: LADDER.length, due: null, reps: cur.reps + 1, lapses: cur.lapses, last: now };
    }
    return {
      box: nb, due: startOfDayMs(now) + LADDER[nb] * DAY_MS,
      reps: cur.reps + 1, lapses: cur.lapses, last: now,
    };
  }
  return {
    box: 0, due: startOfDayMs(now) + LADDER[0] * DAY_MS,
    reps: cur.reps, lapses: cur.lapses + 1, last: now,
  };
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
export default function MemorizeApp({ isTabRoot = false, onBack }) {
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

  const allCards = useMemo(() => (autoCards || []).concat(curated), [autoCards, curated]);

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
    if (chapterTitle) p = p.filter(c => c.chapterTitle.includes(chapterTitle));
    if (filterType === 'bookmark') p = p.filter(c => bookmarks[c.id]);
    else if (filterType !== 'all') p = p.filter(c => c.type === filterType);
    return p;
  }, [allCards, bookId, chapterTitle, filterType, bookmarks]);

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

  // ── 답 처리
  const commitJudge = useCallback((correct) => {
    const card = queue[idx];
    if (!card) return;
    const prev = srs[card.id];
    const ns = nextSrs(prev, correct);
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
    if (idx + 1 >= queue.length) setView('done');
    else setIdx(idx + 1);
  }, [queue, idx, srs, daily, haptic]);

  // 스와이프 → 슬라이드 아웃 → 채점
  const handleSwipeJudge = (correct) => {
    setSwipeOut(correct ? 'right' : 'left');
    // 애니메이션 후 채점. setTimeout으로 effect setState 회피.
    setTimeout(() => commitJudge(correct), 220);
  };

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

  // 키보드
  useEffect(() => {
    if (view !== 'session') return;
    const onKey = (e) => {
      if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); if (!revealed) setRevealed(true); }
      else if ((e.key === 'o' || e.key === 'O' || e.key === '1') && revealed) handleSwipeJudge(true);
      else if ((e.key === 'x' || e.key === 'X' || e.key === '2') && revealed) handleSwipeJudge(false);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [view, revealed, queue, idx]); // eslint-disable-line

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

  const streak = useMemo(() => computeStreak(daily), [daily]);
  const bookmarkCount = useMemo(() => Object.keys(bookmarks).length, [bookmarks]);

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
    return (
      <div className="mem-root">
        {memHeader('통암기', isTabRoot ? null : onBack)}
        <main className="mem-main">
          <div className="mem-hero-min">
            <div className="mem-hero-eyebrow">감정평가사 1차 · 교재 통째 외우기</div>
            <h1 className="mem-hero-h1">어떤 과목부터?</h1>
          </div>

          <div className="mem-subject-grid">
            {SUBJECTS.map(sub => {
              const enabled = !sub.comingSoon;
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
                  }}
                >
                  <div className="mem-subject-icon">{sub.icon}</div>
                  <div className="mem-subject-info">
                    <div className="mem-subject-title">{sub.title}</div>
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

          {/* 스트릭 + sparkline */}
          <div className="mem-streak-card">
            <div className="mem-streak-icon">{streak > 0 ? '🔥' : '🌱'}</div>
            <div className="mem-streak-body">
              <div className="mem-streak-num">{streak}<span>일</span></div>
              <div className="mem-streak-label">{streak > 0 ? '연속 학습 중' : '오늘 시작!'}</div>
            </div>
            <Sparkline data={sparkData} />
          </div>

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
            </div>
            <span className="mem-card-path">{card.chapterTitle}</span>
          </div>

          <div
            ref={cardRef}
            className={`mem-card ${revealed ? 'is-revealed' : ''}`}
            style={{ transform, transition: swipeState.active ? 'none' : 'transform 0.2s ease' }}
            onTouchStart={onTouchStart}
            onTouchMove={onTouchMove}
            onTouchEnd={onTouchEnd}
            onClick={() => !revealed && setRevealed(true)}
          >
            <div className="mem-q"><CardText text={card.q} /></div>
            <div className={`mem-reveal-zone ${revealed ? '' : 'is-hidden'}`}>
              <div className="mem-divider-line" />
              <div className="mem-a"><CardText text={card.a} /></div>
              {card.note && <div className="mem-note">💡 {card.note}</div>}
            </div>
            {!revealed && (
              <div className="mem-card-hint">
                <span>탭 또는 <kbd>Space</kbd> → 정답</span>
              </div>
            )}

            {/* 스와이프 인디케이터 (드래그 중) */}
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
              <div className="mem-kbd-hint">
                <kbd>O</kbd>·<kbd>1</kbd> 맞춤 &nbsp;·&nbsp; <kbd>X</kbd>·<kbd>2</kbd> 틀림 &nbsp;·&nbsp; 좌/우 스와이프
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
            <div className="mem-opt-label">햅틱 (모바일 진동)</div>
            <div className="mem-opt-row">
              <button className={`mem-chip ${haptic ? 'is-active' : ''}`}
                onClick={() => { setHaptic(true); lsSave(HAPTIC_KEY, '1'); }}>켜기</button>
              <button className={`mem-chip ${!haptic ? 'is-active' : ''}`}
                onClick={() => { setHaptic(false); lsSave(HAPTIC_KEY, '0'); }}>끄기</button>
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
    cur += s[i++];
  }
  push();
  return out;
}
