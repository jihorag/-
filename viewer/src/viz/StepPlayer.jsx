// 단계 재생기 — 같은 템플릿을 단계별 params 로 갈아 끼운다.
//
// ponytail: 템플릿이 계산된 좌표를 SVG 속성으로 직접 찍기 때문에 단계 전환은 점프다.
// 크로스페이드로 눈에 덜 거슬리게만 했다. 선·점 기반 템플릿(SupplyDemand·CostCurves·
// IsLm·PhillipsCurve)은 CSS 로 지오메트리 전이를 걸면 Chrome·Safari 에서 실제로
// 미끄러진다. 그게 필요해지면 각 단계를 같은 명령 구조의 path 로 뽑아 보간한다.
import { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Play, Pause } from 'lucide-react';

const STEP_MS = 1600;

export default function StepPlayer({ Comp, paramsList, labels }) {
  const [i, setI] = useState(0);
  const [playing, setPlaying] = useState(false);
  const last = paramsList.length - 1;
  const timer = useRef(null);

  useEffect(() => {
    if (!playing) return undefined;
    timer.current = setInterval(() => {
      setI((prev) => {
        if (prev >= last) { setPlaying(false); return prev; }
        return prev + 1;
      });
    }, STEP_MS);
    return () => clearInterval(timer.current);
  }, [playing, last]);

  const go = (n) => { setPlaying(false); setI(Math.max(0, Math.min(last, n))); };

  return (
    <div>
      <div key={i} style={{ animation: 'vizStepIn 0.28s ease-out' }}>
        <Comp params={paramsList[i]} />
      </div>
      <div style={{
        display: 'flex', alignItems: 'center', gap: 8,
        padding: '6px 10px', borderTop: '1px solid #e5e7eb',
      }}>
        <button onClick={() => go(i - 1)} disabled={i === 0}
          aria-label="이전 단계" style={ctrl(i === 0)}><ChevronLeft size={15} /></button>
        <button onClick={() => (i >= last ? go(0) : setPlaying((p) => !p))}
          aria-label={playing ? '일시정지' : '재생'} style={ctrl(false)}>
          {playing ? <Pause size={15} /> : <Play size={15} />}
        </button>
        <button onClick={() => go(i + 1)} disabled={i === last}
          aria-label="다음 단계" style={ctrl(i === last)}><ChevronRight size={15} /></button>
        <span style={{ fontSize: '0.78rem', color: '#374151', fontWeight: 700 }}>
          {labels[i] || `${i + 1}단계`}
        </span>
        <span style={{ marginLeft: 'auto', display: 'flex', gap: 4 }}>
          {paramsList.map((_, n) => (
            <button key={n} onClick={() => go(n)} aria-label={`${n + 1}단계로`}
              style={{
                width: 7, height: 7, padding: 0, borderRadius: '50%', border: 'none',
                cursor: 'pointer', background: n === i ? '#374151' : '#d1d5db',
              }} />
          ))}
        </span>
      </div>
    </div>
  );
}

function ctrl(disabled) {
  return {
    width: 26, height: 26, borderRadius: 6, border: '1px solid #d1d5db',
    background: '#fff', cursor: disabled ? 'default' : 'pointer',
    opacity: disabled ? 0.35 : 1,
    display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#374151',
  };
}
