// Mermaid 다이어그램 lazy-rendering.
// 첫 사용 시점에 dynamic import → mermaid 모듈 로드 (~700KB).
// 카탈로그 외 자유 흐름도/시퀀스도/ER 다이어그램에 사용.

import { useEffect, useRef, useState } from 'react';

let _mermaidPromise = null;
let _idCounter = 0;

function loadMermaid() {
  if (!_mermaidPromise) {
    // /* @vite-ignore */ — mermaid 패키지 미설치 환경에서 정적 분석 통과.
    // 미설치 시 런타임에 reject 되어 MermaidView 의 error 분기에서 안내 표시.
    _mermaidPromise = import(/* @vite-ignore */ 'mermaid').then((mod) => {
      const m = mod.default || mod;
      m.initialize({
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'strict',
        fontFamily: 'Pretendard Variable, -apple-system, sans-serif',
        flowchart: { useMaxWidth: true, htmlLabels: false, curve: 'basis' },
        sequence: { useMaxWidth: true, mirrorActors: false },
      });
      return m;
    }).catch((e) => {
      // 미설치 시: 명확한 안내 메시지로 다시 throw → MermaidView 의 error 표시.
      throw new Error('mermaid 패키지 미설치 — viewer 디렉터리에서 `npm install` 실행 후 새로고침해주세요.');
    });
  }
  return _mermaidPromise;
}

export default function MermaidView({ raw }) {
  const ref = useRef(null);
  const [svg, setSvg] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    loadMermaid().then(async (mermaid) => {
      try {
        const id = `mermaid-${++_idCounter}`;
        const { svg } = await mermaid.render(id, String(raw || '').trim());
        if (!cancelled) {
          setSvg(svg);
          setLoading(false);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e.message || String(e));
          setLoading(false);
        }
      }
    }).catch((e) => {
      if (!cancelled) {
        setError('Mermaid 로딩 실패: ' + (e.message || e));
        setLoading(false);
      }
    });
    return () => { cancelled = true; };
  }, [raw]);

  if (loading) {
    return (
      <div style={{
        margin: '8px 0', padding: '14px 16px',
        background: '#f0f9ff', border: '1px dashed #bae6fd', borderRadius: 8,
        fontSize: '0.85rem', color: '#0369a1', textAlign: 'center', fontWeight: 600,
      }}>
        🔄 Mermaid 다이어그램 로드 중...
      </div>
    );
  }
  if (error) {
    return (
      <div style={{
        margin: '8px 0', padding: '10px 12px',
        background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8,
        fontSize: '0.78rem', color: '#991b1b',
      }}>
        <div style={{ fontWeight: 700, marginBottom: 4 }}>⚠️ Mermaid 렌더 실패</div>
        <div style={{ marginBottom: 6 }}>{error}</div>
        <details>
          <summary style={{ cursor: 'pointer', color: '#7f1d1d' }}>원본 보기</summary>
          <pre style={{ margin: '6px 0 0', fontSize: '0.72rem', whiteSpace: 'pre-wrap', maxHeight: 200, overflow: 'auto' }}>{raw}</pre>
        </details>
      </div>
    );
  }
  return (
    <div style={{
      margin: '12px 0', padding: 8, background: '#fff',
      border: '1px solid #e5e7eb', borderRadius: 10, overflow: 'auto',
      display: 'flex', justifyContent: 'center',
    }}>
      <div
        ref={ref}
        style={{ width: '100%', maxWidth: 720 }}
        dangerouslySetInnerHTML={{ __html: svg }}
      />
    </div>
  );
}
