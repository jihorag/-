// 비용곡선 — MC / AC / AVC / AFC + profit-max marker (P = MC).
// 의미 파라미터: which curves visible, P (시장가격), 이윤영역 표시 여부.
// 곡선은 단순화한 함수형 (q ∈ [0.05, 1]).

const W = 520, H = 380, PADL = 50, PADB = 50, PADT = 24, PADR = 30;
const PW = W - PADL - PADR;
const PH = H - PADT - PADB;

function nx(q) { return PADL + q * PW; }
function ny(p) { return PADT + (1 - p) * PH; }

// 단순화한 U자 비용곡선 (모든 값 0~1 정규화)
function avc(q) { return 0.20 + 0.6 * (q - 0.55) * (q - 0.55); }
function afc(q) { return 0.06 / Math.max(q, 0.05); }
function ac(q)  { return avc(q) + afc(q); }
function mc(q)  { return 0.20 + 1.8 * (q - 0.55) * (q - 0.55) + 0.20 * (q - 0.55); }

function buildPath(fn, qStart = 0.07, qEnd = 0.98, steps = 60) {
  const pts = [];
  for (let i = 0; i <= steps; i++) {
    const q = qStart + (qEnd - qStart) * (i / steps);
    const p = Math.max(0, Math.min(1.0, fn(q)));
    pts.push([nx(q), ny(p)]);
  }
  return pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');
}

// MC 와 AC 교차점 — 수치 검색 (AC 최저점에서 MC = AC)
function findIntersect(f1, f2, qStart = 0.2, qEnd = 0.98) {
  let bestQ = null, bestDiff = Infinity;
  for (let i = 0; i <= 200; i++) {
    const q = qStart + (qEnd - qStart) * (i / 200);
    const d = Math.abs(f1(q) - f2(q));
    if (d < bestDiff) { bestDiff = d; bestQ = q; }
  }
  return { q: bestQ, p: f1(bestQ) };
}

// P = MC 조건의 q (이윤 극대화 — uphill 부분 사용)
function profitMaxQ(p) {
  for (let i = 200; i >= 0; i--) {
    const q = 0.5 + (0.98 - 0.5) * (i / 200);
    if (mc(q) <= p) return q;
  }
  return null;
}

const CURVE_STYLE = {
  MC:  { color: '#dc2626', label: 'MC' },
  AC:  { color: '#1d4ed8', label: 'AC' },
  AVC: { color: '#0891b2', label: 'AVC' },
  AFC: { color: '#7c3aed', label: 'AFC' },
};

