// 인라인 이미지([IMAGE: ...]) + KaTeX($...$) + 줄바꿈 렌더러
// App.jsx와 MockExam.jsx에서 동일한 문제 본문 렌더링을 위해 분리
import { useState } from 'react';
import { useScrollLock, useEscClose } from './uiHooks';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import VizRouter, { VizPending } from './viz/VizRouter';
import SafeSvg from './viz/SafeSvg';
import MermaidView from './viz/MermaidView';

export const SafeImage = ({ src }) => {
  const [errored, setErrored] = useState(false);
  const [zoom, setZoom] = useState(false);
  useScrollLock(zoom);
  useEscClose(zoom, () => setZoom(false));
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

// 형광펜(==텍스트==) — 실제 형광펜처럼 글자 아래쪽만 칠해지는 마커 효과.
const HILITE = {
  background: 'linear-gradient(transparent 58%, #f6e7a1 58%)',
  color: 'inherit',
  padding: '0 1px',
  borderRadius: 1,
};

// 볼드 안에 형광펜이 들어간 경우(**…==핵심==…**)를 살려서 렌더한다.
// 바깥 split 이 볼드를 통째로 잡아가므로, 볼드 내부를 한 번 더 쪼갠다.
const withHilite = (text, keyPrefix) => {
  const parts = String(text).split(/(==(?:(?!==)[\s\S])+==)/g);
  if (parts.length === 1) return text;
  return parts.map((pt, i) =>
    pt.startsWith('==') && pt.endsWith('==') && pt.length > 4
      ? <mark key={`${keyPrefix}-nh${i}`} style={HILITE}>{pt.slice(2, -2)}</mark>
      : <span key={`${keyPrefix}-nt${i}`}>{pt}</span>
  );
};

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
      const boldParts = p.split(/(\*\*[^*]+\*\*|==(?:(?!==)[\s\S])+==)/g);
      boldParts.forEach((bp, k) => {
        if (bp.startsWith('**') && bp.endsWith('**') && bp.length > 4) {
          inner.push(<strong key={`${ci}-${i}-b${k}`}>{withHilite(bp.slice(2, -2), `${ci}-${i}-b${k}`)}</strong>);
        } else if (bp.startsWith('==') && bp.endsWith('==') && bp.length > 4) {
          inner.push(<mark key={`${ci}-${i}-hl${k}`} style={HILITE}>{bp.slice(2, -2)}</mark>);
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
      // 4) bold(**text**) + 형광펜(==text==) 분리
      const boldParts = mp.split(/(\*\*[^*]+\*\*|==(?:(?!==)[\s\S])+==)/g);
      boldParts.forEach((bp, k) => {
        if (bp.startsWith('**') && bp.endsWith('**') && bp.length > 4) {
          const kp = `${keyPrefix}-${i}-${di}-${j}-b${k}`;
          out.push(<strong key={kp}>{withHilite(bp.slice(2, -2), kp)}</strong>);
        } else if (bp.startsWith('==') && bp.endsWith('==') && bp.length > 4) {
          out.push(<mark key={`${keyPrefix}-${i}-${di}-${j}-hl${k}`} style={HILITE}>{bp.slice(2, -2)}</mark>);
        } else if (bp) {
          out.push(<span key={`${keyPrefix}-${i}-${di}-${j}-t${k}`}>{bp}</span>);
        }
      });
    });
    });
  });
  return out;
};

// 콜아웃 톤 — 수험서 지면처럼 채도를 낮춘 종이·먹색 계열.
// 성격 구분은 되되 화면이 알록달록해지지 않도록 배경은 거의 무채색, 좌측 바로만 구분한다.
const CALLOUT_TONES = {
  '💡': { bg: '#f7f8f9', bar: '#64748b' },   // 팁·보충 — 슬레이트
  '🔑': { bg: '#f8f7f4', bar: '#57534e' },   // 핵심 — 먹색
  '⚠️': { bg: '#fbf7f5', bar: '#9a3412' },   // 함정·주의 — 적갈
  '⚠': { bg: '#fbf7f5', bar: '#9a3412' },
  '✏️': { bg: '#f7f9f7', bar: '#4d7c5f' },   // 예제·풀이 — 청록회색
  '✏': { bg: '#f7f9f7', bar: '#4d7c5f' },
  '⭐': { bg: '#faf8f2', bar: '#a16207' },   // 필수·출제포인트 — 황토
  '📌': { bg: '#f8f9fa', bar: '#94a3b8' },   // 참고
  '📖': { bg: '#f8f8f9', bar: '#6b7280' },   // 도입
  '⏳': { bg: '#f8fafc', bar: '#cbd5e1' },
  _default: { bg: '#f8f9fa', bar: '#a3a3a3' },
};

