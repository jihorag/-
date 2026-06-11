// ⚡ 퀴즈 탭 — 교재 암기 브리지.
// AI 학습(이해) → 퀴즈(암기) → 문제풀이(적용)의 교두보.
// AI 학습과 완전히 같은 목차(leaves)·같은 교재(units/*.md)를 쓰되,
// 문제풀이와는 별개로 "교재 내용 자체를 암기"하는 훈련만 제공한다.
//   ① 🃏 용어 카드 — 교재에서 추출한 용어·정의 (SRS)
//   ② ⬜ 빈칸 인출 — 정의문의 핵심어를 가리고 떠올리기 (콤보)
//   ③ 🗺 목차 인출 — 단원 소제목을 순서대로 떠올리기
import { useState, useEffect, useMemo, useRef } from 'react';
import { ArrowLeft } from 'lucide-react';
import { SUBJECTS, getMastery as getAiMastery } from './aiLearningStore';
import { sliceSection } from './aiClaudeClient';
import { leafQuizStats } from './leafStats';
import { loadChatCards, removeChatCard } from './AILearning';

const MEM_KEY = 'quiz-mem-v1';
// 햅틱 — 1차 문제풀이와 동일한 패턴 (정답 짧게 / 오답 떨림)
const buzz = (ok) => {
  try {
    if (!navigator.vibrate) return;
    navigator.vibrate(ok ? 18 : [35, 30, 35]);
  } catch { /* 미지원 */ }
};
const SRS_DAYS = [1, 3, 7, 14, 30];

const indexUrl = (subjectId) => {
  const s = SUBJECTS.find((x) => x.id === subjectId);
  if (s?.stage === 2) return `/data/study/${subjectId}/ai_index.json`;
  return `/data/study/${subjectId}/ai_taxonomy_index.json`;
};
const studyBase = (subjectId) => `/data/study/${subjectId}/`;

// ───────────────────────── 진행 저장 ─────────────────────────
function loadMem() {
  try { return JSON.parse(localStorage.getItem(MEM_KEY) || '{}') || {}; } catch { return {}; }
}
function saveMem(m) {
  try { localStorage.setItem(MEM_KEY, JSON.stringify(m)); } catch { /* full */ }
}

// ───────────────────────── 교재 → 암기 자산 추출 ─────────────────────────
// md 구조가 단원마다 다르므로 휴리스틱 3종을 합치고 dedupe:
//  1) 정의문: "X란/이란 … 말한다·한다·의미한다" → {term, def}
//  2) 볼드 용어: **용어** → 포함 단락을 def로
//  3) 헤딩(###/####): 목차 인출용
export function extractKnowledge(md) {
  if (!md) return { cards: [], outline: [] };
  const rawLines = md.split('\n');

  // 목차: 네비게이션 블록·앵커 링크 제외한 실제 소제목
  const outline = [];
  for (const l of rawLines) {
    const m = l.match(/^(#{3,5})\s*(?:<a[^>]*><\/a>)?\s*(.+)/);
    if (!m) continue;
    let t = m[2].replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[📘📖📚🗺️#*`]/g, '').trim();
    if (!t || /본문 목차|핵심요약서|기본서|위패스|단권화/.test(t)) continue;
    if (t.length < 2 || t.length > 60) continue;
    outline.push({ level: m[1].length, text: t });
  }

  // 단락 결합 (PDF 줄바꿈으로 끊긴 문장 복원) — 직전 헤딩도 함께 추적
  const paras = []; // {text, head}
  let buf = [];
  let curHead = '';
  for (const l of rawLines) {
    const s = l.trim();
    const hm = s.match(/^#{3,5}\s*(?:<a[^>]*><\/a>)?\s*(.+)/);
    if (hm) {
      curHead = hm[1].replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[📘📖📚🗺️#*`]/g, '')
        .replace(/^[IVXⅠ-Ⅹ\d]+[.)]?\s*/, '').trim();
    }
    if (!s || s.startsWith('#') || s.startsWith('>') || s.startsWith('---') || s.startsWith('|')) {
      if (buf.length) { paras.push({ text: buf.join(' '), head: curHead }); buf = []; }
    } else buf.push(s);
  }
  if (buf.length) paras.push({ text: buf.join(' '), head: curHead });

  // 용어 정제: 선행 부사·접속어 제거, 마지막 의미 단위만
  const STOP_LEAD = /^(여기서|이때|즉|또한|그리고|그러나|한편|다만|보통|일반적으로|우리(?:가)?|이는|특히|따라서|원칙적으로|민법상|법률상)\s*/;
  const cleanTerm = (raw) => {
    let t = raw.replace(/^[^가-힣A-Za-z0-9]+/, '').trim();
    for (let i = 0; i < 3; i++) {
      const n = t.replace(STOP_LEAD, '');
      if (n === t) break; t = n;
    }
    // 너무 길면 마지막 3어절만 (정의문 핵심어는 대개 말미)
    const words = t.split(/\s+/);
    if (words.length > 3) t = words.slice(-3).join(' ');
    return t.trim();
  };

  const cards = [];
  const seen = new Set();
  const push = (term, def, kind) => {
    const key = term.replace(/\s+/g, '');
    if (!key || key.length < 2 || key.length > 25 || seen.has(key)) return;
    if (def.length < 12 || def.length > 320) return;
    if (/^[\d.,)(]+$/.test(key)) return;
    seen.add(key);
    cards.push({ key, term: term.trim(), def: def.trim(), kind });
  };

  for (const { text: p, head } of paras) {
    const clean = p.replace(/\*\*/g, '');
    // 1) 정의문 패턴
    const defRe = /([가-힣A-Za-z0-9·()\s]{2,30}?)(?:이란|란)\s+(.{10,250}?(?:말한다|한다|의미한다|가리킨다|뜻한다))/g;
    let m;
    while ((m = defRe.exec(clean)) !== null) {
      const term = cleanTerm(m[1]);
      if (term.length >= 2) push(term, `${term}(이)란 ${m[2]}`, 'def');
    }
    // 2) 볼드 용어 — 단락을 정의로
    const boldRe = /\*\*([^*\n]{2,28})\*\*/g;
    while ((m = boldRe.exec(p)) !== null) {
      const term = m[1].trim();
      if (/^\d+[.)]?$/.test(term)) continue;        // 번호만인 볼드 제외
      if (clean.length >= 20) push(term, clean.slice(0, 300), 'bold');
    }
    // 3) 헤딩 + 본문 단락 (정의문·볼드가 빈약한 단원 보강)
    if (head && head.length >= 2 && head.length <= 25 && clean.length >= 40
        && !/^(의의|서설|개요|기타|결론)$/.test(head)) {
      push(head, clean.slice(0, 300), 'head');
    }
  }
  // 정의문 카드 우선, 그다음 볼드, 헤딩 순으로 정렬해 상위 40장
  const rank = { def: 0, bold: 1, head: 2 };
  cards.sort((a, b) => rank[a.kind] - rank[b.kind]);
  return { cards: cards.slice(0, 40), outline: outline.slice(0, 30) };
}

// 빈칸 문장: def에서 term 등장부를 ⬜로
function clozeText(card) {
  const esc = card.term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const re = new RegExp(esc.replace(/\s+/g, '\\s*'), 'g');
  const blanked = card.def.replace(re, '⬜'.repeat(Math.min(6, Math.max(2, Math.round(card.term.length / 2)))));
  return blanked === card.def ? null : blanked;
}

// leaf의 암기 진행률 (아는 카드 비율) — total은 채팅카드 실수량 우선
export function memProgressOf(mem, leafId, totalOverride) {
  const m = mem[leafId];
  const total = totalOverride != null ? totalOverride : (m?.total || 0);
  if (!total) return { pct: 0, known: 0, total: 0, outlineDone: !!m?.outlineDone };
  const known = Math.min(total, Object.values(m?.srs || {}).filter(s => s.box >= 2).length);
  return { pct: Math.round((known / total) * 100), known, total, outlineDone: !!m?.outlineDone };
}

// ───────────────────────── 메인 컴포넌트 ─────────────────────────
// 자체 내비: subjects → leaves → train(허브+훈련). App은 quizHome 뷰에서 이 컴포넌트만 렌더.
// 문제풀이 드릴과 동일한 토스 스타일 리스트 행 (browse-row CSS 공유)
function splitRowPrefix(title) {
  const m = (title || '').match(/^(PART\s*\d+|Chapter\s*\d+|제\d+(?:장|절|관|편)|\d+절)\s+(.+)$/);
  if (m) return { prefix: m[1], rest: m[2] };
  return { prefix: null, rest: title };
}
function MemRow({ title, countLabel, pct, showBar, meta, onClick }) {
  const { prefix, rest } = splitRowPrefix(title);
  return (
    <button className="browse-row" onClick={onClick}>
      <div className="browse-row__main">
        <div className="browse-row__title">
          {prefix && <span className="browse-row__prefix">{prefix}</span>}
          {rest}
        </div>
        {showBar && <div className="browse-row__bar"><div style={{ width: `${Math.max(2, pct)}%` }} /></div>}
        {meta && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginTop: 5,
            fontSize: '0.68rem', color: '#6b7280' }}>{meta}</div>
        )}
      </div>
      <div className="browse-row__meta">
        {showBar && pct > 0 && <span className="browse-row__pct">{pct}%</span>}
        <span className="browse-row__count">{countLabel}</span>
        <span className="browse-row__chev">›</span>
      </div>
    </button>
  );
}

