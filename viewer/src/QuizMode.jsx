// ⚡ 드릴 탭 — AI 학습(배움)과 문제풀이(실전) 사이의 '체화' 단계.
// 관(款)을 더 잘게 쪼갠 '주제(좁은 개념)'를 저렴한 AI(Gemini Flash Lite)와
// 짧은 질문↔답↔피드백을 빠르게 왕복하며 인출·체화한다.
//   과목 → 단원(목차) → 주제(미리 추출/수동추가) → 드릴 세션(AI 질답)
// 주제: /data/drill/{subject}.json (로컬 LLM 추출) + drill-topics-custom-v1 (수동)
import { useState, useEffect, useRef, useMemo } from 'react';
import { ArrowLeft, Send, Plus, Sparkles } from 'lucide-react';
import { SUBJECTS, getApiKey as getProviderKey, getBaseUrls, getRoleModel, getPrefs } from './aiLearningStore';
import { sendMessagesUnified, getProviderForModel, modelRequiresProxy } from './aiProviders';
import { resolveCall } from './modelRegistry';
import { sliceSection } from './aiClaudeClient';
import ParsedText from './ParsedText';
import SubjectIcon from './SubjectIcon';
import UnitOutline from './UnitOutline';
import { questionsInLeaf, AI_SUBJECT_TO_QUIZ } from './leafStats';
import { loadPassInsights, drillInsightHint } from './passInsights';
import { drillReviewDue, buildLearnerStatus } from './studyDrill';
import { getMistakeSummary, getNoteEntries, MISTAKE_TYPES } from './studyMeta';
import { loadExamFreq, TIER_META, tierRank } from './examFreq';
import { toast } from './Toast';

// 🃏 드릴에서 만든 두문자/트리거를 암기카드(quiz-chatcards-v1)로 적재 — SRS·오늘복습·퀴즈와 연동.
const CHATCARDS_KEY = 'quiz-chatcards-v1';
function saveDrillCard(leafId, card) {
  try {
    const all = JSON.parse(localStorage.getItem(CHATCARDS_KEY) || '{}') || {};
    const arr = all[leafId] || [];
    if (arr.some((c) => c.term === card.term)) return; // 중복 방지
    arr.push(card);
    all[leafId] = arr.slice(-200);
    localStorage.setItem(CHATCARDS_KEY, JSON.stringify(all));
  } catch { /* quota */ }
}

// 🎯 '내 실제 약점' 블록 — 이 학생이 실제로 틀린 것을 드릴 프롬프트에 주입해
// 구별·인출을 '범용 함정'이 아니라 학생의 진짜 혼동 지점으로 겨냥한다.
function buildMyWeakness(subjectId, leaf, topic) {
  const parts = [];
  // 1) 이 과목에서 자주 하는 실수 유형(퀴즈 오답 태그) — 과목 키 매칭, 없으면 전체 폴백
  const subjKey = SUBJECTS.find((s) => s.id === subjectId)?.tax_key || '';
  let summ = getMistakeSummary(subjKey);
  if (!Object.keys(summ).length) summ = getMistakeSummary();
  const mtypes = Object.entries(summ).sort((a, b) => b[1] - a[1]).slice(0, 3);
  if (mtypes.length) {
    const label = (k) => (MISTAKE_TYPES.find((t) => t.key === k) || {}).label || k;
    parts.push(`[이 학생이 자주 하는 실수] ${mtypes.map(([k, n]) => `${label(k)} ${n}회`).join(' · ')} — 이 함정을 특히 파고들어라.`);
  }
  // 2) 최근 오답노트(과목 필터, 없으면 전체) — 학생 본인의 말
  let notes = getNoteEntries(subjKey);
  if (!notes.length) notes = getNoteEntries();
  notes = notes.slice(-3);
  if (notes.length) {
    parts.push('[학생이 직접 쓴 최근 오답노트]');
    notes.forEach((n) => parts.push(`  - "${(n.t || '').slice(0, 120)}"`));
  }
  // 3) 이 관에서 실제로 틀린 문항(드릴 문항 기록) — leaf 범위, 가장 정확
  const ls = buildLearnerStatus(leaf?.id, leaf?.title); // '' 또는 '## 학습자 성적…' 블록
  let block = '';
  if (parts.length) block += `\n\n## 내 실제 약점 (범용 함정 말고, 내가 실제로 틀린 아래 지점을 콕 집어 구별·인출시켜라)\n${parts.join('\n')}`;
  if (ls) block += (block ? '\n' : '\n\n') + ls;
  return block;
}

