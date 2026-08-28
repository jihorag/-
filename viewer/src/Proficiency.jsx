// 실력 리포트 — AI 학습·드릴·문제풀이를 종합한 진단 문서.
// 디자인: 실제 인쇄 리포트(미색 종이 시트 + 명조 활자 + 레터헤드 + 정량 표 + 겹친 종이 그림자).
// 계산은 proficiencyEngine.js, 시각화는 인라인 SVG(외부 차트 라이브러리 없음).
import { useState, useEffect, useMemo, useRef } from 'react';
import { ArrowLeft, RefreshCw, ChevronRight, TrendingUp, PenLine, Printer } from 'lucide-react';
import { computeProficiency, snapshotProficiency, getProficiencyHistory } from './proficiencyEngine';
import { sendMessagesUnified } from './aiProviders';
import { resolveCall } from './modelRegistry';
import { getPrefs, getRoleModel } from './aiLearningStore';
import { loadPassInsights, planStrategyText } from './passInsights';
import ParsedText from './ParsedText';
import SubjectDiagnostic from './SubjectDiagnostic';

// 활자·지질(紙質)
const SERIF = "'AppleMyungjo','Nanum Myeongjo','Batang','Times New Roman',serif";
const INK = { 900: '#17150f', 800: '#26231b', 700: '#3a362c', 600: '#57513f', 500: '#726b57', 400: '#9a927d', 300: '#c9c2ad', 200: '#e2dccb', 100: '#efe9da', 50: '#f7f2e6' };
const PAPER = '#fbf8f0';   // 미색 종이
const DESK = '#ffffff';    // 바깥 배경(흰색)
const STATUS = {
  mastered: { c: INK[800], label: '숙달' },
  learning: { c: INK[500], label: '학습중' },
  weak: { c: INK[300], label: '취약' },
  untouched: { c: INK[100], label: '미착수' },
};
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const rn = (v) => (v == null ? '–' : Math.round(v));
const NUM = { fontVariantNumeric: 'tabular-nums' };
const ROMAN = ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ'];

// ── 반원 게이지 ──
function Gauge({ value, size = 172 }) {
  const r = size / 2 - 15, cx = size / 2, cy = size / 2;
  const a0 = Math.PI, a1 = 0;
  const ang = a0 + (a1 - a0) * clamp01(value / 100);
  const pt = (a, rad) => [cx + rad * Math.cos(a), cy + rad * Math.sin(a)];
  const arc = (from, to, rad) => {
    const [x0, y0] = pt(from, rad), [x1, y1] = pt(to, rad);
    const large = Math.abs(to - from) > Math.PI ? 1 : 0;
    return `M ${x0} ${y0} A ${rad} ${rad} 0 ${large} 1 ${x1} ${y1}`;
  };
  const [hx, hy] = pt(ang, r);
  const [tx, ty] = pt(a0 + (a1 - a0) * 0.6, r + 3), [tx2, ty2] = pt(a0 + (a1 - a0) * 0.6, r - 12);
  return (
    <svg width={size} height={size / 2 + 22} viewBox={`0 0 ${size} ${size / 2 + 22}`}>
      <path d={arc(a0, a1, r)} fill="none" stroke={INK[200]} strokeWidth={10} strokeLinecap="butt" />
      <path d={arc(a0, ang, r)} fill="none" stroke={INK[800]} strokeWidth={10} strokeLinecap="butt" />
      <line x1={tx} y1={ty} x2={tx2} y2={ty2} stroke={INK[600]} strokeWidth={1.5} />
      <circle cx={hx} cy={hy} r={4.5} fill={PAPER} stroke={INK[800]} strokeWidth={2.5} />
      <text x={cx} y={cy - 2} textAnchor="middle" fontSize={38} fontWeight={700} fill={INK[900]} fontFamily={SERIF}>{Math.round(value)}</text>
    </svg>
  );
}

