// 사례형 답안 IRAC 구조 — 보상법규(2차) 빈출.
// I(사실관계 정리) → R(법령·조문) → A(학설·판례 적용) → C(포섭·결론).
// 각 단계에 시간 가이드·필수 인용·체크포인트.

const STEP_STYLES = {
  I: { label: 'Issue', color: '#dc2626', bg: '#fee2e2', border: '#fecaca', icon: '①' },
  R: { label: 'Rule', color: '#1d4ed8', bg: '#dbeafe', border: '#bfdbfe', icon: '②' },
  A: { label: 'Application', color: '#7c3aed', bg: '#ede9fe', border: '#ddd6fe', icon: '③' },
  C: { label: 'Conclusion', color: '#047857', bg: '#d1fae5', border: '#a7f3d0', icon: '④' },
};

function ExamPatternChart({ params }) {
  const steps = params.steps || [];
  const scorePoint = params.score_point;
  const timeMin = params.time_minutes;

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 14, maxWidth: 760 }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 10, paddingBottom: 8, borderBottom: '2px solid #6366f1' }}>
        <div>
          <div style={{ fontSize: '0.74rem', color: '#6b7280', fontWeight: 700, letterSpacing: '0.04em' }}>사례형 IRAC 구조</div>
          <h3 style={{ margin: '2px 0 0', fontSize: '1.05rem', fontWeight: 800, color: '#111827' }}>
            ⚖️ {params.topic || '사례 답안'}
          </h3>
        </div>
        <div style={{ textAlign: 'right', fontSize: '0.78rem', color: '#475569' }}>
          {typeof scorePoint === 'number' && <div style={{ fontWeight: 800, color: '#4338ca' }}>{scorePoint}점</div>}
          {typeof timeMin === 'number' && <div>⏱ 약 {timeMin}분</div>}
        </div>
      </header>
      {params.case_facts && (
        <div style={{
          padding: '8px 12px', marginBottom: 10, background: '#fef3c7',
          border: '1px solid #fde047', borderRadius: 8,
          fontSize: '0.84rem', color: '#854d0e', lineHeight: 1.55,
        }}>
          <strong>📋 사실관계</strong><br />
          {params.case_facts}
        </div>
      )}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {steps.map((step, i) => {
          const style = STEP_STYLES[step.kind] || STEP_STYLES.A;
          return (
            <div key={i} style={{
              display: 'grid', gridTemplateColumns: '40px 1fr', gap: 10,
              alignItems: 'start',
            }}>
              {/* 단계 표시 */}
              <div style={{
                display: 'flex', flexDirection: 'column', alignItems: 'center',
                paddingTop: 8,
              }}>
                <div style={{
                  width: 32, height: 32, borderRadius: '50%',
                  background: style.color, color: '#fff',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '0.92rem', fontWeight: 800,
                }}>
                  {step.kind}
                </div>
                {i < steps.length - 1 && (
                  <div style={{ width: 2, flex: 1, background: '#e5e7eb', marginTop: 4, minHeight: 20 }} />
                )}
              </div>
              {/* 카드 */}
              <div style={{
                padding: '10px 12px',
                background: style.bg, border: `1.5px solid ${style.border}`,
                borderRadius: 8, marginBottom: 4,
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 4 }}>
                  <div style={{ fontSize: '0.88rem', fontWeight: 800, color: style.color }}>
                    {step.label || style.label}
                  </div>
                  {step.lines && (
                    <div style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 600 }}>
                      ≈ {step.lines}줄
                    </div>
                  )}
                </div>
                {step.description && (
                  <div style={{ fontSize: '0.82rem', color: '#111827', lineHeight: 1.55, marginBottom: 6 }}>
                    {step.description}
                  </div>
                )}
                {step.checkpoints && step.checkpoints.length > 0 && (
                  <ul style={{ margin: '4px 0', paddingLeft: 18, fontSize: '0.8rem', color: '#374151', lineHeight: 1.55 }}>
                    {step.checkpoints.map((c, k) => <li key={k}>{c}</li>)}
                  </ul>
                )}
                {(step.articles || step.cases) && (
                  <div style={{ marginTop: 6, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                    {(step.articles || []).map((a, k) => (
                      <span key={`a-${k}`} style={{
                        padding: '2px 8px', borderRadius: 4,
                        background: '#fff', border: `1px solid ${style.border}`,
                        fontSize: '0.74rem', fontWeight: 700, color: style.color,
                      }}>📜 {a}</span>
                    ))}
                    {(step.cases || []).map((c, k) => (
                      <span key={`c-${k}`} style={{
                        padding: '2px 8px', borderRadius: 4,
                        background: '#fff', border: `1px solid ${style.border}`,
                        fontSize: '0.74rem', fontWeight: 700, color: style.color,
                      }}>⚖️ {c}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
      {params.tips && params.tips.length > 0 && (
        <div style={{
          padding: '8px 10px', marginTop: 10, background: '#f0f9ff',
          border: '1px solid #bae6fd', borderRadius: 8,
          fontSize: '0.78rem', color: '#0369a1', lineHeight: 1.5,
        }}>
          <strong>💡 IRAC 작성 팁</strong>
          <ul style={{ margin: '4px 0 0', paddingLeft: 18 }}>
            {params.tips.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </div>
      )}
      {params.narration && (
        <p style={{ margin: '10px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const examPatternTemplate = {
  name: 'exam-pattern',
  version: 1,
  subjects: ['appraisal_law', 'law'],
  helpText: '사례형 답안 IRAC 구조 (사실→조문→판례→포섭)',
  Component: ExamPatternChart,
  schema: {
    type: 'object',
    required: ['steps'],
    properties: {
      topic: { type: 'string' },
      score_point: { type: 'number' },
      time_minutes: { type: 'number' },
      case_facts: { type: 'string' },
      steps: {
        type: 'array',
        minItems: 3,
        items: {
          type: 'object',
          required: ['kind'],
          properties: {
            kind: { enum: ['I', 'R', 'A', 'C'] },
            label: { type: 'string' },
            description: { type: 'string' },
            lines: { type: 'string' },
            checkpoints: { type: 'array', items: { type: 'string' } },
            articles: { type: 'array', items: { type: 'string' } },
            cases: { type: 'array', items: { type: 'string' } },
          },
        },
      },
      tips: { type: 'array', items: { type: 'string' } },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    topic: '잔여지수용 청구 사례',
    score_point: 40,
    time_minutes: 40,
    case_facts: '甲의 토지 1,000㎡ 중 700㎡ 수용 후 잔여지 300㎡가 부정형으로 남아 종전 사용 곤란. 甲이 잔여지 수용 청구.',
    steps: [
      {
        kind: 'I',
        label: '쟁점 (Issue)',
        lines: '3-4',
        description: '잔여지 수용 청구의 인정 요건과 가격 감소만의 인정 여부',
        checkpoints: ['청구 요건 명확화', '판례 분기점 강조'],
      },
      {
        kind: 'R',
        label: '관련 법령 (Rule)',
        lines: '6-8',
        description: '토지보상법 제74조 잔여지수용 청구 — 종래의 목적대로 사용 곤란할 것',
        articles: ['토지보상법 제74조 제1항', '토지보상법 시행령 제39조'],
      },
      {
        kind: 'A',
        label: '학설·판례 적용 (Application)',
        lines: '12-15',
        description: '판례는 "종래 사용목적 곤란" 기준 엄격 — 단순 가격 감소만으로는 부족',
        cases: ['대판 2008두822', '대판 2014두46669'],
        checkpoints: ['적극·소극 판례 대조', '판례 결정의 이유 명시'],
      },
      {
        kind: 'C',
        label: '포섭·결론 (Conclusion)',
        lines: '5-7',
        description: '甲의 잔여지 300㎡는 부정형·종래 농업 사용 곤란 → 청구 인용 가능',
        checkpoints: ['사실관계 → 요건 매핑', '결론 명확히', '재량 한계 언급'],
      },
    ],
    tips: [
      '판례 사건번호는 정확히 (대판 YYYY두NNNN)',
      'A 단계가 가장 길어야 함 (배점의 50% 이상)',
      'C 단계는 사실관계 요건을 다시 한 번 체크 후 결론',
    ],
    narration: 'IRAC는 사례형 40점 표준 구조. A(적용)에 시간·분량 집중.',
  },
};
