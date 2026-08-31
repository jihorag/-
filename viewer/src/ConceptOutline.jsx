// 개념 완성 목차 — 시안 253:2(ai-chapter).
//
// buildUnitTree 는 세 탭이 공유하는 '단일 목차' 모델이다(unitTree.js 첫 줄).
// 여기서 따로 만들면 네 탭의 목차가 갈라진다. 좁은 폭용 트리(ConceptTree)도
// 같은 모델을 쓴다.
//
// 시안이 예전 목차에 더한 것 넷:
//   1. 요약 한 줄 — 몇 관 중 몇 관, 정답률, 약한 곳 개수
//   2. 이어서 카드 — 중단한 자리로 한 번에
//   3. 목차순 / 약점순 — 무엇부터 볼지 고르게 한다
//   4. 줄마다 약점 배지와 기출 정답률
//
// 「약점」은 기출 정답률이 WEAK_UNDER 미만인 관이다. 논점 진행률이 아니라
// 정답률로 잡는다 — 논점을 다 봤는데 문제를 틀리는 관이 정확히 다시 볼 곳이다.
import { useMemo, useState } from 'react';
import { ChevronRight } from 'lucide-react';
import { buildUnitTree, stripUnitPrefix } from './unitTree';
import { applyScope } from './trackScope';
import { STATE } from './trackProgress';

const WEAK_UNDER = 0.6;

