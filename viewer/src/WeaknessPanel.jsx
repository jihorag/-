// 약점 자동 진단 패널 — Phase β.
// mastery + answer history 가중으로 TOP 5 약점 leaf 추출.
// 각 약점 카드 클릭 → 해당 leaf로 점프 (onJump 콜백).

import { useMemo } from 'react';
import { getMastery, getAllAnswerHistories, detectWeaknesses } from './aiLearningStore';

export default function WeaknessPanel({ leavesBySubject, onJump }) {
  const data = useMemo(() => {
    const mastery = getMastery();
    const answers = getAllAnswerHistories();
    const weak = detectWeaknesses(mastery, answers, 5);
    // leafId → leaf 객체 매핑
    const leafById = new Map();
    Object.values(leavesBySubject || {}).forEach((arr) => {
      (arr || []).forEach((l) => leafById.set(l.id, l));
    });
    return weak.map((w) => ({ ...w, leaf: leafById.get(w.leafId) }))
      .filter((w) => w.leaf);
  }, [leavesBySubject]);

  if (!data.length) {
    return (
      <div style={{
        padding: 16, background: '#f0fdf4',
        border: '1px solid #bbf7d0', borderRadius: 10,
        fontSize: '0.88rem', color: '#15803d', textAlign: 'center',
      }}>
        ✓ 약점으로 분류된 단원 없음. 꾸준한 학습 결과예요.
      </div>
    );
  }

  const KIND_LABEL = {
    quiz: { label: '문제풀이 약점', color: '#dc2626', bg: '#fee2e2' },
    answer: { label: '답안 작성 약점', color: '#7c3aed', bg: '#ede9fe' },
  };

  return (
    <div style={{ padding: 12, background: '#fff', borderRadius: 10, border: '1px solid #e5e7eb' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
        <h3 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 800, color: '#111827' }}>
          🎯 약점 단원 TOP {data.length}
        </h3>
        <span style={{ fontSize: '0.72rem', color: '#9ca3af' }}>정답률 + 답안점수 가중</span>
      </div>
      {data.map((w, i) => {
        const k = KIND_LABEL[w.kind] || KIND_LABEL.quiz;
        const path = w.leaf?.path || [];
        return (
          <button
            key={w.leafId}
            onClick={() => onJump && onJump(w.leaf)}
            style={{
              width: '100%', padding: '10px 12px', marginBottom: 6,
              background: '#fff', border: '1px solid #e5e7eb', borderRadius: 8,
              textAlign: 'left', cursor: 'pointer',
              display: 'flex', alignItems: 'center', gap: 10,
            }}
          >
            <div style={{
              width: 28, height: 28, borderRadius: '50%',
              background: k.bg, color: k.color, fontWeight: 800,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '0.85rem', flexShrink: 0,
            }}>
              #{i + 1}
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{
                fontSize: '0.88rem', fontWeight: 800, color: '#111827',
                overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
              }}>
                {path.slice(-1)[0] || w.leafId}
              </div>
              <div style={{
                fontSize: '0.72rem', color: '#6b7280',
                overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
              }}>
                {path.slice(0, -1).join(' › ')}
              </div>
              <div style={{ marginTop: 2, fontSize: '0.74rem', color: k.color, fontWeight: 600 }}>
                {k.label} · {w.reason}
              </div>
            </div>
            <div style={{ color: '#9ca3af', fontSize: '1rem' }}>›</div>
          </button>
        );
      })}
    </div>
  );
}
