// 홈 — 오늘 할 일 하나와 현황만 남긴 화면.
//
// 매일 여는 화면에서 "그래서 지금 뭘 하지"를 찾는 데 스크롤이 필요하면 홈이 제 일을 못 한다.
// 그래서 두 덩이로만 나눈다.
//   오늘 — 지금 할 일 하나 + 네 갈래 진입
//   현황 — 과목 점수 + 합격까지의 여정
// 상세 지표는 「상세 분석 보기」 뒤로 보낸다. 1단 컬럼에서 펼치면 스크롤이 몇 배가 된다.
//
// 색 규칙: 액센트를 쓰는 자리는 세 곳뿐이다.
//   ① 지금 할 일의 주 버튼  ② 여정의 '다음 목표' 마커  ③ 상세 분석 링크 옆 D-day
// 인장색(붉은색)은 과락 위험에만, 화면당 하나.
// 리터럴 색은 쓰지 않는다 — 전부 tokens.css 의 var() 다.
import { useEffect, useState } from 'react';
import { Sparkles, Zap, Compass, CalendarCheck, Gauge, Route, AlertTriangle } from 'lucide-react';

/** 640px 미만인지. 두 형태를 다 그려놓고 CSS 로 감추면 모바일에 쓸모없는 DOM 이 남는다. */
function useIsNarrow() {
  const q = '(max-width: 639px)';
  const [narrow, setNarrow] = useState(
    () => (typeof window !== 'undefined' ? window.matchMedia(q).matches : false));
  useEffect(() => {
    const mq = window.matchMedia(q);
    const on = (e) => setNarrow(e.matches);
    mq.addEventListener('change', on);
    // 초기값은 useState 초기화에서 이미 읽었다. 여기서 다시 세팅하면 렌더가 연쇄된다.
    return () => mq.removeEventListener('change', on);
  }, []);
  return narrow;
}

const card = {
  background: 'var(--sheet)',
  border: '0.5px solid var(--line)',
  borderRadius: 'var(--radius-lg)',
};
const sectionLabel = {
  fontSize: 'var(--text-2xs)',
  fontWeight: 'var(--weight-bold)',
  letterSpacing: '0.12em',
  color: 'var(--ink-3)',
  paddingLeft: 2,
  margin: '18px 0 8px',
};
const cardHead = {
  display: 'flex', alignItems: 'center', gap: 6,
  fontSize: 14, fontWeight: 'var(--weight-bold)', color: 'var(--ink)',
};
const num = { fontVariantNumeric: 'tabular-nums' };
const srOnly = {
  position: 'absolute', width: 1, height: 1, overflow: 'hidden',
  clip: 'rect(0 0 0 0)', whiteSpace: 'nowrap',
};

/** 과목 한 줄 — 이름 / 막대(합격선 눈금) / 점수. */
function SubjectRow({ name, score, danger, narrow }) {
  const has = score != null;
  const pct = has ? Math.max(0, Math.min(100, score)) : 0;
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: narrow ? 10 : 12, padding: '5px 0' }}>
      <div style={{ width: narrow ? 76 : 104, flexShrink: 0, fontSize: 'var(--text-xs)',
        color: danger ? 'var(--seal-ink)' : 'var(--ink-2)' }}>{name}</div>
      <div style={{ flex: 1, position: 'relative', height: 7,
        borderRadius: 'var(--radius-pill)', background: 'var(--sunken)' }}
        role="progressbar" aria-label={`${name} 실력 점수`}
        aria-valuenow={has ? Math.round(score) : undefined}
        aria-valuemin={0} aria-valuemax={100}
        aria-valuetext={has ? `${score.toFixed(1)}점` : '아직 측정되지 않음'}>
        {/* 값이 0이면 채움을 그리지 않는다 — 폭 0의 점이 남으면 진행된 것처럼 보인다 */}
        {pct > 0 && (
          <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: `${pct}%`,
            borderRadius: 'var(--radius-pill)',
            background: danger ? 'var(--seal)' : 'var(--ink-2)' }} />
        )}
        {/* 합격선 60 눈금 — 막대 위로 솟게 둬서 숫자를 읽지 않아도 넘었는지 보인다 */}
        <div aria-hidden style={{ position: 'absolute', left: '60%', top: -3,
          width: 1, height: 13, background: 'var(--ink-4)' }} />
      </div>
      <div style={{ ...num, width: 44, flexShrink: 0, textAlign: 'right',
        fontSize: has ? 'var(--text-base)' : undefined,
        color: has ? (danger ? 'var(--seal-ink)' : 'var(--ink)') : 'var(--ink-4)' }}>
        {has ? score.toFixed(1) : '—'}
      </div>
    </div>
  );
}