// ── 3축 레이더 ──
function Radar({ U, R, A, size = 104 }) {
  const cx = size / 2, cy = size / 2, rad = size / 2 - 20;
  const axes = [
    { label: '이해', val: U, ang: -Math.PI / 2 },
    { label: '적용', val: A, ang: -Math.PI / 2 + (2 * Math.PI) / 3 },
    { label: '인출', val: R, ang: -Math.PI / 2 + (4 * Math.PI) / 3 },
  ];
  const pt = (ang, rr) => [cx + rr * Math.cos(ang), cy + rr * Math.sin(ang)];
  const poly = axes.map((a) => pt(a.ang, rad * clamp01((a.val || 0) / 100)).join(',')).join(' ');
  const ring = (f) => axes.map((a) => pt(a.ang, rad * f).join(',')).join(' ');
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      {[0.5, 1].map((f, i) => <polygon key={i} points={ring(f)} fill="none" stroke={INK[200]} strokeWidth={0.8} />)}
      {axes.map((a, i) => { const [x, y] = pt(a.ang, rad); return <line key={i} x1={cx} y1={cy} x2={x} y2={y} stroke={INK[200]} strokeWidth={0.8} />; })}
      <polygon points={poly} fill="rgba(38,35,27,0.12)" stroke={INK[700]} strokeWidth={1.3} />
      {axes.map((a, i) => { const [lx, ly] = pt(a.ang, rad + 10); return <text key={i} x={lx} y={ly + 3} textAnchor="middle" fontSize={7.5} fontWeight={700} fill={INK[500]}>{a.label}</text>; })}
    </svg>
  );
}

function Spark({ data }) {
  const w = 300, h = 46, pad = 6;
  const max = Math.max(60, ...data), min = Math.min(40, ...data);
  const x = (i) => pad + (i / Math.max(1, data.length - 1)) * (w - pad * 2);
  const y = (v) => h - pad - ((v - min) / Math.max(1, max - min)) * (h - pad * 2);
  const pts = data.map((v, i) => `${x(i)},${y(v)}`).join(' ');
  return (
    <svg width="100%" viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" style={{ display: 'block' }}>
      <line x1={pad} y1={y(60)} x2={w - pad} y2={y(60)} stroke={INK[300]} strokeWidth={0.8} strokeDasharray="2 3" />
      <polyline points={pts} fill="none" stroke={INK[700]} strokeWidth={1.5} strokeLinejoin="round" />
      {data.map((v, i) => <circle key={i} cx={x(i)} cy={y(v)} r={2} fill={INK[800]} />)}
    </svg>
  );
}

function Grade({ tier }) {
  if (!tier) return null;
  return <span style={{ fontSize: '0.58rem', fontWeight: 800, color: INK[600], border: `1px solid ${INK[400]}`, padding: '0 3px', ...NUM }}>{tier}</span>;
}

// 로마숫자 표제 섹션
function DocSection({ no, title, children }) {
  return (
    <section style={{ marginTop: 26 }}>
      <h2 style={{ fontFamily: SERIF, fontSize: '1.05rem', fontWeight: 800, color: INK[900], margin: '0 0 3px', letterSpacing: '-0.01em' }}>
        <span style={{ color: INK[400], marginRight: 9 }}>{no}</span>{title}
      </h2>
      <div style={{ borderBottom: `1px solid ${INK[300]}`, marginBottom: 13 }} />
      {children}
    </section>
  );
}

const METHODS = [
  ['테스팅 효과', '읽기(이해)보다 인출·문제풀이가 장기기억에 강하므로 인출 35%·적용 45%·이해 20%로 가중한다. (Roediger & Karpicke, 2006)'],
  ['망각곡선·간격효과', '복습 없이 시간이 지나면 인출가능성이 지수적으로 떨어진다. 마지막 학습 경과일과 회독으로 현재 인출가능성을 계산해 오래된 점수를 할인한다. (Ebbinghaus; Cepeda, 2006)'],
  ['시험 타당도', '기출 출제량(A~D급)으로 단원을 가중해 커버리지가 아닌 빈출 실력을 반영한다.'],
  ['메타인지 보정', '“안다”고 표시했으나 틀린 비율을 과신으로 계상해 별도로 짚는다. (Bjork)'],
  ['측정의 정직성', '표본이 적으면 정답률을 Wilson 하한으로 보수적으로 잡고 신뢰도를 병기한다.'],
];

