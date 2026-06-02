// 모든 viz 템플릿을 example 파라미터로 한 페이지에 렌더 — 개발/QA용.
// URL hash 에 #viz-gallery 추가하면 진입.
//
// 각 카드: 템플릿 이름, 설명, 적용 과목, 실제 렌더, 예시 JSON pretty.

import { useState } from 'react';
import { listTemplates } from './vizRegistry';
import VizRouter from './VizRouter';

const SUBJECT_LABEL = {
  economics: '경제학',
  accounting: '회계학',
  civil: '민법',
  law: '관계법규',
  realestate: '부동산학원론',
  appraisal_practice: '실무(2차)',
  appraisal_theory: '이론(2차)',
  appraisal_law: '보상법규(2차)',
};

function TemplateCard({ tpl }) {
  const [showJson, setShowJson] = useState(false);
  const rawJson = JSON.stringify(tpl.exampleParams, null, 2);
  return (
    <div style={{
      background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12,
      padding: 16, marginBottom: 16,
    }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 4 }}>
        <h3 style={{ margin: 0, fontSize: '1.05rem', fontWeight: 800, color: '#111827', fontFamily: 'ui-monospace, monospace' }}>
          {tpl.name}
        </h3>
        <span style={{ fontSize: '0.72rem', color: '#9ca3af' }}>v{tpl.version}</span>
      </header>
      <div style={{ fontSize: '0.82rem', color: '#475569', marginBottom: 8 }}>
        {tpl.helpText}
      </div>
      <div style={{ display: 'flex', gap: 4, marginBottom: 10, flexWrap: 'wrap' }}>
        {(tpl.subjects || []).map((s) => (
          <span key={s} style={{
            padding: '2px 8px', borderRadius: 12,
            background: '#eef2ff', color: '#4338ca',
            fontSize: '0.7rem', fontWeight: 700,
          }}>
            {SUBJECT_LABEL[s] || s}
          </span>
        ))}
      </div>
      <VizRouter name={tpl.name} rawJson={rawJson} />
      <button
        onClick={() => setShowJson((v) => !v)}
        style={{
          marginTop: 8, padding: '4px 10px',
          background: showJson ? '#1f2937' : '#f3f4f6',
          color: showJson ? '#fff' : '#374151',
          border: 'none', borderRadius: 6,
          fontSize: '0.74rem', fontWeight: 700, cursor: 'pointer',
        }}
      >
        {showJson ? 'JSON 숨기기' : '예시 JSON 보기'}
      </button>
      {showJson && (
        <pre style={{
          margin: '8px 0 0', padding: 10, background: '#0f172a', color: '#cbd5e1',
          borderRadius: 8, fontSize: '0.75rem', overflowX: 'auto', maxHeight: 320,
        }}>
          {rawJson}
        </pre>
      )}
    </div>
  );
}

export default function VizGallery({ onClose }) {
  const all = listTemplates();
  const [filter, setFilter] = useState('all');
  const subjects = ['all', ...new Set(all.flatMap((t) => t.subjects || []))];
  const filtered = filter === 'all' ? all : all.filter((t) => (t.subjects || []).includes(filter));

  return (
    <div style={{
      position: 'fixed', inset: 0, background: '#f9fafb',
      zIndex: 1000, overflowY: 'auto', padding: '20px clamp(12px, 4vw, 40px)',
    }}>
      <div style={{ maxWidth: 960, margin: '0 auto' }}>
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.6rem', fontWeight: 800, color: '#111827' }}>
              🎨 시각자료 갤러리
            </h1>
            <p style={{ margin: '4px 0 0', fontSize: '0.88rem', color: '#6b7280' }}>
              등록된 viz 템플릿 {all.length}개 · 예시 파라미터로 렌더
            </p>
          </div>
          {onClose && (
            <button onClick={onClose} style={{
              padding: '8px 14px', background: '#111827', color: '#fff',
              border: 'none', borderRadius: 8, cursor: 'pointer', fontWeight: 700,
            }}>
              ✕ 닫기
            </button>
          )}
        </header>
        <div style={{
          display: 'flex', gap: 4, marginBottom: 16, flexWrap: 'wrap',
          padding: 8, background: '#fff', borderRadius: 10, border: '1px solid #e5e7eb',
        }}>
          {subjects.map((s) => (
            <button key={s} onClick={() => setFilter(s)} style={{
              padding: '6px 12px',
              background: filter === s ? '#4f46e5' : 'transparent',
              color: filter === s ? '#fff' : '#374151',
              border: filter === s ? 'none' : '1px solid #e5e7eb',
              borderRadius: 8, fontSize: '0.8rem', fontWeight: 700, cursor: 'pointer',
            }}>
              {s === 'all' ? '전체' : (SUBJECT_LABEL[s] || s)}
            </button>
          ))}
        </div>
        {filtered.length === 0 && (
          <div style={{ padding: 40, textAlign: 'center', color: '#9ca3af' }}>
            이 과목에 등록된 템플릿이 없습니다.
          </div>
        )}
        {filtered.map((tpl) => <TemplateCard key={tpl.name} tpl={tpl} />)}
      </div>
    </div>
  );
}
