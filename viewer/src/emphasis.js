// 형광펜 규칙 — 색 하나에 뜻 하나.
//
// 색을 늘리면 화면이 알록달록해지는 게 아니라 「이 색이 그어졌다 = 이런 자리다」가
// 읽히도록, 네 가지 역할만 둔다. 규칙은 여기 한 곳에만 있다.
//
//   이름(노랑)   정의되는 용어. 따옴표로 묶인 말.        → 외울 것
//   뒤집힘(분홍) 「~가 아니라」·「반대로」·「달리」        → 시험이 뒤집는 자리
//   수치(초록)   숫자와 단위.                            → 조건이 걸리는 값
//   결론(파랑)   「따라서」·「결과적으로」 뒤의 한 마디    → 그래서 어떻게 되는가
//
// 데이터에 손대지 않고 렌더할 때 적용한다. 878개 논점을 다시 쓰는 대신 규칙이
// 모든 대사에 똑같이 적용되므로, 「이 논점만 형광펜이 없다」가 생기지 않는다.
//
// 이미 저자가 손으로 넣은 마크업(**굵게**, ==형광펜==, $수식$)은 건드리지 않는다.

export const ROLES = ['이름', '뒤집힘', '수치', '결론'];

// 저자 마크업 · 수식 구간은 규칙을 적용하지 않는다.
const PROTECTED = /(\*\*[^*]+\*\*|==(?:(?!==)[\s\S])+==|\$[^$]*\$|\[IMAGE:[^\]]*\])/g;

// 역할별 규칙. 순서가 곧 우선순위 — 먼저 그은 자리에는 다시 긋지 않는다.
const RULES = [
  {
    role: '뒤집힘',
    max: 2,
    // 「A가 아니라」·「~와 달리」 같은 대비 표지. 뒤집어 내는 선지가 사는 자리.
    re: /[^\s,.]{1,14}(?:이|가)\s*아니라|[^\s,.]{1,14}(?:와|과)\s*달리|반대로|거꾸로|헷갈리기\s*쉽|착각하기\s*쉽/g,
  },
  {
    role: '이름',
    max: 2,
    // 따옴표로 묶인 용어. 데이터가 정의어를 이 형태로 쓴다.
    re: /'[^'\n]{2,24}'/g,
  },
  {
    role: '수치',
    max: 3,
    re: /\d[\d,.]*\s?(?:%|원|년|개월|배|명|개|억|만|조|시간|분|일|주|퍼센트|포인트)/g,
  },
  {
    role: '결론',
    max: 1,
    // 접속어 하나만 칠하면 뜻이 없다. 그 뒤 한 마디까지 함께 칠한다.
    re: /(?:따라서|그래서|결과적으로)[^.。\n]{2,40}/g,
  },
];

const overlaps = (a, b) => a.start < b.end && b.start < a.end;

/** 한 덩이의 평문에 규칙을 적용해 `==역할:본문==` 마크업을 심는다. */
function markPlain(text) {
  const hits = [];
  for (const rule of RULES) {
    let n = 0;
    for (const m of text.matchAll(rule.re)) {
      if (n >= rule.max) break;
      const span = { start: m.index, end: m.index + m[0].length, role: rule.role };
      if (hits.some((h) => overlaps(h, span))) continue;
      hits.push(span);
      n += 1;
    }
  }
  if (!hits.length) return text;
  hits.sort((a, b) => a.start - b.start);

  let out = '';
  let at = 0;
  for (const h of hits) {
    out += text.slice(at, h.start);
    out += `==${h.role}:${text.slice(h.start, h.end)}==`;
    at = h.end;
  }
  return out + text.slice(at);
}

/**
 * 대사 한 줄에 형광펜 규칙을 적용한다.
 * 저자 마크업이 있는 구간은 그대로 통과시킨다.
 */
export function markEmphasis(text) {
  if (!text) return text;
  return String(text)
    .split(PROTECTED)
    .map((seg, i) => (i % 2 === 1 ? seg : markPlain(seg)))
    .join('');
}
