// 청구권/법률관계 흐름도 — 단계별 (요건 → 효과 → 다음 단계).
// 각 step은 카드. 단계 간 ↓ 화살표.
// 각 카드: 단계명, 요건 목록, 효과, 조문.

function ClaimFlowChart({ params }) {
  const steps = params.steps || [];

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 14, maxWidth: 680 }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 10 }}>
          ⚖️ {params.scenario}
        </figcaption>
      )}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0 }}>
        {steps.map((step, i) => (
          <div key={i} style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{
              width: '100%', maxWidth: 480,
              padding: '10px 14px',
              background: step.highlight ? '#eef2ff' : '#fff',
              border: `1.5px solid ${step.highlight ? '#4f46e5' : '#d1d5db'}`,
              borderRadius: 10,
            }}>
              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
                marginBottom: 4,
              }}>
                <span style={{
                  fontSize: '0.78rem', fontWeight: 800,
                  color: step.highlight ? '#4338ca' : '#475569',
                }}>
                  Step {i + 1}. {step.label}
                </span>
                {step.article && (
                  <span style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 600 }}>
                    {step.article}
                  </span>
                )}
              </div>
              {step.requirements && step.requirements.length > 0 && (
                <div style={{ marginTop: 4 }}>
                  <div style={{ fontSize: '0.74rem', color: '#dc2626', fontWeight: 700, marginBottom: 2 }}>
                    요건
                  </div>
                  <ul style={{ margin: 0, paddingLeft: 18, fontSize: '0.8rem', color: '#374151', lineHeight: 1.5 }}>
                    {step.requirements.map((r, k) => <li key={k}>{r}</li>)}
                  </ul>
                </div>
              )}
              {step.effect && (
                <div style={{ marginTop: 6 }}>
                  <div style={{ fontSize: '0.74rem', color: '#047857', fontWeight: 700, marginBottom: 2 }}>
                    효과
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#111827', lineHeight: 1.5 }}>
                    {step.effect}
                  </div>
                </div>
              )}
              {step.note && (
                <div style={{ marginTop: 6, padding: '4px 8px', background: '#fef3c7', borderRadius: 6, fontSize: '0.74rem', color: '#92400e', fontWeight: 600 }}>
                  ⚠️ {step.note}
                </div>
              )}
            </div>
            {i < steps.length - 1 && (
              <div style={{ height: 24, display: 'flex', alignItems: 'center' }}>
                <svg width={20} height={24}>
                  <line x1={10} y1={0} x2={10} y2={18} stroke="#9ca3af" strokeWidth={2} />
                  <polyline points="4,16 10,22 16,16" fill="none" stroke="#9ca3af" strokeWidth={2} />
                </svg>
              </div>
            )}
          </div>
        ))}
      </div>
      {params.narration && (
        <p style={{ margin: '10px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const claimFlowTemplate = {
  name: 'claim-flow',
  version: 1,
  subjects: ['civil', 'law', 'appraisal_law'],
  helpText: '청구권/법률관계 단계 흐름 (요건→효과)',
  Component: ClaimFlowChart,
  schema: {
    type: 'object',
    required: ['steps'],
    properties: {
      scenario: { type: 'string' },
      steps: {
        type: 'array',
        minItems: 1,
        items: {
          type: 'object',
          required: ['label'],
          properties: {
            label: { type: 'string' },
            requirements: { type: 'array', items: { type: 'string' } },
            effect: { type: 'string' },
            article: { type: 'string' },
            highlight: { type: 'boolean' },
            note: { type: 'string' },
          },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '미성년자의 법률행위 → 취소 → 부당이득반환',
    steps: [
      {
        label: '미성년자 법률행위',
        requirements: ['만 19세 미만', '법정대리인 동의 없음', '권리만 얻거나 의무만 면하는 행위 X'],
        effect: '취소할 수 있는 법률행위',
        article: '민법 제5조',
      },
      {
        label: '취소권 행사',
        requirements: ['취소권자(미성년자 본인 또는 법정대리인)', '제척기간 내'],
        effect: '소급적 무효',
        article: '민법 제140조·제141조',
        highlight: true,
      },
      {
        label: '부당이득반환',
        requirements: ['이미 이행된 부분 존재'],
        effect: '제한능력자측은 현존이익만 반환',
        article: '민법 제141조 단서',
        note: '선의 제3자 보호 X (절대적 취소)',
      },
    ],
    narration: '미성년자 보호를 위한 3단계 — 행위 → 취소 → 반환. 현존이익 한정이 핵심.',
  },
};
