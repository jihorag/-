// AI 학습 탭 — Claude 대화형 과외 + 진척 추적 + 일별 대화 기록.
// 기존 CivilMemorize(통암기) 탭을 대체. 첫 과목: 민법.
//
// 위험·검토(#8) 반영:
//  - BYOK: API 키는 localStorage에만, 키 없으면 입력 폼.
//  - 일일 메시지 cap (기본 50) — 초과 시 전송 차단.
//  - 큰 단원(M05·B03 등)은 section 단위로만 로드 → 토큰 절약 + prompt caching.
//  - 환각 방지: system 프롬프트에 "교재 인용만" 강제.
//  - 오프라인 안내: 네트워크 없으면 전송 비활성화 + 메시지.

import { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { ArrowLeft, Send, Settings as SettingsIcon, BookOpen, MessageSquare, RotateCcw, ChevronDown, Calendar, Sparkles, Key } from 'lucide-react';
import ParsedText from './ParsedText';
import {
  getByok, setByok, getPrefs, setPrefs,
  getCurrent, setCurrent,
  getMastery, getChapterMastery, updateChapterMastery,
  recordGrade, getDueChapters,
  getSessions, addSession, updateSession,
  getConversation, appendMessage,
  bumpUsage, canSendMessage, getUsage,
  pruneOldConversations,
  addAssessment,
} from './aiLearningStore';
import { sendMessages, buildSystemBlocks, sliceSection, extractJsonBlocks, MODELS } from './aiClaudeClient';

const INDEX_URL = '/data/study/civil/chapters_index.json';
const HANDOVER_URL = '/data/study/civil/handover.md';

function todayStr() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

function uid() {
  try { return crypto.randomUUID(); } catch { return 's_' + Math.random().toString(36).slice(2); }
}

function MasteryBar({ value, color = '#4f46e5' }) {
  const pct = Math.max(0, Math.min(1, value || 0)) * 100;
  return (
    <div style={{ background: '#f3f4f6', borderRadius: 6, height: 6, overflow: 'hidden' }}>
      <div style={{ width: `${pct}%`, height: '100%', background: color, transition: 'width .3s' }} />
    </div>
  );
}

function ChapterPicker({ chapters, current, onPick, mastery }) {
  const [open, setOpen] = useState(false);
  const cur = chapters.find((c) => c.code === current?.code);
  return (
    <div style={{ position: 'relative' }}>
      <button
        onClick={() => setOpen((v) => !v)}
        style={{
          width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: '10px 14px', background: '#fff', border: '1px solid #d1d5db', borderRadius: 10,
          fontSize: '0.95rem', fontWeight: 700, cursor: 'pointer', color: '#111827',
        }}
      >
        <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <BookOpen size={18} color="#4f46e5" />
          {cur ? `${cur.code} · ${cur.title}` : '단원 선택'}
          {cur && '★'.repeat(cur.frequency)}
        </span>
        <ChevronDown size={18} />
      </button>
      {open && (
        <div style={{
          position: 'absolute', top: 'calc(100% + 4px)', left: 0, right: 0, zIndex: 30,
          background: '#fff', border: '1px solid #d1d5db', borderRadius: 10,
          maxHeight: 360, overflowY: 'auto', boxShadow: '0 8px 24px rgba(0,0,0,.12)',
        }}>
          {chapters.map((c) => {
            const m = mastery[c.code] || { coverage: 0, accuracy: 0, status: 'not_started' };
            const active = c.code === current?.code;
            return (
              <button
                key={c.code}
                onClick={() => { onPick(c); setOpen(false); }}
                style={{
                  width: '100%', textAlign: 'left', padding: '10px 14px',
                  background: active ? '#eef2ff' : '#fff', border: 'none',
                  borderBottom: '1px solid #f3f4f6', cursor: 'pointer',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 700, color: '#111827' }}>
                    {c.code} · {c.title} {'★'.repeat(c.frequency)}
                  </span>
                  <span style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                    {m.status === 'mastered' ? '✓ 마스터' : m.status === 'in_progress' ? '진행 중' : '미시작'}
                  </span>
                </div>
                <div style={{ fontSize: '0.78rem', color: '#6b7280', marginTop: 2 }}>{c.subtitle}</div>
                <div style={{ marginTop: 6 }}>
                  <MasteryBar value={m.coverage} />
                </div>
              </button>
            );
          })}
        </div>
      )}
    </div>
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

function SettingsPanel({ prefs, onSave, onClearKey, usage }) {
  const today = usage[todayStr()] || { messages: 0, input_tokens: 0, output_tokens: 0 };
  return (
    <div style={{ padding: 16, background: '#fff', borderRadius: 12, border: '1px solid #e5e7eb' }}>
      <h3 style={{ margin: '0 0 12px 0', fontSize: '1rem' }}>설정</h3>
      <label style={{ display: 'block', fontSize: '0.85rem', color: '#374151', marginBottom: 4 }}>모델</label>
      <select
        value={prefs.model}
        onChange={(e) => onSave({ model: e.target.value })}
        style={{ width: '100%', padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.9rem', marginBottom: 12 }}
      >
        <option value={MODELS.primary}>Sonnet 4.6 (권장)</option>
        <option value={MODELS.fast}>Haiku 4.5 (빠름·저렴)</option>
        <option value={MODELS.premium}>Opus 4.7 (최고품질·비쌈)</option>
      </select>
      <label style={{ display: 'block', fontSize: '0.85rem', color: '#374151', marginBottom: 4 }}>일일 메시지 cap</label>
      <input
        type="number"
        min={0}
        max={500}
        value={prefs.daily_cap}
        onChange={(e) => onSave({ daily_cap: parseInt(e.target.value, 10) || 0 })}
        style={{ width: '100%', padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.9rem', marginBottom: 4 }}
      />
      <div style={{ fontSize: '0.78rem', color: '#6b7280', marginBottom: 12 }}>
        오늘 사용량: {today.messages}회 / 입력 {today.input_tokens.toLocaleString()} 토큰 / 출력 {today.output_tokens.toLocaleString()} 토큰
      </div>
      <button
        onClick={onClearKey}
        style={{ width: '100%', padding: '8px 12px', background: '#fef2f2', color: '#991b1b', border: '1px solid #fecaca', borderRadius: 8, cursor: 'pointer', fontSize: '0.85rem' }}
      >
        API 키 삭제 (재입력 필요)
      </button>
    </div>
  );
}

function MessageBubble({ msg }) {
  const isUser = msg.role === 'user';
  return (
    <div style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', margin: '8px 0' }}>
      <div style={{
        maxWidth: '85%',
        padding: '10px 14px',
        borderRadius: 14,
        background: isUser ? '#4f46e5' : '#f3f4f6',
        color: isUser ? '#fff' : '#111827',
        fontSize: '0.95rem',
        lineHeight: 1.55,
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word',
      }}>
        {isUser ? msg.content : <ParsedText text={msg.content} />}
      </div>
    </div>
  );
}

function HistoryPanel({ onClose }) {
  const [byDate, setByDate] = useState([]);
  useEffect(() => {
    const map = {};
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (!k || !k.startsWith('ailearn-conversations:')) continue;
        const d = k.split(':')[1];
        const arr = JSON.parse(localStorage.getItem(k) || '[]');
        if (Array.isArray(arr) && arr.length) map[d] = arr.length;
      }
    } catch { /* noop */ }
    setByDate(Object.entries(map).sort((a, b) => b[0].localeCompare(a[0])));
  }, []);
  const [pick, setPick] = useState(null);
  const msgs = pick ? getConversation(pick) : [];
  return (
    <div style={{ padding: 16, background: '#fff', borderRadius: 12, border: '1px solid #e5e7eb' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <h3 style={{ margin: 0, fontSize: '1rem', display: 'flex', alignItems: 'center', gap: 6 }}>
          <Calendar size={18} /> 대화 기록
        </h3>
        <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6b7280' }}>✕</button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '140px 1fr', gap: 12 }}>
        <div style={{ maxHeight: 360, overflowY: 'auto', borderRight: '1px solid #f3f4f6', paddingRight: 8 }}>
          {byDate.length === 0 && <div style={{ fontSize: '0.85rem', color: '#9ca3af', padding: '8px 0' }}>기록 없음</div>}
          {byDate.map(([d, n]) => (
            <button
              key={d}
              onClick={() => setPick(d)}
              style={{
                display: 'block', width: '100%', textAlign: 'left',
                padding: '6px 8px', background: pick === d ? '#eef2ff' : 'transparent',
                border: 'none', borderRadius: 6, marginBottom: 4, cursor: 'pointer',
                fontSize: '0.85rem', color: '#111827',
              }}
            >
              {d} <span style={{ color: '#6b7280' }}>({n})</span>
            </button>
          ))}
        </div>
        <div style={{ maxHeight: 360, overflowY: 'auto' }}>
          {!pick && <div style={{ fontSize: '0.85rem', color: '#9ca3af', padding: '8px 0' }}>날짜 선택</div>}
          {msgs.map((m, i) => <MessageBubble key={i} msg={m} />)}
        </div>
      </div>
    </div>
  );
}

export default function AILearning({ isTabRoot, browseExam }) {
  const [byok, setByokState] = useState(getByok());
  const [prefs, setPrefsState] = useState(getPrefs());
  const [chapters, setChapters] = useState([]);
  const [indexMeta, setIndexMeta] = useState(null);
  const [current, setCurrentState] = useState(getCurrent());
  const [mastery, setMasteryState] = useState(getMastery());
  const [handoverMd, setHandoverMd] = useState('');
  const [unitMd, setUnitMd] = useState('');
  const [sectionMd, setSectionMd] = useState('');
  const [sectionKey, setSectionKey] = useState('full');
  const [problemsMd, setProblemsMd] = useState('');
  const [mode, setMode] = useState('study'); // 'study' | 'practice'
  const [pendingNext, setPendingNext] = useState(null); // AI 제안 다음 토픽
  const [due, setDue] = useState(() => getDueChapters());
  const [messages, setMessages] = useState(() => getConversation(todayStr()));
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const [draft, setDraft] = useState('');
  const [error, setError] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const abortRef = useRef(null);
  const scrollRef = useRef(null);

  // 인덱스 로드
  useEffect(() => {
    fetch(INDEX_URL).then((r) => r.json()).then((idx) => {
      setIndexMeta(idx);
      setChapters(idx.chapters || []);
      if (!current && idx.default_start) {
        const def = idx.chapters.find((c) => c.code === idx.default_start.code) || idx.chapters[0];
        if (def) {
          const next = { subject: 'civil', code: def.code, section_key: idx.default_start.default_section || 'full' };
          setCurrentState(next);
          setCurrent(next);
        }
      }
    }).catch((e) => setError('단원 인덱스를 불러오지 못했습니다: ' + e.message));
    fetch(HANDOVER_URL).then((r) => r.text()).then(setHandoverMd).catch(() => setHandoverMd(''));
    pruneOldConversations(7);
  }, []); // eslint-disable-line

  // 단원 본문 로드
  useEffect(() => {
    if (!current) return;
    const c = chapters.find((x) => x.code === current.code);
    if (!c) return;
    fetch('/data/study/civil/' + c.unit_file).then((r) => r.text()).then((md) => {
      setUnitMd(md);
      const k = current.section_key || 'full';
      const sec = (c.sections || []).find((s) => s.key === k);
      if (sec && sec.key !== 'full') setSectionMd(sliceSection(md, sec));
      else setSectionMd('');
      setSectionKey(k);
    }).catch((e) => setError('단원 자료 로드 실패: ' + e.message));
  }, [current?.code, current?.section_key, chapters]);

  // 문제풀이 모드 진입 시에만 problems MD 로드 (지연 로딩)
  useEffect(() => {
    if (mode !== 'practice' || !current) { setProblemsMd(''); return; }
    const c = chapters.find((x) => x.code === current.code);
    if (!c || !c.problems_file) return;
    fetch('/data/study/civil/' + c.problems_file).then((r) => r.text()).then(setProblemsMd).catch(() => setProblemsMd(''));
  }, [mode, current?.code, chapters]);

  // 자동 스크롤
  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, draft]);

  const pickChapter = (c) => {
    const next = { subject: 'civil', code: c.code, section_key: 'full' };
    setCurrentState(next);
    setCurrent(next);
  };

  const switchSection = (key) => {
    const next = { ...current, section_key: key };
    setCurrentState(next);
    setCurrent(next);
  };

  const startNewSession = () => {
    const id = uid();
    addSession({
      id,
      date: todayStr(),
      code: current?.code,
      section_key: sectionKey,
      started_at: new Date().toISOString(),
      ended_at: null,
      msg_count: 0,
      summary: null,
    });
    setSessionId(id);
  };

  const send = useCallback(async () => {
    setError('');
    const text = input.trim();
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

    const userMsg = { role: 'user', content: text };
    appendMessage(todayStr(), userMsg);
    setMessages((arr) => [...arr, { ...userMsg, ts: new Date().toISOString() }]);
    setInput('');
    setStreaming(true);
    setDraft('');

    const curChapter = chapters.find((c) => c.code === current?.code);
    const curMastery = current ? getChapterMastery(current.code) : null;
    const lastSession = getSessions().slice(-2, -1)[0];
    const recentSummary = lastSession?.summary || '';
    const system = buildSystemBlocks({
      handoverMd,
      unitMd: sectionMd ? '' : unitMd,
      sectionMd,
      problemsMd: mode === 'practice' ? problemsMd : '',
      mode,
      currentMastery: curMastery,
      recentSummary,
    });

    // 컨텍스트: 오늘 대화만 (날짜 경계로 분리). MVP: 최근 12 turn.
    const history = [...getConversation(todayStr())].slice(-13);
    const apiMessages = history.map((m) => ({ role: m.role, content: m.content }));

    const ac = new AbortController();
    abortRef.current = ac;
    try {
      const { text: out, usage } = await sendMessages({
        apiKey: byok,
        model: prefs.model,
        system,
        messages: apiMessages,
        maxTokens: 2048,
        signal: ac.signal,
        onDelta: (_chunk, agg) => setDraft(agg),
      });
      const aMsg = { role: 'assistant', content: out };
      appendMessage(todayStr(), aMsg);
      setMessages((arr) => [...arr, { ...aMsg, ts: new Date().toISOString() }]);
      bumpUsage({
        messages: 1,
        input_tokens: (usage.input_tokens || 0) + (usage.cache_read_input_tokens || 0) + (usage.cache_creation_input_tokens || 0),
        output_tokens: usage.output_tokens || 0,
      });
      // 응답에서 JSON 자동 추출 — 채점 / 세션 정리 양쪽 처리
      const blocks = extractJsonBlocks(out);
      let coverageBumped = false;
      blocks.forEach((b) => {
        if (b && typeof b.correct === 'boolean' && current) {
          const code = b.code || current.code;
          recordGrade(code, b.correct);
        }
        if (b && b.session_summary && current) {
          const delta = Number(b.coverage_delta) || 0.05;
          const prev = getChapterMastery(current.code);
          updateChapterMastery(current.code, {
            coverage: Math.min(1, (prev.coverage || 0) + Math.max(0, Math.min(0.3, delta))),
          });
          coverageBumped = true;
          if (sessionId) updateSession(sessionId, { summary: b.session_summary, ended_at: new Date().toISOString() });
          addAssessment({
            session_id: sessionId,
            code: current.code,
            score: null,
            comments: b.session_summary,
            next_topic: b.next_topic || null,
          });
          if (b.next_topic && b.next_topic.code) setPendingNext(b.next_topic);
        }
      });
      if (!coverageBumped && curChapter && current) {
        // 가벼운 진척 가산 (한 턴 기준)
        const m = getChapterMastery(current.code);
        updateChapterMastery(current.code, {
          coverage: Math.min(1, (m.coverage || 0) + 0.01),
        });
      }
      setMasteryState(getMastery());
      setDue(getDueChapters());
      if (sessionId) {
        updateSession(sessionId, { msg_count: history.length + 1 });
      }
    } catch (e) {
      if (e.name !== 'AbortError') setError('Claude 호출 실패: ' + e.message);
    } finally {
      setStreaming(false);
      setDraft('');
      abortRef.current = null;
    }
  }, [input, streaming, byok, prefs.model, prefs.daily_cap, current, chapters, handoverMd, unitMd, sectionMd, sessionId]);

  const stop = () => { if (abortRef.current) abortRef.current.abort(); };

  // ── 렌더 ──────────────────────────────────────────────
  const curChapter = chapters.find((c) => c.code === current?.code);
  const curSec = curChapter?.sections?.find((s) => s.key === sectionKey);
  const cap = canSendMessage();

  if (!byok) {
    return (
      <div className="app-shell" style={{ padding: 16, paddingBottom: 80 }}>
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', padding: '8px 0', marginBottom: 16 }}>
          <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: 8, color: '#111827' }}>
            <Sparkles size={20} color="#4f46e5" /> AI 학습
          </h2>
        </header>
        <ApiKeyForm initial="" onSave={(k) => { setByok(k); setByokState(k); }} />
      </div>
    );
  }

  return (
    <div className="app-shell" style={{ paddingBottom: 80, display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', padding: '8px 12px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2 style={{ margin: 0, fontSize: '1.05rem', display: 'flex', alignItems: 'center', gap: 6, color: '#111827' }}>
          <Sparkles size={18} color="#4f46e5" /> AI 학습 · 민법
        </h2>
        <div style={{ display: 'flex', gap: 4 }}>
          <button onClick={() => setShowHistory((v) => !v)} title="기록" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 6 }}>
            <Calendar size={18} color={showHistory ? '#4f46e5' : '#6b7280'} />
          </button>
          <button onClick={() => setShowSettings((v) => !v)} title="설정" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 6 }}>
            <SettingsIcon size={18} color={showSettings ? '#4f46e5' : '#6b7280'} />
          </button>
        </div>
      </header>

      {due.length > 0 && (
        <div style={{
          padding: '6px 12px', background: '#fef3c7', borderBottom: '1px solid #fcd34d',
          fontSize: '0.78rem', color: '#92400e', display: 'flex', alignItems: 'center', gap: 6,
        }}>
          <RotateCcw size={14} />
          복습 만기 {due.length}단원: {due.map((d) => d.code).join(', ')}
        </div>
      )}
      <div style={{ padding: '8px 12px', borderBottom: '1px solid #e5e7eb', background: '#f9fafb' }}>
        <div style={{ display: 'flex', gap: 4, marginBottom: 8 }}>
          {[['study', '📖 이론'], ['practice', '✏️ 문제풀이']].map(([k, label]) => (
            <button
              key={k}
              onClick={() => setMode(k)}
              style={{
                flex: 1, padding: '6px 10px', borderRadius: 8,
                border: mode === k ? '1.5px solid #4f46e5' : '1px solid #d1d5db',
                background: mode === k ? '#eef2ff' : '#fff',
                color: mode === k ? '#1d4ed8' : '#374151',
                fontWeight: 700, fontSize: '0.85rem', cursor: 'pointer',
              }}
            >
              {label}
            </button>
          ))}
        </div>
        <ChapterPicker chapters={chapters} current={current} onPick={pickChapter} mastery={mastery} />
        {curChapter && curChapter.sections && curChapter.sections.length > 1 && (
          <div style={{ display: 'flex', gap: 4, overflowX: 'auto', marginTop: 8, paddingBottom: 4 }}>
            {curChapter.sections.map((s) => (
              <button
                key={s.key}
                onClick={() => switchSection(s.key)}
                style={{
                  flex: '0 0 auto', padding: '4px 10px', borderRadius: 14,
                  border: sectionKey === s.key ? '1.5px solid #4f46e5' : '1px solid #d1d5db',
                  background: sectionKey === s.key ? '#eef2ff' : '#fff',
                  color: sectionKey === s.key ? '#1d4ed8' : '#374151',
                  fontSize: '0.78rem', fontWeight: 600, cursor: 'pointer', whiteSpace: 'nowrap',
                }}
              >
                {s.name}
              </button>
            ))}
          </div>
        )}
      </div>

      {showSettings && (
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <SettingsPanel
            prefs={prefs}
            usage={getUsage()}
            onSave={(patch) => { const next = setPrefs(patch); setPrefsState(next); }}
            onClearKey={() => { setByok(null); setByokState(''); }}
          />
        </div>
      )}

      {showHistory && (
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <HistoryPanel onClose={() => setShowHistory(false)} />
        </div>
      )}

      <div ref={scrollRef} style={{ flex: 1, overflowY: 'auto', padding: '12px 14px' }}>
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: '#6b7280', marginTop: 40 }}>
            <BookOpen size={40} style={{ opacity: 0.4 }} />
            <p style={{ marginTop: 12, fontSize: '0.95rem' }}>
              {curChapter ? `${curChapter.code} · ${curChapter.title} 학습을 시작하세요` : '단원을 선택하세요'}
            </p>
            <p style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
              "이어서 진행해줘" / "오늘 복습할게" / "{curChapter?.title} 시작하자" 등으로 대화
            </p>
          </div>
        )}
        {messages.map((m, i) => <MessageBubble key={i} msg={m} />)}
        {streaming && draft && (
          <MessageBubble msg={{ role: 'assistant', content: draft }} />
        )}
        {streaming && !draft && (
          <div style={{ padding: 12, color: '#6b7280', fontSize: '0.85rem' }}>생각하는 중…</div>
        )}
        {error && (
          <div style={{ background: '#fef2f2', color: '#991b1b', padding: 10, borderRadius: 8, fontSize: '0.85rem', marginTop: 10, border: '1px solid #fecaca' }}>
            {error}
          </div>
        )}
        {pendingNext && (
          <div style={{
            background: '#eef2ff', color: '#1e40af', padding: 12, borderRadius: 10,
            marginTop: 10, border: '1px solid #c7d2fe',
          }}>
            <div style={{ fontWeight: 700, marginBottom: 4 }}>
              📌 다음 추천: {pendingNext.code} · {chapters.find((c) => c.code === pendingNext.code)?.title || '(단원)'}
            </div>
            {pendingNext.reason && <div style={{ fontSize: '0.85rem', marginBottom: 8 }}>{pendingNext.reason}</div>}
            <div style={{ display: 'flex', gap: 6 }}>
              <button
                onClick={() => {
                  const next = { subject: 'civil', code: pendingNext.code, section_key: pendingNext.section_key || 'full' };
                  setCurrentState(next); setCurrent(next); setPendingNext(null);
                }}
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
        <div style={{ display: 'flex', gap: 6, alignItems: 'flex-end' }}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
            }}
            placeholder={cap.ok ? '메시지를 입력하세요 (Enter 전송, Shift+Enter 줄바꿈)' : '오늘 cap 도달'}
            disabled={!cap.ok || streaming}
            rows={2}
            style={{
              flex: 1, padding: '10px 12px', border: '1px solid #d1d5db', borderRadius: 10,
              fontSize: '0.95rem', resize: 'none', fontFamily: 'inherit',
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
              disabled={!input.trim() || !cap.ok}
              style={{
                padding: '10px 14px',
                background: input.trim() && cap.ok ? '#4f46e5' : '#e5e7eb',
                color: input.trim() && cap.ok ? '#fff' : '#9ca3af',
                border: 'none', borderRadius: 10, cursor: input.trim() && cap.ok ? 'pointer' : 'not-allowed',
                display: 'flex', alignItems: 'center', gap: 4, fontWeight: 700,
              }}
            >
              <Send size={16} />
            </button>
          )}
        </div>
        <div style={{ marginTop: 6, fontSize: '0.72rem', color: '#9ca3af', display: 'flex', justifyContent: 'space-between' }}>
          <span>모델: {prefs.model.replace('claude-', '')}</span>
          <span>
            오늘 {(getUsage()[todayStr()]?.messages || 0)} / {prefs.daily_cap || '∞'} 메시지
          </span>
        </div>
      </div>
    </div>
  );
}
