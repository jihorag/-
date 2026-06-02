// 답안 양식 골격 — 감정평가이론(2차) 빈출 양식 시각화.
// 골격: Ⅰ. 서론/논점 도입 → Ⅱ. 본론 (2-3목차) → Ⅲ. 결론·유의사항.
// 각 목차에 keywords·page guide·필수 인용·시간 가이드.

function AnswerTemplateChart({ params }) {
  const sections = params.sections || [];
  const scorePoint = params.score_point;
  const timeMin = params.time_minutes;

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 14, maxWidth: 720 }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 10, paddingBottom: 8, borderBottom: '2px solid #4f46e5' }}>
        <div>
          <div style={{ fontSize: '0.74rem', color: '#6b7280', fontWeight: 700, letterSpacing: '0.04em' }}>답안 양식</div>
          <h3 style={{ margin: '2px 0 0', fontSize: '1.05rem', fontWeight: 800, color: '#111827' }}>
            📝 {params.topic || '답안 골격'}
          </h3>
        </div>
        <div style={{ textAlign: 'right', fontSize: '0.78rem', color: '#475569' }}>
          {typeof scorePoint === 'number' && <div style={{ fontWeight: 800, color: '#4338ca' }}>{scorePoint}점</div>}
          {typeof timeMin === 'number' && <div>⏱ 약 {timeMin}분</div>}
        </div>
      </header>
      {params.issue && (
        <div style={{
          padding: '6px 10px', marginBottom: 10, background: '#fef3c7',
          borderRadius: 6, fontSize: '0.82rem', color: '#92400e',
        }}>
          🎯 출제 의도: {params.issue}
        </div>
      )}
      {sections.map((sec, i) => {
        const romanNumeral = ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ'][i] || (i + 1);
        return (
          <section key={i} style={{
            marginBottom: 10, padding: '10px 12px',
            background: sec.level === 1 ? '#eef2ff' : '#fff',
            border: `1px solid ${sec.level === 1 ? '#c7d2fe' : '#e5e7eb'}`,
            borderRadius: 8,
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 4 }}>
              <div style={{ fontSize: '0.92rem', fontWeight: 800, color: sec.level === 1 ? '#4338ca' : '#374151' }}>
                {romanNumeral}. {sec.title}
              </div>
              {sec.lines && (
                <div style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 600 }}>
                  ≈ {sec.lines}줄
                </div>
              )}
            </div>
            {sec.description && (
              <div style={{ fontSize: '0.82rem', color: '#374151', lineHeight: 1.55, marginBottom: sec.subsections || sec.keywords ? 6 : 0 }}>
                {sec.description}
              </div>
            )}
            {sec.subsections && sec.subsections.length > 0 && (
              <ol style={{ margin: '4px 0', paddingLeft: 20, fontSize: '0.82rem', color: '#374151', lineHeight: 1.55 }}>
                {sec.subsections.map((sub, k) => (
                  <li key={k} style={{ marginBottom: 2 }}>
                    <strong>{sub.title}</strong>{sub.description ? ` — ${sub.description}` : ''}
                  </li>
                ))}
              </ol>
            )}
            {sec.keywords && sec.keywords.length > 0 && (
              <div style={{ marginTop: 4, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                <span style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700, alignSelf: 'center' }}>핵심 키워드:</span>
                {sec.keywords.map((kw, k) => (
                  <span key={k} style={{
                    padding: '2px 8px', borderRadius: 4,
                    background: '#dbeafe', color: '#1e40af',
                    fontSize: '0.74rem', fontWeight: 700,
                  }}>{kw}</span>
                ))}
              </div>
            )}
            {sec.must_cite && sec.must_cite.length > 0 && (
              <div style={{ marginTop: 4, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                <span style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700, alignSelf: 'center' }}>필수 인용:</span>
                {sec.must_cite.map((c, k) => (
                  <span key={k} style={{
                    padding: '2px 8px', borderRadius: 4,
                    background: '#fef3c7', color: '#92400e',
                    fontSize: '0.74rem', fontWeight: 700,
                  }}>★ {c}</span>
                ))}
              </div>
            )}
          </section>
        );
      })}
      {params.tips && params.tips.length > 0 && (
        <div style={{
          padding: '8px 10px', marginTop: 6, background: '#fef9c3',
          border: '1px solid #fde047', borderRadius: 8,
          fontSize: '0.78rem', color: '#854d0e', lineHeight: 1.5,
        }}>
          <strong>💡 답안 작성 팁</strong>
          <ul style={{ margin: '4px 0 0', paddingLeft: 18 }}>
            {params.tips.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </div>
      )}
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const answerTemplateChart = {
  name: 'answer-template',
  version: 1,
  subjects: ['appraisal_theory', 'appraisal_law', 'appraisal_practice'],
  helpText: '답안 양식 골격 (Ⅰ·Ⅱ·Ⅲ + 키워드·필수 인용·시간 가이드)',
  Component: AnswerTemplateChart,
  schema: {
    type: 'object',
    required: ['sections'],
    properties: {
      topic: { type: 'string' },
      score_point: { type: 'number' },
      time_minutes: { type: 'number' },
      issue: { type: 'string' },
      sections: {
        type: 'array',
        minItems: 2,
        items: {
          type: 'object',
          required: ['title'],
          properties: {
            title: { type: 'string' },
            description: { type: 'string' },
            level: { type: 'number' },  // 1=강조, 2=일반
            lines: { type: 'string' },  // "5-7"
            subsections: {
              type: 'array',
              items: {
                type: 'object',
                required: ['title'],
                properties: {
                  title: { type: 'string' },
                  description: { type: 'string' },
                },
              },
            },
            keywords: { type: 'array', items: { type: 'string' } },
            must_cite: { type: 'array', items: { type: 'string' } },  // ★ 강조 인용
          },
        },
      },
      tips: { type: 'array', items: { type: 'string' } },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    topic: '감정평가의 3방식',
    score_point: 30,
    time_minutes: 30,
    issue: '3방식의 본질·관계·실무 적용',
    sections: [
      {
        title: '서론 — 논점 도입',
        level: 1,
        lines: '4-5',
        description: '감정평가의 정의 및 3방식 도입 의의',
        keywords: ['감정평가 정의', '3방식 본질'],
      },
      {
        title: '본론 — 3방식 각각',
        level: 1,
        lines: '15-18',
        subsections: [
          { title: '원가방식', description: '재조달원가 + 감가수정 → 적산가액' },
          { title: '비교방식', description: '거래사례 보정 (사정·시점·지역·개별) → 비준가액' },
          { title: '수익방식', description: '순영업소득 ÷ 환원이율 → 수익가액' },
        ],
        keywords: ['적산가액', '비준가액', '수익가액', '감가수정'],
      },
      {
        title: '결론 — 본질 관계 + 유의사항',
        level: 1,
        lines: '4-5',
        description: '3방식 병용 원칙 (감정평가법 제3조) + 시산가액 조정의 합리성',
        must_cite: ['감정평가법 제3조', '감정평가실무기준'],
      },
    ],
    tips: [
      '본론 3목차는 동일 양식(정의·산식·장단점)으로 통일하면 채점자 추적 쉬움',
      '결론에 "병용 원칙" 명시 — 단일 방식 X',
      '시산가액 조정은 "합리성" 기준',
    ],
    narration: '이론 30점 표준 양식. Ⅰ서·Ⅱ본·Ⅲ결의 비율 1:3:1이 목표.',
  },
};
