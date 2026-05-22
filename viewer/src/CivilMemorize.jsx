// 민법 통암기 — 김묘엽 「위패스 마이」 민법총칙/물권법
// 데이터: viewer/public/data/civil/{civil_total.json, civil_cards.json, civil_curated.json?}
// SRS: localStorage 'civil-srs' — 기출과 분리된 자체 박스(같은 [1,3,7,16,35,70]일 사다리)

import { useState, useEffect, useMemo, useCallback, useRef } from 'react';

const STORAGE_KEY = 'civil-srs';
const LADDER = [1, 3, 7, 16, 35, 70]; // 일
const DAY_MS = 86400000;
const SESSION_SIZE = 20;

function loadSrs() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}') || {}; }
  catch { return {}; }
}
function saveSrs(s) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); } catch { /* SSR */ }
}

function startOfDayMs(ts = Date.now()) {
  const d = new Date(ts);
  d.setHours(0, 0, 0, 0);
  return d.getTime();
}

// (prev, correct) → next srs entry
function nextSrs(prev, correct, now = Date.now()) {
  const cur = prev || { box: -1, due: 0, reps: 0, lapses: 0, last: 0 };
  if (correct) {
    const nextBox = Math.min(LADDER.length, cur.box + 1);
    if (nextBox >= LADDER.length) {
      return { box: LADDER.length, due: null, reps: cur.reps + 1, lapses: cur.lapses, last: now };
    }
    return {
      box: nextBox,
      due: startOfDayMs(now) + LADDER[nextBox] * DAY_MS,
      reps: cur.reps + 1,
      lapses: cur.lapses,
      last: now,
    };
  }
  // 오답: 박스 0으로 리셋, 내일 다시
  return {
    box: 0,
    due: startOfDayMs(now) + LADDER[0] * DAY_MS,
    reps: cur.reps,
    lapses: cur.lapses + 1,
    last: now,
  };
}

