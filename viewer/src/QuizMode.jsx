// ⚡ 드릴 탭 — AI 학습(배움)과 문제풀이(실전) 사이의 '체화' 단계.
// 관(款)을 더 잘게 쪼갠 '주제(좁은 개념)'를 저렴한 AI(Gemini Flash Lite)와
// 짧은 질문↔답↔피드백을 빠르게 왕복하며 인출·체화한다.
//   과목 → 단원(목차) → 주제(미리 추출/수동추가) → 드릴 세션(AI 질답)
// 주제: /data/drill/{subject}.json (로컬 LLM 추출) + drill-topics-custom-v1 (수동)
import { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Send, Plus, Sparkles } from 'lucide-react';
import { SUBJECTS, getApiKey as getProviderKey, getBaseUrls } from './aiLearningStore';
import { sendMessagesUnified, getProviderForModel, modelRequiresProxy } from './aiProviders';
import { sliceSection } from './aiClaudeClient';
import { toast } from './Toast';

const DRILL_MODEL = 'gemini-3.1-flash-lite';
const PROG_KEY = 'drill-progress-v1';      // { topicId: { status:'done'|'doing', exchanges, ts } }
const CUSTOM_KEY = 'drill-topics-custom-v1'; // { leafId: [{ id, title, hint, manual }] }

const indexUrl = (subjectId) => {
  const s = SUBJECTS.find((x) => x.id === subjectId);
  if (s?.stage === 2) return `/data/study/${subjectId}/ai_index.json`;
  return `/data/study/${subjectId}/ai_taxonomy_index.json`;
};
const studyBase = (subjectId) => `/data/study/${subjectId}/`;
const drillUrl = (subjectId) => `/data/drill/${subjectId}.json`;

const loadJSON = (k, d) => { try { return JSON.parse(localStorage.getItem(k) || JSON.stringify(d)) ?? d; } catch { return d; } };
const saveJSON = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* full */ } };

// ───────────────────────── browse-row (문제풀이와 동일 룩) ─────────────────────────
function splitRowPrefix(title) {
  const m = (title || '').match(/^(PART\s*\d+|Chapter\s*\d+|제\d+(?:장|절|관|편)|\d+절)\s+(.+)$/);
  if (m) return { prefix: m[1], rest: m[2] };
  return { prefix: null, rest: title };
}
function Row({ title, countLabel, pct, showBar, meta, onClick }) {
  const { prefix, rest } = splitRowPrefix(title);
  return (
    <button className="browse-row" onClick={onClick}>
      <div className="browse-row__main">
        <div className="browse-row__title">
          {prefix && <span className="browse-row__prefix">{prefix}</span>}
          {rest}
        </div>
        {showBar && <div className="browse-row__bar"><div style={{ width: `${Math.max(2, pct)}%` }} /></div>}
        {meta && <div style={{ fontSize: '0.7rem', color: '#9ca3af', marginTop: 5 }}>{meta}</div>}
      </div>
      <div className="browse-row__meta">
        {showBar && pct > 0 && <span className="browse-row__pct">{pct}%</span>}
        <span className="browse-row__count">{countLabel}</span>
        <span className="browse-row__chev">›</span>
      </div>
    </button>
  );
}

