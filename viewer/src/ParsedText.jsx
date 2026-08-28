// 인라인 이미지([IMAGE: ...]) + KaTeX($...$) + 줄바꿈 렌더러
// App.jsx와 MockExam.jsx에서 동일한 문제 본문 렌더링을 위해 분리
import { useState, useRef } from 'react';
import { useScrollLock, useEscClose } from './uiHooks';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import VizRouter, { VizPending } from './viz/VizRouter';
import SafeSvg from './viz/SafeSvg';
import MermaidView from './viz/MermaidView';
import { recordItem } from './studyDrill';
import { GLOSSARY, GLOSSARY_RE } from './glossary';

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
// ── 용어 툴팁 — 어려운 법률 용어에 마우스를 올리면(모바일은 탭) 뜻을 보여준다 ──
function GlossaryTerm({ term, def }) {
  const [pos, setPos] = useState(null); // null=닫힘, {left,top,above}=열림
  const ref = useRef(null);
  const show = () => {
    const r = ref.current?.getBoundingClientRect();
    if (!r) return;
    const above = r.bottom + 140 > window.innerHeight; // 아래 공간 부족하면 위로
    setPos({
      left: Math.max(8, Math.min(r.left, window.innerWidth - 288)),
      top: above ? r.top - 8 : r.bottom + 6,
      above,
    });
  };
  const hide = () => setPos(null);
  return (
    <span
      ref={ref}
      onMouseEnter={show}
      onMouseLeave={hide}
      onClick={(e) => { e.stopPropagation(); pos ? hide() : show(); }}
      style={{
        borderBottom: '1px dotted #6366f1', cursor: 'help',
        textUnderlineOffset: 2, color: 'inherit',
      }}
    >
      {term}
      {pos && (
        <span
          role="tooltip"
          style={{
            position: 'fixed', left: pos.left, top: pos.top, zIndex: 5000,
            transform: pos.above ? 'translateY(-100%)' : 'none',
            width: 280, maxWidth: 'calc(100vw - 16px)',
            background: '#1f2937', color: '#f3f4f6',
            fontSize: '0.8rem', lineHeight: 1.55, fontWeight: 400,
            padding: '9px 12px', borderRadius: 9, boxShadow: '0 6px 20px rgba(0,0,0,0.28)',
            whiteSpace: 'normal', textAlign: 'left', pointerEvents: 'none',
            fontFamily: 'inherit',
          }}
        >
          <b style={{ color: '#c7d2fe' }}>{term}</b>
          <span style={{ display: 'block', marginTop: 3 }}>{def}</span>
        </span>
      )}
    </span>
  );
}

// 평문에서 사전 용어를 찾아 GlossaryTerm으로 감싼다. 없으면 문자열 그대로 반환.
function withGlossary(text, keyPrefix) {
  if (!GLOSSARY_RE || !text) return text;
  const parts = String(text).split(GLOSSARY_RE);
  if (parts.length < 2) return text; // 매칭 없음
  return parts.map((p, i) =>
    (i % 2 === 1 && GLOSSARY[p])
      ? <GlossaryTerm key={`${keyPrefix}-gl${i}`} term={p} def={GLOSSARY[p]} />
      : p
  );
}

