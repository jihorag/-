// 민법 교재(.md) → 목차 트리(civil_total.json) + 자동 cloze 카드(civil_cards.json) 빌드
//
// 입력: 사용자의 김묘엽 「위패스 마이」 정리 .md
//   1순위: $HOME/Documents/Claude KAPA CHATING/1차 - 민법_학습자료/{민법총칙,물권법}_정리.md
//   2순위: repoRoot/8_civil/{...}.md (복사본)
//
// 출력: viewer/public/data/civil/civil_total.json, civil_cards.json
//
// 카드 종류(자동 cloze):
//   T1. statute     — 인용된 조문 본문(`> **제N조 (제목)** 본문`) 양방향 카드
//   T2. definition  — 정의문(`X이란 Y을 말한다`) 양방향
//   T3. bold        — 본문 안 `**용어**` 빈칸
//   T4. mnemonic    — 점·중점으로 연결된 두문자(3토큰 이상)
//
// 큐레이팅 카드(OX/단답/사례)는 별도 civil_curated.json로, 본 스크립트는 자동 생성만 담당.

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { createHash } from 'node:crypto';
import { homedir } from 'node:os';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(here, '..', '..');
const destDir = join(here, '..', 'public', 'data', 'civil');

const SOURCES = [
  { id: 'chongchik', title: '민법총칙', files: ['민법총칙_정리.md', '민법총칙_목차.md'] },
  { id: 'mulgwon',   title: '물권법',   files: ['물권법_정리.md',   '물권법_목차.md'] },
];

const SOURCE_DIRS = [
  join(homedir(), 'Documents', 'Claude KAPA CHATING', '1차 - 민법_학습자료'),
  join(repoRoot, '8_civil'),
];

function findSource(filename) {
  for (const dir of SOURCE_DIRS) {
    const p = join(dir, filename);
    if (existsSync(p)) return p;
  }
  return null;
}

function shortId(s) {
  return createHash('sha1').update(s).digest('hex').slice(0, 10);
}

// ─── md → 트리 ───────────────────────────────────────────────
// 헤딩(##/###/####) 기준으로 노드 분해. 본문이 헤딩 같은 줄에 붙어있으면 분리.
function parseTree(md, bookId, bookTitle) {
  const lines = md.split('\n');
  const root = { id: bookId, title: bookTitle, level: 0, children: [], body: [] };
  const stack = [root];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const m = /^(#{2,4})\s+(.+)$/.exec(line);
    if (m) {
      const level = m[1].length;       // 2|3|4
      let header = m[2].trim();
      // 헤딩 뒤에 본문이 붙어 있는 케이스: 첫 번호/괄호 이전을 헤딩으로 자르고 나머지는 본문
      // 예: "II. 국가나 법질서의 개입 필요성 개인의 자유와…"
      // 단순화: 헤딩이 너무 길고(약 40자+) 마침표·읽는 패턴이 있으면 두 토큰만 헤더로
      let trailing = '';
      if (header.length > 40) {
        // 첫 문장이 끝나는 지점 또는 '~이다' 직전까지를 헤더로 잘라봄
        const idx = header.search(/(?<=[가-힣])\s(?=[가-힣])(?=.*[다요음함]\b)/);
        if (idx > 8 && idx < 30) {
          trailing = header.slice(idx + 1).trim();
          header = header.slice(0, idx).trim();
        }
      }
      // 스택에서 level 이상은 pop
      while (stack.length > 1 && stack[stack.length - 1].level >= level) stack.pop();
      const node = { id: shortId(`${bookId}/${header}/${i}`), title: header, level, line: i + 1, children: [], body: [] };
      stack[stack.length - 1].children.push(node);
      stack.push(node);
      if (trailing) node.body.push(trailing);
      continue;
    }
    const txt = line.trim();
    if (!txt) continue;
    stack[stack.length - 1].body.push(line);
  }
  return root;
}