// ───────────────────────── 메인 ─────────────────────────
export default function MemorizeBridge({ onGoSolve, onGoAI }) {
  const [screen, setScreen] = useState('subjects'); // subjects | leaves | topics | drill
  const [subjectId, setSubjectId] = useState(null);
  const [leaves, setLeaves] = useState([]);
  const [leavesError, setLeavesError] = useState(false);
  const [pathStack, setPathStack] = useState([]);
  const [leaf, setLeaf] = useState(null);
  const [topic, setTopic] = useState(null);
  const [drillTopics, setDrillTopics] = useState({}); // 정적 추출분 {leafId:[...]}
  const [custom, setCustom] = useState(() => loadJSON(CUSTOM_KEY, {}));
  const [prog, setProg] = useState(() => loadJSON(PROG_KEY, {}));
  const leavesScrollRef = useRef(0);

  const subj = SUBJECTS.find((s) => s.id === subjectId);

  useEffect(() => {
    if (screen === 'leaves') window.scrollTo(0, leavesScrollRef.current || 0);
    else window.scrollTo(0, 0);
  }, [screen]);

  // 과목 진입 시: 목차 + 드릴 주제 로드
  useEffect(() => {
    if (!subjectId) return;
    let dead = false;
    setLeavesError(false);
    fetch(indexUrl(subjectId)).then((r) => { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
      .then((raw) => {
        if (dead) return;
        // 2차(ai_index)는 units 구조 → unit을 드릴 단원(leaf)으로 변환 (topic은 주제)
        let ls = raw?.leaves || raw || [];
        if (raw?.stage === 2 && Array.isArray(raw.units)) {
          ls = raw.units.map((u) => ({
            id: `${raw.subject_id}__${u.code}`, title: u.title, path: [u.title],
            unit_file: u.unit_file, section_key: 'full', section_lines: null,
          }));
        }
        setLeaves(Array.isArray(ls) ? ls : []);
      })
      .catch(() => { if (!dead) { setLeaves([]); setLeavesError(true); } });
    fetch(drillUrl(subjectId)).then((r) => r.ok ? r.json() : {})
      .then((d) => { if (!dead) setDrillTopics(d || {}); })
      .catch(() => { if (!dead) setDrillTopics({}); });
    return () => { dead = true; };
  }, [subjectId]);

  // leaf의 주제 = 정적 추출분 + 수동 추가분
  const topicsOf = (leafId) => [...(drillTopics[leafId] || []), ...((custom[leafId] || []))];
  const doneCount = (leafId) => topicsOf(leafId).filter((t) => prog[t.id]?.status === 'done').length;

  const markProg = (topicId, patch) => {
    setProg((prev) => { const next = { ...prev, [topicId]: { ...(prev[topicId] || {}), ...patch, ts: Date.now() } }; saveJSON(PROG_KEY, next); return next; });
  };
  const addCustomTopic = (leafId, title, hint) => {
    const t = { id: `custom-${Date.now()}`, title: title.trim(), hint: (hint || '').trim(), manual: true };
    setCustom((prev) => { const next = { ...prev, [leafId]: [...(prev[leafId] || []), t] }; saveJSON(CUSTOM_KEY, next); return next; });
  };
  const removeCustomTopic = (leafId, topicId) => {
    setCustom((prev) => { const next = { ...prev, [leafId]: (prev[leafId] || []).filter((t) => t.id !== topicId) }; saveJSON(CUSTOM_KEY, next); return next; });
  };

  // ── 화면 1: 과목 ──
  if (screen === 'subjects') {
    const T = { card: '#fff', ink: '#191F28', sub: '#8B95A1', track: '#E5E8EB', shadow: '0 2px 8px rgba(0,23,51,0.06)' };
    return (
      <div className="app-container" style={{ minHeight: '100dvh', paddingBottom: 24 }}>
        <div className="screen-head" style={{ paddingTop: 'calc(18px + env(safe-area-inset-top, 0px))' }}>
          <h1 className="screen-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ width: 34, height: 34, borderRadius: 10, background: '#eef2ff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Sparkles size={19} color="#4f46e5" />
            </span>
            AI 드릴
          </h1>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-sub,#64748b)', marginTop: 6, lineHeight: 1.5 }}>
            좁은 개념을 AI와 짧은 질답으로 체화해요 — <b>배움(AI 학습) → 체화(드릴) → 실전(문제풀이)</b>
          </p>
        </div>
        <main className="main-content" style={{ marginTop: 16 }}>
          {[
            { stage: 1, label: '1차 시험 — 객관식 5지선다', chipBg: '#E8F1FE', chipFg: '#3182F6', bar: '#3182F6' },
            { stage: 2, label: '2차 시험 — 서술형·답안 작성', chipBg: '#F0EBFF', chipFg: '#7C3AED', bar: '#7C3AED' },
          ].map(({ stage, label, chipBg, chipFg, bar }) => {
            const subjects = SUBJECTS.filter((s) => s.stage === stage);
            return (
              <div key={stage} style={{ marginBottom: 18 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
                  <div style={{ fontSize: '1rem', color: T.ink, fontWeight: 800 }}>{stage === 1 ? '📖' : '✍️'} {label}</div>
                  <span style={{ fontSize: '0.82rem', color: T.sub, fontWeight: 600 }}>{subjects.length}과목</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', rowGap: 14, columnGap: 12, alignItems: 'start' }}>
                  {subjects.map((s) => {
                    // 과목 완료 주제 수 — topicId가 subjectId로 시작
                    const done = Object.entries(prog).filter(([id, p]) => p?.status === 'done' && id.startsWith(s.id)).length;
                    return (
                      <div key={s.id} style={{ background: T.card, borderRadius: 20, boxShadow: T.shadow }}>
                        <button onClick={() => { setSubjectId(s.id); setPathStack([]); setScreen('leaves'); }}
                          style={{ padding: '20px 18px 16px', textAlign: 'left', background: 'none', border: 'none', cursor: 'pointer', width: '100%', display: 'flex', flexDirection: 'column', gap: 12 }}>
                          <div style={{ display: 'flex' }}>
                            <span style={{ fontSize: '0.7rem', fontWeight: 800, background: chipBg, color: chipFg, padding: '3px 9px', borderRadius: 999 }}>{stage === 1 ? '1차' : '2차'}</span>
                          </div>
                          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                            <div style={{ minWidth: 0, flex: 1 }}>
                              <div style={{ fontWeight: 800, color: T.ink, fontSize: '1.2rem', lineHeight: 1.3 }}>{s.short}</div>
                              <div style={{ fontSize: '0.82rem', color: T.sub, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', marginTop: 4 }}>{s.title}</div>
                            </div>
                            <div style={{ fontSize: '2rem', lineHeight: 1, flex: '0 0 auto' }}>{s.icon}</div>
                          </div>
                          <div style={{ fontSize: '0.8rem', color: done > 0 ? '#4f46e5' : T.sub, fontWeight: 600 }}>
                            {done > 0 ? `✓ ${done}개 주제 체화` : '드릴 시작하기'}
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

  // ── 화면 2: 단원 드릴다운 ──
  if (screen === 'leaves') {
    const under = leaves.filter((l) => pathStack.every((seg, i) => l.path?.[i] === seg));
    const depth = pathStack.length;
    const groupsMap = new Map();
    const leafRows = [];
    for (const l of under) {
      if ((l.path?.length || 0) === depth + 1) leafRows.push(l);
      else { const seg = l.path?.[depth]; if (!seg) continue; if (!groupsMap.has(seg)) groupsMap.set(seg, []); groupsMap.get(seg).push(l); }
    }
    const groupTopics = (ls) => ls.reduce((s, l) => s + topicsOf(l.id).length, 0);
    const groupDone = (ls) => ls.reduce((s, l) => s + doneCount(l.id), 0);
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', paddingBottom: 24 }}>
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => (depth === 0 ? setScreen('subjects') : setPathStack((p) => p.slice(0, -1)))}>
            <ArrowLeft size={24} style={{ marginRight: 8 }} />
            <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>{depth === 0 ? '과목' : '뒤로가기'}</span>
          </button>
        </header>
        <div className="screen-head">
          <div style={{ fontSize: '0.74rem', color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>
            {subj?.short} 드릴{pathStack.map((s, i) => <span key={i}> ▸ {s}</span>)}
          </div>
          <h1 className="screen-title">{subj?.icon} {pathStack.length ? pathStack[pathStack.length - 1] : subj?.title}</h1>
          <p style={{ fontSize: '0.78rem', color: '#6b7280', marginTop: 4 }}>단원 선택 — 그 안의 좁은 개념을 AI와 질답</p>
        </div>
        <main className="main-content" style={{ marginTop: 10 }}>
          {leaves.length === 0 && !leavesError && <div style={{ padding: 30, textAlign: 'center', color: '#9ca3af', fontSize: '0.85rem' }}>목차 불러오는 중…</div>}
          {leavesError && (
            <div style={{ padding: 26, textAlign: 'center', background: '#fff', borderRadius: 12, border: '1px solid #fecaca' }}>
              <div style={{ fontSize: '0.88rem', color: '#b91c1c', fontWeight: 700 }}>목차를 불러오지 못했어요</div>
              <button onClick={() => { const id = subjectId; setSubjectId(null); setTimeout(() => setSubjectId(id), 0); }}
                style={{ marginTop: 12, padding: '9px 20px', borderRadius: 9, border: 'none', background: '#2563eb', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>다시 시도</button>
            </div>
          )}
          {[...groupsMap.entries()].map(([seg, ls]) => {
            const tc = groupTopics(ls); const dc = groupDone(ls);
            return <Row key={seg} title={seg} countLabel={tc > 0 ? `주제 ${tc}` : `${ls.length}개 절`}
              pct={tc ? Math.round((dc / tc) * 100) : 0} showBar={dc > 0} onClick={() => setPathStack((p) => [...p, seg])} />;
          })}
          {leafRows.map((l) => {
            const tc = topicsOf(l.id).length; const dc = doneCount(l.id);
            return <Row key={l.id} title={l.title || l.path?.slice(-1)[0]}
              countLabel={tc > 0 ? `주제 ${tc}` : '주제 없음'}
              pct={tc ? Math.round((dc / tc) * 100) : 0} showBar={dc > 0}
              meta={tc > 0 ? `✓ 체화 ${dc}/${tc}` : null}
              onClick={() => { leavesScrollRef.current = window.scrollY; setLeaf(l); setScreen('topics'); }} />;
          })}
        </main>
      </div>
    );
  }

  // ── 화면 3: 주제 목록 ──
  if (screen === 'topics' && leaf) {
    const topics = topicsOf(leaf.id);
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', paddingBottom: 24 }}>
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => setScreen('leaves')}>
            <ArrowLeft size={24} style={{ marginRight: 8 }} />
            <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>단원 목록</span>
          </button>
        </header>
        <div className="screen-head">
          <h1 className="screen-title">{leaf.title || leaf.path?.slice(-1)[0]}</h1>
          <p style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: 4 }}>좁은 개념을 골라 AI와 질답으로 체화하세요</p>
        </div>
        <main className="main-content" style={{ marginTop: 12 }}>
          <AddTopic onAdd={(t, h) => addCustomTopic(leaf.id, t, h)} />
          {topics.length === 0 && (
            <div style={{ padding: 26, textAlign: 'center', background: '#fff', borderRadius: 12, marginTop: 10 }}>
              <div style={{ fontSize: '0.88rem', color: '#6b7280' }}>아직 추출된 주제가 없어요</div>
              <div style={{ fontSize: '0.76rem', color: '#9ca3af', marginTop: 4 }}>위 “+ 주제 추가”로 직접 만들거나, AI 학습에서 먼저 배우세요</div>
              {onGoAI && <button onClick={() => onGoAI(subjectId, leaf)}
                style={{ marginTop: 12, padding: '10px 18px', borderRadius: 10, border: 'none', background: '#4f46e5', color: '#fff', fontWeight: 800, cursor: 'pointer', fontSize: '0.84rem' }}>🤖 AI 학습으로 배우러 가기</button>}
            </div>
          )}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 10 }}>
            {topics.map((t, i) => {
              const st = prog[t.id]?.status;
              const badge = st === 'done' ? { t: '✓ 체화', c: '#059669', bg: '#ecfdf5' } : st === 'doing' ? { t: '진행중', c: '#d97706', bg: '#fffbeb' } : { t: '시작 전', c: '#9ca3af', bg: '#f3f4f6' };
              return (
                <div key={t.id} style={{ background: '#fff', borderRadius: 12, border: '1px solid #eef0f2', overflow: 'hidden' }}>
                  <button onClick={() => { setTopic(t); setScreen('drill'); }}
                    style={{ width: '100%', textAlign: 'left', padding: '14px 16px', background: 'none', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 10 }}>
                    <span style={{ width: 26, height: 26, borderRadius: 8, background: '#eef2ff', color: '#4f46e5', fontSize: '0.78rem', fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>{i + 1}</span>
                    <span style={{ flex: 1, minWidth: 0 }}>
                      <span style={{ display: 'block', fontWeight: 700, fontSize: '0.92rem', color: '#111827' }}>{t.title}</span>
                      {t.hint && <span style={{ display: 'block', fontSize: '0.76rem', color: '#9ca3af', marginTop: 2, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{t.hint}</span>}
                    </span>
                    <span style={{ fontSize: '0.68rem', fontWeight: 700, color: badge.c, background: badge.bg, padding: '3px 8px', borderRadius: 999, flexShrink: 0 }}>{badge.t}</span>
                    {t.manual && <button onClick={(e) => { e.stopPropagation(); removeCustomTopic(leaf.id, t.id); }} aria-label="주제 삭제"
                      style={{ border: 'none', background: 'none', color: '#d1d5db', cursor: 'pointer', fontSize: '0.9rem', padding: '0 2px' }}>✕</button>}
                  </button>
                </div>
              );
            })}
          </div>
        </main>
      </div>
    );
  }

  // ── 화면 4: 드릴 세션 ──
  if (screen === 'drill' && leaf && topic) {
    const topics = topicsOf(leaf.id);
    const idx = topics.findIndex((t) => t.id === topic.id);
    const nextTopic = idx >= 0 && idx + 1 < topics.length ? topics[idx + 1] : null;
    return (
      <DrillSession
        key={topic.id}
        subjectId={subjectId} leaf={leaf} topic={topic}
        onBack={() => setScreen('topics')}
        onProgress={(patch) => markProg(topic.id, patch)}
        nextTopic={nextTopic}
        onNext={() => { setTopic(nextTopic); }}
        onGoSolve={onGoSolve}
      />
    );
  }

  return null;
}

// ───────────────────────── 주제 추가 폼 ─────────────────────────
function AddTopic({ onAdd }) {
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [hint, setHint] = useState('');
  if (!open) {
    return (
      <button onClick={() => setOpen(true)}
        style={{ width: '100%', padding: '11px 14px', borderRadius: 12, border: '1px dashed #c4b5fd', background: '#faf5ff', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6, color: '#6d28d9', fontWeight: 700, fontSize: '0.85rem' }}>
        <Plus size={16} /> 주제 추가
      </button>
    );
  }
  const valid = title.trim().length >= 2;
  return (
    <div style={{ background: '#faf5ff', border: '1.5px solid #ddd6fe', borderRadius: 12, padding: 12 }}>
      <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="개념 제목 (예: 관습법 성립요건)"
        style={{ width: '100%', padding: '10px 12px', marginBottom: 8, border: '1px solid #d1d5db', borderRadius: 9, fontSize: '16px', boxSizing: 'border-box' }} />
      <input value={hint} onChange={(e) => setHint(e.target.value)} placeholder="인출 핵심 한 줄 (선택)"
        style={{ width: '100%', padding: '10px 12px', marginBottom: 10, border: '1px solid #d1d5db', borderRadius: 9, fontSize: '16px', boxSizing: 'border-box' }} />
      <div style={{ display: 'flex', gap: 8 }}>
        <button onClick={() => { setOpen(false); setTitle(''); setHint(''); }} style={{ flex: 1, padding: '10px', borderRadius: 9, border: '1px solid #d1d5db', background: '#fff', color: '#6b7280', fontWeight: 700, cursor: 'pointer' }}>취소</button>
        <button onClick={() => { if (valid) { onAdd(title, hint); setOpen(false); setTitle(''); setHint(''); } }} disabled={!valid}
          style={{ flex: 2, padding: '10px', borderRadius: 9, border: 'none', background: valid ? '#7c3aed' : '#d1d5db', color: '#fff', fontWeight: 800, cursor: valid ? 'pointer' : 'default' }}>추가</button>
      </div>
    </div>
  );
}

// ───────────────────────── 드릴 세션 (Gemini Flash Lite 질답) ─────────────────────────
function DrillSession({ subjectId, leaf, topic, onBack, onProgress, nextTopic, onNext, onGoSolve }) {
  const [messages, setMessages] = useState([]); // {role, content}
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);
  const [err, setErr] = useState('');
  const [sliceMd, setSliceMd] = useState('');
  const [started, setStarted] = useState(false);
  const abortRef = useRef(null);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  const apiKey = getProviderKey('google');
  const baseUrl = getBaseUrls().google;

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, busy]);

  // 교재 발췌 로드 (그 leaf의 슬라이스)
  useEffect(() => {
    let dead = false;
    if (!leaf.unit_file) { setSliceMd(''); return; }
    fetch(studyBase(subjectId) + leaf.unit_file).then((r) => r.text()).then((md) => {
      if (dead) return;
      // 주제(topic)에 자체 lines가 있으면(2차) 그 부분만, 아니면 leaf 슬라이스(1차)
      const sliced = topic.lines ? sliceSection(md, { lines: topic.lines })
        : (leaf.section_key && leaf.section_key !== 'full' && leaf.section_lines) ? sliceSection(md, { lines: leaf.section_lines }) : md;
      setSliceMd(sliced.slice(0, 6000));
    }).catch(() => { if (!dead) setSliceMd(''); });
    return () => { dead = true; };
  }, [subjectId, leaf]);

  const system = `너는 감정평가사 수험 드릴 코치다. 지금 다루는 좁은 개념은 "${topic.title}"이다.
${topic.hint ? `인출 핵심: ${topic.hint}` : ''}
아래 교재 발췌에만 근거해, 학생이 이 좁은 개념을 스스로 인출하도록 한 번에 하나의 짧은 질문을 던져라.
- 학생 답에 1~2문장으로 맞는지·보충 피드백을 준 뒤, 곧장 다음 짧은 질문.
- 질문은 이 좁은 개념 범위 안에서만. 길게 설명하지 말고 짧게 묻고 답을 끌어내라.
- 3~5회 문답이면 충분하다. 학생이 핵심을 인출했다고 판단되면 한 줄로 칭찬·정리하고
  마지막 줄에 정확히 [DRILL_DONE] 표식을 남겨라.
- 교재 발췌에 없는 내용은 묻지 마라. 답은 한국어, 군더더기 없이.

[교재 발췌]
${sliceMd || '(교재 자료 없음 — 주제 제목·핵심만으로 진행)'}`;

  const callAI = async (history) => {
    const ac = new AbortController();
    abortRef.current = ac;
    setBusy(true); setErr('');
    try {
      const { text } = await sendMessagesUnified({
        apiKey, model: DRILL_MODEL, system,
        messages: history.slice(-10).map((m) => ({ role: m.role, content: m.content })),
        maxTokens: 500, baseUrl, signal: ac.signal,
      });
      if (ac.signal.aborted) return;
      const isDone = /\[DRILL_DONE\]/.test(text);
      const clean = text.replace(/\[DRILL_DONE\]/g, '').trim();
      const fin = [...history, { role: 'assistant', content: clean }];
      setMessages(fin);
      onProgress({ status: isDone ? 'done' : 'doing', exchanges: fin.filter((m) => m.role === 'user').length });
      if (isDone) { setDone(true); try { toast.show('✅ 이 주제를 체화했어요!', 'success', 2200); } catch { /* noop */ } }
    } catch (e) {
      if (!ac.signal.aborted) {
        const proxyHint = modelRequiresProxy(DRILL_MODEL) ? ' (Gemini는 프록시가 필요할 수 있어요 — AI 학습 ⚙️ 설정에서 Google 프록시를 등록하세요)' : '';
        setErr((e.message || '요청 실패') + proxyHint);
      }
    } finally { setBusy(false); abortRef.current = null; }
  };

  // 첫 질문 자동 생성
  const begin = () => { setStarted(true); callAI([{ role: 'user', content: '이 개념 드릴을 시작해줘. 첫 질문을 던져줘.' }]); };
  const submit = () => {
    const t = input.trim(); if (!t || busy || done) return;
    const next = [...messages, { role: 'user', content: t }];
    setMessages(next); setInput('');
    callAI(next);
  };

  if (!apiKey) {
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh' }}>
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={onBack}><ArrowLeft size={24} style={{ marginRight: 8 }} /><span style={{ fontSize: '0.95rem', fontWeight: 600 }}>주제 목록</span></button>
        </header>
        <main className="main-content" style={{ marginTop: 40, textAlign: 'center' }}>
          <div style={{ fontSize: '2rem' }}>🔑</div>
          <div style={{ fontWeight: 800, marginTop: 10, color: '#111827' }}>Google API 키가 필요해요</div>
          <div style={{ fontSize: '0.84rem', color: '#6b7280', marginTop: 8, lineHeight: 1.6 }}>
            AI 드릴은 Gemini Flash Lite로 작동합니다.<br />AI 학습 탭 ⚙️ 설정에서 Google(Gemini) 키를 한 번만 등록하세요.
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', display: 'flex', flexDirection: 'column' }}>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', flexShrink: 0 }}>
        <button className="back-btn" onClick={() => { abortRef.current?.abort(); onBack(); }}>
          <ArrowLeft size={24} style={{ marginRight: 8 }} /><span style={{ fontSize: '0.95rem', fontWeight: 600 }}>주제 목록</span>
        </button>
      </header>
      <div style={{ padding: '12px 16px 8px', flexShrink: 0 }}>
        <div style={{ fontSize: '0.72rem', color: '#9ca3af', fontWeight: 600 }}>⚡ AI 드릴 · {leaf.title || leaf.path?.slice(-1)[0]}</div>
        <div style={{ fontSize: '1.05rem', fontWeight: 800, color: '#111827', marginTop: 2 }}>{topic.title}</div>
        {topic.hint && <div style={{ fontSize: '0.76rem', color: '#7c3aed', marginTop: 2 }}>{topic.hint}</div>}
      </div>
      <main className="main-content" style={{ flex: 1, marginTop: 0, overflowY: 'auto', paddingBottom: 12 }}>
        {!started && (
          <div style={{ textAlign: 'center', padding: '30px 16px' }}>
            <div style={{ fontSize: '0.86rem', color: '#6b7280', lineHeight: 1.6, marginBottom: 16 }}>
              AI가 이 개념에 대해 짧은 질문을 던집니다.<br />한 줄로 답하면 즉시 피드백하고 다음 질문으로 넘어가요.
            </div>
            <button onClick={begin} disabled={busy}
              style={{ padding: '12px 26px', borderRadius: 12, border: 'none', background: '#4f46e5', color: '#fff', fontWeight: 800, fontSize: '0.92rem', cursor: 'pointer' }}>
              {busy ? '준비 중…' : '드릴 시작 →'}
            </button>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} style={{ display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start', marginBottom: 10 }}>
            <div style={{ maxWidth: '82%', padding: '10px 14px', borderRadius: 14, fontSize: '0.92rem', lineHeight: 1.6,
              background: m.role === 'user' ? '#4f46e5' : '#fff', color: m.role === 'user' ? '#fff' : '#1f2937',
              border: m.role === 'user' ? 'none' : '1px solid #eef0f2', whiteSpace: 'pre-wrap' }}>
              {m.content}
            </div>
          </div>
        ))}
        {busy && <div style={{ color: '#9ca3af', fontSize: '0.84rem', padding: '4px 8px' }}>✨ 생각 중…</div>}
        {err && <div style={{ color: '#dc2626', fontSize: '0.82rem', padding: '8px', background: '#fef2f2', borderRadius: 10, marginTop: 6 }}>{err}</div>}
        {done && (
          <div style={{ textAlign: 'center', padding: '16px 8px' }}>
            <div style={{ fontSize: '1.6rem' }}>🎉</div>
            <div style={{ fontWeight: 800, color: '#059669', margin: '6px 0 14px' }}>이 주제 체화 완료!</div>
            <div style={{ display: 'flex', gap: 8, justifyContent: 'center', flexWrap: 'wrap' }}>
              {nextTopic && <button onClick={() => { setMessages([]); setDone(false); setStarted(false); onNext(); }}
                style={{ padding: '11px 20px', borderRadius: 10, border: 'none', background: '#4f46e5', color: '#fff', fontWeight: 800, cursor: 'pointer' }}>다음 주제 →</button>}
              {onGoSolve && <button onClick={() => onGoSolve(leaf)}
                style={{ padding: '11px 20px', borderRadius: 10, border: '1px solid #bbf7d0', background: '#fff', color: '#059669', fontWeight: 800, cursor: 'pointer' }}>✍️ 실전 문제 풀기</button>}
              <button onClick={onBack} style={{ padding: '11px 20px', borderRadius: 10, border: '1px solid #d1d5db', background: '#fff', color: '#6b7280', fontWeight: 700, cursor: 'pointer' }}>주제 목록</button>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </main>
      {started && !done && (
        <div style={{ flexShrink: 0, padding: '8px 12px 12px', background: '#f8fafc', borderTop: '1px solid #eef0f2' }}>
          <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end' }}>
            <textarea ref={inputRef} value={input} onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); submit(); } }}
              placeholder="한 줄로 답해보세요 (Enter 전송)" rows={1} disabled={busy}
              style={{ flex: 1, border: '1.5px solid #c7d2fe', borderRadius: 14, padding: '11px 14px', fontSize: '16px', fontFamily: 'inherit', resize: 'none', outline: 'none', boxSizing: 'border-box' }} />
            <button onClick={submit} disabled={busy || !input.trim()} aria-label="전송"
              style={{ flexShrink: 0, width: 44, height: 44, borderRadius: 12, border: 'none', background: input.trim() && !busy ? '#4f46e5' : '#e5e7eb', color: '#fff', cursor: input.trim() && !busy ? 'pointer' : 'default', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Send size={18} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
