// 시각자료 템플릿 중앙 레지스트리.
// 각 템플릿: { name, version, schema, Component, exampleParams, helpText }
// 새 템플릿 추가는 templates/ 에 컴포넌트 만들고 여기 등록.

import { supplyDemandTemplate } from './templates/SupplyDemand';
import { tAccountTemplate } from './templates/TAccount';
import { legalRelationsTemplate } from './templates/LegalRelations';
import { balanceSheetTemplate } from './templates/BalanceSheet';
import { incomeStatementTemplate } from './templates/IncomeStatement';
import { claimFlowTemplate } from './templates/ClaimFlow';

const _registry = new Map();

function register(t) {
  if (_registry.has(t.name)) {
    // 중복 등록 시 경고만, 덮어쓰기 허용 (HMR 호환)
    console.warn(`[viz] duplicate template: ${t.name}`);
  }
  _registry.set(t.name, t);
}

// 경제
register(supplyDemandTemplate);
// 회계
register(tAccountTemplate);
register(balanceSheetTemplate);
register(incomeStatementTemplate);
// 법 (민법·법규·보상법규)
register(legalRelationsTemplate);
register(claimFlowTemplate);

export function getTemplate(name) {
  return _registry.get(name);
}

export function listTemplates() {
  return Array.from(_registry.values());
}

// AI 시스템 프롬프트에 주입할 카탈로그 텍스트 생성 (per-subject 필터 가능).
// subjects: undefined → 전체, 또는 ['economics', 'accounting'] 등
export function buildCatalog(subjects) {
  const list = listTemplates().filter((t) =>
    !subjects || (t.subjects || []).some((s) => subjects.includes(s))
  );
  if (!list.length) return '';
  return list.map((t) => `### ${t.name} — ${t.helpText}\n\`\`\`viz ${t.name}\n${JSON.stringify(t.exampleParams, null, 2)}\n\`\`\``).join('\n\n');
}