// 인라인 수식($…$)과 일반 텍스트를 섞어 렌더. 굵게·형광펜 **안쪽**에서도 수식이 살아나도록
// 별도 함수로 뺐다. plain=true 면 용어 사전(withGlossary)까지 적용한다.
const renderMathish = (str, keyBase, plain = false) => {
  const nodes = [];
  String(str).split(/(\$[\s\S]*?\$)/g).forEach((mp, j) => {
    if (mp.startsWith('$') && mp.endsWith('$') && mp.length > 2) {
      try {
        const html = katex.renderToString(mp.slice(1, -1), { throwOnError: false, output: 'html' });
        nodes.push(<span key={`${keyBase}-${j}-m`} dangerouslySetInnerHTML={{ __html: html }} />);
      } catch {
        nodes.push(<span key={`${keyBase}-${j}-m`}>{mp}</span>);
      }
    } else if (mp) {
      nodes.push(
        <span key={`${keyBase}-${j}-t`}>{plain ? withGlossary(mp, `${keyBase}-${j}`) : mp}</span>
      );
    }
  });
  return nodes;
};

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
      // 3) bold(**…**) · 형광펜(==…==) 을 **수식보다 먼저** 분리한다.
      //    수식을 먼저 쪼개면 `**$IS_0$ · 케인즈 단순모형**` 처럼 굵게 안에 수식이 든 표현이
      //    `**` 와 나머지로 찢어져 굵게 정규식에 걸리지 않고 별표가 글자로 새어 나온다.
      const boldParts = dp.split(/(\*\*[^*]+\*\*|==(?:(?!==)[\s\S])+==)/g);
      boldParts.forEach((bp, k) => {
        const base = `${keyPrefix}-${i}-${di}-${k}`;
        if (bp.startsWith('**') && bp.endsWith('**') && bp.length > 4) {
          out.push(<strong key={`${base}-b`}>{renderMathish(bp.slice(2, -2), `${base}-b`)}</strong>);
        } else if (bp.startsWith('==') && bp.endsWith('==') && bp.length > 4) {
          out.push(<mark key={`${base}-hl`} style={HILITE}>{renderMathish(bp.slice(2, -2), `${base}-hl`)}</mark>);
        } else if (bp) {
          out.push(...renderMathish(bp, base, true));
        }
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
  // 복습 메이트(마스코트)가 거드는 말 — 강사 발언이 아니라 정리·조언이라는 표시.
  // 다른 콜아웃과 성격이 다르므로 유일하게 푸른 계열을 쓰되 채도는 낮게 둔다.
  '🐶': { bg: '#f5f7fb', bar: '#7c8db5' },
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

// ── 조문 cloze(빈칸 가리기) — 인출 훈련 ─────────────────────────────
// 조문에서 시험·암기의 핵심은 '수치(기간·비율·요건)'와 '핵심 법령어'다.
// 이들을 빈칸으로 가리고, 탭하면 하나씩 드러나 스스로 떠올렸는지 확인한다.
const CLOZE_NUM = String.raw`\d[\d,.]*(?:\s*(?:분의\s*\d+|년|개월|달|월|일|시간|주|퍼센트|%|배|원|만원|억원|명|개|호|회|이상|이하|미만|초과|이내))?`;
const CLOZE_KEYWORDS = [
  '국토교통부장관', '시장·군수·구청장', '감정평가법인등', '중앙토지수용위원회', '지방토지수용위원회',
  '시·도지사', '시장·군수', '지정권자', '이해관계인', '손실보상', '이의신청', '의견청취',
  '재결', '수용', '사용', '허가', '신고', '승인', '인가', '고시', '지정', '변경', '결정',
  '협의', '공람', '열람', '심의', '보상금', '공익사업', '사업시행자', '토지소유자',
];
const CLOZE_RE_SRC = `(${CLOZE_NUM})|(${[...CLOZE_KEYWORDS].sort((a, b) => b.length - a.length).map((k) => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})`;

function StatuteClozeText({ text, keyBase, shownAll, revealed, onToggle }) {
  const re = new RegExp(CLOZE_RE_SRC, 'g');
  const parts = [];
  let last = 0, m, idx = 0;
  while ((m = re.exec(text))) {
    if (m.index > last) parts.push(text.slice(last, m.index));
    let word = m[0], trail = '';
    const t = word.match(/[.,]+$/);
    if (t && /\d/.test(word)) { trail = t[0]; word = word.slice(0, -trail.length); }
    const id = `${keyBase}-${idx++}`;
    const shown = shownAll || revealed.has(id);
    parts.push(
      <button key={id} type="button" onClick={() => onToggle(id)}
        style={{
          display: 'inline-block', verticalAlign: 'baseline', font: 'inherit', cursor: 'pointer',
          margin: '0 1px', padding: '0 3px', borderRadius: 3,
          border: shown ? '1px solid transparent' : '1px dashed #b08d57',
          borderBottom: '1.5px solid #b08d57',
          background: shown ? 'transparent' : '#f3ead2',
          color: shown ? '#a15c07' : 'transparent',
          minWidth: `${Math.max(1.4, Math.min(7, word.length))}em`,
          fontWeight: shown ? 700 : 400,
        }}>
        {shown ? word : ' '.repeat(Math.max(2, Math.min(6, word.length)))}
      </button>
    );
    if (trail) parts.push(trail);
    last = m.index + m[0].length;
  }
  if (last < text.length) parts.push(text.slice(last));
  return parts.length ? parts : text;
}

function StatuteBlock({ title, body, keyPrefix }) {
  const [lawName, article] = splitStatuteTitle(title);
  const tokens = parseStatuteBody(body);
  const [cloze, setCloze] = useState(false);
  const [shownAll, setShownAll] = useState(false);
  const [revealed, setRevealed] = useState(() => new Set());
  const toggleOne = (id) => setRevealed((prev) => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n; });
  const startCloze = () => { setCloze(true); setShownAll(false); setRevealed(new Set()); };
  const hasBlank = cloze && new RegExp(CLOZE_RE_SRC).test(body);
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
        <button type="button"
          onClick={() => (cloze ? setCloze(false) : startCloze())}
          title="핵심 수치·법령어를 빈칸으로 가리고 인출 훈련"
          style={{
            marginLeft: 'auto', fontSize: '0.72em', fontWeight: 700, cursor: 'pointer',
            border: `1px solid ${cloze ? '#b08d57' : '#ddd5c2'}`, borderRadius: 3, padding: '1px 8px',
            background: cloze ? '#f3ead2' : '#fdfcf8', color: cloze ? '#8a5a12' : '#7c7259',
            fontFamily: 'inherit', whiteSpace: 'nowrap',
          }}>
          {cloze ? '👁 답 보기' : '🙈 빈칸'}
        </button>
        {cloze && (
          <button type="button" onClick={() => setShownAll((v) => !v)}
            style={{
              fontSize: '0.72em', fontWeight: 700, cursor: 'pointer',
              border: '1px solid #ddd5c2', borderRadius: 3, padding: '1px 8px',
              background: '#fdfcf8', color: '#7c7259', fontFamily: 'inherit', whiteSpace: 'nowrap',
            }}>
            {shownAll ? '다시 가리기' : '모두 보기'}
          </button>
        )}
        {lawName && (
          <span style={{
            fontSize: '0.74em', fontWeight: 700, color: '#7c7259',
            border: '1px solid #ddd5c2', borderRadius: 3, padding: '1px 7px', background: '#fdfcf8',
            fontFamily: 'inherit', whiteSpace: 'nowrap',
          }}>
            {lawName}
          </span>
        )}
      </div>
      {cloze && !hasBlank && (
        <div style={{ padding: '6px 14px', fontSize: '0.76em', color: '#9a8c6a', background: '#faf7ee' }}>
          이 조문에는 가릴 수치·핵심어가 없어요.
        </div>
      )}
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
              {cloze
                ? <StatuteClozeText text={t.text} keyBase={`${keyPrefix}-cz-${k}`} shownAll={shownAll} revealed={revealed} onToggle={toggleOne} />
                : renderInlines(t.text, `${keyPrefix}-st-${k}`)}
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

// ── 계산 연습 ────────────────────────────────────────────────────
// 회계는 "읽어서" 늘지 않고 "손으로 풀어야" 는다. 풀이를 가려 두고 스스로 세운 뒤 열어 본다.
// (합격수기 공통: 회계는 휘발성 1위 — 정형 틀을 안 보고 재현하는 인출 연습이 핵심)
// `표:` 섹션이 있으면 상각표·전개표를 직접 채워 채점받는 표 채우기 연습이 된다.
//   표: 유효이자율 상각표
//   연도 | 기초장부 | 유효이자 | 표시이자 | 상각액 | 기말장부
//   20X1 | 950,263 | ?95,026 | ?80,000 | ?15,026 | ?965,289   ← ?뒤가 정답인 빈칸
function PracticeCard({ raw, keyPrefix, seq = 0 }) {
  const [open, setOpen] = useState(false);
  const [hint, setHint] = useState(false);
  const [graded, setGraded] = useState(null);
  const [typed, setTyped] = useState({});
  const [checked, setChecked] = useState(false);
  const parts = { 문제: [], 힌트: [], 풀이: [], 답: [] };
  let caption = '';
  const tblRows = [];
  let cur = '문제';
  for (const l of raw.split('\n')) {
    const m = l.match(/^\s*(문제|힌트|풀이|답|표)\s*[:：]\s*(.*)$/);
    if (m) {
      if (m[1] === '표') { cur = '표'; caption = m[2].trim(); continue; }
      cur = m[1]; if (m[2].trim()) parts[cur].push(m[2]); continue;
    }
    if (cur === '표' && l.includes('|')) { tblRows.push(l.split('|').map((c) => c.trim())); continue; }
    if (cur === '표') { if (l.trim()) parts['문제'].push(l); continue; }  // 표 밖 줄은 문제로
    parts[cur].push(l);
  }
  const body = (k) => parts[k].join('\n').trim();
  const solution = [body('풀이'), body('답') && `**답 — ${body('답')}**`].filter(Boolean).join('\n\n');
  // 표 채우기 준비
  const header = tblRows.length ? tblRows[0] : null;
  const data = tblRows.slice(1);
  const blanks = [];
  data.forEach((r, ri) => r.forEach((c, ci) => { if (c.startsWith('?')) blanks.push({ ri, ci, ans: c.slice(1).trim() }); }));
  const hasTable = header && blanks.length > 0;
  const key = (ri, ci) => `${ri}-${ci}`;
  const rightN = checked ? blanks.filter((b) => fmtAmount(typed[key(b.ri, b.ci)] ?? '') === fmtAmount(b.ans)).length : 0;
  const checkTable = () => {
    setChecked(true);
    const ok = blanks.every((b) => fmtAmount(typed[key(b.ri, b.ci)] ?? '') === fmtAmount(b.ans));
    setGraded(ok);
    recordItem({ kind: 'prac', idx: seq, q: body('문제') || caption, isCorrect: ok });
  };
  const grade = (ok) => {
    setGraded(ok);
    recordItem({ kind: 'prac', idx: seq, q: body('문제'), isCorrect: ok });
  };
  return (
    <div style={{
      margin: '14px 0', border: '1px solid #dcd8cf', borderRadius: 6, overflow: 'hidden',
      background: '#fffefb',
    }}>
      <div style={{
        display: 'flex', alignItems: 'center', gap: 8, padding: '7px 13px',
        background: '#f6f4ee', borderBottom: '1px solid #e7e3d9',
      }}>
        <span style={{ fontSize: '0.74em', fontWeight: 800, color: '#6b6250', letterSpacing: '0.03em' }}>
          🧮 계산 연습
        </span>
        {body('힌트') && (
          <button onClick={() => setHint((v) => !v)} style={{
            marginLeft: 'auto', fontSize: '0.71em', fontWeight: 700, padding: '3px 9px', borderRadius: 5,
            cursor: 'pointer', border: '1px solid #e0dbcf', background: hint ? '#faf8f2' : '#fff', color: '#8a7f6a',
          }}>{hint ? '힌트 닫기' : '💡 힌트'}</button>
        )}
        <button onClick={() => setOpen((v) => !v)} style={{
          marginLeft: body('힌트') ? 0 : 'auto',
          fontSize: '0.71em', fontWeight: 800, padding: '3px 10px', borderRadius: 5, cursor: 'pointer',
          border: '1px solid ' + (open ? '#a16207' : '#d6d3d1'),
          background: open ? '#faf8f2' : '#fff', color: open ? '#a16207' : '#57534e',
        }}>{open ? '🔒 다시 가리기' : '👁 풀이 보기'}</button>
      </div>
      {open && graded === null && !hasTable && (
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8, padding: '7px 13px',
          background: '#fcfbf7', borderBottom: '1px solid #eee9dd', fontSize: '0.76em', color: '#6b6250',
        }}>
          <span style={{ fontWeight: 700 }}>스스로 채점하세요</span>
          <button onClick={() => grade(true)} style={{
            marginLeft: 'auto', fontSize: '0.95em', fontWeight: 800, padding: '3px 12px', borderRadius: 5,
            cursor: 'pointer', border: '1.5px solid #4d7c5f', background: '#fff', color: '#4d7c5f',
          }}>✓ 맞음</button>
          <button onClick={() => grade(false)} style={{
            fontSize: '0.95em', fontWeight: 800, padding: '3px 12px', borderRadius: 5,
            cursor: 'pointer', border: '1.5px solid #9a3412', background: '#fff', color: '#9a3412',
          }}>✗ 틀림</button>
        </div>
      )}
      {graded !== null && (
        <div style={{
          padding: '6px 13px', fontSize: '0.76em', fontWeight: 800,
          background: graded ? '#f5f8f5' : '#fbf5f3', color: graded ? '#4d7c5f' : '#9a3412',
          borderBottom: '1px solid ' + (graded ? '#e3ece3' : '#f0e2dc'),
        }}>{graded ? '✓ 맞음으로 기록했습니다' : '✗ 틀림으로 기록했습니다 — 오답 목록에 들어갑니다'}</div>
      )}
      <div style={{ padding: '11px 14px' }}>
        {renderTextBlock(body('문제'), `${keyPrefix}-q`)}
        {hint && body('힌트') && (
          <div style={{
            margin: '9px 0 0', padding: '8px 12px', background: '#faf8f2',
            borderLeft: '3px solid #a16207', borderRadius: 4, fontSize: '0.93em',
          }}>{renderTextBlock(body('힌트'), `${keyPrefix}-h`)}</div>
        )}
        {hasTable && (
          <div style={{ marginTop: 10, border: '1px solid #cfd8e3', borderRadius: 6, background: '#fbfcfe', overflow: 'hidden' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 12px', background: '#eef2f7', borderBottom: '1px solid #dde4ed' }}>
              <span style={{ fontSize: '0.73em', fontWeight: 800, color: '#44546a' }}>📊 표 채우기{caption ? ` — ${caption}` : ''}</span>
              {checked && (
                <span style={{ fontSize: '0.73em', fontWeight: 800, color: rightN === blanks.length ? '#4d7c5f' : '#9a3412' }}>
                  {rightN} / {blanks.length} 정답{rightN === blanks.length ? ' · 완성!' : ''}
                </span>
              )}
              <button onClick={checkTable} style={{
                marginLeft: 'auto', fontSize: '0.71em', fontWeight: 800, padding: '3px 11px', borderRadius: 5,
                cursor: 'pointer', border: '1.5px solid #2563eb', background: '#fff', color: '#2563eb',
              }}>채점</button>
              {checked && (
                <button onClick={() => { setChecked(false); setTyped({}); setGraded(null); }} style={{
                  fontSize: '0.71em', fontWeight: 700, padding: '3px 9px', borderRadius: 5, cursor: 'pointer',
                  border: '1px solid #d6d3d1', background: '#fff', color: '#57534e',
                }}>🔄</button>
              )}
            </div>
            <div style={{ overflowX: 'auto', padding: '0 6px 8px' }}>
              <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: '0.86em' }}>
                <thead><tr>{header.map((h, ci) => (
                  <th key={ci} style={{ padding: '5px 10px', borderBottom: '1.5px solid #57534e', fontWeight: 700,
                    color: '#44403c', textAlign: ci === 0 ? 'left' : 'right', whiteSpace: 'nowrap' }}>{h}</th>
                ))}</tr></thead>
                <tbody>{data.map((r, ri) => (
                  <tr key={ri}>{r.map((c, ci) => {
                    if (!c.startsWith('?')) return (
                      <td key={ci} style={{ padding: '4px 10px', whiteSpace: 'nowrap', textAlign: ci === 0 ? 'left' : 'right',
                        fontFamily: ci === 0 ? undefined : MONO, color: '#292524' }}>{renderInlines(c, `${keyPrefix}-t${ri}-${ci}`)}</td>
                    );
                    const ans = c.slice(1).trim();
                    const got = (typed[key(ri, ci)] ?? '').trim();
                    const ok = checked && fmtAmount(got) === fmtAmount(ans);
                    const ng = checked && !ok;
                    return (
                      <td key={ci} style={{ padding: '3px 8px', textAlign: 'right', whiteSpace: 'nowrap' }}>
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5 }}>
                          <input value={typed[key(ri, ci)] ?? ''}
                            onChange={(e) => setTyped((s) => ({ ...s, [key(ri, ci)]: e.target.value }))} placeholder="?"
                            style={{ width: 90, textAlign: 'right', fontFamily: MONO, fontSize: '0.95em', padding: '2px 6px',
                              borderRadius: 4, border: '1px solid ' + (ng ? '#9a3412' : ok ? '#4d7c5f' : '#c9d3df'),
                              background: ng ? '#fbf5f3' : ok ? '#f5f8f5' : '#fff', color: '#1f2937' }} />
                          {ng && <span style={{ fontSize: '0.82em', color: '#9a3412', fontWeight: 700 }}>{fmtAmount(ans)}</span>}
                          {ok && <span style={{ fontSize: '0.82em', color: '#4d7c5f', fontWeight: 800 }}>✓</span>}
                        </span>
                      </td>
                    );
                  })}</tr>
                ))}</tbody>
              </table>
            </div>
          </div>
        )}
      </div>
      {solution && (
        <div
          onClick={() => !open && setOpen(true)}
          style={{
            position: 'relative', padding: '11px 14px', borderTop: '1px dashed #e0dbcf',
            background: '#fdfdfb', cursor: open ? 'default' : 'pointer',
            filter: open ? 'none' : 'blur(5px)', opacity: open ? 1 : 0.5,
            userSelect: open ? 'auto' : 'none', transition: 'filter .15s, opacity .15s',
          }}
        >
          {renderTextBlock(solution, `${keyPrefix}-a`)}
        </div>
      )}
      {!open && solution && (
        <div onClick={() => setOpen(true)} style={{
          textAlign: 'center', padding: '0 0 10px', marginTop: -34, position: 'relative',
          fontSize: '0.76em', color: '#8a7f6a', cursor: 'pointer', fontWeight: 700,
        }}>먼저 직접 풀어 보세요 · 클릭하면 풀이가 열립니다</div>
      )}
    </div>
  );
}