function CostCurvesChart({ params }) {
  const visible = params.curves_visible || ['MC', 'AC', 'AVC'];
  const fnByName = { MC: mc, AC: ac, AVC: avc, AFC: afc };
  const marketP = typeof params.market_price === 'number' ? Math.max(0, Math.min(1, params.market_price)) : null;
  const profitVisible = !!params.profit_visible && marketP !== null;
  const acMcCross = findIntersect(mc, ac);

  // 이윤 영역: P*q* (가격×수량 사각형) − AC*q* (총비용 사각형)
  const qStar = marketP !== null ? profitMaxQ(marketP) : null;
  const acAtQ = qStar !== null ? ac(qStar) : null;

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12 }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 6 }}>
          📊 {params.scenario}
        </figcaption>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', maxWidth: 560, display: 'block' }}>
        {/* 축 */}
        <line x1={nx(0)} y1={ny(0)} x2={nx(1)} y2={ny(0)} stroke="#9ca3af" strokeWidth={1.5} />
        <line x1={nx(0)} y1={ny(0)} x2={nx(0)} y2={ny(1)} stroke="#9ca3af" strokeWidth={1.5} />
        <text x={nx(1) + 2} y={ny(0) + 4} fontSize={12} fill="#374151">{params.x_label || 'Q (산출량)'}</text>
        <text x={nx(0) - 6} y={ny(1) - 6} fontSize={12} fill="#374151" textAnchor="end">{params.y_label || 'C, P'}</text>

        {/* 이윤 영역 (P > AC) — 사각형 */}
        {profitVisible && qStar !== null && marketP > acAtQ && (
          <rect
            x={nx(0)} y={ny(marketP)}
            width={nx(qStar) - nx(0)} height={ny(acAtQ) - ny(marketP)}
            fill="#bbf7d0" fillOpacity={0.5} stroke="#16a34a" strokeWidth={1} strokeDasharray="3 3"
          />
        )}
        {profitVisible && qStar !== null && marketP < acAtQ && (
          <rect
            x={nx(0)} y={ny(acAtQ)}
            width={nx(qStar) - nx(0)} height={ny(marketP) - ny(acAtQ)}
            fill="#fecaca" fillOpacity={0.5} stroke="#dc2626" strokeWidth={1} strokeDasharray="3 3"
          />
        )}

        {/* 시장 가격선 P */}
        {marketP !== null && (
          <g>
            <line x1={nx(0)} y1={ny(marketP)} x2={nx(1)} y2={ny(marketP)} stroke="#111827" strokeWidth={1.5} strokeDasharray="6 4" />
            <text x={nx(1) + 4} y={ny(marketP) + 4} fontSize={11} fontWeight={700} fill="#111827">P</text>
          </g>
        )}

        {/* 비용곡선들 */}
        {visible.map((name) => {
          const style = CURVE_STYLE[name];
          const fn = fnByName[name];
          if (!style || !fn) return null;
          const d = buildPath(fn);
          return (
            <g key={name}>
              <path d={d} fill="none" stroke={style.color} strokeWidth={2.2} />
              <text x={nx(0.96)} y={ny(fn(0.96)) - 6} fontSize={12} fontWeight={700} fill={style.color} textAnchor="end">{style.label}</text>
            </g>
          );
        })}

        {/* AC 최저점 = MC 교점 */}
        {visible.includes('AC') && visible.includes('MC') && (
          <circle cx={nx(acMcCross.q)} cy={ny(acMcCross.p)} r={3.5} fill="#fff" stroke="#1d4ed8" strokeWidth={2} />
        )}

        {/* 이윤 극대화 점 (P = MC) */}
        {qStar !== null && (
          <g>
            <line x1={nx(qStar)} y1={ny(0)} x2={nx(qStar)} y2={ny(marketP)} stroke="#6b7280" strokeWidth={1} strokeDasharray="2 3" />
            <circle cx={nx(qStar)} cy={ny(marketP)} r={5} fill="#111827" />
            <text x={nx(qStar) + 8} y={ny(marketP) - 8} fontSize={12} fontWeight={800} fill="#111827">Q*</text>
            <text x={nx(qStar)} y={ny(0) + 14} fontSize={11} fill="#374151" textAnchor="middle">Q*</text>
          </g>
        )}
      </svg>
      {/* 자동 해설 */}
      <div style={{ marginTop: 6, fontSize: '0.78rem', color: '#374151', lineHeight: 1.55 }}>
        {visible.includes('AC') && visible.includes('MC') && (
          <div>• AC 최저점에서 <strong style={{ color: '#1d4ed8' }}>MC = AC</strong> (위에서 아래로 통과) — 손익분기점</div>
        )}
        {profitVisible && qStar !== null && (
          <div>• P = MC 조건에서 <strong>Q* ≈ {(qStar * 100).toFixed(0)}%</strong>, {marketP > acAtQ ? <span style={{ color: '#15803d', fontWeight: 700 }}>초과이윤 발생 (P &gt; AC)</span> : <span style={{ color: '#b91c1c', fontWeight: 700 }}>손실 발생 (P &lt; AC)</span>}</div>
        )}
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const costCurvesTemplate = {
  name: 'cost-curves',
  version: 1,
  subjects: ['economics'],
  helpText: '비용곡선 (MC/AC/AVC/AFC + 시장가격 P + 이윤극대화 Q*)',
  Component: CostCurvesChart,
  schema: {
    type: 'object',
    properties: {
      scenario: { type: 'string' },
      curves_visible: {
        type: 'array',
        items: { enum: ['MC', 'AC', 'AVC', 'AFC'] },
      },
      market_price: { type: 'number' },     // 0~1 정규화 가격
      profit_visible: { type: 'boolean' },  // 이윤·손실 사각형 표시
      x_label: { type: 'string' },
      y_label: { type: 'string' },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '완전경쟁기업의 이윤극대화 (P > AC 최저점)',
    curves_visible: ['MC', 'AC', 'AVC'],
    market_price: 0.55,
    profit_visible: true,
    narration: 'P = MC 에서 Q* 결정, P > AC 이므로 초과이윤 발생.',
  },
};
