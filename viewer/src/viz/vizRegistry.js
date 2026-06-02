// 시각자료 템플릿 중앙 레지스트리.
// 각 템플릿: { name, version, schema, Component, exampleParams, helpText }
// 새 템플릿 추가는 templates/ 에 컴포넌트 만들고 여기 등록.

import { supplyDemandTemplate } from './templates/SupplyDemand';
import { tAccountTemplate } from './templates/TAccount';
import { legalRelationsTemplate } from './templates/LegalRelations';
import { balanceSheetTemplate } from './templates/BalanceSheet';
import { incomeStatementTemplate } from './templates/IncomeStatement';
import { claimFlowTemplate } from './templates/ClaimFlow';
import { costCurvesTemplate } from './templates/CostCurves';
import { isLmTemplate } from './templates/IsLm';
import { caseComparisonTemplate } from './templates/CaseComparison';
import { incomeCapitalizationTemplate } from './templates/IncomeCapitalization';
import { dcfTimelineTemplate } from './templates/DcfTimeline';
import { phillipsCurveTemplate } from './templates/PhillipsCurve';
import { indifferenceBudgetTemplate } from './templates/IndifferenceBudget';
import { surplusAreasTemplate } from './templates/SurplusAreas';
import { elasticityZonesTemplate } from './templates/ElasticityZones';
import { salesAdjustmentTemplate } from './templates/SalesAdjustment';
import { answerTemplateChart } from './templates/AnswerTemplate';
import { examPatternTemplate } from './templates/ExamPattern';

const _registry = new Map();

function register(t) {
  if (_registry.has(t.name)) {
    // 중복 등록 시 경고만, 덮어쓰기 허용 (HMR 호환)
    console.warn(`[viz] duplicate template: ${t.name}`);
  }
  _registry.set(t.name, t);
}

// 경제 (8)
register(supplyDemandTemplate);
register(costCurvesTemplate);
register(isLmTemplate);
register(phillipsCurveTemplate);
register(indifferenceBudgetTemplate);
register(surplusAreasTemplate);
register(elasticityZonesTemplate);
// 회계 (3)
register(tAccountTemplate);
register(balanceSheetTemplate);
register(incomeStatementTemplate);
// 법 — 민법·법규·보상법규 (3)
register(legalRelationsTemplate);
register(claimFlowTemplate);
register(caseComparisonTemplate);
// 부동산·감정평가실무 (3)
register(incomeCapitalizationTemplate);
register(dcfTimelineTemplate);
register(salesAdjustmentTemplate);
// 2차 답안 양식 (2)
register(answerTemplateChart);
register(examPatternTemplate);

export function getTemplate(name) {
  return _registry.get(name);
}

export function listTemplates() {
  return Array.from(_registry.values());
}

// AI 시스템 프롬프트에 주입할 카탈로그 텍스트 생성 (per-subject 필터).
// subjects: 단일 string (subject_id) 또는 array, undefined → 전체
// 출력: handover.md 의 [VIZ_CATALOG] 섹션과 동일 포맷 — 그대로 system block 에 캐시됨.
// 사용 통계 기반으로 자주 쓰이는 순으로 정렬 (높은 사용 ↔ AI 가 우선 검토).
export function buildCatalog(subjects) {
  const subjectList = !subjects ? null
    : (Array.isArray(subjects) ? subjects : [subjects]);
  let list = listTemplates().filter((t) =>
    !subjectList || (t.subjects || []).some((s) => subjectList.includes(s))
  );
  // 사용량 정렬 — localStorage 의 viz-usage 활용 (browser only)
  try {
    const usage = JSON.parse(typeof localStorage !== 'undefined' ? (localStorage.getItem('ailearn-viz-usage') || '{}') : '{}');
    list = list.slice().sort((a, b) => {
      const ua = usage[a.name]?.ok || 0;
      const ub = usage[b.name]?.ok || 0;
      return ub - ua;
    });
  } catch { /* noop */ }
  if (!list.length) return '';
  const header = `## [VIZ_CATALOG] 시각자료 사용 규칙 (자동 생성, registry 기반)

그래프·도식·관계도가 필요하면 **반드시 아래 템플릿 중 하나 선택**.
freeform SVG 절대 금지 — 카탈로그에 없으면 \`\`\`mermaid 또는 텍스트/표로.
좌표·축·색·라벨은 컴포넌트가 처리 — AI는 의미적 파라미터만 채움.

`;
  const body = list.map((t) => {
    const example = JSON.stringify(t.exampleParams, null, 2);
    return `### ${t.name} — ${t.helpText}
\`\`\`viz ${t.name}
${example}
\`\`\``;
  }).join('\n\n');
  const footer = `

## 차트 공통 규칙
- 한 메시지에 viz 1개만 (학습 부담 최소화).
- 차트 뒤엔 본문 해설(왜·어떻게·다음 단계)을 마크다운으로 이어 작성. 차트만 단독 X.
- JSON 표준 준수 — 주석·trailing comma 금지.
- 카탈로그 외 도식은 \`\`\`mermaid 폴백 또는 텍스트·표로.`;
  return header + body + footer;
}

// 등록된 템플릿 총수 (디버깅/표시용)
export function templateCount() {
  return _registry.size;
}
