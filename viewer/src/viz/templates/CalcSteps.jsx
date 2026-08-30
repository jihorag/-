// 계산 단계표 — 수식을 단계별로 풀어가는 표 (명목→실질 GDP, 디플레이터, 승수 계산 등).
// KaTeX 로 expr 렌더. ParsedText 는 import 하지 않음(순환 위험) — katex 를 직접 호출하는
// 기존 패턴(src/ParsedText.jsx)을 그대로 따름.

import katex from 'katex';
import 'katex/dist/katex.min.css';

function renderExpr(expr) {
  if (!expr) return null;
  try {
    return { __html: katex.renderToString(expr, { throwOnError: false, output: 'html' }) };
  } catch {
    return { __html: expr };
  }
}

function CalcStepsChart({ params }) {
  const rows = params.rows || [];

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12, maxWidth: 520 }}>
      {params.title && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 8 }}>
          {params.title}
        </figcaption>
      )}
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i} style={{ background: r.emphasis ? '#f9fafb' : 'transparent' }}>
              <td style={{
                padding: '7px 10px', borderBottom: '1px solid #e5e7eb', color: '#475569',
                fontWeight: r.emphasis ? 700 : 500, whiteSpace: 'nowrap', verticalAlign: 'middle',
              }}>
                {r.label}
              </td>
              <td style={{ padding: '7px 10px', borderBottom: '1px solid #e5e7eb', color: '#111827', verticalAlign: 'middle' }}>
                {r.expr && <span dangerouslySetInnerHTML={renderExpr(r.expr)} />}
              </td>
              <td style={{
                padding: '7px 10px', borderBottom: '1px solid #e5e7eb', textAlign: 'right',
                fontFamily: 'ui-monospace, monospace', fontWeight: r.emphasis ? 800 : 600,
                color: r.emphasis ? '#111827' : '#374151', verticalAlign: 'middle',
              }}>
                {r.value}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {params.note && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.note}
        </p>
      )}
    </figure>
  );
}

export const calcStepsTemplate = {
  name: 'calc-steps',
  version: 1,
  subjects: ['economics', 'accounting'],
  helpText: '수식을 단계별로 풀어가는 계산표 (명목·실질 GDP, GDP 디플레이터, 승수 계산 등) — steps 재생과 궁합 좋음',
  Component: CalcStepsChart,
  schema: {
    type: 'object',
    required: ['rows'],
    properties: {
      title: { type: 'string' },
      rows: {
        type: 'array', minItems: 1,
        items: {
          type: 'object', required: ['label'],
          properties: {
            label: { type: 'string' },
            expr: { type: 'string' },
            value: { type: 'string' },
            emphasis: { type: 'boolean' },
          },
        },
      },
      note: { type: 'string' },
    },
  },
  exampleParams: {
    title: '실질 GDP·GDP 디플레이터 계산',
    rows: [
      { label: '명목 GDP', expr: '(2 \\times 8) + (1 \\times 6)', value: '22' },
      { label: '실질 GDP (기준연도 가격)', expr: '(1 \\times 8) + (2 \\times 6)', value: '20' },
      { label: 'GDP 디플레이터', expr: '\\frac{22}{20} \\times 100', value: '110', emphasis: true },
    ],
    note: '명목 GDP 는 당해연도 가격, 실질 GDP 는 기준연도 가격으로 계산.',
  },
};
