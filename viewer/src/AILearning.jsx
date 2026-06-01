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
  recordGrade, getDueChapters,
  getSessions, addSession, updateSession,
  getRoomMessages, appendRoomMessage, clearRoom, getAllRooms,
  bumpUsage, canSendMessage, getUsage,
  pruneOldConversations,
  addAssessment,
  resetLearningProgress,
  migrateLegacyCivilIds,
  SUBJECTS, getSubjectMeta,
} from './aiLearningStore';
import { sendMessages, buildSystemBlocks, sliceSection, extractJsonBlocks, MODELS } from './aiClaudeClient';

const indexUrl = (subjectId) => `/data/study/${subjectId}/ai_taxonomy_index.json`;
const handoverUrl = (subjectId) => `/data/study/${subjectId}/handover.md`;
const studyBase = (subjectId) => `/data/study/${subjectId}/`;

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
function LeafPicker({ leaves, current, onPick, mastery, due, quizStatsByLeaf }) {
  const [open, setOpen] = useState(false);
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
      {open && (
        <div style={{
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
                      <LeafButton leaf={ch._leaf} active={ch._leaf.id === current?.leaf_id} mastery={mastery} due={dueIds} onPick={() => { onPick(ch._leaf); setOpen(false); }} depth={1} />
                    )}
                    {Object.entries(ch.sections).map(([secName, sec]) => {
                      const secLeaves = sec._leaf ? [sec._leaf, ...Object.values(sec.items)] : Object.values(sec.items);
                      if (q && !secLeaves.some(matchQ)) return null;
                      return (
                        <div key={secName}>
                          {sec._leaf && matchQ(sec._leaf) && (
                            <LeafButton leaf={sec._leaf} active={sec._leaf.id === current?.leaf_id} mastery={mastery} due={dueIds} onPick={() => { onPick(sec._leaf); setOpen(false); }} depth={1} sectionLabel={secName} />
                          )}
                          {!sec._leaf && Object.keys(sec.items).length > 0 && (
                            <div style={{ padding: '4px 12px 2px 24px', fontSize: '0.76rem', color: '#6b7280' }}>{secName}</div>
                          )}
                          {Object.values(sec.items).filter(matchQ).map((it) => (
                            <LeafButton key={it.id} leaf={it} active={it.id === current?.leaf_id} mastery={mastery} due={dueIds} onPick={() => { onPick(it); setOpen(false); }} depth={2} />
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

function LeafButton({ leaf, active, mastery, due, onPick, depth = 0, sectionLabel }) {
  const m = mastery[leaf.id] || { coverage: 0, accuracy: 0, status: 'not_started' };
  const isDue = due.has(leaf.id);
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
      {m.coverage > 0 && <div style={{ marginTop: 4 }}><MasteryBar value={m.coverage} /></div>}
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
    const ks = Object.keys(mastery).filter((k) => k.startsWith(s.id + '__'));
    const total = ks.length;
    const covSum = ks.reduce((a, k) => a + (mastery[k]?.coverage || 0), 0);
    const accs = ks.map((k) => mastery[k]?.accuracy || 0).filter((x) => x > 0);
    const masterCount = ks.filter((k) => mastery[k]?.status === 'mastered').length;
    return {
      s,
      total,
      covAvg: total > 0 ? covSum / total : 0,
      accAvg: accs.length > 0 ? accs.reduce((a, b) => a + b, 0) / accs.length : 0,
      masterCount,
    };
  });

  // 단원 진행 ranking — 진행한 모든 leaf 중 top/bottom
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

  // 레이더 다각형 좌표
  const radius = 70;
  const cx = 90;
  const cy = 90;
  const pts = stats.map((st, i) => {
    const angle = (Math.PI * 2 * i) / stats.length - Math.PI / 2;
    const r = radius * (st.covAvg || 0);
    return { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle), s: st.s, st };
  });
  const polyStr = pts.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
  const axisPts = stats.map((_, i) => {
    const angle = (Math.PI * 2 * i) / stats.length - Math.PI / 2;
    return { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle), label: SUBJECTS[i].short };
  });

  return (
    <div style={{ padding: 16, background: '#fff', borderRadius: 12, border: '1px solid #e5e7eb' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <h3 style={{ margin: 0, fontSize: '1rem', display: 'flex', alignItems: 'center', gap: 6 }}>
          <BarChart3 size={18} /> 5과목 종합 분석
        </h3>
        <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6b7280' }}>✕</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '180px 1fr', gap: 16, alignItems: 'start' }}>
        <svg viewBox="0 0 180 180" style={{ width: '100%', height: 'auto' }}>
          {[0.25, 0.5, 0.75, 1].map((r) => (
            <polygon
              key={r}
              points={SUBJECTS.map((_, i) => {
                const a = (Math.PI * 2 * i) / SUBJECTS.length - Math.PI / 2;
                return `${(cx + radius * r * Math.cos(a)).toFixed(1)},${(cy + radius * r * Math.sin(a)).toFixed(1)}`;
              }).join(' ')}
              fill="none" stroke="#e5e7eb" strokeWidth="1"
            />
          ))}
          {axisPts.map((p, i) => (
            <line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="#e5e7eb" strokeWidth="1" />
          ))}
          <polygon points={polyStr} fill="#4f46e5" fillOpacity="0.25" stroke="#4f46e5" strokeWidth="2" />
          {pts.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r="3" fill={p.s.color} />
          ))}
          {axisPts.map((p, i) => (
            <text
              key={i}
              x={p.x + (p.x > cx ? 4 : p.x < cx ? -4 : 0)}
              y={p.y + (p.y > cy ? 10 : p.y < cy ? -4 : 4)}
              fontSize="10"
              textAnchor={p.x > cx ? 'start' : p.x < cx ? 'end' : 'middle'}
              fill="#374151"
            >
              {p.label}
            </text>
          ))}
        </svg>
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
                  <td style={{ padding: '4px 0', color: st.s.color, fontWeight: 700 }}>{st.s.icon} {st.s.short}</td>
                  <td style={{ textAlign: 'right' }}>{Math.round(st.covAvg * 100)}%</td>
                  <td style={{ textAlign: 'right' }}>{st.masterCount}/{st.total}</td>
                  <td style={{ textAlign: 'right' }}>{st.accAvg > 0 ? `${Math.round(st.accAvg * 100)}%` : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
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
  const [mastery, setMasteryState] = useState(getMastery());
  const [handoverMd, setHandoverMd] = useState('');
  const [unitMd, setUnitMd] = useState('');
  const [sectionMd, setSectionMd] = useState('');
  const [problemsMd, setProblemsMd] = useState('');
  const [mode, setMode] = useState('study'); // 'study' | 'practice'
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
      fetch(indexUrl(s.id)).then((r) => r.json()).then((idx) => {
        setLeavesBySubject((prev) => ({ ...prev, [s.id]: idx.leaves || [] }));
      }).catch(() => {});
    });
  }, [showAnalytics]); // eslint-disable-line
  const [sessionId, setSessionId] = useState(null);
  const [idlePromptShown, setIdlePromptShown] = useState(false);
  const [weakSuggestion, setWeakSuggestion] = useState([]);
  const [confirmAction, setConfirmAction] = useState(null); // {label, onYes}
  const [recentRooms, setRecentRooms] = useState(() => getAllRooms());
  const abortRef = useRef(null);
  const scrollRef = useRef(null);
  const idleTimerRef = useRef(null);

  // 인덱스·인수인계서 로드 — subjectId 변경 시 재로드
  useEffect(() => {
    fetch(indexUrl(subjectId)).then((r) => r.json()).then((idx) => {
      setIndexMeta(idx);
      setLeaves(idx.leaves || []);
      // 현재 leaf가 이 과목 leaves에 없으면 default로 재설정
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

  // 문제풀이 모드 진입 시에만 problems MD 로드
  useEffect(() => {
    if (mode !== 'practice' || !current?.leaf_id) { setProblemsMd(''); return; }
    const leaf = leaves.find((l) => l.id === current.leaf_id);
    if (!leaf || !leaf.problems_file) { setProblemsMd(''); return; }
    fetch(studyBase(subjectId) + leaf.problems_file).then((r) => r.text()).then(setProblemsMd).catch(() => setProblemsMd(''));
  }, [mode, current?.leaf_id, leaves, subjectId]);

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
  const switchSubject = (sid) => {
    if (sid === subjectId) return;
    if (abortRef.current) abortRef.current.abort();
    setSubjectId(sid);
    setMessages([]);
    setUnitMd(''); setSectionMd(''); setProblemsMd('');
    setPendingNext(null); setIdlePromptShown(false); setInput('');
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
    const system = buildSystemBlocks({
      handoverMd,                            // ← 캐시 안정: 텍스트 불변
      unitMd: sectionMd ? '' : unitMd,
      sectionMd,
      problemsMd: mode === 'practice' ? problemsMd : '',
      mode,
      currentMastery: curMastery,
      recentSummary,
      leafPath: curLeaf ? curLeaf.path.join(' / ') : '',
    });

    const history = [...getRoomMessages(current.leaf_id)].slice(-13);
    const apiMessages = history.map((m) => ({ role: m.role, content: m.content }));

    const ac = new AbortController();
    abortRef.current = ac;
    try {
      const { text: out, usage } = await sendMessages({
        apiKey: byok,
        model: prefs.model,
        system,
        messages: apiMessages,
        maxTokens: prefs.max_tokens || 1200,
        signal: ac.signal,
        onDelta: (_chunk, agg) => setDraft(agg),
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

  // 인라인 confirm — 브라우저 confirm() 대체. 채팅 영역 하단에 카드로 표시.
  const askConfirm = (label, danger, onYes) => {
    setConfirmAction({ label, danger: !!danger, onYes });
  };

  const curLeaf = leaves.find((l) => l.id === current?.leaf_id);
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
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', padding: '6px 8px', display: 'flex', alignItems: 'center', gap: 4 }}>
        <button
          onClick={() => prevLeaf && pickLeaf(prevLeaf)}
          disabled={!prevLeaf}
          title={prevLeaf ? `← ${prevLeaf.path.slice(-1)[0]}` : ''}
          style={{ background: 'none', border: 'none', cursor: prevLeaf ? 'pointer' : 'not-allowed', padding: 4, opacity: prevLeaf ? 1 : 0.3 }}
        >
          <ChevronLeft size={20} color="#374151" />
        </button>
        <div style={{ flex: 1, minWidth: 0, display: 'flex', alignItems: 'center', gap: 6 }}>
          <Sparkles size={16} color="#4f46e5" />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#111827', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {curLeaf ? curLeaf.path.slice(-1)[0] : 'AI 학습'}
            </div>
            <div style={{ fontSize: '0.68rem', color: '#9ca3af', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {curLeaf ? curLeaf.path.slice(1, -1).join(' › ') : ''}
            </div>
          </div>
          {curLeaf && (() => {
            const m = mastery[curLeaf.id] || { coverage: 0, status: 'not_started' };
            const pct = Math.round((m.coverage || 0) * 100);
            const isMaster = m.status === 'mastered';
            return (
              <span style={{
                fontSize: '0.7rem', fontWeight: 700, padding: '2px 8px', borderRadius: 10,
                background: isMaster ? '#d1fae5' : pct > 0 ? '#eef2ff' : '#f3f4f6',
                color: isMaster ? '#047857' : pct > 0 ? '#4338ca' : '#9ca3af',
                whiteSpace: 'nowrap',
              }}>
                {isMaster ? '✓ 마스터' : `${pct}%`}
              </span>
            );
          })()}
        </div>
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
      {(() => {
        // 5과목 종합 진척 — 현재 과목과 무관하게 모든 leaf mastery 합산
        const overall = {};
        SUBJECTS.forEach((s) => {
          const ks = Object.keys(mastery).filter((k) => k.startsWith(s.id + '__'));
          const total = ks.length;
          const covSum = ks.reduce((sum, k) => sum + (mastery[k]?.coverage || 0), 0);
          const masterCount = ks.filter((k) => mastery[k]?.status === 'mastered').length;
          overall[s.id] = { total, covAvg: total > 0 ? covSum / total : 0, masterCount };
        });
        const anyProgress = Object.values(overall).some((x) => x.covAvg > 0);
        if (!anyProgress) return null;
        return (
          <div style={{ padding: '4px 8px', borderBottom: '1px solid #f3f4f6', background: '#fafafa', display: 'flex', gap: 6, overflowX: 'auto' }}>
            {SUBJECTS.map((s) => {
              const o = overall[s.id];
              const on = s.id === subjectId;
              return (
                <button
                  key={s.id}
                  onClick={() => switchSubject(s.id)}
                  title={`${s.title} · 평균 ${Math.round(o.covAvg * 100)}% · 마스터 ${o.masterCount}`}
                  style={{
                    flex: '0 0 auto', padding: '3px 8px', borderRadius: 8,
                    background: on ? '#fff' : 'transparent',
                    border: on ? `1px solid ${s.color}` : '1px solid transparent',
                    cursor: 'pointer', display: 'flex', flexDirection: 'column', alignItems: 'flex-start', minWidth: 56,
                  }}
                >
                  <span style={{ fontSize: '0.65rem', color: on ? s.color : '#6b7280', fontWeight: 700 }}>{s.icon} {s.short}</span>
                  <div style={{ width: '100%', height: 3, background: '#e5e7eb', borderRadius: 2, marginTop: 2, overflow: 'hidden' }}>
                    <div style={{ width: `${Math.max(2, o.covAvg * 100)}%`, height: '100%', background: s.color }} />
                  </div>
                </button>
              );
            })}
          </div>
        );
      })()}
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

      <div style={{ padding: '8px 12px', borderBottom: '1px solid #e5e7eb', background: '#f9fafb' }}>
        <div style={{ display: 'flex', gap: 4, marginBottom: 8, overflowX: 'auto', paddingBottom: 2 }}>
          {SUBJECTS.map((s) => {
            const on = s.id === subjectId;
            return (
              <button
                key={s.id}
                onClick={() => switchSubject(s.id)}
                style={{
                  flex: '0 0 auto', padding: '5px 10px', borderRadius: 12,
                  border: on ? `1.5px solid ${s.color}` : '1px solid #d1d5db',
                  background: on ? `${s.color}15` : '#fff',
                  color: on ? s.color : '#374151',
                  fontWeight: on ? 800 : 600, fontSize: '0.78rem', cursor: 'pointer', whiteSpace: 'nowrap',
                }}
                title={s.title}
              >
                {s.icon} {s.short}
              </button>
            );
          })}
        </div>
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
        <LeafPicker leaves={leaves} current={current} onPick={pickLeaf} mastery={mastery} due={due} />
        {curLeaf && (
          <div style={{ marginTop: 6, fontSize: '0.72rem', color: '#6b7280', display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
            <span>교재: {curLeaf.unit_code || '—'}</span>
            <span>·</span>
            <span title={curLeaf.section_name}>
              {curLeaf.section_name && curLeaf.section_name !== '전체'
                ? `🔍 ${curLeaf.section_name.length > 24 ? curLeaf.section_name.slice(0, 24) + '…' : curLeaf.section_name}`
                : '전체'}
              {curLeaf.section_key === 'auto' && curLeaf.section_lines && (
                <span style={{ color: '#9ca3af' }}> ({curLeaf.section_lines[1] - curLeaf.section_lines[0]}줄)</span>
              )}
            </span>
            {!curLeaf.unit_file && (
              <span style={{ color: '#dc2626', fontWeight: 700 }}>· ⚠️ 단원 자료 없음</span>
            )}
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
            onResetProgress={() => {
              askConfirm('대화·세션·진척도 전부 초기화 (API 키·설정 유지)', true, () => {
                resetLearningProgress();
                setMessages([]);
                setMasteryState({});
                setDue([]);
                setCurrentState(null);
                setSessionId(null);
                setPendingNext(null);
                setRecentRooms([]);
                if (indexMeta?.default_leaf) {
                  const def = indexMeta.leaves.find((l) => l.id === indexMeta.default_leaf) || indexMeta.leaves[0];
                  if (def) { const next = { subject: 'civil', leaf_id: def.id }; setCurrentState(next); setCurrent(next); }
                }
                setShowSettings(false);
              });
            }}
          />
        </div>
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
              if (sid !== subjectId) switchSubject(sid);
              setTimeout(() => pickLeaf(leaf), 50);
              setShowAnalytics(false);
            }}
          />
        </div>
      )}

      <div ref={scrollRef} style={{ flex: 1, overflowY: 'auto', padding: '12px 14px' }}>
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
                  onClick={() => setMode((m) => m === 'practice' ? 'study' : 'practice')}
                  style={{
                    padding: '9px 16px', background: '#fff', color: '#374151', border: '1px solid #d1d5db',
                    borderRadius: 8, cursor: 'pointer', fontWeight: 600,
                  }}
                >
                  {mode === 'practice' ? '📖 이론으로' : '✏️ 문제풀이로'}
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
          return (
            <div key={i}>
              <MessageBubble msg={m} />
              {opts && (
                <AnswerChoiceRow
                  options={opts}
                  disabled={streaming || !cap.ok}
                  onPick={(o) => quickSend(`${CIRCLED_DIGITS[o.n - 1]}번 — ${o.text}`)}
                />
              )}
            </div>
          );
        })}
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
        <div style={{ display: 'flex', gap: 4, overflowX: 'auto', marginBottom: 6, paddingBottom: 2 }}>
          {(mode === 'practice'
            ? [
                ['📝 기출 한 문제 출제해줘', '기출 한 문제 출제해줘. 함정 분석도 같이.'],
                ['🔄 비슷한 다른 문제', '같은 주제로 다른 기출 문제 한 개 더 출제해줘.'],
                ['💡 정답·해설', '방금 문제 정답과 해설을 자세히 알려줘.'],
              ]
            : [
                ['▶️ 이 단원 시작', '이 단원의 첫 절·관부터 한 사이클(개념→비유→확인 문제→피드백) 시작해줘.'],
                ['🔁 이어서 진행', '직전에 멈춘 곳에서 자연스럽게 이어서 진행해줘.'],
                ['🧩 종합 퀴즈', '이 단원의 종합 퀴즈(빈칸·단답·OX·사례) 한 세트 내줘.'],
                ['🏁 오늘 끝 — 정리', '오늘 학습 정리해줘. 끝.'],
              ]
          ).map(([label, prompt]) => (
            <button
              key={label}
              disabled={streaming || !cap.ok}
              onClick={() => quickSend(prompt)}
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
