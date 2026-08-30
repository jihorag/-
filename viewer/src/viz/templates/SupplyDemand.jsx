// 수요공급 곡선 — 이동 시나리오 시각화.
// AI는 "shift" 의미적 파라미터만 출력. 좌표·균형점·화살표는 컴포넌트가 계산.

const W = 480, H = 360, PADL = 50, PADB = 50, PADT = 24, PADR = 24;
const PW = W - PADL - PADR;
const PH = H - PADT - PADB;

const MAG_TO_SHIFT = { small: 0.10, moderate: 0.20, large: 0.35 };

// 기본 D, S 직선 (정규화 좌표 0~1) → 픽셀 변환
// D: y = 0.9 - 0.7x (우하향), S: y = 0.15 + 0.7x (우상향)
// 교차점 (Q*, P*): 0.9-0.7Q = 0.15+0.7Q → Q* ≈ 0.536, P* ≈ 0.525
function nx(qNorm) { return PADL + qNorm * PW; }
function ny(pNorm) { return PADT + (1 - pNorm) * PH; }

// 곡선 shift 적용 → 새 P*, Q* 계산
function computeCurves(shifts) {
  let dIntercept = 0.9, dSlope = -0.7;   // D: P = 0.9 - 0.7Q
  let sIntercept = 0.15, sSlope = 0.7;   // S: P = 0.15 + 0.7Q
  for (const s of shifts || []) {
    const mag = MAG_TO_SHIFT[s.magnitude] || MAG_TO_SHIFT.moderate;
    if (s.direction === 'up' || s.direction === 'down') {
      // 수직 이동(절편 자체를 이동) — 외부성(PMC→SMC)·AD-AS 충격처럼 "같은 수량에서
      // 가격이 바뀌는" 경우다. D/S 구분 없이 부호가 같다: up=절편 증가.
      const vsign = s.direction === 'up' ? +1 : -1;
      if (s.curve === 'D') dIntercept += vsign * mag;
      else if (s.curve === 'S') sIntercept += vsign * mag;
    } else {
      const sign = s.direction === 'right' ? +1 : -1;
      if (s.curve === 'D') dIntercept += sign * mag;
      else if (s.curve === 'S') sIntercept += sign * mag * -1;  // S 우측 이동 = intercept 감소(=동일가격 더 많이 공급)
    }
  }
  // 교차점: dIntercept + dSlope*Q = sIntercept + sSlope*Q → Q = (dIntercept - sIntercept) / (sSlope - dSlope)
  const qStar = (dIntercept - sIntercept) / (sSlope - dSlope);
  const pStar = dIntercept + dSlope * qStar;
  return {
    d: { intercept: dIntercept, slope: dSlope },
    s: { intercept: sIntercept, slope: sSlope },
    qStar, pStar,
  };
}

function curveEndpoints(c) {
  // y = intercept + slope * x, x in [0, 1]
  return {
    x1: 0, y1: c.intercept,
    x2: 1, y2: c.intercept + c.slope,
  };
}

function clamp01(v) { return Math.max(0, Math.min(1, v)); }

