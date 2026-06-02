// 판례 비교 매트릭스 — N개 판례 × 비교 항목 (사실관계·쟁점·판시·결론·평석).
// 표 형식이되, 컴포넌트가 일관된 디자인·하이라이트 처리.

function CaseComparisonChart({ params }) {
  const cases = params.cases || [];
  const fields = params.fields || ['facts', 'issue', 'holding', 'conclusion'];

  const FIELD_LABEL = {
    facts: '사실관계',
    issue: '쟁점',
    holding: '판시사항',
    conclusion: '결론',
    rule: '법리',
    significance: '의의',
    criticism: '평석',
  };

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12, overflowX: 'auto' }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 8 }}>
          ⚖️ {params.scenario}
        </figcaption>
      )}
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', minWidth: 480 }}>
        <thead>
          <tr>
            <th style={{
              padding: '8px 10px', borderBottom: '2px solid #111827', borderRight: '1px solid #e5e7eb',
              background: '#f9fafb', textAlign: 'left', verticalAlign: 'top', minWidth: 80, color: '#374151',
            }}>
              항목
            </th>
            {cases.map((c, i) => (
              <th key={i} style={{
                padding: '8px 10px', borderBottom: '2px solid #111827',
                borderRight: i < cases.length - 1 ? '1px solid #e5e7eb' : 'none',
                background: c.highlight ? '#fef3c7' : '#f9fafb',
                textAlign: 'left', verticalAlign: 'top', color: '#111827',
              }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 800 }}>{c.title || c.ref || `판례 ${i + 1}`}</div>
                {c.ref && c.title && (
                  <div style={{ fontSize: '0.74rem', color: '#6b7280', fontWeight: 600, marginTop: 2 }}>
                    {c.ref}
                  </div>
                )}
                {c.date && (
                  <div style={{ fontSize: '0.72rem', color: '#9ca3af', marginTop: 2 }}>
                    {c.date}
                  </div>
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {fields.map((f, rowIdx) => (
            <tr key={f}>
              <td style={{
                padding: '8px 10px', borderBottom: '1px solid #e5e7eb', borderRight: '1px solid #e5e7eb',
                background: '#f9fafb', verticalAlign: 'top', fontWeight: 700, color: '#475569',
              }}>
                {FIELD_LABEL[f] || f}
              </td>
              {cases.map((c, ci) => (
                <td key={ci} style={{
                  padding: '8px 10px', borderBottom: '1px solid #e5e7eb',
                  borderRight: ci < cases.length - 1 ? '1px solid #e5e7eb' : 'none',
                  verticalAlign: 'top', color: '#111827', lineHeight: 1.55,
                  background: c.highlight && rowIdx === 0 ? '#fef9c3' : 'transparent',
                }}>
                  {c[f] || <span style={{ color: '#d1d5db' }}>—</span>}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {params.narration && (
        <p style={{ margin: '10px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const caseComparisonTemplate = {
  name: 'case-comparison',
  version: 1,
  subjects: ['civil', 'law', 'appraisal_law'],
  helpText: '판례 N개 비교 매트릭스 (사실관계·쟁점·판시·결론)',
  Component: CaseComparisonChart,
  schema: {
    type: 'object',
    required: ['cases'],
    properties: {
      scenario: { type: 'string' },
      fields: {
        type: 'array',
        items: { enum: ['facts', 'issue', 'holding', 'conclusion', 'rule', 'significance', 'criticism'] },
      },
      cases: {
        type: 'array',
        minItems: 2,
        items: {
          type: 'object',
          properties: {
            title: { type: 'string' },
            ref: { type: 'string' },
            date: { type: 'string' },
            facts: { type: 'string' },
            issue: { type: 'string' },
            holding: { type: 'string' },
            conclusion: { type: 'string' },
            rule: { type: 'string' },
            significance: { type: 'string' },
            criticism: { type: 'string' },
            highlight: { type: 'boolean' },
          },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '잔여지수용 청구 — 핵심 판례 2개 비교',
    fields: ['facts', 'issue', 'holding', 'conclusion'],
    cases: [
      {
        title: '잔여지 종래 사용 곤란',
        ref: '대판 2008두822',
        date: '2008',
        facts: '도로 개설로 잔여지 일부만 남음',
        issue: '잔여지 수용 청구 인정 여부',
        holding: '종래 사용목적대로 사용 곤란 시 수용 청구 가능',
        conclusion: '청구 인용',
        highlight: true,
      },
      {
        title: '잔여지 가치 감소만 인정 X',
        ref: '대판 2014두46669',
        date: '2014',
        facts: '잔여지 일부 가격 하락만 있음',
        issue: '가격 감소만으로 수용 청구 가능 여부',
        holding: '사용 곤란 정도 아닌 단순 가격 감소는 수용 청구 사유 X',
        conclusion: '청구 기각',
      },
    ],
    narration: '잔여지 수용은 "종래 사용목적대로 사용 곤란" 기준 — 단순 가격 감소만으로 부족.',
  },
};
