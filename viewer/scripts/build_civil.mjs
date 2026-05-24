// 통암기 카드 빌더 — 다과목 .md → 목차 트리(total.json) + 자동 cloze 카드(cards.json)
//
// 지원 과목 (SUBJECTS_BUILD):
//   civil       — 민법 (총칙·물권법)
//   accounting  — 회계학 (재무·원가)
//   realestate  — 부동산학원론 (국승옥)
//
// 카드 종류(자동 cloze):
//   T1. statute     — 인용된 조문 본문(`> **제N조 (제목)** 본문`) 양방향
//   T2. definition  — 정의문(`X이란 Y을 말한다`) 양방향
//   T3. bold        — 본문 안 `**용어**` 빈칸
//   T4. mnemonic    — 점·중점으로 연결된 두문자(1글자 토큰 4개+)
//
// 소스 .md가 모두 없으면 — git에 커밋된 기존 JSON을 보존하고 종료
// (Vercel 빌드 환경엔 사용자 `~/Documents/...` 폴더가 없음. 기존 JSON 유지 안전망.)

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { createHash } from 'node:crypto';
import { homedir } from 'node:os';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(here, '..', '..');
const HOME = homedir();

// ─── 다과목 빌드 메타 ────────────────────────────────────
const SUBJECTS_BUILD = [
  {
    id: 'civil',
    title: '민법',
    outDir: join(here, '..', 'public', 'data', 'civil'),
    outFiles: { total: 'civil_total.json', cards: 'civil_cards.json' },
    books: [
      { id: 'chongchik', title: '민법총칙', file: '민법총칙_정리.md' },
      { id: 'mulgwon', title: '물권법', file: '물권법_정리.md' },
    ],
    sourceDirs: [
      join(HOME, 'Documents', 'Claude KAPA CHATING', '1차 - 민법_학습자료'),
      join(repoRoot, '8_civil'),
    ],
  },
  {
    id: 'accounting',
    title: '회계학',
    outDir: join(here, '..', 'public', 'data', 'accounting'),
    outFiles: { total: 'total.json', cards: 'cards.json' },
    books: [
      { id: 'cpa-financial', title: '재무회계', file: '황윤하_재무회계.md' },
      { id: 'cpa-cost', title: '원가회계', file: '황윤하_원가회계.md' },
    ],
    sourceDirs: [
      join(HOME, 'Documents', 'Claude KAPA CHATING', '1차 - 회계학_학습자료'),
      join(repoRoot, '8_accounting'),
    ],
  },
  {
    id: 'realestate',
    title: '부동산학원론',
    outDir: join(here, '..', 'public', 'data', 'realestate'),
    outFiles: { total: 'total.json', cards: 'cards.json' },
    books: [
      { id: 'gook', title: '국승옥 강의노트', file: '국승옥_강의노트.md' },
    ],
    sourceDirs: [
      join(HOME, 'Documents', 'Claude KAPA CHATING', '1차 - 부동산학원론_학습자료'),
      join(repoRoot, '8_realestate'),
    ],
  },
];

function findInDirs(dirs, filename) {
  for (const d of dirs) {
    const p = join(d, filename);
    if (existsSync(p)) return p;
  }
  return null;
}

function shortId(s) { return createHash('sha1').update(s).digest('hex').slice(0, 10); }

// ─── md → 트리 ───────────────────────────────────────────
function parseTree(md, bookId, bookTitle) {
  const lines = md.split('\n');
  const root = { id: bookId, title: bookTitle, level: 0, children: [], body: [] };
  const stack = [root];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const m = /^(#{2,4})\s+(.+)$/.exec(line);
    if (m) {
      const level = m[1].length;
      let header = m[2].trim();
      let trailing = '';
      if (header.length > 40) {
        const idx = header.search(/(?<=[가-힣])\s(?=[가-힣])(?=.*[다요음함]\b)/);
        if (idx > 8 && idx < 30) {
          trailing = header.slice(idx + 1).trim();
          header = header.slice(0, idx).trim();
        }
      }
      while (stack.length > 1 && stack[stack.length - 1].level >= level) stack.pop();
      const node = { id: shortId(`${bookId}/${header}/${i}`), title: header, level, line: i + 1, children: [], body: [] };
      stack[stack.length - 1].children.push(node);
      stack.push(node);
      if (trailing) node.body.push(trailing);
      continue;
    }
    stack[stack.length - 1].body.push(line);
  }
  return root;
}