// AI 총평용 실측 데이터 요약
function buildDataSummary(rep, tab) {
  const o = rep.overall;
  const idx = tab === 1 ? o.stage1Index : o.stage2Index;
  const subs = Object.values(rep.subjects).filter((s) => s && s.stage === tab);
  const L = [`[${tab}차 실력 진단 — 실측 지표]`];
  L.push(`종합 실력 지수 ${Math.round(idx)}/100 (합격선 60${tab === 1 ? `, 예상 원점수 ${o.expected.lo}~${o.expected.hi}점(추정)` : ''}).`);
  L.push('과목별(점수·완성도·이해/인출/적용·기출표본·특이점):');
  for (const s of subs) {
    const bits = [`${s.short} ${Math.round(s.score)}점`, `완성도 ${Math.round(s.completion)}%(숙달 ${s.buckets.mastered}/${s.buckets.total})`, `이해${rn(s.axes.U)}/인출${rn(s.axes.R)}/적용${rn(s.axes.A)}`, s.quizN > 0 ? `기출 ${s.quizN}문항` : '기출 미풀이'];
    const flags = [];
    if (s.axes.U != null && s.axes.R != null && s.axes.U - s.axes.R >= 25) flags.push('이해≫인출(아는 착각)');
    if (s.calibration && s.calibration.overconfidence >= 0.3 && s.calibration.knowN >= 4) flags.push(`과신 ${Math.round(s.calibration.overconfidence * 100)}%`);
    if (s.decayRisk > s.decaySafe && s.decayRisk + s.decaySafe > 0) flags.push('망각 위험권');
    if (s.confidence < 0.3) flags.push('측정 데이터 부족');
    L.push(`- ${bits.join(' · ')}${flags.length ? ' · ' + flags.join(', ') : ''}`);
  }
  const weak = [];
  for (const s of subs) for (const w of s.weakTop.slice(0, 3)) weak.push(`${s.short} ${w.title}(${w.tier ? w.tier + '급' : '-'}, ${STATUS[w.status]?.label || w.status})`);
  if (weak.length) L.push(`빈출×약점 우선순위: ${weak.slice(0, 8).join(' / ')}.`);
  return L.join('\n');
}

