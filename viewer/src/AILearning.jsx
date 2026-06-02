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

import { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { Send, Settings as SettingsIcon, BookOpen, RotateCcw, ChevronDown, ChevronLeft, ChevronRight, Calendar, Sparkles, Key, Search, Trash2, Play, BarChart3, ArrowRight } from 'lucide-react';
import ParsedText from './ParsedText';
import {
  getByok, setByok, getPrefs, setPrefs,
  getCurrent, setCurrent,
  getMastery, getChapterMastery, updateChapterMastery,
  recordGrade, recordAnswerScore, getDueChapters,
  getSessions, addSession, updateSession,
  getRoomMessages, appendRoomMessage, clearRoom, getAllRooms,
  bumpUsage, canSendMessage, getUsage,
  pruneOldConversations,
  addAssessment,
  resetLearningProgress,
  migrateLegacyCivilIds,
  addMock, getMocks,
  SUBJECTS, SUBJECTS_BY_STAGE, getSubjectMeta,
} from './aiLearningStore';
import { sendMessages, buildSystemBlocks, sliceSection, extractJsonBlocks, MODELS } from './aiClaudeClient';

const indexUrl = (subjectId) => {
  const s = SUBJECTS.find((x) => x.id === subjectId);
  if (s?.stage === 2) return `/data/study/${subjectId}/ai_index.json`;
  return `/data/study/${subjectId}/ai_taxonomy_index.json`;
};
const handoverUrl = (subjectId) => `/data/study/${subjectId}/handover.md`;
const studyBase = (subjectId) => `/data/study/${subjectId}/`;

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

function SettingsPanel({ prefs, onSave, onClearKey, onResetProgress, usage }) {
  const today = usage[todayStr()] || { messages: 0, input_tokens: 0, cache_read: 0, cache_write: 0, output_tokens: 0 };
  const cacheTotal = (today.cache_read || 0) + (today.cache_write || 0);
  const cacheHit = cacheTotal > 0 ? Math.round(((today.cache_read || 0) / cacheTotal) * 100) : 0;
  return (
    <div style={{ padding: 16, background: '#fff', borderRadius: 12, border: '1px solid #e5e7eb' }}>
      <h3 style={{ margin: '0 0 12px 0', fontSize: '1rem' }}>설정</h3>
      <label style={{ display: 'block', fontSize: '0.85rem', color: '#374151', marginBottom: 4 }}>모델</label>
      <select
        value={prefs.model}
        onChange={(e) => onSave({ model: e.target.value })}
        style={{ width: '100%', padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.9rem', marginBottom: 12 }}
      >
        <option value={MODELS.primary}>Sonnet 4.6 (균형)</option>
        <option value={MODELS.fast}>Haiku 4.5 (빠름·저렴 ⚡)</option>
        <option value={MODELS.premium}>Opus 4.7 (최고품질·비쌈)</option>
      </select>
      <label style={{ display: 'block', fontSize: '0.85rem', color: '#374151', marginBottom: 4 }}>
        응답 길이 상한 (max_tokens) — 줄이면 더 빠른 응답
      </label>
      <select
        value={prefs.max_tokens || 1200}
        onChange={(e) => onSave({ max_tokens: parseInt(e.target.value, 10) })}
        style={{ width: '100%', padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.9rem', marginBottom: 12 }}
      >
        <option value={600}>600 (짧고 빠름)</option>
        <option value={1200}>1200 (권장)</option>
        <option value={2000}>2000 (길게 설명)</option>
        <option value={3000}>3000 (종합 퀴즈용)</option>
      </select>
      <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.85rem', color: '#374151', marginBottom: 12, cursor: 'pointer' }}>
        <input
          type="checkbox"
          checked={!!prefs.streaming}
          onChange={(e) => onSave({ streaming: e.target.checked })}
        />
        응답 스트리밍 (토큰별 흐름) — 끄면 완성 후 한 번에 표시(권장)
      </label>
      <label style={{ display: 'block', fontSize: '0.85rem', color: '#374151', marginBottom: 4 }}>일일 메시지 cap</label>
      <input
        type="number"
        min={0}
        max={500}
        value={prefs.daily_cap}
        onChange={(e) => onSave({ daily_cap: parseInt(e.target.value, 10) || 0 })}
        style={{ width: '100%', padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.9rem', marginBottom: 4 }}
      />
      <div style={{ fontSize: '0.78rem', color: '#6b7280', marginBottom: 6 }}>
        오늘: {today.messages}회 · 입력 {(today.input_tokens || 0).toLocaleString()} · 출력 {(today.output_tokens || 0).toLocaleString()} 토큰
      </div>
      <div style={{ fontSize: '0.78rem', color: cacheHit >= 70 ? '#047857' : '#92400e', marginBottom: 12 }}>
        캐시 적중률 {cacheHit}% (읽기 {(today.cache_read || 0).toLocaleString()} / 쓰기 {(today.cache_write || 0).toLocaleString()})
        {cacheHit < 50 && cacheTotal > 0 && ' · 5분 안에 다음 질문 보내면 캐시 적중률이 올라갑니다'}
      </div>
      <button
        onClick={onResetProgress}
        style={{ width: '100%', padding: '8px 12px', background: '#fef3c7', color: '#92400e', border: '1px solid #fcd34d', borderRadius: 8, cursor: 'pointer', fontSize: '0.85rem', marginBottom: 6 }}
      >
        🧹 학습 진척 초기화 (대화·세션·진척도 삭제, 키·설정 보존)
      </button>
      <button
        onClick={onClearKey}
        style={{ width: '100%', padding: '8px 12px', background: '#fef2f2', color: '#991b1b', border: '1px solid #fecaca', borderRadius: 8, cursor: 'pointer', fontSize: '0.85rem' }}
      >
        API 키 삭제 (재입력 필요)
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
                    {st.s.icon} {st.s.short}
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
      {(result.strengths?.length || result.missed?.length) && (
        <div style={{ marginTop: 10, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
          {result.strengths?.length > 0 && (
            <div>
              <div style={{ fontSize: '0.74rem', fontWeight: 700, color: '#047857', marginBottom: 4 }}>✅ 강점</div>
              {result.strengths.map((s, i) => <div key={i} style={{ fontSize: '0.72rem', color: '#374151' }}>· {s}</div>)}
            </div>
          )}
          {result.missed?.length > 0 && (
            <div>
              <div style={{ fontSize: '0.74rem', fontWeight: 700, color: '#9a3412', marginBottom: 4 }}>⚠️ 보강</div>
              {result.missed.map((m, i) => <div key={i} style={{ fontSize: '0.72rem', color: '#374151' }}>· {m}</div>)}
            </div>
          )}
        </div>
      )}
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

function MessageBubble({ msg, fadeIn }) {
  const isUser = msg.role === 'user';
  return (
    <div className={fadeIn ? 'ai-msg-fade' : ''} style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', margin: '8px 0' }}>
      <div style={{
        // AI 메시지는 거의 전체 폭(98%), 사용자 메시지는 75% — 대비 + 읽기 편의
        maxWidth: isUser ? '78%' : '98%',
        padding: '12px 16px',
        borderRadius: 14,
        background: isUser ? '#4f46e5' : '#f3f4f6',
        color: isUser ? '#fff' : '#111827',
        fontSize: '0.95rem',
        lineHeight: 1.6,
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word',
      }}>
        {isUser ? msg.content : <ParsedText text={msg.content} />}
      </div>
    </div>
  );
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

export default function AILearning({ isTabRoot, browseExam, weakPaths, weakPathsBySubject, leavesBySubject: leavesBySubjectProp, onJumpToBrowse, getQuizCountForLeaf, quizStatsByLeaf }) {
  useEffect(() => { migrateLegacyCivilIds(); }, []);
  const [byok, setByokState] = useState(getByok());
  const [prefs, setPrefsState] = useState(getPrefs());
  const [indexMeta, setIndexMeta] = useState(null);
  const [leaves, setLeaves] = useState([]);
  const initCur = getCurrent();
  const [subjectId, setSubjectId] = useState(initCur?.subject || 'civil');
  const [current, setCurrentState] = useState(initCur);
  // 자체 홈 화면 ↔ 학습 화면. 매 진입 시 홈으로 시작.
  const [aiView, setAiView] = useState('home'); // 'home' | 'study'
  const [mastery, setMasteryState] = useState(getMastery());
  const [handoverMd, setHandoverMd] = useState('');
  const [unitMd, setUnitMd] = useState('');
  const [sectionMd, setSectionMd] = useState('');
  const [problemsMd, setProblemsMd] = useState('');
  const [mode, setMode] = useState('study'); // 'study' | 'practice' | 'deep' | 'summary' | 'diagnose'
  const [pendingNext, setPendingNext] = useState(null);
  const [due, setDue] = useState(() => getDueChapters());
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const [draft, setDraft] = useState('');
  const [error, setError] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showAnalytics, setShowAnalytics] = useState(false);
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
  const [sessionId, setSessionId] = useState(null);
  const [idlePromptShown, setIdlePromptShown] = useState(false);
  const [weakSuggestion, setWeakSuggestion] = useState([]);
  const [confirmAction, setConfirmAction] = useState(null); // {label, onYes}
  const [recentRooms, setRecentRooms] = useState(() => getAllRooms());
  // 헤더 단원 박스 클릭 → LeafPicker 모달
  const [showLeafPickerModal, setShowLeafPickerModal] = useState(false);
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
  const idleTimerRef = useRef(null);

  // 인덱스·인수인계서 로드 — subjectId 변경 시 재로드
  useEffect(() => {
    fetch(indexUrl(subjectId)).then((r) => r.json()).then((raw) => {
      const idx = raw?.stage === 2 ? normalizeStage2Index(raw) : raw;
      setIndexMeta(idx);
      setLeaves(idx.leaves || []);
      const exists = current?.leaf_id && (idx.leaves || []).some((l) => l.id === current.leaf_id);
      if (!exists && idx.default_leaf) {
        const def = idx.leaves.find((l) => l.id === idx.default_leaf) || idx.leaves[0];
        if (def) {
          const next = { subject: subjectId, leaf_id: def.id };
          setCurrentState(next);
          setCurrent(next);
        }
      }
    }).catch((e) => setError('단원 인덱스를 불러오지 못했습니다: ' + e.message));
    fetch(handoverUrl(subjectId)).then((r) => r.text()).then(setHandoverMd).catch(() => setHandoverMd(''));
    pruneOldConversations(7);
  }, [subjectId]); // eslint-disable-line

  // leaf 자료 로드 (section_lines 슬라이스)
  useEffect(() => {
    if (!current?.leaf_id || leaves.length === 0) return;
    const leaf = leaves.find((l) => l.id === current.leaf_id);
    if (!leaf || !leaf.unit_file) { setUnitMd(''); setSectionMd(''); return; }
    fetch(studyBase(subjectId) + leaf.unit_file).then((r) => r.text()).then((md) => {
      setUnitMd(md);
      if (leaf.section_key && leaf.section_key !== 'full' && leaf.section_lines) {
        setSectionMd(sliceSection(md, { lines: leaf.section_lines }));
      } else {
        setSectionMd('');
      }
    }).catch((e) => setError('단원 자료 로드 실패: ' + e.message));
  }, [current?.leaf_id, leaves, subjectId]);

  // 문제·기출 자료 로드 — 1차 practice, 2차 answer_write / mock_full / topic_extract 모드에서
  useEffect(() => {
    const needs = mode === 'practice' || mode === 'answer_write' || mode === 'mock_full' || mode === 'topic_extract';
    if (!needs || !current?.leaf_id) { setProblemsMd(''); return; }
    const leaf = leaves.find((l) => l.id === current.leaf_id);
    if (!leaf || !leaf.problems_file) { setProblemsMd(''); return; }
    fetch(studyBase(subjectId) + leaf.problems_file).then((r) => r.text()).then(setProblemsMd).catch(() => setProblemsMd(''));
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
    if (!current?.leaf_id) { setMessages([]); return; }
    setMessages(getRoomMessages(current.leaf_id));
    setPendingNext(null);
    setIdlePromptShown(false);
    setInput('');
    if (abortRef.current) abortRef.current.abort();
    if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
  }, [current?.leaf_id]);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, draft]);

  // 메시지 변동 시 최근 방 목록 갱신
  useEffect(() => { setRecentRooms(getAllRooms()); }, [messages]);

  // 이전/다음 leaf 계산 (taxonomy index 순)
  const curIndex = leaves.findIndex((l) => l.id === current?.leaf_id);
  const prevLeaf = curIndex > 0 ? leaves[curIndex - 1] : null;
  const nextLeaf = curIndex >= 0 && curIndex < leaves.length - 1 ? leaves[curIndex + 1] : null;

  // 메시지 1건 이상 쌓인 방만, 현재 leaf 제외, 상위 6개
  const recentChips = useMemo(() => {
    return recentRooms
      .filter((r) => r.leafId !== current?.leaf_id)
      .slice(0, 6)
      .map((r) => ({ ...r, leaf: leaves.find((l) => l.id === r.leafId) }))
      .filter((x) => x.leaf);
  }, [recentRooms, leaves, current?.leaf_id]);

  // 취약 leaf 매칭 — 과목별 dict 우선, 단일 props weakPaths fallback
  useEffect(() => {
    if (!leaves.length) return;
    const src = (weakPathsBySubject && weakPathsBySubject[subjectId]) || weakPaths || [];
    const matched = matchWeakLeaves(src, leaves);
    setWeakSuggestion(matched);
  }, [leaves, weakPaths, weakPathsBySubject, subjectId]);

  // 과목 전환 헬퍼
  const switchSubject = (sid, enterStudy = false) => {
    if (sid === subjectId && !enterStudy) return;
    if (abortRef.current) abortRef.current.abort();
    setSubjectId(sid);
    setMessages([]);
    setUnitMd(''); setSectionMd(''); setProblemsMd('');
    setPendingNext(null); setIdlePromptShown(false); setInput('');
    // stage 전환 시 적합한 default 모드로
    const nextStage = SUBJECTS.find((s) => s.id === sid)?.stage || 1;
    const stage1Modes = ['study', 'practice', 'deep', 'summary', 'diagnose'];
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

  const pickLeaf = (leaf) => {
    const next = { subject: 'civil', leaf_id: leaf.id };
    setCurrentState(next);
    setCurrent(next);
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

  const send = useCallback(async (overrideText) => {
    setError('');
    const text = (typeof overrideText === 'string' ? overrideText : input).trim();
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
    const userMsg = { role: 'user', content: text };
    appendRoomMessage(current.leaf_id, userMsg);
    setMessages((arr) => [...arr, { ...userMsg, ts: new Date().toISOString() }]);
    if (typeof overrideText !== 'string') setInput('');
    setStreaming(true);
    setDraft('');

    const curLeaf = leaves.find((l) => l.id === current?.leaf_id);
    const curMastery = current ? getChapterMastery(current.leaf_id) : null;
    const lastSession = getSessions().slice(-2, -1)[0];
    const recentSummary = lastSession?.summary || '';
    const subjStage = getSubjectMeta(subjectId)?.stage || 1;
    const usesProblems = (subjStage === 1 && mode === 'practice') ||
                         (subjStage === 2 && (mode === 'answer_write' || mode === 'mock_full' || mode === 'topic_extract' || mode === 'template'));
    const system = buildSystemBlocks({
      handoverMd,                            // ← 캐시 안정: 텍스트 불변
      unitMd: sectionMd ? '' : unitMd,
      sectionMd,
      problemsMd: usesProblems ? problemsMd : '',
      mode,
      currentMastery: curMastery,
      recentSummary,
      leafPath: curLeaf ? curLeaf.path.join(' / ') : '',
      stage: subjStage,
      subjectId,
    });

    const history = [...getRoomMessages(current.leaf_id)].slice(-13);
    const apiMessages = history.map((m) => ({ role: m.role, content: m.content }));

    const ac = new AbortController();
    abortRef.current = ac;
    try {
      // 기본: 비-스트리밍(한 번에 받기) — 매 chunk 마다 KaTeX/표 재파싱으로 인한 프레임 드롭 회피.
      // prefs.streaming === true 일 때만 토큰별 흐름 표시.
      const useStream = !!prefs.streaming;
      // 모드별 최대 출력 토큰 — summary/diagnose는 짧게, deep는 길게
      const modeMaxTokens = { summary: 600, diagnose: 900, deep: 1800, practice: 1500, study: 1200 };
      const effectiveMax = prefs.max_tokens || modeMaxTokens[mode] || 1200;
      const { text: out, usage } = await sendMessages({
        apiKey: byok,
        model: prefs.model,
        system,
        messages: apiMessages,
        maxTokens: effectiveMax,
        signal: ac.signal,
        onDelta: useStream ? ((_chunk, agg) => setDraft(agg)) : undefined,
      });
      const aMsg = { role: 'assistant', content: out };
      appendRoomMessage(current.leaf_id, aMsg);
      setMessages((arr) => [...arr, { ...aMsg, ts: new Date().toISOString() }]);
      bumpUsage({
        messages: 1,
        input_tokens: usage.input_tokens || 0,
        cache_read: usage.cache_read_input_tokens || 0,
        cache_write: usage.cache_creation_input_tokens || 0,
        output_tokens: usage.output_tokens || 0,
      });
      const blocks = extractJsonBlocks(out);
      let coverageBumped = false;
      blocks.forEach((b) => {
        if (b && typeof b.correct === 'boolean' && current) {
          recordGrade(current.leaf_id, b.correct);
        }
        // 2차 답안 채점 결과
        if (b && b.graded === true && b.stage === 2 && typeof b.score === 'number' && current) {
          recordAnswerScore(current.leaf_id, {
            score: b.score,
            max: b.max || 30,
            time_used_min: b.time_used_min || 0,
            time_target_min: b.time_target_min || (b.max || 30),
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
          const prev = getChapterMastery(current.leaf_id);
          updateChapterMastery(current.leaf_id, {
            coverage: Math.min(1, (prev.coverage || 0) + Math.max(0, Math.min(0.3, delta))),
          });
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
        const m = getChapterMastery(current.leaf_id);
        updateChapterMastery(current.leaf_id, {
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
      armIdleTimer();
    }
  }, [input, streaming, byok, prefs.model, prefs.daily_cap, prefs.max_tokens, current, leaves, handoverMd, unitMd, sectionMd, problemsMd, mode, sessionId, clearIdleTimer, armIdleTimer]);

  const stop = () => { if (abortRef.current) abortRef.current.abort(); };

  // 빠른 액션: input을 거치지 않고 즉시 send (overrideText 사용)
  const quickSend = (text) => { if (!streaming) send(text); };

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
    setShowSettings(false);
    setShowHistory(false);
    setShowAnalytics(false);
    if (typeof window !== 'undefined' && window.alert) {
      window.alert('✅ 학습 진척이 초기화되었습니다.');
    }
  }, [indexMeta, subjectId]);

  const curLeaf = leaves.find((l) => l.id === current?.leaf_id);
  const cap = canSendMessage();

  if (!byok) {
    return (
      <div style={{ padding: 16 }}>
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
    aiView === 'home' ? (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 64px - env(safe-area-inset-bottom, 0px))', maxWidth: 960, margin: '0 auto', width: '100%' }}>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', padding: '8px 12px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2 style={{ margin: 0, fontSize: '1.05rem', display: 'flex', alignItems: 'center', gap: 6, color: '#111827' }}>
          <Sparkles size={20} color="#4f46e5" /> AI 학습
        </h2>
        <div style={{ display: 'flex', gap: 2 }}>
          <button onClick={() => setShowAnalytics((v) => !v)} title="분석" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 6 }}>
            <BarChart3 size={18} color={showAnalytics ? '#4f46e5' : '#6b7280'} />
          </button>
          <button onClick={() => setShowHistory((v) => !v)} title="단원별 채팅방" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 6 }}>
            <Calendar size={18} color={showHistory ? '#4f46e5' : '#6b7280'} />
          </button>
          <button onClick={() => setShowSettings((v) => !v)} title="설정" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 6 }}>
            <SettingsIcon size={18} color={showSettings ? '#4f46e5' : '#6b7280'} />
          </button>
        </div>
      </header>
      {showSettings && (
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <SettingsPanel
            prefs={prefs}
            usage={getUsage()}
            onSave={(patch) => { const next = setPrefs(patch); setPrefsState(next); }}
            onClearKey={() => { setByok(null); setByokState(''); }}
            onResetProgress={doResetProgress}
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
              setTimeout(() => pickLeaf(leaf), 50);
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
              setTimeout(() => pickLeaf(leaf), 50);
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
              style={{ padding: '6px 14px', fontSize: '0.85rem', fontWeight: 700, background: confirmAction.danger ? '#dc2626' : '#4f46e5', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
              네
            </button>
            <button onClick={() => setConfirmAction(null)}
              style={{ padding: '6px 14px', fontSize: '0.85rem', background: '#fff', color: '#374151', border: '1px solid #d1d5db', borderRadius: 6, cursor: 'pointer' }}>
              취소
            </button>
          </div>
        </div>
      )}
      <div style={{ flex: 1, overflowY: 'auto', padding: '14px 14px 30px' }}>
        {/* 이어서 학습 카드 */}
        {curLeaf && messages.length > 0 && (() => {
          const m = mastery[curLeaf.id] || {};
          const sMeta = getSubjectMeta(subjectId);
          return (
            <button
              onClick={() => setAiView('study')}
              style={{
                width: '100%', textAlign: 'left', padding: 14,
                background: `linear-gradient(135deg, ${sMeta.color}15 0%, #fff 100%)`,
                border: `1.5px solid ${sMeta.color}`,
                borderRadius: 14, cursor: 'pointer', marginBottom: 16,
              }}
            >
              <div style={{ fontSize: '0.72rem', color: sMeta.color, fontWeight: 700, marginBottom: 4 }}>
                ▶️ 이어서 학습 — {sMeta.icon} {sMeta.short}
              </div>
              <div style={{ fontSize: '1rem', fontWeight: 800, color: '#111827' }}>
                {curLeaf.path.slice(-1)[0]}
              </div>
              <div style={{ fontSize: '0.78rem', color: '#6b7280', marginTop: 2 }}>
                {curLeaf.path.slice(0, -1).join(' › ')}
              </div>
              <div style={{ fontSize: '0.72rem', color: '#374151', marginTop: 6 }}>
                {messages.length}건 · 진척 {Math.round((m.coverage || 0) * 100)}%
              </div>
            </button>
          );
        })()}

        {/* 1차 / 2차 섹션 분리 그리드 */}
        {[
          { stage: 1, label: '1차 시험 — 객관식 5지선다', subjects: SUBJECTS_BY_STAGE[1] },
          { stage: 2, label: '2차 시험 — 서술형·답안 작성', subjects: SUBJECTS_BY_STAGE[2] },
        ].map(({ stage, label, subjects }) => (
          <div key={stage} style={{ marginBottom: 18 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
              <div style={{ fontSize: '1rem', color: '#111827', fontWeight: 800 }}>
                {stage === 1 ? '📖' : '✍️'} {label}
              </div>
              <span style={{ fontSize: '0.82rem', color: '#1f2937', fontWeight: 600 }}>{subjects.length}과목</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: 10 }}>
              {subjects.map((s) => {
                // stage1: ailearn-mastery 키가 'civil__...' prefix
                // stage2: 단원 id가 'appraisal_practice_1' 형태
                const ks = Object.keys(mastery).filter((k) => k.startsWith(s.id + '__') || k.startsWith(s.id + '_'));
                const covAvg = ks.length ? ks.reduce((a, k) => a + (mastery[k]?.coverage || 0), 0) / ks.length : 0;
                const masterN = ks.filter((k) => mastery[k]?.status === 'mastered').length;
                const dueN = (due || []).filter((d) => (d.code || '').startsWith(s.id + '__') || (d.code || '').startsWith(s.id + '_')).length;
                const weakN = ((weakPathsBySubject || {})[s.id] || []).length;
                const pct = Math.round(covAvg * 100);
                const isStage2 = s.stage === 2;
                return (
                  <button
                    key={s.id}
                    onClick={() => switchSubject(s.id, true)}
                    style={{
                      padding: 16, textAlign: 'left',
                      background: 'linear-gradient(160deg, #eff6ff 0%, #ffffff 100%)',
                      border: '1px solid #c7d2fe', borderRadius: 12, cursor: 'pointer',
                      display: 'flex', flexDirection: 'column', gap: 6, position: 'relative',
                    }}
                  >
                    {isStage2 && (
                      <span style={{ position: 'absolute', top: 10, right: 10, fontSize: '0.7rem', fontWeight: 800,
                        background: '#4f46e5', color: '#fff', padding: '3px 8px', borderRadius: 999 }}>2차</span>
                    )}
                    <div style={{ fontSize: '1.8rem', lineHeight: 1 }}>{s.icon}</div>
                    <div style={{ fontWeight: 800, color: '#1e3a8a', fontSize: '1.1rem' }}>{s.short}</div>
                    <div style={{ fontSize: '0.82rem', color: '#1f2937', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{s.title}</div>
                    <div style={{ marginTop: 8, height: 5, background: '#dbeafe', borderRadius: 3, overflow: 'hidden' }}>
                      <div style={{ width: `${Math.max(2, pct)}%`, height: '100%', background: '#4f46e5' }} />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.88rem', color: '#111827', marginTop: 4 }}>
                      <span style={{ fontWeight: 800 }}>{pct}%</span>
                      <span style={{ color: '#1f2937', fontWeight: 600 }}>{isStage2 ? `답안 ${masterN}` : `마스터 ${masterN}`}</span>
                    </div>
                    {(dueN > 0 || weakN > 0) && (
                      <div style={{ marginTop: 2, fontSize: '0.78rem', color: '#92400e', display: 'flex', gap: 6, fontWeight: 700 }}>
                        {dueN > 0 && <span>🔁 {dueN}</span>}
                        {weakN > 0 && <span>⚠️ {weakN}</span>}
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}

        {/* 비어있는 첫 사용자 가이드 */}
        {!curLeaf && Object.keys(mastery).length === 0 && (
          <div style={{ marginTop: 20, padding: 14, background: '#f9fafb', border: '1px dashed #d1d5db', borderRadius: 12, fontSize: '0.85rem', color: '#6b7280', textAlign: 'center' }}>
            과목을 선택하면 단원 트리에서 학습할 곳을 고르고 대화를 시작할 수 있어요
          </div>
        )}
      </div>
    </div>
    ) : (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 64px - env(safe-area-inset-bottom, 0px))', maxWidth: 1100, margin: '0 auto', width: '100%' }}>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', gap: 6, padding: '6px 8px' }}>
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
          style={{ background: 'none', border: 'none', cursor: prevLeaf ? 'pointer' : 'not-allowed', padding: 4, opacity: prevLeaf ? 1 : 0.3 }}
        >
          <ChevronLeft size={20} color="#374151" />
        </button>

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
          style={{ background: 'none', border: 'none', cursor: nextLeaf ? 'pointer' : 'not-allowed', padding: 4, opacity: nextLeaf ? 1 : 0.3 }}
        >
          <ChevronRight size={20} color="#374151" />
        </button>
        {messages.length > 0 && curLeaf && (
          <button
            onClick={() => askConfirm(`"${curLeaf.path.slice(-1)[0]}" 채팅방 초기화 (진척도는 유지)`, true, () => {
              if (abortRef.current) abortRef.current.abort();
              clearRoom(curLeaf.id);
              setMessages([]);
              setPendingNext(null);
              setIdlePromptShown(false);
              setRecentRooms(getAllRooms());
            })}
            title="이 채팅방 초기화"
            style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 4 }}
          >
            <Trash2 size={16} color="#ef4444" />
          </button>
        )}
        <button onClick={() => setShowAnalytics((v) => !v)} title="분석" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 4 }}>
          <BarChart3 size={18} color={showAnalytics ? '#4f46e5' : '#6b7280'} />
        </button>
        <button onClick={() => setShowHistory((v) => !v)} title="단원별 채팅방" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 4 }}>
          <Calendar size={18} color={showHistory ? '#4f46e5' : '#6b7280'} />
        </button>
        <button onClick={() => setShowSettings((v) => !v)} title="설정" style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 4 }}>
          <SettingsIcon size={18} color={showSettings ? '#4f46e5' : '#6b7280'} />
        </button>
      </header>
      {recentChips.length > 0 && (
        <div style={{ padding: '4px 8px', borderBottom: '1px solid #f3f4f6', background: '#fafafa', display: 'flex', gap: 4, overflowX: 'auto' }}>
          <span style={{ fontSize: '0.7rem', color: '#9ca3af', alignSelf: 'center', flex: '0 0 auto', padding: '0 4px' }}>최근:</span>
          {recentChips.map((r) => (
            <button
              key={r.leafId}
              onClick={() => pickLeaf(r.leaf)}
              title={r.leaf.path.join(' › ')}
              style={{
                flex: '0 0 auto', padding: '3px 10px', borderRadius: 12,
                background: '#fff', border: '1px solid #e5e7eb', color: '#374151',
                fontSize: '0.72rem', fontWeight: 600, cursor: 'pointer', whiteSpace: 'nowrap',
              }}
            >
              {r.leaf.path.slice(-1)[0]}
              <span style={{ color: '#9ca3af', marginLeft: 4 }}>{r.msg_count}</span>
            </button>
          ))}
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

      <div style={{ padding: '8px 12px', borderBottom: '1px solid #e5e7eb', background: '#f9fafb' }}>
        <div style={{ display: 'flex', gap: 4, marginBottom: 8, overflowX: 'auto', paddingBottom: 2 }}>
          {(() => {
            const isStage2 = getSubjectMeta(subjectId)?.stage === 2;
            if (!isStage2) {
              return [
                ['study', '📖', '이론', '처음 배움'],
                ['practice', '✏️', '문제풀이', '기출 풀이'],
                ['deep', '🧠', '심화', '판례·함정'],
                ['summary', '⚡', '복습', '핵심 압축'],
                ['diagnose', '🎯', '진단', 'OX 5문제'],
              ];
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
          })().map(([k, icon, label, desc]) => (
            <button
              key={k}
              onClick={() => setMode(k)}
              title={desc}
              style={{
                flex: '0 0 auto', padding: '6px 10px', borderRadius: 8,
                border: mode === k ? '1.5px solid #4f46e5' : '1px solid #d1d5db',
                background: mode === k ? '#eef2ff' : '#fff',
                color: mode === k ? '#1d4ed8' : '#374151',
                fontWeight: 700, fontSize: '0.78rem', cursor: 'pointer',
                display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 56,
                lineHeight: 1.1,
              }}
            >
              <span style={{ fontSize: '1rem' }}>{icon}</span>
              <span style={{ marginTop: 2 }}>{label}</span>
            </button>
          ))}
        </div>
        {/* 단원 자료 없음만 작게 안내 */}
        {curLeaf && !curLeaf.unit_file && (
          <div style={{ marginTop: 6, fontSize: '0.72rem', color: '#dc2626', fontWeight: 600 }}>
            ⚠️ 단원 자료 없음 — 인수인계서만으로 진행
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
            onResetProgress={doResetProgress}
          />
        </div>
      )}

      {/* 단원 picker 모달 — 헤더 박스 클릭 시 */}
      {showLeafPickerModal && (
        <>
          <div onClick={() => setShowLeafPickerModal(false)}
            style={{ position: 'fixed', inset: 0, background: 'rgba(15,23,42,0.45)', zIndex: 150 }} />
          <div style={{
            position: 'fixed', top: '8vh', left: '50%', transform: 'translateX(-50%)',
            width: 'min(560px, 92vw)', maxHeight: '80vh', background: '#fff',
            borderRadius: 14, boxShadow: '0 20px 50px rgba(15,23,42,0.25)',
            display: 'flex', flexDirection: 'column', zIndex: 151,
            animation: 'cmdkIn 0.2s cubic-bezier(0.22, 0.61, 0.36, 1)',
            overflow: 'hidden',
          }}>
            <div style={{ padding: '12px 14px', borderBottom: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ fontWeight: 800, color: '#111827' }}>📂 단원 선택</div>
              <button onClick={() => setShowLeafPickerModal(false)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6b7280', fontSize: '1.1rem' }}>✕</button>
            </div>
            <div style={{ overflowY: 'auto', flex: 1 }}>
              <LeafPicker
                inline
                leaves={leaves}
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
            onJump={(leaf) => { pickLeaf(leaf); setShowHistory(false); }}
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
              setTimeout(() => pickLeaf(leaf), 50);
              setShowAnalytics(false);
            }}
          />
        </div>
      )}

      <div ref={scrollRef} style={{ flex: 1, overflowY: 'auto', padding: '10px 10px 16px' }}>
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
                  onClick={() => { pickLeaf(w.leaf); setWeakSuggestion([]); }}
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
              <MessageBubble msg={m} fadeIn={fadeIn} />
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
            생각하는 중…
          </div>
        )}
        {error && (
          <div style={{ background: '#fef2f2', color: '#991b1b', padding: 10, borderRadius: 8, fontSize: '0.85rem', marginTop: 10, border: '1px solid #fecaca' }}>
            {error}
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
              ['▶️ 이 단원 시작', '이 단원의 첫 절·관부터 한 사이클(일상언어→한자풀이→비유→교재표현→쉬운 OX) 시작해줘.'],
              ['🔁 이어서 진행', '직전에 멈춘 곳에서 자연스럽게 이어서 진행해줘.'],
              ['❓ 더 쉽게', '방금 설명한 거 더 쉽게 일상 비유로 다시 풀어줘.'],
              ['🏁 오늘 끝 — 정리', '오늘 학습 정리해줘. 끝.'],
            ],
            practice: [
              ['📝 기출 한 문제', '기출 한 문제 출제해줘. 함정 분석도 같이.'],
              ['🔄 다른 문제', '같은 주제로 다른 기출 문제 한 개 더.'],
              ['💡 정답·해설', '방금 문제 정답과 해설을 자세히 알려줘.'],
            ],
            deep: [
              ['🧠 더 깊게', '이 개념을 더 깊게 — 통설·소수설·관련 판례 정리해줘.'],
              ['⚠️ 함정 분석', '이 단원의 시험 단골 함정 3개 표로 정리해줘.'],
              ['🔀 유사 개념 비교', '헷갈리는 유사 개념과 비교표로 정리해줘.'],
            ],
            summary: [
              ['⚡ 핵심 카드', '이 단원 핵심을 압축 카드 한 장으로(정의·키워드·암기 두문자·빈출 포인트).'],
              ['📌 다음 카드', '다음 절·관 핵심 카드로 넘어가줘.'],
              ['🔢 빈출 5', '이 단원에서 시험 빈출 5개만 짧게 정리.'],
            ],
            diagnose: [
              ['🎯 진단 시작', '이 단원 핵심 5문제 OX/단답을 한꺼번에 내줘. 답은 한 메시지로 적을게.'],
              ['🩺 약점만 다시', '방금 진단에서 틀린 부분만 다시 친절히 가르쳐줘.'],
              ['📊 종합 진단', '진단 결과 표로 정리하고 다음 학습 단원 추천.'],
            ],
            // 2차
            concept_s2: [
              ['▶️ 논점 도입', '이 단원의 첫 논점부터 답안에 어떻게 쓸지 같이 가르쳐줘.'],
              ['📋 답안 골격', '이 논점의 답안 골격(Ⅰ·Ⅱ·Ⅲ)을 보여줘.'],
              ['🔁 이어서', '직전에 멈춘 곳부터 이어서.'],
            ],
            template: [
              ['📋 양식 한 장', '이 단원의 빈출 논점 답안 양식 한 장 보여줘.'],
              ['❓ 빈칸 퀴즈', '방금 양식의 핵심 키워드 5개를 빈칸으로 내줘.'],
              ['🔢 빈출 양식 3', '이 단원 빈출 답안 양식 3개를 표로 정리.'],
            ],
            topic_extract: [
              ['🔍 사례 분석', '이 단원 빈출 사례 1개 제시하고, 어떤 논점 다룰지 물어봐줘.'],
              ['💡 정답 논점', '방금 사례의 정답 논점과 답안 배치 알려줘.'],
              ['🔄 다른 사례', '같은 주제 다른 사례 1개 더.'],
            ],
            answer_write: [
              ['📝 답안 문제', '이 단원에서 30점 분량 답안 문제 1개 출제. 학생이 답안 작성하면 채점해줄게.'],
              ['🎯 40점 문제', '40점 짜리 사례형 논술 1개 출제.'],
              ['📖 모범 답안', '방금 문제 모범 답안 양식 보여줘.'],
            ],
            mock_full: mockSession ? [
              ['⏭️ 다음 문제', '__nextMock__'],
              ['🏁 마무리·종합', '__endMock__'],
            ] : [
              ['🎬 모의 시작', '__startMock__'],
            ],
            calc_s2: [
              ['🧮 계산 시범', '이 논점 계산 산식을 단계별로 시범 보여줘.'],
              ['❓ 함정 체크', '계산 시 자주 빠뜨리는 함정 3개 알려줘.'],
              ['📋 답안 적용', '이 계산을 답안에 어떻게 쓸지 한 줄.'],
            ],
          }[mode] || []).map(([label, prompt]) => (
            <button
              key={label}
              disabled={streaming || !cap.ok}
              onClick={() => {
                if (prompt === '__startMock__') startMock();
                else if (prompt === '__nextMock__') nextMockQuestion();
                else if (prompt === '__endMock__') { setMockSession((s) => s ? { ...s, complete: true } : s); quickSend('모의 종료. 누적 점수·시간 분석·약점 단원 종합 정리.'); }
                else quickSend(prompt);
              }}
              style={{
                flex: '0 0 auto', padding: '5px 10px', borderRadius: 14,
                border: '1px solid #d1d5db', background: '#fff', color: '#374151',
                fontSize: '0.78rem', fontWeight: 600, cursor: streaming || !cap.ok ? 'not-allowed' : 'pointer',
                whiteSpace: 'nowrap', opacity: streaming || !cap.ok ? 0.5 : 1,
              }}
            >
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
                padding: '2px 6px', fontSize: '0.72rem', fontWeight: 700,
                border: '1px solid #d1d5db', borderRadius: 6,
                background: streaming ? '#f3f4f6' : '#fff',
                color: '#4338ca', cursor: streaming ? 'not-allowed' : 'pointer',
              }}
              title="응답 중에는 변경할 수 없습니다"
            >
              <option value={MODELS.primary}>🎯 Sonnet 4.6</option>
              <option value={MODELS.fast}>⚡ Haiku 4.5</option>
              <option value={MODELS.premium}>🧠 Opus 4.7</option>
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
          <AnswerWriteInput
            scorePoint={30}
            disabled={streaming || !cap.ok}
            onSubmit={({ answer, score_point, time_used_sec, time_target_min }) => {
              const min = Math.round(time_used_sec / 60);
              const text = `[답안 작성 — ${score_point}점, ${min}분 사용, 목표 ${time_target_min}분]\n\n${answer}\n\n위 답안을 채점해주세요. 점수·강점·보강·재작성 힌트를 JSON으로.`;
              quickSend(text);
            }}
          />
        )}
        <div style={{ display: 'flex', gap: 6, alignItems: 'flex-end', marginTop: mode === 'answer_write' ? 8 : 0 }}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
            }}
            placeholder={cap.ok
              ? (mode === 'answer_write' ? '추가 질문이나 모범 답안 요청...' : '메시지를 입력하세요 (Enter 전송, Shift+Enter 줄바꿈)')
              : '오늘 cap 도달'}
            disabled={!cap.ok || streaming}
            rows={mode === 'answer_write' ? 1 : 2}
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
      </div>
    </div>
    )
  );
}