function joinParagraphs(bodyLines) {
  if (!bodyLines || !bodyLines.length) return [];
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

// ─── 카드 생성 — subject 단위로 누적 ──────────────────────
function makeCardBuilder(subjectId) {
  const cards = [];
  const push = (c) => {
    if (!c.q || !c.a) return;
    if (c.q.length < 4 || c.a.length < 1) return;
    const id = shortId(`${subjectId}|${c.type}|${c.q}|${c.a}`);
    cards.push({ id, ...c });
  };

  const STATUTE_HEAD = /\*\*\s*제\s*(\d+(?:조의\d+)?)\s*조\s*(?:\(([^)]*)\))?\s*\*\*/;
  const DEF_RE = /([가-힣A-Za-z·•\s]{2,40}?)(?:이란|란)\s+(.+?)\s*(?:을|를)\s*말한다\.?/g;
  const BOLD_RE = /\*\*([^*\n]{1,40})\*\*/g;
  const SENTENCE_SPLIT = /(?<=[다요음함\?\!\.])\s+/;
  const MNEMONIC_RE = /([가-힣](?:\s*[·•・∙]\s*[가-힣]){3,})/g;

  function buildStatute(quote, path) {
    const m = STATUTE_HEAD.exec(quote);
    if (!m) return;
    const num = m[1].replace(/\s+/g, '');
    const label = (m[2] || '').trim();
    const body = quote.slice(m.index + m[0].length).trim().replace(/^[:;:。·,\.]\s*/, '');
    if (body.length < 6) return;
    push({ type: 'statute', direction: 'num2body', chapterPath: path,
      q: `**제${num}조** ${label ? `(${label})` : ''}\n\n___`, a: body });
    const masked = body.length > 80 ? body.slice(0, 80) + '…' : body;
    push({ type: 'statute', direction: 'body2num', chapterPath: path,
      q: `다음은 어느 조문인가?\n\n"${masked}"`,
      a: `제${num}조${label ? ` (${label})` : ''}` });
  }
  function buildDef(para, path) {
    DEF_RE.lastIndex = 0; let m;
    while ((m = DEF_RE.exec(para)) !== null) {
      let term = m[1].trim().replace(/^[(,\.\s]+|[(,\.\s]+$/g, '');
      const half = Math.floor(term.length / 2);
      const halfStr = term.slice(0, half).trim();
      if (halfStr && halfStr.length >= 2 && term.endsWith(halfStr)) term = halfStr;
      term = term.replace(/^(?:\([가-힣]\)|\d+\.|[가-힣]\.)\s*/, '').trim();
      const def = m[2].trim();
      if (term.length < 2 || term.length > 30 || def.length < 4 || def.length > 200) continue;
      push({ type: 'definition', direction: 'term2def', chapterPath: path,
        q: `**${term}**\n\n→ ?`, a: `${def}을(를) 말한다.` });
      push({ type: 'definition', direction: 'def2term', chapterPath: path,
        q: `___ 이란\n\n${def}을(를) 말한다.`, a: term });
    }
  }
  function buildBold(para, path) {
    if (STATUTE_HEAD.test(para)) return;
    const sentences = para.split(SENTENCE_SPLIT);
    for (const sent of sentences) {
      const bolds = [...sent.matchAll(BOLD_RE)];
      if (!bolds.length) continue;
      for (const b of bolds) {
        const term = b[1].trim();
        if (!term || term.length < 2 || term.length > 30) continue;
        if (/^\d+$/.test(term)) continue;
        const cleaned = sent.replace(BOLD_RE, (mm, inner) => (inner === term ? '___' : inner)).trim();
        if (cleaned.length < 8) continue;
        push({ type: 'bold', chapterPath: path, q: cleaned, a: term });
      }
    }
  }
  function buildMnemonic(para, path) {
    MNEMONIC_RE.lastIndex = 0; let m;
    const seen = new Set();
    while ((m = MNEMONIC_RE.exec(para)) !== null) {
      const phrase = m[1].replace(/\s+/g, '');
      if (seen.has(phrase)) continue;
      seen.add(phrase);
      const tokens = phrase.split(/[·•・∙]/).filter(Boolean);
      if (tokens.length < 4 || tokens.length > 12) continue;
      if (tokens.some(t => t.length !== 1)) continue;
      const hint = tokens.map(t => t[0] + '_'.repeat(Math.max(0, t.length - 1))).join('·');
      push({ type: 'mnemonic', chapterPath: path,
        q: `다음을 떠올려 보세요 (${tokens.length}개):\n\n${hint}\n\n_힌트: 본 단락 핵심 두문자_`,
        a: phrase });
    }
  }

  function walk(node, ancestry) {
    const path = ancestry.concat([{ id: node.id, title: node.title, level: node.level }]);
    const paras = joinParagraphs(node.body);
    node.paragraphs = paras;
    for (const p of paras) {
      if (p.kind === 'quote') buildStatute(p.text, path);
      else {
        buildDef(p.text, path);
        buildBold(p.text, path);
        buildMnemonic(p.text, path);
      }
    }
    for (const c of node.children) walk(c, path);
  }

  return { cards, walk };
}

// ─── 메인 ────────────────────────────────────────────────
function runSubject(sub) {
  const anySource = sub.books.some(b => findInDirs(sub.sourceDirs, b.file));
  if (!anySource) {
    console.log(`[build_memorize] ${sub.id}: no source .md — keep existing as-is`);
    return { id: sub.id, status: 'skipped' };
  }

  mkdirSync(sub.outDir, { recursive: true });
  const total = { books: [], built_at: new Date().toISOString() };
  const builder = makeCardBuilder(sub.id);

  for (const book of sub.books) {
    const path = findInDirs(sub.sourceDirs, book.file);
    if (!path) {
      console.warn(`[build_memorize] ${sub.id}: source missing ${book.file} — skip ${book.title}`);
      continue;
    }
    const md = readFileSync(path, 'utf8');
    const tree = parseTree(md, book.id, book.title);
    const beforeCards = builder.cards.length;
    builder.walk(tree, []);
    const made = builder.cards.length - beforeCards;
    total.books.push({ id: book.id, title: book.title, source: path, tree });
    console.log(`[build_memorize] ${sub.id}/${book.title}: ${made} cards, ${tree.children.length} top chapters`);
  }

  for (const c of builder.cards) {
    c.bookId = c.chapterPath?.[0]?.id || 'unknown';
    c.chapterTitle = c.chapterPath.map(n => n.title).join(' > ');
    c.leafId = c.chapterPath[c.chapterPath.length - 1].id;
    delete c.chapterPath;
  }

  writeFileSync(join(sub.outDir, sub.outFiles.total), JSON.stringify(total));
  writeFileSync(join(sub.outDir, sub.outFiles.cards),
    JSON.stringify({ built_at: total.built_at, count: builder.cards.length, cards: builder.cards }));

  const sizeKB = (s) => (s.length / 1024).toFixed(1);
  console.log(`[build_memorize] ${sub.id}: wrote ${sub.outFiles.total} (${sizeKB(JSON.stringify(total))} KB), ${sub.outFiles.cards} (${sizeKB(JSON.stringify(builder.cards))} KB, ${builder.cards.length} cards)`);
  return { id: sub.id, status: 'built', cards: builder.cards.length };
}

function run() {
  console.log(`[build_memorize] start — subjects: ${SUBJECTS_BUILD.map(s => s.id).join(', ')}`);
  for (const sub of SUBJECTS_BUILD) {
    runSubject(sub);
  }
  console.log(`[build_memorize] done`);
}

run();
