// IS-LM 모형 — 재정정책/통화정책에 의한 IS·LM 곡선 이동.
// IS: 우하향 (소득 ↑ → 이자율 ↓), LM: 우상향 (소득 ↑ → 이자율 ↑).
// 의미 파라미터: shifts (curve, dir, magnitude, reason).

const W = 480, H = 360, PADL = 50, PADB = 50, PADT = 24, PADR = 30;
const PW = W - PADL - PADR;
const PH = H - PADT - PADB;

const MAG_TO_SHIFT = { small: 0.10, moderate: 0.18, large: 0.30 };

function nx(y) { return PADL + y * PW; }
function ny(r) { return PADT + (1 - r) * PH; }

// IS: r = isIntercept + isSlope*Y (isSlope < 0, 우하향)
// LM: r = lmIntercept + lmSlope*Y (lmSlope > 0, 우상향)
function computeCurves(shifts) {
  let isIntercept = 0.85, isSlope = -0.7;
  let lmIntercept = 0.10, lmSlope = 0.75;
  for (const s of shifts || []) {
    const mag = MAG_TO_SHIFT[s.magnitude] || MAG_TO_SHIFT.moderate;
    const sign = s.direction === 'right' ? 1 : -1;
    if (s.curve === 'IS') isIntercept += sign * mag;
    else if (s.curve === 'LM') lmIntercept -= sign * mag;  // LM 우측 = intercept 감소
  }
  // 교차점: isIntercept + isSlope*Y = lmIntercept + lmSlope*Y → Y = (isIntercept - lmIntercept) / (lmSlope - isSlope)
  const yStar = (isIntercept - lmIntercept) / (lmSlope - isSlope);
  const rStar = isIntercept + isSlope * yStar;
  return {
    is: { intercept: isIntercept, slope: isSlope },
    lm: { intercept: lmIntercept, slope: lmSlope },
    yStar, rStar,
  };
}

function curveEndpoints(c) {
  return { x1: 0, y1: c.intercept, x2: 1, y2: c.intercept + c.slope };
}

function clamp01(v) { return Math.max(0, Math.min(1, v)); }

