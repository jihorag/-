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

const EssayMode = ({ mode, chapter, questionId, onNavigate, setChapter, setQuestionId, fontScale }) => {
  const [manifest, setManifest] = useState(null);
  const [manifestErr, setManifestErr] = useState(null);
  const [chapterCache, setChapterCache] = useState({});  // { [id]: chapterData (questions merged official+generated) }
  const [progress, setProgressState] = useState(() => loadProgress());
  // 문제 목록 source 필터: 'all' | 'official' | 'ai-vary' | 'ai-new'
  const [sourceFilter, setSourceFilter] = useState('all');

  // 작성 화면 상태
  const [draft, setDraft] = useState('');
  const [startedAt, setStartedAt] = useState(null);
  const [previewModelInWrite, setPreviewModelInWrite] = useState(false);
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

  // ─────────── manifest 로드 ───────────
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const r = await fetch('/data/essay/practice/manifest.json');
        if (!r.ok) throw new Error(`manifest ${r.status}`);
        const m = await r.json();
        if (!cancelled) setManifest(m);
      } catch (e) {
        if (!cancelled) setManifestErr(e.message);
      }
    })();
    return () => { cancelled = true; };
  }, []);

  // ─────────── chapter 데이터 lazy fetch (official + generated 병합) ───────────
  const ensureChapter = useCallback(async (id) => {
    if (chapterCache[id]) return chapterCache[id];
    try {
      const [official, generated] = await Promise.all([
        fetch(`/data/essay/practice/${id}.json`).then(r => r.ok ? r.json() : null),
        fetch(`/data/essay/practice/${id}-generated.json`).then(r => r.ok ? r.json() : null),
      ]);
      if (!official) throw new Error(`chapter ${id} not found`);
      const genQ = generated?.questions || [];
      const merged = {
        ...official,
        questions: [...official.questions, ...genQ],
        officialCount: official.questions.length,
        generatedCount: genQ.length,
      };
      setChapterCache(prev => ({ ...prev, [id]: merged }));
      return merged;
    } catch (e) {
      console.error('essay chapter fetch failed', e);
      return null;
    }
  }, [chapterCache]);

  useEffect(() => {
    if (chapter && !chapterCache[chapter]) ensureChapter(chapter);
  }, [chapter, chapterCache, ensureChapter]);

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
  }, [mode, questionId]);

  // ─────────── auto-save 매 10초 ───────────
  useEffect(() => {
    if (mode !== 'essay_write' || !questionId) return;
    const t = setInterval(() => saveDraft(questionId, draft), 10000);
    return () => clearInterval(t);
  }, [mode, questionId, draft]);

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
    const dur = startedAt ? Date.now() - startedAt : 0;
    setSubmittedAnswer(draft);
    setSubmittedDurationMs(dur);
    onNavigate('essay_result');
  }, [currentQuestion, draft, startedAt, onNavigate]);

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
    const attempt = {
      ts: Date.now(),
      answer: submittedAnswer,
      selfScore,
      selfTier: tier?.id || null,
      rubric: tierMode === 'detail' ? { ...rubric } : null,
      notes: notes.trim() || null,
      durationMs: submittedDurationMs,
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

  if (manifestErr) {
    return shell(<>
      {header('2차 준비', '홈', 'home')}
      <div style={{ padding: 24, color: '#dc2626' }}>
        2차 데이터 로드 실패: {manifestErr}
        <div style={{ marginTop: 8, fontSize: '0.85rem', color: '#9ca3af' }}>
          빌드 시 essay 데이터가 누락된 것 같습니다. `python3 scripts/build_essay.py` 후 다시 시도.
        </div>
      </div>
    </>);
  }
  if (!manifest) {
    return shell(<div style={{ padding: 24, color: '#9ca3af' }}>데이터 불러오는 중…</div>);
  }

  // ═══════════════════ subjects ═══════════════════
  if (mode === 'essay_subjects') {
    return shell(<>
      {header('2차 준비', '홈', 'home')}
      <div className="screen-head"><h1 className="screen-title">📝 2차 준비</h1>
        <p style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: 4 }}>
          논술형 기출 풀이 → 모범답안 확인 → 자기 채점
        </p>
      </div>
      <main className="main-content" style={{ marginTop: 16 }}>
        <button onClick={() => { setChapter(null); setQuestionId(null); onNavigate('essay_chapters'); }}
          style={{ width: '100%', textAlign: 'left', padding: '18px', borderRadius: 14,
            border: '1px solid #fde68a', background: '#fffbeb', cursor: 'pointer' }}>
          <div style={{ fontSize: '1.5rem' }}>💼</div>
          <div style={{ fontWeight: 800, fontSize: '1.05rem', color: '#111827', marginTop: 8 }}>
            {manifest.subject}
          </div>
          <div style={{ fontSize: '0.82rem', color: '#92400e', marginTop: 4 }}>
            {manifest.chapters.length}개 단원 · {manifest.total}문항 (기출 11~36회)
          </div>
          <div style={{ marginTop: 10, fontSize: '0.82rem', color: '#a16207', fontWeight: 700 }}>
            시작 →
          </div>
        </button>
        <div style={{ marginTop: 16, padding: 12, borderRadius: 10,
          background: '#fafafa', border: '1px solid #e5e7eb', fontSize: '0.78rem', color: '#6b7280' }}>
          📌 현재 v1: 감정평가실무만. 이론·법규는 다음 라운드에 추가.
        </div>
      </main>
    </>);
  }

  // ═══════════════════ chapters ═══════════════════
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
      </div>
      <main className="main-content" style={{ marginTop: 16 }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {manifest.chapters.map(c => {
            const cd = chapterCache[c.id];
            const done = cd ? cd.questions.filter(q => progress[q.id]?.attempts?.length).length : 0;
            const pct = c.count ? Math.round((done / c.count) * 100) : 0;
            return (
              <button key={c.id}
                onClick={() => { setChapter(c.id); setQuestionId(null); ensureChapter(c.id); onNavigate('essay_questions'); }}
                style={{ background: '#fff', borderRadius: 12, padding: 16,
                  border: '1px solid #e5e7eb', textAlign: 'left', cursor: 'pointer',
                  boxShadow: 'var(--shadow-sm)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                  <div style={{ fontWeight: 800, fontSize: '1rem', color: '#111827' }}>
                    단원 {c.id} · {c.title}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#2563eb', fontWeight: 700 }}>{pct}%</div>
                </div>
                <div style={{ fontSize: '0.82rem', color: '#6b7280', marginTop: 6 }}>
                  {c.count}문항 · 답안 {c.matchedAnswer}/{c.count} · 회차 {c.rounds.join(', ')}회
                </div>
                <div style={{ height: 4, background: '#f3f4f6', borderRadius: 2,
                  marginTop: 8, overflow: 'hidden' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: '#2563eb' }} />
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
    if (!cd) return shell(<div style={{ padding: 24, color: '#9ca3af' }}>단원 데이터 불러오는 중…</div>);

    // source별 카운트
    const counts = {
      all: cd.questions.length,
      official: cd.questions.filter(q => q.source !== 'ai-generated').length,
      'ai-vary': cd.questions.filter(q => q.source === 'ai-generated' && q.genMode === 'vary').length,
      'ai-new': cd.questions.filter(q => q.source === 'ai-generated' && q.genMode === 'new').length,
    };
    const filterChips = [
      { id: 'all',      label: '전체',     count: counts.all },
      { id: 'official', label: '실문제',   count: counts.official },
      { id: 'ai-vary',  label: '🤖 변형',  count: counts['ai-vary'] },
      { id: 'ai-new',   label: '🤖 신규',  count: counts['ai-new'] },
    ].filter(c => c.count > 0);

    const visible = cd.questions.filter(q => {
      if (sourceFilter === 'all') return true;
      if (sourceFilter === 'official') return q.source !== 'ai-generated';
      if (sourceFilter === 'ai-vary') return q.source === 'ai-generated' && q.genMode === 'vary';
      if (sourceFilter === 'ai-new') return q.source === 'ai-generated' && q.genMode === 'new';
      return true;
    });

    return shell(<>
      {header(`단원 ${chapter}`, '단원 목록', 'essay_chapters')}
      <div className="screen-head"><h1 className="screen-title">{meta?.title || chapter}</h1>
        <p style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: 4 }}>
          기출 {cd.officialCount}문항{cd.generatedCount > 0 && <> · 🤖 AI 생성 {cd.generatedCount}문항</>}
        </p>
      </div>
      <main className="main-content" style={{ marginTop: 16 }}>
        {/* source 필터 chip */}
        {filterChips.length > 1 && (
          <div style={{ display: 'flex', gap: 6, marginBottom: 14, overflowX: 'auto',
            WebkitOverflowScrolling: 'touch' }}>
            {filterChips.map(c => {
              const on = sourceFilter === c.id;
              return (
                <button key={c.id} onClick={() => setSourceFilter(c.id)}
                  style={{ flex: '0 0 auto', padding: '7px 12px', whiteSpace: 'nowrap',
                    border: on ? '1.5px solid #2563eb' : '1px solid #d1d5db',
                    background: on ? '#eff6ff' : '#fff',
                    color: on ? '#1d4ed8' : '#374151',
                    borderRadius: 999, fontWeight: on ? 800 : 600,
                    fontSize: '0.82rem', cursor: 'pointer' }}>
                  {c.label} {c.count}
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
            return (
              <button key={q.id}
                onClick={() => { setQuestionId(q.id); onNavigate('essay_write'); }}
                style={{ background: '#fff', borderRadius: 10, padding: '14px 16px',
                  border: isAI ? '1px solid #ddd6fe' : '1px solid #e5e7eb',
                  textAlign: 'left', cursor: 'pointer',
                  display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                <div style={{ minWidth: 56, fontSize: '0.78rem', color: '#9ca3af', fontWeight: 700 }}>
                  {isAI ? (
                    <>🤖<br /><span style={{ color: '#7c3aed', fontSize: '0.72rem' }}>
                      {q.genMode === 'new' ? '신규' : '변형'}
                    </span></>
                  ) : (
                    <>{q.round}회<br /><span style={{ color: '#374151', fontSize: '0.85rem' }}>{q.questionNum}번</span></>
                  )}
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: '0.88rem', color: '#374151', lineHeight: 1.5,
                    display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
                    overflow: 'hidden' }}>
                    {q.body.slice(0, 200).replace(/\n/g, ' ')}
                  </div>
                  <div style={{ marginTop: 6, display: 'flex', gap: 8, flexWrap: 'wrap',
                    fontSize: '0.72rem' }}>
                    {q.points && (
                      <span style={{ color: '#1d4ed8', fontWeight: 700 }}>{q.points}점</span>
                    )}
                    {isAI && q.genMode === 'vary' && q.seedQuestionId && (
                      <span style={{ color: '#7c3aed', fontWeight: 600 }}>
                        원본: {q.seedQuestionId.replace('v3-', '').replace(/-/g, ' ')}
                      </span>
                    )}
                    {isAI && q.genMode === 'new' && q.topic && (
                      <span style={{ color: '#7c3aed', fontWeight: 600, maxWidth: 260,
                        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {q.topic}
                      </span>
                    )}
                    {!hasAnswer && (
                      <span style={{ color: '#9ca3af' }}>답안 없음</span>
                    )}
                    {attemptCount > 0 && (
                      <span style={{ color: '#16a34a', fontWeight: 700 }}>
                        {attemptCount}회 풀이 · 마지막 {lastScore}점
                      </span>
                    )}
                  </div>
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
          fontSize: '0.85rem', color: '#374151', fontWeight: 700 }}>
          ⏱ {fmtClock(elapsed)}
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
          {/* 문제 본문 — 폰트 사이즈 줄임 (q-text 클래스 대신 직접 0.92rem) */}
          <div style={{ lineHeight: 1.6, fontWeight: 400, color: '#111827',
            fontSize: 'calc(0.92rem * var(--q-fs, 1))' }}>
            <ParsedText text={currentQuestion.body} />
          </div>
        </div>

        {/* 모범답안 미리보기 (제출 전 확인) */}
        {currentQuestion.modelAnswer && (
          <div style={{ marginBottom: 14 }}>
            <button onClick={() => setPreviewModelInWrite(p => !p)}
              style={{ width: '100%', padding: '10px 14px', borderRadius: 10,
                border: `1px dashed ${previewModelInWrite ? '#16a34a' : '#d1d5db'}`,
                background: previewModelInWrite ? '#f0fdf4' : '#fff',
                color: previewModelInWrite ? '#15803d' : '#6b7280',
                fontSize: '0.85rem', fontWeight: 700, cursor: 'pointer', textAlign: 'left',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>💡 모범답안 미리 보기 {previewModelInWrite ? '(보는 중)' : ''}</span>
              <span style={{ fontSize: '0.72rem', fontWeight: 600 }}>
                {previewModelInWrite ? '▲ 닫기' : '▼ 펼치기'}
              </span>
            </button>
            {previewModelInWrite && (
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

        <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#374151', marginBottom: 6 }}>
          ✍ 내 답안
        </div>
        <textarea value={draft} onChange={(e) => setDraft(e.target.value)}
          placeholder="답안을 작성하세요. 매 10초 자동 저장됩니다. 종료 시 다시 이어 쓸 수 있어요."
          style={{ width: '100%', minHeight: 320, padding: 14, borderRadius: 12,
            border: '1px solid #d1d5db', fontSize: '0.95rem', lineHeight: 1.6,
            fontFamily: 'inherit', resize: 'vertical', boxSizing: 'border-box' }} />
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
          disabled={draft.trim().length < 10}
          style={{ flex: 2, padding: '12px', borderRadius: 10, fontWeight: 800,
            border: 'none', background: draft.trim().length < 10 ? '#d1d5db' : '#2563eb',
            color: '#fff', cursor: draft.trim().length < 10 ? 'default' : 'pointer' }}>
          제출 → 모범답안 보기
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
            {currentQuestion.round}회 · {currentQuestion.questionNum}번
            {currentQuestion.points && ` · ${currentQuestion.points}점`}
            · 소요 {fmtClock(submittedDurationMs)}
          </div>
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

        {currentQuestion.modelAnswer ? (
          <section style={{ background: '#fff', borderRadius: 12, padding: 16,
            border: '1px solid #e5e7eb', marginBottom: 14 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
              <div style={{ fontWeight: 700, fontSize: '0.9rem',
                color: currentQuestion.modelAnswerSource === 'ai-generated' ? '#7c3aed' : '#16a34a' }}>
                {currentQuestion.modelAnswerSource === 'ai-generated' ? '🤖 AI 모범답안' : '✅ 모범답안'}
                {currentQuestion.modelAnswerSource === 'round' && ' (회차 전체)'}
                {currentQuestion.modelAnswerSource === 'ai-generated' && (
                  <span style={{ fontSize: '0.7rem', fontWeight: 600, color: '#9ca3af', marginLeft: 6 }}>
                    검증 필요
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
              <div style={{ marginTop: 10, fontSize: '0.85rem', lineHeight: 1.7,
                color: '#374151', whiteSpace: 'pre-wrap' }}>
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
            border: '1px dashed #e5e7eb', marginBottom: 14, fontSize: '0.85rem', color: '#9ca3af' }}>
            모범답안 없음 (이 문제는 답안집에 미수록 또는 자동 매칭 실패)
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

export default EssayMode;
