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

export const ParsedText = ({ text }) => {
  if (!text) return null;
  const parts = text.split(/(\[IMAGE:\s*.*?\])/g);
  return (
    <>
      {parts.map((part, i) => {
        const imgMatch = part.match(/\[IMAGE:\s*(.*?)\]/);
        if (imgMatch) {
          const rawName = imgMatch[1].split('/').pop();
          // PNG/GIF는 빌드 시 동일 파일명의 WebP로 변환됨
          const imageName = rawName.replace(/\.(png|gif)$/i, '.webp');
          return <SafeImage key={i} src={`/images/${imageName}`} />;
        }
        const mathParts = part.split(/(\$[\s\S]*?\$)/g);
        return mathParts.map((mathPart, j) => {
          if (mathPart.startsWith('$') && mathPart.endsWith('$')) {
            const math = mathPart.slice(1, -1);
            try {
              const html = katex.renderToString(math, { throwOnError: false, output: 'html' });
              return <span key={`${i}-${j}`} dangerouslySetInnerHTML={{ __html: html }} />;
            } catch {
              return <span key={`${i}-${j}`}>{mathPart}</span>;
            }
          }
          if (mathPart.indexOf('\n') === -1) return <span key={`${i}-${j}`}>{mathPart}</span>;
          const lines = mathPart.split('\n');
          return (
            <span key={`${i}-${j}`}>
              {lines.map((ln, k) => (
                <span key={k}>{ln}{k < lines.length - 1 && <br />}</span>
              ))}
            </span>
          );
        });
      })}
    </>
  );
};

export default ParsedText;
