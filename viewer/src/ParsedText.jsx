// 인라인 이미지([IMAGE: ...]) + KaTeX($...$) + 줄바꿈 렌더러
// App.jsx와 MockExam.jsx에서 동일한 문제 본문 렌더링을 위해 분리
import { useState } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

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
  // 셀 내 KaTeX 정도만 빠르게 처리 (이미지·줄바꿈은 표에선 무시)
  const parts = cell.split(/(\$[\s\S]*?\$)/g);
  return parts.map((p, i) => {
    if (p.startsWith('$') && p.endsWith('$') && p.length > 2) {
      const math = p.slice(1, -1);
      try {
        const html = katex.renderToString(math, { throwOnError: false, output: 'html' });
        return <span key={i} dangerouslySetInnerHTML={{ __html: html }} />;
      } catch { return <span key={i}>{p}</span>; }
    }
    return <span key={i}>{p}</span>;
  });
};

const renderTextBlock = (text, keyPrefix) => {
  // 이미지·KaTeX·줄바꿈 처리 (기존 ParsedText 로직)
  const parts = text.split(/(\[IMAGE:\s*.*?\])/g);
  return parts.map((part, i) => {
    const imgMatch = part.match(/\[IMAGE:\s*(.*?)\]/);
    if (imgMatch) {
      const rawName = imgMatch[1].split('/').pop();
      const imageName = rawName.replace(/\.(png|gif)$/i, '.webp');
      return <SafeImage key={`${keyPrefix}-${i}`} src={`/images/${imageName}`} />;
    }
    const mathParts = part.split(/(\$[\s\S]*?\$)/g);
    return mathParts.map((mathPart, j) => {
      if (mathPart.startsWith('$') && mathPart.endsWith('$') && mathPart.length > 2) {
        const math = mathPart.slice(1, -1);
        try {
          const html = katex.renderToString(math, { throwOnError: false, output: 'html' });
          return <span key={`${keyPrefix}-${i}-${j}`} dangerouslySetInnerHTML={{ __html: html }} />;
        } catch {
          return <span key={`${keyPrefix}-${i}-${j}`}>{mathPart}</span>;
        }
      }
      if (mathPart.indexOf('\n') === -1) return <span key={`${keyPrefix}-${i}-${j}`}>{mathPart}</span>;
      const lines = mathPart.split('\n');
      return (
        <span key={`${keyPrefix}-${i}-${j}`}>
          {lines.map((ln, k) => (
            <span key={k}>{ln}{k < lines.length - 1 && <br />}</span>
          ))}
        </span>
      );
    });
  });
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
        // text block
        return <span key={idx}>{renderTextBlock(b.content, idx)}</span>;
      })}
    </>
  );
};

export default ParsedText;
