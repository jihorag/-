// 개념 완성 목차 — AI 학습·드릴·문제풀이와 같은 트리를 쓴다.
//
// buildUnitTree 는 세 탭이 공유하는 '단일 목차' 모델이다(unitTree.js 첫 줄).
// 개념 완성만 이걸 안 쓰고 평면 목록을 그리고 있어서 목차가 어긋나 보였다.
import { useMemo, useState } from 'react';
import { ChevronRight, ChevronDown } from 'lucide-react';
import { buildUnitTree, stripUnitPrefix } from './unitTree';
import { applyScope } from './trackScope';
import { STATE } from './trackProgress';

export default function ConceptOutline({ leaves, scope, index, progress, onPick }) {
  const scoped = useMemo(() => applyScope(leaves || [], scope), [leaves, scope]);
  const { divisions, multiDiv } = useMemo(() => buildUnitTree(scoped), [scoped]);
  const [open, setOpen] = useState({});   // 장 단위 접기/펴기

  const counts = (leafId) => {
    const total = index?.[leafId]?.points || 0;
    const rec = (progress || {})[leafId] || {};
    const vals = Object.values(rec);
    const passed = vals.filter((s) => s >= STATE.PASSED).length;
    const seen = vals.filter((s) => s >= STATE.SEEN).length;
    return { total, passed, seen };
  };

  // 장·절 자체가 학습 단위인 leaf(chapter.leaf, section.leaf) — buildUnitTree 가
  // 이 두 자리에도 leaf 를 놓을 수 있다. UnitOutline.jsx 의 chapterLeaves() 와
  // 같은 패턴으로 전부 모아 관 항목과 같은 모양으로 렌더한다. 안 하면 이 leaf 들이
  // 목차에서 조용히 사라진다(경제학은 전부 관 레벨이라 증상이 안 보였을 뿐).
  const chapterLeaves = (ch) => {
    const out = [];
    if (ch.leaf) out.push(ch.leaf);
    ch.sections.forEach((sec) => {
      if (sec.leaf) out.push(sec.leaf);
      sec.items.forEach((it) => out.push(it.leaf));
    });
    return out;
  };

  return (
    <div>
      {divisions.map((div) => (
        <section key={div.name} style={{ marginBottom: 18 }}>
          {multiDiv && (
            <h3 className="concept-out-div">{div.name}</h3>
          )}
          {div.chapters.map((ch) => {
            const key = div.name + '/' + ch.name;
            const isOpen = open[key] !== false;   // 기본은 펼침
            const chTotals = chapterLeaves(ch).reduce((acc, leaf) => {
              const c = counts(leaf.id);
              return { total: acc.total + c.total, passed: acc.passed + c.passed, seen: acc.seen + c.seen };
            }, { total: 0, passed: 0, seen: 0 });
            return (
              <div key={key} style={{ marginBottom: 10 }}>
                <button type="button" className="concept-out-ch"
                  aria-expanded={isOpen}
                  onClick={() => setOpen((o) => ({ ...o, [key]: !isOpen }))}>
                  {isOpen ? <ChevronDown size={14} strokeWidth={1.75} /> : <ChevronRight size={14} strokeWidth={1.75} />}
                  <span className="concept-out-hier">{ch.hier}</span>
                  <span className="concept-out-name">{stripUnitPrefix(ch.name)}</span>
                  {chTotals.total > 0 && (
                    <span className="concept-out-count">{chTotals.passed} / {chTotals.total}</span>
                  )}
                </button>

                {isOpen && (
                  <div style={{ marginLeft: 18, marginTop: 4 }}>
                    {ch.leaf && (
                      <ItemButton leaf={ch.leaf} name={ch.name} c={counts(ch.leaf.id)} onPick={onPick} />
                    )}
                    {ch.sections.map((sec) => (
                      <div key={sec.name}>
                        {sec.leaf
                          ? <ItemButton leaf={sec.leaf} name={sec.name} c={counts(sec.leaf.id)} onPick={onPick} />
                          : (
                            <div className="concept-out-sec">{stripUnitPrefix(sec.name)}</div>
                          )}
                        {sec.items.map((it) => (
                          <ItemButton key={it.leaf.id} leaf={it.leaf} name={it.name}
                            c={counts(it.leaf.id)} onPick={onPick} />
                        ))}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </section>
      ))}
    </div>
  );
}

function ItemButton({ leaf, name, c, onPick }) {
  const empty = c.total === 0;
  return (
    <button type="button" className="concept-out-item" disabled={empty}
      onClick={() => !empty && onPick(leaf.id)}>
      <span className="concept-out-name">{stripUnitPrefix(name)}</span>
      {/* 관 안의 세그먼트 진행바와 같은 표현. 목차에는 논점 순서를 모르므로
          통과·열어봄·미학습 개수만큼 칸을 채운다. */}
      {!empty && <Segments total={c.total} passed={c.passed} seen={c.seen} />}
      <span className="concept-out-count">
        {empty ? '준비 중' : `${c.passed} / ${c.total}`}
      </span>
    </button>
  );
}

function Segments({ total, passed, seen }) {
  return (
    <span className="concept-segs concept-segs--mini" aria-hidden="true">
      {Array.from({ length: total }, (_, i) => (
        <span key={i}
          className={`concept-seg${i < passed ? ' is-passed' : i < seen ? ' is-seen' : ''}`} />
      ))}
    </span>
  );
}