// AI 총평 → '## 소제목' 분리해 명조 정렬 본문으로
function ProseBody({ text }) {
  const parts = (text || '').split(/\n(?=##\s)/).map((s) => s.trim()).filter(Boolean);
  const sections = parts.map((p) => {
    const m = p.match(/^##\s*(.+?)\s*\n([\s\S]*)$/) || p.match(/^##\s*(.+?)\s*$/);
    return m ? { h: m[1].trim(), body: (m[2] || '').trim() } : { h: null, body: p };
  });
  return (
    <div style={{ fontFamily: SERIF }}>
      {sections.map((s, i) => (
        <div key={i} style={{ marginBottom: 12 }}>
          {s.h && <div style={{ fontSize: '0.82rem', fontWeight: 800, color: INK[800], marginBottom: 3 }}>{s.h}</div>}
          {s.body && <div className="report-prose" style={{ fontSize: '0.86rem', color: INK[700], lineHeight: 1.85, textAlign: 'justify' }}><ParsedText text={s.body} /></div>}
        </div>
      ))}
    </div>
  );
}

const PROSE_KEY = 'proficiency-prose-v1';
const loadProse = () => { try { return JSON.parse(localStorage.getItem(PROSE_KEY) || '{}') || {}; } catch { return {}; } };
const saveProse = (m) => { try { localStorage.setItem(PROSE_KEY, JSON.stringify(m)); } catch { /* quota */ } };

function subjectRemark(s) {
  const f = [];
  if (s.axes.U != null && s.axes.R != null && s.axes.U - s.axes.R >= 25) f.push('아는 착각');
  if (s.calibration && s.calibration.overconfidence >= 0.3 && s.calibration.knowN >= 4) f.push(`과신 ${Math.round(s.calibration.overconfidence * 100)}%`);
  if (s.decayRisk > s.decaySafe && s.decayRisk + s.decaySafe > 0) f.push('망각 위험');
  if (s.confidence < 0.3) f.push('표본 부족');
  return f.length ? f.join(' · ') : '양호';
}

export default function Proficiency({ ctx, onGoDrill, onBack, onReview, onOpen }) {
  const [rep, setRep] = useState(null);
  const [busy, setBusy] = useState(false);
  // 상단 선택바(과목별 진단)와 공유하는 단일 선택 — 인쇄 리포트의 1·2차도 여기서 파생.
  const [sel, setSel] = useState('all');
  const S2_IDS = ['appraisal_practice', 'appraisal_theory', 'appraisal_law'];
  const tab = (sel === '2차' || S2_IDS.includes(sel)) ? 2 : 1;
  // 종합 리포트(Ⅰ~Ⅳ)는 개요(전과목·제1차·제2차)에서만. 개별 과목을 고르면 그 과목 진단만 보여준다.
  const isOverview = sel === 'all' || sel === '1차' || sel === '2차';
  const [prose, setProse] = useState(() => loadProse());
  const [proseBusy, setProseBusy] = useState(false);
  const [proseErr, setProseErr] = useState('');
  const insightsRef = useRef(null);

  const ctxRef = useRef(ctx); ctxRef.current = ctx;
  const run = async () => {
    setBusy(true);
    try { const r = await computeProficiency(ctxRef.current || {}); setRep(r); snapshotProficiency(r); } finally { setBusy(false); }
  };
  useEffect(() => { run(); loadPassInsights().then((d) => { insightsRef.current = d; }); /* eslint-disable-line */ }, []);

  const subjectsArr = useMemo(() => (rep ? Object.values(rep.subjects).filter((s) => s && s.stage === tab) : []), [rep, tab]);
  const weakGlobal = useMemo(() => {
    if (!rep) return [];
    const rows = [];
    for (const s of Object.values(rep.subjects)) { if (!s || s.stage !== tab) continue; for (const w of s.weakTop) rows.push({ ...w, sid: s.id, sshort: s.short }); }
    return rows.sort((a, b) => b.leverage - a.leverage).slice(0, 10);
  }, [rep, tab]);
  const hist = useMemo(() => getProficiencyHistory().slice(-14), [rep]);

  const model = (getPrefs() && getPrefs().model) || getRoleModel('gen', null) || getRoleModel('drill', null);
  const { apiKey, baseUrl, needsKey } = model ? resolveCall(model) : { apiKey: '', baseUrl: '', needsKey: true };
  const genProse = async () => {
    if (!rep || proseBusy) return;
    if (needsKey && !apiKey) { setProseErr('AI 총평은 클라우드 모델 키가 필요해요 (AI 학습 ⚙️ 설정).'); return; }
    setProseBusy(true); setProseErr('');
    try {
      const data = buildDataSummary(rep, tab);
      const strat = planStrategyText(insightsRef.current) || '';
      const system = `너는 감정평가사 수험 진단 전문가다. 아래는 한 수험생의 학습을 계산한 '실측 지표'다. 이 숫자들만 근거로 진단 리포트 톤의 총평을 한국어로 써라.
[형식] 마크다운. 다음 소제목을 정확히 '## '로 4개: ## 종합 진단 / ## 강점 / ## 약점과 원인 / ## 이번 주 처방
[규칙] 데이터에 없는 사실 창작 금지. 점수·비율·과목명을 구체적으로 인용. '아는 착각·과신·망각·미착수' 원인을 데이터에서 짚어라. 처방은 앱 기능(드릴 인출·문제풀이·복습)과 연결한 구체적 행동으로. 근거되면 "합격자 다수가 ~"처럼 인용하되 강사·교재 이름은 쓰지 마라. 각 소제목 2~4문장, 전체 350~500자, 진단서 문체(위로·응원 남발 금지).
${strat ? `\n[합격자 패턴 참고]\n${strat}` : ''}`;
      const { text } = await sendMessagesUnified({ apiKey, model, system, messages: [{ role: 'user', content: data }], maxTokens: 900, baseUrl });
      const next = { ...prose, [tab]: { text: (text || '').trim(), ts: Date.now() } };
      setProse(next); saveProse(next);
    } catch (e) { setProseErr(e.message || 'AI 총평 생성 실패'); } finally { setProseBusy(false); }
  };
  useEffect(() => { if (rep && !prose[tab] && !proseBusy && !(needsKey && !apiKey)) genProse(); /* eslint-disable-line */ }, [rep, tab]);

  const curProse = prose[tab];
  const idx = rep ? (tab === 1 ? rep.overall.stage1Index : rep.overall.stage2Index) : 0;
  const exp = rep && tab === 1 ? rep.overall.expected : null;
  const conf = subjectsArr.length ? subjectsArr.reduce((a, s) => a + s.confidence, 0) / subjectsArr.length : 0;
  const delta = Math.round(idx - 60);
  const verdict = idx >= 60 ? '합격선 도달 · 페이스 유지' : idx >= 50 ? '합격선 근접 · 약점 보완 필요' : idx >= 35 ? '기초 형성 단계 · 인출 훈련 집중' : '착수 단계';
  const dateStr = rep ? new Date(rep.generatedAt).toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' }) : '';
  const refNo = rep ? `AP-${tab}-${new Date(rep.generatedAt).toISOString().slice(0, 10).replace(/-/g, '')}` : '';

  const th = { fontFamily: SERIF, fontSize: '0.72rem', fontWeight: 700, color: INK[600], padding: '6px 6px', borderBottom: `1.5px solid ${INK[700]}`, whiteSpace: 'nowrap' };
  const td = { fontSize: '0.76rem', color: INK[800], padding: '7px 6px', borderBottom: `1px solid ${INK[200]}`, textAlign: 'center', ...NUM };

  return (
    <div className="report-desk" style={{ background: DESK, minHeight: '100dvh' }}>
      <header className="top-nav report-tools" style={{ borderBottom: '1px solid #e5e7eb', background: '#fff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {onBack ? <button className="back-btn" onClick={onBack}><ArrowLeft size={24} style={{ marginRight: 8 }} /><span style={{ fontSize: '0.95rem', fontWeight: 600 }}>홈</span></button> : <span />}
        <div style={{ display: 'flex', gap: 2 }}>
          <button onClick={genProse} disabled={proseBusy || !rep} title="AI 총평" style={toolBtn}><PenLine size={14} className={proseBusy ? 'spin' : ''} /> 총평</button>
          <button onClick={run} disabled={busy} title="다시 계산" style={toolBtn}><RefreshCw size={14} className={busy ? 'spin' : ''} /> 계산</button>
          <button onClick={() => window.print()} title="인쇄" style={toolBtn}><Printer size={14} /> 인쇄</button>
        </div>
      </header>

      <div style={{ padding: 'clamp(12px, 3vw, 34px) clamp(6px, 2vw, 22px)' }}>
        {/* 겹친 종이 그림자 */}
        <div style={{ position: 'relative', maxWidth: 920, margin: '0 auto' }}>
          <div aria-hidden className="report-stack" style={{ position: 'absolute', inset: 0, transform: 'translate(6px, 7px)', background: '#efeadd', border: `1px solid ${INK[300]}`, borderRadius: 2 }} />
          <div aria-hidden className="report-stack" style={{ position: 'absolute', inset: 0, transform: 'translate(3px, 3.5px)', background: '#f4efe3', border: `1px solid ${INK[300]}`, borderRadius: 2 }} />
          <article className="report-sheet" style={{ position: 'relative', background: PAPER, border: `1px solid ${INK[300]}`, borderRadius: 2, boxShadow: '0 1px 2px rgba(0,0,0,0.10), 0 14px 34px rgba(0,0,0,0.16)', padding: 'clamp(26px, 5vw, 58px) clamp(22px, 5vw, 60px)', color: INK[800] }}>

            {/* 레터헤드 */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, flexWrap: 'wrap' }}>
              <div style={{ display: 'flex', gap: 13, alignItems: 'center' }}>
                <div style={{ width: 42, height: 42, border: `1.5px solid ${INK[800]}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: SERIF, fontSize: '1.3rem', fontWeight: 800, color: INK[900], flexShrink: 0 }}>評</div>
                <div>
                  <div style={{ fontFamily: SERIF, fontSize: '0.7rem', fontWeight: 700, color: INK[500], letterSpacing: '0.22em' }}>감정평가사 제{tab === 1 ? '1' : '2'}차 시험 대비</div>
                  <h1 style={{ fontFamily: SERIF, fontSize: '1.85rem', fontWeight: 800, color: INK[900], margin: '2px 0 0', letterSpacing: '0.02em' }}>학습 진단 리포트</h1>
                </div>
              </div>
              <div style={{ textAlign: 'right', fontFamily: SERIF, fontSize: '0.72rem', color: INK[500], lineHeight: 1.75, ...NUM }}>
                <div>문서번호 {refNo}</div>
                <div>발행일 {dateStr}</div>
                <div>측정 신뢰도 {Math.round(conf * 100)}%</div>
              </div>
            </div>
            <div style={{ borderTop: `2px solid ${INK[900]}`, marginTop: 10 }} />
            <div style={{ borderTop: `1px solid ${INK[500]}`, marginTop: 2 }} />

            {/* 🩺 과목별 학습 진단 — 같은 시트 안, 종합 리포트 위에 */}
            <SubjectDiagnostic ctx={ctx} onReview={onReview} onOpen={onOpen} sel={sel} onSel={setSel} />

            {isOverview && !rep && <div style={{ padding: 70, textAlign: 'center', color: INK[400], fontFamily: SERIF }}>실력을 계산하는 중…</div>}

            {isOverview && rep && (
              <>
                <div style={{ fontFamily: SERIF, fontSize: '0.78rem', fontWeight: 800, color: INK[500], marginTop: 16 }}>제{tab}차 — 종합 리포트 <span style={{ fontWeight: 600, color: INK[400], fontSize: '0.66rem' }}>(위 선택바에서 과목·차수를 고르면 함께 바뀝니다)</span></div>

                {/* Ⅰ. 종합 소견 */}
                <DocSection no={ROMAN[0]} title="종합 소견">
                  <div style={{ display: 'flex', gap: 26, flexWrap: 'wrap', alignItems: 'flex-start' }}>
                    <div style={{ flex: '1 1 320px', minWidth: 260 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                        <PenLine size={12} color={INK[500]} />
                        <span style={{ fontFamily: SERIF, fontSize: '0.72rem', fontWeight: 700, color: INK[500], letterSpacing: '0.05em' }}>담당 AI 진단관 소견</span>
                        {curProse && <button onClick={genProse} disabled={proseBusy} style={{ marginLeft: 'auto', border: 'none', background: 'none', color: INK[400], fontSize: '0.68rem', fontFamily: SERIF, cursor: 'pointer' }}>다시 쓰기</button>}
                      </div>
                      {proseBusy && <div style={{ fontFamily: SERIF, fontSize: '0.84rem', color: INK[400], padding: '8px 0' }}>진단관이 소견을 작성하는 중…</div>}
                      {!proseBusy && proseErr && <div style={{ fontFamily: SERIF, fontSize: '0.8rem', color: INK[500], background: INK[50], padding: '10px 12px', border: `1px solid ${INK[200]}`, lineHeight: 1.6 }}>{proseErr}</div>}
                      {!proseBusy && !proseErr && curProse && <ProseBody text={curProse.text} />}
                      {!proseBusy && !proseErr && !curProse && (
                        <button onClick={genProse} style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontFamily: SERIF, border: `1px solid ${INK[400]}`, background: 'none', color: INK[700], fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer', padding: '9px 15px' }}><PenLine size={14} /> AI 소견 작성</button>
                      )}
                    </div>
                    {/* 그림: 종합 지수 */}
                    <figure style={{ flex: '0 0 auto', width: 190, margin: 0, textAlign: 'center' }}>
                      <div style={{ border: `1px solid ${INK[300]}`, padding: '10px 8px 6px', background: '#fff' }}>
                        <Gauge value={idx} />
                        <div style={{ display: 'flex', borderTop: `1px solid ${INK[200]}`, marginTop: 4, paddingTop: 7 }}>
                          {exp && <div style={{ flex: 1, borderRight: `1px solid ${INK[200]}` }}><div style={{ fontFamily: SERIF, fontSize: '0.58rem', color: INK[400] }}>예상점수</div><div style={{ fontFamily: SERIF, fontSize: '0.9rem', fontWeight: 800, color: INK[900], ...NUM }}>{exp.lo}–{exp.hi}</div></div>}
                          <div style={{ flex: 1 }}><div style={{ fontFamily: SERIF, fontSize: '0.58rem', color: INK[400] }}>합격선 대비</div><div style={{ fontFamily: SERIF, fontSize: '0.9rem', fontWeight: 800, color: INK[900], ...NUM }}>{delta >= 0 ? `+${delta}` : delta}</div></div>
                        </div>
                      </div>
                      <figcaption style={{ fontFamily: SERIF, fontSize: '0.64rem', color: INK[500], marginTop: 5 }}>〈그림 1〉 종합 실력 지수 · {verdict}</figcaption>
                    </figure>
                  </div>
                </DocSection>

                {/* Ⅱ. 과목별 정량 지표 */}
                <DocSection no={ROMAN[1]} title="과목별 정량 지표">
                  {subjectsArr.length === 0 ? (
                    <div style={{ fontFamily: SERIF, color: INK[400], fontSize: '0.84rem', padding: '8px 0' }}>이 단계는 아직 학습 기록이 없습니다.</div>
                  ) : (
                    <>
                      <div style={{ overflowX: 'auto' }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse', minWidth: 480 }}>
                          <thead>
                            <tr>
                              <th style={{ ...th, textAlign: 'left' }}>과목</th>
                              <th style={th}>실력</th><th style={th}>완성도</th><th style={th}>이해</th><th style={th}>인출</th><th style={th}>적용</th><th style={th}>기출</th>
                              <th style={{ ...th, textAlign: 'left' }}>비고</th>
                            </tr>
                          </thead>
                          <tbody>
                            {subjectsArr.map((s) => (
                              <tr key={s.id}>
                                <td style={{ ...td, textAlign: 'left', fontFamily: SERIF, fontWeight: 700, color: INK[900] }}>{s.short}</td>
                                <td style={{ ...td, fontWeight: 800, color: INK[900] }}>{Math.round(s.score)}</td>
                                <td style={td}>{Math.round(s.completion)}%</td>
                                <td style={td}>{rn(s.axes.U)}</td><td style={td}>{rn(s.axes.R)}</td><td style={td}>{rn(s.axes.A)}</td>
                                <td style={td}>{s.quizN || '–'}</td>
                                <td style={{ ...td, textAlign: 'left', color: INK[600], fontSize: '0.72rem' }}>{subjectRemark(s)}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                      <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap', marginTop: 14, justifyContent: 'center' }}>
                        {subjectsArr.map((s) => (
                          <figure key={s.id} style={{ margin: 0, textAlign: 'center' }}>
                            <Radar U={s.axes.U} R={s.axes.R} A={s.axes.A} />
                            <figcaption style={{ fontFamily: SERIF, fontSize: '0.64rem', color: INK[600], marginTop: -2 }}>{s.short}</figcaption>
                          </figure>
                        ))}
                      </div>
                      <div style={{ fontFamily: SERIF, fontSize: '0.62rem', color: INK[400], marginTop: 6 }}>〈그림 2〉 과목별 3축 프로필(이해·인출·적용)</div>
                    </>
                  )}
                </DocSection>

                {/* Ⅲ. 우선 학습 과제 */}
                {weakGlobal.length > 0 && (
                  <DocSection no={ROMAN[2]} title="우선 학습 과제">
                    <div style={{ fontFamily: SERIF, fontSize: '0.72rem', color: INK[500], marginBottom: 8 }}>시험 레버리지(빈출 × 취약)가 큰 순. 항목을 누르면 해당 드릴로 이동합니다.</div>
                    <ol style={{ margin: 0, padding: 0, listStyle: 'none', counterReset: 'wk' }}>
                      {weakGlobal.map((w) => {
                        const st = STATUS[w.status];
                        return (
                          <li key={w.sid + w.id}>
                            <button onClick={() => onGoDrill && onGoDrill(w.sid, { id: w.id, title: w.title })}
                              style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 9, textAlign: 'left', background: 'none', border: 'none', borderBottom: `1px solid ${INK[200]}`, padding: '8px 2px', cursor: 'pointer' }}>
                              <span style={{ fontFamily: SERIF, fontSize: '0.72rem', fontWeight: 700, color: INK[400], width: 32, flexShrink: 0, ...NUM }}>{w.sshort}</span>
                              <Grade tier={w.tier} />
                              <span style={{ flex: 1, minWidth: 0, fontFamily: SERIF, fontSize: '0.82rem', fontWeight: 600, color: INK[800], overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{w.title}</span>
                              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, flexShrink: 0 }}>
                                <span style={{ width: 6, height: 6, borderRadius: 999, background: st.c, border: `1px solid ${INK[400]}` }} />
                                <span style={{ fontFamily: SERIF, fontSize: '0.68rem', fontWeight: 700, color: INK[500], ...NUM }}>{w.M == null ? '미착수' : `${st.label} ${Math.round(w.M)}`}</span>
                              </span>
                              <ChevronRight size={14} color={INK[400]} style={{ flexShrink: 0 }} />
                            </button>
                          </li>
                        );
                      })}
                    </ol>
                  </DocSection>
                )}

                {/* Ⅳ. 분석 방법 및 유의사항 */}
                <DocSection no={ROMAN[3]} title="분석 방법 및 유의사항">
                  {hist.length >= 2 && (
                    <figure style={{ margin: '0 0 14px' }}>
                      <div style={{ border: `1px solid ${INK[300]}`, padding: '10px 12px', background: '#fff' }}><Spark data={hist.map((h) => (tab === 1 ? h.i1 : h.i2) || 0)} /></div>
                      <figcaption style={{ fontFamily: SERIF, fontSize: '0.62rem', color: INK[500], marginTop: 4 }}>〈그림 3〉 실력 지수 추이(최근 {hist.length}회)</figcaption>
                    </figure>
                  )}
                  <div style={{ columnWidth: 250, columnGap: 26 }}>
                    {METHODS.map(([t, d], i) => (
                      <div key={i} style={{ breakInside: 'avoid', marginBottom: 8, fontFamily: SERIF }}>
                        <span style={{ fontSize: '0.74rem', fontWeight: 800, color: INK[700] }}>{i + 1}. {t} </span>
                        <span style={{ fontSize: '0.73rem', color: INK[500], lineHeight: 1.5 }}>{d}</span>
                      </div>
                    ))}
                  </div>
                </DocSection>

                {/* 푸터 */}
                <div style={{ marginTop: 30, borderTop: `1px solid ${INK[300]}`, paddingTop: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', gap: 12, flexWrap: 'wrap' }}>
                  <div style={{ fontFamily: SERIF, fontSize: '0.66rem', color: INK[500], lineHeight: 1.6, maxWidth: 560 }}>
                    본 리포트는 귀하의 AI 학습·드릴·문제풀이 기록에 근거해 자동 생성되었습니다. 예상 점수·소견은 <b style={{ color: INK[700] }}>추정치</b>이며, 학습 기록이 쌓일수록 정확해집니다.
                  </div>
                  <div style={{ textAlign: 'center', fontFamily: SERIF, color: INK[500] }}>
                    <div style={{ fontSize: '1.05rem', fontWeight: 800, color: INK[800], letterSpacing: '0.05em', borderBottom: `1px solid ${INK[400]}`, paddingBottom: 2 }}>AI 학습 진단</div>
                    <div style={{ fontSize: '0.6rem', marginTop: 3, ...NUM }}>{refNo}</div>
                  </div>
                </div>
              </>
            )}
          </article>
        </div>
      </div>
    </div>
  );
}

const toolBtn = { display: 'flex', alignItems: 'center', gap: 4, border: 'none', background: 'none', color: INK[600], fontWeight: 600, fontSize: '0.76rem', cursor: 'pointer', padding: '8px 10px' };
