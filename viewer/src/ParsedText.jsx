// 인라인 이미지([IMAGE: ...]) + KaTeX($...$) + 줄바꿈 렌더러
// App.jsx와 MockExam.jsx에서 동일한 문제 본문 렌더링을 위해 분리
import { useState } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import VizRouter, { VizPending } from './viz/VizRouter';
import SafeSvg from './viz/SafeSvg';
import MermaidView from './viz/MermaidView';

export const SafeImage = ({ src }) => {
  const [errored, setErrored] = useState(false);
  const [zoom, setZoom] = useState(false);
  if (errored) {
    return <span style={{ display: 'inline-block', color: '#9ca3af', fontSize: '0.85rem', padding: '8px 0' }}>[이미지 없음]</span>;
  }
  return (
    <>
      <img
        src={src}
        alt="content"
        loading="lazy"
        decoding="async"
        className="q-img"
        onClick={() => setZoom(true)}
        onError={() => setErrored(true)}
        style={{ maxWidth: '100%', display: 'block', margin: '12px auto', borderRadius: '4px' }}
      />
      {zoom && (
        <div className="lightbox" role="dialog" aria-label="이미지 확대" onClick={() => setZoom(false)}>
          <button className="lightbox-close" aria-label="닫기" onClick={() => setZoom(false)}>✕</button>
          <img src={src} alt="확대 이미지" onClick={(e) => e.stopPropagation()} />
        </div>
      )}
    </>
  );
};

// 마크다운 표 블록을 React 표로 변환. 표가 아니면 null 반환.
// lines[startIdx] 가 헤더, lines[startIdx+1] 가 delimiter(`|---|---|`), 나머지는 데이터.
const isPipeRow = (l) => {
  const t = l.trim();
  return t.startsWith('|') && t.endsWith('|') && t.length > 2;
};
const splitCells = (l) => l.trim().slice(1, -1).split('|').map(c => c.trim());

const renderTableInlines = (cell) => {
  // 셀 내 KaTeX + bold(**...**) + <br> 처리 (셀 안 줄바꿈은 <br>로 명시)
  if (cell == null) return null;
  // <br> 분리 후 각 chunk를 다시 math/bold 처리
  const brChunks = String(cell).split(/<br\s*\/?>/i);
  return brChunks.map((chunk, ci) => {
    const mathParts = chunk.split(/(\$[\s\S]*?\$)/g);
    const inner = [];
    mathParts.forEach((p, i) => {
      if (p.startsWith('$') && p.endsWith('$') && p.length > 2) {
        const math = p.slice(1, -1);
        try {
          const html = katex.renderToString(math, { throwOnError: false, output: 'html' });
          inner.push(<span key={`${ci}-${i}-m`} dangerouslySetInnerHTML={{ __html: html }} />);
        } catch { inner.push(<span key={`${ci}-${i}-m`}>{p}</span>); }
        return;
      }
      const boldParts = p.split(/(\*\*[^*]+\*\*)/g);
      boldParts.forEach((bp, k) => {
        if (bp.startsWith('**') && bp.endsWith('**') && bp.length > 4) {
          inner.push(<strong key={`${ci}-${i}-b${k}`}>{bp.slice(2, -2)}</strong>);
        } else if (bp) {
          inner.push(<span key={`${ci}-${i}-t${k}`}>{bp}</span>);
        }
      });
    });
    return (
      <span key={ci}>
        {inner}
        {ci < brChunks.length - 1 && <br />}
      </span>
    );
  });
};

