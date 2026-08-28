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
    const passed = Object.values(rec).filter((s) => s >= STATE.PASSED).length;
    return { total, passed };
  };

  return (
    <div>
      {divisions.map((div) => (
        <section key={div.name} style={{ marginBottom: 18 }}>
          {multiDiv && (
            <h3 style={{ fontSize: '0.82rem', color: '#6b7280', fontWeight: 700, margin: '0 0 8px' }}>
              {div.name}
            </h3>
          )}
          {div.chapters.map((ch) => {
            const key = div.name + '/' + ch.name;
            const isOpen = open[key] !== false;   // 기본은 펼침
            const chTotals = ch.sections.flatMap((s) => s.items).reduce((acc, it) => {
              const c = counts(it.leaf.id);
              return { total: acc.total + c.total, passed: acc.passed + c.passed };
            }, { total: 0, passed: 0 });
            return (
              <div key={key} style={{ marginBottom: 10 }}>
                <button onClick={() => setOpen((o) => ({ ...o, [key]: !isOpen }))}
                  style={chapterBtn}>
                  {isOpen ? <ChevronDown size={14} color="#9ca3af" /> : <ChevronRight size={14} color="#9ca3af" />}
                  <span style={{ fontSize: '0.7rem', color: '#9ca3af', fontWeight: 700, minWidth: 26 }}>
                    {ch.hier}
                  </span>
                  <span style={{ flex: 1, fontSize: '0.88rem', color: '#111827', textAlign: 'left' }}>
                    {stripUnitPrefix(ch.name)}
                  </span>
                  {chTotals.total > 0 && (
                    <span style={countPill}>{chTotals.passed} / {chTotals.total}</span>
                  )}
                </button>

                {isOpen && ch.sections.map((sec) => (
                  <div key={sec.name} style={{ marginLeft: 18, marginTop: 4 }}>
                    <div style={{ fontSize: '0.76rem', color: '#6b7280', margin: '6px 0 2px' }}>
                      {stripUnitPrefix(sec.name)}
                    </div>
                    {sec.items.map((it) => {
                      const c = counts(it.leaf.id);
                      const empty = c.total === 0;
                      return (
                        <button key={it.leaf.id} onClick={() => !empty && onPick(it.leaf.id)}
                          disabled={empty} style={{ ...itemBtn, opacity: empty ? 0.45 : 1,
                            cursor: empty ? 'default' : 'pointer' }}>
                          <span style={{ flex: 1, fontSize: '0.84rem', color: '#111827', textAlign: 'left' }}>
                            {stripUnitPrefix(it.name)}
                          </span>
                          <span style={countPill}>
                            {empty ? '준비 중' : `${c.passed} / ${c.total}`}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                ))}
              </div>
            );
          })}
        </section>
      ))}
    </div>
  );
}

const chapterBtn = {
  width: '100%', display: 'flex', alignItems: 'center', gap: 6,
  padding: '8px 10px', border: '1px solid #e5e7eb', borderRadius: 8,
  background: '#fff', cursor: 'pointer',
};
const itemBtn = {
  width: '100%', display: 'flex', alignItems: 'center', gap: 8,
  padding: '7px 10px', border: 'none', borderRadius: 6,
  background: 'transparent',
};
const countPill = {
  fontSize: '0.72rem', color: '#6b7280', fontWeight: 700, whiteSpace: 'nowrap',
};