function IsLmChart({ params }) {
  const initial = computeCurves([]);
  const final = computeCurves(params.shifts || []);
  const hasShift = (params.shifts || []).length > 0;

  const isColor = '#2563eb';
  const lmColor = '#dc2626';
  const isInitColor = '#93c5fd';
  const lmInitColor = '#fca5a5';

  const isF = curveEndpoints(final.is);
  const lmF = curveEndpoints(final.lm);
  const isI = curveEndpoints(initial.is);
  const lmI = curveEndpoints(initial.lm);

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12 }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 6 }}>
          📊 {params.scenario}
        </figcaption>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', maxWidth: 520, display: 'block' }}>
        {/* 축 */}
        <line x1={nx(0)} y1={ny(0)} x2={nx(1)} y2={ny(0)} stroke="#9ca3af" strokeWidth={1.5} />
        <line x1={nx(0)} y1={ny(0)} x2={nx(0)} y2={ny(1)} stroke="#9ca3af" strokeWidth={1.5} />
        <text x={nx(1) + 2} y={ny(0) + 4} fontSize={12} fill="#374151">Y (소득)</text>
        <text x={nx(0) - 6} y={ny(1) - 6} fontSize={12} fill="#374151" textAnchor="end">r (이자율)</text>

        {/* 이전 곡선 (점선) */}
        {hasShift && (
          <>
            <line x1={nx(clamp01(isI.x1))} y1={ny(clamp01(isI.y1))} x2={nx(clamp01(isI.x2))} y2={ny(clamp01(isI.y2))}
              stroke={isInitColor} strokeWidth={1.5} strokeDasharray="4 4" />
            <line x1={nx(clamp01(lmI.x1))} y1={ny(clamp01(lmI.y1))} x2={nx(clamp01(lmI.x2))} y2={ny(clamp01(lmI.y2))}
              stroke={lmInitColor} strokeWidth={1.5} strokeDasharray="4 4" />
            <text x={nx(clamp01(isI.x2)) - 4} y={ny(clamp01(isI.y2)) + 14} fontSize={11} fill={isInitColor} textAnchor="end">IS₀</text>
            <text x={nx(clamp01(lmI.x2)) - 4} y={ny(clamp01(lmI.y2)) - 6} fontSize={11} fill={lmInitColor} textAnchor="end">LM₀</text>
          </>
        )}

        {/* 최종 IS / LM */}
        <line x1={nx(clamp01(isF.x1))} y1={ny(clamp01(isF.y1))} x2={nx(clamp01(isF.x2))} y2={ny(clamp01(isF.y2))}
          stroke={isColor} strokeWidth={2.2} />
        <line x1={nx(clamp01(lmF.x1))} y1={ny(clamp01(lmF.y1))} x2={nx(clamp01(lmF.x2))} y2={ny(clamp01(lmF.y2))}
          stroke={lmColor} strokeWidth={2.2} />
        <text x={nx(clamp01(isF.x2)) - 4} y={ny(clamp01(isF.y2)) + 14} fontSize={12} fontWeight={700} fill={isColor} textAnchor="end">{hasShift ? 'IS₁' : 'IS'}</text>
        <text x={nx(clamp01(lmF.x2)) - 4} y={ny(clamp01(lmF.y2)) - 6} fontSize={12} fontWeight={700} fill={lmColor} textAnchor="end">{hasShift ? 'LM₁' : 'LM'}</text>

        {/* 균형점 가이드 */}
        <line x1={nx(final.yStar)} y1={ny(0)} x2={nx(final.yStar)} y2={ny(final.rStar)} stroke="#6b7280" strokeWidth={1} strokeDasharray="2 3" />
        <line x1={nx(0)} y1={ny(final.rStar)} x2={nx(final.yStar)} y2={ny(final.rStar)} stroke="#6b7280" strokeWidth={1} strokeDasharray="2 3" />

        {/* 균형점 마커 */}
        {hasShift && (
          <>
            <circle cx={nx(initial.yStar)} cy={ny(initial.rStar)} r={4} fill="#fff" stroke="#9ca3af" strokeWidth={2} />
            <text x={nx(initial.yStar) + 6} y={ny(initial.rStar) - 6} fontSize={11} fill="#6b7280">E₀</text>
          </>
        )}
        <circle cx={nx(final.yStar)} cy={ny(final.rStar)} r={5} fill="#111827" />
        <text x={nx(final.yStar) + 8} y={ny(final.rStar) - 6} fontSize={12} fontWeight={700} fill="#111827">{hasShift ? 'E₁' : 'E*'}</text>
      </svg>
      {/* shift 자동 자막 */}
      {hasShift && (
        <ul style={{ margin: '6px 0 0', padding: '0 0 0 18px', fontSize: '0.78rem', color: '#374151', lineHeight: 1.5 }}>
          {params.shifts.map((s, i) => (
            <li key={i}>
              <strong>{s.curve}</strong> {s.direction === 'right' ? '우측' : '좌측'} 이동
              {s.magnitude && s.magnitude !== 'moderate' && ` (${s.magnitude === 'small' ? '소폭' : '대폭'})`}
              {s.reason && ` — ${s.reason}`}
            </li>
          ))}
          <li style={{ color: final.yStar > initial.yStar ? '#15803d' : '#b91c1c', fontWeight: 700 }}>
            ⇒ Y {final.yStar > initial.yStar ? '↑' : '↓'},
            r {final.rStar > initial.rStar ? '↑' : '↓'}
          </li>
        </ul>
      )}
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const isLmTemplate = {
  name: 'is-lm',
  version: 1,
  subjects: ['economics'],
  helpText: 'IS-LM 모형 (재정·통화정책 이동)',
  Component: IsLmChart,
  schema: {
    type: 'object',
    properties: {
      scenario: { type: 'string' },
      shifts: {
        type: 'array',
        items: {
          type: 'object',
          required: ['curve', 'direction'],
          properties: {
            curve: { enum: ['IS', 'LM'] },
            direction: { enum: ['left', 'right'] },
            magnitude: { enum: ['small', 'moderate', 'large'], default: 'moderate' },
            reason: { type: 'string' },
          },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '확장적 재정정책 (G 증가)',
    shifts: [{ curve: 'IS', direction: 'right', magnitude: 'moderate', reason: '정부지출 증가' }],
    narration: 'IS 우측 이동 → Y, r 모두 상승. 단, r 상승으로 일부 구축효과(crowding-out) 발생.',
  },
};