export default function MemorizeBridge({ classifiedList, progress, qid, onGoSolve, onGoAI }) {
  const [screen, setScreen] = useState('subjects'); // subjects | leaves | train
  const [subjectId, setSubjectId] = useState(null);
  const [leaves, setLeaves] = useState([]);
  const [leavesError, setLeavesError] = useState(false);
  const [pathStack, setPathStack] = useState([]);   // 계층 드릴다운 경로 (문제풀이와 동일 탐색)
  const [leaf, setLeaf] = useState(null);
  const [mem, setMem] = useState(loadMem);
  const leavesScrollRef = useRef(0); // 단원 목록 스크롤 보존 (훈련 갔다 와도 그 자리)
  // 🔁 전과목 오늘 복습 큐
  const [reviewQueue, setReviewQueue] = useState([]);
  const [rIdx, setRIdx] = useState(0);
  const [rFlip, setRFlip] = useState(false);

  const subj = SUBJECTS.find(s => s.id === subjectId);
  const aiMastery = useMemo(() => getAiMastery(), [screen]);

  // 목록 복귀 시 스크롤 복원 / 새 화면은 맨 위
  useEffect(() => {
    if (screen === 'leaves') window.scrollTo(0, leavesScrollRef.current || 0);
    else window.scrollTo(0, 0);
  }, [screen]);

  // 과목 목차 로드 (AI 학습과 동일 index)
  useEffect(() => {
    if (!subjectId) return;
    let dead = false;
    setLeavesError(false);
    fetch(indexUrl(subjectId)).then(r => {
      if (!r.ok) throw new Error(String(r.status));
      return r.json();
    }).then(raw => {
      if (dead) return;
      const ls = raw?.leaves || raw || [];
      setLeaves(Array.isArray(ls) ? ls : []);
    }).catch(() => { if (!dead) { setLeaves([]); setLeavesError(true); } });
    return () => { dead = true; };
  }, [subjectId]);

  const updateMem = (leafId, patch) => {
    setMem(prev => {
      const next = { ...prev, [leafId]: { ...(prev[leafId] || {}), ...patch, ts: Date.now() } };
      saveMem(next);
      return next;
    });
  };

  // ── 화면 1: 과목 — 문제풀이 탭과 동일한 섹션·카드 디자인 ──
  if (screen === 'subjects') {
    const T = { card: '#FFFFFF', blue: '#3182F6', blueWeak: '#E8F1FE', ink: '#191F28', sub: '#8B95A1', track: '#E5E8EB', shadow: '0 2px 8px rgba(0, 23, 51, 0.06)', radius: 20 };
    const chatCards = loadChatCards();
    // 과목별 카드/암기 진행 집계
    const statOf = (sid) => {
      let total = 0, known = 0;
      for (const [lid, cards] of Object.entries(chatCards)) {
        if (!lid.startsWith(sid + '__') && !lid.startsWith(sid + '_')) continue;
        total += cards.length;
        const srsMap = mem[lid]?.srs || {};
        known += cards.filter(c => (srsMap[c.term.replace(/\s+/g, '')]?.box || 0) >= 2).length;
      }
      return { total, known, pct: total ? Math.round((known / total) * 100) : 0 };
    };
    // 오늘 복습 due 집계
    const now = Date.now();
    const due = [];
    for (const [lid, cards] of Object.entries(chatCards)) {
      const srsMap = mem[lid]?.srs || {};
      for (const c of cards) {
        const s = srsMap[c.term.replace(/\s+/g, '')];
        if (s && s.due <= now) due.push({ leafId: lid, card: { key: c.term.replace(/\s+/g, ''), ...c } });
      }
    }
    return (
      <div className="app-container" style={{ minHeight: '100dvh', paddingBottom: 24 }}>
        <div className="screen-head" style={{ paddingTop: 'calc(18px + env(safe-area-inset-top, 0px))' }}>
          <h1 className="screen-title">⚡ 퀴즈</h1>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-sub, #64748b)', marginTop: 4 }}>
            AI 학습 대화에서 자동 출제된 내 카드로 암기해요 — 이해 → 암기 → 적용
          </p>
        </div>
        <main className="main-content" style={{ marginTop: 16 }}>
          {/* 🔁 오늘 복습 — 문제풀이의 통합검색 자리와 동일한 상단 배치 */}
          {due.length > 0 && (
            <button onClick={() => { setReviewQueue(due.slice(0, 50)); setRIdx(0); setRFlip(false); setScreen('review'); }}
              style={{ width: '100%', textAlign: 'left', padding: '14px 16px', marginBottom: 20,
                border: '1px solid #fde68a', borderRadius: 12, background: '#fffbeb',
                color: '#92400e', fontSize: '0.95rem', cursor: 'pointer', fontWeight: 700,
                display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>🔁 오늘 복습할 카드 {due.length}장 — 잊기 전에 인출</span>
              <span style={{ fontWeight: 800 }}>시작 →</span>
            </button>
          )}
          {[
            { stage: 1, label: '1차 시험 — 객관식 5지선다', chipBg: T.blueWeak, chipFg: T.blue, bar: T.blue },
            { stage: 2, label: '2차 시험 — 서술형·답안 작성', chipBg: '#F0EBFF', chipFg: '#7C3AED', bar: '#7C3AED' },
          ].map(({ stage, label, chipBg, chipFg, bar }) => {
            const subjects = SUBJECTS.filter(s => s.stage === stage);
            return (
              <div key={stage} style={{ marginBottom: 18 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
                  <div style={{ fontSize: '1rem', color: T.ink, fontWeight: 800 }}>
                    {stage === 1 ? '📖' : '✍️'} {label}
                  </div>
                  <span style={{ fontSize: '0.82rem', color: T.sub, fontWeight: 600 }}>{subjects.length}과목</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', rowGap: 14, columnGap: 12, alignItems: 'start' }}>
                  {subjects.map(s => {
                    const st = statOf(s.id);
                    return (
                      <div key={s.id} style={{ background: T.card, border: 'none', borderRadius: T.radius,
                        display: 'flex', flexDirection: 'column', boxShadow: T.shadow }}>
                        <button onClick={() => { setSubjectId(s.id); setPathStack([]); setScreen('leaves'); }}
                          style={{ padding: '20px 18px 16px', textAlign: 'left', background: 'none', border: 'none',
                            cursor: 'pointer', width: '100%', display: 'flex', flexDirection: 'column', gap: 12 }}>
                          <div style={{ display: 'flex' }}>
                            <span style={{ fontSize: '0.7rem', fontWeight: 800, background: chipBg, color: chipFg,
                              padding: '3px 9px', borderRadius: 999 }}>{stage === 1 ? '1차' : '2차'}</span>
                          </div>
                          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                            <div style={{ minWidth: 0, flex: 1 }}>
                              <div style={{ fontWeight: 800, color: T.ink, fontSize: '1.2rem', letterSpacing: '-0.01em', lineHeight: 1.3 }}>{s.short}</div>
                              <div style={{ fontSize: '0.82rem', color: T.sub, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', marginTop: 4 }}>{s.title}</div>
                            </div>
                            <div style={{ fontSize: '2rem', lineHeight: 1, flex: '0 0 auto' }}>{s.icon}</div>
                          </div>
                          <div>
                            <div style={{ height: 6, background: T.track, borderRadius: 999, overflow: 'hidden' }}>
                              <div style={{ width: `${Math.max(2, st.pct)}%`, height: '100%', background: bar, borderRadius: 999 }} />
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginTop: 5 }}>
                              <span style={{ fontWeight: 800, color: T.ink }}>{st.pct}%</span>
                              <span style={{ color: T.sub, fontWeight: 600 }}>{st.total > 0 ? `카드 ${st.total}장` : '카드 없음'}</span>
                            </div>
                          </div>
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </main>
      </div>
    );
  }

  // ── 🔁 전과목 오늘 복습 러너 ──
  if (screen === 'review') {
    const item = reviewQueue[rIdx];
    const gradeReview = (ok) => {
      const { leafId, card } = item;
      const srsMap = mem[leafId]?.srs || {};
      const prev = srsMap[card.key] || { box: 0, miss: 0 };
      const now = Date.now();
      const entry = ok
        ? { box: Math.min(prev.box + 1, SRS_DAYS.length), due: now + SRS_DAYS[Math.min(prev.box, SRS_DAYS.length - 1)] * 86400000, miss: prev.miss || 0, ts: now }
        : { box: 0, due: now + 10 * 60000, miss: (prev.miss || 0) + 1, ts: now };
      updateMem(leafId, { srs: { ...srsMap, [card.key]: entry } });
      buzz(ok);
      setRFlip(false); setRIdx(i => i + 1);
    };
    const leafLabel = (lid) => {
      const segs = lid.split('__');
      return segs.slice(-1)[0].replace(/_/g, ' ');
    };
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', paddingBottom: 24 }}>
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <button className="back-btn" onClick={() => setScreen('subjects')}>
            <ArrowLeft size={24} style={{ marginRight: 8 }} />
            <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>과목</span>
          </button>
          <span style={{ paddingRight: 10, fontWeight: 700, fontSize: '0.8rem', color: '#6b7280' }}>
            🔁 {Math.min(rIdx, reviewQueue.length)}/{reviewQueue.length}
          </span>
        </header>
        <main className="main-content" style={{ marginTop: 14 }}>
          {!item ? (
            <div style={{ padding: 40, textAlign: 'center' }}>
              <div style={{ fontSize: '2.2rem' }}>🎉</div>
              <div style={{ fontWeight: 800, marginTop: 8 }}>오늘 복습 완료!</div>
              <div style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: 6 }}>
                틀린 카드는 10분 뒤 다시, 맞은 카드는 며칠 뒤에 돌아옵니다.
              </div>
              <button onClick={() => setScreen('subjects')}
                style={{ marginTop: 18, padding: '11px 22px', borderRadius: 10, border: 'none',
                  background: '#d97706', color: '#fff', fontWeight: 800, cursor: 'pointer' }}>
                과목으로
              </button>
            </div>
          ) : (
            <>
              <div style={{ fontSize: '0.7rem', color: '#9ca3af', marginBottom: 8 }}>
                📍 {leafLabel(item.leafId)}
              </div>
              <div onClick={() => setRFlip(f => !f)}
                style={{ background: '#fff', borderRadius: 16, padding: 22, minHeight: 220, cursor: 'pointer',
                  border: `1.5px solid ${rFlip ? '#fcd34d' : '#e5e7eb'}`, boxShadow: '0 4px 14px rgba(0,0,0,0.06)',
                  display: 'flex', flexDirection: 'column' }}>
                <div style={{ fontWeight: 900, fontSize: '1.2rem', color: '#111827' }}>
                  {item.card.term}
                  {item.card.importance >= 3 && <span style={{ marginLeft: 8, fontSize: '0.72rem', color: '#d97706' }}>★ 핵심</span>}
                </div>
                {rFlip
                  ? <div style={{ marginTop: 12, fontSize: '0.92rem', lineHeight: 1.7, color: '#374151' }}>{item.card.def}</div>
                  : <div style={{ marginTop: 'auto', paddingTop: 26, textAlign: 'center', color: '#d97706',
                      fontSize: '0.85rem', fontWeight: 700 }}>떠올려보세요 (탭하면 공개)</div>}
              </div>
              {rFlip ? (
                <div style={{ display: 'flex', gap: 8, marginTop: 14 }}>
                  <button onClick={() => gradeReview(false)} style={gradeBtn('#dc2626', '#fef2f2', '#fecaca')}>✕ 모름</button>
                  <button onClick={() => gradeReview(true)} style={gradeBtn('#059669', '#ecfdf5', '#a7f3d0')}>✓ 알았다</button>
                </div>
              ) : (
                <button onClick={() => setRFlip(true)}
                  style={{ width: '100%', marginTop: 14, padding: '13px', borderRadius: 12, border: 'none',
                    background: '#d97706', color: '#fff', fontWeight: 800, fontSize: '0.95rem', cursor: 'pointer' }}>
                  정답 보기
                </button>
              )}
            </>
          )}
        </main>
      </div>
    );
  }

  // ── 화면 2: 단원 드릴다운 — 문제풀이와 동일한 계층 탐색 UI (browse-row) ──
  if (screen === 'leaves') {
    const chatCards = loadChatCards();
    const cardsOf = (id) => (chatCards[id] || []).length;
    // 현재 경로(pathStack) 하위의 다음 레벨 그룹/절 계산
    const under = leaves.filter(l => pathStack.every((seg, i) => l.path?.[i] === seg));
    const depth = pathStack.length;
    const groupsMap = new Map(); // seg → leaves[]
    const leafRows = [];
    for (const l of under) {
      if ((l.path?.length || 0) === depth + 1) leafRows.push(l);
      else {
        const seg = l.path?.[depth];
        if (!seg) continue;
        if (!groupsMap.has(seg)) groupsMap.set(seg, []);
        groupsMap.get(seg).push(l);
      }
    }
    const dot = (on, color, half) => (
      <span style={{ width: 8, height: 8, borderRadius: '50%', display: 'inline-block',
        background: on ? color : half ? `${color}55` : '#e5e7eb' }} />
    );
    const memPctOf = (ls) => {
      let known = 0, total = 0;
      for (const l of ls) {
        const mp = memProgressOf(mem, l.id, cardsOf(l.id));
        known += mp.known; total += mp.total;
      }
      return total > 0 ? Math.round((known / total) * 100) : 0;
    };
    const groupCards = (ls) => ls.reduce((s, l) => s + cardsOf(l.id), 0);
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', paddingBottom: 24 }}>
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn"
            onClick={() => (depth === 0 ? setScreen('subjects') : setPathStack(p => p.slice(0, -1)))}>
            <ArrowLeft size={24} style={{ marginRight: 8 }} />
            <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>
              {depth === 0 ? '과목' : '뒤로가기'}
            </span>
          </button>
        </header>
        <div className="screen-head">
          {/* 문제풀이와 동일한 브레드크럼 */}
          <div style={{ fontSize: '0.74rem', color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>
            {subj?.short} 암기{pathStack.map((s, i) => <span key={i}> ▸ {s}</span>)}
          </div>
          <h1 className="screen-title">
            {subj?.icon} {pathStack.length ? pathStack[pathStack.length - 1] : `${subj?.title}`}
          </h1>
          <p style={{ fontSize: '0.78rem', color: '#6b7280', marginTop: 4 }}>
            🤖 이해 → ⚡ 암기 → ✍️ 적용
          </p>
        </div>
        <main className="main-content" style={{ marginTop: 10 }}>
          {leaves.length === 0 && !leavesError && (
            <div style={{ padding: 30, textAlign: 'center', color: '#9ca3af', fontSize: '0.85rem' }}>목차 불러오는 중…</div>
          )}
          {leavesError && (
            <div style={{ padding: 26, textAlign: 'center', background: '#fff', borderRadius: 12,
              border: '1px solid #fecaca' }}>
              <div style={{ fontSize: '0.88rem', color: '#b91c1c', fontWeight: 700 }}>목차를 불러오지 못했어요</div>
              <div style={{ fontSize: '0.76rem', color: '#9ca3af', marginTop: 4 }}>네트워크 상태를 확인해주세요</div>
              <button onClick={() => { setSubjectId(null); setTimeout(() => setSubjectId(subj?.id || subjectId), 0); }}
                style={{ marginTop: 12, padding: '9px 20px', borderRadius: 9, border: 'none',
                  background: 'var(--primary, #2563eb)', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>
                다시 시도
              </button>
            </div>
          )}
          {/* 그룹 행 (장·편 — 문제풀이 BrowseRow와 동일 룩) */}
          {[...groupsMap.entries()].map(([seg, ls]) => {
            const pct = memPctOf(ls);
            const gc = groupCards(ls);
            return (
              <MemRow key={seg} title={seg}
                countLabel={gc > 0 ? `카드 ${gc}장` : `${ls.length}개 절`}
                pct={pct} showBar={pct > 0}
                onClick={() => setPathStack(p => [...p, seg])} />
            );
          })}
          {/* 절(leaf) 행 — 브리지 3단계 상태를 메타로 */}
          {leafRows.map(l => {
            const ai = aiMastery[l.id]?.status;
            const mp = memProgressOf(mem, l.id, cardsOf(l.id));
            const qs = leafQuizStats(l, classifiedList, progress, qid);
            return (
              <MemRow key={l.id} title={l.title || l.path?.slice(-1)[0]}
                countLabel={mp.total > 0 ? `${mp.total}장 · ${mp.pct}%` : '카드 없음'}
                pct={mp.pct} showBar={mp.pct > 0}
                meta={<>
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                    {dot(ai === 'mastered', '#4f46e5', ai === 'in_progress')} 🤖 이해
                  </span>
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                    {dot(mp.pct >= 80, '#7c3aed', mp.pct > 0)} ⚡ 암기
                  </span>
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                    {dot(qs.total > 0 && qs.accuracy >= 0.8 && qs.coverage >= 0.5, '#059669', qs.answered > 0)}
                    ✍️ 적용{qs.answered > 0 ? ` ${Math.round(qs.accuracy * 100)}%` : ''}
                  </span>
                </>}
                onClick={() => { leavesScrollRef.current = window.scrollY; setLeaf(l); setScreen('train'); }} />
            );
          })}
        </main>
      </div>
    );
  }

  // ── 화면 3: 단원 훈련 (허브 + 카드/빈칸/목차) ──
  if (screen === 'train' && leaf) {
    return <LeafTrainer key={leaf.id} subjectId={subjectId} leaf={leaf} mem={mem} updateMem={updateMem}
      onBack={() => setScreen('leaves')}
      onGoSolve={onGoSolve} onGoAI={onGoAI}
      solveStats={leafQuizStats(leaf, classifiedList, progress, qid)} />;
  }
  return null;
}

// ───────────────────────── 단원 훈련 화면 ─────────────────────────
function LeafTrainer({ subjectId, leaf, mem, updateMem, onBack, onGoSolve, onGoAI, solveStats }) {
  const [knowledge, setKnowledge] = useState(null); // {cards, outline}
  const [mode, setMode] = useState('hub');          // hub | cards | cloze | outline
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [combo, setCombo] = useState(0);
  const [revealCnt, setRevealCnt] = useState(0);
  const [sessionDone, setSessionDone] = useState(0);
  const timerRef = useRef(null);

  // 카드 소스: 🃏 AI 학습 채팅에서 자동 출제된 내 카드(quiz-chatcards-v1).
  // 목차 인출만 교재 헤딩에서 추출(구조 정보라 품질 안정적).
  useEffect(() => {
    let dead = false;
    (async () => {
      const myCards = (loadChatCards()[leaf.id] || []).map(c => ({
        key: c.term.replace(/\s+/g, ''), ...c,
      }));
      let outline = [];
      if (leaf.unit_file) {
        try {
          const md = await fetch(studyBase(subjectId) + leaf.unit_file).then(r => r.text());
          const sliced = (leaf.section_key && leaf.section_key !== 'full' && leaf.section_lines)
            ? sliceSection(md, { lines: leaf.section_lines }) : md;
          outline = extractKnowledge(sliced).outline;
        } catch { /* offline */ }
      }
      if (dead) return;
      setKnowledge({ cards: myCards, outline });
      if (myCards.length) updateMem(leaf.id, { total: myCards.length });
    })();
    return () => { dead = true; clearTimeout(timerRef.current); };
  }, [subjectId, leaf.id]); // eslint-disable-line react-hooks/exhaustive-deps

  // ⌨️ 데스크톱 단축키: Space=정답 보기, ←=모름, →=알았다, 1~4=4지선다 보기
  useEffect(() => {
    const onKey = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (mode === 'cards' || mode === 'cloze') {
        const list = mode === 'cards' ? queue : clozeQueue;
        const card = list[idx];
        if (!card) return;
        if (e.code === 'Space') { e.preventDefault(); setFlipped(f => !f); }
        else if (flipped && e.key === 'ArrowLeft') grade(card, false);
        else if (flipped && e.key === 'ArrowRight') grade(card, true);
      } else if (mode === 'mcq' && /^[1-4]$/.test(e.key) && !flipped) {
        const btns = document.querySelectorAll('main button[data-mcq]');
        btns[parseInt(e.key, 10) - 1]?.click();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }); // 매 렌더 최신 상태 클로저 사용

  const srs = mem[leaf.id]?.srs || {};
  const grade = (card, ok) => {
    const prev = srs[card.key] || { box: 0, miss: 0 };
    const now = Date.now();
    const entry = ok
      ? { box: Math.min(prev.box + 1, SRS_DAYS.length), due: now + SRS_DAYS[Math.min(prev.box, SRS_DAYS.length - 1)] * 86400000, miss: prev.miss || 0, ts: now }
      : { box: 0, due: now + 10 * 60000, miss: (prev.miss || 0) + 1, ts: now }; // miss≥2 → AI 튜터가 재설명(역피드백)
    updateMem(leaf.id, { srs: { ...srs, [card.key]: entry } });
    buzz(ok);
    setCombo(ok ? combo + 1 : 0);
    setSessionDone(n => n + 1);
    setFlipped(false);
    setIdx(i => i + 1);
  };

  // 훈련 큐: due 우선 + 미학습 (훅은 조기 return보다 항상 먼저)
  const queue = useMemo(() => {
    if (!knowledge) return [];
    const now = Date.now();
    const cs = knowledge.cards;
    const due = cs.filter(c => srs[c.key] && srs[c.key].due <= now);
    const fresh = cs.filter(c => !srs[c.key]).sort((a, b) => (b.importance || 2) - (a.importance || 2));
    const rest = cs.filter(c => srs[c.key] && srs[c.key].due > now);
    return [...due, ...fresh, ...rest];
  }, [knowledge, mode]); // eslint-disable-line react-hooks/exhaustive-deps

  const clozeQueue = useMemo(() => queue.map(c => ({ ...c, blanked: c.cloze || clozeText(c) })).filter(c => c.blanked), [queue]);

  if (!knowledge) {
    return <div className="app-container" style={{ padding: 40, textAlign: 'center', color: '#9ca3af' }}>교재 불러오는 중…</div>;
  }
  const mp = memProgressOf(mem, leaf.id);

  const header = (
    <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb',
      display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <button className="back-btn" onClick={() => (mode === 'hub' ? onBack() : (setMode('hub'), setIdx(0), setFlipped(false), setCombo(0)))}>
        <ArrowLeft size={24} style={{ marginRight: 8 }} />
        <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>{mode === 'hub' ? '단원 목록' : '훈련 선택'}</span>
      </button>
      {mode !== 'hub' && combo >= 2 && (
        <span style={{ paddingRight: 10, fontWeight: 800, fontSize: '0.85rem', color: '#ea580c' }}>🔥 {combo}연속</span>
      )}
    </header>
  );

  // ── 허브 ──
  if (mode === 'hub') {
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', paddingBottom: 24 }}>
        {header}
        <main className="main-content" style={{ marginTop: 14 }}>
          <div style={{ fontSize: '0.72rem', color: '#9ca3af' }}>{(leaf.path || []).slice(0, -1).join(' › ')}</div>
          <h2 style={{ fontSize: '1.15rem', fontWeight: 900, color: '#111827', margin: '4px 0 6px' }}>
            {leaf.title || leaf.path?.slice(-1)[0]}
          </h2>
          <div style={{ fontSize: '0.78rem', color: '#6b7280', marginBottom: 14 }}>
            ⚡ 암기 {mp.pct}% ({mp.known}/{mp.total}) {mp.outlineDone && ' · 🗺 목차 완료'}
          </div>

          {knowledge.cards.length === 0 ? (
            <div style={{ padding: 22, background: '#fff', borderRadius: 14, border: '1.5px dashed #c7d2fe',
              textAlign: 'center' }}>
              <div style={{ fontSize: '1.8rem' }}>🃏</div>
              <div style={{ fontWeight: 800, fontSize: '0.95rem', color: '#111827', marginTop: 8 }}>
                아직 이 단원 카드가 없어요
              </div>
              <div style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: 6, lineHeight: 1.7 }}>
                🤖 <b>AI 학습</b>에서 이 단원을 배우면, 대화에서 나온 핵심이<br />
                <b>자동으로 암기카드로 출제</b>되어 여기에 쌓입니다.
              </div>
              <button onClick={() => onGoAI?.(subjectId, leaf)}
                style={{ marginTop: 14, padding: '11px 22px', borderRadius: 12, border: 'none',
                  background: '#4f46e5', color: '#fff', fontWeight: 800, cursor: 'pointer', fontSize: '0.88rem' }}>
                🤖 AI 학습으로 배우러 가기
              </button>
            </div>
          ) : (
            <>
              <button onClick={() => { setMode('cards'); setIdx(0); setFlipped(false); setCombo(0); setSessionDone(0); }}
                style={trainBtn('#7c3aed', '#f5f3ff', '#ddd6fe')}>
                <span style={{ fontSize: '1.5rem' }}>🃏</span>
                <span style={{ flex: 1 }}>
                  <b style={{ display: 'block', color: '#5b21b6' }}>용어 카드 {knowledge.cards.length}장</b>
                  <span style={smallDesc}>교재 용어·정의 — 앞면 보고 떠올리기 (SRS 복습)</span>
                </span>
              </button>
              {clozeQueue.length > 0 && (
                <button onClick={() => { setMode('cloze'); setIdx(0); setFlipped(false); setCombo(0); setSessionDone(0); }}
                  style={trainBtn('#0891b2', '#ecfeff', '#a5f3fc')}>
                  <span style={{ fontSize: '1.5rem' }}>⬜</span>
                  <span style={{ flex: 1 }}>
                    <b style={{ display: 'block', color: '#155e75' }}>빈칸 인출 {clozeQueue.length}문</b>
                    <span style={smallDesc}>정의문의 핵심어를 가리고 떠올리기</span>
                  </span>
                </button>
              )}
              {knowledge.cards.length >= 4 && (
                <button onClick={() => { setMode('mcq'); setIdx(0); setFlipped(false); setCombo(0); setSessionDone(0); }}
                  style={trainBtn('#d97706', '#fffbeb', '#fde68a')}>
                  <span style={{ fontSize: '1.5rem' }}>✅</span>
                  <span style={{ flex: 1 }}>
                    <b style={{ display: 'block', color: '#92400e' }}>4지선다 {queue.length}문</b>
                    <span style={smallDesc}>객관식으로 변환 — 1차 실전 형식으로 확인</span>
                  </span>
                </button>
              )}
              {knowledge.outline.length >= 3 && (
                <button onClick={() => { setMode('outline'); setRevealCnt(0); }}
                  style={trainBtn('#059669', '#ecfdf5', '#a7f3d0')}>
                  <span style={{ fontSize: '1.5rem' }}>🗺</span>
                  <span style={{ flex: 1 }}>
                    <b style={{ display: 'block', color: '#065f46' }}>목차 인출 {knowledge.outline.length}항목</b>
                    <span style={smallDesc}>이 단원의 뼈대를 순서대로 떠올리기 {mp.outlineDone && '✓'}</span>
                  </span>
                </button>
              )}
            </>
          )}

          {/* 교두보 — 전후 단계로 이동 */}
          <div style={{ display: 'flex', gap: 8, marginTop: 18 }}>
            <button onClick={() => onGoAI?.(subjectId, leaf)} style={bridgeBtn('#4f46e5')}>
              🤖 AI 학습으로<br /><span style={{ fontSize: '0.66rem', fontWeight: 600 }}>이해가 먼저라면</span>
            </button>
            <button onClick={() => onGoSolve?.(leaf)} disabled={!solveStats.total} style={bridgeBtn('#059669', !solveStats.total)}>
              ✍️ 문제풀이로<br /><span style={{ fontSize: '0.66rem', fontWeight: 600 }}>
                {solveStats.total ? `이 단원 ${solveStats.total}문 적용` : '연결된 문제 없음'}
              </span>
            </button>
          </div>
        </main>
      </div>
    );
  }

  // ── ✅ 4지선다 러너 — 카드 → 객관식 자동 변환 (정답 term + 같은 단원 오답 3) ──
  if (mode === 'mcq') {
    const card = queue[idx];
    if (!card) {
      return (
        <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh' }}>
          {header}
          <main className="main-content" style={{ marginTop: 40, textAlign: 'center' }}>
            <div style={{ fontSize: '2.2rem' }}>🎉</div>
            <div style={{ fontWeight: 800, marginTop: 8 }}>4지선다 완료! ({sessionDone}문)</div>
            <button onClick={() => { setMode('hub'); setIdx(0); }}
              style={{ marginTop: 18, padding: '11px 22px', borderRadius: 10, border: 'none',
                background: '#d97706', color: '#fff', fontWeight: 800, cursor: 'pointer' }}>
              훈련 선택으로
            </button>
          </main>
        </div>
      );
    }
    const stem = card.cloze || clozeText(card) || card.def.replace(card.term, '⬜⬜');
    // 보기: 정답 + 같은 단원 다른 term 3 (id 시드 셔플 — 같은 문제는 같은 배열)
    const others = knowledge.cards.filter(c => c.key !== card.key).map(c => c.term);
    const seed = (card.id || card.key).split('').reduce((s, ch) => s + ch.charCodeAt(0), 0);
    const opts = [card.term, ...others.sort((a, b) => ((a + seed).length % 3) - ((b + seed).length % 3)).slice(0, 3)]
      .sort((a, b) => ((a.charCodeAt(0) + seed) % 7) - ((b.charCodeAt(0) + seed) % 7));
    const picked = flipped; // flipped를 '선택한 보기' 저장으로 재사용 (string)
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh' }}>
        {header}
        <main className="main-content" style={{ marginTop: 14 }}>
          <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#9ca3af', marginBottom: 8 }}>
            ✅ 4지선다 · {idx + 1}/{queue.length}
          </div>
          <div style={{ background: '#fff', borderRadius: 14, padding: 18, marginBottom: 12,
            boxShadow: '0 2px 8px rgba(0,0,0,0.05)', fontSize: '0.95rem', lineHeight: 1.7, color: '#111827' }}>
            ⬜에 들어갈 것은?
            <div style={{ marginTop: 8, color: '#374151' }}>{stem}</div>
          </div>
          {opts.map((o, i) => {
            const isAns = o === card.term;
            const isSel = picked === o;
            let border = '#e5e7eb'; let bg = '#fff';
            if (picked) {
              if (isAns) { border = '#16a34a'; bg = '#f0fdf4'; }
              else if (isSel) { border = '#ef4444'; bg = '#fef2f2'; }
            }
            return (
              <button key={i} disabled={!!picked} data-mcq
                onClick={() => {
                  setFlipped(o);
                  timerRef.current = setTimeout(() => { grade(card, o === card.term); }, o === card.term ? 600 : 1100);
                }}
                style={{ display: 'block', width: '100%', textAlign: 'left', padding: '12px 14px',
                  marginBottom: 8, borderRadius: 12, border: `1.5px solid ${border}`, background: bg,
                  fontSize: '0.92rem', fontWeight: 600, color: '#1f2937',
                  cursor: picked ? 'default' : 'pointer' }}>
                {i + 1}. {o}
              </button>
            );
          })}
        </main>
      </div>
    );
  }

  // ── 카드/빈칸 러너 ──
  if (mode === 'cards' || mode === 'cloze') {
    const list = mode === 'cards' ? queue : clozeQueue;
    const card = list[idx];
    if (!card) {
      return (
        <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh' }}>
          {header}
          <main className="main-content" style={{ marginTop: 40, textAlign: 'center' }}>
            <div style={{ fontSize: '2.2rem' }}>🎉</div>
            <div style={{ fontWeight: 800, marginTop: 8 }}>한 바퀴 완료! ({sessionDone}장)</div>
            <div style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: 6 }}>
              ⚡ 암기 {memProgressOf(mem, leaf.id).pct}% — '모름' 카드는 10분 뒤 다시 나와요
            </div>
            <button onClick={() => { setMode('hub'); setIdx(0); }}
              style={{ marginTop: 18, padding: '11px 22px', borderRadius: 10, border: 'none',
                background: '#7c3aed', color: '#fff', fontWeight: 800, cursor: 'pointer' }}>
              훈련 선택으로
            </button>
          </main>
        </div>
      );
    }
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh' }}>
        {header}
        <main className="main-content" style={{ marginTop: 14 }}>
          <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#9ca3af', marginBottom: 8 }}>
            {mode === 'cards' ? '🃏 용어 카드' : '⬜ 빈칸 인출'} · {idx + 1}/{list.length}
          </div>
          <div onClick={() => setFlipped(f => !f)}
            style={{ background: '#fff', borderRadius: 16, padding: 22, minHeight: 240, cursor: 'pointer',
              border: `1.5px solid ${flipped ? '#a78bfa' : '#e5e7eb'}`, boxShadow: '0 4px 14px rgba(0,0,0,0.06)',
              display: 'flex', flexDirection: 'column' }}>
            {mode === 'cards' ? (
              <>
                <div style={{ fontWeight: 900, fontSize: '1.25rem', color: '#111827' }}>
                  {card.term}
                  {card.importance >= 3 && <span style={{ marginLeft: 8, fontSize: '0.75rem', color: '#d97706' }}>★ 핵심</span>}
                </div>
                {flipped
                  ? <div style={{ marginTop: 14, fontSize: '0.92rem', lineHeight: 1.7, color: '#374151' }}>{card.def}</div>
                  : <div style={{ marginTop: 'auto', paddingTop: 30, textAlign: 'center', color: '#7c3aed',
                      fontSize: '0.85rem', fontWeight: 700 }}>정의를 떠올려보세요<br />
                      <span style={{ color: '#9ca3af', fontWeight: 500, fontSize: '0.72rem' }}>(탭하면 공개)</span></div>}
              </>
            ) : (
              <>
                <div style={{ fontSize: '0.95rem', lineHeight: 1.75, color: '#374151' }}>
                  {flipped ? card.def : card.blanked}
                </div>
                {!flipped && <div style={{ marginTop: 'auto', paddingTop: 22, textAlign: 'center', color: '#0891b2',
                  fontSize: '0.85rem', fontWeight: 700 }}>⬜에 들어갈 말을 떠올려보세요<br />
                  <span style={{ color: '#9ca3af', fontWeight: 500, fontSize: '0.72rem' }}>(탭하면 공개)</span></div>}
                {flipped && <div style={{ marginTop: 12, fontWeight: 800, color: '#0891b2' }}>정답: {card.term}</div>}
              </>
            )}
          </div>
          {flipped ? (
            <>
            <div style={{ display: 'flex', gap: 8, marginTop: 14 }}>
              <button onClick={() => grade(card, false)} style={gradeBtn('#dc2626', '#fef2f2', '#fecaca')}>
                ✕ 모름<br /><span style={{ fontSize: '0.65rem' }}>10분 후</span>
              </button>
              <button onClick={() => grade(card, true)} style={gradeBtn('#059669', '#ecfdf5', '#a7f3d0')}>
                ✓ 알았다<br /><span style={{ fontSize: '0.65rem' }}>
                  {SRS_DAYS[Math.min(srs[card.key]?.box || 0, SRS_DAYS.length - 1)]}일 후</span>
              </button>
            </div>
            <button onClick={() => {
              if (!window.confirm('이 카드를 삭제할까요? (부실하거나 불필요한 카드 정리)')) return;
              if (card.id) removeChatCard(leaf.id, card.id);
              setFlipped(false); setIdx(i => i + 1);
            }}
              style={{ width: '100%', marginTop: 8, padding: '7px', borderRadius: 8, border: 'none',
                background: 'none', color: '#9ca3af', fontSize: '0.72rem', cursor: 'pointer' }}>
              🗑 부실 카드 삭제
            </button>
            </>
          ) : (
            <button onClick={() => setFlipped(true)}
              style={{ width: '100%', marginTop: 14, padding: '13px', borderRadius: 12, border: 'none',
                background: mode === 'cards' ? '#7c3aed' : '#0891b2', color: '#fff', fontWeight: 800,
                fontSize: '0.95rem', cursor: 'pointer' }}>
              정답 보기
            </button>
          )}
          <div style={{ marginTop: 10, textAlign: 'center', fontSize: '0.68rem', color: '#c2c8d0' }}>
            ⌨️ Space 정답 · ← 모름 · → 알았다
          </div>
        </main>
      </div>
    );
  }

  // ── 목차 인출 ──
  if (mode === 'outline') {
    const items = knowledge.outline;
    const allOpen = revealCnt >= items.length;
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', paddingBottom: 24 }}>
        {header}
        <main className="main-content" style={{ marginTop: 14 }}>
          <div style={{ fontSize: '0.85rem', color: '#065f46', background: '#ecfdf5',
            border: '1px solid #a7f3d0', borderRadius: 10, padding: '9px 13px', marginBottom: 12, lineHeight: 1.6 }}>
            🗺 이 단원의 뼈대 {items.length}개 — <b>먼저 머릿속으로 순서를 떠올린 뒤</b> 하나씩 확인하세요.
          </div>
          {items.map((o, i) => (
            <div key={i} style={{ padding: '9px 13px', marginBottom: 6, borderRadius: 10,
              paddingLeft: 13 + (o.level - 3) * 14,
              background: i < revealCnt ? '#fff' : '#e5e7eb',
              border: '1px solid #e5e7eb', fontSize: '0.86rem', fontWeight: o.level <= 3 ? 800 : 500,
              color: i < revealCnt ? '#111827' : 'transparent', userSelect: 'none',
              textShadow: i < revealCnt ? 'none' : '0 0 10px rgba(100,100,100,0.6)' }}>
              {i < revealCnt ? o.text : '●'.repeat(Math.min(14, o.text.length))}
            </div>
          ))}
          {!allOpen ? (
            <button onClick={() => setRevealCnt(n => n + 1)}
              style={{ width: '100%', marginTop: 10, padding: '13px', borderRadius: 12, border: 'none',
                background: '#059669', color: '#fff', fontWeight: 800, cursor: 'pointer' }}>
              다음 항목 공개 ({revealCnt}/{items.length})
            </button>
          ) : (
            <button onClick={() => { updateMem(leaf.id, { outlineDone: true }); setMode('hub'); }}
              style={{ width: '100%', marginTop: 10, padding: '13px', borderRadius: 12, border: 'none',
                background: '#065f46', color: '#fff', fontWeight: 800, cursor: 'pointer' }}>
              ✓ 목차 인출 완료
            </button>
          )}
        </main>
      </div>
    );
  }
  return null;
}

const trainBtn = (color, bg, border) => ({
  width: '100%', display: 'flex', alignItems: 'center', gap: 12, textAlign: 'left',
  padding: '14px 16px', marginBottom: 10, borderRadius: 14, cursor: 'pointer',
  border: `1.5px solid ${border}`, background: bg, fontSize: '0.92rem',
});
const smallDesc = { display: 'block', fontSize: '0.72rem', color: '#6b7280', marginTop: 2, fontWeight: 500 };
const gradeBtn = (color, bg, border) => ({
  flex: 1, padding: '13px', borderRadius: 12, border: `1px solid ${border}`,
  background: bg, color, fontWeight: 800, cursor: 'pointer',
});
const bridgeBtn = (color, disabled) => ({
  flex: 1, padding: '11px', borderRadius: 12, border: `1.5px solid ${color}44`,
  background: '#fff', color: disabled ? '#9ca3af' : color, fontWeight: 800, fontSize: '0.8rem',
  cursor: disabled ? 'default' : 'pointer', lineHeight: 1.5, opacity: disabled ? 0.6 : 1,
});
