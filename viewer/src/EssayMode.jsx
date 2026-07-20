// 2차 논술 문제풀이 모드 — 자기채점 MVP
// 5 sub-view: essay_subjects → essay_chapters → essay_questions → essay_write → essay_result
//
// localStorage:
//   quiz-essay-progress      : { [qid]: { attempts: [{ts, answer, selfScore, selfTier, notes, durationMs}], lastSeen } }
//   quiz-essay-draft:{qid}   : 작성 중 답안 (auto-save 매 10초)
//
// 데이터 흐름: viewer/public/data/essay/practice/manifest.json → <chapter>.json on demand
import { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import { ArrowLeft } from 'lucide-react';
import { ParsedText } from './ParsedText';

const PROGRESS_KEY = 'quiz-essay-progress';
const DRAFT_PREFIX = 'quiz-essay-draft:';
const SELF_TIER_KEY = 'quiz-essay-tier-mode'; // 'simple' | 'detail'

// 모범답안 마크다운에서 목차(헤딩 구조)만 추출 — ⚡ 목차 스파링 대조용
// ## <문 N> / ### (물음N) / #### Ⅰ. … / **1. …** 패턴을 레벨별로 잡는다.
export function extractOutline(modelAnswer) {
  if (!modelAnswer) return [];
  const out = [];
  for (const raw of modelAnswer.split('\n')) {
    const line = raw.trim();
    let m;
    if ((m = line.match(/^(#{2,4})\s+(.+)/))) {
      out.push({ level: m[1].length - 2, text: m[2].replace(/\*\*/g, '').trim() });
    } else if ((m = line.match(/^\*\*(\d+[.)]\s*[^*]+)\*\*\s*$/))) {
      out.push({ level: 3, text: m[1].trim() });
    } else if ((m = line.match(/^\*\*([ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ][.\s][^*]+)\*\*\s*$/))) {
      out.push({ level: 2, text: m[1].trim() });
    }
  }
  return out;
}

const DIFF_META = {
  1: { label: '★☆☆☆☆', name: '입문',   color: '#16a34a', bg: '#f0fdf4' },
  2: { label: '★★☆☆☆', name: '기초',   color: '#0891b2', bg: '#ecfeff' },
  3: { label: '★★★☆☆', name: '표준',   color: '#2563eb', bg: '#eff6ff' },
  4: { label: '★★★★☆', name: '응용',   color: '#ea580c', bg: '#fff7ed' },
  5: { label: '★★★★★', name: '고난도', color: '#dc2626', bg: '#fef2f2' },
};

const TIER_OPTIONS = [
  { id: 'great', label: '잘함', subLabel: '80점+ 수준', color: '#16a34a', bg: '#f0fdf4', score: 85 },
  { id: 'ok',    label: '보통', subLabel: '60-79점',   color: '#2563eb', bg: '#eff6ff', score: 70 },
  { id: 'weak',  label: '부족', subLabel: '40-59점',   color: '#ea580c', bg: '#fff7ed', score: 50 },
  { id: 'fail',  label: '모름', subLabel: '40점 미만', color: '#dc2626', bg: '#fef2f2', score: 30 },
];

const RUBRIC_DEFAULT = [
  { id: 'point',   label: '핵심 논점 포함',   weight: 30 },
  { id: 'logic',   label: '논리 전개 명확',   weight: 25 },
  { id: 'closure', label: '결론·판단 적절',   weight: 25 },
  { id: 'source',  label: '조문/판례 인용',   weight: 20 },
];

const loadProgress = () => {
  try { return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}') || {}; }
  catch { return {}; }
};
const saveProgress = (p) => {
  try { localStorage.setItem(PROGRESS_KEY, JSON.stringify(p)); } catch { /* SSR */ }
};
const loadDraft = (qid) => {
  try { return localStorage.getItem(DRAFT_PREFIX + qid) || ''; }
  catch { return ''; }
};
const saveDraft = (qid, text) => {
  try {
    if (text) localStorage.setItem(DRAFT_PREFIX + qid, text);
    else localStorage.removeItem(DRAFT_PREFIX + qid);
  } catch { /* SSR */ }
};
const clearDraft = (qid) => {
  try { localStorage.removeItem(DRAFT_PREFIX + qid); } catch { /* SSR */ }
};

const fmtClock = (ms) => {
  const s = Math.max(0, Math.floor(ms / 1000));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const ss = s % 60;
  const pad = (n) => String(n).padStart(2, '0');
  return h > 0 ? `${h}:${pad(m)}:${pad(ss)}` : `${pad(m)}:${pad(ss)}`;
};
const fmtDate = (ts) => {
  const d = new Date(ts);
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
};

// 키워드 매칭 — 공백 무시·소문자·약어 변형 허용으로 너무 빡빡하지 않게
const normalize = (s) => (s || '').toLowerCase().replace(/\s+/g, '').replace(/[·•・∙]/g, '');
const keywordVariants = (kp) => {
  // "감칙 제14조" → ["감칙제14조", "감칙14조", "감정평가에관한규칙제14조"]
  const base = normalize(kp);
  const variants = new Set([base]);
  // "제N조" → "N조"
  variants.add(base.replace(/제(\d+)조/g, '$1조'));
  // "감칙" → "감정평가에관한규칙"
  variants.add(base.replace(/감칙/g, '감정평가에관한규칙'));
  variants.add(base.replace(/감칙/g, '감정평가규칙'));
  // "토지보상법" → 약어
  variants.add(base.replace(/토지보상법/g, '보상법'));
  return [...variants].filter(v => v.length >= 2);
};
const matchKeyword = (answerText, kp) => {
  const norm = normalize(answerText);
  return keywordVariants(kp).some(v => norm.includes(v));
};
const matchAll = (answerText, keyPoints) => {
  if (!keyPoints || !keyPoints.length) return null;
  return keyPoints.map(kp => ({ kp, matched: matchKeyword(answerText, kp) }));
};

// 2차 논술 3과목 레지스트리 — 과목별 데이터 디렉토리
const ESSAY_SUBJECTS = [
  { key: 'practice', dir: '/data/essay/practice/', title: '감정평가실무', short: '실무', icon: '🏛️', color: '#7c3aed', bg: '#f5f3ff', border: '#ddd6fe', desc: '계산·산식 위주 논술' },
  { key: 'theory', dir: '/data/essay/theory/', title: '감정평가이론', short: '이론', icon: '📚', color: '#0d9488', bg: '#f0fdfa', border: '#99f6e4', desc: '논점 서술형 논술' },
  { key: 'law', dir: '/data/essay/law/', title: '감정평가 및 보상법규', short: '보상법규', icon: '⚖️', color: '#be123c', bg: '#fff1f2', border: '#fecdd3', desc: '행정법·보상 논술' },
];

const EssayMode = ({ mode, chapter, questionId, onNavigate, setChapter, setQuestionId, fontScale, entrySubject, entryNonce, entryChapter, entrySubchapter }) => {
  const [subjKey, setSubjKey] = useState(entrySubject || 'practice'); // 현재 2차 과목
  const subj = ESSAY_SUBJECTS.find((s) => s.key === subjKey) || ESSAY_SUBJECTS[0];
  const subjDirRef = useRef(subj.dir); subjDirRef.current = subj.dir; // 현재 과목 dir(레이스 가드용)
  // 문제풀이 탭 등에서 특정 과목으로 진입할 때 동기화 (nonce가 바뀔 때마다)
  useEffect(() => {
    if (entrySubject && ESSAY_SUBJECTS.some((s) => s.key === entrySubject)) setSubjKey(entrySubject);
    // AI 학습 토픽 → 해당 단원·토픽(subchapter) 연습문제로 딥링크
    if (entryChapter) {
      setChapter(entryChapter);
      setQuestionId(null);
      ensureChapter(entryChapter);
      setSubchapterFilter(entrySubchapter || null);
      onNavigate('essay_questions');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entryNonce]);
  const [manifest, setManifest] = useState(null);
  const [manifestErr, setManifestErr] = useState(null);
  const [subjMeta, setSubjMeta] = useState({}); // {key: {subject, total, chapters}} — 과목 카드용 요약
  const [chapterCache, setChapterCache] = useState({});  // { [id]: chapterData (questions merged official+generated) }
  const [chapterErrors, setChapterErrors] = useState({}); // { [id]: errMsg } — 로드 실패 시 재시도 안내용
  const [progress, setProgressState] = useState(() => loadProgress());
  // 문제 목록 source 필터: 'all' | 'official' | 'ai-vary' | 'ai-new'
  const [sourceFilter, setSourceFilter] = useState('all');
  // 난이도 필터: null | 1 | 2 | 3 | 4 | 5
  const [diffFilter, setDiffFilter] = useState(null);
  // subchapter 필터: null (전체) | 'XX-Y' subchapter id
  const [subchapterFilter, setSubchapterFilter] = useState(null);

  // 작성 화면 상태
  const [draft, setDraft] = useState('');
  const [startedAt, setStartedAt] = useState(null);
  const [previewModelInWrite, setPreviewModelInWrite] = useState(false);
  // ⚡ 목차 스파링: 답안 전체 대신 목차만 빠르게 작성 → 모범 목차와 대조 (회독용)
  const [outlineMode, setOutlineMode] = useState(false);
  const [outlineResult, setOutlineResult] = useState(null); // 제출한 내 목차 텍스트
  const [tierMode, setTierMode] = useState(() => {
    try { return localStorage.getItem(SELF_TIER_KEY) || 'simple'; }
    catch { return 'simple'; }
  });
  // 결과 화면 상태: 방금 제출 / 채점
  const [submittedAnswer, setSubmittedAnswer] = useState('');
  const [submittedDurationMs, setSubmittedDurationMs] = useState(0);
  const [showModel, setShowModel] = useState(false);
  const [selectedTier, setSelectedTier] = useState(null);
  const [rubric, setRubric] = useState({});
  const [notes, setNotes] = useState('');

  // ─────────── manifest 로드 (현재 과목) ───────────
  useEffect(() => {
    let cancelled = false;
    setManifest(null); setManifestErr(null); setChapterCache({}); setChapterErrors({});
    (async () => {
      try {
        const r = await fetch(`${subj.dir}manifest.json`);
        if (!r.ok) throw new Error(`manifest ${r.status}`);
        const m = await r.json();
        if (!cancelled) setManifest(m);
      } catch (e) {
        if (!cancelled) setManifestErr(e.message);
      }
    })();
    return () => { cancelled = true; };
  }, [subj.dir]);

  // ─────────── 과목 카드 요약(총 문항·단원수) 미리 로드 ───────────
  useEffect(() => {
    let cancelled = false;
    Promise.all(ESSAY_SUBJECTS.map(async (s) => {
      try {
        const r = await fetch(`${s.dir}manifest.json`);
        if (!r.ok) return [s.key, null];
        const m = await r.json();
        return [s.key, { subject: m.subject, total: m.total, chapters: (m.chapters || []).length }];
      } catch { return [s.key, null]; }
    })).then((pairs) => { if (!cancelled) setSubjMeta(Object.fromEntries(pairs)); });
    return () => { cancelled = true; };
  }, []);

  // ─────────── 통계 계산 헬퍼 ───────────
  // questions 배열을 받아 sub-concept별·난이도별 학습 통계 도출
  const computeStats = (questions, progressMap) => {
    const subStats = {};   // subconcept → {total, attempted, avgScore, avgKeyword}
    const diffStats = {};  // difficulty → {total, attempted, avgScore}
    let totalAttempted = 0;
    let totalScoreSum = 0;
    let totalKeywordHitSum = 0, totalKeywordTotalSum = 0;
    for (const q of questions) {
      const sub = q.subconcept || '(미분류)';
      const diff = q.difficulty || 0;
      subStats[sub] = subStats[sub] || { total: 0, attempted: 0, scoreSum: 0, kwHit: 0, kwTotal: 0 };
      subStats[sub].total++;
      diffStats[diff] = diffStats[diff] || { total: 0, attempted: 0, scoreSum: 0 };
      diffStats[diff].total++;
      const prog = progressMap[q.id];
      if (prog && prog.attempts && prog.attempts.length) {
        const lastAttempt = prog.attempts[prog.attempts.length - 1];
        subStats[sub].attempted++;
        diffStats[diff].attempted++;
        subStats[sub].scoreSum += lastAttempt.selfScore || 0;
        diffStats[diff].scoreSum += lastAttempt.selfScore || 0;
        totalAttempted++;
        totalScoreSum += lastAttempt.selfScore || 0;
        if (lastAttempt.keywordHit) {
          subStats[sub].kwHit += lastAttempt.keywordHit.hit;
          subStats[sub].kwTotal += lastAttempt.keywordHit.total;
          totalKeywordHitSum += lastAttempt.keywordHit.hit;
          totalKeywordTotalSum += lastAttempt.keywordHit.total;
        }
      }
    }
    // 평균 계산 + 약점 정렬
    const subArr = Object.entries(subStats).map(([k, v]) => ({
      sub: k, total: v.total, attempted: v.attempted,
      avgScore: v.attempted ? Math.round(v.scoreSum / v.attempted) : null,
      kwPct: v.kwTotal ? Math.round((v.kwHit / v.kwTotal) * 100) : null,
    })).sort((a, b) => (a.avgScore ?? 999) - (b.avgScore ?? 999));
    const diffArr = Object.entries(diffStats).map(([k, v]) => ({
      diff: parseInt(k), total: v.total, attempted: v.attempted,
      avgScore: v.attempted ? Math.round(v.scoreSum / v.attempted) : null,
    })).sort((a, b) => a.diff - b.diff);
    return {
      subArr, diffArr,
      total: questions.length,
      attempted: totalAttempted,
      avgScore: totalAttempted ? Math.round(totalScoreSum / totalAttempted) : null,
      avgKeyword: totalKeywordTotalSum ? Math.round((totalKeywordHitSum / totalKeywordTotalSum) * 100) : null,
    };
  };

  // 다음 추천 문제 — 미풀이 + 가장 약한 sub-concept 우선
  const recommendNext = (questions, progressMap) => {
    const stats = computeStats(questions, progressMap);
    const weakSubs = stats.subArr.filter(s => s.avgScore != null).slice(0, 3).map(s => s.sub);
    // 미풀이 문제 중 약점 subconcept 우선
    const candidates = questions.filter(q => !progressMap[q.id]?.attempts?.length);
    candidates.sort((a, b) => {
      const aWeak = weakSubs.includes(a.subconcept);
      const bWeak = weakSubs.includes(b.subconcept);
      if (aWeak !== bWeak) return aWeak ? -1 : 1;
      return (a.difficulty || 99) - (b.difficulty || 99);  // 쉬운 것부터
    });
    return candidates.slice(0, 3);
  };

  // 없는 파일이면 dev 서버가 index.html(200)을 폴백으로 주므로, JSON 파싱 실패는 null 처리
  const safeJson = async (url) => {
    try {
      const r = await fetch(url);
      if (!r.ok) return null;
      return await r.json();          // HTML(<!doctype)이면 파싱 예외 → null
    } catch { return null; }
  };

  // ─────────── chapter 데이터 lazy fetch (official + generated 병합) ───────────
  const ensureChapter = useCallback(async (id) => {
    if (chapterCache[id]) return chapterCache[id];
    const dir = subj.dir; // 호출 시점 과목 — 도착 시 과목이 바뀌었으면 캐시 쓰지 않음
    try {
      const [official, generated] = await Promise.all([
        safeJson(`${dir}${id}.json`),
        safeJson(`${dir}${id}-generated.json`),
      ]);
      if (!official) throw new Error(`chapter ${id} not found`);
      // 과목이 바뀐 뒤 옛 fetch 가 도착하면, 리셋된 새 과목 캐시에 같은 id 로 덮어써
      // 다른 과목의 논술 문제가 노출된다 → 도착 시점 과목이 다르면 폐기.
      if (dir !== subjDirRef.current) return null;
      const genQ = generated?.questions || [];
      const merged = {
        ...official,
        questions: [...official.questions, ...genQ],
        officialCount: official.questions.length,
        generatedCount: genQ.length,
      };
      setChapterCache(prev => ({ ...prev, [id]: merged }));
      setChapterErrors(prev => { if (!prev[id]) return prev; const n = { ...prev }; delete n[id]; return n; });
      return merged;
    } catch (e) {
      console.error('essay chapter fetch failed', e);
      setChapterErrors(prev => ({ ...prev, [id]: e.message || '로드 실패' }));
      return null;
    }
  }, [chapterCache, subj.dir]);

  const retryChapter = useCallback((id) => {
    setChapterErrors(prev => { const n = { ...prev }; delete n[id]; return n; });
    ensureChapter(id);
  }, [ensureChapter]);

  useEffect(() => {
    // 캐시 없고 아직 실패 기록도 없을 때만 1회 시도 (실패 시 무한 재시도 방지)
    if (chapter && !chapterCache[chapter] && !chapterErrors[chapter]) ensureChapter(chapter);
  }, [chapter, chapterCache, chapterErrors, ensureChapter]);

  // ─────────── 작성 화면 진입 시 draft 로드 + 타이머 시작 ───────────
  useEffect(() => {
    if (mode !== 'essay_write' || !questionId) return;
    setDraft(loadDraft(questionId));
    setStartedAt(Date.now());
    setShowModel(false);
    setSelectedTier(null);
    setRubric({});
    setNotes('');
    setPreviewModelInWrite(false);
    setOutlineResult(null);  // 스파링 대조 패널은 문제별 리셋(모드 토글은 유지 — 연속 회독용)
  }, [mode, questionId]);

  // ─────────── auto-save 매 10초 ───────────
  // draft 를 deps 에 넣으면 매 키입력마다 clearInterval→새 10초 카운트가 리셋되어,
  // 쉼 없이 타이핑하는 동안엔 자동저장이 영영 안 뜬다(크래시/새로고침 시 작성분 유실).
  // draft 는 ref 로 읽고, 인터벌은 문항이 바뀔 때만 재설정한다.
  const draftRef = useRef(draft); draftRef.current = draft;
  useEffect(() => {
    if (mode !== 'essay_write' || !questionId) return undefined;
    const t = setInterval(() => saveDraft(questionId, draftRef.current), 10000);
    return () => clearInterval(t);
  }, [mode, questionId]);

  // ─────────── 작성 중 새로고침·탭 닫기 경고 (최대 10초 분량 유실 방지) ───────────
  useEffect(() => {
    if (mode !== 'essay_write' || draft.trim().length === 0) return undefined;
    const handler = (e) => { e.preventDefault(); e.returnValue = ''; };
    window.addEventListener('beforeunload', handler);
    return () => window.removeEventListener('beforeunload', handler);
  }, [mode, draft]);

  // ─────────── 현재 question 찾기 헬퍼 ───────────
  const currentQuestion = useMemo(() => {
    if (!questionId || !chapter) return null;
    const cd = chapterCache[chapter];
    if (!cd) return null;
    return cd.questions.find(q => q.id === questionId) || null;
  }, [chapter, questionId, chapterCache]);

  // ─────────── 액션: 제출 ───────────
  const onSubmit = useCallback(() => {
    if (!currentQuestion) return;
    if (outlineMode) { setOutlineResult(draft); return; }  // ⚡ 스파링: 화면 내 목차 대조
    const dur = startedAt ? Date.now() - startedAt : 0;
    setSubmittedAnswer(draft);
    setSubmittedDurationMs(dur);
    onNavigate('essay_result');
  }, [currentQuestion, draft, startedAt, onNavigate, outlineMode]);

  // ─────────── 액션: 자기 채점 저장 ───────────
  const onSaveGrade = useCallback(() => {
    if (!currentQuestion) return;
    const tier = TIER_OPTIONS.find(t => t.id === selectedTier);
    if (!tier && tierMode === 'simple') return;
    let selfScore;
    if (tierMode === 'simple') {
      selfScore = tier.score;
    } else {
      // detail: 가중 평균
      const total = RUBRIC_DEFAULT.reduce((s, r) => s + r.weight, 0);
      const got = RUBRIC_DEFAULT.reduce((s, r) => s + (rubric[r.id] ? r.weight : 0), 0);
      selfScore = Math.round((got / total) * 100);
    }
    // 키워드 적중률 자동 계산 (attempts 누적 통계용)
    let keywordHit = null;
    if (currentQuestion.keyPoints && currentQuestion.keyPoints.length) {
      const matches = matchAll(submittedAnswer, currentQuestion.keyPoints);
      keywordHit = {
        hit: matches.filter(m => m.matched).length,
        total: matches.length,
        missed: matches.filter(m => !m.matched).map(m => m.kp),
      };
    }
    const attempt = {
      ts: Date.now(),
      answer: submittedAnswer,
      selfScore,
      selfTier: tier?.id || null,
      rubric: tierMode === 'detail' ? { ...rubric } : null,
      notes: notes.trim() || null,
      durationMs: submittedDurationMs,
      keywordHit,
    };
    setProgressState(prev => {
      const cur = prev[currentQuestion.id] || { attempts: [] };
      const next = {
        ...prev,
        [currentQuestion.id]: {
          ...cur,
          attempts: [...(cur.attempts || []), attempt],
          lastSeen: Date.now(),
        },
      };
      saveProgress(next);
      return next;
    });
    clearDraft(currentQuestion.id);
    setShowModel(false);
    setSelectedTier(null);
    setRubric({});
    setNotes('');
    // 채점 후 문제 목록으로
    onNavigate('essay_questions');
  }, [currentQuestion, selectedTier, tierMode, rubric, submittedAnswer, submittedDurationMs, notes, onNavigate]);

  // ─────────── 공통 컨테이너 ───────────
  const shell = (content) => (
    <div className="app-container" style={{ '--q-fs': fontScale }}>{content}</div>
  );
  const header = (title, backLabel, backTo) => (
    <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
      <button className="back-btn" onClick={() => onNavigate(backTo)}>
        <ArrowLeft size={24} style={{ marginRight: 8 }} />
        <span style={{ fontSize: '1rem', fontWeight: 600 }}>{backLabel}</span>
      </button>
    </header>
  );

  // ═══════════════════ subjects (3과목 선택 — manifest 가드보다 먼저) ═══════════════════
  if (mode === 'essay_subjects') {
    return shell(<>
      {header('2차 준비', '홈', 'home')}
      <div className="screen-head"><h1 className="screen-title">📝 2차 논술</h1>
        <p style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: 4 }}>
          과목을 골라 논술 기출을 풀고, 모범답안·AI 채점으로 점검하세요
        </p>
      </div>
      <main className="main-content" style={{ marginTop: 16, display: 'flex', flexDirection: 'column', gap: 12 }}>
        {ESSAY_SUBJECTS.map((s) => {
          const meta = subjMeta[s.key];
          const ready = meta && meta.total > 0;
          return (
            <button key={s.key}
              onClick={() => { if (s.key !== subjKey) setSubjKey(s.key); setChapter(null); setQuestionId(null); onNavigate('essay_chapters'); }}
              style={{ width: '100%', textAlign: 'left', padding: '18px', borderRadius: 14,
                border: `1px solid ${s.border}`, background: s.bg, cursor: 'pointer' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <span style={{ fontSize: '1.6rem' }}>{s.icon}</span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: 800, fontSize: '1.05rem', color: '#111827' }}>{s.title}</div>
                  <div style={{ fontSize: '0.78rem', color: '#6b7280', marginTop: 2 }}>{s.desc}</div>
                </div>
                <span style={{ fontSize: '0.82rem', fontWeight: 800, color: s.color }}>시작 →</span>
              </div>
              <div style={{ fontSize: '0.8rem', color: s.color, marginTop: 8, fontWeight: 700 }}>
                {meta == null ? '· 불러오는 중…' : (ready ? `${meta.chapters}개 단원 · ${meta.total}문항` : '· 준비 중')}
              </div>
            </button>
          );
        })}
        <div style={{ marginTop: 4, padding: 12, borderRadius: 10,
          background: '#fafafa', border: '1px solid #e5e7eb', fontSize: '0.76rem', color: '#6b7280' }}>
          실무는 기출 11~36회 예시답안 포함. 이론·법규는 기출 논점 기반으로 단계적 확장 중입니다.
        </div>
      </main>
    </>);
  }

  if (manifestErr) {
    return shell(<>
      {header('2차 준비', '과목', 'essay_subjects')}
      <div style={{ padding: 24, color: '#dc2626' }}>
        {subj.title} 데이터 로드 실패: {manifestErr}
        <div style={{ marginTop: 8, fontSize: '0.85rem', color: '#9ca3af' }}>
          이 과목 데이터가 아직 없거나 누락됐을 수 있어요. 다른 과목을 선택해 주세요.
        </div>
        <button onClick={() => onNavigate('essay_subjects')}
          style={{ marginTop: 14, padding: '10px 18px', borderRadius: 8, fontWeight: 700, border: 'none', background: '#2563eb', color: '#fff', cursor: 'pointer', minHeight: 44 }}>
          ← 과목 선택
        </button>
      </div>
    </>);
  }
  if (!manifest) {
    return shell(<div style={{ padding: 24, color: '#9ca3af' }}>데이터 불러오는 중…</div>);
  }

  // ═══════════════════ chapters ═══════════════════
  // ═══════════════════ 🃏 인출카드 ═══════════════════
  if (mode === 'essay_cards') {
    if (!manifest) return shell(<div style={{ padding: 24, color: '#9ca3af' }}>로딩 중…</div>);
    return <EssayCards subjDir={subj.dir} manifest={manifest}
      onBack={() => onNavigate('essay_chapters')} />;
  }

  if (mode === 'essay_chapters') {
    const overallAttempts = manifest.chapters.reduce((sum, c) => {
      // 진척 카운트 (그 단원의 question 중 attempts 있는 것)
      const cd = chapterCache[c.id];
      if (!cd) return sum;
      return sum + cd.questions.filter(q => progress[q.id]?.attempts?.length).length;
    }, 0);
    return shell(<>
      {header('과목 선택', '과목', 'essay_subjects')}
      <div className="screen-head"><h1 className="screen-title">{manifest.subject}</h1>
        <p style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: 4 }}>
          단원 선택 · 진행 {overallAttempts}/{manifest.total}
        </p>
        <button onClick={() => onNavigate('essay_cards')}
          style={{ marginTop: 10, width: '100%', padding: '11px 14px', borderRadius: 12,
            border: '1.5px solid #ddd6fe', background: '#f5f3ff', cursor: 'pointer',
            display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontWeight: 800, fontSize: '0.9rem', color: '#5b21b6' }}>
            🃏 논점 인출카드
          </span>
          <span style={{ fontSize: '0.72rem', color: '#7c3aed', fontWeight: 600 }}>
            기출·GS 논점·조문 암기 →
          </span>
        </button>
      </div>
      <main className="main-content" style={{ marginTop: 16 }}>
        {/* 1차 문제풀이와 동일한 browse-list 드릴다운 UI */}
        <div className="browse-list">
          {manifest.chapters.filter(c => c.id !== 'cleanup' && ((c.count || 0) > 0 || c.aiUnit)).map(c => {
            const cd = chapterCache[c.id];
            const done = cd ? cd.questions.filter(q => progress[q.id]?.attempts?.length).length : 0;
            const pct = c.count ? Math.round((done / c.count) * 100) : 0;
            const subMeta = [
              c.count > 0 && c.withAnswer > 0 ? `답안 ${Math.min(c.withAnswer, c.count)}/${c.count}` : '',
              c.sessionCount ? `모의 ${c.sessionCount}회분` : '',
              c.rounds?.length ? (c.rounds.length > 8
                ? `${c.rounds.length}개 회차 (${c.rounds[0]}~${c.rounds[c.rounds.length - 1]}회)`
                : `회차 ${c.rounds.join(', ')}회`) : '',
            ].filter(Boolean).join(' · ');
            return (
              <button key={c.id} className="browse-row"
                onClick={() => {
                  setChapter(c.id); setQuestionId(null); setSubchapterFilter(null); ensureChapter(c.id);
                  // 소단원(subchapter)이 2개 이상이면 소단원 목록으로 한 단계 더 — 1차 장→절→관,
                  // AI학습 unit→topic과 동일한 계층. GS·기출 등 소단원 없는 단원은 바로 문항으로.
                  const hasSubs = (c.subchapters || []).length >= 2;
                  onNavigate(hasSubs ? 'essay_subchapters' : 'essay_questions');
                }}>
                <div className="browse-row__main">
                  <div className="browse-row__title">
                    <span className="browse-row__prefix">단원 {c.aiCode || c.id}</span>
                    {c.title}
                  </div>
                  {done > 0 && <div className="browse-row__bar"><div style={{ width: `${Math.max(2, pct)}%` }} /></div>}
                  {subMeta && <div style={{ fontSize: '0.72rem', color: '#9ca3af', marginTop: 5 }}>{subMeta}</div>}
                </div>
                <div className="browse-row__meta">
                  {done > 0 && <span className="browse-row__pct">{pct}%</span>}
                  <span className="browse-row__count">{c.count > 0 ? `${c.count}문항` : '준비 중'}</span>
                  <span className="browse-row__chev">›</span>
                </div>
              </button>
            );
          })}
        </div>
      </main>
    </>);
  }

  // ═══════════════════ subchapters (소단원 드릴 — 1차 절→관·AI학습 unit→topic과 동일 계층) ═══════════════════
  if (mode === 'essay_subchapters') {
    const cd = chapter ? chapterCache[chapter] : null;
    const meta = chapter ? manifest.chapters.find(c => c.id === chapter) : null;
    if (!cd) return shell(
      chapterErrors[chapter]
        ? <div style={{ padding: 24, textAlign: 'center' }}>
            <div style={{ color: '#dc2626', fontWeight: 600, marginBottom: 12 }}>⚠️ 단원 자료를 불러오지 못했어요</div>
            <button onClick={() => retryChapter(chapter)}
              style={{ padding: '10px 18px', borderRadius: 8, fontWeight: 700, border: 'none', background: '#2563eb', color: '#fff', cursor: 'pointer', minHeight: 44 }}>↻ 다시 시도</button>
          </div>
        : <div style={{ padding: 16 }}><div className="skeleton skeleton-row" /><div className="skeleton skeleton-row" /><div className="skeleton skeleton-row" /></div>
    );
    const subs = meta?.subchapters || [];
    const subCount = {}; const subDone = {};
    cd.questions.forEach(q => {
      if (!q.subchapter) return;
      subCount[q.subchapter] = (subCount[q.subchapter] || 0) + 1;
      if (progress[q.id]?.attempts?.length) subDone[q.subchapter] = (subDone[q.subchapter] || 0) + 1;
    });
    const totalQ = cd.questions.length;
    const totalDone = cd.questions.filter(q => progress[q.id]?.attempts?.length).length;
    const goQuestions = (scId) => { setSubchapterFilter(scId); onNavigate('essay_questions'); };
    return shell(<>
      {header(`단원 ${meta?.aiCode || chapter}`, '단원 목록', 'essay_chapters')}
      <div className="screen-head"><h1 className="screen-title">{meta?.title || chapter}</h1>
        <p style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: 4 }}>소단원 선택 · 진행 {totalDone}/{totalQ}</p>
      </div>
      <main className="main-content" style={{ marginTop: 16 }}>
        <div className="browse-list">
          {/* 전체 풀기 — 1차 '장 전체 풀기' 행과 동일 */}
          <button className="browse-row browse-row--all" onClick={() => goQuestions(null)}>
            <div className="browse-row__main">
              <div className="browse-row__title">
                <span className="browse-row__prefix">전체</span>{meta?.title} 전체 풀기
              </div>
            </div>
            <div className="browse-row__meta">
              <span className="browse-row__count">{totalQ}문항</span>
              <span className="browse-row__chev">›</span>
            </div>
          </button>
          {/* 소단원 행 — 문항 있는 것만 (AI학습 topic 목록과 일치) */}
          {subs.filter(sc => subCount[sc.id] > 0).map((sc, i) => {
            const cnt = subCount[sc.id]; const done = subDone[sc.id] || 0;
            const pct = cnt ? Math.round((done / cnt) * 100) : 0;
            return (
              <button key={sc.id} className="browse-row" onClick={() => goQuestions(sc.id)}>
                <div className="browse-row__main">
                  <div className="browse-row__title">
                    <span className="browse-row__prefix">{i + 1}</span>{sc.title}
                  </div>
                  {done > 0 && <div className="browse-row__bar"><div style={{ width: `${Math.max(2, pct)}%` }} /></div>}
                </div>
                <div className="browse-row__meta">
                  {done > 0 && <span className="browse-row__pct">{pct}%</span>}
                  <span className="browse-row__count">{cnt}문항</span>
                  <span className="browse-row__chev">›</span>
                </div>
              </button>
            );
          })}
        </div>
      </main>
    </>);
  }

  // ═══════════════════ questions ═══════════════════
  if (mode === 'essay_questions') {
    const cd = chapter ? chapterCache[chapter] : null;
    const meta = chapter ? manifest.chapters.find(c => c.id === chapter) : null;
    if (!cd) return shell(
      chapterErrors[chapter]
        ? <div style={{ padding: 24, textAlign: 'center' }}>
            <div style={{ color: '#dc2626', fontWeight: 600, marginBottom: 12 }}>⚠️ 단원 자료를 불러오지 못했어요</div>
            <div style={{ color: '#6b7280', fontSize: '0.85rem', marginBottom: 16 }}>{chapterErrors[chapter]}</div>
            <button onClick={() => retryChapter(chapter)}
              style={{ padding: '10px 18px', borderRadius: 8, fontWeight: 700, border: 'none',
                background: '#2563eb', color: '#fff', cursor: 'pointer', minHeight: 44 }}>↻ 다시 시도</button>
          </div>
        : <div style={{ padding: 24, color: '#6b7280' }}>단원 데이터 불러오는 중…</div>
    );

    // source별 카운트 — 기출(official/past) / GS 모의(gs) / 연습문제(practice-set) / AI 명확히 구분
    const isOfficial = (q) => q.source === 'official' || q.source === 'past' || q.source == null;
    const isGS = (q) => q.source === 'gs';
    const isPractice = (q) => q.source === 'practice-set';
    const isAIVary = (q) => q.source === 'ai-generated' && q.genMode === 'vary';
    const isAINew = (q) => q.source === 'ai-generated' && q.genMode === 'new';
    // 소스 칩 카운트도 소단원 진입 시 그 소단원 기준 (전체 풀기면 단원 전체)
    const countBase = subchapterFilter ? cd.questions.filter(q => q.subchapter === subchapterFilter) : cd.questions;
    const counts = {
      all: countBase.length,
      official: countBase.filter(isOfficial).length,
      gs: countBase.filter(isGS).length,
      'practice-set': countBase.filter(isPractice).length,
      'ai-vary': countBase.filter(isAIVary).length,
      'ai-new': countBase.filter(isAINew).length,
    };
    const filterChips = [
      { id: 'all',          label: '전체',          count: counts.all },
      { id: 'official',     label: '📘 실문제(기출)', count: counts.official },
      { id: 'gs',           label: '📗 GS 모의(예시답안)', count: counts.gs },
      { id: 'practice-set', label: '📝 연습문제',    count: counts['practice-set'] },
      { id: 'ai-vary',      label: '🤖 AI 변형',    count: counts['ai-vary'] },
      { id: 'ai-new',       label: '🤖 AI 신규',    count: counts['ai-new'] },
    ].filter(c => c.count > 0);

    // 난이도별 카운트
    const diffCounts = {};
    [1,2,3,4,5].forEach(d => { diffCounts[d] = cd.questions.filter(q => q.difficulty === d).length; });
    const hasDiff = [1,2,3,4,5].some(d => diffCounts[d] > 0);

    // subchapter 메타 + 카운트
    const subchapterList = meta?.subchapters || [];
    const subchapterCounts = {};
    subchapterList.forEach(sc => {
      subchapterCounts[sc.id] = cd.questions.filter(q => q.subchapter === sc.id).length;
    });

    const visible = cd.questions.filter(q => {
      if (sourceFilter === 'official' && !isOfficial(q)) return false;
      if (sourceFilter === 'gs' && !isGS(q)) return false;
      if (sourceFilter === 'practice-set' && !isPractice(q)) return false;
      if (sourceFilter === 'ai-vary' && !isAIVary(q)) return false;
      if (sourceFilter === 'ai-new' && !isAINew(q)) return false;
      if (diffFilter !== null && q.difficulty !== diffFilter) return false;
      if (subchapterFilter !== null && q.subchapter !== subchapterFilter) return false;
      return true;
    });

    // practice-set 문제의 subchapter별 순번 (전체 데이터 기준, 필터 무관)
    const practiceOrder = {};
    {
      const counter = {};
      cd.questions
        .filter(q => q.source === 'practice-set' && q.subchapter)
        .forEach(q => {
          counter[q.subchapter] = (counter[q.subchapter] || 0) + 1;
          const sc = subchapterList.find(s => s.id === q.subchapter);
          practiceOrder[q.id] = { title: sc?.title || '연습', no: counter[q.subchapter] };
        });
    }

    // 학습 통계 + 추천
    const stats = computeStats(cd.questions, progress);
    const recommendations = recommendNext(cd.questions, progress);

    // 뒤로가기: 소단원 경유로 들어왔으면 소단원 목록으로, 아니면(GS 등) 단원 목록으로
    const hasSubs = (meta?.subchapters || []).length >= 2;
    return shell(<>
      {header(
        hasSubs && subchapterFilter ? subchapterList.find(s => s.id === subchapterFilter)?.title || meta?.title : `단원 ${meta?.aiCode || chapter}`,
        hasSubs ? '소단원' : '단원 목록',
        hasSubs ? 'essay_subchapters' : 'essay_chapters')}
      {(() => {
        // 소단원 진입 시 제목·문항수·진행을 그 소단원 기준으로 (전체 풀기면 단원 기준)
        const scTitle = subchapterFilter ? subchapterList.find(s => s.id === subchapterFilter)?.title : null;
        const scope = subchapterFilter ? cd.questions.filter(q => q.subchapter === subchapterFilter) : cd.questions;
        const totalQ = scope.length;
        const doneQ = scope.filter(q => progress[q.id]?.attempts?.length).length;
        const pct = totalQ ? Math.round((doneQ / totalQ) * 100) : 0;
        return (
          <div className="screen-head">
            <h1 className="screen-title">{scTitle || meta?.title || chapter} ({totalQ}문항)</h1>
            {scTitle && <p style={{ fontSize: '0.78rem', color: '#9ca3af', margin: '2px 0 0' }}>{meta?.title}</p>}
            <div style={{ height: 6, background: '#eef2f7', borderRadius: 999, overflow: 'hidden', margin: '10px 0 8px' }}>
              <div style={{ width: `${Math.max(2, pct)}%`, height: '100%', background: '#2563eb', borderRadius: 999 }} />
            </div>
            <p style={{ fontSize: '0.85rem', color: '#6b7280', margin: 0 }}>
              푼 문제 <b style={{ color: '#1d4ed8' }}>{doneQ}/{totalQ}</b>
              {!subchapterFilter && stats.attempted > 0 && <> · 평균 <b style={{ color: '#16a34a' }}>{stats.avgScore}점</b></>}
              {!subchapterFilter && stats.avgKeyword != null && <> · 키워드 <b style={{ color: '#7c3aed' }}>{stats.avgKeyword}%</b></>}
            </p>
          </div>
        );
      })()}
      <main className="main-content" style={{ marginTop: 16 }}>
        {/* 추천 학습 카드 — 단원 전체 풀기일 때만 (소단원 드릴 진입 시엔 중복이라 숨김) */}
        {recommendations.length > 0 && subchapterFilter === null && (
          <section style={{ background: '#eff6ff', borderRadius: 12, padding: 14,
            border: '1px solid #bfdbfe', marginBottom: 14 }}>
            <div style={{ fontWeight: 800, fontSize: '0.9rem', color: '#1d4ed8',
              marginBottom: 8 }}>
              💡 다음 추천 학습
              {stats.attempted > 0 && stats.subArr.filter(s => s.avgScore != null).length > 0 && (
                <span style={{ marginLeft: 6, fontSize: '0.72rem', fontWeight: 600,
                  color: '#6b7280' }}>
                  (약점 영역 우선)
                </span>
              )}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {recommendations.map(q => (
                <button key={q.id}
                  onClick={() => { setQuestionId(q.id); onNavigate('essay_write'); }}
                  style={{ background: '#fff', border: '1px solid #bfdbfe',
                    borderRadius: 8, padding: '8px 12px', cursor: 'pointer',
                    textAlign: 'left', display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span style={{ fontSize: '0.78rem', fontWeight: 700,
                    color: '#1d4ed8', minWidth: 30 }}>
                    {q.difficulty ? '★'.repeat(q.difficulty) : ''}
                  </span>
                  <span style={{ flex: 1, fontSize: '0.82rem', color: '#374151',
                    overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {q.subconcept || q.topic ||
                      (q.gsRound
                        ? `GS ${q.gsRound} ${q.questionNum}번`
                        : q.round
                          ? `${q.round}회 ${q.questionNum}번`
                          : '문제')}
                  </span>
                  <span style={{ fontSize: '0.72rem', color: '#9ca3af' }}>
                    {q.points}점 →
                  </span>
                </button>
              ))}
            </div>
            {stats.subArr.filter(s => s.avgScore != null && s.avgScore < 60).length > 0 && (
              <div style={{ marginTop: 10, fontSize: '0.72rem', color: '#6b7280' }}>
                ⚠ 약점: {stats.subArr.filter(s => s.avgScore != null && s.avgScore < 60)
                  .slice(0, 2).map(s => `${s.sub} (${s.avgScore}점)`).join(', ')}
              </div>
            )}
          </section>
        )}

        {/* source 필터 chip */}
        {filterChips.length > 1 && (
          <div style={{ display: 'flex', gap: 6, marginBottom: 8, overflowX: 'auto',
            WebkitOverflowScrolling: 'touch' }}>
            {filterChips.map(c => {
              const on = sourceFilter === c.id;
              return (
                <button key={c.id} onClick={() => setSourceFilter(c.id)}
                  style={{ flex: '0 0 auto', padding: '6px 11px', whiteSpace: 'nowrap',
                    border: on ? '1.5px solid #2563eb' : '1px solid #d1d5db',
                    background: on ? '#eff6ff' : '#fff',
                    color: on ? '#1d4ed8' : '#374151',
                    borderRadius: 999, fontWeight: on ? 800 : 600,
                    fontSize: '0.78rem', cursor: 'pointer' }}>
                  {c.label} {c.count}
                </button>
              );
            })}
          </div>
        )}
        {/* 난이도 필터 chip */}
        {hasDiff && (
          <div style={{ display: 'flex', gap: 6, marginBottom: 14, overflowX: 'auto',
            WebkitOverflowScrolling: 'touch' }}>
            <button onClick={() => setDiffFilter(null)}
              style={{ flex: '0 0 auto', padding: '5px 10px', whiteSpace: 'nowrap',
                border: diffFilter === null ? '1.5px solid #6b7280' : '1px solid #d1d5db',
                background: diffFilter === null ? '#f3f4f6' : '#fff',
                color: diffFilter === null ? '#111827' : '#6b7280',
                borderRadius: 999, fontWeight: diffFilter === null ? 800 : 600,
                fontSize: '0.75rem', cursor: 'pointer' }}>
              난이도 전체
            </button>
            {[1,2,3,4,5].filter(d => diffCounts[d] > 0).map(d => {
              const on = diffFilter === d;
              const m = DIFF_META[d];
              return (
                <button key={d} onClick={() => setDiffFilter(on ? null : d)}
                  style={{ flex: '0 0 auto', padding: '5px 10px', whiteSpace: 'nowrap',
                    border: on ? `1.5px solid ${m.color}` : '1px solid #d1d5db',
                    background: on ? m.bg : '#fff',
                    color: on ? m.color : '#6b7280',
                    borderRadius: 999, fontWeight: on ? 800 : 600,
                    fontSize: '0.75rem', cursor: 'pointer' }}>
                  {m.label} {m.name} {diffCounts[d]}
                </button>
              );
            })}
          </div>
        )}
        {/* subchapter 필터 chip — '전체 풀기'로 들어왔을 때만. 소단원 드릴 진입 시엔
            이미 그 소단원이므로 칩 숨김(중복·'전체'처럼 보임 방지) — 다른 소단원은 뒤로가서 선택 */}
        {subchapterList.length > 1 && subchapterFilter === null && (
          <div style={{ display: 'flex', gap: 6, marginBottom: 14, overflowX: 'auto',
            WebkitOverflowScrolling: 'touch' }}>
            <button onClick={() => setSubchapterFilter(null)}
              style={{ flex: '0 0 auto', padding: '5px 10px', whiteSpace: 'nowrap',
                border: subchapterFilter === null ? '1.5px solid #0891b2' : '1px solid #d1d5db',
                background: subchapterFilter === null ? '#ecfeff' : '#fff',
                color: subchapterFilter === null ? '#0e7490' : '#6b7280',
                borderRadius: 999, fontWeight: subchapterFilter === null ? 800 : 600,
                fontSize: '0.74rem', cursor: 'pointer' }}>
              📚 전체 소단원
            </button>
            {subchapterList.filter(sc => subchapterCounts[sc.id] > 0).map(sc => {
              const on = subchapterFilter === sc.id;
              return (
                <button key={sc.id} onClick={() => setSubchapterFilter(on ? null : sc.id)}
                  style={{ flex: '0 0 auto', padding: '5px 10px', whiteSpace: 'nowrap',
                    border: on ? '1.5px solid #0891b2' : '1px solid #d1d5db',
                    background: on ? '#ecfeff' : '#fff',
                    color: on ? '#0e7490' : '#374151',
                    borderRadius: 999, fontWeight: on ? 800 : 600,
                    fontSize: '0.74rem', cursor: 'pointer' }}>
                  {sc.title} {subchapterCounts[sc.id]}
                </button>
              );
            })}
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {visible.map(q => {
            const prog = progress[q.id];
            const attemptCount = prog?.attempts?.length || 0;
            const lastScore = attemptCount ? prog.attempts[attemptCount - 1].selfScore : null;
            const hasAnswer = !!q.modelAnswer;
            const isAI = q.source === 'ai-generated';
            const isPracticeSet = q.source === 'practice-set';
            const practiceMeta = isPracticeSet ? practiceOrder[q.id] : null;
            // 1차 문항 카드와 동일하게 흰 카드 통일 — 출처 구분은 상단 배지로
            const cardBorder = '1px solid #eef0f2';
            const cardBg = '#fff';
            // 출처 배지 — 1차 카드 헤더의 출처 표기와 동일 톤
            const src = isAI
              ? { label: `🤖 AI ${q.genMode === 'new' ? '신규' : '변형'}`, fg: '#7c3aed', bg: '#f3f0ff' }
              : isPracticeSet
                ? { label: practiceMeta ? `📝 연습 ${practiceMeta.no}` : '📝 연습', fg: '#65a30d', bg: '#f7fee7' }
                : q.gsRound
                  ? { label: `GS ${q.gsRound} ${q.questionNum}번`, fg: '#0891b2', bg: '#ecfeff' }
                  : { label: `${q.round}회 ${q.questionNum}번`, fg: '#1d4ed8', bg: '#eff6ff' };
            return (
              <button key={q.id}
                onClick={() => { setQuestionId(q.id); onNavigate('essay_write'); }}
                style={{ background: cardBg, borderRadius: 12, padding: '18px 20px',
                  border: cardBorder, textAlign: 'left', cursor: 'pointer',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.05)', display: 'block', width: '100%' }}>
                {/* 상단: Q + 출처·난이도 배지 (좌) · 배점 (우) — 1차 문항 카드와 동일 구조 */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                    <span style={{ fontWeight: 700, fontSize: '1.05rem', color: '#2563eb' }}>Q.</span>
                    <span style={{ fontSize: '0.75rem', fontWeight: 700, padding: '2px 9px',
                      borderRadius: 999, color: src.fg, background: src.bg }}>{src.label}</span>
                    {q.difficulty && DIFF_META[q.difficulty] && (
                      <span style={{ fontSize: '0.75rem', fontWeight: 700, padding: '2px 8px',
                        borderRadius: 999, color: DIFF_META[q.difficulty].color, background: DIFF_META[q.difficulty].bg }}>
                        {DIFF_META[q.difficulty].label} {DIFF_META[q.difficulty].name}
                      </span>
                    )}
                  </span>
                  {q.points && (
                    <span style={{ color: '#1d4ed8', fontWeight: 800, fontSize: '0.95rem', flexShrink: 0 }}>{q.points}점</span>
                  )}
                </div>
                {/* 논점(topic) — 있으면 굵게 */}
                {q.topic && !isPracticeSet && (
                  <div style={{ fontSize: '0.92rem', fontWeight: 700, color: '#111827', lineHeight: 1.45,
                    marginBottom: 4, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {q.topic}
                  </div>
                )}
                {/* 문제 본문 */}
                <div style={{ fontSize: '0.95rem', color: '#1f2937', lineHeight: 1.6,
                  display: '-webkit-box', WebkitLineClamp: q.topic && !isPracticeSet ? 2 : 3,
                  WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                  {q.body.slice(0, 260).replace(/\n/g, ' ').replace(/\*\*/g, '').replace(/^#+\s*/gm, '').replace(/`/g, '')}
                </div>
                {q.subconcept && (
                  <div style={{ marginTop: 8 }}>
                    <span style={{ color: '#92400e', background: '#fffbeb', fontSize: '0.72rem',
                      padding: '2px 8px', borderRadius: 999, fontWeight: 700,
                      display: 'inline-block', maxWidth: '100%', overflow: 'hidden',
                      textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>📚 {q.subconcept}</span>
                  </div>
                )}
                {/* 하단: 풀이 기록 (좌) · 답안 작성 CTA (우) */}
                <div style={{ marginTop: 14, paddingTop: 12, borderTop: '1px solid #f1f3f5',
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.78rem' }}>
                  <span style={{ color: attemptCount > 0 ? '#16a34a' : '#9ca3af', fontWeight: attemptCount > 0 ? 700 : 500 }}>
                    {attemptCount > 0
                      ? `✓ ${attemptCount}회 풀이 · 마지막 ${lastScore}점`
                      : (hasAnswer ? '예시답안 있음' : '답안 없음')}
                  </span>
                  <span style={{ color: '#2563eb', fontWeight: 700 }}>답안 작성 →</span>
                </div>
              </button>
            );
          })}
          {visible.length === 0 && (
            <div style={{ padding: 30, textAlign: 'center', color: '#9ca3af',
              background: '#fafafa', borderRadius: 12, fontSize: '0.88rem' }}>
              해당 source 문제가 없어요.
            </div>
          )}
        </div>
      </main>
    </>);
  }

  // ═══════════════════ write ═══════════════════
  if (mode === 'essay_write') {
    if (!currentQuestion) return shell(<div style={{ padding: 24, color: '#9ca3af' }}>문항 불러오는 중…</div>);
    const elapsed = startedAt ? Date.now() - startedAt : 0;
    return shell(<>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb',
        display: 'flex', justifyContent: 'space-between' }}>
        <button className="back-btn" onClick={() => { saveDraft(currentQuestion.id, draft); onNavigate('essay_questions'); }}>
          <ArrowLeft size={24} style={{ marginRight: 8 }} />
          <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>저장 후 종료</span>
        </button>
        <div style={{ display: 'flex', alignItems: 'center', padding: '6px 12px',
          fontSize: '0.85rem', fontWeight: 700,
          color: currentQuestion.points && elapsed > currentQuestion.points * 60000 ? '#dc2626' : '#374151' }}>
          ⏱ {fmtClock(elapsed)}
          {currentQuestion.points ? (
            <span style={{ marginLeft: 6, fontSize: '0.72rem', fontWeight: 600, color: '#9ca3af' }}>
              / 권장 {currentQuestion.points}분
            </span>
          ) : null}
        </div>
      </header>

      <main className="main-content" style={{ marginTop: 12 }}>
        <div style={{ background: '#fff', borderRadius: 12, padding: 18,
          boxShadow: '0 2px 8px rgba(0,0,0,0.05)', marginBottom: 14 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 12 }}>
            <span style={{ fontWeight: 700, fontSize: '0.85rem', color: '#9ca3af' }}>
              {currentQuestion.source === 'ai-generated' ? (
                <span style={{ color: '#7c3aed' }}>
                  🤖 AI {currentQuestion.genMode === 'new' ? '신규' : '변형'} 문제
                </span>
              ) : currentQuestion.gsRound ? (
                <span style={{ color: '#0891b2' }}>
                  📝 GS {currentQuestion.gsRound} · {currentQuestion.questionNum}번
                  {currentQuestion.sourceRound && currentQuestion.sourceQNum && (
                    <span style={{ color: '#9ca3af', marginLeft: 6, fontSize: '0.75rem' }}>
                      (← {currentQuestion.sourceRound}회 {currentQuestion.sourceQNum}번 변형)
                    </span>
                  )}
                </span>
              ) : (
                <>{currentQuestion.round}회 · {currentQuestion.questionNum}번</>
              )}
            </span>
            {currentQuestion.points && (
              <span style={{ fontWeight: 800, fontSize: '0.95rem', color: '#1d4ed8' }}>
                {currentQuestion.points}점
              </span>
            )}
          </div>
          {currentQuestion.source === 'ai-generated' && (
            <div style={{ fontSize: '0.72rem', color: '#7c3aed', background: '#f5f3ff',
              border: '1px solid #ddd6fe', borderRadius: 8, padding: '6px 10px',
              marginBottom: 10 }}>
              AI 생성 문제입니다. 모범답안도 AI가 작성한 것이므로 학습 시 비판적으로 검토하세요.
              {currentQuestion.genMode === 'vary' && currentQuestion.changedFromOriginal &&
                ` (원본 대비: ${currentQuestion.changedFromOriginal})`}
              {currentQuestion.genMode === 'new' && currentQuestion.topic &&
                ` 논점: ${currentQuestion.topic}`}
            </div>
          )}
          {(currentQuestion.subconcept || currentQuestion.learningGoal) && (
            <div style={{ fontSize: '0.75rem', background: '#fffbeb',
              border: '1px solid #fde68a', borderRadius: 8, padding: '8px 12px',
              marginBottom: 10, color: '#92400e' }}>
              {currentQuestion.subconcept && (
                <div style={{ fontWeight: 800 }}>📚 학습 주제: {currentQuestion.subconcept}</div>
              )}
              {currentQuestion.learningGoal && (
                <div style={{ marginTop: 4, color: '#a16207' }}>
                  💡 이 문제로 배우는 것: {currentQuestion.learningGoal}
                </div>
              )}
            </div>
          )}
          {/* 문제 본문 — 폰트 사이즈 줄임 (q-text 클래스 대신 직접 0.92rem) */}
          <div style={{ lineHeight: 1.6, fontWeight: 400, color: '#111827',
            fontSize: 'calc(0.92rem * var(--q-fs, 1))' }}>
            <ParsedText text={currentQuestion.body} />
          </div>
        </div>

        {/* 모범답안 미리보기 (제출 전 확인) */}
        {currentQuestion.modelAnswer && (
          <div style={{ marginBottom: 14 }}>
            <button onClick={() => setPreviewModelInWrite(p => p === true ? false : p === 'ask' ? true : 'ask')}
              style={{ width: '100%', padding: '10px 14px', borderRadius: 10,
                border: `1px dashed ${previewModelInWrite === true ? '#16a34a' : '#d1d5db'}`,
                background: previewModelInWrite === true ? '#f0fdf4' : '#fff',
                color: previewModelInWrite === true ? '#15803d' : '#6b7280',
                fontSize: '0.85rem', fontWeight: 700, cursor: 'pointer', textAlign: 'left',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>💡 모범답안 미리 보기 {previewModelInWrite === true ? '(보는 중)' : ''}</span>
              <span style={{ fontSize: '0.72rem', fontWeight: 600 }}>
                {previewModelInWrite === true ? '▲ 닫기' : '▼ 펼치기'}
              </span>
            </button>
            {previewModelInWrite === 'ask' && (
              <div style={{ marginTop: 8, padding: '10px 14px', background: '#fffbeb',
                border: '1px solid #fde68a', borderRadius: 10, fontSize: '0.8rem',
                color: '#92400e', display: 'flex', justifyContent: 'space-between',
                alignItems: 'center', gap: 10 }}>
                <span>제출 전에 보면 학습 효과가 줄어요. 직접 작성 후 「제출 → 모범답안 보기」를 권장합니다.</span>
                <button onClick={() => setPreviewModelInWrite(true)}
                  style={{ flexShrink: 0, padding: '6px 12px', borderRadius: 8,
                    border: '1px solid #f59e0b', background: '#fff', color: '#b45309',
                    fontSize: '0.78rem', fontWeight: 700, cursor: 'pointer' }}>
                  그래도 보기
                </button>
              </div>
            )}
            {previewModelInWrite === true && (
              <div style={{ marginTop: 8, padding: 14, background: '#f9fafb',
                borderRadius: 10, border: '1px solid #e5e7eb',
                fontSize: 'calc(0.85rem * var(--q-fs, 1))', lineHeight: 1.65,
                color: '#374151' }}>
                <ParsedText text={currentQuestion.modelAnswer} />
                <div style={{ marginTop: 8, fontSize: '0.7rem', color: '#9ca3af', fontStyle: 'italic' }}>
                  ※ 답안을 보고도 작성·자기채점 가능. 본격 학습은 가리고 풀이 권장.
                </div>
              </div>
            )}
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
          <span style={{ fontWeight: 700, fontSize: '0.88rem', color: '#374151' }}>
            {outlineMode ? '🗂 내 목차' : '✍ 내 답안'}
          </span>
          {currentQuestion.modelAnswer && (
            <button onClick={() => { setOutlineMode(m => !m); setOutlineResult(null); }}
              style={{ padding: '4px 12px', borderRadius: 999, fontSize: '0.75rem', fontWeight: 700,
                border: `1.5px solid ${outlineMode ? '#f59e0b' : '#d1d5db'}`,
                background: outlineMode ? '#fffbeb' : '#fff',
                color: outlineMode ? '#b45309' : '#6b7280', cursor: 'pointer' }}>
              ⚡ 목차 스파링 {outlineMode ? 'ON' : 'OFF'}
            </button>
          )}
        </div>
        {outlineMode && (
          <div style={{ fontSize: '0.75rem', color: '#b45309', background: '#fffbeb',
            border: '1px solid #fde68a', borderRadius: 8, padding: '7px 11px', marginBottom: 8 }}>
            답안 전체 대신 <b>목차만</b> 잡아보세요 (권장 5분). Ⅰ. Ⅱ. / 1. 2. 형식으로 줄바꿈하며 작성 →
            제출하면 모범답안 목차와 나란히 대조됩니다. 가볍게 여러 문제를 회독하는 훈련입니다.
          </div>
        )}
        <textarea value={draft} onChange={(e) => setDraft(e.target.value)}
          placeholder={outlineMode
            ? 'Ⅰ. 평가개요\nⅡ. 비교표준지 선정\n 1. 선정기준\n 2. …\n식으로 목차만 빠르게.'
            : '답안을 작성하세요. 매 10초 자동 저장됩니다. 종료 시 다시 이어 쓸 수 있어요.'}
          style={{ width: '100%', minHeight: outlineMode ? 200 : 320, padding: 14, borderRadius: 12,
            border: `1px solid ${outlineMode ? '#fcd34d' : '#d1d5db'}`, fontSize: '0.95rem', lineHeight: 1.6,
            fontFamily: 'inherit', resize: 'vertical', boxSizing: 'border-box' }} />
        {/* ⚡ 목차 대조 결과 — 인라인 패널 */}
        {outlineMode && outlineResult != null && (() => {
          const model = extractOutline(currentQuestion.modelAnswer);
          return (
            <div style={{ marginTop: 12, border: '1.5px solid #f59e0b', borderRadius: 12,
              overflow: 'hidden' }}>
              <div style={{ background: '#fffbeb', padding: '8px 12px', fontWeight: 800,
                fontSize: '0.85rem', color: '#b45309' }}>
                ⚡ 목차 대조 — 빠진 항목·순서를 비교해보세요
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr' }}>
                <div style={{ padding: 12, borderRight: '1px solid #fde68a' }}>
                  <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#9ca3af', marginBottom: 6 }}>내 목차</div>
                  <div style={{ fontSize: '0.8rem', lineHeight: 1.7, whiteSpace: 'pre-wrap', color: '#374151' }}>
                    {outlineResult || '(비어 있음)'}
                  </div>
                </div>
                <div style={{ padding: 12, background: '#fafaf9' }}>
                  <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#16a34a', marginBottom: 6 }}>모범답안 목차</div>
                  <div style={{ fontSize: '0.8rem', lineHeight: 1.7, color: '#374151' }}>
                    {model.map((o, i) => (
                      <div key={i} style={{ paddingLeft: o.level * 12,
                        fontWeight: o.level <= 1 ? 800 : o.level === 2 ? 700 : 400 }}>
                        {o.text}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              <div style={{ display: 'flex', gap: 8, padding: '8px 12px', background: '#fffbeb' }}>
                <button onClick={() => setOutlineResult(null)}
                  style={{ flex: 1, padding: '8px', borderRadius: 8, border: '1px solid #fcd34d',
                    background: '#fff', color: '#b45309', fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer' }}>
                  다시 잡기
                </button>
                <button onClick={() => setPreviewModelInWrite(true)}
                  style={{ flex: 1, padding: '8px', borderRadius: 8, border: 'none',
                    background: '#16a34a', color: '#fff', fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer' }}>
                  전체 모범답안 보기
                </button>
              </div>
            </div>
          );
        })()}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          marginTop: 8, fontSize: '0.75rem', color: '#9ca3af' }}>
          <span>{draft.length}자</span>
          <button onClick={() => { if (window.confirm('초안 지울까요?')) { setDraft(''); clearDraft(currentQuestion.id); } }}
            style={{ border: 'none', background: 'none', color: '#9ca3af',
              cursor: 'pointer', fontSize: '0.75rem' }}>
            초안 지우기
          </button>
        </div>
      </main>

      <div style={{ position: 'sticky', bottom: 0, background: '#fff',
        borderTop: '1px solid #e5e7eb', padding: '10px 12px',
        display: 'flex', gap: 8 }}>
        <button onClick={() => { saveDraft(currentQuestion.id, draft); onNavigate('essay_questions'); }}
          style={{ flex: 1, padding: '12px', borderRadius: 10, fontWeight: 700,
            border: '1px solid #d1d5db', background: '#fff', color: '#374151',
            cursor: 'pointer' }}>
          저장하고 종료
        </button>
        <button onClick={onSubmit}
          disabled={draft.trim().length < (outlineMode ? 2 : 10)}
          style={{ flex: 2, padding: '12px', borderRadius: 10, fontWeight: 800,
            border: 'none',
            background: draft.trim().length < (outlineMode ? 2 : 10) ? '#d1d5db' : (outlineMode ? '#d97706' : '#2563eb'),
            color: '#fff', cursor: draft.trim().length < (outlineMode ? 2 : 10) ? 'default' : 'pointer' }}>
          {outlineMode ? '⚡ 목차 제출 → 모범 목차 대조' : '제출 → 모범답안 보기'}
        </button>
      </div>
    </>);
  }

  // ═══════════════════ result ═══════════════════
  if (mode === 'essay_result') {
    if (!currentQuestion) return shell(<div style={{ padding: 24, color: '#9ca3af' }}>결과 데이터 없음</div>);
    const cur = progress[currentQuestion.id];
    const prevAttempts = cur?.attempts || [];
    return shell(<>
      {header('결과', '문제 목록', 'essay_questions')}
      <main className="main-content" style={{ marginTop: 16 }}>
        <section style={{ background: '#fff', borderRadius: 12, padding: 16,
          boxShadow: 'var(--shadow-sm)', marginBottom: 14 }}>
          <div style={{ fontSize: '0.78rem', color: '#9ca3af', fontWeight: 700 }}>
            {currentQuestion.gsRound
              ? `GS ${currentQuestion.gsRound} · ${currentQuestion.questionNum}번`
              : `${currentQuestion.round}회 · ${currentQuestion.questionNum}번`}
            {currentQuestion.points && ` · ${currentQuestion.points}점`}
            · 소요 {fmtClock(submittedDurationMs)}
          </div>
          {currentQuestion.sourceRound && currentQuestion.sourceQNum && (
            <div style={{ marginTop: 4, fontSize: '0.72rem', color: '#0891b2', fontWeight: 600 }}>
              📚 출처: {currentQuestion.sourceRound}회 {currentQuestion.sourceQNum}번 기출문제 변형
            </div>
          )}
          <div style={{ marginTop: 10, fontWeight: 700, fontSize: '0.88rem', color: '#374151' }}>📝 문제</div>
          <div style={{ marginTop: 6, fontSize: '0.83rem', lineHeight: 1.6,
            color: '#111827', maxHeight: 280, overflow: 'auto',
            padding: 10, background: '#f9fafb', borderRadius: 8 }}>
            <ParsedText text={currentQuestion.body} />
          </div>
        </section>

        <section style={{ background: '#eff6ff', borderRadius: 12, padding: 16,
          border: '1px solid #bfdbfe', marginBottom: 14 }}>
          <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#1d4ed8' }}>✍ 내 답안</div>
          <div style={{ marginTop: 6, fontSize: '0.83rem', lineHeight: 1.7,
            color: '#111827', whiteSpace: 'pre-wrap' }}>
            {submittedAnswer || '(답안 없음)'}
          </div>
          <div style={{ marginTop: 6, fontSize: '0.72rem', color: '#1e40af' }}>
            {submittedAnswer.length}자
          </div>
        </section>

        {/* 키워드 매칭 — 자기채점 객관성 보조 */}
        {currentQuestion.keyPoints && currentQuestion.keyPoints.length > 0 && (() => {
          const matches = matchAll(submittedAnswer, currentQuestion.keyPoints);
          const hitCount = matches.filter(m => m.matched).length;
          const total = matches.length;
          const pct = total ? Math.round((hitCount / total) * 100) : 0;
          const color = pct >= 80 ? '#16a34a' : pct >= 60 ? '#2563eb' : pct >= 40 ? '#ea580c' : '#dc2626';
          return (
            <section style={{ background: '#fff', borderRadius: 12, padding: 16,
              boxShadow: 'var(--shadow-sm)', marginBottom: 14 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                <div style={{ fontWeight: 800, fontSize: '0.92rem', color: '#111827' }}>
                  🎯 핵심 키워드 적중
                </div>
                <div style={{ fontWeight: 800, fontSize: '1.05rem', color }}>
                  {hitCount} / {total} ({pct}%)
                </div>
              </div>
              <div style={{ fontSize: '0.72rem', color: '#9ca3af', marginTop: 2, marginBottom: 10 }}>
                답안 텍스트에서 자동 검색. 누락된 키워드는 학습 보강 필요.
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {matches.map((m, i) => (
                  <span key={i} style={{
                    padding: '4px 10px', borderRadius: 999,
                    fontSize: '0.75rem', fontWeight: 600,
                    background: m.matched ? '#f0fdf4' : '#fef2f2',
                    color: m.matched ? '#15803d' : '#b91c1c',
                    border: `1px solid ${m.matched ? '#bbf7d0' : '#fecaca'}`,
                  }}>
                    {m.matched ? '✓' : '✗'} {m.kp}
                  </span>
                ))}
              </div>
            </section>
          );
        })()}

        {currentQuestion.modelAnswer ? (
          <section style={{ background: '#fff', borderRadius: 12, padding: 16,
            border: '1px solid #e5e7eb', marginBottom: 14 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
              <div style={{ fontWeight: 700, fontSize: '0.9rem',
                color: currentQuestion.modelAnswerSource === 'ai-direct-note' ? '#0891b2'
                  : currentQuestion.modelAnswerSource === 'ai-generated' ? '#7c3aed'
                  : currentQuestion.modelAnswerSource === 'ai-direct' ? '#2563eb'
                  : '#16a34a' }}>
                {currentQuestion.modelAnswerSource === 'ai-direct-note' ? '📚 학습 안내 (자기채점)'
                  : currentQuestion.modelAnswerSource === 'ai-generated' ? '🤖 AI 모범답안'
                  : currentQuestion.modelAnswerSource === 'ai-direct' ? '🧠 LLM 풀이 (학습용)'
                  : '✅ 모범답안'}
                {currentQuestion.modelAnswerSource === 'round' && ' (회차 전체)'}
                {currentQuestion.modelAnswerSource === 'ai-generated' && (
                  <span style={{ fontSize: '0.7rem', fontWeight: 600, color: '#9ca3af', marginLeft: 6 }}>
                    검증 필요
                  </span>
                )}
                {currentQuestion.modelAnswerSource === 'ai-direct' && (
                  <span style={{ fontSize: '0.7rem', fontWeight: 600, color: '#9ca3af', marginLeft: 6 }}>
                    핵심산식·법규 위주 · 수치는 가정
                  </span>
                )}
              </div>
              <button onClick={() => setShowModel(s => !s)}
                style={{ border: '1px solid #d1d5db', background: '#fff',
                  borderRadius: 8, padding: '4px 10px', fontSize: '0.78rem',
                  fontWeight: 700, cursor: 'pointer' }}>
                {showModel ? '숨기기' : '펼치기'}
              </button>
            </div>
            {showModel && (
              <div style={{ marginTop: 10, fontSize: '0.83rem', lineHeight: 1.7,
                color: '#374151' }}>
                <ParsedText text={currentQuestion.modelAnswer} />
              </div>
            )}
            {!showModel && (
              <div style={{ marginTop: 6, fontSize: '0.78rem', color: '#9ca3af' }}>
                먼저 자기채점한 뒤 펼쳐서 비교해보세요. (자동 reveal 안 함)
              </div>
            )}
          </section>
        ) : (
          <section style={{ background: '#fafafa', borderRadius: 12, padding: 14,
            border: '1px dashed #e5e7eb', marginBottom: 14, fontSize: '0.85rem', color: '#6b7280' }}>
            {subj.key === 'practice'
              ? '모범답안 없음 (이 문제는 답안집에 미수록 또는 자동 매칭 실패)'
              : '📝 모범답안은 단계적으로 추가 중이에요. 아래 자기채점(키워드)과 AI 학습 탭의 답안 채점으로 점검해 보세요.'}
          </section>
        )}

        <section style={{ background: '#fff', borderRadius: 12, padding: 16,
          boxShadow: 'var(--shadow-sm)', marginBottom: 14 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
            <div style={{ fontWeight: 800, fontSize: '0.95rem', color: '#111827' }}>
              🎯 자기 채점
            </div>
            <div style={{ display: 'flex', gap: 4 }}>
              {[['simple','간단'], ['detail','상세']].map(([id, lbl]) => (
                <button key={id} onClick={() => {
                  setTierMode(id);
                  try { localStorage.setItem(SELF_TIER_KEY, id); } catch { /* SSR */ }
                }}
                  style={{ fontSize: '0.72rem', padding: '4px 9px', borderRadius: 6,
                    border: tierMode === id ? '1px solid #2563eb' : '1px solid #d1d5db',
                    background: tierMode === id ? '#eff6ff' : '#fff',
                    color: tierMode === id ? '#1d4ed8' : '#6b7280',
                    fontWeight: 700, cursor: 'pointer' }}>
                  {lbl}
                </button>
              ))}
            </div>
          </div>

          {tierMode === 'simple' ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)',
              gap: 8, marginTop: 12 }}>
              {TIER_OPTIONS.map(t => {
                const on = selectedTier === t.id;
                return (
                  <button key={t.id} onClick={() => setSelectedTier(t.id)}
                    style={{ padding: '14px 10px', borderRadius: 10,
                      border: `1.5px solid ${on ? t.color : '#e5e7eb'}`,
                      background: on ? t.bg : '#fff', cursor: 'pointer',
                      textAlign: 'center' }}>
                    <div style={{ fontWeight: 800, fontSize: '0.95rem', color: t.color }}>
                      {t.label}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: '#6b7280', marginTop: 2 }}>
                      {t.subLabel}
                    </div>
                  </button>
                );
              })}
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 12 }}>
              {RUBRIC_DEFAULT.map(r => {
                const on = !!rubric[r.id];
                return (
                  <button key={r.id} onClick={() => setRubric(prev => ({ ...prev, [r.id]: !prev[r.id] }))}
                    style={{ display: 'flex', alignItems: 'center', gap: 10,
                      padding: '10px 14px', borderRadius: 8, cursor: 'pointer',
                      border: `1.5px solid ${on ? '#16a34a' : '#e5e7eb'}`,
                      background: on ? '#f0fdf4' : '#fff', textAlign: 'left' }}>
                    <span style={{ width: 22, height: 22, borderRadius: 5,
                      background: on ? '#16a34a' : '#fff',
                      border: on ? 'none' : '1.5px solid #d1d5db',
                      color: '#fff', display: 'flex', alignItems: 'center',
                      justifyContent: 'center', fontSize: '0.85rem' }}>
                      {on ? '✓' : ''}
                    </span>
                    <span style={{ flex: 1, fontWeight: 700, fontSize: '0.88rem',
                      color: '#374151' }}>{r.label}</span>
                    <span style={{ fontSize: '0.72rem', color: '#9ca3af' }}>
                      {r.weight}점
                    </span>
                  </button>
                );
              })}
              <div style={{ marginTop: 6, fontSize: '0.78rem', color: '#6b7280', textAlign: 'right' }}>
                예상 점수: <b style={{ color: '#1d4ed8' }}>
                  {Math.round((RUBRIC_DEFAULT.reduce((s, r) => s + (rubric[r.id] ? r.weight : 0), 0) /
                    RUBRIC_DEFAULT.reduce((s, r) => s + r.weight, 0)) * 100) || 0}점
                </b>
              </div>
            </div>
          )}

          <textarea value={notes} onChange={(e) => setNotes(e.target.value)}
            placeholder="메모 (놓친 논점, 보강할 점 등 — 선택)"
            style={{ width: '100%', minHeight: 60, padding: 10, marginTop: 12,
              borderRadius: 8, border: '1px solid #d1d5db', fontSize: '0.85rem',
              fontFamily: 'inherit', resize: 'vertical', boxSizing: 'border-box' }} />

          <button onClick={onSaveGrade}
            disabled={tierMode === 'simple' && !selectedTier}
            style={{ width: '100%', marginTop: 12, padding: '12px',
              borderRadius: 10, fontWeight: 800,
              border: 'none',
              background: tierMode === 'simple' && !selectedTier ? '#d1d5db' : '#2563eb',
              color: '#fff',
              cursor: tierMode === 'simple' && !selectedTier ? 'default' : 'pointer' }}>
            저장하고 문제 목록으로
          </button>
        </section>

        {prevAttempts.length > 0 && (
          <section style={{ background: '#fff', borderRadius: 12, padding: 16,
            boxShadow: 'var(--shadow-sm)' }}>
            <div style={{ fontWeight: 800, fontSize: '0.92rem', color: '#374151', marginBottom: 10 }}>
              이전 풀이 ({prevAttempts.length}회)
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {[...prevAttempts].reverse().slice(0, 5).map((a, i) => (
                <div key={i} style={{ display: 'flex', justifyContent: 'space-between',
                  alignItems: 'center', fontSize: '0.82rem',
                  padding: '6px 10px', background: '#f9fafb', borderRadius: 6 }}>
                  <span style={{ color: '#6b7280' }}>{fmtDate(a.ts)}</span>
                  <span style={{ fontWeight: 800, color:
                    a.selfScore >= 80 ? '#16a34a' :
                    a.selfScore >= 60 ? '#2563eb' :
                    a.selfScore >= 40 ? '#ea580c' : '#dc2626' }}>
                    {a.selfScore}점
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </>);
  }

  return null;
};

// ═══════════════════ 🃏 논점 인출카드 ═══════════════════
// 기출·GS 전 문항의 topic/logicalPoints/lawRefs로 만든 인출 훈련 카드.
// 앞면: 문제 상황(topic) → 핵심 논점·근거조문을 머릿속으로 인출 → 뒷면과 대조.
// 간단 SRS: 모름(10분) / 애매(1일) / 알았다(박스 승급: 1·3·7·14·30일)
const CARDS_SRS_KEY = 'quiz-essay-cards-srs-v1';
const SRS_DAYS = [1, 3, 7, 14, 30];

function loadCardSrs() {
  try { return JSON.parse(localStorage.getItem(CARDS_SRS_KEY) || '{}') || {}; } catch { return {}; }
}

export function EssayCards({ subjDir, manifest, onBack }) {
  const [deck, setDeck] = useState(null);      // 전체 카드
  const [queue, setQueue] = useState([]);      // 오늘 큐 (due + 새 카드)
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [srs, setSrs] = useState(loadCardSrs);
  const [doneCount, setDoneCount] = useState(0);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const ids = (manifest?.chapters || [])
        .filter(c => c.id !== 'cleanup' && (c.count || 0) > 0)
        .map(c => c.id);
      const all = [];
      await Promise.all(ids.map(async (id) => {
        try {
          const r = await fetch(`${subjDir}${id}.json`);
          if (!r.ok) return;
          const d = await r.json();
          for (const q of d.questions || []) {
            if ((q.source === 'official' || q.source === 'gs') && q.topic &&
                (q.logicalPoints?.length || q.lawRefs?.length)) {
              all.push({ id: q.id, chapter: id, topic: q.topic, points: q.points,
                logicalPoints: q.logicalPoints || [], lawRefs: q.lawRefs || [] });
            }
          }
        } catch { /* skip chapter */ }
      }));
      if (cancelled) return;
      const cur = loadCardSrs();
      const now = Date.now();
      const due = all.filter(c => cur[c.id] && cur[c.id].due <= now);
      const fresh = all.filter(c => !cur[c.id]).sort(() => Math.random() - 0.5);
      setDeck(all);
      setQueue([...due, ...fresh].slice(0, 30)); // 한 세션 30장
    })();
    return () => { cancelled = true; };
  }, [subjDir, manifest]);

  const grade = (kind) => {
    const card = queue[idx];
    if (!card) return;
    const cur = { ...srs };
    const prev = cur[card.id] || { box: 0 };
    const now = Date.now();
    if (kind === 'again') cur[card.id] = { box: 0, due: now + 10 * 60000 };
    else if (kind === 'hard') cur[card.id] = { box: prev.box, due: now + 86400000 };
    else cur[card.id] = { box: Math.min(prev.box + 1, SRS_DAYS.length - 1),
      due: now + SRS_DAYS[Math.min(prev.box, SRS_DAYS.length - 1)] * 86400000 };
    setSrs(cur);
    try { localStorage.setItem(CARDS_SRS_KEY, JSON.stringify(cur)); } catch { /* full */ }
    setDoneCount(n => n + 1);
    setFlipped(false);
    setIdx(i => i + 1);
  };

  const card = queue[idx];
  const learned = deck ? deck.filter(c => srs[c.id] && srs[c.id].box >= 2).length : 0;

  return (
    <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh' }}>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <button className="back-btn" onClick={onBack}>
          <ArrowLeft size={24} style={{ marginRight: 8 }} />
          <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>단원 목록</span>
        </button>
        <span style={{ padding: '6px 12px', fontSize: '0.8rem', color: '#6b7280', fontWeight: 700 }}>
          {deck ? `오늘 ${Math.min(idx, queue.length)}/${queue.length} · 누적 학습 ${learned}/${deck.length}` : ''}
        </span>
      </header>
      <main className="main-content" style={{ marginTop: 16, paddingBottom: 24 }}>
        {!deck ? (
          <div style={{ padding: 40, textAlign: 'center', color: '#9ca3af' }}>카드 준비 중…</div>
        ) : !card ? (
          <div style={{ padding: 40, textAlign: 'center' }}>
            <div style={{ fontSize: '2.2rem' }}>🎉</div>
            <div style={{ fontWeight: 800, marginTop: 8, color: '#111827' }}>오늘 큐 완료!</div>
            <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: 6 }}>
              {doneCount}장 학습 · 복습 예약 카드는 due가 되면 다시 나타납니다.
            </div>
            <button onClick={onBack} style={{ marginTop: 18, padding: '10px 22px', borderRadius: 10,
              border: 'none', background: '#7c3aed', color: '#fff', fontWeight: 800, cursor: 'pointer' }}>
              단원 목록으로
            </button>
          </div>
        ) : (
          <>
            <div onClick={() => setFlipped(f => !f)}
              style={{ background: '#fff', borderRadius: 16, padding: 22, minHeight: 300,
                boxShadow: '0 4px 16px rgba(0,0,0,0.07)', cursor: 'pointer',
                border: flipped ? '1.5px solid #a78bfa' : '1.5px solid #e5e7eb',
                display: 'flex', flexDirection: 'column' }}>
              <div style={{ fontSize: '0.7rem', fontWeight: 700, color: '#9ca3af', marginBottom: 10 }}>
                단원 {card.chapter}{card.points ? ` · ${card.points}점 문제` : ''} · 카드 {idx + 1}
              </div>
              <div style={{ fontWeight: 800, fontSize: '1.02rem', color: '#111827', lineHeight: 1.55 }}>
                {card.topic}
              </div>
              {!flipped ? (
                <div style={{ marginTop: 'auto', paddingTop: 24, textAlign: 'center',
                  color: '#7c3aed', fontSize: '0.85rem', fontWeight: 700 }}>
                  이 문제의 <b>핵심 논점</b>과 <b>근거조문</b>을 떠올려보세요<br />
                  <span style={{ color: '#9ca3af', fontWeight: 500, fontSize: '0.75rem' }}>(탭하면 정답 공개)</span>
                </div>
              ) : (
                <div style={{ marginTop: 14 }}>
                  {card.logicalPoints.length > 0 && (
                    <>
                      <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#7c3aed', marginBottom: 6 }}>핵심 논점</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 12 }}>
                        {card.logicalPoints.map((lp, i) => (
                          <span key={i} style={{ fontSize: '0.78rem', background: '#f5f3ff',
                            color: '#5b21b6', border: '1px solid #ddd6fe', borderRadius: 999,
                            padding: '3px 10px', fontWeight: 600 }}>{lp}</span>
                        ))}
                      </div>
                    </>
                  )}
                  {card.lawRefs.length > 0 && (
                    <>
                      <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#0891b2', marginBottom: 6 }}>근거조문</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                        {card.lawRefs.map((lr, i) => (
                          <span key={i} style={{ fontSize: '0.78rem', background: '#ecfeff',
                            color: '#155e75', border: '1px solid #a5f3fc', borderRadius: 999,
                            padding: '3px 10px', fontWeight: 600 }}>{lr}</span>
                        ))}
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
            {flipped ? (
              <div style={{ display: 'flex', gap: 8, marginTop: 14 }}>
                <button onClick={() => grade('again')} style={{ flex: 1, padding: '13px',
                  borderRadius: 12, border: '1px solid #fecaca', background: '#fef2f2',
                  color: '#dc2626', fontWeight: 800, cursor: 'pointer' }}>✕ 모름<br />
                  <span style={{ fontSize: '0.65rem', fontWeight: 600 }}>10분 후</span></button>
                <button onClick={() => grade('hard')} style={{ flex: 1, padding: '13px',
                  borderRadius: 12, border: '1px solid #fde68a', background: '#fffbeb',
                  color: '#b45309', fontWeight: 800, cursor: 'pointer' }}>~ 애매<br />
                  <span style={{ fontSize: '0.65rem', fontWeight: 600 }}>1일 후</span></button>
                <button onClick={() => grade('good')} style={{ flex: 1, padding: '13px',
                  borderRadius: 12, border: '1px solid #a7f3d0', background: '#ecfdf5',
                  color: '#059669', fontWeight: 800, cursor: 'pointer' }}>✓ 알았다<br />
                  <span style={{ fontSize: '0.65rem', fontWeight: 600 }}>
                    {SRS_DAYS[Math.min((srs[card.id]?.box || 0), SRS_DAYS.length - 1)]}일 후
                  </span></button>
              </div>
            ) : (
              <button onClick={() => setFlipped(true)} style={{ width: '100%', marginTop: 14,
                padding: '13px', borderRadius: 12, border: 'none', background: '#7c3aed',
                color: '#fff', fontWeight: 800, fontSize: '0.95rem', cursor: 'pointer' }}>
                정답 보기
              </button>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default EssayMode;
