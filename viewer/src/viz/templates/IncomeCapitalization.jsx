// 수익환원법 — 직접환원 흐름 시각화.
// PGI → -공실/대손 → EGI → -운영비 → NOI ÷ 환원이율 → V.
// 각 step 카드 + 산식·금액·해설.

function fmt(n) {
  if (typeof n !== 'number') return n || '';
  return n.toLocaleString('ko-KR');
}

function StepCard({ label, value, formula, color, note }) {
  return (
    <div style={{
      flex: '0 0 auto', minWidth: 130,
      padding: '8px 10px',
      background: color.bg, border: `1.5px solid ${color.border}`,
      borderRadius: 8,
    }}>
      <div style={{ fontSize: '0.72rem', color: color.text, fontWeight: 700, marginBottom: 2 }}>{label}</div>
      <div style={{ fontSize: '0.92rem', fontWeight: 800, color: color.text, fontFamily: 'ui-monospace, monospace' }}>
        {typeof value === 'number' ? fmt(value) : (value || '—')}
      </div>
      {formula && <div style={{ marginTop: 2, fontSize: '0.7rem', color: '#6b7280' }}>{formula}</div>}
      {note && <div style={{ marginTop: 2, fontSize: '0.7rem', color: '#92400e' }}>⚠️ {note}</div>}
    </div>
  );
}

function ArrowDown() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '4px 0' }}>
      <svg width={20} height={20}>
        <line x1={10} y1={0} x2={10} y2={14} stroke="#9ca3af" strokeWidth={2} />
        <polyline points="4,12 10,18 16,12" fill="none" stroke="#9ca3af" strokeWidth={2} />
      </svg>
    </div>
  );
}

function IncomeCapitalizationChart({ params }) {
  const pgi = params.pgi;
  const vacancy = params.vacancy_loss || 0;
  const egi = typeof params.egi === 'number' ? params.egi : (typeof pgi === 'number' ? pgi - vacancy : null);
  const opex = params.operating_expenses || 0;
  const noi = typeof params.noi === 'number' ? params.noi : (typeof egi === 'number' ? egi - opex : null);
  const capRate = params.cap_rate;  // 0.06 등 비율
  const value = typeof params.value === 'number' ? params.value
    : (typeof noi === 'number' && typeof capRate === 'number' && capRate > 0 ? noi / capRate : null);

  const blue = { bg: '#dbeafe', border: '#1d4ed8', text: '#1e40af' };
  const orange = { bg: '#ffedd5', border: '#c2410c', text: '#9a3412' };
  const red = { bg: '#fee2e2', border: '#b91c1c', text: '#991b1b' };
  const green = { bg: '#d1fae5', border: '#047857', text: '#065f46' };
  const purple = { bg: '#ede9fe', border: '#6d28d9', text: '#5b21b6' };

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 14, maxWidth: 680 }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 10 }}>
          🏠 {params.scenario}
        </figcaption>
      )}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 0, alignItems: 'stretch' }}>
        <StepCard label="가능총수익 (PGI)" value={pgi} formula="임대료 × 임대면적" color={blue} />
        {vacancy > 0 && (
          <>
            <ArrowDown />
            <StepCard label="− 공실·대손손실" value={vacancy} formula={`PGI × 공실률 (${params.vacancy_rate ? (params.vacancy_rate * 100).toFixed(1) + '%' : '?'})`} color={orange} />
          </>
        )}
        <ArrowDown />
        <StepCard label="유효총수익 (EGI)" value={egi} formula="PGI − 공실·대손" color={blue} />
        {opex > 0 && (
          <>
            <ArrowDown />
            <StepCard label="− 운영경비 (OE)" value={opex} formula="제세공과·관리비·수선비 등 (자본적 지출 X)" color={red} note={params.opex_note} />
          </>
        )}
        <ArrowDown />
        <StepCard label="순영업소득 (NOI)" value={noi} formula="EGI − OE" color={green} />
        <ArrowDown />
        <div style={{
          padding: '8px 10px',
          background: purple.bg, border: `1.5px solid ${purple.border}`,
          borderRadius: 8,
        }}>
          <div style={{ fontSize: '0.72rem', color: purple.text, fontWeight: 700, marginBottom: 2 }}>÷ 환원이율 (R)</div>
          <div style={{ fontSize: '0.92rem', fontWeight: 800, color: purple.text, fontFamily: 'ui-monospace, monospace' }}>
            {typeof capRate === 'number' ? `${(capRate * 100).toFixed(2)}%` : '?'}
          </div>
          {params.cap_rate_method && (
            <div style={{ marginTop: 2, fontSize: '0.7rem', color: '#6b7280' }}>
              산정법: {params.cap_rate_method}
            </div>
          )}
        </div>
        <ArrowDown />
        <div style={{
          padding: '12px 14px',
          background: '#fef3c7', border: `2px solid #f59e0b`,
          borderRadius: 10,
        }}>
          <div style={{ fontSize: '0.78rem', color: '#92400e', fontWeight: 800, marginBottom: 4 }}>
            ➡ 부동산 가치 (V)
          </div>
          <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#7c2d12', fontFamily: 'ui-monospace, monospace' }}>
            {typeof value === 'number' ? fmt(value) + ' 원' : '?'}
          </div>
          <div style={{ marginTop: 2, fontSize: '0.72rem', color: '#92400e' }}>V = NOI ÷ R</div>
        </div>
      </div>
      {params.narration && (
        <p style={{ margin: '10px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const incomeCapitalizationTemplate = {
  name: 'income-capitalization',
  version: 1,
  subjects: ['appraisal_practice', 'realestate'],
  helpText: '수익환원법 직접환원 흐름 (PGI → NOI → V)',
  Component: IncomeCapitalizationChart,
  schema: {
    type: 'object',
    properties: {
      scenario: { type: 'string' },
      pgi: { type: 'number' },
      vacancy_loss: { type: 'number' },
      vacancy_rate: { type: 'number' },
      egi: { type: 'number' },
      operating_expenses: { type: 'number' },
      opex_note: { type: 'string' },
      noi: { type: 'number' },
      cap_rate: { type: 'number' },
      cap_rate_method: { type: 'string' },
      value: { type: 'number' },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '근린상가 직접환원 평가',
    pgi: 120000000,
    vacancy_rate: 0.05,
    vacancy_loss: 6000000,
    operating_expenses: 24000000,
    cap_rate: 0.07,
    cap_rate_method: '시장추출법 (인근 유사사례 평균)',
    narration: 'NOI 9천만 / 환원이율 7% → 약 12.86억. 자본적 지출은 OE 제외.',
  },
};
