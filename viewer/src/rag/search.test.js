import test from 'node:test';
import assert from 'node:assert/strict';
import { queryTerms, scoreChunk, searchChunks, withTerms } from './search.js';

const mk = (id, title, text) => ({
  id, path: [title], text,
  terms: [...new Set(
    text.split(/[^0-9A-Za-z가-힣]+/).filter((w) => w.length >= 2)
      .flatMap((w) => [w, ...Array.from({ length: w.length - 1 }, (_, i) => w.slice(i, i + 2))]),
  )],
});

const CHUNKS = [
  mk('a', '한계대체율', '한계대체율은 무차별곡선의 기울기이며 체감한다'),
  mk('b', '구축효과', '구축효과는 정부지출이 민간투자를 밀어내는 현상이다'),
  mk('c', '탄력성', '수요의 가격탄력성은 대체재가 많을수록 커진다'),
];

test('질문에서 두 글자 이상 어절을 뽑는다', () => {
  const t = queryTerms('구축효과가 뭐예요?');
  assert.ok(t.includes('구축효과가'));
  assert.ok(!t.includes('가'));
});

test('겹치는 말이 많을수록 점수가 높다', () => {
  const t = queryTerms('구축효과');
  assert.ok(scoreChunk(CHUNKS[1], t) > scoreChunk(CHUNKS[0], t));
});

test('가장 관련 있는 청크가 맨 앞', () => {
  const hits = searchChunks(CHUNKS, '구축효과가 뭐예요?');
  assert.equal(hits[0].id, 'b');
});

test('limit 을 넘지 않는다', () => {
  assert.equal(searchChunks(CHUNKS, '한계 구축 탄력', 2).length, 2);
});

test('겹치는 말이 없으면 빈손으로 돌려준다 — 지어내지 않게', () => {
  assert.deepEqual(searchChunks(CHUNKS, '점심 메뉴 추천'), []);
});

test('빈 질문은 빈 결과', () => {
  assert.deepEqual(searchChunks(CHUNKS, ''), []);
  assert.deepEqual(searchChunks(null, '구축효과'), []);
});

test('withTerms — terms 가 없는 청크에 채워 넣는다', () => {
  const [c] = withTerms([{ id: 'a', path: ['제3절'], text: '한계대체율은 체감한다' }]);
  assert.ok(Array.isArray(c.terms) && c.terms.length > 0);
  assert.ok(c.terms.includes('한계대체율은'));
  assert.ok(c.terms.includes('제3절'), '제목도 검색어에 들어가야 한다');
});

test('withTerms — 이미 terms 가 있으면 그대로 둔다', () => {
  const src = { id: 'a', path: [], text: 'x', terms: ['미리'] };
  assert.equal(withTerms([src])[0], src);
});
