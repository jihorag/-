// 강조 규칙 — 형광펜은 두 색, 나머지는 굵기.
//
// 2026-09-01 개정. 예전에는 네 색(이름·뒤집힘·수치·결론)이었는데, 한 말풍선에
// 서너 자리가 칠해지면 강조가 아니라 배경이 된다. 색을 늘리는 대신 형광펜이
// 하는 일을 둘로 줄이고, 나머지는 굵기로만 세운다.
//
//   노랑 형광펜   외울 공식·정의            → 매입원가 + 전환원가 + 기타 원가
//   보라 형광펜   시험이 뒤집는 자리        → 수익으로 잡는 것이 아닙니다
//   굵게          문장 속 핵심, 수치        → 매입원가에 붙습니다 / 60%
//
// 초록·파랑은 쓰지 않는다. 색은 노랑과 보라 둘뿐이다.
//
// 지키는 것 둘:
//   · 형광펜은 **구(句) 단위**로만. 낱말 하나, 특히 숫자 하나에는 달지 않는다.
//     「하위 10%가 사회 부의 10%」에서 10% 마다 칠하면 문장이 얼룩진다.
//   · 한 말풍선에 형광펜은 **하나까지**. 노랑과 보라를 같은 말풍선에 함께 쓰지 않는다.
//
// 데이터에 손대지 않고 렌더할 때 적용한다. 규칙이 모든 대사에 똑같이 걸리므로
// 「이 논점만 형광펜이 없다」가 생기지 않는다.
//
// 이미 저자가 손으로 넣은 마크업(**굵게**, ==형광펜==, $수식$)은 건드리지 않는다.

export const ROLES = ['공식', '뒤집힘'];

// 저자 마크업 · 수식 구간은 규칙을 적용하지 않는다.
const PROTECTED = /(\*\*[^*]+\*\*|==(?:(?!==)[\s\S])+==|\$[^$]*\$|\[IMAGE:[^\]]*\])/g;

// 형광펜을 달 수 있는 최소 길이. 이보다 짧으면 구가 아니라 낱말이다.
const MIN_PHRASE = 6;

// ── 형광펜 (한 대사에 통틀어 하나) ─────────────────────────────────────
// 순서가 곧 우선순위. 뒤집히는 자리가 공식보다 시험에서 더 값이 나가므로 먼저 본다.
const HILITE = [
  {
    role: '뒤집힘',
    // 「A가 아니라 B」·「~와 달리」 같은 대비 표지. 표지 하나만 칠하면 뜻이 없어
    // 그 뒤 한 마디까지 함께 잡는다.
    re: /[^\s,.]{1,14}(?:이|가)\s*아니라[^.。\n]{0,24}|[^\s,.]{1,14}(?:와|과)\s*달리[^.。\n]{0,24}|(?:반대로|거꾸로)[^.。\n]{2,24}|[^\s,.]{0,14}(?:헷갈리기|착각하기)\s*쉽[^.。\n]{0,20}/g,
  },
  {
    role: '공식',
    // 등호·더하기로 이어진 식, 또는 따옴표로 묶인 정의어.
    re: /[^\s。\n]+\s*(?:=|＝)\s*[^.。\n]{3,40}|[^\s,.]{2,20}(?:\s*\+\s*[^\s,.]{2,20}){1,4}|'[^'\n]{4,24}'/g,
  },
];

// ── 굵기 ──────────────────────────────────────────────────────────────
// 「그래서/따라서」 뒤 한 마디가 우선이다. 수치는 그 자리가 비었을 때만,
// 그것도 문장에 하나뿐일 때만 굵게 한다(아래 수치 주석).
const CONCLUSION = /(?:따라서|그래서|결과적으로)[^.。\n]{2,40}/g;
const NUMBER = /\d[\d,.]*\s?(?:%|원|개월|배|명|개|억|만|조|시간|분|일|주|퍼센트|포인트)|\d[\d,.]*\s?년(?!대)/g;
// 연도는 값이 아니라 날짜다. 「2025년 대졸 초임」에서 굵어야 할 것은 연도가 아니다.
const YEAR = /^(?:19|20)\d{2}\s?년$/;

// 한 말풍선에 강조는 통틀어 둘까지. 화면에 말풍선 서넛이 보이므로 그래야
// 「한 화면에 세 곳」이 지켜진다. 그 이상은 강조가 아니라 배경이 된다.
const MAX_MARKS = 2;

const overlaps = (a, b) => a.start < b.end && b.start < a.end;

/** 한 덩이의 평문에 규칙을 적용한다. */
function markPlain(text, budget) {
  const hits = [];

  // 형광펜 — 대사 전체에 하나. budget 은 호출자(markEmphasis)가 들고 있다.
  if (budget.hilite > 0) {
    outer:
    for (const rule of HILITE) {
      for (const m of text.matchAll(rule.re)) {
        if (m[0].trim().length < MIN_PHRASE) continue;   // 낱말 하나는 안 칠한다
        hits.push({ start: m.index, end: m.index + m[0].length, role: rule.role, hl: true });
        budget.hilite -= 1;
        break outer;
      }
    }
  }

  const push = (m) => {
    if (hits.length >= MAX_MARKS) return false;
    const span = { start: m.index, end: m.index + m[0].length, hl: false };
    if (hits.some((h) => overlaps(h, span))) return false;
    hits.push(span);
    return true;
  };

  // 결론 한 마디.
  for (const m of text.matchAll(CONCLUSION)) { if (push(m)) break; }

  // 수치. 같은 문장에 숫자가 여럿이면 **하나도** 굵게 하지 않는다 —
  // 「하위 10%가 사회 부의 10%」에서 10% 마다 칠하면 문장이 얼룩진다.
  // 그 문장 전체가 중요하면 결론 규칙이 이미 잡았고, 숫자는 그냥 둔다.
  const nums = [...text.matchAll(NUMBER)].filter((m) => !YEAR.test(m[0].trim()));
  if (nums.length === 1) push(nums[0]);

  if (!hits.length) return text;
  hits.sort((a, b) => a.start - b.start);

  let out = '';
  let at = 0;
  for (const h of hits) {
    out += text.slice(at, h.start);
    const body = text.slice(h.start, h.end);
    out += h.hl ? `==${h.role}:${body}==` : `**${body}**`;
    at = h.end;
  }
  return out + text.slice(at);
}

/**
 * 대사 한 줄에 강조 규칙을 적용한다.
 * 저자 마크업이 있는 구간은 그대로 통과시킨다.
 */
export function markEmphasis(text) {
  if (!text) return text;
  const budget = { hilite: 1 };   // 한 말풍선에 형광펜 하나
  return String(text)
    .split(PROTECTED)
    .map((seg, i) => (i % 2 === 1 ? seg : markPlain(seg, budget)))
    .join('');
}
