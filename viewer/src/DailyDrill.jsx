// 오늘의 인출 — 과목을 가로지르는 데일리 드릴.
//
// 합격수기 공통 전술: "회계는 휘발성 1위 — 하루만 안 봐도 손이 굳는다. 매일 인출."
// 지금까지는 관을 하나씩 찾아 들어가야만 문제를 만났다. 여기서는
// ① 마지막에 틀린 문항 ② 복습 만기가 지난 문항 을 섞어 한 자리에서 다시 묻는다.
import { useMemo, useState } from 'react';
import ParsedText from './ParsedText';
import { getDrillQueue, getDrillCounts, recordItem } from './studyDrill';

const KIND_LABEL = { ox: 'OX', prac: '계산', frame: '와꾸', journal: '분개' };

export default function DailyDrill({ limit = 20, onGoLeaf }) {
  const [round, setRound] = useState(0);            // 다시 뽑기용
  const queue = useMemo(() => getDrillQueue(limit), [limit, round]);
  const counts = useMemo(() => getDrillCounts(), [round]);
  const [i, setI] = useState(0);
  const [reveal, setReveal] = useState(false);
  const [tally, setTally] = useState({ right: 0, wrong: 0 });

  if (!queue.length) {
    return (
      <div style={{ padding: '40px 20px', textAlign: 'center', color: '#9ca3af', lineHeight: 1.8 }}>
        <div style={{ fontSize: '2rem', marginBottom: 10 }}>☕</div>
        <div style={{ fontWeight: 800, color: '#57534e', marginBottom: 6 }}>지금 인출할 문항이 없습니다</div>
        <div style={{ fontSize: '0.85rem' }}>
          교재의 <b>✅ OX</b>·<b>🧮 연습</b> 탭에서 문제를 풀면<br />
          틀린 것과 복습 만기가 된 것이 여기 모입니다.
        </div>
      </div>
    );
  }

  const done = i >= queue.length;
  const cur = queue[i];

  const answer = (ok) => {
    recordItem({
      kind: cur.kind, idx: cur.idx, q: cur.q, isCorrect: ok,
      leaf: { subject: cur.subject, leafId: cur.leafId, leafTitle: cur.leafTitle },
    });
    setTally((t) => ({ right: t.right + (ok ? 1 : 0), wrong: t.wrong + (ok ? 0 : 1) }));
    setReveal(false);
    setI((n) => n + 1);
  };

  return (
    <div style={{ padding: '14px 16px 24px' }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 10, flexWrap: 'wrap' }}>
        <span style={{ fontWeight: 900, fontSize: '1.02rem', color: '#1c1917' }}>🎯 오늘의 인출</span>
        <span style={{ fontSize: '0.76rem', color: '#78716c' }}>
          오답 {counts.wrong} · 복습 만기 {counts.due} · 누적 {counts.total}문항
        </span>
        <button
          onClick={() => { setRound((r) => r + 1); setI(0); setReveal(false); setTally({ right: 0, wrong: 0 }); }}
          style={{
            marginLeft: 'auto', fontSize: '0.73rem', fontWeight: 700, padding: '4px 10px',
            borderRadius: 6, border: '1px solid #d6d3d1', background: '#fff', color: '#57534e', cursor: 'pointer',
          }}>🔄 다시 뽑기</button>
      </div>

      {done ? (
        <div style={{
          padding: '26px 18px', textAlign: 'center', border: '1px solid #e7e5e4',
          borderRadius: 10, background: '#fdfdfb',
        }}>
          <div style={{ fontSize: '1.6rem', marginBottom: 8 }}>{tally.wrong === 0 ? '🎉' : '💪'}</div>
          <div style={{ fontWeight: 800, color: '#1c1917', marginBottom: 4 }}>
            {queue.length}문항 완료 — 정답 {tally.right} · 오답 {tally.wrong}
          </div>
          <div style={{ fontSize: '0.83rem', color: '#78716c', lineHeight: 1.7 }}>
            {tally.wrong > 0
              ? '틀린 문항은 내일 다시 나옵니다. 맞힌 것은 간격을 늘려 다시 물어봅니다.'
              : '전부 맞혔습니다. 복습 간격이 한 칸씩 늘어납니다.'}
          </div>
          <button
            onClick={() => { setRound((r) => r + 1); setI(0); setTally({ right: 0, wrong: 0 }); }}
            style={{
              marginTop: 14, fontSize: '0.8rem', fontWeight: 800, padding: '7px 16px', borderRadius: 7,
              border: '1px solid #a16207', background: '#faf8f2', color: '#a16207', cursor: 'pointer',
            }}>이어서 더 풀기</button>
        </div>
      ) : (
        <>
          <div style={{
            display: 'flex', alignItems: 'center', gap: 7, marginBottom: 8,
            fontSize: '0.74rem', color: '#78716c',
          }}>
            <span style={{
              fontWeight: 800, padding: '2px 8px', borderRadius: 5,
              background: cur.kind === 'ox' ? '#eef2f7' : '#faf8f2',
              color: cur.kind === 'ox' ? '#44546a' : '#a16207',
            }}>{KIND_LABEL[cur.kind] || cur.kind}</span>
            <span style={{ fontWeight: 700, color: '#57534e' }}>{cur.leafTitle || cur.leafId}</span>
            {!cur.lastCorrect && <span style={{ color: '#9a3412', fontWeight: 700 }}>· 지난번 오답</span>}
            <span style={{ marginLeft: 'auto', fontVariantNumeric: 'tabular-nums' }}>{i + 1} / {queue.length}</span>
          </div>

          <div style={{
            border: '1px solid #e7e5e4', borderRadius: 9, padding: '14px 16px',
            background: '#fff', minHeight: 96,
          }}>
            <ParsedText text={cur.q} />
          </div>

          {!reveal ? (
            <button onClick={() => setReveal(true)} style={{
              width: '100%', marginTop: 10, padding: '10px', borderRadius: 8, cursor: 'pointer',
              border: '1px dashed #d6d3d1', background: '#fafaf9', color: '#78716c',
              fontSize: '0.82rem', fontWeight: 700,
            }}>머릿속으로 답을 세운 뒤 눌러 주세요</button>
          ) : (
            <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
              <button onClick={() => answer(true)} style={{
                flex: 1, padding: '11px', borderRadius: 8, cursor: 'pointer', fontSize: '0.86rem', fontWeight: 800,
                border: '1.5px solid #4d7c5f', background: '#f5f8f5', color: '#4d7c5f',
              }}>✓ 맞혔다</button>
              <button onClick={() => answer(false)} style={{
                flex: 1, padding: '11px', borderRadius: 8, cursor: 'pointer', fontSize: '0.86rem', fontWeight: 800,
                border: '1.5px solid #9a3412', background: '#fbf5f3', color: '#9a3412',
              }}>✗ 틀렸다</button>
            </div>
          )}

          {onGoLeaf && (
            <button onClick={() => onGoLeaf(cur)} style={{
              marginTop: 8, width: '100%', padding: '7px', borderRadius: 7, cursor: 'pointer',
              border: '1px solid #e7e5e4', background: '#fff', color: '#78716c', fontSize: '0.76rem', fontWeight: 700,
            }}>📖 이 문항이 있는 관으로 가기</button>
          )}
        </>
      )}
    </div>
  );
}