// ── 와꾸(정형 풀이 틀) ────────────────────────────────────────────
// 계산 유형마다 정해진 틀이 있다. 그 틀을 **안 보고 재현**하는 것이 인출 연습이다.
// 값을 가려 빈 틀로 만들었다가 채워 볼 수 있다.
function FrameCard({ raw, keyPrefix, seq = 0 }) {
  const [blank, setBlank] = useState(false);
  const [fill, setFill] = useState(false);      // 직접 입력해 재현하는 모드
  const [typed, setTyped] = useState({});
  const [checked, setChecked] = useState(false);
  let title = '';
  const rows = [];
  for (const l of raw.split('\n')) {
    if (!l.trim()) continue;
    const m = l.match(/^\s*(제목|틀)\s*[:：]\s*(.*)$/);
    if (m) { title = m[2].trim(); continue; }
    const c = l.split('|');
    rows.push([c[0] ?? '', (c[1] ?? '').trim(), (c[2] ?? '').trim()]);
  }
  return (
    <div style={{
      margin: '14px 0', border: '1.5px solid #cfd8e3', borderRadius: 6,
      background: '#fbfcfe', overflow: 'hidden',
    }}>
      <div style={{
        display: 'flex', alignItems: 'center', gap: 8, padding: '7px 13px',
        background: '#eef2f7', borderBottom: '1px solid #dde4ed',
      }}>
        <span style={{ fontSize: '0.74em', fontWeight: 800, color: '#44546a', letterSpacing: '0.03em' }}>
          📐 와꾸{title ? ` — ${title}` : ''}
        </span>
        <button onClick={() => setBlank((v) => !v)} style={{
          marginLeft: 'auto', fontSize: '0.71em', fontWeight: 800, padding: '3px 10px', borderRadius: 5,
          cursor: 'pointer', border: '1px solid ' + (blank ? '#2563eb' : '#d6dde6'),
          background: blank ? '#eff6ff' : '#fff', color: blank ? '#2563eb' : '#57534e',
        }}>{blank ? '👁 채운 틀 보기' : '✍️ 빈 틀로 연습'}</button>
        <button onClick={() => { setFill((v) => !v); setChecked(false); setTyped({}); setBlank(false); }} style={{
          fontSize: '0.71em', fontWeight: 800, padding: '3px 10px', borderRadius: 5,
          cursor: 'pointer', border: '1px solid ' + (fill ? '#a16207' : '#d6dde6'),
          background: fill ? '#faf8f2' : '#fff', color: fill ? '#a16207' : '#57534e',
        }}>{fill ? '✕ 훈련 종료' : '🧠 재현 훈련'}</button>
      </div>
      {fill && (
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8, padding: '7px 13px',
          background: '#fcfbf7', borderBottom: '1px solid #eee9dd', fontSize: '0.76em', color: '#6b6250',
        }}>
          <span style={{ fontWeight: 700 }}>틀을 보지 않고 값을 채워 보세요</span>
          <button onClick={() => {
            setChecked(true);
            const wrong = rows.filter((r) => {
              const want = fmtAmount(r[1]);
              const got = (typed[rows.indexOf(r)] ?? '').trim();
              return want !== '—' && got !== '' && fmtAmount(got) !== want;
            }).length;
            const blankN = rows.filter((r, k) => (typed[k] ?? '').trim() === '' && fmtAmount(r[1]) !== '—').length;
            recordItem({ kind: 'frame', idx: seq, q: `[와꾸] ${title || keyPrefix}`,
              isCorrect: wrong === 0 && blankN === 0 });
          }} style={{
            marginLeft: 'auto', fontSize: '0.95em', fontWeight: 800, padding: '3px 12px', borderRadius: 5,
            cursor: 'pointer', border: '1.5px solid #2563eb', background: '#fff', color: '#2563eb',
          }}>대조하기</button>
        </div>
      )}
      <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: '0.88em' }}>
        <tbody>
          {rows.map((r, k) => {
            const label = r[0];
            const strong = /^\s*=/.test(label);
            const clean = label.replace(/^\s*=\s*/, '').trimEnd();
            const pad = (clean.match(/^\s*/) || [''])[0].length;
            return (
              <tr key={k}>
                <td style={{
                  padding: '3px 12px', paddingLeft: 12 + pad * 4, whiteSpace: 'nowrap',
                  fontWeight: strong ? 700 : 400, color: '#1f2937',
                  borderTop: strong ? '1px solid #9ca3af' : undefined,
                }}>{renderInlines(clean.trim(), `${keyPrefix}-f-${k}`)}</td>
                <td style={{
                  textAlign: 'right', fontFamily: MONO, fontVariantNumeric: 'tabular-nums',
                  padding: '3px 12px', whiteSpace: 'nowrap', fontWeight: strong ? 700 : 400,
                  color: blank ? '#c7cdd4' : '#1f2937',
                  borderTop: strong ? '1px solid #9ca3af' : undefined,
                }}>
                  {fill ? (() => {
                    const want = fmtAmount(r[1]);
                    const got = (typed[k] ?? '').trim();
                    const ok = checked && want !== '—' && fmtAmount(got) === want;
                    const ng = checked && want !== '—' && !ok;
                    return (
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
                        <input
                          value={typed[k] ?? ''}
                          onChange={(e) => setTyped((s) => ({ ...s, [k]: e.target.value }))}
                          placeholder={want === '—' ? '' : '?'}
                          disabled={want === '—'}
                          style={{
                            width: 96, textAlign: 'right', fontFamily: MONO, fontSize: '0.95em',
                            padding: '2px 6px', borderRadius: 4,
                            border: '1px solid ' + (ng ? '#9a3412' : ok ? '#4d7c5f' : '#d6dde6'),
                            background: want === '—' ? '#f5f5f4' : ng ? '#fbf5f3' : ok ? '#f5f8f5' : '#fff',
                            color: '#1f2937',
                          }}
                        />
                        {ng && <span style={{ fontSize: '0.8em', color: '#9a3412', fontWeight: 700 }}>{want}</span>}
                        {ok && <span style={{ fontSize: '0.8em', color: '#4d7c5f', fontWeight: 800 }}>✓</span>}
                      </span>
                    );
                  })() : blank ? '________' : fmtAmount(r[1])}
                </td>
                {rows.some((x) => x[2]) && (
                  <td style={{ padding: '3px 12px', fontSize: '0.9em', color: '#6b7280' }}>
                    {renderInlines(r[2], `${keyPrefix}-fn-${k}`)}
                  </td>
                )}
              </tr>
            );
          })}
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

