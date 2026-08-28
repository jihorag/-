// 시각자료 라우터: name + params 받아 등록된 컴포넌트 디스패치.
// JSON 파싱 실패 / 스키마 검증 실패 시 에러 박스 표시 + 원본 코드 폴백.

import { Suspense, useEffect } from 'react';
import { getTemplate } from './vizRegistry';
import { validate } from './validate';
import VizFrame from './VizFrame';
import { incrementVizUsage } from '../aiLearningStore';
import { stepParamsList, stepLabels } from './steps';
import StepPlayer from './StepPlayer';

function ErrorBox({ name, errors, rawText }) {
  return (
    <div style={{
      margin: '8px 0', padding: '10px 12px',
      background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8,
      fontSize: '0.78rem', color: '#991b1b',
    }}>
      <div style={{ fontWeight: 700, marginBottom: 4 }}>⚠️ 시각자료 렌더 실패: {name}</div>
      <ul style={{ margin: '4px 0 8px 16px', padding: 0 }}>
        {errors.map((e, i) => <li key={i}>{e}</li>)}
      </ul>
      {rawText && (
        <details>
          <summary style={{ cursor: 'pointer', color: '#7f1d1d' }}>원본 JSON 보기</summary>
          <pre style={{ margin: '6px 0 0', fontSize: '0.72rem', whiteSpace: 'pre-wrap', maxHeight: 200, overflow: 'auto' }}>{rawText}</pre>
        </details>
      )}
    </div>
  );
}

function TrackedRender({ name, ok, children }) {
  useEffect(() => {
    try { incrementVizUsage(name, ok); } catch { /* noop */ }
  }, [name, ok]);
  return children;
}

export default function VizRouter({ name, rawJson }) {
  const tpl = getTemplate(name);
  if (!tpl) {
    return <TrackedRender name={name} ok={false}>
      <ErrorBox name={name} errors={[`등록되지 않은 템플릿: "${name}"`]} rawText={rawJson} />
    </TrackedRender>;
  }
  let params;
  try {
    params = JSON.parse(rawJson || '{}');
  } catch (e) {
    return <TrackedRender name={name} ok={false}>
      <ErrorBox name={name} errors={[`JSON 파싱 오류: ${e.message}`]} rawText={rawJson} />
    </TrackedRender>;
  }
  const paramsList = stepParamsList(params);
  const labels = stepLabels(params);
  const errs = [];
  paramsList.forEach((p, i) => {
    const r = validate(tpl.schema, p);
    if (!r.ok) errs.push(...r.errors.map((e) => (paramsList.length > 1 ? `[${i + 1}단계] ${e}` : e)));
  });
  const v = { ok: errs.length === 0, errors: errs };
  if (!v.ok) {
    return <TrackedRender name={name} ok={false}>
      <ErrorBox name={name} errors={v.errors} rawText={rawJson} />
    </TrackedRender>;
  }
  const Comp = tpl.Component;
  return (
    <TrackedRender name={name} ok={true}>
      <VizFrame templateName={name}>
        <Suspense fallback={<div style={{ padding: 14, background: '#eef2ff', borderRadius: 8, fontSize: '0.82rem', color: '#4338ca', textAlign: 'center' }}>📊 {name} 로드 중...</div>}>
          {paramsList.length > 1
            ? <StepPlayer Comp={Comp} paramsList={paramsList} labels={labels} />
            : <Comp params={paramsList[0]} />}
        </Suspense>
      </VizFrame>
    </TrackedRender>
  );
}

// 스트리밍 중 임시 표시 (펜스 열려 있고 아직 안 닫힘)
export function VizPending({ name }) {
  return (
    <div style={{
      margin: '8px 0', padding: '14px 16px',
      background: '#eef2ff', border: '1px dashed #c7d2fe', borderRadius: 8,
      fontSize: '0.85rem', color: '#4338ca', textAlign: 'center', fontWeight: 700,
    }}>
      📊 {name} 생성 중...
    </div>
  );
}