export default function ConceptOutline({
  leaves, scope, index, progress, onPick, quizStatsByLeaf, subjectName,
}) {
  const [sort, setSort] = useState('목차순');
  const scoped = useMemo(() => applyScope(leaves || [], scope), [leaves, scope]);
  const { divisions, multiDiv } = useMemo(() => buildUnitTree(scoped), [scoped]);

  // 장·절 자체가 학습 단위인 leaf 도 관 항목과 같은 모양으로 편다. 안 하면
  // 그 leaf 들이 목차에서 조용히 사라진다(경제학은 전부 관 레벨이라 증상이 없었다).
  const rowsOf = (ch) => {
    const out = [];
    if (ch.leaf) out.push({ leaf: ch.leaf, name: ch.name });
    ch.sections.forEach((sec) => {
      if (sec.leaf) out.push({ leaf: sec.leaf, name: sec.name });
      sec.items.forEach((it) => out.push({ leaf: it.leaf, name: it.name }));
    });
    return out;
  };

  const stat = useMemo(() => {
    const f = (id) => {
      const total = index?.[id]?.points || 0;
      const rec = (progress || {})[id] || {};
      const passed = Object.values(rec).filter((s) => s >= STATE.PASSED).length;
      const q = quizStatsByLeaf?.[id];
      const acc = q && q.answered > 0 ? q.accuracy : null;
      return {
        total, passed,
        done: total > 0 && passed >= total,
        exam: q?.total || 0,
        acc,
        weak: acc !== null && acc < WEAK_UNDER,
      };
    };
    return f;
  }, [index, progress, quizStatsByLeaf]);

  // 화면 전체를 요약하는 한 줄. 관 수·완료 관 수·정답률·약한 곳.
  const all = useMemo(
    () => divisions.flatMap((d) => d.chapters.flatMap(rowsOf)),
    // rowsOf 는 순수 함수라 의존성에 넣지 않는다.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [divisions],
  );
  const summary = useMemo(() => {
    let total = 0, done = 0, weak = 0, answered = 0, correct = 0;
    all.forEach(({ leaf }) => {
      const s = stat(leaf.id);
      if (s.total > 0) total += 1;
      if (s.done) done += 1;
      if (s.weak) weak += 1;
      const q = quizStatsByLeaf?.[leaf.id];
      if (q) { answered += q.answered; correct += q.correct; }
    });
    return { total, done, weak, acc: answered > 0 ? correct / answered : null };
  }, [all, stat, quizStatsByLeaf]);

  // 이어서 — 손을 댔지만 아직 안 끝난 첫 관. 없으면 아직 안 연 첫 관.
  const resume = useMemo(() => {
    let untouched = null;
    for (const r of all) {
      const s = stat(r.leaf.id);
      if (s.total === 0) continue;
      if (s.passed > 0 && !s.done) return { ...r, s };
      if (!untouched && s.passed === 0) untouched = { ...r, s };
    }
    return untouched;
  }, [all, stat]);

  const weakFirst = useMemo(
    () => all
      .map((r) => ({ ...r, s: stat(r.leaf.id) }))
      .filter((r) => r.s.total > 0 && r.s.acc !== null)
      .sort((a, b) => a.s.acc - b.s.acc),
    [all, stat],
  );

  return (
    <div className="cout">
      <section className="cout-summary">
        <div className="cout-summary-row">
          <span>
            {summary.total}관 중 {summary.done}관
            {summary.acc !== null && ` · 정답률 ${Math.round(summary.acc * 100)}%`}
          </span>
          {summary.weak > 0 && <span className="cout-weakn">약한 곳 {summary.weak}</span>}
        </div>
        <div className="cout-track">
          <div className="cout-track-fill"
            style={{ width: summary.total ? `${(summary.done / summary.total) * 100}%` : 0 }} />
        </div>

        {resume && (
          <button type="button" className="cout-continue" onClick={() => onPick(resume.leaf.id)}>
            <span className="cout-continue-t">
              <span className="cout-continue-title">이어서 · {stripUnitPrefix(resume.name)}</span>
              <span className="cout-continue-sub">논점 {resume.s.passed} / {resume.s.total}</span>
            </span>
            <ChevronRight size={16} strokeWidth={1.75} />
          </button>
        )}

        {weakFirst.length > 0 && (
          <div className="cout-sort" role="group" aria-label="정렬">
            {['목차순', '약점순'].map((k) => (
              <button type="button" key={k} className={`cout-chip${sort === k ? ' is-on' : ''}`}
                aria-pressed={sort === k} onClick={() => setSort(k)}>{k}</button>
            ))}
          </div>
        )}
      </section>

      {sort === '약점순'
        ? (
          <div className="cout-group">
            <div className="cout-ch">
              <span>정답률이 낮은 순</span>
              <span className="cout-ch-count">{weakFirst.length}관</span>
            </div>
            <div className="cout-items">
              {weakFirst.map((r) => (
                <Row key={r.leaf.id} name={r.name} s={r.s} onPick={() => onPick(r.leaf.id)} />
              ))}
            </div>
          </div>
        )
        : divisions.map((div) => (
          <div key={div.name}>
            {multiDiv && <h3 className="cout-div">{div.name}</h3>}
            {div.chapters.map((ch) => {
              const rows = rowsOf(ch);
              const chDone = rows.filter((r) => stat(r.leaf.id).done).length;
              const chTotal = rows.filter((r) => stat(r.leaf.id).total > 0).length;
              return (
                <div className="cout-group" key={div.name + '/' + ch.name}>
                  <div className="cout-ch">
                    <span>{ch.hier} {stripUnitPrefix(ch.name)}</span>
                    {chTotal > 0 && <span className="cout-ch-count">{chDone} / {chTotal}</span>}
                  </div>
                  <div className="cout-items">
                    {rows.map((r) => (
                      <Row key={r.leaf.id} name={r.name} s={stat(r.leaf.id)}
                        onPick={() => onPick(r.leaf.id)} />
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        ))}
    </div>
  );
}

function Row({ name, s, onPick }) {
  const empty = s.total === 0;
  return (
    <button type="button" className={`cout-row${s.done ? ' is-done' : ''}`}
      disabled={empty} onClick={() => !empty && onPick()}>
      <span className="cout-row-t">
        <span className="cout-row-name">{stripUnitPrefix(name)}</span>
        <span className="cout-row-meta">
          {s.weak && <span className="cout-weak">약점</span>}
          <span>
            {empty ? '준비 중' : `논점 ${s.passed} / ${s.total}`}
            {s.exam ? ` · 기출 ${s.exam}` : ''}
          </span>
        </span>
      </span>
      {/* 아직 안 푼 절은 비운다 — 「—」가 줄줄이 늘어서면 그 대시가 먼저 읽힌다. */}
      <span className={`cout-pct${s.weak ? ' is-low' : ''}`}>
        {s.acc !== null ? `${Math.round(s.acc * 100)}%` : ''}
      </span>
      <span className="cout-tail">
        {s.done ? <span className="cout-donetag">완료</span> : <ChevronRight size={16} strokeWidth={1.75} />}
      </span>
    </button>
  );
}