function AnswerSheet({ raw, keyPrefix, seq = 0 }) {
  const rows = raw.split('\n').filter((l) => l.trim());
  // 2차는 목차 자체가 점수다. 가려 놓고 안 보고 재현하는 것이 곧 인출 훈련이다.
  const [hide, setHide] = useState(false);
  return (
    <div style={{
      margin: '16px 0', border: '1px solid #dcd8cf', borderLeft: '3px solid #6b7280',
      borderRadius: 5, background: '#fdfdfc', padding: '12px 16px 14px',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
        <span style={{
          fontSize: '0.72em', fontWeight: 800, color: '#6b7280', letterSpacing: '0.04em',
          textTransform: 'uppercase',
        }}>✍️ 답안 목차</span>
        <button onClick={() => setHide((v) => !v)} style={{
          marginLeft: 'auto', fontSize: '0.71em', fontWeight: 800, padding: '3px 10px', borderRadius: 5,
          cursor: 'pointer', border: '1px solid ' + (hide ? '#a16207' : '#dcd8cf'),
          background: hide ? '#faf8f2' : '#fff', color: hide ? '#a16207' : '#57534e',
        }}>{hide ? '👁 목차 보기' : '🧠 가리고 재현'}</button>
        {hide && (
          <button onClick={() => { setHide(false); recordItem({ kind: 'outline', idx: seq, q: `[답안목차] ${rows[0] || keyPrefix}`, isCorrect: true }); }}
            style={{
              fontSize: '0.71em', fontWeight: 800, padding: '3px 10px', borderRadius: 5, cursor: 'pointer',
              border: '1.5px solid #4d7c5f', background: '#fff', color: '#4d7c5f',
            }}>✓ 재현했다</button>
        )}
      </div>
      {rows.map((l, k) => {
        const s = l.trim();
        const hit = ANSWER_LEVELS.find((lv) => lv.re.test(s));
        if (!hit) {
          return (
            <div key={k} style={{ paddingLeft: 18, margin: '2px 0', color: '#57534e', fontSize: '0.9em' }}>
              {hide ? <span style={{ color: '#d6d3d1' }}>{'_'.repeat(Math.min(28, s.length))}</span>
                    : renderInlines(s, `${keyPrefix}-ans-${k}`)}
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
            <span>{hide
              ? <span style={{ color: '#d6d3d1', letterSpacing: '0.06em' }}>
                  {'_'.repeat(Math.max(6, Math.min(24, (m[2] || '').length)))}
                </span>
              : renderInlines(m[2], `${keyPrefix}-ans-${k}`)}</span>
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

// ── 대표 예제·사례형의 풀이 가리기 ──────────────────────────────
// `#### ✏️ 대표 예제` / `#### ✏️ 사례형 적용` 섹션에서 문제(콜아웃)는 남기고
// 풀이만 가린다. 스스로 풀어 본 뒤 열어 보게 하려는 것.
// 데이터를 건드리지 않고, 풀이 구간을 <!--풀이가림--> 센티넬로 감싼 뒤
// 블록 파서가 reveal 블록으로 렌더한다(내부에 ```표·분개 펜스가 있어도 안전).
const EX_HEAD = /^####\s*✏️\s*(대표\s*예제|사례형\s*적용)/;
const SOLUTION_MARK = /^\s*\*\*(풀이|검토|해설|정답|답)\b/;
function wrapExampleSolutions(text) {
  const src = text.split('\n');
  const out = [];
  let i = 0;
  while (i < src.length) {
    if (!EX_HEAD.test(src[i])) { out.push(src[i]); i += 1; continue; }
    out.push(src[i]); i += 1;                      // 예제 헤딩은 그대로
    // 섹션 본문 = 다음 헤딩(또는 EOF) 전까지
    const start = i;
    while (i < src.length && !/^#{1,6}\s/.test(src[i])) i += 1;
    const body = src.slice(start, i);
    // 분할점: 풀이 마커 우선, 없으면 선행 콜아웃 블록 뒤
    let cut = body.findIndex((l) => SOLUTION_MARK.test(l));
    if (cut < 0) {
      let k = 0;
      while (k < body.length && body[k].trim() === '') k += 1;
      if (k < body.length && /^\s*>/.test(body[k])) {   // 문제가 콜아웃이면
        while (k < body.length && (/^\s*>/.test(body[k]) || body[k].trim() === '')) k += 1;
        cut = k;
      }
    }
    const hasSolution = cut >= 0 && body.slice(cut).some((l) => l.trim());
    const hasProblem = cut > 0 && body.slice(0, cut).some((l) => l.trim());
    // 문제·풀이 어느 쪽이든 비면 그대로 둔다(문제까지 가리는 사고 방지)
    if (!hasSolution || !hasProblem) { out.push(...body); continue; }
    out.push(...body.slice(0, cut));
    out.push('<!--풀이가림-->');
    out.push(...body.slice(cut));
    out.push('<!--/풀이가림-->');
  }
  return out.join('\n');
}

// 풀이 가림 블록 — 클릭하면 열리고 다시 가릴 수 있다.
function SolutionReveal({ raw, keyPrefix }) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ margin: '4px 0 10px' }}>
      <button onClick={() => setOpen((v) => !v)} style={{
        fontSize: '0.74rem', fontWeight: 800, padding: '4px 11px', borderRadius: 6, cursor: 'pointer',
        border: '1px solid ' + (open ? '#a16207' : '#d6d3d1'),
        background: open ? '#faf8f2' : '#fff', color: open ? '#a16207' : '#57534e',
      }}>{open ? '🔒 풀이 가리기' : '👁 풀이 보기'}</button>
      <div
        onClick={() => !open && setOpen(true)}
        style={{
          position: 'relative', marginTop: 6, borderRadius: 8, padding: '2px 12px',
          background: open ? 'transparent' : '#f7f7f6', cursor: open ? 'default' : 'pointer',
          filter: open ? 'none' : 'blur(6px)', opacity: open ? 1 : 0.5,
          userSelect: open ? 'auto' : 'none', transition: 'filter .15s, opacity .15s',
        }}
      >
        <ParsedText text={raw} />
      </div>
      {!open && (
        <div onClick={() => setOpen(true)} style={{
          textAlign: 'center', marginTop: -30, position: 'relative', paddingBottom: 8,
          fontSize: '0.75rem', fontWeight: 700, color: '#8a7f6a', cursor: 'pointer',
        }}>먼저 스스로 풀어 보세요 · 클릭하면 풀이가 열립니다</div>
      )}
    </div>
  );
}

export const ParsedText = ({ text }) => {
  if (!text) return null;
  // 라인 단위로 스캔하면서 표 블록과 일반 텍스트 블록을 교차 추출
  const lines = wrapExampleSolutions(text).split('\n');
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
    // 풀이 가림 센티넬 — 내부에 ``` 펜스가 있어도 안전하도록 주석 마커로 감싼다.
    if (l.trim() === '<!--풀이가림-->') {
      flushText();
      const bodyLines = [];
      let j = i + 1;
      while (j < lines.length && lines[j].trim() !== '<!--/풀이가림-->') { bodyLines.push(lines[j]); j += 1; }
      blocks.push({ type: 'reveal', raw: bodyLines.join('\n') });
      i = j + 1;
      continue;
    }
    // 시각자료 fence 감지: ```viz <template-name>  /  ```mermaid  /  ```svg
    const vizMatch = l.match(/^```(viz)\s+([a-z0-9_-]+)\s*$/i);
    const mermaidMatch = l.match(/^```mermaid\s*$/i);
    const svgMatch = l.match(/^```svg\s*$/i);
    // 회계 양식 fence — 재무제표 / 분개 / T계정
    const acctMatch = l.match(/^```(재무제표|분개|T계정|t계정|답안|연습|와꾸)\s*$/);
    if (vizMatch || mermaidMatch || svgMatch || acctMatch) {
      flushText();
      const kind = acctMatch
        ? (acctMatch[1] === '재무제표' ? 'fs' : acctMatch[1] === '분개' ? 'je'
           : acctMatch[1] === '답안' ? 'ans' : acctMatch[1] === '연습' ? 'prac'
           : acctMatch[1] === '와꾸' ? 'frame' : 'ta')
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
        else if (['fs','je','ta','ans','prac','frame'].includes(kind))
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
        if (b.type === 'reveal') return <SolutionReveal key={idx} raw={b.raw} keyPrefix={`rv-${idx}`} />;
        if (b.type === 'ans') {
          const seq = blocks.slice(0, idx).filter((x) => x.type === 'ans').length;
          return <AnswerSheet key={idx} raw={b.raw} keyPrefix={`ans-${idx}`} seq={seq} />;
        }
        if (b.type === 'prac') {
          const seq = blocks.slice(0, idx).filter((x) => x.type === 'prac').length;
          return <PracticeCard key={idx} raw={b.raw} keyPrefix={`prac-${idx}`} seq={seq} />;
        }
        if (b.type === 'frame') {
          const seq = blocks.slice(0, idx).filter((x) => x.type === 'frame').length;
          return <FrameCard key={idx} raw={b.raw} keyPrefix={`frame-${idx}`} seq={seq} />;
        }
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
