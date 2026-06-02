// 학습 노트 패널 — Phase γ.
// AI 응답·viz 차트·자유 텍스트를 노트로 저장. 태그·검색 지원.

import { useMemo, useState } from 'react';
import { getNotes, addNote, removeNote } from './aiLearningStore';

const KIND_META = {
  viz:     { icon: '🎨', label: 'viz', color: '#4f46e5', bg: '#eef2ff' },
  message: { icon: '💬', label: 'AI', color: '#0891b2', bg: '#cffafe' },
  manual:  { icon: '✏️', label: '메모', color: '#475569', bg: '#f1f5f9' },
};

export default function NotesPanel({ onJump }) {
  const [version, setVersion] = useState(0);
  const [filter, setFilter] = useState('all');
  const [q, setQ] = useState('');

  const notes = useMemo(() => getNotes(), [version]);
  const filtered = useMemo(() => {
    return notes.filter((n) => {
      if (filter !== 'all' && n.kind !== filter) return false;
      if (q) {
        const haystack = `${n.title || ''} ${n.content || ''} ${(n.tags || []).join(' ')} ${n.leafTitle || ''}`.toLowerCase();
        if (!haystack.includes(q.toLowerCase())) return false;
      }
      return true;
    });
  }, [notes, filter, q]);

  const handleDelete = (id) => {
    if (!window.confirm('이 노트를 삭제하시겠습니까?')) return;
    removeNote(id);
    setVersion((v) => v + 1);
  };

  return (
    <div style={{ padding: 12, background: '#fff', borderRadius: 10, border: '1px solid #e5e7eb' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 10 }}>
        <h3 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 800, color: '#111827' }}>
          📓 학습 노트 · {filtered.length}/{notes.length}
        </h3>
      </div>
      <div style={{ display: 'flex', gap: 4, marginBottom: 8, flexWrap: 'wrap' }}>
        {['all', 'viz', 'message', 'manual'].map((k) => (
          <button key={k} onClick={() => setFilter(k)}
            style={{
              padding: '4px 10px', borderRadius: 999, cursor: 'pointer',
              border: filter === k ? '1.5px solid #4f46e5' : '1px solid #d1d5db',
              background: filter === k ? '#eef2ff' : '#fff',
              color: filter === k ? '#1e40af' : '#6b7280',
              fontSize: '0.74rem', fontWeight: 700,
            }}>
            {k === 'all' ? '전체' : KIND_META[k]?.label || k}
          </button>
        ))}
      </div>
      <input
        type="text"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="검색 (제목·내용·태그)"
        style={{
          width: '100%', padding: '8px 12px',
          border: '1px solid #d1d5db', borderRadius: 8,
          fontSize: '0.85rem', marginBottom: 10,
        }}
      />
      {filtered.length === 0 && (
        <div style={{
          padding: 24, textAlign: 'center',
          fontSize: '0.85rem', color: '#9ca3af',
        }}>
          {notes.length === 0
            ? '아직 저장한 노트가 없습니다. AI 응답 옆 💾 버튼으로 저장하세요.'
            : '검색 결과가 없습니다.'}
        </div>
      )}
      {filtered.map((n) => {
        const meta = KIND_META[n.kind] || KIND_META.manual;
        return (
          <div key={n.id} style={{
            padding: 10, marginBottom: 6,
            background: '#fff', border: '1px solid #e5e7eb', borderRadius: 8,
          }}>
            <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 4 }}>
              <span style={{
                display: 'inline-flex', alignItems: 'center', gap: 4,
                padding: '2px 8px', borderRadius: 4,
                background: meta.bg, color: meta.color,
                fontSize: '0.72rem', fontWeight: 700,
              }}>{meta.icon} {meta.label}</span>
              <span style={{ fontSize: '0.7rem', color: '#9ca3af' }}>
                {n.ts?.slice(0, 16).replace('T', ' ')}
              </span>
            </div>
            {n.title && (
              <div style={{ fontWeight: 800, fontSize: '0.88rem', color: '#111827', marginBottom: 2 }}>
                {n.title}
              </div>
            )}
            {n.leafTitle && (
              <div style={{ fontSize: '0.74rem', color: '#6b7280', marginBottom: 4 }}>
                📂 {n.leafTitle}
              </div>
            )}
            {n.content && (
              <div style={{
                fontSize: '0.82rem', color: '#374151', lineHeight: 1.55,
                maxHeight: 100, overflow: 'hidden', position: 'relative',
                whiteSpace: 'pre-wrap',
              }}>
                {n.content.length > 240 ? n.content.slice(0, 240) + '…' : n.content}
              </div>
            )}
            <div style={{ marginTop: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 6 }}>
              <div style={{ flex: 1 }}>
                {(n.tags || []).map((t, i) => (
                  <span key={i} style={{
                    marginRight: 4,
                    padding: '1px 6px', borderRadius: 3,
                    background: '#f3f4f6', color: '#6b7280',
                    fontSize: '0.7rem',
                  }}>#{t}</span>
                ))}
              </div>
              {n.leafId && onJump && (
                <button onClick={() => onJump(n.leafId)} style={{
                  padding: '3px 8px', background: '#eef2ff', color: '#4338ca',
                  border: '1px solid #c7d2fe', borderRadius: 4,
                  fontSize: '0.7rem', fontWeight: 700, cursor: 'pointer',
                }}>이동 →</button>
              )}
              <button onClick={() => handleDelete(n.id)} style={{
                padding: '3px 8px', background: '#fef2f2', color: '#991b1b',
                border: '1px solid #fecaca', borderRadius: 4,
                fontSize: '0.7rem', fontWeight: 700, cursor: 'pointer',
              }}>삭제</button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