/** 여정 마커 — 합격 / 다음 목표 / 예정. 색만으로 상태를 전하지 않는다. */
function Marker({ status, size = 16 }) {
  const base = {
    width: size, height: size, borderRadius: 'var(--radius-pill)', flexShrink: 0,
    display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
  };
  if (status === 'passed') {
    return <span style={{ ...base, background: 'var(--ink)', color: 'var(--ink-invert)', fontSize: 9 }}>✓</span>;
  }
  if (status === 'next') return <span style={{ ...base, background: 'var(--accent)' }} />;
  return <span style={{ ...base, border: '1.5px solid var(--line-strong)' }} />;
}
const STATUS_WORD = { passed: '합격', next: '다음 목표', pending: '예정' };
const markerStatus = (mk) => (mk.next ? 'next' : mk.status === 'passed' ? 'passed' : 'pending');
const statusInk = (st) => (st === 'next' ? 'var(--accent-ink)'
  : st === 'passed' ? 'var(--ink-2)' : 'var(--ink-3)');

/** 합격까지의 여정 — 넓으면 격자, 좁으면 리스트. 형태가 아예 다르다. */
function Journey({ rows, thisYear, thisMonth, nextLabel, nextDday, onEdit, narrow }) {
  const head = (
    <div style={{ display: 'flex', alignItems: 'center', marginBottom: 14 }}>
      <div style={cardHead}>
        <Route size={16} strokeWidth={1.8} color="var(--ink-2)" aria-hidden />
        합격까지의 여정
      </div>
      <div style={{ marginLeft: 'auto', fontSize: 'var(--text-2xs)', color: 'var(--ink-3)' }}>
        {nextLabel}
        {nextDday && <span style={{ ...num, color: 'var(--accent-ink)' }}>{nextDday}</span>}
        {onEdit && <>
          {' · '}
          <button onClick={onEdit} style={{ background: 'none', border: 'none', padding: 0,
            color: 'var(--ink-3)', cursor: 'pointer', fontSize: 'var(--text-2xs)' }}>편집</button>
        </>}
      </div>
    </div>
  );

  if (narrow) {
    // 390px 에서 한 칸이 29px 이라 격자에는 마커도 라벨도 안 들어간다. 리스트로 친다.
    return (
      <section style={{ ...card, padding: 16 }}>
        {head}
        {rows.map((r) => {
          const evs = (r.markers || []).slice().sort((a, b) => a.month - b.month);
          if (!evs.length) return null;
          return (
            <div key={r.id}>
              <div style={{ padding: '12px 0 6px', display: 'flex', gap: 8, alignItems: 'baseline' }}>
                <span style={{ fontSize: 'var(--text-sm)', color: 'var(--ink)' }}>{r.year}</span>
                <span style={{ fontSize: 'var(--text-2xs)', color: 'var(--ink-3)' }}>
                  {r.grade} · {r.age}세
                </span>
              </div>
              {evs.map((mk) => {
                const st = markerStatus(mk);
                return (
                  <div key={mk.id} style={{ display: 'flex', gap: 10, alignItems: 'center',
                    minHeight: 40, borderTop: '0.5px solid var(--line-2)' }}>
                    <span style={{ ...num, width: 36, fontSize: 'var(--text-xs)', color: 'var(--ink-3)' }}>
                      {mk.month}월
                    </span>
                    <Marker status={st} />
                    <span style={{ fontSize: 'var(--text-xs)', color: 'var(--ink)' }}>{mk.label}</span>
                    <span style={{ marginLeft: 'auto', fontSize: 'var(--text-2xs)', color: statusInk(st) }}>
                      {STATUS_WORD[st]}
                    </span>
                  </div>
                );
              })}
            </div>
          );
        })}
      </section>
    );
  }

  return (
    <section style={{ ...card, padding: 16 }}>
      {head}
      <div style={{ display: 'grid', gridTemplateColumns: '68px repeat(12, 1fr)', gap: '6px 2px' }}>
        <div />
        {Array.from({ length: 12 }, (_, i) => (
          <div key={i} style={{ textAlign: 'center', fontSize: 'var(--text-2xs)', color: 'var(--ink-4)' }}>
            {i + 1}
          </div>
        ))}
        {rows.map((r) => [
          <div key={`${r.id}-y`}>
            <div style={{ fontSize: 'var(--text-sm)', color: 'var(--ink)' }}>{r.year}</div>
            <div style={{ fontSize: 'var(--text-2xs)', color: 'var(--ink-3)' }}>
              {r.grade} · {r.age}세
            </div>
          </div>,
          ...Array.from({ length: 12 }, (_, i) => {
            const m = i + 1;
            const mk = (r.markers || []).find((x) => x.month === m);
            const isNow = r.year === thisYear && m === thisMonth;
            const st = mk ? markerStatus(mk) : null;
            return (
              <div key={`${r.id}-${m}`} style={{
                position: 'relative', height: 44, borderRadius: 'var(--radius-sm)',
                background: isNow ? 'var(--accent-bg)' : 'var(--sheet-3)',
                display: 'flex', flexDirection: 'column',
                alignItems: 'center', justifyContent: 'center', gap: 2,
              }}>
                {mk && <>
                  <span style={{ fontSize: 'var(--text-2xs)', color: statusInk(st) }}>{mk.label}</span>
                  <Marker status={st} />
                  <span style={srOnly}>{r.year}년 {m}월 {mk.label} {STATUS_WORD[st]}</span>
                </>}
              </div>
            );
          }),
        ])}
      </div>
      <div style={{ display: 'flex', gap: 16, marginTop: 14 }}>
        {['passed', 'next', 'pending'].map((st) => (
          <span key={st} style={{ display: 'inline-flex', alignItems: 'center', gap: 6,
            fontSize: 'var(--text-2xs)', color: 'var(--ink-3)' }}>
            <Marker status={st} size={12} /> {STATUS_WORD[st]}
          </span>
        ))}
      </div>
    </section>
  );
}