function shuffleArr(arr) {
  const out = arr.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

// 카드 큐 구성: due → fresh → in-progress 순서, 셔플 후 N장
function buildQueue(pool, srs, n = SESSION_SIZE) {
  const now = Date.now();
  const due = [], fresh = [], inProg = [];
  for (const c of pool) {
    const s = srs[c.id];
    if (!s) fresh.push(c);
    else if (s.box >= LADDER.length) continue; // graduated
    else if (s.due == null || s.due <= now) due.push(c);
    else inProg.push(c);
  }
  let q = shuffleArr(due).slice(0, n);
  if (q.length < n) q = q.concat(shuffleArr(fresh).slice(0, n - q.length));
  if (q.length < n) q = q.concat(shuffleArr(inProg).slice(0, n - q.length));
  return q;
}

// 챕터 필터: chapterTitle prefix로 매칭
function filterByChapter(cards, bookId, chapterTitle) {
  if (!chapterTitle) return cards.filter(c => c.bookId === bookId);
  return cards.filter(c => c.bookId === bookId && c.chapterTitle.includes(chapterTitle));
}

const CARD_TYPE_LABEL = {
  statute: '조문',
  definition: '정의',
  bold: '핵심어',
  mnemonic: '두문자',
  curated: '핵심',
};

export default function CivilMemorize({ onBack, isTabRoot = false }) {
  const [data, setData] = useState(null);
  const [autoCards, setAutoCards] = useState(null);
  const [curated, setCurated] = useState([]);
  const [loadErr, setLoadErr] = useState(null);
  const [srs, setSrs] = useState(loadSrs);

  // 화면 상태: 'home' | 'session' | 'done' | 'browse'
  const [view, setView] = useState('home');
  const [bookId, setBookId] = useState(null);     // 'chongchik' | 'mulgwon'
  const [chapterTitle, setChapterTitle] = useState(null);
  const [filterType, setFilterType] = useState('all'); // 'all' | 'statute' | 'definition' | 'mnemonic' | 'curated'

  const [queue, setQueue] = useState([]);
  const [idx, setIdx] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [sessionStats, setSessionStats] = useState({ correct: 0, wrong: 0 });
  const [expandSource, setExpandSource] = useState(false);

  // 데이터 로드 (한 번)
  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const [r1, r2] = await Promise.all([
          fetch('/data/civil/civil_total.json'),
          fetch('/data/civil/civil_cards.json'),
        ]);
        if (!alive) return;
        if (!r1.ok || !r2.ok) throw new Error(`fetch failed: ${r1.status}/${r2.status}`);
        const total = await r1.json();
        const cards = await r2.json();
        if (!alive) return;
        setData(total);
        setAutoCards(cards.cards || []);
      } catch (e) {
        if (alive) setLoadErr(e.message || String(e));
      }
      try {
        const r = await fetch('/data/civil/civil_curated.json');
        if (r.ok) {
          const j = await r.json();
          if (alive) setCurated((j.cards || []).map(c => ({ ...c, type: c.type || 'curated' })));
        }
      } catch { /* optional */ }
    })();
    return () => { alive = false; };
  }, []);

  // 통합 카드 풀
  const allCards = useMemo(() => {
    if (!autoCards) return [];
    return autoCards.concat(curated);
  }, [autoCards, curated]);

  // 책별 진척
  const bookProgress = useMemo(() => {
    if (!data) return [];
    const now = Date.now();
    return data.books.map(b => {
      const pool = allCards.filter(c => c.bookId === b.id);
      let learned = 0, mastered = 0, due = 0;
      for (const c of pool) {
        const s = srs[c.id];
        if (s && s.box >= LADDER.length) mastered++;
        else if (s) {
          learned++;
          if (s.due == null || s.due <= now) due++;
        }
      }
      return {
        id: b.id, title: b.title,
        total: pool.length,
        fresh: pool.length - learned - mastered,
        learned, mastered, due,
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

  // 카드 풀(현재 선택된 책 + 챕터 + 타입)
  const currentPool = useMemo(() => {
    if (!bookId) return [];
    let pool = filterByChapter(allCards, bookId, chapterTitle);
    if (filterType !== 'all') pool = pool.filter(c => c.type === filterType);
    return pool;
  }, [allCards, bookId, chapterTitle, filterType]);

  // 세션 시작
  const startSession = useCallback(() => {
    const q = buildQueue(currentPool, srs);
    if (!q.length) return;
    setQueue(q);
    setIdx(0);
    setRevealed(false);
    setExpandSource(false);
    setSessionStats({ correct: 0, wrong: 0 });
    setView('session');
  }, [currentPool, srs]);

  // 답 처리
  const onJudge = (correct) => {
    const card = queue[idx];
    if (!card) return;
    const updated = { ...srs, [card.id]: nextSrs(srs[card.id], correct) };
    setSrs(updated);
    saveSrs(updated);
    setSessionStats(s => ({ correct: s.correct + (correct ? 1 : 0), wrong: s.wrong + (correct ? 0 : 1) }));
    setRevealed(false);
    setExpandSource(false);
    if (idx + 1 >= queue.length) setView('done');
    else setIdx(idx + 1);
  };

  // 키보드 단축키: 스페이스(공개), O/X(채점)
  useEffect(() => {
    if (view !== 'session') return;
    const onKey = (e) => {
      if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); if (!revealed) setRevealed(true); }
      else if ((e.key === 'o' || e.key === 'O') && revealed) onJudge(true);
      else if ((e.key === 'x' || e.key === 'X') && revealed) onJudge(false);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [view, revealed, idx, queue]); // eslint-disable-line

  if (loadErr) {
    return (
      <div className="civil-root">
        <CivilHeader title="민법 통암기" onBack={onBack} />
        <div style={{ padding: 24, color: 'var(--danger)' }}>
          데이터 로드 실패: {loadErr}
        </div>
      </div>
    );
  }
  if (!data || !autoCards) {
    return (
      <div className="civil-root">
        <CivilHeader title="민법 통암기" onBack={onBack} />
        <div style={{ padding: 24, color: 'var(--text-sub)' }}>불러오는 중…</div>
      </div>
    );
  }

  if (view === 'home') {
    return (
      <div className="civil-root">
        <CivilHeader title="통암기" onBack={isTabRoot ? null : onBack} />
        <main className="civil-main">
          <div className="civil-hero">
            <div className="civil-hero-tag">김묘엽 「위패스 마이」 교재 통암기</div>
            <div className="civil-hero-stats">
              자동 cloze {autoCards.length.toLocaleString()}장
              {curated.length > 0 && ` · 큐레이팅 ${curated.length}장`}
              <span className="civil-divider">·</span>
              <b>{Object.keys(srs).length}</b>장 학습 시작
            </div>
          </div>

          <div className="civil-book-grid">
            {bookProgress.map(b => {
              const pct = b.total ? Math.round((b.mastered / b.total) * 100) : 0;
              return (
                <button key={b.id} className="civil-book-card"
                  onClick={() => { setBookId(b.id); setChapterTitle(null); setView('browse'); }}>
                  <div className="civil-book-title">{b.title}</div>
                  <div className="civil-book-meta">
                    카드 {b.total}장 · 마스터 {b.mastered} · 학습중 {b.learned}
                    {b.due > 0 && <span className="civil-pill civil-pill-due">오늘 복습 {b.due}</span>}
                  </div>
                  <div className="civil-book-bar">
                    <div className="civil-book-bar-fill" style={{ width: `${pct}%` }} />
                  </div>
                  <div className="civil-book-pct">마스터 {pct}%</div>
                </button>
              );
            })}
          </div>

          <section className="civil-section">
            <div className="civil-section-title">통암기란?</div>
            <ul className="civil-howto">
              <li><b>스페이스</b> 또는 카드 탭 → 정답 공개</li>
              <li><b>O</b> = 맞춤 / <b>X</b> = 틀림 (자가 채점)</li>
              <li>틀리면 내일 다시, 맞히면 1·3·7·16·35·70일 간격으로 재출제 (Leitner)</li>
              <li>6번 연속 맞히면 <b>마스터</b> 처리, 더 이상 출제 X</li>
            </ul>
          </section>
        </main>
      </div>
    );
  }

  if (view === 'browse') {
    const book = bookProgress.find(b => b.id === bookId);
    if (!book) return null;
    return (
      <div className="civil-root">
        <CivilHeader title={book.title} onBack={() => setView('home')} />
        <main className="civil-main">
          <div className="civil-quick">
            <button className="civil-btn-primary"
              disabled={book.total === 0}
              onClick={() => { setChapterTitle(null); setFilterType('all'); setTimeout(startSession, 0); }}>
              📚 전 단원 통째로 {SESSION_SIZE}장
            </button>
            {book.due > 0 && (
              <button className="civil-btn-secondary"
                onClick={() => {
                  setChapterTitle(null); setFilterType('all');
                  // due만 모은 풀
                  const now = Date.now();
                  const duePool = allCards.filter(c => c.bookId === book.id).filter(c => {
                    const s = srs[c.id]; return s && s.due != null && s.due <= now && s.box < LADDER.length;
                  });
                  const q = shuffleArr(duePool).slice(0, SESSION_SIZE);
                  if (q.length) {
                    setQueue(q); setIdx(0); setRevealed(false);
                    setSessionStats({ correct: 0, wrong: 0 }); setView('session');
                  }
                }}>
                🔁 오늘 복습 {book.due}장
              </button>
            )}
          </div>

          <div className="civil-section-title">단원별</div>
          <div className="civil-ch-list">
            {book.chapters.map(ch => {
              const pct = ch.total ? Math.round((ch.mastered / ch.total) * 100) : 0;
              return (
                <button key={ch.id} className="civil-ch-row"
                  disabled={ch.total === 0}
                  onClick={() => {
                    setChapterTitle(ch.title); setFilterType('all');
                    setTimeout(startSession, 0);
                  }}>
                  <div className="civil-ch-name">{ch.title}</div>
                  <div className="civil-ch-meta">
                    {ch.total}장
                    {ch.due > 0 && <span className="civil-pill civil-pill-due">{ch.due}</span>}
                    {ch.mastered > 0 && <span className="civil-pill civil-pill-mast">⭐ {ch.mastered}</span>}
                  </div>
                  <div className="civil-ch-bar"><div className="civil-ch-bar-fill" style={{ width: `${pct}%` }} /></div>
                </button>
              );
            })}
          </div>
        </main>
      </div>
    );
  }

  if (view === 'session') {
    const card = queue[idx];
    if (!card) {
      return (
        <div className="civil-root">
          <CivilHeader title="통암기" onBack={() => setView('browse')} />
          <div style={{ padding: 24 }}>카드가 없습니다.</div>
        </div>
      );
    }
    return (
      <div className="civil-root">
        <CivilHeader title={`${idx + 1}/${queue.length}`} onBack={() => {
          if (sessionStats.correct + sessionStats.wrong > 0 && !window.confirm('세션을 종료할까요? 지금까지 진행은 저장됐어요.')) return;
          setView('browse');
        }} />
        <div className="civil-progress-bar">
          <div className="civil-progress-fill" style={{ width: `${((idx) / queue.length) * 100}%` }} />
        </div>
        <main className="civil-main civil-session">
          <div className="civil-card-meta">
            <span className="civil-pill">{CARD_TYPE_LABEL[card.type] || card.type}</span>
            <span className="civil-card-path">{card.chapterTitle}</span>
          </div>
          <div className="civil-card" onClick={() => !revealed && setRevealed(true)}>
            <div className="civil-q">
              <CardText text={card.q} />
            </div>
            {revealed && (
              <>
                <div className="civil-divider-line" />
                <div className="civil-a">
                  <CardText text={card.a} />
                </div>
                {card.note && <div className="civil-note">💡 {card.note}</div>}
              </>
            )}
            {!revealed && <div className="civil-hint-tap">탭하거나 스페이스 → 정답</div>}
          </div>

          {revealed && (
            <div className="civil-judge">
              <button className="civil-btn-x" onClick={() => onJudge(false)}>
                <span style={{ fontSize: 22 }}>✗</span><span>틀림 (X)</span>
              </button>
              <button className="civil-btn-o" onClick={() => onJudge(true)}>
                <span style={{ fontSize: 22 }}>✓</span><span>맞춤 (O)</span>
              </button>
            </div>
          )}

          <div className="civil-session-stats">
            맞춤 {sessionStats.correct} · 틀림 {sessionStats.wrong}
            {srs[card.id] && (
              <span> · 박스 {srs[card.id].box >= LADDER.length ? '⭐ 졸업' : `${srs[card.id].box}/${LADDER.length - 1}`}</span>
            )}
          </div>
        </main>
      </div>
    );
  }

  if (view === 'done') {
    const acc = sessionStats.correct + sessionStats.wrong > 0
      ? Math.round((sessionStats.correct / (sessionStats.correct + sessionStats.wrong)) * 100) : 0;
    return (
      <div className="civil-root">
        <CivilHeader title="세션 완료" onBack={() => setView('browse')} />
        <main className="civil-main civil-done">
          <div className="civil-done-emoji">🎯</div>
          <div className="civil-done-title">{queue.length}장 끝!</div>
          <div className="civil-done-stats">
            맞춤 <b>{sessionStats.correct}</b> · 틀림 <b style={{ color: 'var(--danger)' }}>{sessionStats.wrong}</b>
            <div style={{ marginTop: 4, fontSize: '0.9rem', color: 'var(--text-sub)' }}>정답률 {acc}%</div>
          </div>
          <div className="civil-quick" style={{ marginTop: 24 }}>
            <button className="civil-btn-primary" onClick={startSession}>한 세션 더 ({SESSION_SIZE}장)</button>
            <button className="civil-btn-secondary" onClick={() => setView('browse')}>단원 선택</button>
          </div>
        </main>
      </div>
    );
  }

  return null;
}

// ─── 작은 부품들 ─────────────────────────────────────────────

function CivilHeader({ title, onBack }) {
  return (
    <header className="civil-header">
      {onBack
        ? <button className="civil-back" onClick={onBack} aria-label="뒤로">‹</button>
        : <div style={{ width: 40 }} />}
      <div className="civil-header-title">{title}</div>
      <div style={{ width: 40 }} />
    </header>
  );
}

// 줄바꿈/마크다운 light 렌더 (`**bold**`, 빈칸 `___`)
function CardText({ text }) {
  if (!text) return null;
  const parts = text.split(/(\n)/);
  return (
    <>
      {parts.map((p, i) => {
        if (p === '\n') return <br key={i} />;
        return <span key={i}>{renderInline(p)}</span>;
      })}
    </>
  );
}

function renderInline(s) {
  // 토큰화: **bold**, ___ (blank), 일반
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
      out.push(<span key={out.length} className="civil-blank">＿＿＿</span>);
      i += 3;
      continue;
    }
    cur += s[i++];
  }
  push();
  return out;
}