const DRILL_MODEL = 'moonshot:kimi-k2.6'; // 드릴 기본(역할 미설정 시). 로컬은 느려서 기본에서 제외.
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
function TierBadge({ tier }) {
  const m = tier && TIER_META[tier];
  if (!m) return null;
  return (
    <span title="기출 출제량 기준 중요도(과목 내 상대)"
      style={{ fontSize: '0.6rem', fontWeight: 800, color: m.color, background: m.bg, border: `1px solid ${m.bd}`, borderRadius: 6, padding: '1px 5px', flexShrink: 0, verticalAlign: 'middle', marginLeft: 6 }}>
      {m.label}
    </span>
  );
}
function Row({ title, countLabel, pct, showBar, meta, tier, onClick }) {
  const { prefix, rest } = splitRowPrefix(title);
  return (
    <button className="browse-row" onClick={onClick}>
      <div className="browse-row__main">
        <div className="browse-row__title">
          {prefix && <span className="browse-row__prefix">{prefix}</span>}
          {rest}
          <TierBadge tier={tier} />
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
export default function MemorizeBridge({ onGoSolve, onGoSubjectPractice, onGoAI, initialJump, onJumpConsumed, leavesBySubject = {}, classifiedList = [], progress = {}, qid = (q) => q.id }) {
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
  const [freqMap, setFreqMap] = useState({}); // 🔥 기출 출제량 → 중요도 A~D급 배지 { leafId: {n, tier} }
  const leavesScrollRef = useRef(0);

  const subj = SUBJECTS.find((s) => s.id === subjectId);

  // 📝 이 과목 저품질 연습문제(문제풀이에서 분리된) — leaf별 개수. 경로 prefix 누적으로 O(문항수) 1회 집계.
  const practiceByLeaf = useMemo(() => {
    const m = {};
    const subjName = AI_SUBJECT_TO_QUIZ[subjectId];
    if (!subjName || !leaves.length) return m;
    const counts = new Map();
    for (const q of classifiedList) {
      if (!q.lowq || q.taxSubjectName !== subjName) continue;
      const path = [q.taxSubSubjectName, q.taxChapterName, q.taxSectionName, q.taxItemName].filter(Boolean);
      for (let i = 1; i <= path.length; i++) {
        const k = path.slice(0, i).join('|');
        counts.set(k, (counts.get(k) || 0) + 1);
      }
    }
    for (const l of leaves) m[l.id] = counts.get((l.path || []).join('|')) || 0;
    return m;
  }, [classifiedList, leaves, subjectId]);

  // 🔥 기출 빈도(중요도) 맵 — 과목 바뀔 때 로드
  useEffect(() => {
    if (!subjectId) { setFreqMap({}); return; }
    let dead = false;
    loadExamFreq(subjectId).then((m) => { if (!dead) setFreqMap(m || {}); });
    return () => { dead = true; };
  }, [subjectId]);

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

  // 외부 딥링크(오답·약점 → 이 개념 드릴): subjectId 로드 후 해당 leaf의 주제 화면으로 점프
  useEffect(() => {
    if (!initialJump?.leafId) return;
    if (subjectId !== initialJump.subjectId) { setSubjectId(initialJump.subjectId); setPathStack([]); return; }
    if (leavesError) { onJumpConsumed && onJumpConsumed(); return; } // 인덱스 로드 실패 → 소비(안 하면 stale jump가 네비 하이재킹)
    if (!leaves.length) return; // leaf 목록 로드 대기
    // 1차는 정확 매칭. 2차는 딥링크 leafId가 topic 단위(subject__code__topicId)일 수 있어
    // 드릴 leaf(subject__code)와 안 맞음 → 앞 2토막(단원 prefix)으로 폴백.
    const unitId = initialJump.leafId.split('__').slice(0, 2).join('__');
    const found = leaves.find((l) => l.id === initialJump.leafId) || leaves.find((l) => l.id === unitId);
    if (found) { setLeaf(found); setTopic(null); setScreen('topics'); }
    onJumpConsumed && onJumpConsumed(); // 성공/실패 무관 1회 소비
  }, [initialJump, subjectId, leaves, leavesError]);

  // leaf의 주제 = 정적 추출분 + 수동 추가분
  const topicsOf = (leafId) => [...(drillTopics[leafId] || []), ...((custom[leafId] || []))];
  const doneCount = (leafId) => topicsOf(leafId).filter((t) => prog[t.id]?.status === 'done').length;

  const markProg = (topicId, patch) => {
    setProg((prev) => {
      const cur = prev[topicId] || {};
      let extra = {};
      // 🔁 체화 완료 시: 회독수(box)를 올리고 기억곡선 간격으로 다음 복습 도래를 잡는다(회독 드릴).
      if (patch.status === 'done') {
        const box = Math.min(4, (cur.box || 0) + 1);
        extra = { box, reps: (cur.reps || 0) + 1, due: drillReviewDue(box) };
      }
      const next = { ...prev, [topicId]: { ...cur, ...patch, ...extra, ts: Date.now() } };
      saveJSON(PROG_KEY, next); return next;
    });
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
            AI 질답으로 개념을 체화하고 · <b style={{ color: '#7c3aed' }}>연습문제</b>로 굳혀요 — 배움(AI 학습) → 체화·연습(드릴) → 실전 기출(문제풀이)
          </p>
        </div>
        <main className="main-content" style={{ marginTop: 16 }}>
          {[
            { stage: 1, label: '1차 시험 — 객관식 5지선다', chipBg: '#E8F1FE', chipFg: '#3182F6', bar: '#3182F6' },
            { stage: 2, label: '2차 시험 — 서술형·답안 작성', chipBg: '#F0EBFF', chipFg: '#7C3AED', bar: '#7C3AED' },
          ].map(({ stage, label, chipBg, chipFg, bar }) => {
            const subjects = stage === 1
              ? ['accounting', 'economics', 'civil', 'realestate', 'law'].map((id) => SUBJECTS.find((s) => s.id === id)).filter(Boolean)
              : SUBJECTS.filter((s) => s.stage === stage);
            return (
              <div key={stage} style={{ marginBottom: 18 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
                  <div style={{ fontSize: '1rem', color: T.ink, fontWeight: 800 }}>{stage === 1 ? '📖' : '✍️'} {label}</div>
                  <span style={{ fontSize: '0.82rem', color: T.sub, fontWeight: 600 }}>{subjects.length}과목</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', rowGap: 14, columnGap: 12, alignItems: 'stretch' }}>
                  {subjects.map((s) => {
                    // 과목 완료 주제 수 — 정적 주제 id는 subjectId로 시작하지만, 수동 주제 id는
                    // 'custom-…'라 prefix로 안 잡힌다. 해당 과목 leaf 아래 커스텀 주제 id도 포함.
                    const customIds = new Set();
                    Object.entries(custom).forEach(([lid, arr]) => {
                      if (lid.startsWith(s.id)) (arr || []).forEach((t) => customIds.add(t.id));
                    });
                    const done = Object.entries(prog).filter(([id, p]) => p?.status === 'done' && (id.startsWith(s.id) || customIds.has(id))).length;
                    // 세부과목(path[0]) 칩 — AI 학습·문제풀이와 동일. 2~4개면 카드에 노출.
                    const divs = [];
                    { const seen = new Set(); for (const l of (leavesBySubject[s.id] || [])) { const top = l.path && l.path[0]; if (top && !seen.has(top)) { seen.add(top); divs.push(top); } } }
                    { const ORD = ({ accounting: ['회계원리', '재무회계', '원가관리회계', '고급회계'], economics: ['미시경제학', '거시경제학', '국제경제학', '재정학'], civil: ['민법총칙', '물권총론', '소유권', '제한물권'], realestate: ['부동산학원론', '감정평가론'] })[s.id]; if (ORD) divs.sort((a, b) => (ORD.indexOf(a) + 1 || 99) - (ORD.indexOf(b) + 1 || 99)); }
                    const showDivs = stage === 1 && divs.length >= 2 && divs.length <= 4;
                    return (
                      <div key={s.id} style={{ background: T.card, borderRadius: 20, boxShadow: T.shadow, display: 'flex', flexDirection: 'column' }}>
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
                            <div style={{ flex: '0 0 auto', display: 'flex', alignItems: 'center' }}><SubjectIcon id={s.id} size={30} color="#8B95A1" /></div>
                          </div>
                          <div style={{ fontSize: '0.8rem', color: done > 0 ? '#4f46e5' : T.sub, fontWeight: 600 }}>
                            {done > 0 ? `✓ ${done}개 주제 체화` : '드릴 시작하기'}
                          </div>
                        </button>
                        {showDivs && (
                          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6, padding: '0 18px 16px', marginTop: 'auto' }}>
                            {divs.map((top) => (
                              <button key={top} onClick={() => { setSubjectId(s.id); setPathStack([top]); setScreen('leaves'); }} title={top}
                                style={{ padding: '11px 6px', fontSize: '0.84rem', fontWeight: 700, background: chipBg, color: chipFg, border: 'none', borderRadius: 10, cursor: 'pointer', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', textAlign: 'center' }}>
                                {top}
                              </button>
                            ))}
                          </div>
                        )}
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
    const divFilter = pathStack[0] || null;
    const visLeaves = divFilter ? leaves.filter((l) => l.path?.[0] === divFilter) : leaves;
    // 📝 이 과목 저품질 연습문제 전체 수(단원 미매핑분 포함) — 단원 배지 합보다 많을 수 있다.
    const subjName = AI_SUBJECT_TO_QUIZ[subjectId];
    const subjLowTotal = subjName ? classifiedList.reduce((n, q) => n + (q.taxSubjectName === subjName && q.lowq ? 1 : 0), 0) : 0;
    // 🔁 회독 드릴 — 체화 후 기억곡선 간격이 도래한 주제(이 과목). 재드릴하면 box(회독)↑.
    const nowTs = Date.now();
    const dueReviews = [];
    for (const l of leaves) for (const t of topicsOf(l.id)) {
      const p = prog[t.id];
      if (p && p.status === 'done' && p.due && p.due <= nowTs) dueReviews.push({ l, t });
    }
    // 우선순위: 빈출(기출 A급) → 약점(덜 회독한 box 낮은 것) → 오래 밀린(due 지난) 순
    dueReviews.sort((a, b) =>
      tierRank(freqMap[b.l.id]?.tier) - tierRank(freqMap[a.l.id]?.tier)
      || (prog[a.t.id]?.box || 0) - (prog[b.t.id]?.box || 0)
      || (prog[a.t.id]?.due || 0) - (prog[b.t.id]?.due || 0));
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', paddingBottom: 24 }}>
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => (divFilter ? setPathStack([]) : setScreen('subjects'))}>
            <ArrowLeft size={24} style={{ marginRight: 8 }} />
            <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>{divFilter ? '전체 단원' : '과목'}</span>
          </button>
        </header>
        <div className="screen-head">
          <div style={{ fontSize: '0.74rem', color: '#9ca3af', fontWeight: 600, marginBottom: 4 }}>
            {subj?.short} 드릴{divFilter ? <span> ▸ {divFilter}</span> : null}
          </div>
          <h1 className="screen-title">{subj?.icon} {divFilter || subj?.title}</h1>
          <p style={{ fontSize: '0.78rem', color: '#6b7280', marginTop: 4 }}>단원을 고르면 AI 질답 체화 + <b style={{ color: '#7c3aed' }}>📝 연습문제</b> 풀이 · <b style={{ color: '#4361ee' }}>#숫자</b> = 과목 내 학습 순서</p>
          {Object.keys(freqMap).length > 0 && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 6, fontSize: '0.68rem', color: '#94a3b8' }}>
              <TierBadge tier="A" /> <span>= 기출 다출제(빈출) · 과목 내 상대 중요도</span>
            </div>
          )}
        </div>
        <main className="main-content" style={{ marginTop: 10 }}>
          {subjLowTotal > 0 && onGoSubjectPractice && (
            <button onClick={() => onGoSubjectPractice(subjectId)}
              style={{ width: '100%', textAlign: 'left', display: 'flex', alignItems: 'center', gap: 12, background: '#fff', border: '1px solid #ede9fe', borderRadius: 14, padding: '13px 16px', marginBottom: 12, cursor: 'pointer', boxShadow: '0 1px 6px rgba(124,58,237,0.06)' }}>
              <span style={{ width: 38, height: 38, borderRadius: 11, background: '#f5f3ff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.15rem', flexShrink: 0 }}>📝</span>
              <span style={{ flex: 1, minWidth: 0 }}>
                <span style={{ display: 'block', fontWeight: 800, fontSize: '0.92rem', color: '#111827' }}>{subj?.short} 연습문제 전체 {subjLowTotal.toLocaleString()}개</span>
                <span style={{ display: 'block', fontSize: '0.72rem', color: '#7c3aed', marginTop: 2 }}>단원에 안 잡히는 문제까지 한 번에 풀기</span>
              </span>
              <span style={{ fontSize: '1.1rem', color: '#7c3aed', flexShrink: 0 }}>›</span>
            </button>
          )}
          {leaves.length === 0 && !leavesError && <div style={{ padding: 30, textAlign: 'center', color: '#9ca3af', fontSize: '0.85rem' }}>목차 불러오는 중…</div>}
          {leavesError && (
            <div style={{ padding: 26, textAlign: 'center', background: '#fff', borderRadius: 12, border: '1px solid #fecaca' }}>
              <div style={{ fontSize: '0.88rem', color: '#b91c1c', fontWeight: 700 }}>목차를 불러오지 못했어요</div>
              <button onClick={() => { const id = subjectId; setSubjectId(null); setTimeout(() => setSubjectId(id), 0); }}
                style={{ marginTop: 12, padding: '9px 20px', borderRadius: 9, border: 'none', background: '#2563eb', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>다시 시도</button>
            </div>
          )}
          {dueReviews.length > 0 && (
            <div style={{ background: '#fff', border: '1px solid #ddd6fe', borderRadius: 12, padding: '10px 12px', marginBottom: 12 }}>
              <div style={{ fontSize: '0.8rem', fontWeight: 800, color: '#6d28d9', marginBottom: 7 }}>🔁 복습 드릴 {dueReviews.length}개 도래 <span style={{ fontWeight: 600, color: '#a5a3c9', fontSize: '0.68rem' }}>· 기억곡선 회독</span></div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
                {dueReviews.slice(0, 8).map(({ l, t }) => (
                  <button key={t.id} onClick={() => { setLeaf(l); setTopic(t); setScreen('drill'); }}
                    style={{ display: 'flex', alignItems: 'center', gap: 8, textAlign: 'left', background: '#f5f3ff', border: '1px solid #ede9fe', borderRadius: 9, padding: '7px 10px', cursor: 'pointer' }}>
                    <span style={{ fontSize: '0.6rem', fontWeight: 800, color: '#6d28d9', background: '#ede9fe', borderRadius: 6, padding: '2px 6px', flexShrink: 0 }}>{prog[t.id]?.box || 1}회독</span>
                    <span style={{ flex: 1, minWidth: 0, fontSize: '0.8rem', fontWeight: 700, color: '#1e293b', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{t.title}<TierBadge tier={freqMap[l.id]?.tier} /></span>
                    <span style={{ fontSize: '0.9rem', color: '#7c3aed', flexShrink: 0 }}>›</span>
                  </button>
                ))}
              </div>
              {dueReviews.length > 8 && <div style={{ fontSize: '0.7rem', color: '#94a3b8', marginTop: 5 }}>외 {dueReviews.length - 8}개</div>}
            </div>
          )}
          {leaves.length > 0 && !leavesError && (
            <div style={{ background: '#fff', borderRadius: 14, boxShadow: '0 1px 6px rgba(15,23,42,0.06)', border: '1px solid #eef0f3', padding: '6px 6px 8px' }}>
              <UnitOutline
                leaves={visLeaves}
                onPick={(l) => { leavesScrollRef.current = window.scrollY; setLeaf(l); setScreen('topics'); }}
                renderMeta={(l) => { const tc = topicsOf(l.id).length; const dc = doneCount(l.id); const pc = practiceByLeaf[l.id] || 0; return (
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 7 }}>
                    {tc > 0
                      ? <span style={{ fontSize: '0.68rem', fontWeight: 700, color: dc >= tc ? '#16a34a' : '#94a3b8' }}>{dc > 0 ? `체화 ${dc}/${tc}` : `주제 ${tc}`}</span>
                      : <span style={{ fontSize: '0.66rem', color: '#cbd5e1' }}>주제 없음</span>}
                    {pc > 0 && <span style={{ fontSize: '0.66rem', fontWeight: 800, color: '#7c3aed', background: '#f5f3ff', border: '1px solid #ede9fe', borderRadius: 6, padding: '1px 6px' }}>📝 연습 {pc}</span>}
                  </span>); }}
                tierBadge={(l) => <TierBadge tier={freqMap[l.id]?.tier} />}
              />
            </div>
          )}
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
          {(() => {
            // 📝 이 단원 저품질 연습문제 — 문제풀이에서 분리돼 드릴에서만 푼다.
            const practice = questionsInLeaf(classifiedList, leaf).filter((q) => q.lowq);
            if (!practice.length || !onGoSolve) return null;
            const answered = practice.reduce((n, q) => { const p = progress[qid(q)]; return n + (p && p.correct != null ? 1 : 0); }, 0);
            const pct = Math.round((answered / practice.length) * 100);
            return (
              <button onClick={() => onGoSolve(leaf)}
                style={{ width: '100%', textAlign: 'left', display: 'flex', alignItems: 'center', gap: 12, background: '#fff', border: '1px solid #ede9fe', borderRadius: 14, padding: '14px 16px', marginBottom: 12, cursor: 'pointer', boxShadow: '0 1px 6px rgba(124,58,237,0.06)' }}>
                <span style={{ width: 40, height: 40, borderRadius: 12, background: '#f5f3ff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem', flexShrink: 0 }}>📝</span>
                <span style={{ flex: 1, minWidth: 0 }}>
                  <span style={{ display: 'block', fontWeight: 800, fontSize: '0.95rem', color: '#111827' }}>연습문제 {practice.length}개 풀기</span>
                  <span style={{ display: 'block', fontSize: '0.74rem', color: '#7c3aed', marginTop: 2 }}>{answered > 0 ? `${answered}/${practice.length}문항 풀이 · ${pct}%` : '이 단원 실전 감각을 굳혀요'}</span>
                </span>
                <span style={{ fontSize: '1.1rem', color: '#7c3aed', flexShrink: 0 }}>›</span>
              </button>
            );
          })()}
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
        onProgress={(patch) => markProg(topic.id, patch.status === 'done' ? { ...patch, leafId: leaf.id, topicTitle: topic.title, subjectId } : patch)}
        nextTopic={nextTopic}
        onNext={() => { setTopic(nextTopic); }}
        onGoSolve={onGoSolve}
        practiceCount={practiceByLeaf[leaf.id] || 0}
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
function DrillSession({ subjectId, leaf, topic, onBack, onProgress, nextTopic, onNext, onGoSolve, practiceCount = 0 }) {
  const [messages, setMessages] = useState([]); // {role, content}
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);
  const [err, setErr] = useState('');
  const [sliceMd, setSliceMd] = useState('');
  const [started, setStarted] = useState(false);
  const [pInsights, setPInsights] = useState(null); // 🎓 합격수기 기반 인출법
  useEffect(() => { loadPassInsights().then((d) => { if (d) setPInsights(d); }); }, []);
  const [drillMode, setDrillMode] = useState('default'); // default | outline | distinguish | mention | precedent
  const abortRef = useRef(null);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  // 드릴 모델 = 역할('drill') 라우팅. 미설정이면 'AI 학습'과 같은 모델(prefs.model)로 폴백해 통일감 유지.
  // (예전엔 Kimi로 폴백해서, AI 학습만 작동하는 모델로 바꾼 사용자는 드릴이 죽었음)
  const drillModel = (getPrefs() && getPrefs().model) || getRoleModel('drill', null) || DRILL_MODEL;
  const { apiKey, baseUrl, needsKey } = resolveCall(drillModel);
  const is2cha = SUBJECTS.find((s) => s.id === subjectId)?.stage === 2; // 2차=논술, 1차=객관식

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

  const commonHead = `이번 드릴에서 다루는 좁은 개념은 오직 "${topic.title}" 하나다.
${topic.hint ? `인출 핵심: ${topic.hint}` : ''}
[목표] 학생이 '보고 아는' 수준이 아니라 '안 보고 스스로 떠올리는(인출)' 수준이 되게 한다. 강의하지 마라 — 너는 묻는 사람이고, 떠올리는 건 학생이다.`;
  // 🎯 학생 실제 오답 — 구별/인출을 진짜 혼동 지점으로 겨냥(세션 내 고정)
  const myWeakness = useMemo(() => buildMyWeakness(subjectId, leaf, topic), [subjectId, leaf?.id, topic?.id]);
  const tail = `[피드백 — 짧고 정직하게] 맞으면 한 줄 인정 + 빠진 키워드 보강. 틀리거나 빠지면 "무엇이 빠졌는지"를 1~2문장으로 정확히 짚어라(칭찬만 X). 가능하면 떠올리기 쉬운 트리거 키워드 2~3개나 두문자로 묶어줘라("이 단어만 보면 ~가 떠오르게").
모든 질문·피드백은 아래 교재 발췌 범위 안에서만, 한국어로 군더더기 없이.

[교재 발췌]
${sliceMd || '(교재 자료 없음 — 주제 제목·핵심만으로 진행)'}${drillInsightHint(pInsights, subjectId, is2cha ? 2 : 1)}${myWeakness}`;

  // 체화 완료 시 두문자/트리거를 암기카드로 남긴다(합격 암기법 loop). 앞면=두문자·트리거, 뒷면=풀어낸 핵심.
  const cardRule = `이어서 딱 한 줄로 정확히 "[CARD] 앞면 || 뒷면" 형식의 암기카드를 하나 만들어라(앞면=트리거 키워드나 두문자, 뒷면=그걸 풀어낸 핵심 한 줄). 그 다음 줄에 정확히 [DRILL_DONE]. 아직이면 계속 물어라.`;
  // 드릴 모드별 [질문 가이드 + 마무리]. 마무리는 '…정리하고 '로 끝내 cardRule 로 이어진다. (합격수기 기반)
  const MODE_BODY = {
    outline: `[목차 인출 모드] 목표는 학생이 이 쟁점 '답안의 전체 목차(뼈대)'를 안 보고 처음부터 끝까지 빠짐없이 세우는 것이다('목차만 외워도 70점' — 합격자 공통).
· 먼저 "이 쟁점이 나오면 답안 목차를 큰 것부터 빠짐없이 세워봐"라고 요청(내용 서술 말고 목차 뼈대만).
· 학생 목차를 교재 근거 '표준 목차'와 대조해 (✓맞은)/(✗빠진) 목차를 나열하고 완성도 "맞은수/전체수"를 매 라운드 알려줘라. 빠진 목차를 다시 세우게 유도.
[마무리] 학생이 표준 목차를 (거의) 빠짐없이 완주하면 '목차 뼈대 한 줄 + 두문자'로 정리하고 `,
    distinguish: `[구별 드릴 모드] 목표는 '헷갈리는 옆 개념'과의 경계를 정확히 인출시키는 것이다(1차 오답의 핵심).
· 교재 발췌에서 이 개념과 혼동되는 옆 개념을 골라 "A와 B가 어떻게 다른가", "이 진술은 A인가 B인가?"로 콕 집어 구별시켜라. 3~5회, 매번 빠진 차이를 파고든다.
[마무리] 학생이 핵심 차이·경계를 정확히 인출하면 'A vs B 한 줄 구별 포인트'로 정리하고 `,
    mention: `[실무 멘트 인출 모드] 목표는 이 논점 상황에서 답안에 쓸 '득점 멘트·적용 조문·유의사항'을 스스로 떠올리는 것이다(계산 아님, 'A상황=A멘트' — 합격자 실무 공통).
· "이런 상황이면 답안에 뭐라고 쓸까 — 핵심 멘트·근거 조문·유의사항"을 인출시켜라. 빠진 멘트·조문을 정확히 짚어라. 3~5회.
[마무리] 학생이 핵심 멘트·조문을 인출하면 '멘트 트리거 + 근거 조문'으로 정리하고 `,
    precedent: `[판례 인출 모드] 목표는 이 논점의 핵심 판례를 '결과'가 아니라 '취지·논거'와 근거 조문까지 인출하는 것이다(법규 합격 공통).
· "이 논점의 판례는? 결과 말고 그 '취지·논거'와 근거 조문까지 떠올려봐"로 인출시켜라. (판례 번호는 지어내지 말 것.) 3~5회.
[마무리] 학생이 판례 취지·논거·조문을 인출하면 '판례 취지 한 줄 + 두문자'로 정리하고 `,
    default2: `2차는 객관식이 아니라 답안지에 직접 쓰는 시험이다. 핵심은 "백지에 목차·논점·근거를 안 보고 쓸 수 있는가"이다.
[질문 — 한 번에 하나, 짧게. 답을 질문 안에 흘리지 마라]
· 목차형: "이 쟁점이 출제되면 답안 목차(뼈대)를 떠올려봐 — 의의 → 논점/요건 → 근거 → 결론"
· 의의·키워드형: "이 개념의 의의를 답안용 한 줄 + 하위 핵심 키워드 2~3개"
· 근거형: "이 결론을 무슨 조문·판례 논거로 뒷받침하나?" (결론만이면 부족)
· 적용형: "이런 상황이면 어떤 논점을 꺼내 쓰나?" (실무는 'A상황=A멘트')
유형을 섞어 3~5회. 매 답을 보고 빠진 목차·논거를 파고든다.
[마무리] 학생이 목차를 세우고 핵심 의의·근거까지 인출하면 '목차 키워드 + 핵심 근거'로 정리하고 `,
    default1: `[질문 — 한 번에 하나, 짧게. 보기·정답 노출 X]
· 인출형: "정의/요건/효과/구조를 스스로 떠올려봐" (열린 질문)
· 구별형: 헷갈리는 옆 개념과 "A와 B가 어떻게 다른가" (1차 오답의 핵심)
· 함정형: 한 줄 진술을 주고 "맞나 틀리나? 왜?" (조건 일부만 바꾼 함정)
세 유형을 섞어 3~5회. 매 답을 보고 약한 곳을 파고든다.
[마무리] 학생이 핵심을 인출하고 구별·함정 판별까지 하면 '트리거 키워드 2~3개'로 정리하고 `,
  };
  const roleLabel = is2cha ? "감정평가사 2차(논술 답안) 수험 '드릴 코치'" : "감정평가사 1차 수험 '드릴 코치'";
  const body = is2cha ? (MODE_BODY[drillMode] || MODE_BODY.default2)
    : (drillMode === 'distinguish' ? MODE_BODY.distinguish : MODE_BODY.default1);
  const system = `너는 ${roleLabel}다. ${commonHead}
${body}${cardRule}

${tail}`;

  const callAI = async (history) => {
    const ac = new AbortController();
    abortRef.current = ac;
    setBusy(true); setErr('');
    try {
      const { text } = await sendMessagesUnified({
        apiKey, model: drillModel, system,
        messages: history.slice(-10).map((m) => ({ role: m.role, content: m.content })),
        maxTokens: 500, baseUrl, signal: ac.signal,
      });
      if (ac.signal.aborted) return;
      const isDone = /\[DRILL_DONE\]/.test(text);
      // 🃏 [CARD] 앞면 || 뒷면 → 암기카드(quiz-chatcards-v1)로 저장하고 화면 표시에선 제거
      const cm = text.match(/\[CARD\]\s*(.+?)\s*\|\|\s*(.+?)\s*(?:\[DRILL_DONE\]|\n|$)/);
      if (cm && leaf?.id) {
        const term = cm[1].trim().slice(0, 120);
        const def = cm[2].replace(/\[DRILL_DONE\]/g, '').trim().slice(0, 400);
        if (term && def) {
          saveDrillCard(leaf.id, { id: `drill-${topic.id}-${Date.now()}`, term, def, cloze: '', type: '암기' });
          try { toast.show('🃏 암기카드로 저장했어요', 'success', 2000); } catch { /* noop */ }
        }
      }
      const clean = text.replace(/\[CARD\][^\n]*/g, '').replace(/\[DRILL_DONE\]/g, '').trim();
      const fin = [...history, { role: 'assistant', content: clean }];
      setMessages(fin);
      onProgress({ status: isDone ? 'done' : 'doing', exchanges: fin.filter((m) => m.role === 'user').length });
      if (isDone) { setDone(true); try { toast.show('✅ 이 주제를 체화했어요!', 'success', 2200); } catch { /* noop */ } }
    } catch (e) {
      if (!ac.signal.aborted) {
        const proxyHint = needsKey && modelRequiresProxy(drillModel) ? ' (프록시가 필요할 수 있어요 — AI 학습 ⚙️ 설정에서 프록시를 등록하세요)' : '';
        setErr((e.message || '요청 실패') + proxyHint);
      }
    } finally { setBusy(false); abortRef.current = null; }
  };

  // 첫 질문 자동 생성
  const BEGIN_MSG = {
    outline: '목차 인출 시작. 이 쟁점 답안의 전체 목차(뼈대)를 큰 것부터 빠짐없이 세워볼게 — 목차만 세우도록 요청해줘.',
    distinguish: '구별 드릴 시작. 이 개념과 헷갈리는 옆 개념을 콕 집어 A vs B로 구별시켜줘.',
    mention: '실무 멘트 인출 시작. 이 논점 상황에서 답안에 쓸 멘트·조문·유의사항을 떠올리게 해줘.',
    precedent: '판례 인출 시작. 이 논점 판례의 취지·논거·근거 조문을 떠올리게 해줘.',
  };
  const begin = () => { setStarted(true); callAI([{ role: 'user', content: BEGIN_MSG[drillMode] || '드릴 시작. 설명·요약 말고, 이 개념을 내가 스스로 떠올리게 하는 짧은 인출 질문 하나로 바로 시작해줘.' }]); };
  const submit = () => {
    const t = input.trim(); if (!t || busy || done) return;
    const next = [...messages, { role: 'user', content: t }];
    setMessages(next); setInput('');
    callAI(next);
  };

  if (needsKey && !apiKey) {
    return (
      <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh' }}>
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={onBack}><ArrowLeft size={24} style={{ marginRight: 8 }} /><span style={{ fontSize: '0.95rem', fontWeight: 600 }}>주제 목록</span></button>
        </header>
        <main className="main-content" style={{ marginTop: 40, textAlign: 'center' }}>
          <div style={{ fontSize: '2rem' }}>🔑</div>
          <div style={{ fontWeight: 800, marginTop: 10, color: '#111827' }}>드릴 모델의 API 키가 필요해요</div>
          <div style={{ fontSize: '0.84rem', color: '#6b7280', marginTop: 8, lineHeight: 1.6 }}>
            현재 드릴 모델(<b>{drillModel}</b>)은 클라우드 키가 필요합니다.<br />
            AI 학습 ⚙️ 설정에서 키를 등록하거나, <b>🖥 로컬(Ollama) 모델</b>로 바꾸면 무료로 씁니다.
          </div>
        </main>
      </div>
    );
  }

  return (
    // 고정 높이(하단 탭바 64px 예약) + main minHeight:0 — 안 그러면 입력창이 고정탭 아래로
    // 가리고 main 이 내부 스크롤되지 않는다(AILearning 채팅과 동일 패턴).
    <div className="app-container" style={{ background: '#f8fafc', height: 'calc(100dvh - 64px - env(safe-area-inset-bottom, 0px))', display: 'flex', flexDirection: 'column' }}>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', flexShrink: 0 }}>
        <button className="back-btn" onClick={() => { abortRef.current?.abort(); onBack(); }}>
          <ArrowLeft size={24} style={{ marginRight: 8 }} /><span style={{ fontSize: '0.95rem', fontWeight: 600 }}>주제 목록</span>
        </button>
      </header>
      <div style={{ padding: '10px 16px', flexShrink: 0, background: '#fff', borderBottom: '1px solid #eef0f2' }}>
        <div style={{ fontSize: '0.72rem', color: '#9ca3af', fontWeight: 600 }}>⚡ AI 드릴 · {leaf.title || leaf.path?.slice(-1)[0]}</div>
        <div style={{ fontSize: '1.05rem', fontWeight: 800, color: '#111827', marginTop: 2 }}>{topic.title}</div>
        {topic.hint && <div style={{ fontSize: '0.76rem', color: '#7c3aed', marginTop: 2 }}>{topic.hint}</div>}
      </div>
      <main className="main-content" style={{ flex: 1, minHeight: 0, marginTop: 0, overflowY: 'auto', paddingBottom: 12 }}>
        {!started && (() => {
          const MODE_META = {
            default: { label: '기본', color: '#4f46e5', go: '드릴 시작 →', desc: <>AI가 이 개념에 대해 짧은 질문을 던집니다.<br />한 줄로 답하면 즉시 피드백하고 다음 질문으로 넘어가요.</> },
            outline: { label: '🧩 목차', color: '#7c3aed', go: '목차 인출 시작 →', desc: <>답안 <b>목차(뼈대)를 백지로</b> 세우면 표준 목차와 대조해<br />빠진 목차·완성도를 짚어줍니다. (합격자: 목차만 외워도 70점)</> },
            distinguish: { label: '🔀 구별', color: '#0891b2', go: '구별 드릴 시작 →', desc: <>헷갈리는 <b>옆 개념과의 차이</b>를 콕 집어 구별시킵니다.<br />(1차 오답의 핵심)</> },
            mention: { label: '✍️ 멘트', color: '#c2410c', go: '멘트 인출 시작 →', desc: <>상황을 주고 답안에 쓸 <b>득점 멘트·조문·유의사항</b>을<br />스스로 떠올리게 합니다.</> },
            precedent: { label: '⚖️ 판례', color: '#b45309', go: '판례 인출 시작 →', desc: <>논점의 <b>판례 취지·논거·근거 조문</b>을<br />스스로 인출하게 합니다.</> },
          };
          const avail = is2cha
            ? (subjectId === 'appraisal_practice' ? ['default', 'outline', 'mention']
              : subjectId === 'appraisal_law' ? ['default', 'outline', 'precedent']
              : ['default', 'outline'])
            : ['default', 'distinguish'];
          const mm = MODE_META[drillMode] || MODE_META.default;
          return (
            <div style={{ textAlign: 'center', padding: '30px 16px' }}>
              <div style={{ fontSize: '0.86rem', color: '#6b7280', lineHeight: 1.6, marginBottom: 16 }}>{mm.desc}</div>
              {myWeakness && (
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: 5, fontSize: '0.72rem', fontWeight: 700, color: '#0e7490', background: '#ecfeff', border: '1px solid #cffafe', borderRadius: 999, padding: '4px 11px', marginBottom: 16 }}>
                  🎯 내 오답·실수 패턴을 반영해 겨냥합니다
                </div>
              )}
              {avail.length > 1 && (
                <div style={{ display: 'flex', gap: 6, justifyContent: 'center', flexWrap: 'wrap', marginBottom: 16 }}>
                  {avail.map((k) => { const on = drillMode === k; const meta = MODE_META[k]; return (
                    <button key={k} onClick={() => setDrillMode(k)}
                      style={{ padding: '6px 13px', borderRadius: 999, cursor: 'pointer', fontWeight: 800, fontSize: '0.76rem',
                        border: on ? `1.5px solid ${meta.color}` : '1px solid #e5e7eb', background: on ? '#f8fafc' : '#fff', color: on ? meta.color : '#94a3b8' }}>{meta.label}</button>
                  ); })}
                </div>
              )}
              <button onClick={begin} disabled={busy}
                style={{ padding: '12px 26px', borderRadius: 12, border: 'none', background: mm.color, color: '#fff', fontWeight: 800, fontSize: '0.92rem', cursor: 'pointer' }}>
                {busy ? '준비 중…' : mm.go}
              </button>
            </div>
          );
        })()}
        {/* 말풍선 — AI 학습(대화형 학습)과 동일한 채팅 디자인 언어 */}
        {messages.map((m, i) => {
          const isUser = m.role === 'user';
          const fadeIn = i === messages.length - 1 && !isUser && !busy;
          return (
            <div key={i} className={fadeIn ? 'ai-msg-fade' : ''}
              style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', margin: '8px 0' }}>
              <div style={{
                maxWidth: isUser ? '78%' : '98%',
                padding: '12px 16px', borderRadius: 14,
                background: isUser ? '#4f46e5' : '#f3f4f6',
                color: isUser ? '#fff' : '#111827',
                fontSize: '0.95rem', lineHeight: 1.6,
                whiteSpace: 'pre-wrap', wordBreak: 'break-word',
              }}>
                {isUser ? m.content : <ParsedText text={m.content} />}
              </div>
            </div>
          );
        })}
        {busy && (
          <div style={{ display: 'flex', justifyContent: 'flex-start', margin: '8px 0' }}>
            <div style={{ padding: '12px 16px', borderRadius: 14, background: '#f3f4f6', color: '#9ca3af', fontSize: '0.92rem' }}>
              ✨ 생각 중…
            </div>
          </div>
        )}
        {err && <div style={{ color: '#dc2626', fontSize: '0.82rem', padding: '8px', background: '#fef2f2', borderRadius: 10, marginTop: 6 }}>{err}</div>}
        {done && (
          <div style={{ textAlign: 'center', padding: '16px 8px' }}>
            <div style={{ fontSize: '1.6rem' }}>🎉</div>
            <div style={{ fontWeight: 800, color: '#059669', margin: '6px 0 14px' }}>이 주제 체화 완료!</div>
            <div style={{ display: 'flex', gap: 8, justifyContent: 'center', flexWrap: 'wrap' }}>
              {nextTopic && <button onClick={() => { setMessages([]); setDone(false); setStarted(false); onNext(); }}
                style={{ padding: '11px 20px', borderRadius: 10, border: 'none', background: '#4f46e5', color: '#fff', fontWeight: 800, cursor: 'pointer' }}>다음 주제 →</button>}
              {onGoSolve && practiceCount > 0 && <button onClick={() => onGoSolve(leaf)}
                style={{ padding: '11px 20px', borderRadius: 10, border: '1px solid #ddd6fe', background: '#fff', color: '#7c3aed', fontWeight: 800, cursor: 'pointer' }}>📝 연습문제 {practiceCount}개 풀기</button>}
              <button onClick={onBack} style={{ padding: '11px 20px', borderRadius: 10, border: '1px solid #d1d5db', background: '#fff', color: '#6b7280', fontWeight: 700, cursor: 'pointer' }}>주제 목록</button>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </main>
      {started && !done && (
        <div style={{ flexShrink: 0, padding: '10px 16px 14px', background: '#f8fafc', borderTop: '1px solid #eef0f2' }}>
          <div style={{ display: 'flex', gap: 6, alignItems: 'flex-end' }}>
            <textarea ref={inputRef} value={input} onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); submit(); } }}
              placeholder="한 줄로 답해보세요 (Enter 전송, Shift+Enter 줄바꿈)" rows={2} disabled={busy}
              style={{ flex: 1, padding: '10px 12px', border: '1px solid #d1d5db', borderRadius: 10, fontSize: '16px', fontFamily: 'inherit', resize: 'none', outline: 'none', boxSizing: 'border-box', background: busy ? '#f9fafb' : '#fff' }} />
            {busy ? (
              <button onClick={() => { abortRef.current?.abort(); setBusy(false); }}
                style={{ padding: '10px 14px', background: '#fef2f2', color: '#991b1b', border: '1px solid #fecaca', borderRadius: 10, cursor: 'pointer', fontWeight: 700 }}>중단</button>
            ) : (
              <button onClick={submit} disabled={!input.trim()} aria-label="전송"
                style={{ padding: '10px 14px', background: input.trim() ? '#4f46e5' : '#e5e7eb', color: input.trim() ? '#fff' : '#9ca3af', border: 'none', borderRadius: 10, cursor: input.trim() ? 'pointer' : 'not-allowed', display: 'flex', alignItems: 'center', gap: 4, fontWeight: 700 }}>
                <Send size={16} />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