function SupplyDemandChart({ params }) {
  const initial = computeCurves([]);   // 이동 전
  const final = computeCurves(params.shifts || []);
  const hasShift = (params.shifts || []).length > 0;
  const ann = params.annotations || {};
  const showInitialCurves = hasShift;

  const dColor = '#dc2626';
  const sColor = '#2563eb';
  const dInitColor = '#fca5a5';
  const sInitColor = '#93c5fd';

  const dFinal = curveEndpoints(final.d);
  const sFinal = curveEndpoints(final.s);
  const dInit = curveEndpoints(initial.d);
  const sInit = curveEndpoints(initial.s);

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
        {/* 축 라벨 */}
        <text x={nx(1) + 2} y={ny(0) + 4} fontSize={12} fill="#374151">{(params.axes?.x_label) || 'Q (수량)'}</text>
        <text x={nx(0) - 6} y={ny(1) - 6} fontSize={12} fill="#374151" textAnchor="end">{(params.axes?.y_label) || 'P (가격)'}</text>

        {/* 이동 전 곡선 (점선, 흐림) */}
        {showInitialCurves && (
          <>
            <line x1={nx(clamp01(dInit.x1))} y1={ny(clamp01(dInit.y1))} x2={nx(clamp01(dInit.x2))} y2={ny(clamp01(dInit.y2))}
              stroke={dInitColor} strokeWidth={1.5} strokeDasharray="4 4" />
            <line x1={nx(clamp01(sInit.x1))} y1={ny(clamp01(sInit.y1))} x2={nx(clamp01(sInit.x2))} y2={ny(clamp01(sInit.y2))}
              stroke={sInitColor} strokeWidth={1.5} strokeDasharray="4 4" />
            <text x={nx(clamp01(dInit.x2)) - 4} y={ny(clamp01(dInit.y2)) + 14} fontSize={11} fill={dInitColor} textAnchor="end">D₀</text>
            <text x={nx(clamp01(sInit.x2)) - 4} y={ny(clamp01(sInit.y2)) - 6} fontSize={11} fill={sInitColor} textAnchor="end">S₀</text>
          </>
        )}

        {/* 이동 후(또는 단일) 곡선 */}
        <line x1={nx(clamp01(dFinal.x1))} y1={ny(clamp01(dFinal.y1))} x2={nx(clamp01(dFinal.x2))} y2={ny(clamp01(dFinal.y2))}
          stroke={dColor} strokeWidth={2.2} />
        <line x1={nx(clamp01(sFinal.x1))} y1={ny(clamp01(sFinal.y1))} x2={nx(clamp01(sFinal.x2))} y2={ny(clamp01(sFinal.y2))}
          stroke={sColor} strokeWidth={2.2} />
        <text x={nx(clamp01(dFinal.x2)) - 4} y={ny(clamp01(dFinal.y2)) + 14} fontSize={12} fontWeight={700} fill={dColor} textAnchor="end">{hasShift ? 'D₁' : 'D'}</text>
        <text x={nx(clamp01(sFinal.x2)) - 4} y={ny(clamp01(sFinal.y2)) - 6} fontSize={12} fontWeight={700} fill={sColor} textAnchor="end">{hasShift ? 'S₁' : 'S'}</text>

        {/* 균형점 점선 가이드 */}
        <line x1={nx(final.qStar)} y1={ny(0)} x2={nx(final.qStar)} y2={ny(final.pStar)} stroke="#6b7280" strokeWidth={1} strokeDasharray="2 3" />
        <line x1={nx(0)} y1={ny(final.pStar)} x2={nx(final.qStar)} y2={ny(final.pStar)} stroke="#6b7280" strokeWidth={1} strokeDasharray="2 3" />

        {/* 균형점 마커 */}
        {showInitialCurves && (
          <>
            <circle cx={nx(initial.qStar)} cy={ny(initial.pStar)} r={4} fill="#fff" stroke="#9ca3af" strokeWidth={2} />
            <text x={nx(initial.qStar) + 6} y={ny(initial.pStar) - 6} fontSize={11} fill="#6b7280">E₀</text>
          </>
        )}
        <circle cx={nx(final.qStar)} cy={ny(final.pStar)} r={5} fill="#111827" />
        <text x={nx(final.qStar) + 8} y={ny(final.pStar) - 6} fontSize={12} fontWeight={700} fill="#111827">{hasShift ? 'E₁' : 'E*'}</text>

        {/* 가격·수량 변화량 화살표 */}
        {showInitialCurves && ann.price_change?.show_arrow && (
          <ChangeArrow
            x1={nx(0) - 16} y1={ny(initial.pStar)}
            x2={nx(0) - 16} y2={ny(final.pStar)}
            label={ann.price_change.label || (final.pStar > initial.pStar ? 'ΔP↑' : 'ΔP↓')}
            color="#7c3aed"
            labelPos="left"
          />
        )}
        {showInitialCurves && ann.quantity_change?.show_arrow && (
          <ChangeArrow
            x1={nx(initial.qStar)} y1={ny(0) + 16}
            x2={nx(final.qStar)} y2={ny(0) + 16}
            label={ann.quantity_change.label || (final.qStar > initial.qStar ? 'ΔQ↑' : 'ΔQ↓')}
            color="#7c3aed"
            labelPos="below"
          />
        )}
      </svg>
      {/* shift 이유 자동 표시 */}
      {hasShift && (
        <ul style={{ margin: '6px 0 0', padding: '0 0 0 18px', fontSize: '0.78rem', color: '#374151', lineHeight: 1.5 }}>
          {params.shifts.map((s, i) => (
            <li key={i}>
              <strong>{s.curve === 'D' ? '수요' : '공급'}</strong> {
                { left: '좌측', right: '우측', up: '상방', down: '하방' }[s.direction] || s.direction
              } 이동
              {s.magnitude && s.magnitude !== 'moderate' && ` (${s.magnitude === 'small' ? '소폭' : '대폭'})`}
              {s.reason && ` — ${s.reason}`}
            </li>
          ))}
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

function ChangeArrow({ x1, y1, x2, y2, label, color, labelPos }) {
  const dx = x2 - x1, dy = y2 - y1;
  const len = Math.hypot(dx, dy);
  if (len < 4) return null;
  const ux = dx / len, uy = dy / len;
  const headLen = 6;
  // 화살촉 점
  const hx1 = x2 - headLen * (ux + uy);
  const hy1 = y2 - headLen * (uy - ux);
  const hx2 = x2 - headLen * (ux - uy);
  const hy2 = y2 - headLen * (uy + ux);
  return (
    <g>
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={1.6} />
      <polyline points={`${hx1},${hy1} ${x2},${y2} ${hx2},${hy2}`} fill="none" stroke={color} strokeWidth={1.6} />
      {label && (
        <text
          x={labelPos === 'left' ? x1 - 4 : (x1 + x2) / 2}
          y={labelPos === 'below' ? y1 + 14 : (y1 + y2) / 2}
          fontSize={11} fill={color} fontWeight={700}
          textAnchor={labelPos === 'left' ? 'end' : 'middle'}
        >
          {label}
        </text>
      )}
    </g>
  );
}

export const supplyDemandTemplate = {
  name: 'supply-demand',
  version: 1,
  subjects: ['economics'],
  helpText: '수요공급 곡선 (이동·균형점·변화량)',
  Component: SupplyDemandChart,
  schema: {
    type: 'object',
    required: [],
    properties: {
      scenario: { type: 'string' },
      shifts: {
        type: 'array',
        items: {
          type: 'object',
          required: ['curve', 'direction'],
          properties: {
            curve: { enum: ['D', 'S'] },
            direction: { enum: ['left', 'right', 'up', 'down'] },
            magnitude: { enum: ['small', 'moderate', 'large'], default: 'moderate' },
            reason: { type: 'string' },
          },
        },
      },
      annotations: {
        type: 'object',
        properties: {
          price_change: { type: 'object', properties: { show_arrow: { type: 'boolean' }, label: { type: 'string' } } },
          quantity_change: { type: 'object', properties: { show_arrow: { type: 'boolean' }, label: { type: 'string' } } },
        },
      },
      axes: {
        type: 'object',
        properties: { x_label: { type: 'string' }, y_label: { type: 'string' } },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '소득 증가로 수요 우측 이동',
    shifts: [{ curve: 'D', direction: 'right', magnitude: 'moderate', reason: '정상재 수요 ↑' }],
    annotations: {
      price_change: { show_arrow: true },
      quantity_change: { show_arrow: true },
    },
    narration: '수요 증가로 균형 가격·수량 모두 상승.',
  },
};