// ─── 본문 정규화 ─────────────────────────────────────────────
// OCR 결과 줄바꿈을 문장 단위로 합치고, 각주 번호 노이즈를 줄임.
function joinParagraphs(bodyLines) {
  if (!bodyLines || !bodyLines.length) return [];
  // 1) blockquote(`> ...`)는 별도 단락으로
  // 2) 빈줄로 단락 분할, 줄바꿈은 공백으로 합쳐 한 단락 한 문자열
  const paras = [];
  let buf = [];
  let quoteBuf = [];
  const flushBuf = () => {
    if (buf.length) {
      const joined = buf.join(' ').replace(/\s+/g, ' ').trim();
      if (joined) paras.push({ kind: 'p', text: joined });
      buf = [];
    }
  };
  const flushQuote = () => {
    if (quoteBuf.length) {
      const joined = quoteBuf.join(' ').replace(/\s+/g, ' ').trim();
      if (joined) paras.push({ kind: 'quote', text: joined });
      quoteBuf = [];
    }
  };
  for (const raw of bodyLines) {
    const line = raw.replace(/\t/g, ' ');
    if (!line.trim()) { flushBuf(); flushQuote(); continue; }
    if (/^\s*>\s*/.test(line)) {
      flushBuf();
      quoteBuf.push(line.replace(/^\s*>\s*/, ''));
    } else {
      flushQuote();
      buf.push(line);
    }
  }
  flushBuf(); flushQuote();
  return paras;
}

// ─── 카드 생성기 ─────────────────────────────────────────────
const cards = []; // {id, type, chapterPath, q, a, hint?}

function pushCard(c) {
  if (!c.q || !c.a) return;
  if (c.q.length < 4 || c.a.length < 1) return;
  const id = shortId(`${c.type}|${c.q}|${c.a}`);
  cards.push({ id, ...c });
}

// T1: 인용 조문 카드. `**제N조 (제목)**` 헤더 + 본문 → 양방향 두 장
const STATUTE_HEAD = /\*\*\s*제\s*(\d+(?:조의\d+)?)\s*조\s*(?:\(([^)]*)\))?\s*\*\*/;

function buildStatuteCards(quote, path) {
  const m = STATUTE_HEAD.exec(quote);
  if (!m) return;
  const num = m[1].replace(/\s+/g, '');
  const label = (m[2] || '').trim();
  const body = quote.slice(m.index + m[0].length).trim().replace(/^[:;：。·,\.]\s*/, '');
  if (body.length < 6) return;
  // A) 조문 → 본문
  pushCard({
    type: 'statute',
    direction: 'num2body',
    chapterPath: path,
    q: `**제${num}조** ${label ? `(${label})` : ''}\n\n___`,
    a: body,
  });
  // B) 본문 → 조문번호+제목 (마스크된 핵심구만 노출)
  const masked = body.length > 80 ? body.slice(0, 80) + '…' : body;
  pushCard({
    type: 'statute',
    direction: 'body2num',
    chapterPath: path,
    q: `다음은 어느 조문인가?\n\n"${masked}"`,
    a: `제${num}조${label ? ` (${label})` : ''}`,
  });
}

// T2: 정의문. "X이란 Y을 말한다."
const DEF_RE = /([가-힣A-Za-z·•\s]{2,40}?)(?:이란|란)\s+(.+?)\s*(?:을|를)\s*말한다\.?/g;

