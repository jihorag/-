// 학습 단원 트리 + 서수 — AI학습·드릴·문제풀이 세 탭이 공유하는 '단일 목차' 모델.
// 입력: leavesBySubject[sid] (한 과목의 leaf 배열). 배열 순서 = 커리큘럼(학습) 순서.
// 산출: 세부과목(division) → 장(chapter) → 절(section) → 관(item) 트리 +
//       각 leaf의 서수 { seq, total, hier } — seq/total = 과목 내 통합순번, hier = 계층 서수("1장·2절").

// 이름 문자열 안의 서수를 레벨에 맞게만 뽑는다(절 자리에서 '장'을 잘못 집지 않도록).
function levelLabel(name = '', pos, level) {
  const want = { ch: ['장', '편'], sec: ['절'], it: ['관'] }[level];
  let m;
  if ((m = name.match(/제?\s*(\d+)\s*(장|절|관|편|강)/)) && want.includes(m[2])) return `${+m[1]}${m[2]}`;
  if (level === 'ch') {
    if ((m = name.match(/PART\s*0*(\d+)/i))) return `${+m[1]}편`;
    if ((m = name.match(/Chapter\s*0*(\d+)/i))) return `${+m[1]}장`;
  }
  const defWord = { ch: '장', sec: '절', it: '관' }[level];
  return `${pos}${defWord}`;
}

// 표시용 이름 — 앞의 교재 서수 접두어를 떼어 배지와 중복되지 않게 한다.
export function stripUnitPrefix(name = '') {
  const out = name.replace(/^(?:제?\s*\d+\s*(?:장|절|관|편|강)|PART\s*0*\d+|Chapter\s*0*\d+)\s*[·.:]?\s*/i, '').trim();
  return out || name;
}

const setHier = (map, id, hier) => { const o = map.get(id); if (o) o.hier = hier; };

/**
 * @param {Array} leaves  한 과목의 leaf 배열(커리큘럼 순서)
 * @returns {{divisions:Array, ordinalById:Map, total:number, multiDiv:boolean}}
 */
export function buildUnitTree(leaves = []) {
  const divisions = [];
  const divMap = new Map();
  const ordinalById = new Map();
  const total = leaves.length;

  leaves.forEach((l, i) => {
    if (!l) return;
    const path = Array.isArray(l.path) && l.path.length ? l.path : [l.title || l.id || ''];
    const [dName, cName, sName, iName] = path;
    ordinalById.set(l.id, { seq: i + 1, total, hier: '' });

    let div = divMap.get(dName);
    if (!div) { div = { name: dName, chapters: [], _chMap: new Map() }; divMap.set(dName, div); divisions.push(div); }

    if (cName == null) return; // division 레벨 leaf(희귀) — 통합순번만

    let ch = div._chMap.get(cName);
    if (!ch) { ch = { name: cName, no: div.chapters.length + 1, hier: '', leaf: null, sections: [], _secMap: new Map() }; div._chMap.set(cName, ch); div.chapters.push(ch); ch.hier = levelLabel(cName, ch.no, 'ch'); }

    if (sName == null) { ch.leaf = l; setHier(ordinalById, l.id, ch.hier); return; }

    let sec = ch._secMap.get(sName);
    if (!sec) { sec = { name: sName, no: ch.sections.length + 1, hier: '', leaf: null, items: [] }; ch._secMap.set(sName, sec); ch.sections.push(sec); sec.hier = `${ch.hier}·${levelLabel(sName, sec.no, 'sec')}`; }

    if (iName == null) { sec.leaf = l; setHier(ordinalById, l.id, sec.hier); return; }

    const it = { name: iName, no: sec.items.length + 1, hier: `${sec.hier}·${levelLabel(iName, sec.items.length + 1, 'it')}`, leaf: l };
    sec.items.push(it);
    setHier(ordinalById, l.id, it.hier);
  });

  // 내부 Map은 노출하지 않는다(렌더는 배열만 사용)
  divisions.forEach((d) => { delete d._chMap; d.chapters.forEach((c) => { delete c._secMap; }); });
  return { divisions, ordinalById, total, multiDiv: divisions.length > 1 };
}

// 계획용 '장(章) 단원 풀' — 학습 계획이 이 순서·서수로 하루치를 배분한다.
// 각 항목: { name, div(세부과목), chap(장 이름), hier('3장'·'1편'), level('장'·'편'),
//           secCount, itemCount, sub('절 3 · 관 8' = 이 장의 분량) }. 커리큘럼(학습) 순서 유지.
export function subjectChapterPool(leaves = []) {
  const { divisions, multiDiv } = buildUnitTree(leaves);
  const out = [];
  divisions.forEach((div) => div.chapters.forEach((ch) => {
    const secCount = ch.sections.length;
    const itemCount = ch.sections.reduce((n, s) => n + s.items.length, 0);
    const level = (ch.hier || '').replace(/[0-9]/g, '') || '장';
    const sub = secCount ? (itemCount ? `절 ${secCount} · 관 ${itemCount}` : `절 ${secCount}`) : null;
    out.push({
      name: (multiDiv ? `${div.name} · ` : '') + stripUnitPrefix(ch.name),
      div: multiDiv ? div.name : '', chap: stripUnitPrefix(ch.name),
      hier: ch.hier, level, secCount, itemCount, sub,
    });
  }));
  return out;
}
