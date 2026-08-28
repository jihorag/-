// AI 학습 탭 — Claude 대화형 과외 + 진척 추적 + 일별 대화 기록.
// 단원 체계: viewer/public/data/taxonomy.json 의 민법 트리(과목→장→절→관)와 동일.
// 각 leaf(관/절/장)는 교재 단원 MD의 슬라이스로 매핑됨 → 학습/문제풀이/둘러보기 단원 축이 단일.
//
// 위험·검토(#8) 반영:
//  - BYOK: API 키는 localStorage 단일 기기.
//  - 일일 메시지 cap 기본 50.
//  - section_lines 슬라이스 + prompt caching → 토큰 절약.
//  - 환각 방지 system rules.
//  - 오프라인 안내.

/* eslint-disable react-hooks/set-state-in-effect */
/* eslint-disable react-refresh/only-export-components */
import { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { Send, BookOpen, RotateCcw, ChevronDown, ChevronLeft, ChevronRight, Calendar, Sparkles, Key, Search, Trash2, Play, BarChart3, ArrowRight, Download, Upload, Settings,
  RefreshCw, Lightbulb, Flag, FileText, Shuffle, CheckCircle2, Brain, AlertTriangle, GitCompare, Zap, Bookmark, ListOrdered, Target, Activity, ClipboardList, HelpCircle, Calculator, SkipForward, PenLine, Layers,
  PencilLine, Timer, Compass } from 'lucide-react';
import ParsedText from './ParsedText';
import SubjectIcon from './SubjectIcon';
import {
  getByok, setByok, getPrefs, setPrefs,
  getCurrent, setCurrent,
  getMastery, getChapterMastery, updateChapterMastery,
  modeToPhase, MASTERY_PHASES, PHASE_LABEL,
  recordGrade, recordAnswerScore, getDueChapters,
  getSessions, addSession, updateSession,
  getRoomMessages, appendRoomMessage, popRoomMessage, clearRoom, getAllRooms,
  buildRoomExport, parseRoomImport, importRoomMessages,
  bumpUsage, canSendMessage, getUsage,
  pruneOldConversations,
  addAssessment,
  resetLearningProgress,
  migrateLegacyCivilIds,
  addMock, getMocks,
  SUBJECTS, SUBJECTS_BY_STAGE, getSubjectMeta,
  getApiKey, getBaseUrls, setApiKey, setBaseUrl,
  appendAnswer,
  getMsgRatings, rateMsg, addNote, getNotes,
  markActiveToday,
} from './aiLearningStore';
import { buildPersonalNotes, personalNoteStats } from './studyMeta';
import { useScrollLock, useEscClose } from './uiHooks';
import AnswerHistoryWidget from './AnswerHistoryWidget';
import { SpeakButton } from './Speech';
import { buildSystemBlocks, sliceSection, sliceLectureNote, stripNoteComments, stripLectureCitations, mergeLectureIntoDoc, splitLectureByTab, classifyDocHeading, extractJsonBlocks, MODELS } from './aiClaudeClient';
import { loadPassInsights, passInsightBlock } from './passInsights';

// AI가 로직용으로 붙이는 ```json 마커(채점·진단·분개·선행)는 화면에서 숨긴다.
const stripAiMarkers = (s) => (s || '').replace(/```json[\s\S]*?```/g, '').trim();

// 교재 슬라이스를 탭별로 분리 — "#### ✅ OX 확인문제" / "#### 🧠 암기법" 헤딩을 만나면
// 그 아래 내용을 해당 탭으로 보낸다. 관 제목급(###)을 만나면 다시 이론으로 복귀.
export function splitDocTabs(md) {
  const empty = { theory: '', ox: '', mem: '', law: '', prac: '', std: '' };
  if (!md) return empty;
  const buckets = { theory: [], ox: [], mem: [], law: [], prac: [], std: [] };
  let cur = 'theory';
  for (const line of md.split('\n')) {
    const h = line.match(/^(#{2,4})\s*(.*)$/);
    if (h) {
      const title = h[2];
      // 갈라내는 규칙은 aiClaudeClient 의 classifyDocHeading 한 곳에 있다.
      // 강의 필기 배정(splitLectureByTab)도 같은 규칙을 써야 필기가 같은 탭으로 간다.
      const tab = classifyDocHeading(title);
      // 특수 섹션 제목 줄은 탭 이름이 대신하므로 본문에서 뺀다.
      // 특수 섹션에 해당하지 않는 헤딩을 만나면 이론으로 되돌린다.
      // level<=3 만 리셋하면, 관 중간에 있는 `#### 📐 기준서 원문` 뒤의 모든 절
      // (요건표·분개·재무제표·계산예제·기출포인트)이 기준서 탭으로 새어 들어간다.
      cur = tab;
      if (tab !== 'theory') continue;
    }
    buckets[cur].push(line);
  }
  return {
    theory: buckets.theory.join('\n').trim(),
    ox: buckets.ox.join('\n').trim(),
    mem: buckets.mem.join('\n').trim(),
    law: buckets.law.join('\n').trim(),
    prac: buckets.prac.join('\n').trim(),
    std: buckets.std.join('\n').trim(),
  };
}

// OX 지문 파싱 — "**1.** 지문" 다음 줄의 "→ ..." 를 정답·해설로 묶는다.
function parseOX(md) {
  const items = [];
  const intro = [];
  let cur = null;
  for (const line of (md || '').split('\n')) {
    const q = line.match(/^\s*\*\*(\d+)\.\*\*\s*(.*)$/);
    if (q) {
      if (cur) items.push(cur);
      cur = { no: q[1], q: [q[2]], a: [] };
      continue;
    }
    if (/^\s*→/.test(line)) {
      if (cur) cur.a.push(line.replace(/^\s*→\s*/, ''));
      continue;
    }
    if (cur) (cur.a.length ? cur.a : cur.q).push(line);
    else intro.push(line);
  }
  if (cur) items.push(cur);
  return {
    intro: intro.join('\n').trim(),
    items: items.map((it) => ({ no: it.no, q: it.q.join('\n').trim(), a: it.a.join('\n').trim() })),
  };
}

// OX 확인문제 — 정답은 가려두고 클릭하면 드러난다. 초기화로 다시 전부 가림.
// 해설 첫머리의 `**O**.` / `**X**.` 에서 정답을 읽는다.
const oxAnswerOf = (a) => {
  const m = String(a || '').match(/^\s*\*\*\s*([OXox])\s*\*\*/);
  return m ? m[1].toUpperCase() : null;
};

function OXQuiz({ md }) {
  const { intro, items } = useMemo(() => parseOX(md), [md]);
  const [picked, setPicked] = useState({});   // { [i]: 'O' | 'X' }
  const [shown, setShown] = useState({});
  useEffect(() => { setShown({}); setPicked({}); }, [md]);   // 관이 바뀌면 자동 초기화
  if (!items.length) return <ParsedText text={md} />;
  const graded = items.map((it, i) => {
    const ans = oxAnswerOf(it.a);
    const p = picked[i];
    return p && ans ? p === ans : null;
  });
  const answered = graded.filter((g) => g !== null).length;
  const right = graded.filter((g) => g === true).length;
  const btn = {
    fontSize: '0.72rem', fontWeight: 700, padding: '4px 9px', borderRadius: 6,
    border: '1px solid #d6d3d1', background: '#fff', color: '#57534e', cursor: 'pointer',
  };
  const pick = (i, v, it) => {
    if (picked[i]) return;                       // 한 번 답하면 고정 — 기록의 신뢰도를 지킨다
    const ans = oxAnswerOf(it.a);
    setPicked((s) => ({ ...s, [i]: v }));
    setShown((s) => ({ ...s, [i]: true }));      // 답하면 해설을 바로 연다
    if (ans) recordItem({ kind: 'ox', idx: i, q: it.q, isCorrect: v === ans });
  };
  const choiceBtn = (on, tone) => ({
    fontSize: '0.82rem', fontWeight: 800, width: 38, height: 30, borderRadius: 6, cursor: 'pointer',
    border: '1.5px solid ' + (on ? tone : '#dcd8d3'),
    background: on ? tone : '#fff', color: on ? '#fff' : '#78716c',
  });
  return (
    <>
      {intro && <ParsedText text={intro} />}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, margin: '12px 0 4px', flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.75rem', fontWeight: 800, color: answered === items.length ? '#4d7c5f' : '#a8a29e' }}>
          {answered} / {items.length} 풀이
          {answered > 0 && <span style={{ color: '#57534e' }}> · 정답 {right} ({Math.round((right / answered) * 100)}%)</span>}
        </span>
        <button style={{ ...btn, marginLeft: 'auto' }} onClick={() => { setShown({}); setPicked({}); }}>🔄 초기화</button>
        <button style={btn} onClick={() => setShown(Object.fromEntries(items.map((_, i) => [i, true])))}>👁 모두 보기</button>
      </div>
      {items.map((it, i) => {
        const g = graded[i];
        return (
          <div key={i} style={{ borderTop: '1px solid #eeecea', padding: '12px 0 4px' }}>
            <div style={{ display: 'flex', gap: 8, alignItems: 'baseline' }}>
              <span style={{ fontWeight: 800, color: '#78716c', flexShrink: 0 }}>{it.no}.</span>
              <div style={{ flex: 1, minWidth: 0 }}><ParsedText text={it.q} /></div>
            </div>
            <div style={{ display: 'flex', gap: 6, alignItems: 'center', margin: '6px 0 2px' }}>
              <button style={choiceBtn(picked[i] === 'O', '#4d7c5f')} onClick={() => pick(i, 'O', it)}>O</button>
              <button style={choiceBtn(picked[i] === 'X', '#9a3412')} onClick={() => pick(i, 'X', it)}>X</button>
              {g !== null && (
                <span style={{ fontSize: '0.75rem', fontWeight: 800, color: g ? '#4d7c5f' : '#9a3412' }}>
                  {g ? '✓ 정답' : '✗ 오답'}
                </span>
              )}
              {g === null && !shown[i] && (
                <span style={{ fontSize: '0.72rem', color: '#a8a29e' }}>먼저 답해 보세요</span>
              )}
            </div>
            <div
              onClick={() => setShown((s) => ({ ...s, [i]: !s[i] }))}
              title={shown[i] ? '다시 가리기' : '클릭하여 정답 확인'}
              style={{ position: 'relative', cursor: 'pointer', marginTop: 2, borderRadius: 6,
                background: shown[i] ? (g === false ? '#fbf7f5' : '#f7f9f7') : '#f5f5f4', padding: '7px 10px', minHeight: 34 }}
            >
              <div style={{ filter: shown[i] ? 'none' : 'blur(5px)', opacity: shown[i] ? 1 : 0.55,
                userSelect: shown[i] ? 'auto' : 'none', transition: 'filter .15s, opacity .15s', pointerEvents: 'none' }}>
                <ParsedText text={it.a} />
              </div>
              {!shown[i] && (
                <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '0.73rem', fontWeight: 700, color: '#78716c', letterSpacing: '0.02em' }}>
                  클릭하여 정답 확인
                </div>
              )}
            </div>
          </div>
        );
      })}
    </>
  );
}
import { recordItem, setActiveLeaf, buildLearnerStatus, getDrillQueue, getDrillCounts } from './studyDrill';
import DailyDrill from './DailyDrill';
import { sendMessagesUnified, getProviderForModel } from './aiProviders';
import { discoverLocalModels } from './modelRegistry';
import { isTauri } from './tauriShim';
import { toast } from './Toast';

const indexUrl = (subjectId) => {
  const s = SUBJECTS.find((x) => x.id === subjectId);
  if (s?.stage === 2) return `/data/study/${subjectId}/ai_index.json`;
  return `/data/study/${subjectId}/ai_taxonomy_index.json`;
};
const handoverUrl = (subjectId) => `/data/study/${subjectId}/handover.md`;
const studyBase = (subjectId) => `/data/study/${subjectId}/`;

// ── 🃏 채팅 → 자동 암기카드 (퀴즈 탭 연동) ─────────────────────────
// AI 튜터와의 매 문답에서 "시험에 나올 암기 포인트"를 백그라운드로 추출해
// localStorage(quiz-chatcards-v1)에 leaf별로 적재. 퀴즈 탭이 이 덱으로 훈련한다.
export const CHATCARDS_KEY = 'quiz-chatcards-v1';
export function loadChatCards() {
  try { return JSON.parse(localStorage.getItem(CHATCARDS_KEY) || '{}') || {}; } catch { return {}; }
}
function saveChatCards(all) {
  try { localStorage.setItem(CHATCARDS_KEY, JSON.stringify(all)); } catch { /* full */ }
}
// 퀴즈 탭에서 직접 카드 추가/수정 — 자동 출제와 같은 저장소를 쓰므로
// SRS·오늘복습·4지선다·다기기 동기화가 그대로 적용된다.
export function upsertChatCard(leafId, card) {
  const all = loadChatCards();
  const arr = all[leafId] || [];
  const idx = arr.findIndex(c => c.id === card.id);
  if (idx >= 0) arr[idx] = { ...arr[idx], ...card };
  else arr.push(card);
  all[leafId] = arr.slice(-200);
  saveChatCards(all);
  return arr;
}
// 퀴즈 탭에서 부실 카드 삭제 (자동 출제 품질의 최종 관문은 사용자)
export function removeChatCard(leafId, cardId) {
  const all = loadChatCards();
  if (!all[leafId]) return;
  all[leafId] = all[leafId].filter(c => c.id !== cardId);
  if (!all[leafId].length) delete all[leafId];
  saveChatCards(all);
}

const CARDGEN_FAST = { anthropic: 'claude-haiku-4-5-20251001', openai: 'gpt-5.4-mini', google: 'gemini-3.1-flash-lite' };

// fire-and-forget — 채팅 UX를 막지 않는다. 실패는 조용히 무시.
async function generateChatCards({ provider, apiKey, baseUrl, leafId, leafPath, userText, assistantText, onSaved }) {
  try {
    if (!apiKey || !leafId || !assistantText || assistantText.length < 80) return;
    const existing = loadChatCards();
    const have = (existing[leafId] || []).map(c => c.term).slice(-40);
    const sys = `당신은 감정평가사 수험 암기카드 작성기입니다. 방금의 튜터링 문답에서 학생이 배운 "시험에 나올 수 있는 핵심 포인트"만 카드로 추출합니다.
규칙:
- 대화에 실제로 설명된 내용만. 잡담·인사·메타 대화·단순 확인이면 빈 배열.
- 카드: {"term":"용어(2~20자)","def":"핵심 내용(40~200자, 시험 포인트·근거조문 포함)","cloze":"def에서 핵심어 1곳을 ⬜⬜로 가린 문장","type":"개념|구별|요건|조문|판례|숫자","importance":1~3}
- importance: 3=빈출·핵심(학생이 헷갈려했거나 시험 단골), 2=중요, 1=참고
- 학생 질문에 "모르겠다/헷갈린다/다시" 같은 혼란 신호가 있으면 그 지점을 반드시 카드화하고 importance 3.
- 최대 3장. 이미 있는 카드와 중복 금지: [${have.join(', ')}]
- JSON만 출력: {"cards":[...]}`;
    const { text } = await sendMessagesUnified({
      apiKey, model: CARDGEN_FAST[provider] || CARDGEN_FAST.anthropic,
      system: sys, maxTokens: 600, baseUrl,
      messages: [{ role: 'user', content: `[단원] ${leafPath}\n[학생] ${userText.slice(0, 800)}\n[튜터] ${assistantText.slice(0, 2500)}` }],
    });
    const m = text.match(/\{[\s\S]*\}/);
    const parsed = JSON.parse(m ? m[0] : text);
    const cards = (parsed.cards || []).filter(c => c.term && c.def && c.def.length >= 20);
    if (!cards.length) return;
    const all = loadChatCards();
    const arr = all[leafId] || [];
    const seen = new Set(arr.map(c => c.term.replace(/\s+/g, '')));
    let added = 0;
    for (const c of cards) {
      const key = c.term.replace(/\s+/g, '');
      if (seen.has(key)) continue;
      seen.add(key);
      arr.push({ id: `cc-${Date.now()}-${added}`, term: c.term.trim(), def: c.def.trim(),
        cloze: c.cloze || '', type: c.type || '개념',
        importance: Math.min(3, Math.max(1, c.importance || 2)), ts: Date.now() });
      added++;
    }
    if (!added) return;
    all[leafId] = arr.slice(-200); // leaf당 최대 200장
    saveChatCards(all);
    onSaved?.(added, arr.length);
  } catch { /* 카드 생성 실패는 학습 흐름에 영향 없음 */ }
}

// 홈 과목 카드의 대분류 버튼.
// DIV_GROUPS: 여러 path[0]를 한 버튼으로 묶고 라벨을 지정. 정의된 과목은 이 그룹만 노출.
// 정의가 없는 과목은 path[0]별로 자동 생성(아래 DIV_EXCLUDE로 일부 숨김 가능).
const DIV_GROUPS = {
  economics: [
    { label: '미시경제', tops: ['미시경제학'] },
    { label: '거시경제', tops: ['거시경제학'] },
    { label: '국제경제', tops: ['국제경제학'] },
    { label: '재정학', tops: ['재정학'] },
  ],
  accounting: [
    { label: '회계원리', tops: ['회계원리'] },
    { label: '재무회계', tops: ['재무회계'] },
    { label: '원가관리회계', tops: ['원가관리회계'] },
    { label: '고급회계', tops: ['고급회계'] },
  ],
  civil: [
    { label: '민법총칙', tops: ['민법총칙'] },
    { label: '물권총론', tops: ['물권총론'] },
    { label: '소유권', tops: ['소유권'] },
    { label: '제한물권', tops: ['제한물권'] },
  ],
  realestate: [
    { label: '부동산학원론', tops: ['부동산학원론'] },
    { label: '감정평가론', tops: ['감정평가론'] },
  ],
  // 법규 9개 PART → 3개 그룹(빈출 감정평가법·공시 먼저). 필요시 그룹핑 조정 가능.
  law: [
    { label: '감정평가·공시', tops: ['PART 08 감정평가 및 감정평가사에 관한 법률', 'PART 07 부동산 가격공시에 관한 법률'] },
    { label: '국토·건축·정비', tops: ['PART 01 국토의 계획 및 이용에 관한 법률', 'PART 02 건축법', 'PART 03 도시 및 주거환경정비법'] },
    { label: '등기·지적·국유·담보', tops: ['PART 05 부동산등기법', 'PART 04 공간정보의 구축 및 관리 등에 관한 법률', 'PART 06 국유재산법', 'PART 09 동산.채권 등의 담보에 관한 법률'] },
  ],
};
const DIV_EXCLUDE = {};
const DIV_LABEL_MAP = {};

// 토스(Toss) 스타일 디자인 토큰 — 연회색 배경 + 순백 카드 + 부드러운 그림자 + 단일 포인트색
const TOSS = {
  bg: '#F2F4F6',      // 페이지 배경
  card: '#FFFFFF',    // 카드 표면
  blue: '#3182F6',    // 포인트(토스블루)
  blueDark: '#1B64DA',
  blueWeak: '#E8F1FE',// 포인트 약한 배경
  ink: '#191F28',     // 주요 텍스트
  sub: '#8B95A1',     // 보조 텍스트
  chipBg: '#F2F4F6',  // 칩 배경
  chipInk: '#4E5968', // 칩 텍스트
  track: '#E5E8EB',   // 진행바 트랙
  shadow: '0 2px 8px rgba(0, 23, 51, 0.06)',
  radius: 20,
};

// PC(≥1024px) 감지 — 2컬럼 레이아웃 분기용. 모바일/태블릿은 기존 단일 컬럼 유지.
function useIsDesktop() {
  const [isDesktop, setIsDesktop] = useState(() =>
    typeof window !== 'undefined' && window.matchMedia('(min-width: 1024px)').matches
  );
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const mq = window.matchMedia('(min-width: 1024px)');
    const handler = (e) => setIsDesktop(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);
  return isDesktop;
}

// 2차 ai_index.json 을 1차 leaves 배열 호환 구조로 변환
function normalizeStage2Index(idx) {
  if (!idx || idx.stage !== 2) return idx;
  const leaves = [];
  (idx.units || []).forEach((u) => {
    const baseId = `${idx.subject_id}__${u.code}`;
    // 단원 자체를 leaf로 (topics 없거나 첫 진입용)
    leaves.push({
      id: baseId,
      path: [idx.subject, u.title],
      leaf_type: 'unit',
      title: u.title,
      subject_root: idx.subject,
      frequency: u.frequency || 1,
      unit_code: u.code,
      unit_file: u.unit_file,
      problems_file: u.problems_file,
      section_key: 'full',
      section_lines: [1, 999999],
      section_name: '전체',
      est_minutes: u.est_minutes,
      stage: 2,
      subtitle: u.subtitle,
    });
    // 각 topic도 별도 leaf
    (u.topics || []).forEach((t) => {
      leaves.push({
        id: `${baseId}__${t.id}`,
        path: [idx.subject, u.title, t.title],
        leaf_type: 'topic',
        title: t.title,
        subject_root: idx.subject,
        frequency: u.frequency || 1,
        unit_code: u.code,
        unit_file: u.unit_file,
        problems_file: u.problems_file,
        section_key: 'topic',
        section_lines: t.section_lines || [1, 999999],
        section_name: t.title,
        stage: 2,
        templates: t.templates,
        key_cases: t.key_cases,
        key_statutes: t.key_statutes,
      });
    });
  });
  // default_unit → leaf id
  const defLeaf = leaves.find((l) => l.unit_code === idx.default_unit) || leaves[0];
  return {
    ...idx,
    leaves,
    default_leaf: defLeaf?.id || null,
  };
}

function todayStr() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

function uid() {
  try { return crypto.randomUUID(); } catch { return 's_' + Math.random().toString(36).slice(2); }
}

// 인라인 확인 — 브라우저 confirm() 대체. 1단계 클릭 시 노란 확인 상태로 변함.
function InlineConfirm({ label, danger, onYes, onNo, compact }) {
  const [armed, setArmed] = useState(false);
  if (!armed) {
    return (
      <button
        onClick={() => setArmed(true)}
        style={{
          padding: compact ? '4px 8px' : '6px 10px', fontSize: '0.78rem',
          background: danger ? '#fef2f2' : '#fff',
          color: danger ? '#991b1b' : '#374151',
          border: `1px solid ${danger ? '#fecaca' : '#d1d5db'}`,
          borderRadius: 6, cursor: 'pointer', fontWeight: 600,
        }}
      >
        {label}
      </button>
    );
  }
  return (
    <span style={{ display: 'inline-flex', gap: 4, alignItems: 'center' }}>
      <span style={{ fontSize: '0.75rem', color: '#92400e' }}>정말요?</span>
      <button
        onClick={() => { setArmed(false); onYes && onYes(); }}
        style={{ padding: '4px 10px', fontSize: '0.78rem', background: danger ? '#dc2626' : '#4f46e5', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontWeight: 700 }}
      >
        예
      </button>
      <button
        onClick={() => { setArmed(false); onNo && onNo(); }}
        style={{ padding: '4px 10px', fontSize: '0.78rem', background: '#fff', color: '#374151', border: '1px solid #d1d5db', borderRadius: 6, cursor: 'pointer' }}
      >
        아니요
      </button>
    </span>
  );
}

function MasteryBar({ value, color = '#4f46e5' }) {
  const pct = Math.max(0, Math.min(1, value || 0)) * 100;
  return (
    <div style={{ background: '#f3f4f6', borderRadius: 6, height: 5, overflow: 'hidden' }}>
      <div style={{ width: `${pct}%`, height: '100%', background: color, transition: 'width .3s' }} />
    </div>
  );
}

// 평탄 leaf 리스트를 들여쓰기로 시각화하는 picker.
// path 길이에 따른 들여쓰기 + 검색.
function LeafPicker({ leaves, current, onPick, mastery, due, quizStatsByLeaf, inline = false }) {
  const [open, setOpen] = useState(inline);
  const [q, setQ] = useState('');
  const cur = leaves.find((l) => l.id === current?.leaf_id);
  // 트리 그룹화: subject → chapter → section → item
  const tree = useMemo(() => {
    const t = {};
    leaves.forEach((l) => {
      const [s, c, sec, it] = l.path;
      t[s] = t[s] || {};
      if (c) {
        t[s][c] = t[s][c] || { _leaf: null, sections: {} };
        if (!sec && !it) t[s][c]._leaf = l;
        if (sec) {
          t[s][c].sections[sec] = t[s][c].sections[sec] || { _leaf: null, items: {} };
          if (!it) t[s][c].sections[sec]._leaf = l;
          if (it) t[s][c].sections[sec].items[it] = l;
        }
      }
    });
    return t;
  }, [leaves]);

  const dueIds = useMemo(() => new Set(due.map((d) => d.code)), [due]);

  const matchQ = (l) => !q.trim() || l.path.join(' / ').toLowerCase().includes(q.trim().toLowerCase());

  return (
    <div style={{ position: 'relative' }}>
      {!inline && (
        <button
          onClick={() => setOpen((v) => !v)}
          style={{
            width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '10px 14px', background: '#fff', border: '1px solid #d1d5db', borderRadius: 10,
            fontSize: '0.92rem', fontWeight: 700, cursor: 'pointer', color: '#111827',
            textAlign: 'left',
          }}
        >
          <span style={{ display: 'flex', alignItems: 'center', gap: 8, flex: 1, minWidth: 0 }}>
            <BookOpen size={18} color="#4f46e5" />
            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {cur ? cur.path.slice(1).join(' › ') || cur.path[0] : '단원 선택'}
            </span>
          </span>
          <ChevronDown size={18} />
        </button>
      )}
      {open && (
        <div style={inline ? {
          background: '#fff',
        } : {
          position: 'absolute', top: 'calc(100% + 4px)', left: 0, right: 0, zIndex: 30,
          background: '#fff', border: '1px solid #d1d5db', borderRadius: 10,
          maxHeight: 480, overflowY: 'auto', boxShadow: '0 8px 24px rgba(0,0,0,.12)',
        }}>
          <div style={{ padding: 8, borderBottom: '1px solid #f3f4f6', position: 'sticky', top: 0, background: '#fff' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, background: '#f3f4f6', borderRadius: 8, padding: '6px 10px' }}>
              <Search size={14} color="#6b7280" />
              <input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="단원·관 검색 (예: 행위능력, 명의신탁)"
                style={{ flex: 1, border: 'none', background: 'transparent', outline: 'none', fontSize: '0.85rem' }}
              />
            </div>
          </div>
          {Object.entries(tree).map(([subj, chs]) => (
            <div key={subj}>
              <div style={{ padding: '8px 12px', background: '#f9fafb', fontWeight: 800, fontSize: '0.78rem', color: '#4338ca' }}>
                {subj}
              </div>
              {Object.entries(chs).map(([chName, ch]) => {
                const chLeaves = [];
                if (ch._leaf) chLeaves.push(ch._leaf);
                Object.entries(ch.sections).forEach(([_, sec]) => {
                  if (sec._leaf) chLeaves.push(sec._leaf);
                  Object.values(sec.items).forEach((l) => chLeaves.push(l));
                });
                if (q && !chLeaves.some(matchQ)) return null;
                return (
                  <div key={chName}>
                    <div style={{ padding: '6px 12px', fontSize: '0.82rem', fontWeight: 700, color: '#111827', borderTop: '1px solid #f3f4f6' }}>
                      {chName}
                    </div>
                    {ch._leaf && matchQ(ch._leaf) && (
                      <LeafButton leaf={ch._leaf} active={ch._leaf.id === current?.leaf_id} mastery={mastery} due={dueIds} quizStatsByLeaf={quizStatsByLeaf} onPick={() => { onPick(ch._leaf); if (!inline) setOpen(false); }} depth={1} />
                    )}
                    {Object.entries(ch.sections).map(([secName, sec]) => {
                      const secLeaves = sec._leaf ? [sec._leaf, ...Object.values(sec.items)] : Object.values(sec.items);
                      if (q && !secLeaves.some(matchQ)) return null;
                      return (
                        <div key={secName}>
                          {sec._leaf && matchQ(sec._leaf) && (
                            <LeafButton leaf={sec._leaf} active={sec._leaf.id === current?.leaf_id} mastery={mastery} due={dueIds} quizStatsByLeaf={quizStatsByLeaf} onPick={() => { onPick(sec._leaf); if (!inline) setOpen(false); }} depth={1} sectionLabel={secName} />
                          )}
                          {!sec._leaf && Object.keys(sec.items).length > 0 && (
                            <div style={{ padding: '4px 12px 2px 24px', fontSize: '0.76rem', color: '#6b7280' }}>{secName}</div>
                          )}
                          {Object.values(sec.items).filter(matchQ).map((it) => (
                            <LeafButton key={it.id} leaf={it} active={it.id === current?.leaf_id} mastery={mastery} due={dueIds} quizStatsByLeaf={quizStatsByLeaf} onPick={() => { onPick(it); if (!inline) setOpen(false); }} depth={2} />
                          ))}
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function LeafButton({ leaf, active, mastery, due, quizStatsByLeaf, onPick, depth = 0, sectionLabel }) {
  const m = mastery[leaf.id] || { coverage: 0, accuracy: 0, status: 'not_started' };
  const isDue = due.has(leaf.id);
  const qs = quizStatsByLeaf?.[leaf.id];
  return (
    <button
      onClick={onPick}
      style={{
        width: '100%', textAlign: 'left', padding: `6px 12px 6px ${12 + depth * 14}px`,
        background: active ? '#eef2ff' : '#fff', border: 'none', cursor: 'pointer',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 6 }}>
        <span style={{ fontSize: '0.85rem', color: '#111827', flex: 1, minWidth: 0 }}>
          {sectionLabel && <span style={{ color: '#6b7280', fontSize: '0.76rem' }}>{sectionLabel} · </span>}
          {leaf.path[leaf.path.length - 1]}
          {leaf.frequency >= 3 && <span style={{ color: '#dc2626', marginLeft: 4 }}>★</span>}
          {isDue && <span style={{ background: '#fef3c7', color: '#92400e', fontSize: '0.7rem', padding: '0 6px', borderRadius: 4, marginLeft: 4 }}>복습</span>}
        </span>
        <span style={{ fontSize: '0.7rem', color: '#9ca3af', whiteSpace: 'nowrap' }}>
          {m.status === 'mastered' ? '✓' : m.coverage > 0 ? `${Math.round(m.coverage * 100)}%` : ''}
        </span>
      </div>
      {/* 진척: AI(상) + Quiz(하) 듀얼 막대 */}
      {(m.coverage > 0 || (qs && qs.answered > 0)) && (
        <div style={{ marginTop: 4, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {m.coverage > 0 && <MasteryBar value={m.coverage} color="#4f46e5" />}
          {qs && qs.total > 0 && qs.answered > 0 && (
            <MasteryBar value={qs.accuracy} color="#10b981" />
          )}
        </div>
      )}
      {qs && qs.total > 0 && (
        <div style={{ fontSize: '0.7rem', color: '#6b7280', marginTop: 2 }}>
          기출 {qs.answered}/{qs.total}
          {qs.answered > 0 && ` · 정답률 ${Math.round(qs.accuracy * 100)}%`}
          {qs.due > 0 && <span style={{ color: '#92400e' }}> · 복습 {qs.due}</span>}
        </div>
      )}
    </button>
  );
}

function ApiKeyForm({ initial, onSave }) {
  const [key, setKey] = useState(initial || '');
  const [show, setShow] = useState(false);
  return (
    <div style={{ padding: 16, background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, maxWidth: 520, margin: '24px auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
        <Key size={18} color="#4f46e5" />
        <h3 style={{ margin: 0, fontSize: '1.05rem', color: '#111827' }}>Claude API 키 입력 (BYOK)</h3>
      </div>
      <p style={{ fontSize: '0.85rem', color: '#6b7280', lineHeight: 1.5 }}>
        본 앱은 사용자의 Claude API 키로 직접 Anthropic에 요청합니다. 키는 이 기기 localStorage에만 저장되고 서버로 전송되지 않습니다.
        <br />
        키는 <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noreferrer" style={{ color: '#4f46e5' }}>console.anthropic.com</a>에서 발급받을 수 있습니다.
      </p>
      <div style={{ display: 'flex', gap: 6, marginTop: 12 }}>
        <input
          type={show ? 'text' : 'password'}
          value={key}
          onChange={(e) => setKey(e.target.value)}
          placeholder="sk-ant-..."
          style={{ flex: 1, padding: '10px 12px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.9rem' }}
        />
        <button onClick={() => setShow((v) => !v)} style={{ padding: '8px 12px', background: '#f3f4f6', border: '1px solid #d1d5db', borderRadius: 8, cursor: 'pointer' }}>
          {show ? '숨김' : '표시'}
        </button>
      </div>
      <button
        onClick={() => onSave(key.trim())}
        disabled={!key.trim().startsWith('sk-')}
        style={{
          marginTop: 12, width: '100%', padding: '11px 16px',
          background: key.trim().startsWith('sk-') ? '#4f46e5' : '#9ca3af',
          color: '#fff', border: 'none', borderRadius: 8, fontWeight: 700,
          cursor: key.trim().startsWith('sk-') ? 'pointer' : 'not-allowed',
        }}
      >
        저장
      </button>
    </div>
  );
}


// 설정 패널 — API 키(Anthropic·OpenAI·Google) + 프록시 URL + 기본 prefs
function SettingsPanel({ byok, prefs, onClose, onSave }) {
  const [antKey, setAntKey] = useState(byok || '');
  const [oaiKey, setOaiKey] = useState(() => getApiKey('openai'));
  const [gKey, setGKey] = useState(() => getApiKey('google'));
  const [msKey, setMsKey] = useState(() => getApiKey('moonshot'));
  const [baseUrls, setBaseUrlsState] = useState(() => getBaseUrls());
  const [dailyCap, setDailyCap] = useState(prefs.daily_cap || 500);
  const [streaming, setStreaming] = useState(!!prefs.streaming);
  const [showAnt, setShowAnt] = useState(false);
  const [showOai, setShowOai] = useState(false);
  const [showG, setShowG] = useState(false);
  const [showMs, setShowMs] = useState(false);
  const [saved, setSaved] = useState(false);

  const save = () => {
    setByok(antKey.trim() || null);
    setApiKey('openai', oaiKey.trim() || null);
    setApiKey('google', gKey.trim() || null);
    setApiKey('moonshot', msKey.trim() || null);
    setBaseUrl('openai', baseUrls.openai || null);
    setBaseUrl('google', baseUrls.google || null);
    setPrefs({ daily_cap: Number(dailyCap) || 500, streaming });
    setSaved(true);
    setTimeout(() => { setSaved(false); onSave && onSave(antKey.trim()); }, 900);
  };

  const row = (label, val, setVal, show, setShow, placeholder) => (
    <div style={{ marginBottom: 12 }}>
      <div style={{ fontSize: '0.78rem', fontWeight: 700, color: '#374151', marginBottom: 4 }}>{label}</div>
      <div style={{ display: 'flex', gap: 6 }}>
        <input
          type={show ? 'text' : 'password'}
          value={val}
          onChange={(e) => setVal(e.target.value)}
          placeholder={placeholder}
          style={{ flex: 1, padding: '8px 10px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.88rem', fontFamily: 'monospace' }}
        />
        <button onClick={() => setShow((v) => !v)} style={{ padding: '6px 10px', background: '#f3f4f6', border: '1px solid #d1d5db', borderRadius: 8, cursor: 'pointer', fontSize: '0.78rem' }}>
          {show ? '숨김' : '표시'}
        </button>
      </div>
    </div>
  );

  return (
    <div style={{ padding: 16, background: '#fff', border: '1px solid #e5e7eb', borderRadius: 14, maxWidth: 520, margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
        <h3 style={{ margin: 0, fontSize: '1rem', display: 'flex', alignItems: 'center', gap: 6 }}>
          <Settings size={17} /> 설정
        </h3>
        <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6b7280', fontSize: '1.1rem' }}>✕</button>
      </div>

      <div style={{ fontSize: '0.8rem', fontWeight: 800, color: '#4338ca', marginBottom: 8 }}>🔑 API 키</div>
      {row('Moonshot (Kimi · 추천)', msKey, setMsKey, showMs, setShowMs, 'sk-... (platform.moonshot.ai)')}
      {row('Anthropic (Claude)', antKey, setAntKey, showAnt, setShowAnt, 'sk-ant-...')}
      {row('OpenAI (GPT)', oaiKey, setOaiKey, showOai, setShowOai, 'sk-...')}
      {row('Google (Gemini)', gKey, setGKey, showG, setShowG, 'AIza...')}

      <div style={{ fontSize: '0.8rem', fontWeight: 800, color: '#4338ca', marginBottom: 8, marginTop: 4 }}>🌐 프록시 Base URL (CORS 우회용, 선택)</div>
      <div style={{ marginBottom: 10 }}>
        <div style={{ fontSize: '0.75rem', color: '#6b7280', marginBottom: 4 }}>OpenAI 프록시</div>
        <input value={baseUrls.openai || ''} onChange={(e) => setBaseUrlsState((p) => ({ ...p, openai: e.target.value }))}
          placeholder="https://my-proxy.workers.dev"
          style={{ width: '100%', padding: '7px 10px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.85rem', boxSizing: 'border-box' }} />
      </div>
      <div style={{ marginBottom: 12 }}>
        <div style={{ fontSize: '0.75rem', color: '#6b7280', marginBottom: 4 }}>Google 프록시</div>
        <input value={baseUrls.google || ''} onChange={(e) => setBaseUrlsState((p) => ({ ...p, google: e.target.value }))}
          placeholder="https://my-google-proxy.workers.dev"
          style={{ width: '100%', padding: '7px 10px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.85rem', boxSizing: 'border-box' }} />
      </div>

      <div style={{ fontSize: '0.8rem', fontWeight: 800, color: '#4338ca', marginBottom: 8 }}>⚙️ 기타 설정</div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
        <label style={{ fontSize: '0.82rem', color: '#374151', flex: 1 }}>일일 메시지 cap</label>
        <input type="number" value={dailyCap} onChange={(e) => setDailyCap(e.target.value)} min={1} max={9999}
          style={{ width: 70, padding: '5px 8px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.88rem', textAlign: 'right' }} />
        <span style={{ fontSize: '0.78rem', color: '#9ca3af' }}>건</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
        <label style={{ fontSize: '0.82rem', color: '#374151', flex: 1 }}>스트리밍 응답</label>
        <button
          onClick={() => setStreaming((v) => !v)}
          style={{
            padding: '4px 12px', borderRadius: 14, fontSize: '0.78rem', fontWeight: 700, cursor: 'pointer',
            background: streaming ? '#eef2ff' : '#f3f4f6',
            color: streaming ? '#4338ca' : '#6b7280',
            border: `1px solid ${streaming ? '#c7d2fe' : '#d1d5db'}`,
          }}
        >{streaming ? 'ON' : 'OFF'}</button>
      </div>

      <button
        onClick={save}
        style={{
          width: '100%', padding: '11px', background: saved ? '#16a34a' : '#4f46e5',
          color: '#fff', border: 'none', borderRadius: 10, fontWeight: 800, fontSize: '0.95rem', cursor: 'pointer',
          transition: 'background .2s',
        }}
      >
        {saved ? '✓ 저장됨' : '저장'}
      </button>
    </div>
  );
}

// 응답 텍스트에서 ①~⑤ 또는 1)~5) 옵션 줄을 추출.
// 응답이 정답·해설을 이미 포함하면(예: "정답: ②") null 반환.
const CIRCLED_DIGITS = ['①', '②', '③', '④', '⑤'];
function extractMultipleChoice(text) {
  if (!text) return null;
  if (/정답\s*[:：]/.test(text) || /correct\s*answer/i.test(text)) return null;
  const lines = text.split('\n').map((l) => l.trim()).filter(Boolean);
  const opts = [];
  for (const l of lines) {
    const m1 = l.match(/^[①②③④⑤]\s*(.+)$/);
    const m2 = l.match(/^([1-5])[\.\)]\s*(.+)$/);
    if (m1) opts.push({ n: CIRCLED_DIGITS.indexOf(l[0]) + 1, text: m1[1] });
    else if (m2) opts.push({ n: parseInt(m2[1], 10), text: m2[2] });
  }
  // 5지선다만 인식. 중복 번호 제거.
  const uniq = [];
  const seen = new Set();
  for (const o of opts) {
    if (seen.has(o.n) || o.n < 1 || o.n > 5) continue;
    seen.add(o.n); uniq.push(o);
  }
  if (uniq.length < 2 || uniq.length > 5) return null;
  return uniq;
}

function AnswerChoiceRow({ options, onPick, disabled }) {
  return (
    <div style={{
      display: 'flex', gap: 6, padding: '8px 12px', marginTop: 4,
      background: '#fef9c3', borderTop: '1px solid #fde68a',
      borderRadius: '0 0 12px 12px',
    }}>
      <div style={{ fontSize: '0.78rem', color: '#854d0e', alignSelf: 'center', marginRight: 4, fontWeight: 700 }}>답:</div>
      {options.map((o) => (
        <button
          key={o.n}
          onClick={() => onPick(o)}
          disabled={disabled}
          title={o.text.slice(0, 40)}
          style={{
            width: 36, height: 36, borderRadius: '50%',
            border: '1.5px solid #ca8a04', background: '#fff', color: '#854d0e',
            fontWeight: 800, fontSize: '0.95rem', cursor: disabled ? 'not-allowed' : 'pointer',
            opacity: disabled ? 0.5 : 1,
          }}
        >
          {CIRCLED_DIGITS[o.n - 1]}
        </button>
      ))}
    </div>
  );
}

// 5과목 종합 분석 — 레이더(다각형) + 단원별 상위/하위 5
function AnalyticsPanel({ mastery, onClose, onJump, leavesBySubject }) {
  const stats = SUBJECTS.map((s) => {
    const ks = Object.keys(mastery).filter((k) => k.startsWith(s.id + '__') || k.startsWith(s.id + '_'));
    const total = ks.length;
    const covSum = ks.reduce((a, k) => a + (mastery[k]?.coverage || 0), 0);
    const accs = ks.map((k) => mastery[k]?.accuracy || 0).filter((x) => x > 0);
    const masterCount = ks.filter((k) => mastery[k]?.status === 'mastered').length;
    const isStage2 = s.stage === 2;
    const avgScoreSum = isStage2 ? ks.reduce((a, k) => a + (mastery[k]?.avg_score_pct || 0), 0) / 100 : 0;
    return {
      s,
      total,
      covAvg: total > 0 ? covSum / total : 0,
      accAvg: accs.length > 0 ? accs.reduce((a, b) => a + b, 0) / accs.length : 0,
      masterCount,
      isStage2,
      avgScoreAvg: isStage2 && total > 0 ? avgScoreSum / total : 0,
    };
  });
  const statsStage1 = stats.filter((x) => !x.isStage2);
  const statsStage2 = stats.filter((x) => x.isStage2);

  const allRanked = useMemo(() => {
    const arr = [];
    SUBJECTS.forEach((s) => {
      const leaves = leavesBySubject[s.id] || [];
      leaves.forEach((leaf) => {
        const m = mastery[leaf.id];
        if (m && (m.coverage || 0) > 0) {
          arr.push({ leaf, subject: s, ...m });
        }
      });
    });
    return arr.sort((a, b) => (b.coverage || 0) - (a.coverage || 0));
  }, [mastery, leavesBySubject]);

  const top5 = allRanked.slice(0, 5);
  const bottom5 = allRanked.slice(-5).reverse();

  // 레이더 렌더 헬퍼 (stage별)
  const renderRadar = (data, label) => {
    if (data.length < 3) return null;
    const radius = 60, cx = 80, cy = 80;
    const pts = data.map((st, i) => {
      const angle = (Math.PI * 2 * i) / data.length - Math.PI / 2;
      const r = radius * (st.covAvg || 0);
      return { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle), s: st.s };
    });
    const polyStr = pts.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
    const axisPts = data.map((st, i) => {
      const angle = (Math.PI * 2 * i) / data.length - Math.PI / 2;
      return { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle), label: st.s.short };
    });
    return (
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '0.74rem', color: '#4338ca', fontWeight: 700, marginBottom: 4 }}>{label}</div>
        <svg viewBox="0 0 160 160" style={{ width: '100%', maxWidth: 180 }}>
          {[0.25, 0.5, 0.75, 1].map((r) => (
            <polygon
              key={r}
              points={data.map((_, i) => {
                const a = (Math.PI * 2 * i) / data.length - Math.PI / 2;
                return `${(cx + radius * r * Math.cos(a)).toFixed(1)},${(cy + radius * r * Math.sin(a)).toFixed(1)}`;
              }).join(' ')}
              fill="none" stroke="#e5e7eb" strokeWidth="1"
            />
          ))}
          {axisPts.map((p, i) => (
            <line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="#e5e7eb" strokeWidth="1" />
          ))}
          <polygon points={polyStr} fill="#4f46e5" fillOpacity="0.22" stroke="#4f46e5" strokeWidth="2" />
          {pts.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r="3" fill="#4f46e5" />
          ))}
          {axisPts.map((p, i) => (
            <text key={i}
              x={p.x + (p.x > cx ? 4 : p.x < cx ? -4 : 0)}
              y={p.y + (p.y > cy ? 10 : p.y < cy ? -4 : 4)}
              fontSize="9" fontWeight="700"
              textAnchor={p.x > cx + 2 ? 'start' : p.x < cx - 2 ? 'end' : 'middle'}
              fill="#4338ca">{p.label}</text>
          ))}
        </svg>
      </div>
    );
  };

  return (
    <div style={{ padding: 16, background: '#fff', borderRadius: 12, border: '1px solid #e5e7eb' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <h3 style={{ margin: 0, fontSize: '1rem', display: 'flex', alignItems: 'center', gap: 6 }}>
          <BarChart3 size={18} /> 8과목 종합 분석
        </h3>
        <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6b7280' }}>✕</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 14 }}>
        {renderRadar(statsStage1, '📖 1차 5과목')}
        {renderRadar(statsStage2, '✍️ 2차 3과목')}
      </div>

      <div>
          <table style={{ width: '100%', fontSize: '0.78rem', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ color: '#6b7280' }}>
                <th style={{ textAlign: 'left' }}>과목</th>
                <th style={{ textAlign: 'right' }}>평균</th>
                <th style={{ textAlign: 'right' }}>마스터</th>
                <th style={{ textAlign: 'right' }}>정답률</th>
              </tr>
            </thead>
            <tbody>
              {stats.map((st) => (
                <tr key={st.s.id} style={{ borderTop: '1px solid #f3f4f6' }}>
                  <td style={{ padding: '4px 0', color: st.s.color, fontWeight: 700 }}>
                    <SubjectIcon id={st.s.id} size={13} color="#8B95A1" style={{ verticalAlign: '-2px', marginRight: 3 }} />{st.s.short}
                    {st.isStage2 && <span style={{ marginLeft: 4, fontSize: '0.6rem', background: st.s.color, color: '#fff', padding: '1px 4px', borderRadius: 4 }}>2차</span>}
                  </td>
                  <td style={{ textAlign: 'right' }}>{Math.round(st.covAvg * 100)}%</td>
                  <td style={{ textAlign: 'right' }}>{st.masterCount}/{st.total}</td>
                  <td style={{ textAlign: 'right' }}>{st.isStage2 ? (st.avgScoreAvg > 0 ? `${Math.round(st.avgScoreAvg * 100)}%` : '—') : (st.accAvg > 0 ? `${Math.round(st.accAvg * 100)}%` : '—')}</td>
                </tr>
              ))}
            </tbody>
          </table>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginTop: 16 }}>
        <div>
          <div style={{ fontSize: '0.78rem', fontWeight: 700, color: '#065f46', marginBottom: 4 }}>🏆 진척 상위 5</div>
          {top5.length === 0 && <div style={{ fontSize: '0.78rem', color: '#9ca3af' }}>없음</div>}
          {top5.map((x) => (
            <button
              key={x.leaf.id}
              onClick={() => onJump(x.leaf, x.subject.id)}
              style={{
                display: 'block', width: '100%', textAlign: 'left',
                padding: '4px 6px', background: 'transparent', border: 'none',
                borderRadius: 4, cursor: 'pointer', fontSize: '0.78rem', color: '#111827',
              }}
            >
              <span style={{ color: x.subject.color, fontWeight: 700 }}>{x.subject.icon}</span>{' '}
              {x.leaf.path.slice(-1)[0]}{' '}
              <span style={{ color: '#9ca3af' }}>{Math.round((x.coverage || 0) * 100)}%</span>
            </button>
          ))}
        </div>
        <div>
          <div style={{ fontSize: '0.78rem', fontWeight: 700, color: '#9a3412', marginBottom: 4 }}>🐌 진척 하위 5 (활성)</div>
          {bottom5.length === 0 && <div style={{ fontSize: '0.78rem', color: '#9ca3af' }}>없음</div>}
          {bottom5.map((x) => (
            <button
              key={x.leaf.id}
              onClick={() => onJump(x.leaf, x.subject.id)}
              style={{
                display: 'block', width: '100%', textAlign: 'left',
                padding: '4px 6px', background: 'transparent', border: 'none',
                borderRadius: 4, cursor: 'pointer', fontSize: '0.78rem', color: '#111827',
              }}
            >
              <span style={{ color: x.subject.color, fontWeight: 700 }}>{x.subject.icon}</span>{' '}
              {x.leaf.path.slice(-1)[0]}{' '}
              <span style={{ color: '#9ca3af' }}>{Math.round((x.coverage || 0) * 100)}%</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

// 법규 판례 카드 위젯 — [대법원 YYYY. M. DD. 선고 NNNN두NNNN] 패턴 파싱
function parseLawCases(md) {
  if (!md) return [];
  const out = [];
  const re = /\[대법원\s+(\d{4})\.\s*(\d{1,2})\.\s*(\d{1,2})\.\s*선고\s+(\d+(?:두|다|누|가)\d+(?:\s*전합)?)[^\]]*\]([\s\S]*?)(?=\[대법원|\n##\s|$)/g;
  let m;
  while ((m = re.exec(md))) {
    const date = `${m[1]}.${m[2].padStart(2,'0')}.${m[3].padStart(2,'0')}`;
    const caseNo = m[4].trim().replace(/\s+/g, ' ');
    const bodyFull = m[5].trim();
    const body = bodyFull.length > 600 ? bodyFull.slice(0, 600) + '…' : bodyFull;
    if (body.length > 80) out.push({ date, caseNo, body, fullLen: bodyFull.length });
  }
  // 중복 사건번호 제거 (앞 등장 유지)
  const seen = new Set();
  return out.filter((c) => { if (seen.has(c.caseNo)) return false; seen.add(c.caseNo); return true; });
}

function LawCasesWidget({ casesMd, onAskAI }) {
  const cards = useMemo(() => parseLawCases(casesMd), [casesMd]);
  const [idx, setIdx] = useState(0);
  if (cards.length === 0) return null;
  const c = cards[idx];
  return (
    <div style={{
      background: 'linear-gradient(180deg, #fef2f2 0%, #fff 100%)',
      border: '1px solid #fecaca', borderRadius: 12, padding: 14, marginBottom: 10,
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <div style={{ fontWeight: 800, color: '#991b1b', fontSize: '0.88rem' }}>
          ⚖️ 판례 카드 <span style={{ color: '#6b7280', fontWeight: 500 }}>({idx + 1}/{cards.length})</span>
        </div>
        <div style={{ fontSize: '0.7rem', color: '#6b7280' }}>{cards.length}개 판례 추출</div>
      </div>
      <div style={{
        background: '#fff', border: '1px dashed #fecaca', borderRadius: 8, padding: 14,
        fontSize: '0.88rem', lineHeight: 1.65, color: '#111827',
      }}>
        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#991b1b', marginBottom: 6 }}>
          대판 {c.caseNo} <span style={{ color: '#6b7280', fontWeight: 500 }}>· {c.date}</span>
        </div>
        <div style={{ whiteSpace: 'pre-wrap', maxHeight: 260, overflowY: 'auto' }}>
          {c.body}
        </div>
      </div>
      <div style={{ display: 'flex', gap: 6, marginTop: 10, alignItems: 'center' }}>
        <button onClick={() => setIdx((i) => Math.max(0, i - 1))} disabled={idx === 0}
          style={{ padding: '6px 12px', cursor: idx === 0 ? 'not-allowed' : 'pointer',
            background: '#fff', border: '1px solid #d1d5db', borderRadius: 6,
            opacity: idx === 0 ? 0.4 : 1, fontWeight: 700 }}>
          ◀ 이전
        </button>
        <button onClick={() => setIdx((i) => Math.min(cards.length - 1, i + 1))} disabled={idx >= cards.length - 1}
          style={{ padding: '6px 12px', cursor: idx >= cards.length - 1 ? 'not-allowed' : 'pointer',
            background: '#fff', border: '1px solid #d1d5db', borderRadius: 6,
            opacity: idx >= cards.length - 1 ? 0.4 : 1, fontWeight: 700 }}>
          다음 ▶
        </button>
        <button onClick={() => onAskAI && onAskAI(c)}
          style={{ marginLeft: 'auto', padding: '6px 12px', cursor: 'pointer',
            background: '#dc2626', color: '#fff', border: 'none', borderRadius: 6, fontWeight: 700, fontSize: '0.82rem' }}>
          🤖 답안 인용 시범
        </button>
      </div>
    </div>
  );
}

// 이론 답안 양식 카드 위젯 — _all.md 에서 ### Form N 블록 파싱
function parseTemplateForms(md) {
  if (!md) return [];
  const out = [];
  const re = /###\s*Form\s*(\d+)\s*\n```[^\n]*\n([\s\S]+?)\n```/g;
  let m;
  while ((m = re.exec(md))) {
    out.push({ id: m[1], body: m[2].trim() });
  }
  return out;
}

function TemplateCardWidget({ templatesMd, onAskAI }) {
  const cards = useMemo(() => parseTemplateForms(templatesMd), [templatesMd]);
  const [idx, setIdx] = useState(0);
  const [shuffle, setShuffle] = useState(false);
  if (cards.length === 0) return null;
  const order = shuffle ? cards.map((_, i) => i).sort((a, b) => (a * 7919) % 13 - (b * 7919) % 13) : cards.map((_, i) => i);
  const actual = cards[order[idx] || 0];
  return (
    <div style={{
      background: 'linear-gradient(180deg, #f0fdf4 0%, #fff 100%)',
      border: '1px solid #86efac', borderRadius: 12, padding: 14, marginBottom: 10,
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <div style={{ fontWeight: 800, color: '#047857', fontSize: '0.88rem' }}>
          📋 답안 양식 {actual.id} <span style={{ color: '#6b7280', fontWeight: 500 }}>({idx + 1}/{cards.length})</span>
        </div>
        <div style={{ display: 'flex', gap: 4 }}>
          <button onClick={() => setShuffle((v) => !v)}
            style={{ fontSize: '0.7rem', padding: '3px 8px', cursor: 'pointer',
              border: shuffle ? '1px solid #16a34a' : '1px solid #d1d5db',
              background: shuffle ? '#dcfce7' : '#fff', color: shuffle ? '#15803d' : '#6b7280', borderRadius: 6 }}>
            🎲 셔플
          </button>
        </div>
      </div>
      <div style={{
        background: '#fff', border: '1px dashed #86efac', borderRadius: 8, padding: 14,
        fontSize: '0.95rem', lineHeight: 1.7, color: '#111827',
        whiteSpace: 'pre-wrap', minHeight: 80,
      }}>
        {actual.body}
      </div>
      <div style={{ display: 'flex', gap: 6, marginTop: 10, alignItems: 'center' }}>
        <button onClick={() => setIdx((i) => Math.max(0, i - 1))} disabled={idx === 0}
          style={{ padding: '6px 12px', cursor: idx === 0 ? 'not-allowed' : 'pointer',
            background: '#fff', border: '1px solid #d1d5db', borderRadius: 6,
            opacity: idx === 0 ? 0.4 : 1, fontWeight: 700 }}>
          ◀ 이전
        </button>
        <button onClick={() => setIdx((i) => Math.min(cards.length - 1, i + 1))} disabled={idx >= cards.length - 1}
          style={{ padding: '6px 12px', cursor: idx >= cards.length - 1 ? 'not-allowed' : 'pointer',
            background: '#fff', border: '1px solid #d1d5db', borderRadius: 6,
            opacity: idx >= cards.length - 1 ? 0.4 : 1, fontWeight: 700 }}>
          다음 ▶
        </button>
        <button onClick={() => onAskAI && onAskAI(actual)}
          style={{ marginLeft: 'auto', padding: '6px 12px', cursor: 'pointer',
            background: '#16a34a', color: '#fff', border: 'none', borderRadius: 6, fontWeight: 700, fontSize: '0.82rem' }}>
          🤖 AI에 더 자세히
        </button>
      </div>
    </div>
  );
}

// 2차 답안 작성 입력 — 큰 textarea + 타이머
function AnswerWriteInput({ scorePoint, onSubmit, disabled }) {
  const [answer, setAnswer] = useState('');
  const [scoreSel, setScoreSel] = useState(scorePoint || 30);
  const [timerOn, setTimerOn] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  useEffect(() => {
    if (!timerOn) return;
    const t = setInterval(() => setElapsed((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, [timerOn]);
  const targetMin = scoreSel; // 1점 ≈ 1분
  const mm = Math.floor(elapsed / 60);
  const ss = String(elapsed % 60).padStart(2, '0');
  const submit = () => {
    if (!answer.trim()) return;
    onSubmit({
      answer: answer.trim(),
      score_point: scoreSel,
      time_used_sec: elapsed,
      time_target_min: targetMin,
    });
    setAnswer(''); setElapsed(0); setTimerOn(false);
  };
  return (
    <div style={{ background: '#fafafa', border: '1px solid #c7d2fe', borderRadius: 12, padding: 10 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6, flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#4338ca' }}>📝 답안 작성</span>
        <div style={{ display: 'flex', gap: 4 }}>
          {[10, 20, 30, 40].map((p) => (
            <button key={p} onClick={() => setScoreSel(p)}
              style={{
                padding: '3px 8px', fontSize: '0.72rem', fontWeight: 700, cursor: 'pointer',
                borderRadius: 6, border: scoreSel === p ? '1px solid #4f46e5' : '1px solid #d1d5db',
                background: scoreSel === p ? '#eef2ff' : '#fff',
                color: scoreSel === p ? '#1d4ed8' : '#6b7280',
              }}>{p}점</button>
          ))}
        </div>
        <span style={{ fontSize: '0.7rem', color: '#6b7280' }}>
          권장 {targetMin}분 · ~{Math.round(scoreSel * 0.7)}줄
        </span>
        <span style={{ marginLeft: 'auto', fontSize: '0.8rem', fontWeight: 700, color: timerOn ? '#ea580c' : '#9ca3af' }}>
          ⏱ {mm}:{ss}
        </span>
      </div>
      <textarea
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        placeholder={'Ⅰ. 서\n\nⅡ. 본론\n  1. ...\n  2. ...\n\nⅢ. 결론·유의사항'}
        rows={10}
        disabled={disabled}
        style={{
          width: '100%', padding: 10,
          fontFamily: 'inherit', fontSize: '0.92rem', lineHeight: 1.7,
          border: '1px solid #d1d5db', borderRadius: 8, resize: 'vertical',
          background: disabled ? '#f3f4f6' : '#fff',
        }}
      />
      <div style={{ display: 'flex', gap: 6, marginTop: 8 }}>
        <button onClick={() => setTimerOn((v) => !v)}
          style={{
            padding: '8px 12px', fontSize: '0.82rem', fontWeight: 700, cursor: 'pointer',
            background: timerOn ? '#fef3c7' : '#fff', color: timerOn ? '#92400e' : '#374151',
            border: `1px solid ${timerOn ? '#fcd34d' : '#d1d5db'}`, borderRadius: 8,
          }}>
          {timerOn ? '⏸ 일시정지' : '⏱ 타이머 시작'}
        </button>
        <button onClick={() => { setElapsed(0); setTimerOn(false); }}
          style={{ padding: '8px 12px', fontSize: '0.82rem', background: '#fff', color: '#6b7280',
            border: '1px solid #d1d5db', borderRadius: 8, cursor: 'pointer' }}>
          ↻ 리셋
        </button>
        <button onClick={submit} disabled={!answer.trim() || disabled}
          style={{
            marginLeft: 'auto', padding: '8px 16px', fontSize: '0.85rem', fontWeight: 800, cursor: !answer.trim() || disabled ? 'not-allowed' : 'pointer',
            background: !answer.trim() || disabled ? '#e5e7eb' : '#4f46e5',
            color: !answer.trim() || disabled ? '#9ca3af' : '#fff',
            border: 'none', borderRadius: 8,
          }}>
          📝 제출하고 AI 채점
        </button>
      </div>
    </div>
  );
}

// 2차 답안 채점 결과 카드
function ScoringResultCard({ result, onRewrite, onShowModel }) {
  const pct = result.max > 0 ? (result.score / result.max) * 100 : 0;
  const tier = pct >= 70 ? '합격선' : pct >= 60 ? '통과권' : '보강 필요';
  const color = pct >= 70 ? '#16a34a' : pct >= 60 ? '#ea580c' : '#dc2626';
  return (
    <div style={{ background: '#fff', border: `2px solid ${color}`, borderRadius: 14, padding: 14, marginTop: 6 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
        <div>
          <span style={{ fontSize: '2rem', fontWeight: 800, color }}>{result.score}</span>
          <span style={{ color: '#9ca3af' }}> / {result.max}점</span>
        </div>
        <span style={{ background: color, color: '#fff', padding: '4px 10px', borderRadius: 999, fontSize: '0.78rem', fontWeight: 700 }}>
          {tier} {Math.round(pct)}%
        </span>
      </div>
      {result.completion_pct != null && (() => {
        const cp = Math.max(0, Math.min(100, result.completion_pct));
        const cpCol = cp >= 90 ? '#16a34a' : cp >= 70 ? '#ea580c' : '#dc2626';
        return (
          <div style={{ marginTop: 10, padding: '8px 10px', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 5 }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#111827' }}>🏁 완주율 (다 채웠나)</span>
              <span style={{ fontSize: '0.82rem', fontWeight: 800, color: cpCol }}>{cp}%</span>
            </div>
            <div style={{ height: 7, background: '#e5e7eb', borderRadius: 4, overflow: 'hidden' }}>
              <div style={{ width: `${cp}%`, height: '100%', background: cpCol }} />
            </div>
            {cp < 90 && (
              <div style={{ fontSize: '0.68rem', color: '#9a3412', marginTop: 4 }}>
                "잘 쓰기보다 다 쓰기" — 빈 목차·미작성 논점을 채우면 점수가 더 오릅니다.
              </div>
            )}
          </div>
        );
      })()}
      {(result.structure_score != null || result.content_score != null) && (
        <div style={{ marginTop: 10, display: 'flex', flexDirection: 'column', gap: 4 }}>
          {[
            ['구조', result.structure_score, 10, '#4f46e5'],
            ['내용', result.content_score, 15, '#10b981'],
            ['완성도', result.completeness_score, 5, '#f59e0b'],
          ].map(([label, s, max, col]) => s == null ? null : (
            <div key={label} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.74rem' }}>
              <span style={{ width: 44, color: '#374151', fontWeight: 600 }}>{label}</span>
              <div style={{ flex: 1, height: 5, background: '#f3f4f6', borderRadius: 3, overflow: 'hidden' }}>
                <div style={{ width: `${(s / max) * 100}%`, height: '100%', background: col }} />
              </div>
              <span style={{ width: 36, textAlign: 'right', color: '#6b7280' }}>{s}/{max}</span>
            </div>
          ))}
        </div>
      )}
      {(() => {
        // 득점/감점 지점(구체적 목차·논점)이 있으면 우선 표시, 없으면 강점/보강으로 폴백
        const scored = result.scored_points?.length ? result.scored_points : result.strengths;
        const lost = result.lost_points?.length ? result.lost_points : result.missed;
        const scoredLabel = result.scored_points?.length ? '✅ 득점 지점' : '✅ 강점';
        const lostLabel = result.lost_points?.length ? '➖ 감점·누락 지점' : '⚠️ 보강';
        if (!scored?.length && !lost?.length) return null;
        return (
          <div style={{ marginTop: 10, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            {scored?.length > 0 && (
              <div>
                <div style={{ fontSize: '0.74rem', fontWeight: 700, color: '#047857', marginBottom: 4 }}>{scoredLabel}</div>
                {scored.map((s, i) => <div key={i} style={{ fontSize: '0.72rem', color: '#374151', marginBottom: 2 }}>· {s}</div>)}
              </div>
            )}
            {lost?.length > 0 && (
              <div>
                <div style={{ fontSize: '0.74rem', fontWeight: 700, color: '#9a3412', marginBottom: 4 }}>{lostLabel}</div>
                {lost.map((m, i) => <div key={i} style={{ fontSize: '0.72rem', color: '#374151', marginBottom: 2 }}>· {m}</div>)}
              </div>
            )}
          </div>
        );
      })()}
      {result.rewrite_hint && (
        <div style={{ marginTop: 10, padding: 8, background: '#fffbeb', border: '1px solid #fde68a', borderRadius: 6, fontSize: '0.78rem', color: '#92400e' }}>
          💡 {result.rewrite_hint}
        </div>
      )}
      {(result.time_used_min || result.time_target_min) && (
        <div style={{ marginTop: 8, fontSize: '0.7rem', color: '#6b7280' }}>
          ⏱ {result.time_used_min || 0}분 사용 / 목표 {result.time_target_min || 0}분
        </div>
      )}
      <div style={{ display: 'flex', gap: 6, marginTop: 12 }}>
        {onShowModel && (
          <button onClick={onShowModel}
            style={{ flex: 1, padding: '8px', background: '#fff', color: '#4338ca',
              border: '1px solid #c7d2fe', borderRadius: 6, cursor: 'pointer', fontWeight: 700, fontSize: '0.8rem' }}>
            💡 모범 답안
          </button>
        )}
        {onRewrite && (
          <button onClick={onRewrite}
            style={{ flex: 1, padding: '8px', background: '#4f46e5', color: '#fff',
              border: 'none', borderRadius: 6, cursor: 'pointer', fontWeight: 700, fontSize: '0.8rem' }}>
            📝 다시 쓰기
          </button>
        )}
      </div>
    </div>
  );
}

function MessageBubble({ msg, fadeIn, leafId, leafTitle }) {
  const isUser = msg.role === 'user';
  const msgKey = `${leafId || ''}::${msg.ts || msg.content?.slice(0, 40)}`;
  const [rating, setRatingState] = useState(() => {
    try { return getMsgRatings()[msgKey]?.rating || 0; } catch { return 0; }
  });
  const [savedToNote, setSavedToNote] = useState(false);
  const rate = (val) => {
    const next = rating === val ? 0 : val;
    setRatingState(next);
    try { rateMsg(msgKey, next); } catch { /* noop */ }
  };
  const saveAsNote = () => {
    if (isUser) return;
    const title = (msg.content || '').split('\n').find((l) => l.trim())?.slice(0, 60) || 'AI 응답';
    try {
      addNote({
        kind: 'message',
        title,
        content: msg.content,
        leafId: leafId || null,
        leafTitle: leafTitle || null,
      });
      setSavedToNote(true);
      setTimeout(() => setSavedToNote(false), 2000);
    } catch { /* noop */ }
  };
  return (
    <div className={fadeIn ? 'ai-msg-fade' : ''} style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', margin: '8px 0' }}>
      <div style={{ maxWidth: isUser ? '78%' : '98%', display: 'flex', flexDirection: 'column', alignItems: isUser ? 'flex-end' : 'stretch' }}>
        <div style={{
          // AI 메시지는 거의 전체 폭(98%), 사용자 메시지는 75% — 대비 + 읽기 편의
          padding: '12px 16px',
          borderRadius: 14,
          background: isUser ? '#4f46e5' : '#f3f4f6',
          color: isUser ? '#fff' : '#111827',
          fontSize: '0.95rem',
          lineHeight: 1.6,
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        }}>
          {msg.imageUrl && (
            <img src={msg.imageUrl} alt="첨부한 문제 사진"
              style={{ maxWidth: '100%', borderRadius: 10, marginBottom: 8, display: 'block' }} />
          )}
          {isUser ? msg.content : <ParsedText text={stripAiMarkers(msg.content)} />}
        </div>
        {!isUser && (
          <div className="ai-msg-actions" style={{ display: 'flex', gap: 4, marginTop: 4, paddingLeft: 4 }}>
            <button onClick={() => rate(1)} title="이해됐어요" style={msgBtn(rating === 1 ? '#dcfce7' : '#fff', rating === 1 ? '#15803d' : '#6b7280')}>👍</button>
            <button onClick={() => rate(-1)} title="더 자세히" style={msgBtn(rating === -1 ? '#fef2f2' : '#fff', rating === -1 ? '#b91c1c' : '#6b7280')}>🤔</button>
            <button onClick={saveAsNote} title="노트로 저장" style={msgBtn(savedToNote ? '#dbeafe' : '#fff', savedToNote ? '#1d4ed8' : '#6b7280')}>
              {savedToNote ? '✓ 저장됨' : '💾'}
            </button>
            <SpeakButton text={msg.content} />
          </div>
        )}
      </div>
    </div>
  );
}
function msgBtn(bg, color) {
  return {
    padding: '3px 8px', background: bg, color,
    border: '1px solid #e5e7eb', borderRadius: 4,
    fontSize: '0.74rem', fontWeight: 700, cursor: 'pointer',
  };
}

function HistoryPanel({ leaves, onClose, onJump, onClearRoom }) {
  const [rooms, setRooms] = useState(() => getAllRooms());
  const [pick, setPick] = useState(null);
  const [query, setQuery] = useState('');
  const refresh = () => setRooms(getAllRooms());
  const leafById = useMemo(() => new Map(leaves.map((l) => [l.id, l])), [leaves]);
  const msgs = pick ? getRoomMessages(pick) : [];
  const pickLeaf = pick ? leafById.get(pick) : null;

  // 전체 단원 채팅방에서 키워드 검색 — 일치 메시지 발견된 방만 노출
  const searchHits = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return null;
    const hits = [];
    rooms.forEach((r) => {
      const arr = getRoomMessages(r.leafId);
      const matchedMsgs = arr
        .map((m, i) => ({ m, i }))
        .filter(({ m }) => (m.content || '').toLowerCase().includes(q));
      if (matchedMsgs.length > 0) {
        hits.push({ leafId: r.leafId, leaf: leafById.get(r.leafId), count: matchedMsgs.length, sample: matchedMsgs[0].m });
      }
    });
    return hits;
  }, [query, rooms, leafById]);

  const displayList = searchHits || rooms;
  return (
    <div style={{ padding: 16, background: '#fff', borderRadius: 12, border: '1px solid #e5e7eb' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <h3 style={{ margin: 0, fontSize: '1rem', display: 'flex', alignItems: 'center', gap: 6 }}>
          <Calendar size={18} /> 단원별 채팅방
        </h3>
        <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6b7280' }}>✕</button>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '6px 10px', background: '#f3f4f6', borderRadius: 8, marginBottom: 8 }}>
        <Search size={14} color="#6b7280" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="모든 채팅방에서 키워드 검색 (예: 행위능력, CVP)"
          style={{ flex: 1, border: 'none', background: 'transparent', outline: 'none', fontSize: '0.85rem' }}
        />
        {query && <button onClick={() => setQuery('')} style={{ background: 'none', border: 'none', color: '#6b7280', cursor: 'pointer', fontSize: '0.85rem' }}>✕</button>}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '180px 1fr', gap: 12 }}>
        <div style={{ maxHeight: 360, overflowY: 'auto', borderRight: '1px solid #f3f4f6', paddingRight: 8 }}>
          {displayList.length === 0 && (
            <div style={{ fontSize: '0.85rem', color: '#9ca3af', padding: '8px 0' }}>
              {query ? `"${query}" 일치 없음` : '채팅방 없음'}
            </div>
          )}
          {displayList.map((r) => {
            const leaf = r.leaf || leafById.get(r.leafId);
            const title = leaf ? leaf.path.slice(-1)[0] : r.leafId;
            const sub = leaf ? leaf.path.slice(1, -1).join(' › ') : '';
            const isHit = !!searchHits;
            return (
              <button
                key={r.leafId}
                onClick={() => setPick(r.leafId)}
                style={{
                  display: 'block', width: '100%', textAlign: 'left',
                  padding: '8px 10px', background: pick === r.leafId ? '#eef2ff' : 'transparent',
                  border: 'none', borderRadius: 6, marginBottom: 4, cursor: 'pointer',
                  fontSize: '0.85rem', color: '#111827',
                }}
              >
                <div style={{ fontWeight: 700 }}>{title}</div>
                <div style={{ fontSize: '0.7rem', color: '#6b7280' }}>{sub}</div>
                <div style={{ fontSize: '0.72rem', color: '#9ca3af', marginTop: 2 }}>
                  {isHit ? `🔍 ${r.count}건 일치` : `${r.msg_count}건 · ${(r.last_ts || '').slice(0, 16).replace('T', ' ')}`}
                </div>
              </button>
            );
          })}
        </div>
        <div style={{ maxHeight: 360, display: 'flex', flexDirection: 'column' }}>
          {!pick && <div style={{ fontSize: '0.85rem', color: '#9ca3af', padding: '8px 0' }}>채팅방 선택</div>}
          {pick && (
            <>
              <div style={{ display: 'flex', gap: 6, marginBottom: 8 }}>
                <button
                  onClick={() => { if (pickLeaf) onJump(pickLeaf); }}
                  disabled={!pickLeaf}
                  style={{ padding: '6px 10px', fontSize: '0.78rem', background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 6, cursor: pickLeaf ? 'pointer' : 'not-allowed' }}
                >
                  이 단원으로 이동
                </button>
                <InlineConfirm
                  label="이 채팅방 삭제"
                  danger
                  onYes={() => { onClearRoom(pick); setPick(null); refresh(); }}
                />
              </div>
              <div style={{ flex: 1, overflowY: 'auto' }}>
                {msgs.map((m, i) => <MessageBubble key={i} msg={m} />)}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// Quiz 오답 통계 → leaf path 매칭. App.jsx에서 미리 계산한 weakPaths를 leaf id로 변환.
function matchWeakLeaves(weakPaths, leaves) {
  if (!weakPaths || !weakPaths.length || !leaves || !leaves.length) return [];
  const byPath = new Map(leaves.map((l) => [l.path.filter(Boolean).join('|'), l]));
  const out = [];
  weakPaths.forEach((w) => {
    const candidates = [
      w.path.join('|'),
      w.path.slice(0, 3).join('|'),
      w.path.slice(0, 2).join('|'),
    ];
    for (const k of candidates) {
      const leaf = byPath.get(k);
      if (leaf) { out.push({ ...w, leaf }); break; }
    }
  });
  // 동일 leaf 중복 제거 (가장 wrong_rate 높은 항목 유지)
  const dedup = new Map();
  out.forEach((x) => {
    const prev = dedup.get(x.leaf.id);
    if (!prev || x.wrong_rate > prev.wrong_rate) dedup.set(x.leaf.id, x);
  });
  return Array.from(dedup.values()).slice(0, 5);
}

const IDLE_MS = 10 * 60 * 1000; // 10분

// 모드 아이콘(단색 lucide)/이름 — 추천 배너·모드 버튼 공용
const MODE_ICON = {
  study: BookOpen, practice: PencilLine, deep: Brain, summary: Zap, diagnose: Target, journal: PenLine, calc: Calculator,
  concept_s2: BookOpen, template: ClipboardList, topic_extract: Search, answer_write: PenLine, mock_full: Timer, calc_s2: Calculator,
};
const MODE_NAME = {
  study: '이론', practice: '문제풀이', deep: '심화', summary: '복습', diagnose: '진단', journal: '분개', calc: '계산',
  concept_s2: '개념', template: '양식', topic_extract: '논점', answer_write: '답안', mock_full: '실전', calc_s2: '계산',
};

// 🧭 실시간 학습 추천 — 현재 단원의 실력 신호로 '다음에 누를 모드'를 고른다.
// 학습과학 흐름: (기록없음→진단) 이해부족→이론 · 이해했으면→문제풀이(인출) · 틀리면→심화 · 오래되면→복습.
function recommendMode({ m, qs, isDue, stage, subjectId }) {
  const cov = m?.coverage || 0;
  const attempted = (m?.attempted || 0) + (qs?.answered || 0);
  const acc = (qs && qs.answered) ? qs.accuracy : (m?.accuracy || 0);
  const box = m?.srs_box || 0;
  const mastered = m?.status === 'mastered';
  const pct = (x) => Math.round(x * 100);

  if (stage === 2) {
    if (cov < 0.4) return { mode: 'concept_s2', reason: '아직 논점 개념이 얕아요 — 개념 도입부터 시작하세요.' };
    if (attempted < 1) return { mode: 'template', reason: '개념은 잡혔어요 — 답안 골격(양식)을 외울 때입니다.' };
    if (acc && acc < 0.6) return { mode: 'topic_extract', reason: '논점 포착이 약해요 — 사례로 논점 뽑기를 연습하세요.' };
    if (!mastered) return { mode: 'answer_write', reason: '이제 실제로 답안을 써서 채점받아 볼 때입니다.' };
    return { mode: 'mock_full', reason: '완성 단계 — 실전 타이머로 굳히세요.', done: true };
  }
  // 1차
  if (isDue) return { mode: 'summary', reason: '복습 시기가 됐어요 — 기억이 옅어지기 전에 핵심만 빠르게 다지기.' };
  if (cov < 0.15 && attempted === 0) return { mode: 'diagnose', reason: '아직 학습 기록이 없어요 — OX 5문제로 지금 실력부터 진단해요.' };
  if (cov < 0.45) return { mode: 'study', reason: `이론 이해가 ${pct(cov)}%로 아직 낮아요 — 개념부터 배우세요.` };
  if (attempted < 3) return { mode: 'practice', reason: '이론은 익혔어요 — 기출을 풀어 인출·적용으로 확인할 때.' };
  if (acc < 0.6) {
    const calcSubj = subjectId === 'accounting' || subjectId === 'economics';
    return { mode: 'deep', reason: `정답률이 ${pct(acc)}%예요 — 함정·판례 심화로 약점을 보강하세요.`, alt: calcSubj ? 'calc' : null };
  }
  if (box < 2 && !mastered) return { mode: 'summary', reason: '잘하고 있어요 — 핵심 압축 복습으로 굳히고 회독을 올리세요.' };
  if (mastered) return { mode: 'summary', reason: '이 단원 완성 ✓ — 가끔 복습으로 유지하고 다음 단원으로 넘어가도 좋아요.', done: true };
  return { mode: 'practice', reason: '꾸준히 문제로 감각을 유지하세요.' };
}

export default function AILearning({ isTabRoot, browseExam, weakPaths, weakPathsBySubject, leavesBySubject: leavesBySubjectProp, onJumpToBrowse, getQuizCountForLeaf, quizStatsByLeaf }) {
  useEffect(() => { migrateLegacyCivilIds(); }, []);
  const isDesktop = useIsDesktop();
  const [showDoc, setShowDoc] = useState(true); // 데스크톱 3단: 우측 패널 표시
  const [docTab, setDocTab] = useState('doc');   // 우측 패널 탭: doc(이론) | ox | mem | progress
  const [maskHl, setMaskHl] = useState(false);   // 형광펜 가리기(암기 시트) 모드
  const [byok, setByokState] = useState(getByok());
  const [prefs, setPrefsState] = useState(getPrefs());
  // 로컬(Ollama) 설치 모델 자동감지 — 드롭다운 선택지로만 노출(기본은 Kimi). 자동 전환 안 함.
  const [localModels, setLocalModels] = useState([]);
  useEffect(() => { let dead = false; discoverLocalModels().then((m) => { if (!dead) setLocalModels(m); }); return () => { dead = true; }; }, []);
  const [indexMeta, setIndexMeta] = useState(null);
  const [leaves, setLeaves] = useState([]);
  const initCur = getCurrent();
  // 저장된 subject가 잘못됐을 수 있어(레거시 하드코딩) leaf_id의 prefix에서 과목을 우선 도출.
  const [subjectId, setSubjectId] = useState(
    (initCur?.leaf_id || '').split('__')[0] || initCur?.subject || 'civil'
  );
  const [current, setCurrentState] = useState(initCur);
  // 자체 홈 화면 ↔ 학습 화면.
  // 마지막에 보던 단원이 있으면 그 학습 화면으로 자동 복원 (재진입 시 "초기화된 듯" 보이는 문제 해결).
  const [aiView, setAiView] = useState(() => (initCur?.leaf_id ? 'study' : 'home')); // 'home' | 'study'
  const [mastery, setMasteryState] = useState(getMastery());
  const [handoverMd, setHandoverMd] = useState('');
  const [unitMd, setUnitMd] = useState('');
  const [sectionMd, setSectionMd] = useState('');
  // 🎓 합격수기 78건 기반 과목별 공부법 — 튜터 프롬프트에 얹어 '합격자처럼' 강조점·암기법 반영
  const [passInsights, setPassInsights] = useState(null);
  useEffect(() => { loadPassInsights().then((d) => { if (d) setPassInsights(d); }); }, []);
  // 교재 슬라이스를 이론/OX/암기로 분리 — 우측 패널 탭 구성에 사용
  const docParts = useMemo(() => splitDocTabs(sectionMd || unitMd), [sectionMd, unitMd]);
  // 인출 대기(오답 + 복습 만기) 개수 — 탭 배지에 쓴다. 문항을 풀 때마다 갱신되도록
  // docTab·sectionMd 변화에 얹어 다시 센다(로컬 저장소 읽기라 비용이 없다).
  const drillN = useMemo(() => {
    const c = getDrillCounts();
    return c.wrong + c.due;
  }, [docTab, sectionMd]);
  // 상단 헤더 실폭 감지 — 교재 패널을 열면 가운데가 좁아져 아이콘이 겹치므로 단계적으로 감춘다.
  // 콜백 ref — 헤더는 과목 진입 후에야 렌더되므로 useEffect([])로는 옵저버가 붙지 않는다.
  const headRoRef = useRef(null);
  const [headW, setHeadW] = useState(1200);
  const headerRef = useCallback((node) => {
    if (headRoRef.current) { headRoRef.current.disconnect(); headRoRef.current = null; }
    if (node && typeof ResizeObserver !== 'undefined') {
      setHeadW(node.getBoundingClientRect().width);
      const ro = new ResizeObserver((entries) => {
        for (const e of entries) setHeadW(e.contentRect.width);
      });
      ro.observe(node);
      headRoRef.current = ro;
    }
  }, []);
  const tight = headW < 560;       // 저장·불러오기·초기화(파일/삭제) 숨김
  const veryTight = headW < 440;   // 채팅방 달력까지 숨김
  const ICON_BTN = { background: 'none', border: 'none', cursor: 'pointer', padding: 4, flex: '0 0 auto' };
  const [problemsMd, setProblemsMd] = useState('');
  const [lectureMd, setLectureMd] = useState('');   // 관 × 회독별 강의 필기(유닛 파일 전체)
  // 이 관의 강의 필기를 탭별로 미리 나눠 둔다.
  // 앵커가 `🧠 암기법` 같은 다른 탭의 소제목을 가리키면 이론 맨 뒤로 밀리는데,
  // 그러면 정작 그 내용이 있어야 할 암기 탭에는 없고 이론 끝에 뜬금없이 붙는다.
  const lectureByTab = useMemo(
    () => splitLectureByTab(sectionMd || unitMd,
                            stripLectureCitations(sliceLectureNote(lectureMd, current?.leaf_id))),
    [sectionMd, unitMd, lectureMd, current?.leaf_id],
  );
  const [showLectureNote, setShowLectureNote] = useState(false);
  const [mode, setMode] = useState('study'); // 'study' | 'practice' | 'deep' | 'summary' | 'diagnose'
  const [pendingNext, setPendingNext] = useState(null);
  const [due, setDue] = useState(() => getDueChapters());
  // 커리큘럼 스텝 딥링크 — mount 시 저장된 AI 모드/문서탭으로 1회 진입(과목 진입 로직 정착 후 적용).
  useEffect(() => {
    let j = null;
    try { j = JSON.parse(localStorage.getItem('ailearn-jump') || 'null'); } catch { j = null; }
    if (!j) return;
    try { localStorage.removeItem('ailearn-jump'); } catch { /* noop */ }
    const S1 = ['study', 'practice', 'deep', 'summary', 'diagnose', 'journal', 'calc'];
    const S2 = ['concept_s2', 'template', 'topic_extract', 'answer_write', 'mock_full', 'calc_s2'];
    const timer = setTimeout(() => {
      if (j.mode) {
        const st = SUBJECTS.find((s) => s.id === subjectId)?.stage || 1;
        if ((st === 2 ? S2 : S1).includes(j.mode)) setMode(j.mode);
      }
      if (j.docTab) setDocTab(j.docTab);
    }, 80);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  // 📷 문제 사진 첨부 — 이번 전송 1회용 {dataUrl, media_type, data}
  const [pendingImage, setPendingImage] = useState(null);
  const attachImage = useCallback((file) => {
    if (!file || !file.type.startsWith('image/')) return;
    const fr = new FileReader();
    fr.onload = () => {
      const imgEl = new Image();
      imgEl.onload = () => {
        // Claude vision 권장 한도(1568px)로 축소 + JPEG 재인코딩 (용량·토큰 절약)
        const MAX = 1568;
        const scale = Math.min(1, MAX / Math.max(imgEl.width, imgEl.height));
        const cv = document.createElement('canvas');
        cv.width = Math.round(imgEl.width * scale);
        cv.height = Math.round(imgEl.height * scale);
        cv.getContext('2d').drawImage(imgEl, 0, 0, cv.width, cv.height);
        const dataUrl = cv.toDataURL('image/jpeg', 0.85);
        setPendingImage({ dataUrl, media_type: 'image/jpeg', data: dataUrl.split(',')[1] });
      };
      imgEl.src = fr.result;
    };
    fr.readAsDataURL(file);
  }, []);
  const [streaming, setStreaming] = useState(false);
  const [draft, setDraft] = useState('');
  const [error, setError] = useState('');
  const [lastFailedText, setLastFailedText] = useState('');
  const [lastTruncated, setLastTruncated] = useState(false); // ✂️ 마지막 답변이 한도로 잘렸는지 // 전송 실패 시 재시도용
  const [thinkSec, setThinkSec] = useState(0); // 비스트리밍 대기 경과초
  const [showHistory, setShowHistory] = useState(false);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  // 5과목 leaves 캐시 — App.jsx에서 미리 받아둔 props 사용. fallback으로 자체 fetch.
  const [leavesBySubject, setLeavesBySubject] = useState(leavesBySubjectProp || {});
  useEffect(() => {
    if (leavesBySubjectProp) setLeavesBySubject(leavesBySubjectProp);
  }, [leavesBySubjectProp]);
  useEffect(() => {
    setLeavesBySubject((prev) => ({ ...prev, [subjectId]: leaves }));
  }, [subjectId, leaves]);
  useEffect(() => {
    if (!showAnalytics) return;
    SUBJECTS.forEach((s) => {
      if (leavesBySubject[s.id]) return;
      fetch(indexUrl(s.id)).then((r) => r.json()).then((raw) => {
        const idx = raw?.stage === 2 ? normalizeStage2Index(raw) : raw;
        setLeavesBySubject((prev) => ({ ...prev, [s.id]: idx.leaves || [] }));
      }).catch(() => {});
    });
  }, [showAnalytics]); // eslint-disable-line
  // 홈 화면: 과목 카드의 대분류 버튼을 위해 1차 과목 leaves 미리 로드
  useEffect(() => {
    if (aiView !== 'home') return;
    SUBJECTS_BY_STAGE[1].forEach((s) => {
      if (leavesBySubject[s.id]?.length) return;
      fetch(indexUrl(s.id)).then((r) => r.json()).then((raw) => {
        const idx = raw?.stage === 2 ? normalizeStage2Index(raw) : raw;
        setLeavesBySubject((prev) => ({ ...prev, [s.id]: idx.leaves || [] }));
      }).catch(() => {});
    });
  }, [aiView]); // eslint-disable-line
  const [sessionId, setSessionId] = useState(null);
  const [idlePromptShown, setIdlePromptShown] = useState(false);
  const [weakSuggestion, setWeakSuggestion] = useState([]);
  const [confirmAction, setConfirmAction] = useState(null); // {label, onYes}
  const [recentRooms, setRecentRooms] = useState(() => getAllRooms());
  // 헤더 단원 박스 클릭 → LeafPicker 모달
  const [showLeafPickerModal, setShowLeafPickerModal] = useState(false);
  useScrollLock(showLeafPickerModal);
  useEscClose(showLeafPickerModal, () => setShowLeafPickerModal(false));
  // 2차 실전 모의 세션 — null | { startedAt, totalMin, curQ, totalQ, scoreDist, scores: [{q, score, max, time_used_min}] }
  const [mockSession, setMockSession] = useState(null);
  const [mockTick, setMockTick] = useState(0);
  useEffect(() => {
    if (!mockSession) return;
    const t = setInterval(() => setMockTick((x) => x + 1), 1000);
    return () => clearInterval(t);
  }, [mockSession]);
  const abortRef = useRef(null);
  const scrollRef = useRef(null);
  const stickBottomRef = useRef(true); // 채팅 자동 스크롤: 바닥 근처 여부
  const inputRef = useRef(null); // 전송 후 포커스 복원용
  const idleTimerRef = useRef(null);
  const importInputRef = useRef(null); // 세이브파일 불러오기용 숨김 input

  // 인덱스·인수인계서 로드 — subjectId 변경 시 재로드
  useEffect(() => {
    // dead 플래그: 과목 A→B 빠른 전환 시 A 응답이 늦게 도착해 B의 leaves/current/handover 를
    // 덮어써 '화면은 B, LLM 컨텍스트는 A' 가 되는 크로스-과목 오염 방지.
    let dead = false;
    fetch(indexUrl(subjectId)).then((r) => r.json()).then((raw) => {
      if (dead) return;
      const idx = raw?.stage === 2 ? normalizeStage2Index(raw) : raw;
      setIndexMeta(idx);
      setLeaves(idx.leaves || []);
      // 대분류(division) 진입 대기 스코프가 있으면 그것을 원자적으로 적용(default_leaf보다 우선).
      const pend = pendingScopeRef.current;
      if (pend) {
        pendingScopeRef.current = null;
        const div = pend.division;
        const tops = div ? (div.tops || (div.label ? [div.label] : null)) : null;
        const lf = (idx.leaves || []).find((l) => l.id === pend.leafId)
          || (tops ? (idx.leaves || []).find((l) => tops.includes(l.path && l.path[0])) : null)
          || (idx.default_leaf && (idx.leaves || []).find((l) => l.id === idx.default_leaf))
          || (idx.leaves || [])[0];
        if (lf) {
          const next = { subject: subjectId, leaf_id: lf.id, division: div ? (div.label || null) : null, divisionTops: tops };
          setCurrentState(next); setCurrent(next);
        }
        return;
      }
      const subjectChanged = current?.subject !== subjectId;
      const exists = !subjectChanged && current?.leaf_id && (idx.leaves || []).some((l) => l.id === current.leaf_id);
      // 저장된 단원이 인덱스에 없더라도 채팅 기록이 남아 있으면 덮어쓰지 않는다.
      // (인덱스 변동·타이밍으로 current가 기본 단원으로 리셋되어 이전 대화가 안 보이던 문제 방지)
      const hasRoom = !subjectChanged && current?.leaf_id && getRoomMessages(current.leaf_id).length > 0;
      if ((subjectChanged || (!exists && !hasRoom)) && idx.default_leaf) {
        const def = idx.leaves.find((l) => l.id === idx.default_leaf) || idx.leaves[0];
        if (def) {
          const next = { subject: subjectId, leaf_id: def.id };
          setCurrentState(next);
          setCurrent(next);
        }
      }
    }).catch((e) => { if (!dead) setError('단원 인덱스를 불러오지 못했습니다: ' + e.message); });
    fetch(handoverUrl(subjectId)).then((r) => r.text()).then((md) => { if (!dead) setHandoverMd(md); }).catch(() => { if (!dead) setHandoverMd(''); });
    pruneOldConversations(7);
    return () => { dead = true; };
  }, [subjectId]); // eslint-disable-line

  // leaf 자료 로드 (section_lines 슬라이스)
  useEffect(() => {
    if (!current?.leaf_id || leaves.length === 0) return undefined;
    const leaf = leaves.find((l) => l.id === current.leaf_id);
    if (!leaf || !leaf.unit_file) { setUnitMd(''); setSectionMd(''); return undefined; }
    setActiveLeaf({ subject: subjectId, leafId: leaf.id, leafTitle: leaf.title || '' });
    let dead = false; // 빠른 단원 전환 시 이전 leaf 자료가 늦게 도착해 덮어쓰는 것 방지
    fetch(studyBase(subjectId) + leaf.unit_file).then((r) => r.text()).then((md) => {
      if (dead) return;
      setUnitMd(md);
      if (leaf.section_key && leaf.section_key !== 'full' && leaf.section_lines) {
        setSectionMd(sliceSection(md, { lines: leaf.section_lines }));
      } else {
        setSectionMd('');
      }
    }).catch((e) => { if (!dead) setError('단원 자료 로드 실패: ' + e.message); });
    return () => { dead = true; };
  }, [current?.leaf_id, leaves, subjectId]);

  // 문제·기출 자료 로드 — 1차 practice, 2차 answer_write / mock_full / topic_extract 모드에서
  useEffect(() => {
    const needs = mode === 'practice' || mode === 'answer_write' || mode === 'mock_full' || mode === 'topic_extract';
    if (!needs || !current?.leaf_id) { setProblemsMd(''); return undefined; }
    const leaf = leaves.find((l) => l.id === current.leaf_id);
    if (!leaf || !leaf.problems_file) { setProblemsMd(''); return undefined; }
    let dead = false; // 빠른 단원/모드 전환 시 이전 leaf 문제자료가 늦게 덮어쓰는 것 방지
    fetch(studyBase(subjectId) + leaf.problems_file).then((r) => r.text()).then((md) => { if (!dead) setProblemsMd(md); }).catch(() => { if (!dead) setProblemsMd(''); });
    return () => { dead = true; };
  }, [mode, current?.leaf_id, leaves, subjectId]);

  // 강의 필기 로드 — 관 × 회독별. 모드 탭을 바꾸면 그 회독의 강의 필기로 갈아끼운다.
  // 아직 만들어지지 않은 관·회독이 대부분이므로 404는 조용히 빈 문자열 처리한다.
  useEffect(() => {
    if (!current?.leaf_id || leaves.length === 0) { setLectureMd(''); return undefined; }
    const leaf = leaves.find((l) => l.id === current.leaf_id);
    const unitCode = leaf?.unit_code;
    if (!unitCode) { setLectureMd(''); return undefined; }
    const phase = modeToPhase(mode);
    let dead = false;
    fetch(`${studyBase(subjectId)}lectures/notes/${unitCode}.${phase}.md`)
      .then((r) => (r.ok ? r.text() : ''))
      .then((md) => { if (!dead) setLectureMd(md || ''); })
      .catch(() => { if (!dead) setLectureMd(''); });
    return () => { dead = true; };
  }, [mode, current?.leaf_id, leaves, subjectId]);

  // 2차 template 모드 — 자료 로드
  // 이론: templates/_all.md (답안 양식 61개)
  // 법규: meta/cases.md (판례 카드)
  useEffect(() => {
    if (mode !== 'template') return;
    if (problemsMd) return;
    if (subjectId === 'appraisal_theory') {
      fetch(studyBase(subjectId) + 'templates/_all.md').then((r) => r.text()).then(setProblemsMd).catch(() => {});
    } else if (subjectId === 'appraisal_law') {
      fetch(studyBase(subjectId) + 'meta/cases.md').then((r) => r.text()).then(setProblemsMd).catch(() => {});
    }
  }, [mode, subjectId, problemsMd]);

  // leaf 전환 시 해당 단원의 채팅방 로드. streaming은 중단·입력·idle 초기화.
  useEffect(() => {
    stickBottomRef.current = true; // 단원 전환 시 바닥으로
    if (!current?.leaf_id) { setMessages([]); return; }
    setMessages(getRoomMessages(current.leaf_id));
    setPendingNext(null);
    setIdlePromptShown(false);
    setLastTruncated(false); // 단원 전환 시 이전 단원의 '이어쓰기' 플래그가 새 단원에 누출되지 않게
    setInput('');
    if (abortRef.current) abortRef.current.abort();
    if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
  }, [current?.leaf_id]);

  // 대기 경과초 카운터 (특히 비스트리밍 모드에서 진행 단서 제공)
  useEffect(() => {
    if (!streaming) { setThinkSec(0); return undefined; }
    setThinkSec(0);
    const t = setInterval(() => setThinkSec((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, [streaming]);

  // 채팅 stick-to-bottom: 사용자가 바닥 근처일 때만 자동 스크롤.
  // 위로 올려 이전 내용을 읽는 중이면 스트리밍 토큰이 와도 끌어내리지 않음.
  useEffect(() => {
    if (stickBottomRef.current && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, draft]);

  // 메시지 변동 시 최근 방 목록 갱신
  useEffect(() => { setRecentRooms(getAllRooms()); }, [messages]);

  // 이전/다음 leaf 계산 (taxonomy index 순)
  // 활성 대분류(division)로 학습 범위를 한정(scope). null이면 과목 전체.
  // 홈에서 '민법총칙'·'미시경제' 등 대분류 버튼으로 들어오면 그 분류 단원만 다룬다.
  const activeDivision = current?.division || null; // 표시용 라벨
  // 실제 필터용: 묶인 path[0] 집합. 구버전 호환(divisionTops 없으면 division 단일값 사용).
  const activeTops = current?.divisionTops || (activeDivision ? [activeDivision] : null);
  const scopedLeaves = activeTops
    ? leaves.filter((l) => activeTops.includes(l.path && l.path[0]))
    : leaves;
  const curIndex = scopedLeaves.findIndex((l) => l.id === current?.leaf_id);
  const prevLeaf = curIndex > 0 ? scopedLeaves[curIndex - 1] : null;
  const nextLeaf = curIndex >= 0 && curIndex < scopedLeaves.length - 1 ? scopedLeaves[curIndex + 1] : null;

  // 취약 leaf 매칭 — 과목별 dict 우선, 단일 props weakPaths fallback
  useEffect(() => {
    if (!leaves.length) return;
    const src = (weakPathsBySubject && weakPathsBySubject[subjectId]) || weakPaths || [];
    const matched = matchWeakLeaves(src, leaves);
    setWeakSuggestion(matched);
  }, [leaves, weakPaths, weakPathsBySubject, subjectId]);

  // 과목 전환 헬퍼
  // 과목 전환 후 인덱스가 로드되면 적용할 '대기 스코프'(division 진입). setTimeout 경쟁 제거용.
  const pendingScopeRef = useRef(null); // { leafId, division:{label,tops} } | null
  const switchSubject = (sid, enterStudy = false) => {
    if (sid === subjectId && !enterStudy) return;
    if (abortRef.current) abortRef.current.abort();
    setSubjectId(sid);
    setMessages([]);
    setUnitMd(''); setSectionMd(''); setProblemsMd('');
    setPendingNext(null); setIdlePromptShown(false); setInput('');
    setMockSession(null); // 과목 전환 시 진행 중 모의 세션 정리 (다른 과목 맥락 잔존 방지)
    // stage 전환 시 적합한 default 모드로
    const nextStage = SUBJECTS.find((s) => s.id === sid)?.stage || 1;
    const stage1Modes = ['study', 'practice', 'deep', 'summary', 'diagnose', 'journal', 'calc'];
    const stage2Modes = ['concept_s2', 'template', 'topic_extract', 'answer_write', 'mock_full', 'calc_s2'];
    if (nextStage === 2 && !stage2Modes.includes(mode)) setMode('concept_s2');
    else if (nextStage === 1 && !stage1Modes.includes(mode)) setMode('study');
    if (enterStudy) setAiView('study');
  };

  // 응답 끝나면 10분 idle 타이머 시작. 다음 user 메시지·언마운트·세션 종료 시 clear.
  const armIdleTimer = useCallback(() => {
    if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
    idleTimerRef.current = setTimeout(() => {
      setIdlePromptShown(true);
    }, IDLE_MS);
  }, []);
  const clearIdleTimer = useCallback(() => {
    if (idleTimerRef.current) { clearTimeout(idleTimerRef.current); idleTimerRef.current = null; }
    setIdlePromptShown(false);
  }, []);
  useEffect(() => () => clearIdleTimer(), [clearIdleTimer]);

  // division 인자: undefined=현재 스코프 유지(이전/다음 이동 등) / null=해제 / {label,tops}=새 스코프
  const pickLeaf = (leaf, division = undefined) => {
    // 과목은 leaf id prefix에서 도출 (이전엔 'civil' 하드코딩 버그).
    const sid = (leaf?.id || '').split('__')[0] || subjectId || 'civil';
    let label = null, tops = null;
    if (division === undefined) {            // 유지
      label = current?.division || null;
      tops = current?.divisionTops || (current?.division ? [current.division] : null);
    } else if (division) {                    // 새 스코프
      label = division.label || null;
      tops = division.tops || (division.label ? [division.label] : null);
    }                                         // division === null → 해제(label·tops null)
    const next = { subject: sid, leaf_id: leaf.id, division: label, divisionTops: tops };
    setCurrentState(next);
    setCurrent(next);
  };

  // 홈 대분류 버튼 → 그 분류로 진입(범위 한정). division = path[0] 원문.
  const jumpToLeaf = (sid, leaf, division = null) => {
    if (!leaf) return;
    if (sid !== subjectId) {
      // 과목 전환: 인덱스 로드 후 원자적으로 스코프 적용(경쟁 없음).
      pendingScopeRef.current = { leafId: leaf.id, division };
      switchSubject(sid, true);
    } else {
      setAiView('study');
      pickLeaf(leaf, division);
    }
  };
  // 과목 전체 학습 진입 — 대분류 스코프 해제
  const enterSubjectWhole = (sid) => {
    if (sid !== subjectId) { switchSubject(sid, true); return; } // 타 과목: default_leaf가 division 없이 설정됨
    setAiView('study');
    if (current?.division && current?.leaf_id) {
      const lf = leaves.find((l) => l.id === current.leaf_id) || { id: current.leaf_id };
      pickLeaf(lf, null);
    }
  };
  // 학습 화면에서 현재 단원은 유지하고 분류 스코프만 해제(전체 보기)
  const clearDivision = () => {
    if (!current?.division || !current?.leaf_id) return;
    const lf = leaves.find((l) => l.id === current.leaf_id) || { id: current.leaf_id };
    pickLeaf(lf, null);
  };
  // 과목의 대분류(path[0]) 목록 — 각 그룹의 첫 leaf로 진입할 수 있게 반환
  // DIV_EXCLUDE: 홈 버튼에서 숨길 대분류 (학습 화면 단원 트리에선 그대로 접근 가능)
  const divisionsFor = (sid) => {
    const lvs = (leavesBySubject[sid]?.length ? leavesBySubject[sid] : (sid === subjectId ? leaves : [])) || [];
    // 그룹 정의가 있으면 그룹 단위로 (여러 path[0]를 한 버튼으로 묶음)
    const groups = DIV_GROUPS[sid];
    if (groups) {
      return groups
        .map((g) => ({ label: g.label, tops: g.tops, leaf: lvs.find((l) => g.tops.includes(l.path && l.path[0])) }))
        .filter((g) => g.leaf);
    }
    // 그룹 정의가 없으면 path[0]별 자동 (각자 단일 그룹)
    const ex = DIV_EXCLUDE[sid];
    const map = new Map();
    for (const l of lvs) {
      const top = l.path && l.path[0];
      if (!top || map.has(top)) continue;
      if (ex && ex.has(top)) continue;
      map.set(top, l);
    }
    return Array.from(map, ([top, leaf]) => ({ label: top, tops: [top], leaf }));
  };
  const cleanDivLabel = (s) => {
    const raw = String(s || '');
    if (DIV_LABEL_MAP[raw]) return DIV_LABEL_MAP[raw];
    return raw.replace(/^PART\s*\d+\s*/i, '').replace(/^Chapter\s*\d+\s*/i, '').trim();
  };

  const startNewSession = () => {
    const id = uid();
    addSession({
      id,
      date: todayStr(),
      code: current?.leaf_id,
      section_key: 'full',
      started_at: new Date().toISOString(),
      ended_at: null,
      msg_count: 0,
      summary: null,
    });
    setSessionId(id);
  };

  const send = useCallback(async (overrideText, opts = {}) => {
    const isRegen = !!opts.regenerate; // 🔄 답변 다시 생성 — 마지막 응답을 버리고 같은 질문 재요청
    setError('');
    const img = isRegen ? null : pendingImage; // 📷 첨부 사진 (이번 전송에만 사용, 재생성엔 미사용)
    let text = (typeof overrideText === 'string' ? overrideText : input).trim();
    if (img && !text) text = '이 문제(사진)를 단계별로 풀이해주고, 어떤 단원·논점인지 알려줘.';
    if (!text || streaming) return;
    const cap = canSendMessage();
    if (!cap.ok) {
      setError(`오늘 메시지 cap(${prefs.daily_cap})에 도달했습니다. 설정에서 cap을 늘리거나 내일 다시 시도하세요.`);
      return;
    }
    if (typeof navigator !== 'undefined' && navigator.onLine === false) {
      setError('오프라인 상태입니다. AI 학습 탭은 인터넷 연결이 필요합니다.');
      return;
    }
    if (!sessionId) startNewSession();

    clearIdleTimer();
    if (!current?.leaf_id) { setError('단원을 먼저 선택하세요.'); setStreaming(false); return; }
    const sendLeafId = current.leaf_id; // 응답 저장 대상 고정 (전송 중 단원 전환 레이스 방지)
    // 사진은 localStorage 용량 문제로 저장본에는 텍스트 표식만 남기고,
    // 화면(imageUrl)·이번 API 호출에만 실데이터를 사용한다.
    let regenPopped = null; // 재생성 실패 시 기존 답변 복원용
    if (isRegen) {
      // 저장소·화면 양쪽에서 마지막 assistant 응답 제거 → 히스토리가 user로 끝나게
      const roomArr = getRoomMessages(sendLeafId);
      if (roomArr.length && roomArr[roomArr.length - 1].role === 'assistant') regenPopped = popRoomMessage(sendLeafId);
      setMessages((arr) => {
        const a = [...arr];
        if (a.length && a[a.length - 1].role === 'assistant') a.pop();
        return a;
      });
    } else {
      const userMsg = { role: 'user', content: (img ? '[📷 문제 사진 첨부]\n' : '') + text };
      appendRoomMessage(sendLeafId, userMsg);
      setMessages((arr) => [...arr, { ...userMsg, ts: new Date().toISOString(), imageUrl: img?.dataUrl }]);
      setPendingImage(null);
      if (typeof overrideText !== 'string') setInput('');
    }
    stickBottomRef.current = true; // 내가 보냈으면 바닥으로
    setLastFailedText('');
    setError('');
    setStreaming(true);
    setDraft('');

    const curLeaf = leaves.find((l) => l.id === current?.leaf_id);
    // 진척은 지금 보고 있는 회독 기준으로 튜터에게 알린다 — 1회독 학생과 3회독 학생에게
    // 같은 깊이로 말하면 안 되기 때문이다.
    const curPhase = modeToPhase(mode);
    const curMastery = current ? getChapterMastery(current.leaf_id, curPhase) : null;
    const lastSession = getSessions().slice(-2, -1)[0];
    let recentSummary = lastSession?.summary || '';
    // 🔁 퀴즈 탭 반복 오답(miss≥2) 카드 → 튜터가 대화 중 자연스럽게 재설명·확인하도록 주입
    try {
      const memAll = JSON.parse(localStorage.getItem('quiz-mem-v1') || '{}');
      const srsMap = memAll[sendLeafId]?.srs || {};
      const weak = (loadChatCards()[sendLeafId] || [])
        .filter(c => (srsMap[c.term.replace(/\s+/g, '')]?.miss || 0) >= 2)
        .slice(0, 5).map(c => c.term);
      if (weak.length) {
        recentSummary += `\n[퀴즈 반복 오답] 학생이 암기 퀴즈에서 거듭 틀린 포인트: ${weak.join(', ')} — 이번 대화에서 기회가 되면 자연스럽게 다시 설명하고 이해를 확인하는 질문을 하라.`;
      }
    } catch { /* noop */ }
    const subjStage = getSubjectMeta(subjectId)?.stage || 1;
    // problems 자료 조건부 로딩 — 항상 보내면 캐시 한 자리(약 10K 토큰)를 점유.
    //  · 1차 practice / 2차 mock_full 은 항상 (문제풀이가 주 활동)
    //  · 2차 answer_write / topic_extract / template 은 사용자 메시지에 트리거 키워드 있을 때만
    const triggerWords = /(문제|기출|출제|사례|판례|양식|풀어|풀자|새\s*문제|다른\s*문제|모범\s*답안|채점)/;
    const userText = text || '';
    const triggered = triggerWords.test(userText);
    const usesProblems =
      (subjStage === 1 && mode === 'practice') ||
      (subjStage === 2 && mode === 'mock_full') ||
      (subjStage === 2 && (mode === 'answer_write' || mode === 'topic_extract' || mode === 'template') && triggered);
    const system = buildSystemBlocks({
      handoverMd,                            // ← 캐시 안정: 텍스트 불변
      unitMd: sectionMd ? '' : unitMd,
      sectionMd,
      problemsMd: usesProblems ? problemsMd : '',
      lectureMd: sliceLectureNote(lectureMd, current?.leaf_id),
      phase: curPhase,
      mode,
      currentMastery: curMastery,
      // 교재만 주던 AI에게 ① 문항 성적 ② 학생이 직접 쓴 노트·약점을 함께 준다 — 개인화해 약한 곳부터 짚게 한다.
      recentSummary: recentSummary
        + buildLearnerStatus(current?.leaf_id, curLeaf?.title)
        + buildPersonalNotes(getSubjectMeta(subjectId)?.tax_key || getSubjectMeta(subjectId)?.title || '', curLeaf?.title, getNotes()),
      leafPath: curLeaf ? curLeaf.path.join(' / ') : '',
      stage: subjStage,
      subjectId,
      passInsights: passInsightBlock(passInsights, subjectId, subjStage), // 합격수기 기반 과목별 공부법
    });

    // 대화 히스토리 캐싱:
    //  - 윈도우 25개 (기존 13 → 25). 같은 단원에서 25개까지는 캐시 prefix 안정.
    //  - 마지막 6개는 캐시 안 함 (새 메시지가 계속 들어오는 꼬리 영역).
    //  - 전체 방 메시지가 윈도우를 넘는 순간 prefix 가 매 라운드 한 칸씩 밀려 캐시 미스만 발생 → 그 경우 캐싱 비활성.
    const HISTORY_WINDOW = 25;
    const CACHE_TAIL_KEEP = 6;
    const allRoomMsgs = getRoomMessages(current.leaf_id);
    const history = [...allRoomMsgs].slice(-HISTORY_WINDOW);
    const cacheStable = allRoomMsgs.length <= HISTORY_WINDOW;
    const cacheCut = history.length - CACHE_TAIL_KEEP - 1;
    const apiMessages = history.map((m, i) => {
      if (cacheStable && i === cacheCut && cacheCut >= 1) {
        return {
          role: m.role,
          content: [{ type: 'text', text: m.content, cache_control: { type: 'ephemeral', ttl: '1h' } }],
        };
      }
      return { role: m.role, content: m.content };
    });
    // 📷 이번 전송에 사진이 있으면 마지막 user 메시지를 vision 블록으로 교체 (Claude 형식)
    if (img && apiMessages.length) {
      const lastIdx = apiMessages.length - 1;
      const lastText = typeof apiMessages[lastIdx].content === 'string'
        ? apiMessages[lastIdx].content : text;
      apiMessages[lastIdx] = {
        role: 'user',
        content: [
          { type: 'image', source: { type: 'base64', media_type: img.media_type, data: img.data } },
          { type: 'text', text: lastText },
        ],
      };
    }

    const ac = new AbortController();
    abortRef.current = ac;
    try {
      // 기본: 비-스트리밍(한 번에 받기) — 매 chunk 마다 KaTeX/표 재파싱으로 인한 프레임 드롭 회피.
      // prefs.streaming === true 일 때만 토큰별 흐름 표시.
      const useStream = !!prefs.streaming;
      // 모드별 최대 출력 토큰 — summary/diagnose는 짧게, deep는 길게
      // 모드별 출력 cap — 학습 경험 우선. 응답이 잘리지 않을 정도로 여유 있게.
      const modeMaxTokens = {
        // 1차
        summary: 600, diagnose: 900, deep: 1800, practice: 1500, study: 1200,
        // 2차
        concept_s2: 1400, template: 1000, topic_extract: 1300,
        answer_write: 1800, mock_full: 1600, calc_s2: 1300,
      };
      const effectiveMax = prefs.max_tokens || modeMaxTokens[mode] || 1200;
      // 모델에 따라 프로바이더 자동 선택 (claude/gpt/gemini).
      // OpenAI·Gemini 는 보통 CORS 차단되지만, 일부 환경(extension, 프록시 헤더, 정책 변경)에서 통과될 수 있어 일단 시도.
      // 실패하면 catch 에서 안내.
      const provider = getProviderForModel(prefs.model);
      const providerName = provider === 'openai' ? 'OpenAI' : provider === 'google' ? 'Google'
        : provider === 'moonshot' ? 'Moonshot' : provider === 'local' ? '로컬(Ollama)' : 'Anthropic';
      const providerKey = provider === 'anthropic' ? byok : getApiKey(provider);
      const baseUrls = getBaseUrls();
      // 로컬(Ollama)은 키 불필요. 그 외 프로바이더는 키 필수.
      if (provider !== 'local' && !providerKey) {
        throw new Error(`${providerName} API 키가 설정되지 않았습니다. 우상단 ⚙️ 설정에서 입력해주세요.`);
      }
      const { text: out, usage, stop_reason } = await sendMessagesUnified({
        apiKey: providerKey,
        model: prefs.model,
        system,
        messages: apiMessages,
        maxTokens: effectiveMax,
        baseUrl: baseUrls[provider],
        reasoningEffort: prefs.reasoning_effort,
        verbosity: prefs.verbosity,
        signal: ac.signal,
        onDelta: useStream ? ((_chunk, agg) => setDraft(agg)) : undefined,
      });
      if (ac.signal.aborted) return; // 단원 전환 등으로 취소됐으면 저장 안 함
      const aMsg = { role: 'assistant', content: out };
      appendRoomMessage(sendLeafId, aMsg);
      // ✂️ 출력 한도 잘림 감지 (Gemini MAX_TOKENS / OpenAI length / Claude max_tokens)
      const wasTruncated = /max_?tokens|length/i.test(String(stop_reason || ''));
      setLastTruncated(wasTruncated);
      if (wasTruncated) {
        try { toast.show('✂️ 답변이 출력 한도에 걸려 잘렸어요 — 아래 [이어쓰기]를 누르면 계속 작성합니다', 'info', 3000); } catch { /* noop */ }
      }
      // 🃏 이번 문답에서 암기 포인트를 백그라운드 추출 → 퀴즈 탭 자동 출제 (실패 무해)
      // 재생성은 같은 문답 반복이므로 중복 출제 방지 차원에서 생략
      // 로컬은 CARDGEN_FAST 매핑이 없어 클라우드로 새는 걸 방지 — 카드 자동생성은 4.5-b(역할 라우팅)에서 로컬 지원.
      if (!isRegen && provider !== 'local' && provider !== 'moonshot') generateChatCards({
        provider, apiKey: providerKey, baseUrl: baseUrls[provider],
        leafId: sendLeafId, leafPath: curLeaf ? curLeaf.path.join(' / ') : '',
        userText: text, assistantText: out,
        onSaved: (added, totalCards) => {
          try { toast.show(`🃏 퀴즈 탭에 암기카드 ${added}장 자동 출제 (이 단원 ${totalCards}장)`, 'success', 2500); } catch { /* noop */ }
        },
      });
      // 전송 시점과 현재 단원이 같을 때만 화면 갱신 (다른 방으로 옮겼으면 무시)
      if (current?.leaf_id === sendLeafId) {
        setMessages((arr) => [...arr, { ...aMsg, ts: new Date().toISOString() }]);
      }
      bumpUsage({
        messages: 1,
        input_tokens: usage.input_tokens || 0,
        cache_read: usage.cache_read_input_tokens || 0,
        cache_write: usage.cache_creation_input_tokens || 0,
        output_tokens: usage.output_tokens || 0,
      });
      try { markActiveToday(); } catch { /* noop */ }
      const blocks = extractJsonBlocks(out);
      let coverageBumped = false;
      blocks.forEach((b) => {
        if (b && typeof b.correct === 'boolean' && current) {
          recordGrade(current.leaf_id, b.correct, curPhase);
        }
        // ✍️ 분개 채점 결과 → 문항 단위 SRS 기록. 유형(topic)으로 키를 잡아
        // 같은 유형을 또 맞히면 졸업, 계속 틀리면 오늘의 인출에 재출제된다.
        if (b && b.journal === true && typeof b.correct === 'boolean') {
          const slug = (b.topic || '분개').replace(/\s+/g, '').slice(0, 40);
          try { recordItem({ kind: 'journal', idx: slug, q: (b.topic || '분개 연습').slice(0, 200), isCorrect: b.correct }); } catch { /* noop */ }
        }
        // 🔙 선행 결손 역추적 → 원클릭으로 그 단원 이동(pendingNext 재사용)
        if (b && b.prereq === true && b.unit) {
          const cand = leaves.find((l) => (l.title || '').includes(b.unit))
            || leaves.find((l) => (l.path || []).join('/').includes(b.unit));
          if (cand) setPendingNext({ leaf: cand, reason: b.reason || `선행 개념 복습: ${b.unit}` });
        }
        // 2차 답안 채점 결과
        if (b && b.graded === true && b.stage === 2 && typeof b.score === 'number' && current) {
          recordAnswerScore(current.leaf_id, {
            score: b.score,
            max: b.max || 30,
            time_used_min: b.time_used_min || 0,
            time_target_min: b.time_target_min || (b.max || 30),
          });
          // Phase α — 답안 히스토리 누적 (시간순 추이 + 인사이트)
          appendAnswer(current.leaf_id, {
            score: b.score,
            max: b.max || 30,
            structure_score: b.structure_score,
            content_score: b.content_score,
            completeness_score: b.completeness_score,
            completion_pct: b.completion_pct,
            scored_points: b.scored_points || [],
            lost_points: b.lost_points || [],
            strengths: b.strengths || [],
            missed: b.missed || [],
            rewrite_hint: b.rewrite_hint || '',
            time_used_min: b.time_used_min || 0,
            time_target_min: b.time_target_min || (b.max || 30),
            answer_text: (history[history.length - 1]?.content || '').slice(0, 5000),
          });
          coverageBumped = true;
          setMasteryState(getMastery());
          // 모의 세션 중이면 점수 누적
          if (mockSession && !mockSession.complete) {
            setMockSession((s) => ({
              ...s,
              scores: [...s.scores, {
                q: s.curQ,
                score: b.score,
                max: b.max || s.scoreDist[s.curQ - 1],
                time_used_min: b.time_used_min || 0,
              }],
            }));
          }
        }
        if (b && b.session_summary && current) {
          const delta = Number(b.coverage_delta) || 0.05;
          const prev = getChapterMastery(current.leaf_id, curPhase);
          updateChapterMastery(current.leaf_id, {
            coverage: Math.min(1, (prev.coverage || 0) + Math.max(0, Math.min(0.3, delta))),
        }, curPhase);
          coverageBumped = true;
          if (sessionId) updateSession(sessionId, { summary: b.session_summary, ended_at: new Date().toISOString() });
          addAssessment({
            session_id: sessionId,
            code: current.leaf_id,
            score: null,
            comments: b.session_summary,
            next_topic: b.next_topic || null,
          });
          if (b.next_topic) {
            // next_topic.code가 leaf_id면 사용, 아니면 path 매칭
            const candidate = leaves.find((l) => l.id === b.next_topic.code)
              || leaves.find((l) => l.path.join('/').includes(b.next_topic.code || ''));
            if (candidate) setPendingNext({ leaf: candidate, reason: b.next_topic.reason });
          }
        }
      });
      if (!coverageBumped && current) {
        const m = getChapterMastery(current.leaf_id, curPhase);
        updateChapterMastery(current.leaf_id, {
          coverage: Math.min(1, (m.coverage || 0) + 0.01),
        }, curPhase);
      }
      setMasteryState(getMastery());
      setDue(getDueChapters());
      if (sessionId) {
        updateSession(sessionId, { msg_count: history.length + 1 });
      }
    } catch (e) {
      if (e.name !== 'AbortError') {
        // 낙관적으로 추가한 user 메시지 롤백 + 입력 복원 (짝 없는 메시지 영구 누적·내용 소실 방지)
        popRoomMessage(sendLeafId);
        if (current?.leaf_id === sendLeafId) {
          setMessages((arr) => (arr.length && arr[arr.length - 1].role === 'user' ? arr.slice(0, -1) : arr));
        }
        setLastFailedText(text);
        if (typeof overrideText !== 'string') setInput(text);
        // 🔄 재생성 실패 — 지웠던 기존 답변을 원위치 (재생성이 실패해도 손해 없음)
        if (isRegen && regenPopped) {
          appendRoomMessage(sendLeafId, regenPopped);
          if (current?.leaf_id === sendLeafId) {
            setMessages((arr) => [...arr, { ...regenPopped, ts: new Date().toISOString() }]);
          }
        }
        const isNet = e.message && /fetch|network|cors|failed to fetch/i.test(e.message);
        const provName = getProviderForModel(prefs.model);
        const provLabel = provName === 'openai' ? 'GPT' : provName === 'google' ? 'Gemini' : 'Claude';
        const corsHint = isNet && provName !== 'anthropic'
          ? ` (브라우저 CORS 차단 가능성 — 설정에서 프록시 baseUrl 입력 또는 Anthropic 모델로 전환)`
          : '';
        setError(`${provLabel} 호출 실패: ${e.message}${corsHint}`);
      }
    } finally {
      setStreaming(false);
      setDraft('');
      abortRef.current = null;
      armIdleTimer();
      // 전송 완료 후 입력창 포커스 복원 (전송 중 disabled로 blur됐던 것 회복)
      if (typeof window !== 'undefined') {
        requestAnimationFrame(() => { try { inputRef.current?.focus(); } catch { /* noop */ } });
      }
    }
  }, [input, pendingImage, streaming, byok, prefs.model, prefs.daily_cap, prefs.max_tokens, current, leaves, handoverMd, unitMd, sectionMd, problemsMd, mode, sessionId, clearIdleTimer, armIdleTimer]);

  const stop = () => { if (abortRef.current) abortRef.current.abort(); };

  // 빠른 액션: input을 거치지 않고 즉시 send (overrideText 사용)
  const quickSend = (text) => { if (!streaming) send(text); };

  // 🔄 답변 다시 생성 — 마지막 assistant 응답을 버리고 직전 질문으로 재요청
  const regenerate = () => {
    if (streaming) return;
    const last = messages[messages.length - 1];
    if (!last || last.role !== 'assistant') return;
    const lastUser = [...messages].reverse().find((m) => m.role === 'user');
    if (!lastUser) return;
    const text = (lastUser.content || '').replace(/^\[📷 문제 사진 첨부\]\n/, '');
    send(text, { regenerate: true });
  };

  // mockSession.complete가 true로 바뀌면 자동 저장 (멱등성 — saved 플래그)
  useEffect(() => {
    if (mockSession?.complete && !mockSession.saved && mockSession.scores.length > 0) {
      const total = mockSession.scores.reduce((a, x) => a + x.score, 0);
      const max = mockSession.scoreDist.reduce((a, x) => a + x, 0);
      const elapsed_min = Math.floor((Date.now() - mockSession.startedAt) / 60000);
      addMock({
        subject_id: subjectId,
        leaf_id: current?.leaf_id,
        scores: mockSession.scores,
        total,
        max,
        pct: max > 0 ? Math.round((total / max) * 100) : 0,
        target_min: mockSession.totalMin,
        elapsed_min,
      });
      setMockSession((s) => s ? { ...s, saved: true } : s);
    }
  }, [mockSession?.complete, mockSession?.saved]); // eslint-disable-line

  // 2차 실전 모의 — 시작/종료 헬퍼
  const startMock = () => {
    const totalMin = subjectId === 'appraisal_law' ? 120 : 100;
    const scoreDist = [40, 30, 20, 10];
    setMockSession({
      startedAt: Date.now(),
      totalMin,
      curQ: 1,
      totalQ: 4,
      scoreDist,
      scores: [],
      complete: false,
    });
    quickSend(`실전 모의 시작 — 4문제 세트 (${scoreDist.join('·')}점). 첫 번째 40점 문제부터 출제. 사례·자료 포함.`);
  };
  const endMock = () => setMockSession(null);
  const nextMockQuestion = () => {
    if (!mockSession) return;
    if (mockSession.curQ >= mockSession.totalQ) {
      // 종합 단계
      setMockSession((s) => ({ ...s, complete: true }));
      const total = mockSession.scores.reduce((a, x) => a + x.score, 0);
      const max = mockSession.scoreDist.reduce((a, x) => a + x, 0);
      quickSend(`모의 4문제 종료. 누적 ${total}/${max}점. 종합 분석·시간 사용·약점 단원 추천 표로 정리해줘.`);
      return;
    }
    const nextQ = mockSession.curQ + 1;
    const nextScore = mockSession.scoreDist[nextQ - 1];
    setMockSession((s) => ({ ...s, curQ: nextQ }));
    quickSend(`다음 ${nextQ}번 문제 (${nextScore}점) 출제해줘.`);
  };

  // 인라인 confirm — 브라우저 confirm() 대체. 채팅 영역 하단에 카드로 표시.
  const askConfirm = (label, danger, onYes) => {
    setConfirmAction({ label, danger: !!danger, onYes });
  };

  // ── 세이브파일: 현재 단원 채팅 내보내기 / 불러오기 ──────────
  const exportRoom = () => {
    if (!curLeaf) return;
    if (messages.length === 0) {
      if (typeof window !== 'undefined') window.alert('이 단원엔 아직 대화가 없습니다.');
      return;
    }
    const data = buildRoomExport(curLeaf.id, { path: curLeaf.path, subject: subjectId });
    const safe = (curLeaf.path?.slice(-1)[0] || curLeaf.id).replace(/[\\/:*?"<>|\s]+/g, '_').slice(0, 40);
    const stamp = new Date().toISOString().slice(0, 10);
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AI학습_${safe}_${stamp}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };
  const onImportFile = (e) => {
    const file = e.target.files && e.target.files[0];
    e.target.value = ''; // 같은 파일 재선택 허용
    if (!file || !curLeaf) return;
    const reader = new FileReader();
    reader.onload = () => {
      const parsed = parseRoomImport(reader.result);
      if (!parsed) {
        if (typeof window !== 'undefined') window.alert('저장 파일 형식이 올바르지 않습니다.');
        return;
      }
      const incoming = parsed.messages;
      if (incoming.length === 0) {
        if (typeof window !== 'undefined') window.alert('저장 파일에 대화가 없습니다.');
        return;
      }
      const fromPath = Array.isArray(parsed.meta.leafPath) ? parsed.meta.leafPath.slice(-1)[0] : null;
      const note = fromPath && fromPath !== curLeaf.path.slice(-1)[0] ? `\n(저장 출처: "${fromPath}")` : '';
      askConfirm(
        `"${curLeaf.path.slice(-1)[0]}"에 저장 파일 불러오기 — 현재 ${messages.length}개를 ${incoming.length}개로 교체${note}`,
        true,
        () => {
          if (abortRef.current) abortRef.current.abort();
          importRoomMessages(curLeaf.id, incoming, 'replace');
          setMessages(getRoomMessages(curLeaf.id));
          setPendingNext(null);
          setIdlePromptShown(false);
          setRecentRooms(getAllRooms());
        }
      );
    };
    reader.onerror = () => { if (typeof window !== 'undefined') window.alert('파일을 읽지 못했습니다.'); };
    reader.readAsText(file);
  };

  // 학습 진척 즉시 초기화 — native confirm 사용해 항상 보이도록
  const doResetProgress = useCallback(() => {
    if (typeof window !== 'undefined' && !window.confirm(
      '대화·세션·진척도를 모두 초기화하시겠습니까?\nAPI 키와 설정은 유지됩니다.'
    )) return;
    if (abortRef.current) abortRef.current.abort();
    resetLearningProgress();
    setMessages([]);
    setMasteryState({});
    setDue([]);
    setSessionId(null);
    setPendingNext(null);
    setRecentRooms([]);
    setConfirmAction(null);
    // current 초기화 후 default leaf로 재설정
    setCurrentState(null);
    setCurrent(null);
    if (indexMeta?.default_leaf) {
      const def = (indexMeta.leaves || []).find((l) => l.id === indexMeta.default_leaf) || (indexMeta.leaves || [])[0];
      if (def) {
        const next = { subject: subjectId, leaf_id: def.id };
        setCurrentState(next);
        setCurrent(next);
      }
    }
    setShowHistory(false);
    setShowAnalytics(false);
    if (typeof window !== 'undefined' && window.alert) {
      window.alert('✅ 학습 진척이 초기화되었습니다.');
    }
  }, [indexMeta, subjectId]);

  const curLeaf = leaves.find((l) => l.id === current?.leaf_id);
  const cap = canSendMessage();

  // 회독 진척 — 지금 탭(=회독)에서 이 과목의 관을 몇 개 끝냈는지, 다음에 뭘 볼지.
  // 2차는 회독 축을 쓰지 않으므로 표시하지 않는다.
  const PHASE_DONE = 0.95;
  const phaseProgress = useMemo(() => {
    if (getSubjectMeta(subjectId)?.stage === 2 || !leaves.length) return null;
    const phase = modeToPhase(mode);
    let done = 0;
    let next = null;
    leaves.forEach((l) => {
      if ((mastery[l.id]?.phases?.[phase]?.coverage || 0) >= PHASE_DONE) done += 1;
      else if (!next) next = l;
    });
    // 게이팅은 막지 않고 안내만 — 앞 회독이 덜 된 관을 다음 회독으로 보고 있으면 한 줄 띄운다.
    let gateHint = null;
    const idx = MASTERY_PHASES.indexOf(phase);
    if (idx > 0 && curLeaf) {
      const prevPhase = MASTERY_PHASES[idx - 1];
      if ((mastery[curLeaf.id]?.phases?.[prevPhase]?.coverage || 0) < PHASE_DONE) {
        gateHint = `이 관은 ${PHASE_LABEL[prevPhase]}이 아직입니다`;
      }
    }
    return { phase, total: leaves.length, done, next, gateHint };
  }, [leaves, mastery, mode, subjectId, curLeaf]);

  // 🧭 실시간 학습 추천 — 현재 단원 실력을 진단해 다음 모드를 자동 제안(모드 버튼에 내제화)
  const rec = (() => {
    if (!current?.leaf_id) return null;
    const m = mastery[current.leaf_id] || {};
    const qs = quizStatsByLeaf?.[current.leaf_id];
    const isDue = Array.isArray(due) ? due.some((d) => (d.code || d) === current.leaf_id) : false;
    const stage = getSubjectMeta(subjectId)?.stage || 1;
    return recommendMode({ m, qs, isDue, stage, subjectId });
  })();

  // 게이트: Claude 키가 없어도 로컬(Ollama)이나 다른 프로바이더 키가 있으면 통과.
  // 데스크톱(Tauri)에선 로컬 감지 타이밍/네이티브 fetch 여부와 무관하게 항상 UI 진입 허용
  // (모델 드롭다운·send 에러가 안내). 웹에서만 키 게이트 유지.
  const hasUsableModel = byok || localModels.length > 0
    || getApiKey('openai') || getApiKey('google') || getApiKey('moonshot');
  if (!hasUsableModel && !isTauri()) {
    return (
      <div style={{ padding: 16 }}>
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', padding: '8px 0', marginBottom: 16 }}>
          <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: 8, color: '#111827' }}>
            <Sparkles size={20} color="#4f46e5" /> AI 학습
          </h2>
        </header>
        {/* 키가 없어도 무엇을 할 수 있는지 먼저 보여줌 */}
        <div style={{ maxWidth: 520, margin: '0 auto 4px', padding: 16, background: '#f5f3ff',
          border: '1px solid #ddd6fe', borderRadius: 12 }}>
          <div style={{ fontWeight: 800, fontSize: '0.95rem', color: '#4f46e5', marginBottom: 8 }}>
            AI 튜터와 단원별 1:1 학습
          </div>
          <ul style={{ margin: 0, paddingLeft: 18, fontSize: '0.82rem', color: '#4b5563', lineHeight: 1.8 }}>
            <li>교재 전 단원을 대화하며 개념 학습 → 이해 확인 퀴즈</li>
            <li>문제풀이 중 막히면 「AI 튜터로 이 단원 배우기」로 바로 연결</li>
            <li>학습 기록 기반 약점 분석·복습 추천</li>
          </ul>
          <div style={{ marginTop: 10, fontSize: '0.75rem', color: '#7c3aed' }}>
            사용하려면 아래에 본인 Claude API 키를 한 번만 등록하세요. (기기에만 저장)
          </div>
        </div>
        <ApiKeyForm initial="" onSave={(k) => { setByok(k); setByokState(k); }} />
      </div>
    );
  }

  return (
    aiView === 'home' ? (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: 0, height: 'calc(100dvh - 64px - env(safe-area-inset-bottom, 0px))', maxWidth: 960, margin: '0 auto', width: '100%', background: TOSS.bg }}>
      <header className="top-nav" style={{ background: TOSS.bg, padding: '14px 18px 8px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'static', minHeight: 0, flex: '0 0 auto' }}>
        <h2 style={{ margin: 0, fontSize: '1.35rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: 7, color: TOSS.ink, letterSpacing: '-0.02em' }}>
          <Sparkles size={22} color={TOSS.blue} /> AI 학습
        </h2>
        <div style={{ display: 'flex', gap: 2 }}>
          <button className="icon-btn" onClick={() => setShowAnalytics((v) => !v)} title="분석" style={{ background: showAnalytics ? TOSS.blueWeak : 'none', border: 'none', cursor: 'pointer', padding: 8, borderRadius: 10 }}>
            <BarChart3 size={20} color={showAnalytics ? TOSS.blue : TOSS.sub} />
          </button>
          <button className="icon-btn" onClick={() => setShowHistory((v) => !v)} title="단원별 채팅방" style={{ background: showHistory ? TOSS.blueWeak : 'none', border: 'none', cursor: 'pointer', padding: 8, borderRadius: 10 }}>
            <Calendar size={20} color={showHistory ? TOSS.blue : TOSS.sub} />
          </button>
          <button className="icon-btn" onClick={() => setShowSettings((v) => !v)} title="설정 (API 키·프록시·cap)" style={{ background: showSettings ? TOSS.blueWeak : 'none', border: 'none', cursor: 'pointer', padding: 8, borderRadius: 10 }}>
            <Settings size={20} color={showSettings ? TOSS.blue : TOSS.sub} />
          </button>
        </div>
      </header>
      {showSettings && (
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <SettingsPanel
            byok={byok}
            prefs={prefs}
            onClose={() => setShowSettings(false)}
            onSave={(k) => { setByokState(k); setPrefsState(getPrefs()); setShowSettings(false); }}
          />
        </div>
      )}
      {showHistory && (
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <HistoryPanel
            leaves={Object.values(leavesBySubject).flat()}
            onClose={() => setShowHistory(false)}
            onJump={(leaf) => {
              const sid = (leaf.id || '').split('__')[0];
              if (sid !== subjectId) switchSubject(sid, true); else setAiView('study');
              setTimeout(() => pickLeaf(leaf, null), 50); // 다른 분류일 수 있어 스코프 해제
              setShowHistory(false);
            }}
            onClearRoom={(leafId) => {
              clearRoom(leafId);
              if (leafId === current?.leaf_id) setMessages([]);
            }}
          />
        </div>
      )}
      {showAnalytics && (
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <AnalyticsPanel
            mastery={mastery}
            leavesBySubject={leavesBySubject}
            onClose={() => setShowAnalytics(false)}
            onJump={(leaf, sid) => {
              if (sid !== subjectId) switchSubject(sid, true); else setAiView('study');
              setTimeout(() => pickLeaf(leaf, null), 50); // 다른 분류일 수 있어 스코프 해제
              setShowAnalytics(false);
            }}
          />
        </div>
      )}
      {confirmAction && (
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <div style={{
            background: confirmAction.danger ? '#fef2f2' : '#eef2ff',
            border: `1px solid ${confirmAction.danger ? '#fecaca' : '#c7d2fe'}`,
            color: confirmAction.danger ? '#991b1b' : '#1e40af',
            padding: 12, borderRadius: 10, display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap',
          }}>
            <div style={{ flex: 1, fontSize: '0.88rem', fontWeight: 600 }}>{confirmAction.label}?</div>
            <button onClick={() => { const a = confirmAction; setConfirmAction(null); a.onYes && a.onYes(); }}
              style={{ padding: '6px 14px', fontSize: '0.85rem', fontWeight: 700, background: confirmAction.danger ? '#dc2626' : TOSS.blue, color: '#fff', border: 'none', borderRadius: 8, cursor: 'pointer' }}>
              네
            </button>
            <button onClick={() => setConfirmAction(null)}
              style={{ padding: '6px 14px', fontSize: '0.85rem', background: '#fff', color: '#374151', border: '1px solid #d1d5db', borderRadius: 6, cursor: 'pointer' }}>
              취소
            </button>
          </div>
        </div>
      )}
      <div style={{ flex: 1, minHeight: 0, overflowY: 'auto', padding: '8px 18px 32px' }}>
        {/* 이어서 학습 카드 */}
        {curLeaf && messages.length > 0 && (() => {
          const m = mastery[curLeaf.id] || {};
          const sMeta = getSubjectMeta(subjectId);
          return (
            <button
              onClick={() => setAiView('study')}
              style={{
                width: '100%', textAlign: 'left', padding: 18,
                background: TOSS.blue,
                border: 'none',
                borderRadius: TOSS.radius, cursor: 'pointer', marginBottom: 18,
                boxShadow: '0 6px 16px rgba(49, 130, 246, 0.28)',
              }}
            >
              <div style={{ fontSize: '0.78rem', color: 'rgba(255,255,255,0.85)', fontWeight: 700, marginBottom: 6, display: 'flex', alignItems: 'center', gap: 4 }}>
                <Play size={13} fill="#fff" color="#fff" /> 이어서 학습 · {sMeta.short}
              </div>
              <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#fff', letterSpacing: '-0.01em' }}>
                {curLeaf.path.slice(-1)[0]}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'rgba(255,255,255,0.8)', marginTop: 4 }}>
                {curLeaf.path.slice(0, -1).join(' › ')}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'rgba(255,255,255,0.92)', marginTop: 10, fontWeight: 600 }}>
                대화 {messages.length}건 · 진척 {Math.round((m.coverage || 0) * 100)}%
              </div>
            </button>
          );
        })()}

        {/* 1차 / 2차 — 문제풀이 탭과 동일한 평면 섹션 + 흰 카드 그리드 */}
        <div>
          {[
            {
              stage: 1, label: '1차 시험 — 객관식 5지선다',
              // 표시 순서: 회계학·경제학·민법 (위) / 부동산학·관계법규 (아래) — 3+2
              subjects: ['accounting', 'economics', 'civil', 'realestate', 'law'].map((id) => SUBJECTS.find((s) => s.id === id)).filter(Boolean),
              chipBg: TOSS.blueWeak, chipFg: TOSS.blue,
              barColor: TOSS.blue,
            },
            {
              stage: 2, label: '2차 시험 — 서술형·답안 작성',
              subjects: SUBJECTS_BY_STAGE[2],
              chipBg: '#F0EBFF', chipFg: '#7C3AED',
              barColor: '#7C3AED',
            },
          ].map(({ stage, label, subjects, chipBg, chipFg, barColor }) => (
            <div key={stage} style={{ marginBottom: 18 }}>
              {/* 섹션 라벨 — 문제풀이와 동일 패턴 */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
                <div style={{ fontSize: '1rem', color: TOSS.ink, fontWeight: 800 }}>
                  {stage === 1 ? <BookOpen size={16} color="#8B95A1" strokeWidth={2} style={{ verticalAlign: '-3px' }} /> : <PenLine size={16} color="#8B95A1" strokeWidth={2} style={{ verticalAlign: '-3px' }} />} {label}
                </div>
                <span style={{ fontSize: '0.82rem', color: TOSS.sub, fontWeight: 600 }}>{subjects.length}과목</span>
              </div>
              {/* 과목 카드 그리드 — 문제풀이와 동일 스펙 */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', rowGap: 14, columnGap: 12, alignItems: 'stretch' }}>
                {subjects.map((s) => {
                  const ks = Object.keys(mastery).filter((k) => k.startsWith(s.id + '__') || k.startsWith(s.id + '_'));
                  const covAvg = ks.length ? ks.reduce((a, k) => a + (mastery[k]?.coverage || 0), 0) / ks.length : 0;
                  const masterN = ks.filter((k) => mastery[k]?.status === 'mastered').length;
                  const dueN = (due || []).filter((d) => (d.code || '').startsWith(s.id + '__') || (d.code || '').startsWith(s.id + '_')).length;
                  const weakN = ((weakPathsBySubject || {})[s.id] || []).length;
                  const pct = Math.round(covAvg * 100);
                  const isStage2 = s.stage === 2;
                  const divisions = isStage2 ? [] : divisionsFor(s.id);
                  const showDivs = !isStage2 && divisions.length >= 2 && divisions.length <= 4;
                  const showSingle = isStage2 || (!isStage2 && divisions.length >= 5);
                  const chipStyle = {
                    padding: '11px 6px', fontSize: '0.84rem', fontWeight: 700,
                    background: chipBg, color: chipFg, border: 'none',
                    borderRadius: 10, cursor: 'pointer', whiteSpace: 'nowrap',
                    overflow: 'hidden', textOverflow: 'ellipsis', textAlign: 'center',
                  };
                  return (
                    <div
                      key={s.id}
                      style={{
                        background: TOSS.card, border: 'none', borderRadius: 20, position: 'relative',
                        display: 'flex', flexDirection: 'column',
                        boxShadow: '0 2px 8px rgba(0, 23, 51, 0.06)',
                      }}
                    >
                      <button
                        onClick={() => enterSubjectWhole(s.id)}
                        style={{
                          padding: '20px 18px 16px', textAlign: 'left', background: 'none', border: 'none',
                          cursor: 'pointer', width: '100%', display: 'flex', flexDirection: 'column', gap: 12,
                        }}
                      >
                        <div style={{ display: 'flex' }}>
                          <span style={{ fontSize: '0.7rem', fontWeight: 800, background: chipBg, color: chipFg, padding: '3px 9px', borderRadius: 999 }}>{isStage2 ? '2차' : '1차'}</span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                          <div style={{ minWidth: 0, flex: 1 }}>
                            <div style={{ fontWeight: 800, color: TOSS.ink, fontSize: '1.2rem', letterSpacing: '-0.01em', lineHeight: 1.3 }}>{s.short}</div>
                            <div style={{ fontSize: '0.82rem', color: TOSS.sub, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', marginTop: 4 }}>{s.title}</div>
                          </div>
                          <div style={{ flex: '0 0 auto', display: 'flex', alignItems: 'center' }}><SubjectIcon id={s.id} size={30} color="#8B95A1" /></div>
                        </div>
                        <div>
                          <div style={{ height: 6, background: TOSS.track, borderRadius: 999, overflow: 'hidden' }}>
                            <div style={{ width: `${Math.max(2, pct)}%`, height: '100%', background: barColor, borderRadius: 999 }} />
                          </div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginTop: 5 }}>
                            <span style={{ fontWeight: 800, color: TOSS.ink }}>{pct}%</span>
                            <span style={{ color: TOSS.sub, fontWeight: 600 }}>{isStage2 ? `답안 ${masterN}` : `마스터 ${masterN}`}</span>
                          </div>
                        </div>
                        {(dueN > 0 || weakN > 0) && (
                          <div style={{ fontSize: '0.74rem', color: '#FF8A00', display: 'flex', gap: 6, fontWeight: 700 }}>
                            {dueN > 0 && <span>🔁 복습 {dueN}</span>}
                            {weakN > 0 && <span>⚠️ 약점 {weakN}</span>}
                          </div>
                        )}
                      </button>
                      {showDivs && (
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6, padding: '0 18px 14px', marginTop: 'auto' }}>
                          {divisions.map((d) => (
                            <button key={d.label} onClick={() => jumpToLeaf(s.id, d.leaf, { label: d.label, tops: d.tops })} title={d.label} style={chipStyle}>
                              {cleanDivLabel(d.label)}
                            </button>
                          ))}
                        </div>
                      )}
                      {showSingle && (
                        <div style={{ padding: '0 18px 14px', marginTop: 'auto' }}>
                          <button onClick={() => enterSubjectWhole(s.id)} style={{ ...chipStyle, width: '100%' }}>
                            {s.title}
                          </button>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* 비어있는 첫 사용자 가이드 */}
        {!curLeaf && Object.keys(mastery).length === 0 && (
          <div style={{ marginTop: 20, padding: 18, background: TOSS.card, border: 'none', borderRadius: TOSS.radius, boxShadow: TOSS.shadow, fontSize: '0.88rem', color: TOSS.sub, textAlign: 'center', lineHeight: 1.5 }}>
            과목을 선택하면 단원 트리에서 학습할 곳을 고르고 대화를 시작할 수 있어요
          </div>
        )}
      </div>
    </div>
    ) : (
    <div style={isDesktop ? {
      display: 'grid',
      // 교재 패널은 기본서 상세(표·수식·그래프)를 담아 더 넓게 — 화면이 넓을수록 여유 있게
      gridTemplateColumns: showDoc ? '340px minmax(0, 1fr) clamp(360px, 30vw, 520px)' : '340px minmax(0, 1fr)',
      // 단일 행을 뷰포트 높이로 고정. 미지정 시 행이 콘텐츠(implicit auto)로 잡혀
      // 좌측 단원 트리가 길면 그리드가 뷰포트보다 커지고 채팅 컬럼 스크롤이 깨짐.
      gridTemplateRows: 'minmax(0, 1fr)',
      gap: 0,
      height: isTauri() ? '100dvh' : 'calc(100dvh - 64px - env(safe-area-inset-bottom, 0px))',
      // 데스크톱 셸이 좌측 rail 만큼 padding-left 를 주므로 100% 로 그 영역을 채운다(구 100vw 트릭 제거)
      width: '100%',
      position: 'relative',
      background: '#fff',
    } : { display: 'flex', flexDirection: 'column', minHeight: 0, height: 'calc(100dvh - 64px - env(safe-area-inset-bottom, 0px))', maxWidth: 1100, margin: '0 auto', width: '100%' }}>
      {/* PC 전용 좌측 단원 사이드바 — LeafPicker inline */}
      {isDesktop && (
        <aside style={{
          borderRight: '1px solid #e5e7eb', background: '#fafafa',
          display: 'flex', flexDirection: 'column', overflow: 'hidden', minHeight: 0,
        }}>
          <div style={{ padding: '10px 12px', borderBottom: '1px solid #e5e7eb', background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontWeight: 800, fontSize: '0.88rem', color: '#111827', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                📂 {getSubjectMeta(subjectId)?.title || '과목'}
              </div>
              {activeDivision && (
                <div style={{ fontSize: '0.72rem', color: TOSS.blue, fontWeight: 700, marginTop: 2 }}>
                  {cleanDivLabel(activeDivision)} 범위
                </div>
              )}
            </div>
            {activeDivision ? (
              <button onClick={clearDivision} title="이 과목 전체 단원 보기" style={{ background: TOSS.blueWeak, border: 'none', cursor: 'pointer', color: TOSS.blue, fontSize: '0.72rem', fontWeight: 800, padding: '4px 9px', borderRadius: 999, flex: '0 0 auto' }}>
                전체 보기
              </button>
            ) : (
              <button onClick={() => setAiView('home')} title="과목 변경" style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6b7280', fontSize: '0.75rem', fontWeight: 700, flex: '0 0 auto' }}>
                과목 ▾
              </button>
            )}
          </div>
          <div style={{ flex: 1, overflowY: 'auto', padding: 8 }}>
            <LeafPicker
              inline
              leaves={scopedLeaves}
              current={current}
              onPick={(leaf) => pickLeaf(leaf)}
              mastery={mastery}
              due={due}
              quizStatsByLeaf={quizStatsByLeaf}
            />
          </div>
        </aside>
      )}
      <div style={{ display: 'flex', flexDirection: 'column', minWidth: 0, minHeight: 0, height: '100%' }}>
      <header ref={headerRef} className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', gap: 6, padding: '6px 8px', position: 'static', minHeight: 0, flex: '0 0 auto', overflow: 'hidden' }}>
        <button
          onClick={() => setAiView('home')}
          title="과목 홈"
          style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 4, color: '#4f46e5', fontSize: '0.85rem', fontWeight: 700, whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: 2 }}
        >
          <ChevronLeft size={18} />홈
        </button>
        <button
          onClick={() => prevLeaf && pickLeaf(prevLeaf)}
          disabled={!prevLeaf}
          title={prevLeaf ? `← ${prevLeaf.path.slice(-1)[0]}` : ''}
          style={{ ...ICON_BTN, cursor: prevLeaf ? 'pointer' : 'not-allowed', opacity: prevLeaf ? 1 : 0.55 }}
        >
          <ChevronLeft size={20} color="#374151" />
        </button>
        {isDesktop && (
          <button onClick={() => setShowDoc((v) => !v)} title={showDoc ? '교재 원문 패널 숨기기' : '교재 원문 보기'}
            style={{ background: showDoc ? '#eef2ff' : 'none', border: 'none', cursor: 'pointer', padding: '4px 8px', borderRadius: 8, color: showDoc ? '#4f46e5' : '#9ca3af', fontSize: '0.76rem', fontWeight: 800, flex: '0 0 auto', whiteSpace: 'nowrap' }}>
            📖 교재
          </button>
        )}

        {/* 가운데: 단원 박스 — 클릭 시 LeafPicker 모달 (단원/소단원 선택 통합) */}
        <button
          onClick={() => setShowLeafPickerModal(true)}
          style={{
            flex: 1, minWidth: 0,
            display: 'flex', alignItems: 'center', gap: 8,
            padding: '5px 10px',
            background: 'linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%)',
            border: '1px solid #e0e7ff',
            borderRadius: 10, cursor: 'pointer', textAlign: 'left',
          }}
          title="단원 변경"
        >
          <Sparkles size={16} color="#4f46e5" style={{ flex: '0 0 auto' }} />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: '0.95rem', fontWeight: 800, color: '#111827', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {curLeaf ? curLeaf.path.slice(-1)[0] : 'AI 학습'}
            </div>
            <div style={{ fontSize: '0.7rem', color: '#475569', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {curLeaf ? curLeaf.path.slice(1, -1).join(' › ') : '단원 선택'}
              {curLeaf?.unit_code && (
                <span style={{ marginLeft: 6, color: '#94a3b8' }}>
                  · {curLeaf.unit_code}
                  {curLeaf.section_name && curLeaf.section_name !== '전체' && ` · ${curLeaf.section_name.slice(0, 12)}${curLeaf.section_name.length > 12 ? '…' : ''}`}
                </span>
              )}
            </div>
          </div>
          {curLeaf && (() => {
            const m = mastery[curLeaf.id] || { coverage: 0, status: 'not_started' };
            const isStage2 = getSubjectMeta(subjectId)?.stage === 2;
            const isMaster = m.status === 'mastered';
            if (isStage2) {
              const cnt = m.answer_count || 0;
              const avg = Math.round(m.avg_score_pct || 0);
              return (
                <span style={{
                  fontSize: '0.72rem', fontWeight: 800, padding: '3px 9px', borderRadius: 999,
                  background: isMaster ? '#d1fae5' : cnt > 0 ? '#ede9fe' : '#fff',
                  color: isMaster ? '#047857' : cnt > 0 ? '#5b21b6' : '#475569',
                  border: '1px solid ' + (isMaster ? '#a7f3d0' : cnt > 0 ? '#ddd6fe' : '#e2e8f0'),
                  whiteSpace: 'nowrap', flex: '0 0 auto',
                }}>
                  {isMaster ? '✓ 마스터' : cnt > 0 ? `📝${cnt} · ${avg}%` : '미시작'}
                </span>
              );
            }
            const pct = Math.round((m.coverage || 0) * 100);
            return (
              <span style={{
                fontSize: '0.72rem', fontWeight: 800, padding: '3px 9px', borderRadius: 999,
                background: isMaster ? '#d1fae5' : pct > 0 ? '#fff' : '#fff',
                color: isMaster ? '#047857' : pct > 0 ? '#4338ca' : '#475569',
                border: '1px solid ' + (isMaster ? '#a7f3d0' : pct > 0 ? '#c7d2fe' : '#e2e8f0'),
                whiteSpace: 'nowrap', flex: '0 0 auto',
              }}>
                {isMaster ? '✓ 마스터' : `${pct}%`}
              </span>
            );
          })()}
          <ChevronDown size={14} color="#94a3b8" style={{ flex: '0 0 auto' }} />
        </button>

        <button
          onClick={() => nextLeaf && pickLeaf(nextLeaf)}
          disabled={!nextLeaf}
          title={nextLeaf ? `${nextLeaf.path.slice(-1)[0]} →` : ''}
          style={{ ...ICON_BTN, cursor: nextLeaf ? 'pointer' : 'not-allowed', opacity: nextLeaf ? 1 : 0.55 }}
        >
          <ChevronRight size={20} color="#374151" />
        </button>
        {curLeaf && !tight && (
          <>
            <input
              ref={importInputRef}
              type="file"
              accept="application/json,.json"
              onChange={onImportFile}
              style={{ display: 'none' }}
            />
            <button
              onClick={exportRoom}
              title={messages.length > 0 ? `이 단원 채팅 저장파일 내보내기 (${messages.length}개)` : '이 단원엔 대화 없음'}
              style={{ ...ICON_BTN, opacity: messages.length === 0 ? 0.6 : 1 }}
            >
              <Download size={16} color="#4f46e5" />
            </button>
            <button
              onClick={() => importInputRef.current && importInputRef.current.click()}
              title="저장파일 불러오기 (현재 단원 채팅 교체)"
              style={ICON_BTN}
            >
              <Upload size={16} color="#0891b2" />
            </button>
          </>
        )}
        {curLeaf && !tight && (
          <button
            onClick={() => {
              if (messages.length === 0) {
                if (typeof window !== 'undefined') window.alert('이 단원엔 아직 대화가 없습니다.');
                return;
              }
              askConfirm(`"${curLeaf.path.slice(-1)[0]}" 채팅방 초기화 (${messages.length}개 메시지 삭제, 진척도는 유지)`, true, () => {
                if (abortRef.current) abortRef.current.abort();
                clearRoom(curLeaf.id);
                setMessages([]);
                setPendingNext(null);
                setIdlePromptShown(false);
                setRecentRooms(getAllRooms());
              });
            }}
            title={messages.length > 0 ? `이 채팅방 초기화 (${messages.length}개)` : '이 단원엔 대화 없음'}
            style={{ ...ICON_BTN, opacity: messages.length === 0 ? 0.6 : 1 }}
          >
            <Trash2 size={16} color="#ef4444" />
          </button>
        )}
        <button className="icon-btn" onClick={() => setShowAnalytics((v) => !v)} title="분석" style={ICON_BTN}>
          <BarChart3 size={18} color={showAnalytics ? '#4f46e5' : '#6b7280'} />
        </button>
        {!veryTight && (
          <button className="icon-btn" onClick={() => setShowHistory((v) => !v)} title="단원별 채팅방" style={ICON_BTN}>
            <Calendar size={18} color={showHistory ? '#4f46e5' : '#6b7280'} />
          </button>
        )}
        <button className="icon-btn" onClick={() => setShowSettings((v) => !v)} title="설정 (API 키·프록시·cap)" style={ICON_BTN}>
          <Settings size={18} color={showSettings ? '#4f46e5' : '#6b7280'} />
        </button>
      </header>
      {showSettings && (
        <div style={{ padding: 10, borderBottom: '1px solid #e5e7eb' }}>
          <SettingsPanel
            byok={byok}
            prefs={prefs}
            onClose={() => setShowSettings(false)}
            onSave={(k) => { setByokState(k); setPrefsState(getPrefs()); setShowSettings(false); }}
          />
        </div>
      )}
      {due.length > 0 && (
        <div style={{
          padding: '6px 12px', background: '#fef3c7', borderBottom: '1px solid #fcd34d',
          fontSize: '0.78rem', color: '#92400e', display: 'flex', alignItems: 'center', gap: 6,
        }}>
          <RotateCcw size={14} /> 복습 만기 {due.length}개
        </div>
      )}
      {mockSession && (() => {
        const elapsed = Math.floor((Date.now() - mockSession.startedAt) / 1000);
        const totalSec = mockSession.totalMin * 60;
        const remaining = Math.max(0, totalSec - elapsed);
        const mm = Math.floor(remaining / 60);
        const ss = String(remaining % 60).padStart(2, '0');
        const overTime = elapsed > totalSec;
        const acc = mockSession.scores.reduce((a, x) => a + x.score, 0);
        const accMax = mockSession.scoreDist.slice(0, Math.max(mockSession.scores.length, mockSession.curQ - 1)).reduce((a, x) => a + x, 0);
        const totalMax = mockSession.scoreDist.reduce((a, x) => a + x, 0);
        const progress = (mockSession.scores.length / mockSession.totalQ) * 100;
        return (
          <div style={{
            padding: '8px 12px', background: 'linear-gradient(90deg, #ede9fe 0%, #ddd6fe 100%)',
            borderBottom: '1px solid #c4b5fd',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6, flexWrap: 'wrap' }}>
              <span style={{ fontWeight: 800, color: '#5b21b6', fontSize: '0.85rem' }}>
                🎬 실전 모의 {mockSession.curQ}/{mockSession.totalQ}
              </span>
              <span style={{ fontSize: '0.74rem', color: '#7c3aed', fontWeight: 700 }}>
                ⏱ {overTime ? '+' : ''}{mm}:{ss}{overTime && ' 초과'}
              </span>
              <span style={{ fontSize: '0.74rem', color: '#5b21b6' }}>
                누적 {acc}/{accMax || 0}점 (만점 {totalMax})
              </span>
              <button onClick={endMock}
                style={{ marginLeft: 'auto', padding: '3px 9px', fontSize: '0.7rem', fontWeight: 700,
                  background: '#fff', color: '#991b1b', border: '1px solid #fecaca', borderRadius: 6, cursor: 'pointer' }}>
                중단
              </button>
            </div>
            <div style={{ height: 4, background: '#fff', borderRadius: 2, overflow: 'hidden' }}>
              <div style={{ width: `${progress}%`, height: '100%', background: '#7c3aed', transition: 'width .3s' }} />
            </div>
            {mockSession.complete && (
              <div style={{ marginTop: 8, padding: 8, background: '#fff', borderRadius: 6, border: '1px solid #c4b5fd' }}>
                <div style={{ fontWeight: 800, color: '#5b21b6', marginBottom: 4 }}>
                  ✅ 모의 완료 — 총 {acc}/{totalMax}점 ({Math.round((acc / totalMax) * 100)}%)
                </div>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', fontSize: '0.72rem', color: '#374151' }}>
                  {mockSession.scores.map((sc, i) => (
                    <span key={i} style={{ background: '#f3f4f6', padding: '2px 6px', borderRadius: 4 }}>
                      Q{sc.q}: {sc.score}/{sc.max}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      })()}

      <div style={{ padding: '4px 12px', borderBottom: '1px solid #e5e7eb', background: '#f9fafb' }}>
        {/* 🧭 실시간 학습 추천 — 실력 진단 → 다음 모드 자동 제안 */}
        {rec && rec.mode !== mode && (() => {
          const RIcon = MODE_ICON[rec.mode]; const rlabel = MODE_NAME[rec.mode] || '';
          return (
            <button onClick={() => setMode(rec.mode)}
              style={{ width: '100%', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: 2, marginTop: 4, marginBottom: 6,
                background: rec.done ? '#ecfdf5' : '#eef2ff', border: `1px solid ${rec.done ? '#a7f3d0' : '#c7d2fe'}`, borderRadius: 10, padding: '7px 11px', cursor: 'pointer' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: 3, fontSize: '0.72rem', fontWeight: 800, color: rec.done ? '#047857' : '#4338ca' }}><Compass size={12} strokeWidth={2.2} /> AI 추천</span>
                {RIcon && <RIcon size={15} strokeWidth={2} color={rec.done ? '#047857' : '#4338ca'} />}
                <span style={{ fontSize: '0.82rem', fontWeight: 800, color: '#111827' }}>{rlabel}</span>
                <span style={{ marginLeft: 'auto', fontSize: '0.74rem', fontWeight: 800, color: rec.done ? '#047857' : '#4338ca' }}>▶ 시작</span>
              </div>
              <div style={{ fontSize: '0.74rem', color: '#475569', lineHeight: 1.4 }}>{rec.reason}</div>
            </button>
          );
        })()}
        <div style={{ display: 'flex', gap: 4, marginBottom: 0, overflowX: 'auto', paddingBottom: 2 }}>
          {(() => {
            const isStage2 = getSubjectMeta(subjectId)?.stage === 2;
            if (!isStage2) {
              const s1 = [
                ['study', '📖', '이론', '처음 배움'],
                ['practice', '✏️', '문제풀이', '기출 풀이'],
                ['deep', '🧠', '심화', '판례·함정'],
                ['summary', '⚡', '복습', '핵심 압축'],
                ['diagnose', '🎯', '진단', 'OX 5문제'],
              ];
              if (subjectId === 'accounting') s1.push(['journal', '✍️', '분개', '차변/대변 채점']);
              if (subjectId === 'accounting' || subjectId === 'economics') s1.push(['calc', '🧮', '계산', '한 단계씩']);
              return s1;
            }
            const list = [
              ['concept_s2', '📖', '개념', '논점 도입'],
              ['template', '📋', '양식', '답안 골격 외우기'],
              ['topic_extract', '🔍', '논점', '사례 분석'],
              ['answer_write', '📝', '답안', '작성·채점'],
              ['mock_full', '🎬', '실전', '4문제 타이머'],
            ];
            if (subjectId === 'appraisal_practice') list.push(['calc_s2', '🧮', '계산', '산식 풀이']);
            return list;
          })().map(([k, icon, label, desc]) => {
            const isRec = rec && rec.mode === k && mode !== k; // 추천이면서 현재 모드가 아님
            return (
            <button
              key={k}
              onClick={() => setMode(k)}
              title={isRec ? `🧭 추천: ${rec.reason}` : desc}
              style={{
                flex: '0 0 auto', padding: '4px 10px', borderRadius: 999,
                border: mode === k ? '1.5px solid #4f46e5' : isRec ? '1.5px solid #10b981' : '1px solid #d1d5db',
                background: mode === k ? '#eef2ff' : isRec ? '#ecfdf5' : '#fff',
                color: mode === k ? '#1d4ed8' : isRec ? '#047857' : '#374151',
                fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer',
                display: 'inline-flex', alignItems: 'center', gap: 5,
                lineHeight: 1.2, whiteSpace: 'nowrap',
                boxShadow: isRec ? '0 0 0 2px #a7f3d0' : 'none',
              }}
            >
              {isRec && <span style={{ width: 6, height: 6, borderRadius: 999, background: '#10b981', flexShrink: 0 }} />}
              {(() => { const MI = MODE_ICON[k]; return MI ? <MI size={15} strokeWidth={2} color={mode === k ? '#1d4ed8' : isRec ? '#047857' : '#6b7280'} /> : <span style={{ fontSize: '0.9rem' }}>{icon}</span>; })()}
              <span>{label}</span>
            </button>
            );
          })}
        </div>
        {/* 회독 진척 배지 — 모드 탭이 곧 회독 축이므로 지금 탭의 회독 상태를 보여준다.
            1차에서만 의미가 있다(2차는 회독 축을 쓰지 않는다). */}
        {phaseProgress && (
          <div style={{
            marginTop: 6, display: 'flex', alignItems: 'center', gap: 8,
            flexWrap: 'wrap', fontSize: '0.72rem', color: '#4b5563',
          }}>
            <span style={{ fontWeight: 800, color: '#374151' }}>
              🔁 {PHASE_LABEL[phaseProgress.phase]}
            </span>
            <span style={{
              flex: '0 0 96px', height: 5, borderRadius: 999,
              background: '#e5e7eb', overflow: 'hidden',
            }}>
              <span style={{
                display: 'block', height: '100%', borderRadius: 999, background: '#6b7280',
                width: `${phaseProgress.total ? (phaseProgress.done / phaseProgress.total) * 100 : 0}%`,
              }} />
            </span>
            <span>{phaseProgress.total}관 중 <b style={{ color: '#374151' }}>{phaseProgress.done}관</b> 완료</span>
            {phaseProgress.next && (
              <button
                onClick={() => pickLeaf(phaseProgress.next)}
                style={{
                  padding: '2px 8px', borderRadius: 999, border: '1px solid #d1d5db',
                  background: '#fff', color: '#374151', fontSize: '0.7rem',
                  fontWeight: 700, cursor: 'pointer', maxWidth: 220,
                  overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}
                title={phaseProgress.next.path.join(' › ')}
              >
                다음: {phaseProgress.next.title || phaseProgress.next.path.slice(-1)[0]}
              </button>
            )}
            {phaseProgress.gateHint && (
              <span style={{ color: '#b45309' }}>· {phaseProgress.gateHint}</span>
            )}
          </div>
        )}
        {/* 단원 자료 없음만 작게 안내 */}
        {curLeaf && !curLeaf.unit_file && (
          <div style={{ marginTop: 6, fontSize: '0.72rem', color: '#dc2626', fontWeight: 600 }}>
            ⚠️ 단원 자료 없음 — 인수인계서만으로 진행
          </div>
        )}
      </div>

      {/* 단원 picker 모달 — 헤더 박스 클릭 시 */}
      {showLeafPickerModal && (
        <>
          <div onClick={() => setShowLeafPickerModal(false)}
            style={{ position: 'fixed', inset: 0, background: 'rgba(15,23,42,0.45)', zIndex: 'var(--z-overlay)' }} />
          <div style={{
            position: 'fixed', top: '8vh', left: '50%', transform: 'translateX(-50%)',
            width: 'min(560px, 92vw)', maxHeight: '80vh', background: '#fff',
            borderRadius: 14, boxShadow: '0 20px 50px rgba(15,23,42,0.25)',
            display: 'flex', flexDirection: 'column', zIndex: 'var(--z-modal-top)',
            animation: 'cmdkIn 0.2s cubic-bezier(0.22, 0.61, 0.36, 1)',
            overflow: 'hidden',
          }}>
            <div style={{ padding: '12px 14px', borderBottom: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
              <div style={{ fontWeight: 800, color: '#111827', minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                📂 단원 선택{activeDivision && <span style={{ color: TOSS.blue, marginLeft: 6 }}>· {cleanDivLabel(activeDivision)}</span>}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, flex: '0 0 auto' }}>
                {activeDivision && (
                  <button onClick={() => { clearDivision(); }} title="이 과목 전체 단원 보기" style={{ background: TOSS.blueWeak, border: 'none', cursor: 'pointer', color: TOSS.blue, fontSize: '0.74rem', fontWeight: 800, padding: '4px 9px', borderRadius: 999 }}>
                    전체 보기
                  </button>
                )}
                <button onClick={() => setShowLeafPickerModal(false)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6b7280', fontSize: '1.1rem' }}>✕</button>
              </div>
            </div>
            <div style={{ overflowY: 'auto', flex: 1 }}>
              <LeafPicker
                inline
                leaves={scopedLeaves}
                current={current}
                onPick={(leaf) => { pickLeaf(leaf); setShowLeafPickerModal(false); }}
                mastery={mastery}
                due={due}
                quizStatsByLeaf={quizStatsByLeaf}
              />
            </div>
          </div>
        </>
      )}

      {showHistory && (
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <HistoryPanel
            leaves={leaves}
            onClose={() => setShowHistory(false)}
            onJump={(leaf) => { pickLeaf(leaf, null); setShowHistory(false); }}
            onClearRoom={(leafId) => {
              clearRoom(leafId);
              if (leafId === current?.leaf_id) setMessages([]);
            }}
          />
        </div>
      )}

      {showAnalytics && (
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <AnalyticsPanel
            mastery={mastery}
            leavesBySubject={leavesBySubject}
            onClose={() => setShowAnalytics(false)}
            onJump={(leaf, sid) => {
              if (sid !== subjectId) switchSubject(sid, true);
              else setAiView('study');
              setTimeout(() => pickLeaf(leaf, null), 50); // 다른 분류일 수 있어 스코프 해제
              setShowAnalytics(false);
            }}
          />
        </div>
      )}

      <div ref={scrollRef}
        onScroll={(e) => {
          const el = e.currentTarget;
          stickBottomRef.current = el.scrollHeight - el.scrollTop - el.clientHeight < 120;
        }}
        style={{ flex: 1, minHeight: 0, overflowY: 'auto', padding: '10px 10px 16px' }}>
        {messages.length === 0 && curLeaf && (() => {
          const m = mastery[curLeaf.id] || { coverage: 0, status: 'not_started' };
          const isMaster = m.status === 'mastered';
          const isResume = !isMaster && (m.coverage > 0 || m.status === 'in_progress');
          // 마스터된 leaf면 자동 다음 단원 카드 노출
          if (isMaster && nextLeaf) {
            return (
              <div style={{
                background: 'linear-gradient(180deg, #d1fae5 0%, #fff 100%)',
                border: '1px solid #6ee7b7', borderRadius: 14, padding: 18, marginTop: 12,
                textAlign: 'center',
              }}>
                <div style={{ fontSize: '2rem', marginBottom: 4 }}>✅</div>
                <div style={{ fontSize: '0.85rem', color: '#047857', fontWeight: 700, marginBottom: 4 }}>
                  {curLeaf.path.slice(-1)[0]} — 마스터 완료
                </div>
                <div style={{ fontSize: '0.78rem', color: '#374151', marginBottom: 12 }}>
                  다음은 {nextLeaf.path.slice(-1)[0]} 입니다
                </div>
                <div style={{ display: 'flex', gap: 6, justifyContent: 'center', flexWrap: 'wrap' }}>
                  <button
                    onClick={() => pickLeaf(nextLeaf)}
                    style={{
                      padding: '9px 16px', background: '#059669', color: '#fff', border: 'none',
                      borderRadius: 8, cursor: 'pointer', fontWeight: 700,
                      display: 'inline-flex', alignItems: 'center', gap: 6,
                    }}
                  >
                    다음 단원으로 <ArrowRight size={14} />
                  </button>
                  <button
                    onClick={() => quickSend('이 단원 복습 퀴즈 5문제 내줘. 함정 강조.')}
                    disabled={!cap.ok}
                    style={{
                      padding: '9px 16px', background: '#fff', color: '#065f46', border: '1px solid #6ee7b7',
                      borderRadius: 8, cursor: cap.ok ? 'pointer' : 'not-allowed', fontWeight: 600,
                    }}
                  >
                    🔁 복습 퀴즈
                  </button>
                </div>
              </div>
            );
          }
          // 2차 환영 카드 — 답안 작성 위주
          const isStage2 = getSubjectMeta(subjectId)?.stage === 2;
          if (isStage2) {
            const answerCount = m.answer_count || 0;
            const avgScore = Math.round(m.avg_score_pct || 0);
            return (
              <div style={{
                background: 'linear-gradient(180deg, #ede9fe 0%, #fff 100%)',
                border: '1px solid #c4b5fd', borderRadius: 14, padding: 18, marginTop: 12,
                textAlign: 'center',
              }}>
                <div style={{ fontSize: '2rem', marginBottom: 4 }}>✍️</div>
                <div style={{ fontSize: '0.78rem', color: '#7c3aed', fontWeight: 600, marginBottom: 4 }}>
                  {curLeaf.path.slice(1, -1).join(' › ')}
                </div>
                <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#111827', marginBottom: 6 }}>
                  {curLeaf.path.slice(-1)[0]}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#374151', marginBottom: 12 }}>
                  {answerCount > 0
                    ? `답안 ${answerCount}회 작성 · 평균 ${avgScore}% — 계속 연습?`
                    : '2차 단원입니다. 답안 작성·논점 추출 위주로 학습합니다.'}
                </div>
                <div style={{
                  background: '#fff', border: '1px solid #ddd6fe', borderRadius: 8,
                  padding: '8px 12px', marginBottom: 12, fontSize: '0.74rem', color: '#5b21b6',
                  display: 'inline-block',
                }}>
                  📂 단원 {curLeaf.unit_code || '—'} · {curLeaf.est_minutes ? `권장 ${curLeaf.est_minutes}분` : '서술형'}
                </div>
                {/* 2차 모드별 시작 버튼 */}
                <div style={{ display: 'flex', gap: 6, justifyContent: 'center', flexWrap: 'wrap' }}>
                  <button onClick={() => { setMode('concept_s2'); quickSend('이 단원의 첫 논점부터 답안에 어떻게 쓸지 같이 가르쳐줘.'); }}
                    disabled={!cap.ok}
                    style={{ padding: '9px 14px', background: '#7c3aed', color: '#fff', border: 'none',
                      borderRadius: 8, cursor: cap.ok ? 'pointer' : 'not-allowed', fontWeight: 700,
                      display: 'inline-flex', alignItems: 'center', gap: 6 }}>
                    <Play size={14} /> 개념 시작
                  </button>
                  <button onClick={() => setMode('answer_write')}
                    style={{ padding: '9px 14px', background: '#fff', color: '#5b21b6',
                      border: '1px solid #c4b5fd', borderRadius: 8, cursor: 'pointer', fontWeight: 700 }}>
                    📝 답안 작성
                  </button>
                  <button onClick={() => setMode('template')}
                    style={{ padding: '9px 14px', background: '#fff', color: '#5b21b6',
                      border: '1px solid #c4b5fd', borderRadius: 8, cursor: 'pointer', fontWeight: 600 }}>
                    📋 양식
                  </button>
                  <button onClick={() => setMode('mock_full')}
                    style={{ padding: '9px 14px', background: '#fff', color: '#5b21b6',
                      border: '1px solid #c4b5fd', borderRadius: 8, cursor: 'pointer', fontWeight: 600 }}>
                    🎬 실전 모의
                  </button>
                </div>
                {!curLeaf.unit_file && (
                  <div style={{ width: '100%', marginTop: 10, fontSize: '0.76rem', color: '#9a3412' }}>
                    ⚠️ 단원 자료가 없어 인수인계서만으로 진행됩니다.
                  </div>
                )}
                {/* 모의 history 미니 패널 */}
                {(() => {
                  const mocks = getMocks().filter((m) => m.subject_id === subjectId).slice(-5).reverse();
                  if (mocks.length === 0) return null;
                  return (
                    <div style={{ marginTop: 14, padding: 10, background: '#fff', border: '1px solid #ddd6fe',
                      borderRadius: 8, textAlign: 'left' }}>
                      <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#5b21b6', marginBottom: 6 }}>
                        🎬 최근 모의 ({mocks.length})
                      </div>
                      {mocks.map((m, i) => (
                        <div key={i} style={{ display: 'flex', justifyContent: 'space-between',
                          alignItems: 'center', fontSize: '0.72rem', padding: '3px 0',
                          borderTop: i > 0 ? '1px solid #f3f4f6' : 'none' }}>
                          <span style={{ color: '#6b7280' }}>{(m.ts || '').slice(0, 10)}</span>
                          <span style={{ fontWeight: 700, color: m.pct >= 70 ? '#16a34a' : m.pct >= 60 ? '#ea580c' : '#dc2626' }}>
                            {m.total}/{m.max} ({m.pct}%)
                          </span>
                          <span style={{ color: '#9ca3af' }}>{m.elapsed_min}분</span>
                        </div>
                      ))}
                    </div>
                  );
                })()}
              </div>
            );
          }
          return (
            <div style={{
              background: 'linear-gradient(180deg, #eef2ff 0%, #fff 100%)',
              border: '1px solid #c7d2fe', borderRadius: 14, padding: 18, marginTop: 12,
              textAlign: 'center',
            }}>
              <div style={{ fontSize: '2rem', marginBottom: 4 }}>👋</div>
              <div style={{ fontSize: '0.78rem', color: '#6366f1', fontWeight: 600, marginBottom: 4 }}>
                {curLeaf.path.slice(1, -1).join(' › ')}
              </div>
              <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#111827', marginBottom: 6 }}>
                {curLeaf.path.slice(-1)[0]}
              </div>
              <div style={{ fontSize: '0.85rem', color: '#374151', marginBottom: 10 }}>
                {isResume
                  ? `진척 ${Math.round((m.coverage || 0) * 100)}% — 이어서 진행할까요?`
                  : '새 단원 채팅방입니다. 한 사이클로 시작해 봅시다.'}
              </div>
              <div style={{
                background: '#fff', border: '1px solid #e0e7ff', borderRadius: 8,
                padding: '8px 12px', marginBottom: 12, fontSize: '0.78rem', color: '#4338ca',
                display: 'inline-block',
              }}>
                📂 {curLeaf.unit_code || '—'} · {curLeaf.section_name || '전체'}
                {curLeaf.section_key === 'auto' && curLeaf.section_lines && (
                  <span style={{ color: '#9ca3af', marginLeft: 6 }}>
                    ({curLeaf.section_lines[1] - curLeaf.section_lines[0]}줄 · 키워드 자동 매칭)
                  </span>
                )}
              </div>
              <div style={{ display: 'flex', gap: 6, justifyContent: 'center', flexWrap: 'wrap' }}>
                <button
                  onClick={() => quickSend(isResume
                    ? '직전에 멈춘 곳에서 자연스럽게 이어서 진행해줘.'
                    : '이 단원의 첫 절·관부터 한 사이클(개념→비유→확인 문제→피드백) 시작해줘.')}
                  disabled={!cap.ok}
                  style={{
                    padding: '9px 16px', background: '#4f46e5', color: '#fff', border: 'none',
                    borderRadius: 8, cursor: cap.ok ? 'pointer' : 'not-allowed', fontWeight: 700,
                    display: 'inline-flex', alignItems: 'center', gap: 6,
                  }}
                >
                  <Play size={14} />
                  {isResume ? '이어서 진행' : '이 단원 시작하기'}
                </button>
                <button
                  onClick={() => setMode('diagnose')}
                  style={{
                    padding: '9px 16px', background: '#fff', color: '#374151', border: '1px solid #d1d5db',
                    borderRadius: 8, cursor: 'pointer', fontWeight: 600,
                  }}
                >
                  🎯 약점부터 진단
                </button>
                {/* 둘러보기 점프 — 이 단원의 quiz 문제 수 표시 */}
                {onJumpToBrowse && getQuizCountForLeaf && (() => {
                  const n = getQuizCountForLeaf(curLeaf);
                  if (n <= 0) return null;
                  return (
                    <button
                      onClick={() => onJumpToBrowse(curLeaf)}
                      style={{
                        padding: '9px 16px', background: '#fff', color: '#1e40af',
                        border: '1px solid #c7d2fe', borderRadius: 8, cursor: 'pointer', fontWeight: 600,
                      }}
                    >
                      📚 기출 {n}문제 보기
                    </button>
                  );
                })()}
                {/* 단원 자료 없음 안내 */}
                {!curLeaf.unit_file && (
                  <div style={{ width: '100%', marginTop: 8, fontSize: '0.78rem', color: '#9a3412' }}>
                    ⚠️ 교재 단원 자료가 없어, 인수인계서만으로 학습이 진행됩니다.
                  </div>
                )}
              </div>
            </div>
          );
        })()}
        {messages.length === 0 && weakSuggestion.length > 0 && (
          <div style={{
            background: '#fff7ed', border: '1px solid #fed7aa', borderRadius: 10, padding: 12, marginTop: 16,
          }}>
            <div style={{ fontWeight: 700, color: '#9a3412', marginBottom: 6, fontSize: '0.9rem' }}>
              ⚠️ 기출에서 자주 틀린 단원 — 우선 학습 추천
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {weakSuggestion.map((w) => (
                <button
                  key={w.leaf.id}
                  onClick={() => { pickLeaf(w.leaf, null); setWeakSuggestion([]); }}
                  style={{
                    textAlign: 'left', padding: '8px 10px', background: '#fff',
                    border: '1px solid #fed7aa', borderRadius: 8, cursor: 'pointer',
                  }}
                >
                  <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#111827' }}>
                    {w.leaf.path.slice(-1)[0]}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#9a3412' }}>
                    오답률 {Math.round(w.wrong_rate * 100)}% ({w.correct}/{w.attempts}) · {w.leaf.path.slice(1, -1).join(' › ')}
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
        {/* 🧠 개인화 배지 — AI가 학생이 직접 쓴 노트·약점을 참고 중임을 보여준다 */}
        {messages.length === 0 && curLeaf && (() => {
          const sn = getSubjectMeta(subjectId)?.tax_key || getSubjectMeta(subjectId)?.title || '';
          const ps = personalNoteStats(sn);
          if (!ps.notes && !ps.mistakes) return null;
          const bits = [];
          if (ps.notes) bits.push(`내 오답노트 ${ps.notes}개`);
          if (ps.mistakes && ps.topLabel) bits.push(`자주 하는 '${ps.topLabel}' 실수`);
          return (
            <div style={{ background: '#eef2ff', border: '1px solid #c7d2fe', borderRadius: 10, padding: '10px 12px', marginTop: 12, display: 'flex', alignItems: 'flex-start', gap: 8 }}>
              <Brain size={16} color="#4338ca" style={{ marginTop: 2, flexShrink: 0 }} />
              <div style={{ fontSize: '0.8rem', color: '#3730a3', lineHeight: 1.55 }}>
                <b>AI가 내 노트를 참고해요</b> — {bits.join(' · ')}을(를) 반영해 개인화된 설명과 확인 질문을 합니다.
              </div>
            </div>
          );
        })()}
        {messages.map((m, i) => {
          const isLast = i === messages.length - 1;
          const showChoices = isLast && !streaming && mode === 'practice' && m.role === 'assistant';
          const opts = showChoices ? extractMultipleChoice(m.content) : null;
          const fadeIn = isLast && m.role === 'assistant' && !streaming;
          // 2차 채점 결과 카드 — 마지막 assistant 메시지에 graded:true, stage:2 JSON 있을 때
          let scoringResult = null;
          if (isLast && m.role === 'assistant' && !streaming) {
            const blocks = extractJsonBlocks(m.content);
            scoringResult = blocks.find((b) => b?.graded === true && b?.stage === 2);
          }
          return (
            <div key={i}>
              <MessageBubble msg={m} fadeIn={fadeIn} leafId={current?.leaf_id} leafTitle={curLeaf?.path?.slice(-1)[0]} />
              {opts && (
                <AnswerChoiceRow
                  options={opts}
                  disabled={streaming || !cap.ok}
                  onPick={(o) => quickSend(`${CIRCLED_DIGITS[o.n - 1]}번 — ${o.text}`)}
                />
              )}
              {scoringResult && (
                <ScoringResultCard
                  result={scoringResult}
                  onRewrite={() => quickSend('같은 논점으로 다시 답안 작성할게. 같은 문제 다시 보여줘.')}
                  onShowModel={() => quickSend('이 문제의 모범 답안과 핵심 키워드를 보여줘.')}
                />
              )}
              {/* 🔄 답변 다시 생성 — 마지막 assistant 응답에만, 생성 중엔 숨김 */}
              {isLast && m.role === 'assistant' && !streaming && (
                <div style={{ display: 'flex', justifyContent: 'flex-start', gap: 6, margin: '2px 0 6px 4px' }}>
                  {lastTruncated && (
                    <button onClick={() => { setLastTruncated(false); quickSend('방금 답변이 중간에 끊겼어. 끊긴 지점부터 이어서 계속 작성해줘.'); }}
                      disabled={!cap.ok}
                      title="한도로 잘린 답변을 이어서 작성"
                      style={{ display: 'inline-flex', alignItems: 'center', gap: 5,
                        padding: '6px 12px', borderRadius: 999, cursor: cap.ok ? 'pointer' : 'default',
                        border: '1px solid #fcd34d', background: '#fffbeb',
                        color: '#b45309', fontSize: '0.74rem', fontWeight: 800 }}>
                      ✍️ 이어쓰기
                    </button>
                  )}
                  <button onClick={regenerate} disabled={!cap.ok}
                    title="마지막 답변을 버리고 같은 질문으로 다시 생성"
                    style={{ display: 'inline-flex', alignItems: 'center', gap: 5,
                      padding: '6px 12px', borderRadius: 999, cursor: cap.ok ? 'pointer' : 'default',
                      border: `1px solid ${TOSS.line}`, background: '#fff',
                      color: TOSS.sub, fontSize: '0.74rem', fontWeight: 700 }}>
                    <RotateCcw size={12} /> 답변 다시 생성
                  </button>
                </div>
              )}
            </div>
          );
        })}
        {streaming && draft && (
          // streaming 중에도 ParsedText로 마크다운/수식 렌더링 (sanitize로 미닫힌 토큰 자동 보정)
          <div style={{ display: 'flex', justifyContent: 'flex-start', margin: '8px 0' }}>
            <div style={{
              maxWidth: '98%', padding: '12px 16px', borderRadius: 14,
              background: '#f3f4f6', color: '#111827',
              fontSize: '0.95rem', lineHeight: 1.6,
              whiteSpace: 'pre-wrap', wordBreak: 'break-word',
            }}>
              <ParsedText text={draft} />
              <span className="ai-streaming-cursor" style={{
                display: 'inline-block', width: 8, height: '1em',
                background: '#4f46e5', marginLeft: 2, verticalAlign: 'text-bottom',
                animation: 'aiCursorBlink 1s steps(2) infinite',
              }} />
            </div>
          </div>
        )}
        {streaming && !draft && (
          <div style={{ padding: 12, color: '#6b7280', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ display: 'inline-flex', gap: 4 }}>
              <span className="ai-thinking-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: '#4f46e5', animation: 'aiThink 1.2s ease-in-out infinite' }} />
              <span className="ai-thinking-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: '#4f46e5', animation: 'aiThink 1.2s ease-in-out 0.2s infinite' }} />
              <span className="ai-thinking-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: '#4f46e5', animation: 'aiThink 1.2s ease-in-out 0.4s infinite' }} />
            </span>
            생각하는 중…{thinkSec >= 3 ? ` ${thinkSec}s` : ''}
          </div>
        )}
        {error && (
          <div style={{ background: '#fef2f2', color: '#991b1b', padding: 10, borderRadius: 8, fontSize: '0.85rem', marginTop: 10, border: '1px solid #fecaca', display: 'flex', alignItems: 'flex-start', gap: 8, justifyContent: 'space-between' }}>
            <span style={{ flex: 1, minWidth: 0 }}>{error}</span>
            {lastFailedText && !streaming && (
              <button
                onClick={() => { const t = lastFailedText; setLastFailedText(''); setError(''); quickSend(t); }}
                style={{ flex: '0 0 auto', padding: '4px 10px', fontSize: '0.78rem', fontWeight: 700, background: '#fff', color: '#991b1b', border: '1px solid #fecaca', borderRadius: 6, cursor: 'pointer', minHeight: 32 }}
              >↻ 다시 보내기</button>
            )}
          </div>
        )}
        {confirmAction && (
          <div style={{
            background: confirmAction.danger ? '#fef2f2' : '#eef2ff',
            border: `1px solid ${confirmAction.danger ? '#fecaca' : '#c7d2fe'}`,
            color: confirmAction.danger ? '#991b1b' : '#1e40af',
            padding: 12, borderRadius: 10, marginTop: 10,
            display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap',
          }}>
            <div style={{ flex: 1, fontSize: '0.88rem', fontWeight: 600 }}>{confirmAction.label}?</div>
            <button
              onClick={() => { const a = confirmAction; setConfirmAction(null); a.onYes && a.onYes(); }}
              style={{
                padding: '6px 14px', fontSize: '0.85rem', fontWeight: 700,
                background: confirmAction.danger ? '#dc2626' : '#4f46e5',
                color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer',
              }}
            >
              네
            </button>
            <button
              onClick={() => setConfirmAction(null)}
              style={{
                padding: '6px 14px', fontSize: '0.85rem',
                background: '#fff', color: '#374151', border: '1px solid #d1d5db', borderRadius: 6, cursor: 'pointer',
              }}
            >
              취소
            </button>
          </div>
        )}
        {idlePromptShown && !streaming && messages.length > 0 && (
          <div style={{
            background: '#ecfdf5', color: '#065f46', padding: 12, borderRadius: 10,
            marginTop: 10, border: '1px solid #a7f3d0',
          }}>
            <div style={{ fontWeight: 700, marginBottom: 4 }}>⏱️ 10분간 응답이 없네요</div>
            <div style={{ fontSize: '0.85rem', marginBottom: 8 }}>오늘 학습 정리하고 다음 추천 받을까요?</div>
            <div style={{ display: 'flex', gap: 6 }}>
              <button
                onClick={() => { clearIdleTimer(); quickSend('오늘 학습 정리해줘. 끝.'); }}
                style={{ padding: '6px 14px', background: '#059669', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontWeight: 700 }}
              >
                정리하기
              </button>
              <button
                onClick={clearIdleTimer}
                style={{ padding: '6px 14px', background: '#fff', color: '#374151', border: '1px solid #d1d5db', borderRadius: 6, cursor: 'pointer' }}
              >
                닫기
              </button>
            </div>
          </div>
        )}
        {pendingNext && (
          <div style={{
            background: '#eef2ff', color: '#1e40af', padding: 12, borderRadius: 10,
            marginTop: 10, border: '1px solid #c7d2fe',
          }}>
            <div style={{ fontWeight: 700, marginBottom: 4 }}>
              📌 다음 추천: {pendingNext.leaf.path.slice(-1)[0]}
            </div>
            <div style={{ fontSize: '0.78rem', color: '#3730a3', marginBottom: 4 }}>
              {pendingNext.leaf.path.join(' › ')}
            </div>
            {pendingNext.reason && <div style={{ fontSize: '0.85rem', marginBottom: 8 }}>{pendingNext.reason}</div>}
            <div style={{ display: 'flex', gap: 6 }}>
              <button
                onClick={() => { pickLeaf(pendingNext.leaf); setPendingNext(null); }}
                style={{ padding: '6px 14px', background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontWeight: 700 }}
              >
                이 단원으로 이동
              </button>
              <button
                onClick={() => setPendingNext(null)}
                style={{ padding: '6px 14px', background: '#fff', color: '#374151', border: '1px solid #d1d5db', borderRadius: 6, cursor: 'pointer' }}
              >
                나중에
              </button>
            </div>
          </div>
        )}
      </div>

      <div style={{ padding: 10, borderTop: '1px solid #e5e7eb', background: '#fff' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
          <div style={{ display: 'flex', gap: 4, overflowX: 'auto', paddingBottom: 2, flex: 1, minWidth: 0 }}>
          {({
            // 1차
            study: [
              [Play, '이 단원 시작', '이 단원을 처음부터 시작하자. ① 오늘 다룰 범위를 한 줄로 예고하고 ② 첫 개념을 「일상 언어 → 한자 풀이 → 생활 비유 → 교재 표현」 순서로 설명한 뒤 ③ 이해 확인용 쉬운 OX 2문제를 내줘. 한 번에 개념 하나씩만, 내가 답하면 다음으로 넘어가자.'],
              [RefreshCw, '이어서 진행', '직전에 어디까지 했는지 한 줄로 짚어주고 거기서부터 이어서 진행해줘. 앞에서 내가 틀렸거나 헷갈려 한 부분이 있으면 그것부터 짧게 복습시킨 다음 넘어가줘.'],
              [Lightbulb, '더 쉽게', '방금 설명을 더 쉽게 다시 풀어줘. 전문용어는 최대한 빼고, 구체적인 숫자 예시와 일상 비유를 들어서 처음 배우는 사람도 이해할 수준으로. 마지막에 한 문장 요약을 붙여줘.'],
              [Flag, '오늘 끝 · 정리', '오늘 학습을 마무리하자. ① 오늘 다룬 개념 3~5줄 요약 ② 내가 약했던 포인트 ③ 다음에 이어서 볼 지점 ④ 복습용 핵심 키워드 5개 순으로 정리해줘.'],
            ],
            practice: [
              [FileText, '기출 한 문제', '이 단원 기출 유형으로 5지선다 1문제를 내줘. 지금은 정답을 알려주지 말고 문제만 제시해줘. 내가 답을 고르면 그때 정답과 해설, 오답 선지별 함정을 짚어줘.'],
              [Shuffle, '다른 문제', '같은 단원의 다른 논점으로 5지선다 1문제 더 내줘. 앞 문제와 겹치지 않는 포인트로, 역시 정답은 내가 답한 뒤에.'],
              [CheckCircle2, '정답 · 해설', '방금 문제의 정답과 해설을 알려줘. 각 선지가 왜 맞고 틀렸는지 하나씩 짚고, 이 문제의 핵심 함정과 앞으로 나올 수 있는 변형 방향까지 알려줘.'],
            ],
            deep: [
              [Brain, '더 깊게', '이 개념을 시험 수준보다 한 단계 깊게 설명해줘. 이론적 배경, 학설 대립이 있다면 통설과 소수설, 그리고 실제 출제된 심화 논점까지 짚어줘.'],
              [AlertTriangle, '함정 분석', '이 단원에서 수험생이 자주 틀리는 함정 5개를 표로 정리해줘. 열은 「함정 / 틀리는 이유 / 올바른 이해 / 관련 출제 포인트」로.'],
              [GitCompare, '유사 개념 비교', '이 단원에서 헷갈리기 쉬운 유사 개념들을 비교표로 정리해줘. 구별 기준을 명확히 하고, 각 항목에 한 줄 암기 팁을 붙여줘.'],
            ],
            summary: [
              [Zap, '핵심 카드', '이 단원 핵심을 압축 카드 한 장으로 만들어줘. 「정의 / 핵심 산식·명제 / 빈출 포인트 / 두문자 암기법 / 자주 틀리는 함정」 순서로 간결하게.'],
              [Bookmark, '다음 카드', '다음 절·관의 핵심 카드로 넘어가줘. 앞과 같은 형식으로 만들어줘.'],
              [ListOrdered, '빈출 5', '이 단원에서 시험에 가장 자주 나오는 5가지를 빈출 순으로 정리해줘. 각각 한 줄 설명과 어떤 형태로 출제되는지를 함께.'],
            ],
            diagnose: [
              [Target, '진단 시작', '이 단원 이해도를 진단하자. 핵심 5문제(OX 3 + 단답 2)를 번호를 붙여 한 번에 내줘. 정답은 내가 5개를 한 메시지로 답한 다음에 알려줘.'],
              [Activity, '약점만 다시', '방금 진단에서 틀린 것만 골라 다시 가르쳐줘. 왜 틀렸는지 원인부터 짚고, 같은 함정을 쓰는 변형 문제 1개로 확인시켜줘.'],
              [ClipboardList, '종합 진단', '진단 결과를 표로 정리해줘. 열은 「문항 / 정오 / 관련 개념 / 보완 필요도」로. 그리고 다음에 학습하면 좋을 단원을 추천해줘.'],
            ],
            // 1차 회계 — 분개 채점
            journal: [
              [PenLine, '분개 시작', '분개 드릴을 시작하자. 인사말 없이 바로, 이 단원에 맞는 짧은 거래 상황 1개(구체 숫자 포함)를 주고 내가 차변/대변으로 분개하도록 물어봐줘. 채점은 내가 분개를 쓴 뒤에.'],
              [CheckCircle2, '채점해줘', '방금 내가 쓴 분개를 채점해줘. 어느 계정·어느 방향(차변/대변)이 틀렸는지 정확히 짚고, 올바른 분개와 이 거래가 재무상태표·손익계산서에 미치는 영향을 1~2줄로 알려줘. 그다음 조금 더 어려운 거래로 넘어가줘.'],
              [Shuffle, '다른 거래', '같은 단원의 다른 유형 거래 1개를 더 내줘. 앞과 겹치지 않는 계정이 나오게, 역시 분개는 내가 한 뒤에 채점.'],
            ],
            // 1차 회계·경제 — 계산 단계 코칭
            calc: [
              [Calculator, '계산 시작', '이 단원 계산 유형 1문제를 내고, 한 번에 풀지 말고 한 단계씩 나를 이끌어줘. "먼저 무슨 식/틀(와꾸)을 써야 할까?"부터 물어봐줘. 정답은 마지막에.'],
              [Lightbulb, '다음 단계 힌트', '지금 막혔어. 답을 주지 말고 다음 한 단계만 힌트로 알려줘.'],
              [CheckCircle2, '검산', '내 답을 같은 방식 재계산 말고 다른 경로로 검산하는 법을 알려줘(예: 총액↔단가 역산, 대차평균, 단위 확인).'],
            ],
            // 2차
            concept_s2: [
              [Play, '논점 도입', '이 단원의 첫 논점부터 시작하자. 논점의 의의와 쟁점을 짚고, 실제 답안에서 이 논점을 어떤 목차·분량으로 쓰는지까지 함께 가르쳐줘.'],
              [ClipboardList, '답안 골격', '이 논점의 답안 골격을 Ⅰ·Ⅱ·Ⅲ 목차로 보여줘. 각 목차에 들어갈 핵심 문장과 배점 비중도 함께.'],
              [RefreshCw, '이어서', '직전에 멈춘 논점부터 이어서 진행해줘. 앞서 약했던 부분이 있으면 먼저 짚어주고.'],
            ],
            template: [
              [ClipboardList, '양식 한 장', '이 단원의 빈출 논점 답안 양식을 한 장으로 보여줘. 목차 구조와 각 항목의 필수 키워드를 포함해서.'],
              [HelpCircle, '빈칸 퀴즈', '방금 양식에서 핵심 키워드 5개를 빈칸으로 만들어 내줘. 내가 채우면 채점해줘.'],
              [ListOrdered, '빈출 양식 3', '이 단원 빈출 답안 양식 3개를 표로 정리해줘. 열은 「논점 / 목차 구조 / 필수 키워드 / 배점」으로.'],
            ],
            topic_extract: [
              [Search, '사례 분석', '이 단원 빈출 사례 1개를 제시하고, 내가 어떤 논점을 다룰지 먼저 답하도록 물어봐줘. 정답 논점은 내가 답한 뒤에.'],
              [Lightbulb, '정답 논점', '방금 사례에서 다뤄야 할 정답 논점과 답안에서의 배치 순서를 알려줘. 놓치기 쉬운 부수 논점도 함께.'],
              [Shuffle, '다른 사례', '같은 주제의 다른 사례 1개를 더 제시해줘. 앞 사례와 논점이 겹치지 않게.'],
            ],
            answer_write: [
              [PenLine, '답안 문제', '이 단원에서 30점 분량 답안 문제 1개를 출제해줘. 내가 답안을 작성하면 목차·논점·분량 기준으로 채점하고 첨삭해줘.'],
              [Target, '40점 문제', '40점짜리 사례형 논술 1개를 출제해줘. 사실관계를 구체적으로 주고, 배점 배분도 함께 제시해줘.'],
              [BookOpen, '모범 답안', '방금 문제의 모범 답안을 목차 형태로 보여줘. 각 목차별 필수 문장과 득점 포인트를 표시해줘.'],
            ],
            mock_full: mockSession ? [
              [SkipForward, '다음 문제', '__nextMock__'],
              [Flag, '마무리 · 종합', '__endMock__'],
            ] : [
              [Play, '모의 시작', '__startMock__'],
            ],
            calc_s2: [
              [Calculator, '계산 시범', '이 논점의 계산 산식을 단계별로 시범 보여줘. 각 단계에서 어떤 값을 왜 쓰는지 설명하면서.'],
              [AlertTriangle, '함정 체크', '이 계산에서 자주 빠뜨리는 함정 3개를 알려줘. 각각 실제로 어떻게 감점되는지와 함께.'],
              [Layers, '답안 적용', '이 계산 결과를 답안에 어떻게 서술할지 실제 문장으로 보여줘. 산식 제시 방식과 단위 표기까지.'],
            ],
          }[mode] || []).map(([Icon, label, prompt]) => (
            <button
              key={label}
              disabled={streaming || !cap.ok}
              onClick={() => {
                if (prompt === '__startMock__') startMock();
                else if (prompt === '__nextMock__') nextMockQuestion();
                else if (prompt === '__endMock__') { setMockSession((s) => s ? { ...s, complete: true } : s); quickSend('모의 종료. 누적 점수·시간 분석·약점 단원 종합 정리.'); }
                else quickSend(prompt);
              }}
              title={prompt.startsWith('__') ? label : prompt}
              style={{
                flex: '0 0 auto', display: 'inline-flex', alignItems: 'center', gap: 5,
                padding: '6px 11px', borderRadius: 8,
                border: '1px solid #e7e5e4', background: '#fafaf9', color: '#44403c',
                fontSize: '0.78rem', fontWeight: 700, letterSpacing: '-0.01em',
                cursor: streaming || !cap.ok ? 'not-allowed' : 'pointer',
                whiteSpace: 'nowrap', opacity: streaming || !cap.ok ? 0.45 : 1,
              }}
            >
              <Icon size={13} strokeWidth={2.2} style={{ flexShrink: 0, color: '#78716c' }} />
              {label}
            </button>
          ))}
          </div>
          <label style={{ display: 'inline-flex', alignItems: 'center', gap: 4, flexShrink: 0, fontSize: '0.72rem', color: '#9ca3af' }}>
            <span>모델</span>
            <select
              value={prefs.model}
              onChange={(e) => { const next = setPrefs({ model: e.target.value }); setPrefsState(next); }}
              disabled={streaming}
              style={{
                padding: '3px 6px', fontSize: '0.72rem', fontWeight: 700,
                border: '1px solid #e7e5e4', borderRadius: 6,
                background: streaming ? '#f5f5f4' : '#fafaf9',
                color: '#57534e', cursor: streaming ? 'not-allowed' : 'pointer',
              }}
              title="응답 중에는 변경할 수 없습니다"
            >
              <optgroup label="🌙 Moonshot (Kimi · 저렴+강력, 추천)">
                <option value="moonshot:kimi-k2.6">🌙 Kimi K2.6 (가성비)</option>
                <option value="moonshot:kimi-k3">🌙 Kimi K3 (최상급)</option>
                <option value="moonshot:kimi-k2.5">🌙 Kimi K2.5 (최저가)</option>
              </optgroup>
              {localModels.length > 0 && (
                <optgroup label="🖥 로컬 (Ollama · 무료·오프라인)">
                  {localModels.map((m) => (
                    <option key={m.ref} value={m.ref}>💰 {m.label}{m.sizeGB ? ` (${m.sizeGB}GB)` : ''}</option>
                  ))}
                </optgroup>
              )}
              <optgroup label="Anthropic (브라우저 직호출)">
                <option value="claude-sonnet-4-6">🎯 Sonnet 4.6</option>
                <option value="claude-haiku-4-5-20251001">⚡ Haiku 4.5</option>
                <option value="claude-opus-4-7">🧠 Opus 4.7</option>
              </optgroup>
              <optgroup label="OpenAI (프록시 필요)">
                <option value="gpt-5.4">🔵 GPT-5.4</option>
                <option value="gpt-5.4-mini">🔵 GPT-5.4 mini</option>
              </optgroup>
              <optgroup label="Google (CORS 통과 가능 / 일부 프록시 필요)">
                <option value="gemini-3.5-flash">🟢 Gemini 3.5 Flash</option>
                <option value="gemini-3.1-pro-preview">🟢 Gemini 3.1 Pro</option>
                <option value="gemini-3.1-flash-lite">🟢 Gemini 3.1 Flash Lite</option>
              </optgroup>
            </select>
          </label>
        </div>
        {mode === 'template' && subjectId === 'appraisal_theory' && problemsMd && (
          <TemplateCardWidget
            templatesMd={problemsMd}
            onAskAI={(card) => quickSend(`답안 양식 ${card.id}을 더 자세히 풀어 설명해주세요. 골격·핵심 키워드·이 양식이 잘 쓰이는 논점·40점 답안 분량으로 펼치면 어떻게 되는지.`)}
          />
        )}
        {mode === 'template' && subjectId === 'appraisal_law' && problemsMd && (
          <LawCasesWidget
            casesMd={problemsMd}
            onAskAI={(card) => quickSend(`대판 ${card.caseNo}(${card.date}) 판례를 답안에서 어떻게 인용하는지 시범 보여주세요. 의의·요건·판시사항 핵심 + 답안 인용 형식.`)}
          />
        )}
        {mode === 'answer_write' && (
          <>
            <AnswerHistoryWidget
              leafId={current?.leaf_id}
              onLoadAnswer={(prevText) => {
                if (typeof window !== 'undefined' && prevText) {
                  setInput(`[이전 답안 불러옴]\n${prevText}`);
                }
              }}
            />
            <AnswerWriteInput
              scorePoint={30}
              disabled={streaming || !cap.ok}
              onSubmit={({ answer, score_point, time_used_sec, time_target_min }) => {
                const min = Math.round(time_used_sec / 60);
                const text = `[답안 작성 — ${score_point}점, ${min}분 사용, 목표 ${time_target_min}분]\n\n${answer}\n\n위 답안을 채점해주세요. 점수·강점·보강·재작성 힌트를 JSON으로.`;
                quickSend(text);
              }}
            />
          </>
        )}
        {/* 📷 첨부 사진 미리보기 */}
        {pendingImage && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6,
            padding: '6px 8px', background: '#f5f3ff', border: '1px solid #ddd6fe', borderRadius: 10 }}>
            <img src={pendingImage.dataUrl} alt="첨부한 문제 사진"
              style={{ height: 52, borderRadius: 6, border: '1px solid #c4b5fd' }} />
            <span style={{ flex: 1, fontSize: '0.74rem', color: '#5b21b6', fontWeight: 600 }}>
              📷 문제 사진 첨부됨 — 전송하면 AI가 풀이하고 관련 단원을 알려줘요
            </span>
            <button onClick={() => setPendingImage(null)} aria-label="사진 제거"
              style={{ border: 'none', background: 'none', color: '#7c3aed', fontWeight: 800,
                cursor: 'pointer', fontSize: '1rem', padding: 4 }}>✕</button>
          </div>
        )}
        <div style={{ display: 'flex', gap: 6, alignItems: 'flex-end', marginTop: mode === 'answer_write' ? 8 : 0 }}>
          {getProviderForModel(prefs.model) === 'anthropic' && (
            <label aria-label="문제 사진 첨부" title="막힌 문제를 찍어서 질문"
              style={{ padding: '10px 11px', borderRadius: 10, cursor: (cap.ok && !streaming) ? 'pointer' : 'not-allowed',
                border: `1px solid ${pendingImage ? '#a78bfa' : '#d1d5db'}`,
                background: pendingImage ? '#f5f3ff' : '#fff', fontSize: '1.05rem', lineHeight: 1,
                opacity: (cap.ok && !streaming) ? 1 : 0.5 }}>
              📷
              <input type="file" accept="image/*" style={{ display: 'none' }}
                disabled={!cap.ok || streaming}
                onChange={(e) => { attachImage(e.target.files?.[0]); e.target.value = ''; }} />
            </label>
          )}
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              // 한글 IME 조합 중 Enter는 글자 확정용이므로 전송하지 않음
              if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); send(); }
            }}
            placeholder={cap.ok
              ? (mode === 'answer_write' ? '추가 질문이나 모범 답안 요청...' : '메시지를 입력하세요 (Enter 전송, Shift+Enter 줄바꿈)')
              : '오늘 cap 도달'}
            disabled={!cap.ok || streaming}
            rows={mode === 'answer_write' ? 1 : 2}
            style={{
              flex: 1, padding: '10px 12px', border: '1px solid #d1d5db', borderRadius: 10,
              // 16px 미만이면 iOS Safari가 포커스 시 페이지를 확대(zoom)함 → 16px 고정
              fontSize: '16px', resize: 'none', fontFamily: 'inherit',
              background: !cap.ok ? '#f9fafb' : '#fff',
            }}
          />
          {streaming ? (
            <button onClick={stop} style={{
              padding: '10px 14px', background: '#fef2f2', color: '#991b1b',
              border: '1px solid #fecaca', borderRadius: 10, cursor: 'pointer', fontWeight: 700,
            }}>중단</button>
          ) : (
            <button
              onClick={send}
              disabled={!(input.trim() || pendingImage) || !cap.ok}
              style={{
                padding: '10px 14px',
                background: (input.trim() || pendingImage) && cap.ok ? '#4f46e5' : '#e5e7eb',
                color: (input.trim() || pendingImage) && cap.ok ? '#fff' : '#9ca3af',
                border: 'none', borderRadius: 10, cursor: (input.trim() || pendingImage) && cap.ok ? 'pointer' : 'not-allowed',
                display: 'flex', alignItems: 'center', gap: 4, fontWeight: 700,
              }}
            >
              <Send size={16} />
            </button>
          )}
        </div>
      </div>
      </div>{/* /right column (PC) — wrapper added for 2-col grid */}
      {/* PC 3단째: 우측 교재 원문 패널 — AI가 참고하는 원문을 대화와 나란히 */}
      {isDesktop && showDoc && (
        <aside style={{ borderLeft: '1px solid #e5e7eb', background: '#fbfbfd', display: 'flex', flexDirection: 'column', overflow: 'hidden', minHeight: 0 }}>
          <div style={{ padding: '7px 8px', borderBottom: '1px solid #e5e7eb', background: '#fff', display: 'flex', alignItems: 'center', gap: 4, flex: '0 0 auto' }}>
            {[
              ['doc', '📖 이론'],
              // 교재에 그 절이 없어도 **강의 필기만 있으면** 탭을 띄운다.
              // 안 그러면 필기가 갈 탭이 통째로 안 보여 내용이 사라진다.
              ...(docParts.ox ? [['ox', '✅ OX']] : []),
              ...(docParts.mem || lectureByTab.mem ? [['mem', '🧠 암기']] : []),
              ...(docParts.prac || lectureByTab.prac ? [['prac', '🧮 연습']] : []),
              ...(docParts.std || lectureByTab.std ? [['std', '📐 기준서']] : []),
              ...(docParts.law || lectureByTab.law ? [['law', '⚖️ 법전']] : []),
              ['drill', drillN > 0 ? `🎯 인출 ${drillN}` : '🎯 인출'],
            ].map(([k, lab]) => (
              <button key={k} onClick={() => setDocTab(k)}
                style={{ fontSize: '0.73rem', fontWeight: 800, padding: '5px 9px', borderRadius: 6, cursor: 'pointer',
                  border: docTab === k ? '1px solid #d6d3d1' : '1px solid transparent',
                  background: docTab === k ? '#f5f5f4' : 'none', color: docTab === k ? '#1c1917' : '#a8a29e' }}>
                {lab}
              </button>
            ))}
            {(docTab === 'doc' || docTab === 'mem') && (
              <button
                onClick={() => setMaskHl((v) => !v)}
                title={maskHl ? '형광펜 다시 보이기' : '형광펜 가리기 — 암기 시트처럼 핵심어를 가리고 클릭하면 드러납니다'}
                style={{ marginLeft: 'auto', fontSize: '0.72rem', fontWeight: 800, padding: '4px 8px', borderRadius: 6,
                  cursor: 'pointer', border: '1px solid ' + (maskHl ? '#a16207' : '#e7e5e4'),
                  background: maskHl ? '#faf8f2' : '#fff', color: maskHl ? '#a16207' : '#78716c' }}
              >
                {maskHl ? '👁 보이기' : '🔒 가리기'}
              </button>
            )}
            <button onClick={() => setShowDoc(false)} title="패널 숨기기" style={{ marginLeft: (docTab === 'doc' || docTab === 'mem') ? 4 : 'auto', background: 'none', border: 'none', cursor: 'pointer', color: '#9ca3af', fontSize: '0.95rem', lineHeight: 1 }}>✕</button>
          </div>
          <div
            className={maskHl ? 'hl-mask' : undefined}
            onClick={maskHl ? (e) => {
              // 가리기 모드에서 형광펜을 클릭하면 그 항목만 드러낸다(다시 누르면 가림)
              const m = e.target.closest && e.target.closest('mark');
              if (m) m.classList.toggle('hl-open');
            } : undefined}
            style={{ flex: 1, overflowY: 'auto', padding: '12px 16px', fontSize: '0.84rem', lineHeight: 1.75, color: '#374151' }}>
            {docTab === 'drill' ? (
              <DailyDrill
                onGoLeaf={(it) => {
                  const lf = leaves.find((l) => l.id === it.leafId);
                  if (lf) { pickLeaf(lf); setDocTab('doc'); }
                }}
              />
            ) : ['doc','ox','mem','law','prac','std'].includes(docTab) ? (
              (() => {
                const body = docTab === 'ox' ? docParts.ox : docTab === 'mem' ? docParts.mem
                  : docTab === 'law' ? docParts.law : docTab === 'prac' ? docParts.prac
                  : docTab === 'std' ? docParts.std : (docParts.theory || sectionMd || unitMd);
                // 교재와 강의 설명을 **한 흐름으로 합쳐서** 보여준다.
                // 뒤에 통째로 붙이면 같은 주제를 두 번 읽게 되고 둘이 따로 논다.
                // 필기의 `<!-- after: … -->` 앵커가 교재 어느 소제목 뒤에 들어갈지 정한다.
                // 암기·법전·연습·기준서 탭도 각자 몫의 필기를 받는다(lectureByTab).
                // OX 탭만 예외 — 아래 OXQuiz 가 지문을 파싱해 퀴즈로 만들기 때문에 섞으면 깨진다.
                const lecPart = docTab === 'doc' ? lectureByTab.theory : lectureByTab[docTab];
                const merged = docTab === 'ox' ? body : mergeLectureIntoDoc(body, lecPart);
                if (docTab === 'ox' && body) return <OXQuiz md={body} />;
                if (merged) return <ParsedText text={merged} />;
                return (
                  <div style={{ color: '#9ca3af', fontSize: '0.82rem', textAlign: 'center', marginTop: 48, lineHeight: 1.6 }}>
                    {docTab === 'ox' ? <>이 관의 OX 확인문제는<br />아직 준비되지 않았습니다.</>
                      : docTab === 'mem' ? <>이 관의 암기법은<br />아직 준비되지 않았습니다.</>
                      : docTab === 'law' ? <>이 관의 법조문 원문은<br />아직 준비되지 않았습니다.</>
                      : docTab === 'prac' ? <>이 관의 계산 연습은<br />아직 준비되지 않았습니다.</>
                      : docTab === 'std' ? <>이 관의 기준서 원문은<br />아직 준비되지 않았습니다.</>
                      : <>단원을 선택하면<br />AI가 참고하는 교재 원문을<br />여기서 함께 볼 수 있어요.</>}
                  </div>
                );
              })()
            ) : (
              (() => {
                const m = (mastery && current?.leaf_id) ? (mastery[current.leaf_id] || {}) : {};
                const qs = (quizStatsByLeaf && current?.leaf_id) ? quizStatsByLeaf[current.leaf_id] : null;
                const cov = Math.round((m.coverage || 0) * 100);
                const acc = m.attempted ? Math.round((m.accuracy || 0) * 100) : null;
                const Bar = ({ pct, color }) => (
                  <div style={{ height: 8, background: '#eef0f2', borderRadius: 999, overflow: 'hidden', marginTop: 4 }}>
                    <div style={{ width: `${Math.min(100, pct)}%`, height: '100%', background: color }} />
                  </div>
                );
                const Row = ({ label, value, pct, color }) => (
                  <div style={{ marginBottom: 14 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', fontWeight: 700, color: '#374151' }}>
                      <span>{label}</span><span style={{ color }}>{value}</span>
                    </div>
                    {pct != null && <Bar pct={pct} color={color} />}
                  </div>
                );
                return (
                  <div>
                    <div style={{ fontSize: '0.78rem', fontWeight: 800, color: '#111827', marginBottom: 12 }}>이 단원 진행</div>
                    <Row label="AI 학습 커버리지" value={`${cov}%`} pct={cov} color="#4f46e5" />
                    <Row label="이해도(채점)" value={acc == null ? '기록 없음' : `${acc}% · ${m.attempted}회`} pct={acc == null ? null : acc} color="#059669" />
                    {qs && <Row label="기출 진행" value={`${qs.answered || 0}/${qs.total || 0}`} pct={qs.total ? Math.round((qs.answered / qs.total) * 100) : 0} color="#2563eb" />}
                    <div style={{ fontSize: '0.72rem', color: '#9ca3af', marginTop: 8, lineHeight: 1.6 }}>
                      대화하며 개념을 익히고, 문제풀이·채점으로 진행도가 올라갑니다.
                    </div>
                  </div>
                );
              })()
            )}
          </div>
        </aside>
      )}
    </div>
    )
  );
}
