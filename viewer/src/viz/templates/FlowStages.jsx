// 시점·단계 흐름 — 계약 전→후, 단기→장기, 정책 시행 전→직후→최종 같은 순서 있는 국면.
// 가로 배치 + 화살표. 2~4단계 권장(helpText 로 안내, 스키마는 minItems:2 만 강제).

function FlowStagesChart({ params }) {
  const stages = params.stages || [];

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12, overflowX: 'auto' }}>
      {params.caption && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 8 }}>
          {params.caption}
        </figcaption>
      )}
      <div style={{ display: 'flex', alignItems: 'stretch', gap: 0, minWidth: stages.length * 150 }}>
        {stages.map((s, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'stretch' }}>
            <div style={{
              width: 150, border: '1px solid #e5e7eb', borderRadius: 8, padding: '10px 12px',
              background: '#f9fafb',
            }}>
              <div style={{ fontSize: '0.72rem', color: '#9ca3af', fontWeight: 700 }}>{s.label}</div>
              <div style={{ fontSize: '0.86rem', fontWeight: 800, color: '#111827', marginTop: 2 }}>{s.title}</div>
              {s.note && <div style={{ fontSize: '0.76rem', color: '#6b7280', marginTop: 4, lineHeight: 1.5 }}>{s.note}</div>}
            </div>
            {i < stages.length - 1 && (
              <div style={{ display: 'flex', alignItems: 'center', padding: '0 8px', fontSize: '1.1rem', color: '#9ca3af' }}>
                →
              </div>
            )}
          </div>
        ))}
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const flowStagesTemplate = {
  name: 'flow-stages',
  version: 1,
  subjects: ['economics', 'civil', 'law', 'appraisal_law'],
  helpText: '순서 있는 국면·시점 흐름 (계약 전/후, 단기/장기, 정책 시행 전/직후/최종 등) 2~4단계',
  Component: FlowStagesChart,
  schema: {
    type: 'object',
    required: ['stages'],
    properties: {
      stages: {
        type: 'array', minItems: 2,
        items: {
          type: 'object', required: ['label', 'title'],
          properties: {
            label: { type: 'string' },
            title: { type: 'string' },
            note: { type: 'string' },
          },
        },
      },
      caption: { type: 'string' },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    caption: '비대칭정보의 시점별 문제',
    stages: [
      { label: '계약 전', title: '역선택', note: '숨은 특성 — 선별·신호발송' },
      { label: '계약 후', title: '도덕적 해이', note: '숨은 행동 — 감시·유인설계' },
    ],
    narration: '거래 시점을 기준으로 역선택과 도덕적 해이를 구분.',
  },
};