// ── 법전(法典) 블록 ───────────────────────────────────────────────
// `> 📌 **국토계획법 제6조(용도지역의 지정)** — "① … 1. … 가. …"` 형태의 조문 인용을
// 실제 법전 지면처럼 조·항·호·목 계층으로 펼쳐 보여준다.
// 원문이 한 줄로 뭉쳐 들어와도 마커(①/1./가.)를 기준으로 줄을 나눈다.

// 조문 인용인지 판별 — 볼드 제목 안에 `제N조`가 있고 ` — ` 로 문언이 이어지는 형태.
const STATUTE_RE = /^\*\*([^*]*제\s*\d+조[^*]*)\*\*\s*[—–-]\s*([\s\S]+)$/;
const MOK_LETTERS = '가나다라마바사아자차카타파하';

// 제목을 [법령명, 조문표시] 로 쪼갠다. 예: "국토계획법 시행령 제31조 제2항" → ["국토계획법 시행령", "제31조 제2항"]
function splitStatuteTitle(title) {
  const m = title.match(/^(.*?)\s*(제\s*\d+조.*)$/);
  return m ? [m[1].trim(), m[2].trim()] : ['', title.trim()];
}

// 문언을 마커 단위 토큰으로 분해. depth 1=항, 2=호, 3=목.
function parseStatuteBody(raw) {
  // 저술 시 목 구분에 ` / ` 를 쓴 곳이 있다. 마커(가./나.)가 계층을 알려주므로 공백으로 눕힌다.
  const text = String(raw)
    .replace(/^["“”]|["“”]$/g, '')
    .replace(/\s*\/\s*/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  const re = new RegExp(`([①-⑳])|(?:^|[\\s])(\\d{1,2})\\.\\s|(?:^|[\\s])([${MOK_LETTERS}])\\.\\s`, 'g');
  const tokens = [];
  let cur = { depth: 0, marker: '', text: '' };
  let last = 0;
  let m;
  while ((m = re.exec(text))) {
    cur.text += text.slice(last, m.index);
    tokens.push(cur);
    const depth = m[1] ? 1 : m[2] ? 2 : 3;
    const marker = m[1] || `${m[2] || m[3]}.`;
    cur = { depth, marker, text: '' };
    last = re.lastIndex;
  }
  cur.text += text.slice(last);
  tokens.push(cur);
  return tokens
    .map((t) => ({ ...t, text: t.text.trim() }))
    .filter((t) => t.text || t.marker);
}

function StatuteBlock({ title, body, keyPrefix }) {
  const [lawName, article] = splitStatuteTitle(title);
  const tokens = parseStatuteBody(body);
  return (
    <div style={{
      background: '#fdfcf8', border: '1px solid #e8e3d6', borderLeft: '3px solid #8a7f6a',
      borderRadius: 5, margin: '14px 0', overflow: 'hidden',
      fontFamily: '"Nanum Myeongjo", "AppleMyungjo", Georgia, serif',
    }}>
      <div style={{
        display: 'flex', alignItems: 'baseline', gap: 8, flexWrap: 'wrap',
        padding: '8px 14px', background: '#f6f2e8', borderBottom: '1px solid #e8e3d6',
      }}>
        <span style={{ fontWeight: 800, fontSize: '0.97em', color: '#3f3a2f', letterSpacing: '-0.01em' }}>
          {article}
        </span>
        {lawName && (
          <span style={{
            marginLeft: 'auto', fontSize: '0.74em', fontWeight: 700, color: '#7c7259',
            border: '1px solid #ddd5c2', borderRadius: 3, padding: '1px 7px', background: '#fdfcf8',
            fontFamily: 'inherit', whiteSpace: 'nowrap',
          }}>
            {lawName}
          </span>
        )}
      </div>
      <div style={{ padding: '10px 14px 12px', color: '#2f2b24', fontSize: '0.93em', lineHeight: 1.95 }}>
        {tokens.map((t, k) => (
          <div key={k} style={{
            display: 'flex', gap: 6,
            paddingLeft: t.depth > 1 ? (t.depth - 1) * 17 : 0,
            margin: t.depth === 1 ? '5px 0 0' : '1px 0',
          }}>
            {t.marker && (
              <span style={{ flex: '0 0 auto', fontWeight: t.depth === 1 ? 700 : 500, color: '#6b6250' }}>
                {t.marker}
              </span>
            )}
            <span style={{ flex: 1, textAlign: 'justify' }}>
              {renderInlines(t.text, `${keyPrefix}-st-${k}`)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── 회계 지면 ────────────────────────────────────────────────────
// 회계는 "표"가 아니라 **양식**이다. 금액은 우측정렬·천단위 콤마·음수는 괄호,
// 계정은 계층 들여쓰기, 소계는 단선·총계는 이중선. 일반 마크다운 표로는 표현되지 않는다.

const MONO = '"SF Mono", "Menlo", "D2Coding", monospace';

// 숫자면 회계 표기로. 음수는 (1,200), 0은 —, 그 외 문자열은 그대로.
function fmtAmount(v) {
  const s = String(v == null ? '' : v).trim();
  if (s === '' || s === '-' || s === '—') return '—';
  const cleaned = s.replace(/,/g, '');
  if (!/^-?\d+(\.\d+)?$/.test(cleaned)) return s;
  const n = Number(cleaned);
  const body = Math.abs(n).toLocaleString('ko-KR');
  return n < 0 ? `(${body})` : body;
}

// `　` 전각공백 또는 2칸 들여쓰기로 계정 계층을 표현한다.
function accountIndent(label) {
  const m = String(label).match(/^([\s　]*)/);
  const pad = m ? m[1].replace(/　/g, '  ').length : 0;
  return { depth: Math.floor(pad / 2), text: String(label).trim() };
}

const AmountCell = ({ v, bold, rule }) => (
  <td style={{
    textAlign: 'right', fontFamily: MONO, fontVariantNumeric: 'tabular-nums',
    padding: '3px 10px', whiteSpace: 'nowrap',
    fontWeight: bold ? 700 : 400,
    borderTop: rule === 'sub' ? '1px solid #9ca3af' : undefined,
    borderBottom: rule === 'total' ? '3px double #4b5563' : undefined,
  }}>{fmtAmount(v)}</td>
);

/** ```재무제표 — 첫 줄 메타(제목/단위), 이후 `계정 | 금액 | 금액` */
function FinancialStatement({ raw, keyPrefix }) {
  const lines = raw.split('\n').map(l => l.replace(/\s+$/, '')).filter(l => l.trim());
  const meta = {};
  const body = [];
  for (const l of lines) {
    const m = l.match(/^(제목|단위|기준일|기간|회사)\s*[:：]\s*(.*)$/);
    if (m) { meta[m[1]] = m[2].trim(); continue; }
    if (/^[-=]{3,}$/.test(l.trim())) continue;
    body.push(l);
  }
  if (!body.length) return null;
  const cells = body.map(l => l.split('|').map(c => c.replace(/\s+$/, '')));
  const headerRow = cells[0].length > 1 && cells[0].slice(1).every(c => !/\d/.test(c)) ? cells[0] : null;
  const rows = headerRow ? cells.slice(1) : cells;
  const nCols = Math.max(...cells.map(c => c.length)) - 1;

  return (
    <div style={{
      margin: '16px 0', border: '1px solid #d6d3d1', borderRadius: 5,
      background: '#fffefb', overflowX: 'auto',
    }}>
      {(meta['제목'] || meta['회사'] || meta['단위'] || meta['기준일'] || meta['기간']) && (
        <div style={{ padding: '9px 14px 7px', borderBottom: '1px solid #e7e5e4', background: '#faf9f6' }}>
          {meta['제목'] && (
            <div style={{ textAlign: 'center', fontWeight: 800, fontSize: '1.02em', color: '#292524', letterSpacing: '0.02em' }}>
              {meta['제목']}
            </div>
          )}
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 3, fontSize: '0.76em', color: '#78716c' }}>
            <span>{meta['회사'] || ''}</span>
            <span>{meta['기준일'] || meta['기간'] || ''}</span>
            <span>{meta['단위'] ? `(단위: ${meta['단위']})` : ''}</span>
          </div>
        </div>
      )}
      <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: '0.88em' }}>
        {headerRow && (
          <thead>
            <tr>
              <th style={{ textAlign: 'left', padding: '5px 12px', borderBottom: '1.5px solid #57534e', fontWeight: 700, color: '#44403c' }}>
                {headerRow[0].trim() || '과목'}
              </th>
              {headerRow.slice(1).map((h, k) => (
                <th key={k} style={{ textAlign: 'right', padding: '5px 10px', borderBottom: '1.5px solid #57534e', fontWeight: 700, color: '#44403c', whiteSpace: 'nowrap' }}>
                  {h.trim()}
                </th>
              ))}
            </tr>
          </thead>
        )}
        <tbody>
          {rows.map((r, k) => {
            let label = r[0] ?? '';
            // 접두 `=` 총계(이중선) · `-` 소계(단선) · `**굵게**`
            let rule = null;
            const t = label.trim();
            if (t.startsWith('=')) { rule = 'total'; label = label.replace('=', ''); }
            else if (t.startsWith('~')) { rule = 'sub'; label = label.replace('~', ''); }
            const { depth, text } = accountIndent(label);
            const bold = rule !== null || /^\*\*.*\*\*$/.test(text);
            const clean = text.replace(/^\*\*|\*\*$/g, '');
            const vals = r.slice(1);
            return (
              <tr key={k}>
                <td style={{
                  padding: '3px 12px', paddingLeft: 12 + depth * 16,
                  fontWeight: bold ? 700 : 400, color: '#292524', whiteSpace: 'nowrap',
                  borderTop: rule === 'sub' ? '1px solid #9ca3af' : undefined,
                  borderBottom: rule === 'total' ? '3px double #4b5563' : undefined,
                }}>{renderInlines(clean, `${keyPrefix}-fs-${k}`)}</td>
                {Array.from({ length: nCols }).map((_, c) => (
                  <AmountCell key={c} v={vals[c]} bold={bold} rule={rule} />
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

/** ```분개 — `차변계정 | 금액 | 대변계정 | 금액` */
function JournalEntry({ raw, keyPrefix }) {
  const lines = raw.split('\n').filter(l => l.trim() && !/^[-=]{3,}$/.test(l.trim()));
  const meta = {};
  const rows = [];
  for (const l of lines) {
    const m = l.match(/^(제목|일자|설명)\s*[:：]\s*(.*)$/);
    if (m) { meta[m[1]] = m[2].trim(); continue; }
    const c = l.split('|').map(x => x.trim());
    rows.push([c[0] || '', c[1] || '', c[2] || '', c[3] || '']);
  }
  const sum = (i) => rows.reduce((a, r) => {
    const n = Number(String(r[i]).replace(/[,()]/g, ''));
    return a + (Number.isFinite(n) ? n : 0);
  }, 0);
  const dr = sum(1), cr = sum(3);
  return (
    <div style={{ margin: '16px 0', border: '1px solid #d6d3d1', borderRadius: 5, background: '#fffefb', overflowX: 'auto' }}>
      <div style={{ padding: '7px 12px', borderBottom: '1px solid #e7e5e4', background: '#f6f5f1', fontSize: '0.8em', fontWeight: 800, color: '#44403c' }}>
        ✍️ 분개{meta['일자'] ? ` · ${meta['일자']}` : ''}{meta['제목'] ? ` — ${meta['제목']}` : ''}
      </div>
      <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: '0.88em' }}>
        <thead>
          <tr>
            {['차변', '금액', '대변', '금액'].map((h, k) => (
              <th key={k} style={{
                padding: '4px 10px', borderBottom: '1.5px solid #57534e', fontWeight: 700, color: '#44403c',
                textAlign: k % 2 ? 'right' : 'left',
                borderLeft: k === 2 ? '1px solid #d6d3d1' : undefined,
              }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, k) => (
            <tr key={k}>
              <td style={{ padding: '3px 10px', whiteSpace: 'nowrap' }}>{renderInlines(r[0], `${keyPrefix}-je-d-${k}`)}</td>
              <AmountCell v={r[1]} />
              <td style={{ padding: '3px 10px', whiteSpace: 'nowrap', borderLeft: '1px solid #d6d3d1' }}>
                {renderInlines(r[2], `${keyPrefix}-je-c-${k}`)}
              </td>
              <AmountCell v={r[3]} />
            </tr>
          ))}
          {rows.length > 1 && (
            <tr>
              <td style={{ padding: '3px 10px', fontWeight: 700, borderTop: '1px solid #9ca3af' }}>합계</td>
              <AmountCell v={dr} bold rule="sub" />
              <td style={{ padding: '3px 10px', fontWeight: 700, borderTop: '1px solid #9ca3af', borderLeft: '1px solid #d6d3d1' }}>합계</td>
              <AmountCell v={cr} bold rule="sub" />
            </tr>
          )}
        </tbody>
      </table>
      {rows.length > 1 && dr !== cr && (
        <div style={{ padding: '5px 12px', fontSize: '0.76em', color: '#9a3412', background: '#fbf7f5' }}>
          ⚠️ 차변 합계와 대변 합계가 다릅니다 ({fmtAmount(dr)} / {fmtAmount(cr)})
        </div>
      )}
    </div>
  );
}

/** ```T계정 — `차변항목 | 금액 | 대변항목 | 금액`, 첫 줄 `제목:` */
function TAccount({ raw, keyPrefix }) {
  const lines = raw.split('\n').filter(l => l.trim() && !/^[-=]{3,}$/.test(l.trim()));
  let title = '';
  const rows = [];
  for (const l of lines) {
    const m = l.match(/^(제목|계정)\s*[:：]\s*(.*)$/);
    if (m) { title = m[2].trim(); continue; }
    const c = l.split('|').map(x => x.trim());
    rows.push([c[0] || '', c[1] || '', c[2] || '', c[3] || '']);
  }
  return (
    <div style={{ margin: '16px 0', maxWidth: 560 }}>
      {title && (
        <div style={{ textAlign: 'center', fontWeight: 800, fontSize: '0.92em', color: '#292524', marginBottom: 2 }}>
          {title}
        </div>
      )}
      <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: '0.86em',
        borderTop: '2px solid #57534e' }}>
        <tbody>
          {rows.map((r, k) => (
            <tr key={k}>
              <td style={{ padding: '3px 10px', whiteSpace: 'nowrap' }}>{renderInlines(r[0], `${keyPrefix}-t-a-${k}`)}</td>
              <AmountCell v={r[1]} />
              <td style={{ padding: '3px 10px', whiteSpace: 'nowrap', borderLeft: '2px solid #57534e' }}>
                {renderInlines(r[2], `${keyPrefix}-t-b-${k}`)}
              </td>
              <AmountCell v={r[3]} />
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ── 2차 답안 양식 ────────────────────────────────────────────────
// 감정평가실무 2차는 "답안을 쓰는 시험"이라 목차 계층(Ⅰ / 1. / (1) / ①)이 곧 점수다.
// 답안지 지면처럼 계층을 들여쓰고 상위 항목을 굵게 세운다.
const ANSWER_LEVELS = [
  { re: /^([ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+)[.·]?\s*(.*)$/, depth: 0, weight: 800 },
  { re: /^(\d+)\.\s*(.*)$/, depth: 1, weight: 700 },
  { re: /^(\(\d+\))\s*(.*)$/, depth: 2, weight: 600 },
  { re: /^([①-⑳])\s*(.*)$/, depth: 3, weight: 400 },
];

function AnswerSheet({ raw, keyPrefix }) {
  const rows = raw.split('\n').filter((l) => l.trim());
  return (
    <div style={{
      margin: '16px 0', border: '1px solid #dcd8cf', borderLeft: '3px solid #6b7280',
      borderRadius: 5, background: '#fdfdfc', padding: '12px 16px 14px',
    }}>
      <div style={{
        fontSize: '0.72em', fontWeight: 800, color: '#6b7280', letterSpacing: '0.04em',
        marginBottom: 8, textTransform: 'uppercase',
      }}>✍️ 답안 목차</div>
      {rows.map((l, k) => {
        const s = l.trim();
        const hit = ANSWER_LEVELS.find((lv) => lv.re.test(s));
        if (!hit) {
          return (
            <div key={k} style={{ paddingLeft: 18, margin: '2px 0', color: '#57534e', fontSize: '0.9em' }}>
              {renderInlines(s, `${keyPrefix}-ans-${k}`)}
            </div>
          );
        }
        const m = s.match(hit.re);
        return (
          <div key={k} style={{
            display: 'flex', gap: 7, paddingLeft: hit.depth * 18,
            margin: hit.depth === 0 ? '7px 0 2px' : '2px 0',
            fontWeight: hit.weight, color: hit.depth === 0 ? '#1c1917' : '#44403c',
            fontSize: hit.depth === 0 ? '0.95em' : '0.9em',
            lineHeight: 1.7,
          }}>
            <span style={{ flex: '0 0 auto', color: '#78716c' }}>{m[1]}</span>
            <span>{renderInlines(m[2], `${keyPrefix}-ans-${k}`)}</span>
          </div>
        );
      })}
    </div>
  );
}

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
    // 헤더 — 위계를 시각적으로 분명히. #~### = 절/관 타이틀(밑줄), #### = 소제목(좌측 액센트 바)
    const hMatch = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (hMatch) {
      const level = hMatch[1].length;
      const content = hMatch[2];
      const style = level <= 3
        ? {
            fontWeight: 800,
            fontSize: level === 1 ? '1.24em' : level === 2 ? '1.15em' : '1.08em',
            color: '#1c1917',
            margin: level === 1 ? '4px 0 12px' : '24px 0 10px',
            paddingBottom: 7,
            borderBottom: '1.5px solid #d6d3d1',
            letterSpacing: '-0.01em',
            lineHeight: 1.45,
          }
        : {
            fontWeight: 700,
            fontSize: '1em',
            color: '#292524',
            margin: '18px 0 7px',
            paddingLeft: 10,
            borderLeft: '3px solid #78716c',
            lineHeight: 1.45,
          };
      elements.push(
        <div key={`${keyPrefix}-h-${i}`} style={style}>
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
    // 콜아웃(인용박스) — 연속된 "> ..." 라인 묶기. 강사 여백노트/팁/보충 표현용.
    // 첫 토큰이 이모지(💡⚠️📌📖✏️🔑 등)면 라벨로 강조.
    if (/^>\s?/.test(trimmed)) {
      const raw = [];
      while (i < rawLines.length && /^>\s?/.test(rawLines[i].trim())) {
        raw.push(rawLines[i].trim().replace(/^>\s?/, ''));
        i++;
      }
      const body = raw.join('\n');
      const emojiHead = body.match(/^(\p{Extended_Pictographic}[️]?)\s*(.*)$/su);
      // 조문 인용(📌 **○○법 제N조(표제)** — "문언")은 법전 지면처럼 조·항·호·목으로 펼친다.
      const st = (emojiHead ? emojiHead[2] : body).match(STATUTE_RE);
      if (st) {
        elements.push(
          <StatuteBlock key={`${keyPrefix}-law-${i}`} title={st[1]} body={st[2]}
            keyPrefix={`${keyPrefix}-law-${i}`} />
        );
        continue;
      }
      const tone = CALLOUT_TONES[emojiHead?.[1]] || CALLOUT_TONES._default;
      elements.push(
        <div
          key={`${keyPrefix}-cal-${i}`}
          style={{
            background: tone.bg,
            borderLeft: `4px solid ${tone.bar}`,
            borderRadius: '6px',
            padding: '11px 15px',
            margin: '14px 0',
            color: '#334155',
            fontSize: '0.95em',
            lineHeight: 1.75,
          }}
        >
          {emojiHead ? (
            <>
              <span style={{ marginRight: 6 }}>{emojiHead[1]}</span>
              {renderTextBlock(emojiHead[2], `${keyPrefix}-cal-${i}-b`)}
            </>
          ) : (
            renderTextBlock(body, `${keyPrefix}-cal-${i}-b`)
          )}
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
        <ul key={`${keyPrefix}-ul-${i}`} style={{ margin: '8px 0', paddingLeft: 22 }}>
          {items.map((it, k) => (
            <li key={k} style={{ margin: '5px 0', lineHeight: 1.75 }}>{renderInlines(it, `${keyPrefix}-li-${k}`)}</li>
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
      if (ct === '' || /^(---+|___+|\*\*\*+)$/.test(ct) || /^(#{1,4})\s+/.test(ct) || /^\s*[-*]\s+/.test(cur) || /^>\s?/.test(ct) || /^[ㄱㄴㄷㄹㅁㅂㅅㅇ]\.\s+/.test(ct)) break;
      paraLines.push(cur);
      i++;
    }
    elements.push(
      <div key={`${keyPrefix}-p-${i}`} style={{ margin: '9px 0', lineHeight: 1.8 }}>
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
    // 회계 양식 fence — 재무제표 / 분개 / T계정
    const acctMatch = l.match(/^```(재무제표|분개|T계정|t계정|답안)\s*$/);
    if (vizMatch || mermaidMatch || svgMatch || acctMatch) {
      flushText();
      const kind = acctMatch
        ? (acctMatch[1] === '재무제표' ? 'fs' : acctMatch[1] === '분개' ? 'je'
           : acctMatch[1] === '답안' ? 'ans' : 'ta')
        : vizMatch ? 'viz' : mermaidMatch ? 'mermaid' : 'svg';
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
        else if (kind === 'fs' || kind === 'je' || kind === 'ta' || kind === 'ans')
          blocks.push({ type: kind, raw: bodyLines.join('\n') });
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
        if (b.type === 'fs') return <FinancialStatement key={idx} raw={b.raw} keyPrefix={`fs-${idx}`} />;
        if (b.type === 'je') return <JournalEntry key={idx} raw={b.raw} keyPrefix={`je-${idx}`} />;
        if (b.type === 'ta') return <TAccount key={idx} raw={b.raw} keyPrefix={`ta-${idx}`} />;
        if (b.type === 'ans') return <AnswerSheet key={idx} raw={b.raw} keyPrefix={`ans-${idx}`} />;
        if (b.type === 'viz_pending') {
          return <VizPending key={idx} name={b.name} />;
        }
        if (b.type === 'table') {
          return (
            <div key={idx} className="md-table-wrap" style={{ overflowX: 'auto', margin: '14px 0',
              border: '1px solid #e7e5e4', borderRadius: 6 }}>
              <table style={{ borderCollapse: 'collapse', fontSize: '0.88em',
                width: '100%', minWidth: 'max-content' }}>
                <thead>
                  <tr>
                    {b.headers.map((h, k) => (
                      <th key={k} style={{ padding: '9px 12px', background: '#f5f5f4',
                        color: '#1c1917', fontWeight: 700, textAlign: 'left',
                        whiteSpace: 'nowrap', borderBottom: '1.5px solid #d6d3d1' }}>
                        {renderTableInlines(h)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {b.rows.map((r, ri) => (
                    <tr key={ri} style={{ background: ri % 2 ? '#fafaf9' : '#fff' }}>
                      {r.map((c, ci) => (
                        <td key={ci} style={{ padding: '9px 12px', verticalAlign: 'top',
                          borderTop: ri ? '1px solid #f0efed' : 'none', lineHeight: 1.7 }}>
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
        return <div key={idx} className="parsed-text">{renderTextBlock(b.content, idx)}</div>;
      })}
    </>
  );
};

export default ParsedText;