// 인라인 마크다운 (** ** bold, $ $ math, [IMAGE: ...]) 처리
const renderInlines = (text, keyPrefix) => {
  if (text == null || text === '') return null;
  // 1) 이미지 분리
  const imgParts = String(text).split(/(\[IMAGE:\s*.*?\])/g);
  const out = [];
  imgParts.forEach((part, i) => {
    const imgMatch = part.match(/\[IMAGE:\s*(.*?)\]/);
    if (imgMatch) {
      const rawName = imgMatch[1].split('/').pop();
      const imageName = rawName.replace(/\.(png|gif)$/i, '.webp');
      out.push(<SafeImage key={`${keyPrefix}-img-${i}`} src={`/images/${imageName}`} />);
      return;
    }
    // 2) 디스플레이 수식 $$...$$ 먼저 분리 (블록 렌더)
    const dispParts = part.split(/(\$\$[\s\S]+?\$\$)/g);
    dispParts.forEach((dp, di) => {
      if (dp.startsWith('$$') && dp.endsWith('$$') && dp.length > 4) {
        const math = dp.slice(2, -2).trim();
        try {
          const html = katex.renderToString(math, { throwOnError: false, output: 'html', displayMode: true });
          out.push(<div key={`${keyPrefix}-${i}-${di}-dm`} dangerouslySetInnerHTML={{ __html: html }} style={{ margin: '8px 0', overflowX: 'auto' }} />);
        } catch {
          out.push(<span key={`${keyPrefix}-${i}-${di}-dm`}>{dp}</span>);
        }
        return;
      }
      // 3) 인라인 수식 + bold (math 먼저)
      const mathParts = dp.split(/(\$[\s\S]*?\$)/g);
    mathParts.forEach((mp, j) => {
      if (mp.startsWith('$') && mp.endsWith('$') && mp.length > 2) {
        const math = mp.slice(1, -1);
        try {
          const html = katex.renderToString(math, { throwOnError: false, output: 'html' });
          out.push(<span key={`${keyPrefix}-${i}-${di}-${j}-m`} dangerouslySetInnerHTML={{ __html: html }} />);
        } catch {
          out.push(<span key={`${keyPrefix}-${i}-${di}-${j}-m`}>{mp}</span>);
        }
        return;
      }
      // 4) bold (**text**) 분리
      const boldParts = mp.split(/(\*\*[^*]+\*\*)/g);
      boldParts.forEach((bp, k) => {
        if (bp.startsWith('**') && bp.endsWith('**') && bp.length > 4) {
          out.push(<strong key={`${keyPrefix}-${i}-${di}-${j}-b${k}`}>{bp.slice(2, -2)}</strong>);
        } else if (bp) {
          out.push(<span key={`${keyPrefix}-${i}-${di}-${j}-t${k}`}>{bp}</span>);
        }
      });
    });
    });
  });
  return out;
};

