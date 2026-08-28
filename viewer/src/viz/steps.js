// viz 단계 재생 — params.steps 를 base params 위에 병합한다.
// 템플릿 18개는 전부 순수 params → SVG 라서, 여기서 파라미터만 갈아 끼우면
// 템플릿 파일을 하나도 안 건드리고 전부 애니메이션이 된다.

/** step 의 label 을 빼고 나머지를 base 위에 얕게 덮어쓴다. base 는 건드리지 않는다. */
export function mergeStep(base, step) {
  const { label, ...rest } = step || {};
  void label;
  return { ...base, ...rest };
}

/** params → 단계별 params 배열. steps 가 없으면 길이 1. */
export function stepParamsList(params) {
  const { steps, ...base } = params || {};
  if (!Array.isArray(steps) || steps.length === 0) return [base];
  return steps.map((s) => mergeStep(base, s));
}

/** 화면에 띄울 단계 라벨. 없으면 1-based 번호. */
export function stepLabels(params) {
  const steps = params?.steps;
  if (!Array.isArray(steps) || steps.length === 0) return [];
  return steps.map((s, i) => s?.label || `${i + 1}단계`);
}
