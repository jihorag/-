// 소비자/생산자 잉여 + 사중손실(deadweight) 영역 시각화.
// supply-demand 와 동일 D/S 기본 → 균형점 기준 잉여 삼각형.
// 정책 옵션: price_ceiling, price_floor, tax, subsidy (옵션 중 하나만)

const W = 480, H = 360, PADL = 50, PADB = 50, PADT = 24, PADR = 24;
const PW = W - PADL - PADR;
const PH = H - PADT - PADB;

function nx(q) { return PADL + q * PW; }
function ny(p) { return PADT + (1 - p) * PH; }

// D: P = 0.9 - 0.7Q,  S: P = 0.15 + 0.7Q  → Q* ≈ 0.536, P* ≈ 0.525
const dP = (q) => 0.9 - 0.7 * q;
const sP = (q) => 0.15 + 0.7 * q;
const dQ = (p) => (0.9 - p) / 0.7;
const sQ = (p) => (p - 0.15) / 0.7;

function SurplusAreasChart({ params }) {
  const qStar = (0.9 - 0.15) / (0.7 + 0.7);
  const pStar = dP(qStar);
  const csVisible = params.consumer_visible !== false;
  const psVisible = params.producer_visible !== false;
  const dwVisible = params.deadweight_visible || false;
  const policy = params.policy;  // {type: 'tax'|'ceiling'|'floor', value: 0~1}

  // 정책 적용
  let qActual = qStar, pBuyer = pStar, pSeller = pStar, dwArea = null;
  if (policy && policy.type === 'tax' && typeof policy.value === 'number') {
    // 종량세 t: 소비자 D 곡선 위에서, 공급자 S 위에서 → 새 균형: D 가격 - S 가격 = t
    const t = policy.value;
    // 균형: dP(q) - sP(q) = t  → 0.75 - 1.4q = t  → q = (0.75 - t)/1.4
    qActual = (0.75 - t) / 1.4;
    pBuyer = dP(qActual);
    pSeller = sP(qActual);
    // 사중손실: 삼각형 (Q_star - Q_actual) × t / 2
    dwArea = { qA: qActual, qB: qStar, pTop: pBuyer, pBot: pSeller };
  } else if (policy && policy.type === 'ceiling' && typeof policy.value === 'number') {
    const pCap = policy.value;
    if (pCap < pStar) {
      qActual = sQ(pCap);  // 공급량이 작아짐
      pBuyer = pCap;
      pSeller = pCap;
      dwArea = { qA: qActual, qB: qStar, pTop: dP(qActual), pBot: pCap };
    }
  } else if (policy && policy.type === 'floor' && typeof policy.value === 'number') {
    const pFloor = policy.value;
    if (pFloor > pStar) {
      qActual = dQ(pFloor);  // 수요량이 작아짐
      pBuyer = pFloor;
      pSeller = pFloor;
      dwArea = { qA: qActual, qB: qStar, pTop: pFloor, pBot: sP(qActual) };
    }
  } else if (policy && policy.type === 'subsidy' && typeof policy.value === 'number') {
    // 보조금 s: 조세의 반대 부호 — 판매자 수취가격이 구매자 지불가격보다 s 만큼 높다.
    // 균형: sP(q) - dP(q) = s → 1.4q - 0.75 = s → q = (0.75 + s)/1.4
    const s = policy.value;
    qActual = (0.75 + s) / 1.4;
    pBuyer = dP(qActual);
    pSeller = sP(qActual);
    // 사중손실: 과잉생산 구간(Q* ~ Q_actual)의 삼각형 — tax 와 반대로 qActual 이 더 크다.
    dwArea = { qA: qActual, qB: qStar, pTop: pSeller, pBot: pBuyer };
  }

  // 잉여 폴리곤 좌표
  const buildD = (q1, q2) => {
    const pts = [];
    const steps = 30;
    for (let i = 0; i <= steps; i++) {
      const q = q1 + (q2 - q1) * (i / steps);
      pts.push([nx(q), ny(dP(q))]);
    }
    return pts;
  };
  const buildS = (q1, q2) => {
    const pts = [];
    const steps = 30;
    for (let i = 0; i <= steps; i++) {
      const q = q1 + (q2 - q1) * (i / steps);
      pts.push([nx(q), ny(sP(q))]);
    }
    return pts;
  };
  const pointsAttr = (pts) => pts.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');

  // CS: D 위, P_buyer 아래 (0 ~ qActual)
  const csPolygon = [...buildD(0, qActual), [nx(qActual), ny(pBuyer)], [nx(0), ny(pBuyer)]];
  // PS: P_seller 위, S 아래 (0 ~ qActual)
  const psPolygon = [[nx(0), ny(pSeller)], [nx(qActual), ny(pSeller)], ...buildS(qActual, 0)];

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12 }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 6 }}>
          📊 {params.scenario}
        </figcaption>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', maxWidth: 520, display: 'block' }}>
        <line x1={nx(0)} y1={ny(0)} x2={nx(1)} y2={ny(0)} stroke="#9ca3af" strokeWidth={1.5} />
        <line x1={nx(0)} y1={ny(0)} x2={nx(0)} y2={ny(1)} stroke="#9ca3af" strokeWidth={1.5} />
        <text x={nx(1) + 2} y={ny(0) + 4} fontSize={12} fill="#374151">Q</text>
        <text x={nx(0) - 6} y={ny(1) - 6} fontSize={12} fill="#374151" textAnchor="end">P</text>

        {/* 잉여 영역 */}
        {csVisible && <polygon points={pointsAttr(csPolygon)} fill="#bfdbfe" fillOpacity={0.6} stroke="#2563eb" strokeWidth={1} />}
        {psVisible && <polygon points={pointsAttr(psPolygon)} fill="#bbf7d0" fillOpacity={0.6} stroke="#16a34a" strokeWidth={1} />}

        {/* 사중손실 영역 (정책 있을 때) */}
        {dwVisible && dwArea && (
          <polygon
            points={pointsAttr([
              [nx(dwArea.qA), ny(dwArea.pTop)],
              [nx(dwArea.qB), ny(pStar)],
              [nx(dwArea.qA), ny(dwArea.pBot)],
            ])}
            fill="#fecaca" fillOpacity={0.7} stroke="#dc2626" strokeWidth={1.5}
          />
        )}

        {/* D, S 곡선 */}
        <line x1={nx(0)} y1={ny(0.9)} x2={nx(1)} y2={ny(0.2)} stroke="#dc2626" strokeWidth={2.2} />
        <line x1={nx(0)} y1={ny(0.15)} x2={nx(1)} y2={ny(0.85)} stroke="#2563eb" strokeWidth={2.2} />
        <text x={nx(0.97)} y={ny(0.2) + 14} fontSize={12} fontWeight={700} fill="#dc2626" textAnchor="end">D</text>
        <text x={nx(0.97)} y={ny(0.85) - 6} fontSize={12} fontWeight={700} fill="#2563eb" textAnchor="end">S</text>

        {/* 균형점 */}
        <circle cx={nx(qStar)} cy={ny(pStar)} r={4} fill="#111827" />
        <text x={nx(qStar) + 8} y={ny(pStar) - 6} fontSize={11} fontWeight={700} fill="#111827">E*</text>

        {/* 정책 가격선 */}
        {policy && policy.type === 'ceiling' && (
          <>
            <line x1={nx(0)} y1={ny(policy.value)} x2={nx(1)} y2={ny(policy.value)} stroke="#f59e0b" strokeWidth={2} strokeDasharray="5 3" />
            <text x={nx(0.85)} y={ny(policy.value) - 4} fontSize={11} fontWeight={700} fill="#f59e0b">상한가</text>
          </>
        )}
        {policy && policy.type === 'floor' && (
          <>
            <line x1={nx(0)} y1={ny(policy.value)} x2={nx(1)} y2={ny(policy.value)} stroke="#f59e0b" strokeWidth={2} strokeDasharray="5 3" />
            <text x={nx(0.85)} y={ny(policy.value) - 4} fontSize={11} fontWeight={700} fill="#f59e0b">하한가</text>
          </>
        )}
      </svg>
      <div style={{ marginTop: 6, fontSize: '0.78rem', color: '#374151', lineHeight: 1.55 }}>
        {csVisible && <div>• <span style={{ background: '#bfdbfe', padding: '0 4px' }}>소비자 잉여 (CS)</span> — D 곡선과 P 가격선 사이</div>}
        {psVisible && <div>• <span style={{ background: '#bbf7d0', padding: '0 4px' }}>생산자 잉여 (PS)</span> — P 가격선과 S 곡선 사이</div>}
        {dwVisible && dwArea && <div>• <span style={{ background: '#fecaca', padding: '0 4px', color: '#7f1d1d' }}>사중손실 (DWL)</span> — {policy?.type === 'subsidy' ? '보조금으로 과잉생산된 구간의 손실' : '정책으로 거래 안 이뤄진 손실'}</div>}
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const surplusAreasTemplate = {
  name: 'surplus-areas',
  version: 1,
  subjects: ['economics'],
  helpText: '소비자/생산자 잉여 + 정책별 사중손실 영역',
  Component: SurplusAreasChart,
  schema: {
    type: 'object',
    properties: {
      scenario: { type: 'string' },
      consumer_visible: { type: 'boolean' },
      producer_visible: { type: 'boolean' },
      deadweight_visible: { type: 'boolean' },
      policy: {
        type: 'object',
        properties: {
          type: { enum: ['tax', 'ceiling', 'floor', 'subsidy'] },
          value: { type: 'number' },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '가격 상한제(ceiling) → 사중손실 발생',
    consumer_visible: true,
    producer_visible: true,
    deadweight_visible: true,
    policy: { type: 'ceiling', value: 0.4 },
    narration: '상한가 < 균형가 → 공급량 감소, 거래량 축소. CS 일부 + PS 일부가 사중손실로 전환.',
  },
};
