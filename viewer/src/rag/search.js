// 교재 청크 검색 — 키 없이 동작한다.
//
// 임베딩을 쓰지 않는 이유: 임베딩은 제공자마다 다르고 Anthropic 에는 엔드포인트가
// 없다. 제공자를 바꾸면 인덱스를 다시 만들어야 한다. 어느 제공자든 최소한은
// 동작해야 하므로 어절과 2-gram 으로 점수를 낸다.
//
// 정직하게: 키워드 검색은 임베딩보다 약하다. 「물가가 오르면 실질임금은?」처럼
// 용어가 안 겹치는 질문은 잘 못 찾는다. 못 찾으면 **빈손으로 돌려준다** —
// 엉뚱한 청크를 주느니 튜터가 「교재에서 못 찾았습니다」라고 말하는 편이 낫다.

/** 검색에 쓸 최소 점수. 이보다 낮으면 관계없는 것. */
const MIN_SCORE = 1;

export function queryTerms(q) {
  const words = String(q || '').split(/[^0-9A-Za-z가-힣]+/).filter((w) => w.length >= 2);
  const set = new Set(words);
  for (const w of words) {
    for (let i = 0; i < w.length - 1; i += 1) set.add(w.slice(i, i + 2));
  }
  return [...set];
}

export function scoreChunk(chunk, terms) {
  if (!chunk?.terms?.length || !terms.length) return 0;
  const have = new Set(chunk.terms);
  let score = 0;
  for (const t of terms) {
    if (!have.has(t)) continue;
    // 긴 말이 겹치는 쪽이 값지다. 두 글자 조각 하나는 우연일 수 있다.
    score += t.length >= 3 ? 3 : 1;
  }
  return score;
}

export function searchChunks(chunks, q, limit = 6) {
  if (!Array.isArray(chunks) || !chunks.length) return [];
  const terms = queryTerms(q);
  if (!terms.length) return [];
  return chunks
    .map((c) => ({ ...c, score: scoreChunk(c, terms) }))
    .filter((c) => c.score >= MIN_SCORE)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}

/**
 * 청크에 검색어(terms)를 채워 돌려준다.
 *
 * 파일에는 terms 를 담지 않는다 — 본문에서 그대로 유도되는 값이라 담으면 용량이
 * 두 배가 된다(실측 본문 2.1MB / terms 4.0MB). 대신 로드 직후 한 번 만든다.
 * 규칙의 정본은 scripts/lectures/build_rag_chunks.py 의 terms_of() 다 — 둘이 같아야 한다.
 */
export function withTerms(chunks) {
  return (chunks || []).map((c) => (c.terms ? c : { ...c, terms: queryTerms(`${(c.path || []).join(' ')} ${c.text || ''}`) }));
}