/** 이번 주 7칸 — 목표를 지킨 날은 채운다. */
function Week({ week }) {
  if (!week || !week.length) return null;
  return (
    <span style={{ display: 'inline-flex', gap: 4, flexShrink: 0 }}>
      {week.map((w, i) => (
        <span key={i} title={w.label} aria-label={`${w.label} ${w.met ? '목표 달성' : '미달성'}`}
          style={{
            width: 8, height: 8, borderRadius: 2,
            background: w.isToday ? 'var(--line-strong)' : w.met ? 'var(--ink-2)' : 'var(--sunken)',
          }} />
      ))}
    </span>
  );
}

const QUICK_ICON = { tutor: Sparkles, drill: Zap, quiz: Compass, plan: CalendarCheck };

export default function HomeToday({
  greeting, streakDays, examLabel, dday,
  now,        // { label, title, desc, cta, minutes, onGo }
  goal,       // { done, target, week: [{met, isToday, label}] }
  quick,      // [{ key, title, desc, onGo }]
  subjects,   // [{ id, name, shortName, score, danger }]
  riskNote,
  journey,    // { rows, thisYear, thisMonth, nextLabel, nextDday, onEdit }
  emptyHint,
  onDetail,
}) {
  const narrow = useIsNarrow();
  const gpct = goal && goal.target ? Math.min(100, Math.round((goal.done / goal.target) * 100)) : 0;

  // 연속 0일은 격려가 아니라 지적으로 읽힌다. 0이면 아예 내지 않는다.
  const meta = [
    streakDays > 0 ? `연속 ${streakDays}일` : null,
    dday ? (narrow ? dday : `${examLabel} ${dday}`) : null,
  ].filter(Boolean).join(' · ');

  return (
    <div className="home-col">
      <header style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
        <h1 style={{ fontSize: 'var(--text-base)', fontWeight: 'var(--weight-bold)',
          color: 'var(--ink)', margin: 0 }}>{greeting}</h1>
        {meta && (
          <div style={{ marginLeft: 'auto', fontSize: 'var(--text-2xs)', color: 'var(--ink-3)' }}>
            {meta}
          </div>
        )}
      </header>

      <div style={sectionLabel}>오늘</div>

      <section style={{ ...card, marginBottom: 8 }}>
        <div style={{ padding: narrow ? 16 : 18 }}>
          <div style={{ fontSize: 'var(--text-2xs)', color: 'var(--ink-3)', marginBottom: 8 }}>
            {now.label}
          </div>
          <div style={{ fontSize: narrow ? 19 : 22, fontWeight: 'var(--weight-bold)',
            color: 'var(--ink)', lineHeight: 1.35, marginBottom: 6 }}>{now.title}</div>
          {now.desc && (
            <div style={{ fontSize: 'var(--text-sm)', color: 'var(--ink-2)', marginBottom: 16 }}>
              {now.desc}
            </div>
          )}
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <button onClick={now.onGo} style={{
              background: 'var(--accent)', color: 'var(--ink-invert)', border: 'none',
              borderRadius: 'var(--radius-md)', padding: '12px 22px', minHeight: 'var(--touch-min)',
              fontSize: 'var(--text-base)', fontWeight: 'var(--weight-bold)', cursor: 'pointer',
            }}>{now.cta}</button>
            {now.minutes ? (
              <span style={{ fontSize: 'var(--text-sm)', color: 'var(--ink-3)' }}>약 {now.minutes}분</span>
            ) : null}
          </div>
        </div>

        {goal && (
          <div style={{ borderTop: '0.5px solid var(--line-2)', padding: '12px 18px',
            display: 'flex', flexDirection: narrow ? 'column' : 'row',
            alignItems: narrow ? 'flex-start' : 'center', gap: narrow ? 8 : 12 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, width: '100%' }}>
              <span style={{ flexShrink: 0, whiteSpace: 'nowrap',
                fontSize: 'var(--text-xs)', color: 'var(--ink-3)' }}>오늘 목표</span>
              <div style={{ flex: 1, height: 6, borderRadius: 'var(--radius-pill)',
                background: 'var(--sunken)' }}
                role="progressbar" aria-label="오늘 목표 진행"
                aria-valuenow={goal.done} aria-valuemin={0} aria-valuemax={goal.target}>
                {/* 0일 때 폭 0의 점을 남기면 카드 테두리에 걸려 잘린 것처럼 보인다 */}
                {gpct > 0 && (
                  <div style={{ width: `${gpct}%`, height: '100%',
                    borderRadius: 'var(--radius-pill)', background: 'var(--ink-2)' }} />
                )}
              </div>
              <span style={{ ...num, flexShrink: 0, whiteSpace: 'nowrap',
                fontSize: 'var(--text-sm)', color: 'var(--ink)' }}>
                {goal.done} / {goal.target}
              </span>
              {!narrow && <Week week={goal.week} />}
            </div>
            {narrow && <Week week={goal.week} />}
          </div>
        )}
      </section>

      <div className="home-quick">
        {quick.map((q) => {
          const Ico = QUICK_ICON[q.key] || Sparkles;
          return (
            <button key={q.key} onClick={q.onGo} style={{
              ...card, padding: '12px 13px', minHeight: 64,
              // 부제가 있는 칸과 없는 칸의 높이를 맞추고, 내용을 세로 가운데에 둔다.
              // 가로는 왼쪽 정렬이라 align-items 가 아니라 justify-content 로 가운데를 잡는다.
              display: 'flex', flexDirection: 'column', justifyContent: 'center',
              textAlign: 'left', cursor: 'pointer',
            }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Ico size={15} strokeWidth={1.8} color="var(--ink-2)" aria-hidden />
                <span style={{ fontSize: 'var(--text-sm)', fontWeight: 'var(--weight-bold)',
                  color: 'var(--ink)' }}>{q.title}</span>
              </span>
              {/* 자리채움 문구를 넣지 않는다. 값이 없으면 부제를 아예 안 낸다 */}
              {q.desc && (
                <span style={{ display: 'block', marginTop: 3,
                  fontSize: 'var(--text-2xs)', color: 'var(--ink-3)' }}>{q.desc}</span>
              )}
            </button>
          );
        })}
      </div>

      <div style={sectionLabel}>현황</div>

      <section style={{ ...card, padding: 16, marginBottom: 8 }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 14 }}>
          <div style={cardHead}>
            <Gauge size={16} strokeWidth={1.8} color="var(--ink-2)" aria-hidden />
            과목 현황
          </div>
          {!emptyHint && (
            <div style={{ marginLeft: 'auto', fontSize: 'var(--text-2xs)', color: 'var(--ink-3)' }}>
              눈금 = 합격선 60
            </div>
          )}
        </div>
        {/* 점수가 하나도 없으면 눈금만 있는 빈 막대 5줄이 남는다. 그건 아무 뜻도 전하지 못한다 */}
        {emptyHint ? (
          <div style={{ fontSize: 'var(--text-sm)', color: 'var(--ink-3)',
            lineHeight: 1.6, padding: '4px 0 8px' }}>{emptyHint}</div>
        ) : subjects.map((s) => (
          <SubjectRow key={s.id} narrow={narrow}
            name={narrow && s.shortName ? s.shortName : s.name}
            score={s.score} danger={s.danger} />
        ))}
        {riskNote && (
          <div style={{ marginTop: 14, background: 'var(--seal-bg)',
            border: '0.5px solid var(--seal-line)', borderRadius: 'var(--radius-md)',
            padding: '10px 12px', display: 'flex', gap: 8, alignItems: 'flex-start' }}>
            <AlertTriangle size={15} strokeWidth={1.9} color="var(--seal)" aria-hidden
              style={{ flexShrink: 0, marginTop: 1 }} />
            <span style={{ fontSize: 'var(--text-xs)', color: 'var(--seal-ink)', lineHeight: 1.5 }}>
              {riskNote}
            </span>
          </div>
        )}
      </section>

      {journey && journey.rows.length > 0 && <Journey {...journey} narrow={narrow} />}

      <div style={{ textAlign: 'center', marginTop: 8 }}>
        <button onClick={onDetail} style={{
          background: 'none', border: 'none', cursor: 'pointer', minHeight: 'var(--touch-min)',
          padding: '0 12px', fontSize: 'var(--text-sm)', color: 'var(--accent-ink)',
        }}>상세 분석 보기 →</button>
      </div>
    </div>
  );
}