function buildDefinitionCards(para, path) {
  let m;
  DEF_RE.lastIndex = 0;
  while ((m = DEF_RE.exec(para)) !== null) {
    const term = m[1].trim().replace(/^[(,\.\s]+|[(,\.\s]+$/g, '');
    const def  = m[2].trim();
    if (term.length < 2 || term.length > 30 || def.length < 4 || def.length > 200) continue;
    // 용어 → 정의
    pushCard({
      type: 'definition',
      direction: 'term2def',
      chapterPath: path,
      q: `**${term}**\n\n→ ?`,
      a: `${def}을(를) 말한다.`,
    });
    // 정의 → 용어
    pushCard({
      type: 'definition',
      direction: 'def2term',
      chapterPath: path,
      q: `___ 이란\n\n${def}을(를) 말한다.`,
      a: term,
    });
  }
}

// T3: 본문 bold 빈칸 (조문 헤드는 제외)
const BOLD_RE = /\*\*([^*\n]{1,40})\*\*/g;
const SENTENCE_SPLIT = /(?<=[다요음함\?\!\.])\s+/;

function buildBoldCards(para, path) {
  // 조문 헤더 패턴이면 스킵(T1이 다룸)
  if (STATUTE_HEAD.test(para)) return;
  // 문장 단위로 분리해서, bold 포함 문장만 카드화
  const sentences = para.split(SENTENCE_SPLIT);
  for (const sent of sentences) {
    const bolds = [...sent.matchAll(BOLD_RE)];
    if (!bolds.length) continue;
    for (const b of bolds) {
      const term = b[1].trim();
      if (!term || term.length < 2 || term.length > 30) continue;
      if (/^\d+$/.test(term)) continue; // 단순 숫자만은 노이즈
      const cleaned = sent.replace(BOLD_RE, (mm, inner) => (inner === term ? '___' : inner)).trim();
      if (cleaned.length < 8) continue;
      pushCard({
        type: 'bold',
        chapterPath: path,
        q: cleaned,
        a: term,
      });
    }
  }
}

// T4: 진짜 두문자(1글자 토큰 4개 이상) — "불·상·대·유·유·인" 같은 시험 두문자만 채택.
// "농업·임업·어업" 류 단순 열거는 제외하기 위해 토큰 길이=1로 한정.
const MNEMONIC_RE = /([가-힣](?:\s*[·•・∙]\s*[가-힣]){3,})/g;

function buildMnemonicCards(para, path) {
  MNEMONIC_RE.lastIndex = 0;
  let m;
  const seen = new Set();
  while ((m = MNEMONIC_RE.exec(para)) !== null) {
    const phrase = m[1].replace(/\s+/g, '');
    if (seen.has(phrase)) continue;
    seen.add(phrase);
    const tokens = phrase.split(/[·•・∙]/).filter(Boolean);
    if (tokens.length < 4 || tokens.length > 12) continue;
    if (tokens.some(t => t.length !== 1)) continue;
    // 카드: 토큰 수와 첫 글자 힌트만 노출
    const hint = tokens.map(t => t[0] + '_'.repeat(Math.max(0, t.length - 1))).join('·');
    pushCard({
      type: 'mnemonic',
      chapterPath: path,
      q: `다음을 떠올려 보세요 (${tokens.length}개):\n\n${hint}\n\n_힌트: 본 단락 핵심 두문자_`,
      a: phrase,
    });
  }
}

// ─── 노드를 순회하며 카드 생성 ───────────────────────────────
function walkAndBuild(node, ancestry, bookTitle) {
  const path = ancestry.concat([{ id: node.id, title: node.title, level: node.level }]);
  const paras = joinParagraphs(node.body);
  node.paragraphs = paras;
  // 카드 생성은 leaf 또는 본문 있는 노드에 한해
  for (const p of paras) {
    if (p.kind === 'quote') buildStatuteCards(p.text, path);
    else {
      buildDefinitionCards(p.text, path);
      buildBoldCards(p.text, path);
      buildMnemonicCards(p.text, path);
    }
  }
  for (const c of node.children) walkAndBuild(c, path, bookTitle);
}

// ─── 메인 ────────────────────────────────────────────────────
function run() {
  mkdirSync(destDir, { recursive: true });
  const total = { books: [], built_at: new Date().toISOString() };
  const cardsByBook = {};

  for (const src of SOURCES) {
    const bodyPath = findSource(src.files[0]);
    if (!bodyPath) {
      console.warn(`[build_civil] source missing: ${src.files[0]} — skip ${src.title}`);
      continue;
    }
    const md = readFileSync(bodyPath, 'utf8');
    const tree = parseTree(md, src.id, src.title);
    const beforeCards = cards.length;
    walkAndBuild(tree, [], src.title);
    const made = cards.length - beforeCards;
    // 책 카드는 cards 전역에 누적된 후 책별로 마킹할 수도 있지만 chapterPath에 책 노드가 들어있어 분리 가능
    cardsByBook[src.id] = made;
    total.books.push({
      id: src.id,
      title: src.title,
      source: bodyPath,
      tree,
    });
    console.log(`[build_civil] ${src.title}: ${made} cards, ${tree.children.length} top chapters`);
  }

  // 카드에 book id 부착(첫 ancestor가 책)
  for (const c of cards) {
    c.bookId = c.chapterPath?.[0]?.id || 'unknown';
    // chapterPath는 너무 무거우므로 leaf 이름만 보관, 전체 path는 별도로
    c.chapterTitle = c.chapterPath.map(n => n.title).join(' > ');
    c.leafId = c.chapterPath[c.chapterPath.length - 1].id;
    delete c.chapterPath;
  }

  writeFileSync(join(destDir, 'civil_total.json'), JSON.stringify(total));
  writeFileSync(join(destDir, 'civil_cards.json'), JSON.stringify({ built_at: total.built_at, count: cards.length, cards }));

  const sizeKB = (s) => (s.length / 1024).toFixed(1);
  const totalSize = sizeKB(JSON.stringify(total));
  const cardSize  = sizeKB(JSON.stringify(cards));
  console.log(`[build_civil] wrote civil_total.json (${totalSize} KB), civil_cards.json (${cardSize} KB, ${cards.length} cards)`);
}

run();