// 미완성 마크다운 토큰 자동 보정 (streaming 중간 / max_tokens 절단 대응)
function sanitizeMarkdown(text) {
  if (!text) return text;
  let t = String(text);
  // ``` 코드블록 (가장 외곽) — 홀수면 닫기
  const fenceCount = (t.match(/```/g) || []).length;
  if (fenceCount % 2 === 1) t += '\n```';
  // ** 굵게 — 홀수면 닫기
  const starCount = (t.match(/\*\*/g) || []).length;
  if (starCount % 2 === 1) t += '**';
  // $$ 디스플레이 수식 — 홀수면 닫기
  const ddCount = (t.match(/\$\$/g) || []).length;
  if (ddCount % 2 === 1) t += '$$';
  // 단일 $ 인라인 수식 — 홀수면 닫기 ($$ 사용분 제외)
  const dollarCount = (t.match(/\$/g) || []).length;
  const singleDollar = dollarCount - ddCount * 2;
  if (singleDollar % 2 === 1) t += '$';
  return t;
}

const renderTextBlock = (text, keyPrefix) => {
  // ① 미완성 마크다운 보정 → ② **...** 안 줄바꿈 정규화
  const sanitized = sanitizeMarkdown(text);
  const normalizedText = String(sanitized || '').replace(
    /\*\*([\s\S]+?)\*\*/g,
    (match, inner) => '**' + inner.replace(/\s*\n+\s*/g, ' ').trim() + '**'
  );
  // 라인 단위로 ## 헤더, --- 수평선, - 리스트, 빈줄 단락 분리, 일반 단락 처리
  const rawLines = normalizedText.split('\n');
  const elements = [];
  let i = 0;
  while (i < rawLines.length) {
    const ln = rawLines[i];
    const trimmed = ln.trim();
    // 수평선
    if (/^(---+|___+|\*\*\*+)$/.test(trimmed)) {
      elements.push(<hr key={`${keyPrefix}-hr-${i}`} style={{ border: 0, borderTop: '1px solid #e5e7eb', margin: '12px 0' }} />);
      i++;
      continue;
    }
    // 헤더 — ##/### 등
    const hMatch = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (hMatch) {
      const level = hMatch[1].length;
      const content = hMatch[2];
      const fontSize = level === 1 ? '1.1em' : level === 2 ? '1.05em' : level === 3 ? '0.98em' : '0.92em';
      const color = level <= 2 ? '#111827' : '#374151';
      const marginTop = level <= 2 ? 12 : 8;
      elements.push(
        <div key={`${keyPrefix}-h-${i}`} style={{ fontWeight: 700, fontSize, color, margin: `${marginTop}px 0 4px` }}>
          {renderInlines(content, `${keyPrefix}-h-${i}`)}
        </div>
      );
      i++;
      continue;
    }
    // 보기 ㄱㄴㄷㄹㅁ 박스 — 연속된 "ㄱ. " / "ㄴ. " ... 라인을 박스로 묶기
    const bogiHead = trimmed.match(/^([ㄱ-ㅎ])\.\s+(.+)$/);
    if (bogiHead && /[ㄱㄴㄷㄹㅁㅂㅅㅇ]/.test(bogiHead[1])) {
      const items = [];
      while (i < rawLines.length) {
        const cur = rawLines[i].trim();
        const m = cur.match(/^([ㄱ-ㅎ])\.\s+(.*)$/);
        if (!m || !/[ㄱㄴㄷㄹㅁㅂㅅㅇ]/.test(m[1])) break;
        items.push({ marker: m[1], content: m[2] });
        i++;
      }
      elements.push(
        <div
          key={`${keyPrefix}-bogi-${i}`}
          style={{
            background: '#f8fafc',
            border: '1px solid #e2e8f0',
            borderLeft: '3px solid #94a3b8',
            borderRadius: '6px',
            padding: '12px 16px',
            margin: '10px 0',
          }}
        >
          {items.map((it, k) => (
            <div
              key={k}
              style={{
                display: 'flex',
                gap: '10px',
                margin: k === 0 ? '0' : '6px 0 0',
                lineHeight: 1.6,
                alignItems: 'baseline',
              }}
            >
              <span style={{ fontWeight: 700, minWidth: '20px', color: '#475569', flexShrink: 0 }}>
                {it.marker}.
              </span>
              <span style={{ flex: 1 }}>
                {renderInlines(it.content, `${keyPrefix}-bogi-${k}`)}
              </span>
            </div>
          ))}
        </div>
      );
      continue;
    }
    // 리스트 항목 — 연속된 - / * 라인 묶기
    if (/^\s*[-*]\s+/.test(ln)) {
      const items = [];
      while (i < rawLines.length && /^\s*[-*]\s+/.test(rawLines[i])) {
        const content = rawLines[i].replace(/^\s*[-*]\s+/, '');
        items.push(content);
        i++;
      }
      elements.push(
        <ul key={`${keyPrefix}-ul-${i}`} style={{ margin: '4px 0 4px 0', paddingLeft: 20 }}>
          {items.map((it, k) => (
            <li key={k} style={{ margin: '2px 0' }}>{renderInlines(it, `${keyPrefix}-li-${k}`)}</li>
          ))}
        </ul>
      );
      continue;
    }
    // 빈 줄 → 단락 구분
    if (trimmed === '') {
      elements.push(<div key={`${keyPrefix}-br-${i}`} style={{ height: 6 }} />);
      i++;
      continue;
    }
    // 일반 라인 — 연속된 일반 라인 묶어서 단락으로
    const paraLines = [];
    while (i < rawLines.length) {
      const cur = rawLines[i];
      const ct = cur.trim();
      if (ct === '' || /^(---+|___+|\*\*\*+)$/.test(ct) || /^(#{1,4})\s+/.test(ct) || /^\s*[-*]\s+/.test(cur) || /^[ㄱㄴㄷㄹㅁㅂㅅㅇ]\.\s+/.test(ct)) break;
      paraLines.push(cur);
      i++;
    }
    elements.push(
      <div key={`${keyPrefix}-p-${i}`} style={{ margin: '2px 0' }}>
        {paraLines.map((pl, k) => (
          <span key={k}>
            {renderInlines(pl, `${keyPrefix}-p-${i}-${k}`)}
            {k < paraLines.length - 1 && <br />}
          </span>
        ))}
      </div>
    );
  }
  return elements;
};

export const ParsedText = ({ text }) => {
  if (!text) return null;
  // 라인 단위로 스캔하면서 표 블록과 일반 텍스트 블록을 교차 추출
  const lines = text.split('\n');
  const blocks = [];   // { type: 'table' | 'text', ... }
  let i = 0;
  let textBuf = [];
  const flushText = () => {
    if (textBuf.length) {
      blocks.push({ type: 'text', content: textBuf.join('\n') });
      textBuf = [];
    }
  };
  while (i < lines.length) {
    const l = lines[i];
    // 시각자료 fence 감지: ```viz <template-name>  /  ```mermaid  /  ```svg
    const vizMatch = l.match(/^```(viz)\s+([a-z0-9_-]+)\s*$/i);
    const mermaidMatch = l.match(/^```mermaid\s*$/i);
    const svgMatch = l.match(/^```svg\s*$/i);
    if (vizMatch || mermaidMatch || svgMatch) {
      flushText();
      const kind = vizMatch ? 'viz' : mermaidMatch ? 'mermaid' : 'svg';
      const name = vizMatch ? vizMatch[2] : kind;
      const bodyLines = [];
      let j = i + 1;
      let closed = false;
      while (j < lines.length) {
        if (/^```\s*$/.test(lines[j])) { closed = true; break; }
        bodyLines.push(lines[j]);
        j++;
      }
      if (closed) {
        if (kind === 'viz')         blocks.push({ type: 'viz', name, raw: bodyLines.join('\n') });
        else if (kind === 'mermaid') blocks.push({ type: 'mermaid', raw: bodyLines.join('\n') });
        else                          blocks.push({ type: 'svg', raw: bodyLines.join('\n') });
        i = j + 1;
      } else {
        // 스트리밍 중 — 아직 펜스 안 닫힘.
        blocks.push({ type: 'viz_pending', name: kind === 'viz' ? name : kind });
        i = j;
      }
      continue;
    }
    // 표 시작 감지: 현재 라인 + 다음 라인이 pipe row이고, 다음 라인이 delimiter
    if (i + 1 < lines.length && isPipeRow(l) && isPipeRow(lines[i+1])) {
      const delimCells = splitCells(lines[i+1]);
      const isDelim = delimCells.length > 0 && delimCells.every(c => /^:?-+:?$/.test(c));
      if (isDelim) {
        flushText();
        const headers = splitCells(l);
        const rows = [];
        let j = i + 2;
        while (j < lines.length && isPipeRow(lines[j])) {
          rows.push(splitCells(lines[j]));
          j++;
        }
        blocks.push({ type: 'table', headers, rows });
        i = j;
        continue;
      }
    }
    textBuf.push(l);
    i++;
  }
  flushText();

  return (
    <>
      {blocks.map((b, idx) => {
        if (b.type === 'viz') {
          return <VizRouter key={idx} name={b.name} rawJson={b.raw} />;
        }
        if (b.type === 'mermaid') {
          return <MermaidView key={idx} raw={b.raw} />;
        }
        if (b.type === 'svg') {
          return <SafeSvg key={idx} raw={b.raw} />;
        }
        if (b.type === 'viz_pending') {
          return <VizPending key={idx} name={b.name} />;
        }
        if (b.type === 'table') {
          return (
            <div key={idx} style={{ overflowX: 'auto', margin: '8px 0' }}>
              <table style={{ borderCollapse: 'collapse', fontSize: '0.85em',
                width: '100%', minWidth: 'max-content' }}>
                <thead>
                  <tr>
                    {b.headers.map((h, k) => (
                      <th key={k} style={{ border: '1px solid #d1d5db', padding: '6px 10px',
                        background: '#f9fafb', fontWeight: 700, textAlign: 'left',
                        whiteSpace: 'nowrap' }}>
                        {renderTableInlines(h)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {b.rows.map((r, ri) => (
                    <tr key={ri}>
                      {r.map((c, ci) => (
                        <td key={ci} style={{ border: '1px solid #e5e7eb', padding: '6px 10px',
                          verticalAlign: 'top' }}>
                          {renderTableInlines(c)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        }
        // text block (block-level 요소 — div·ul·hr 등 — 반환)
        return <div key={idx}>{renderTextBlock(b.content, idx)}</div>;
      })}
    </>
  );
};

export default ParsedText;
