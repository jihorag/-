// 🩺 과목별 학습 진단 — 종합 리포트와 동일한 A4 종이(명조·먹색) 양식.
// "약점 → 합격자 처방 → 지금 할 일" + 시각 그래프(반원 게이지·레이더) + AI 맞춤 소견.
// 처방·소견은 합격수기 78건(pass_insights) 근거. 1차: 기출 정오 분해 / 2차: 논술형 전략.
import { useMemo, useState } from 'react';
import { SUBJECTS, getPrefs } from './aiLearningStore';
import { sendMessagesUnified } from './aiProviders';
import { resolveCall } from './modelRegistry';
import ParsedText from './ParsedText';
import { buildSubjectDiag } from './subjectDiag';
import { SERIF, INK, NUM, DocSection } from './reportTheme';

const S1 = SUBJECTS.filter((s) => s.stage === 1);
const S2 = SUBJECTS.filter((s) => s.stage === 2);
const ALL_SUBS = [...S1, ...S2];
const isS2 = (id) => S2.some((s) => s.id === id);
const pct = (a) => (a == null ? null : Math.round(a * 100));

// 합격수기 78건에서 증류한 과목별 처방(pass_insights.json 근거).
const RX = {
  economics: { stratShort: '문풀 7~10회독·계산 반복', strat: '강의는 1회독만 하고 곧바로 문풀로 — 문제를 많이 가져갈수록 변형에 강해집니다. 계산은 반복으로 손이 기억하게, 실전처럼 시간 재며 푸세요.', pitfall: '전공 자만으로 기본을 건너뛰면 오히려 최저점. 시간압박이 크니 평소 시간 체크 필수.',
    tips: ['문풀 위주 다회독', '계산 반복으로 속도', '실전처럼 시간 재기', '기본강의 1회독 필수'],
    dim: { '계산': '정형 계산 유형을 반복해 속도·정확도를 확보하세요. 시간을 재며 푸는 게 합격자 공통.', '그래프·도해': '수요·공급 곡선의 이동·균형 변화를 그림으로 반복 정리하세요.', '개념·이론': '읽기보다 문제로 개념을 굳히세요 — 강의 1회독 후 곧바로 문풀 전환.' } },
  accounting: { stratShort: '빈출 선택집중·기출 반복', strat: '기출을 무한반복하되 원가·재무 등 빈출에 선택과 집중, 가성비 낮은 파트(IFRS·리스)는 과감히 버리세요.', pitfall: '1차 최다 과락 과목. 기출만 반복하면 새 문제 대응이 약해지니 기본기도 챙기세요.',
    tips: ['기본강의부터(노베이스)', '빈출 파트 선택과 집중', '말문제 녹음 반복', '가성비 낮은 단원 버리기'],
    dim: { '계산·분개': '빈출 계산 유형을 무한반복으로 체화하세요. 저빈출은 버리고 시간을 빈출에.', '개념·이론': '말(이론)문제는 육성 녹음해 반복 청취 — 합격자는 30회독 수준으로 굳혔습니다.' } },
  civil: { stratShort: '기본강의+선지·조문 암기', strat: '기본강의는 반드시(패스가 패착), 이후 기출 지문·선지를 반복해 오답을 눈에 바르듯 체화하세요. 조문 암기 병행.', pitfall: '기본강의를 건너뛰거나 조문 암기를 소홀히 하는 것이 대표 실패 원인.',
    tips: ['기본강의 필수', '선지 반복 암기', '조문집 병행', '베이스 있으면 전략과목화'],
    dim: { '판례': '판례 지문·선지를 반복해 결론을 즉시 떠올리도록 암기하세요.', '조문·개념': '조문·요약집을 반복 암기(합격자 요약집 10회독)하고 선지를 반복하세요.' } },
  realestate: { stratShort: '요약집+기출 고효율', strat: '강의노트+기출 1~2회독만으로 평균을 견인(80+)하는 전략과목. 투입은 최소로, 직전 1회독으로도 방어됩니다.', pitfall: '쉽다고 손 놓으면 실점, 반대로 과투입은 비효율. 딱 요약집+기출만.',
    tips: ['평균 견인용 전략과목', '요약집+기출 위주', '직전 1회독 방어', '과투입 금지'],
    dim: { '계산': '요약집+기출 회독으로 계산 유형만 빠르게 굳히세요(투입 최소).', '개념·이론': '강의노트+기출 회독으로 빠르게 고득점 — 평균 견인용 전략과목.' } },
  law: { stratShort: '조문·판례 암기·빈출 집중', strat: '조문·판례 암기가 핵심. 요약서 다회독으로 국계법·감정평가사법 등 빈출에 집중하고 저빈출(건축법 등)은 버리세요. 암기과목이라 일찍 시작할수록 유리.', pitfall: '늦게 시작하면 암기 부족으로 실점. 고득점 사례는 일찍·많이 암기한 경우.',
    tips: ['조문 암기 필수', '판례 정리', '저빈출 버리고 빈출 집중', '암기과목이라 일찍 시작'],
    dim: { '조문암기': '조문을 요약서로 반복 암기하고 A급(빈출)부터 자투리 시간에 인출하세요.', '판례': '판례의 결론·번호까지 정리해 스스로 인출하세요.', '계산': '계산은 빈출 유형만 골라 반복하세요.', '개념': '빈출 개념 위주로 정리하고 저빈출은 과감히 버리세요.' } },
  appraisal_practice: { stratShort: '매일 100점 양치기·채점평 족보화', strat: "매일 100~200점씩 풀되 '풀이보다 복습'이 생명 — 채점평을 답안지에 옮겨 득점·실점 포인트를 족보화하고 주2~3회 반복하면 계단식 상승. 유형별 목차집을 만들어 문제 보자마자 목차가 나오게, 계산도 멘트·순서를 암기하세요.", pitfall: '가장 흔한 과락 — 유형 미경험·시간배분 미숙·완주 실패·양치기만 하고 복습 소홀. 반드시 프린트로 시간 내 실전 연습.',
    tips: ['매일 아침 100점', '채점평을 답안지에 옮겨 족보화', '유형별 목차집 통암기', '완주·시간엄수', '프린트로 실전 연습'] },
  appraisal_theory: { stratShort: '목차 암기·기본서 회독·백지쓰기', strat: "목차 암기가 관건('목차만 외워도 70%'). 주제별 정형 구성을 통암기하고 기출을 백지에 직접 써보며 모범답안과 비교(첨삭)하세요. 서브 요약보다 기본서 회독 우선, 각론은 A급(수익환원·최유효이용)에 시간을 몰기.", pitfall: '각론 암기 부족이 과락 직결. 예시답안 달달 암기는 변형에 무너집니다.',
    tips: ['의의 주요 10개 정확히', '목차·두문자 통암기', '기본서 회독 우선', '각론 A급 집중', '기출 백지쓰기+첨삭'] },
  appraisal_law: { stratShort: '법전·판례 매일 암기·목차 우선', strat: "암기가 알파이자 오메가. 법전을 매일 조문 암기(토지보상법 1~92조), 판례는 취지·논거·번호까지 두문자로. '목차=답안'이라 논점 찾기가 먼저이고, '일반론-판례-검토-사안포섭' 논리로 소결을 풍부히 쓰세요.", pitfall: "가장 흔한 실패는 '늦은 시작'. 조문을 서브 암기로 대체하려다 못 쓰고, 예시답안 암기만 하면 사안 포섭이 약합니다.",
    tips: ['법전 매일 조문 암기', '판례 번호·논거 두문자', '목차 우선(논점 찾기)', '행정법 기초 먼저', 'A급부터 누적 암기'] },
};
const rxDim = (sid, dim) => (RX[sid] && RX[sid].dim && RX[sid].dim[dim]) || '';

// 과목별 빈출 A급 논점 — AI 프롬프트에 주입해 구체 논점을 짚게 한다.
const HOT = {
  economics: ['수요·공급과 탄력성', '소비자균형(무차별곡선·예산선)', '생산·비용함수', '시장구조(독점·과점)', '조세귀착·후생손실', 'IS-LM·총수요총공급', '화폐·통화승수·물가', '국제수지·환율'],
  accounting: ['재고자산', '유형·무형자산', '금융자산·사채', '수익인식', '원가배부·종합원가', 'CVP·표준원가', '현금흐름표'],
  civil: ['법률행위·의사표시', '대리·무효취소', '물권변동·점유', '소유권·용익물권', '담보물권(저당·유치)', '채무불이행·계약', '부당이득·불법행위'],
  realestate: ['부동산 특성·개념', '수요·공급·탄력성', '감정평가 3방식', '부동산정책·시장', '투자분석(NPV·IRR)', '지대·입지이론'],
  law: ['국토계획법(용도지역·지구)', '감정평가법·규칙', '부동산공시법(공시지가)', '토지보상법(보상평가)', '부동산등기법·지적'],
};

const clamp = (x) => Math.max(0, Math.min(100, x || 0));

// ── 반원 게이지(정답률) ──
function Gauge({ value, label, size = 128 }) {
  const r = size / 2 - 12, cx = size / 2, cy = size / 2, a0 = Math.PI, a1 = 0;
  const v = clamp(value); const ang = a0 + (a1 - a0) * (v / 100);
  const pt = (a, rad) => [cx + rad * Math.cos(a), cy + rad * Math.sin(a)];
  const arc = (from, to, rad) => { const [x0, y0] = pt(from, rad), [x1, y1] = pt(to, rad); const large = Math.abs(to - from) > Math.PI ? 1 : 0; return `M ${x0} ${y0} A ${rad} ${rad} 0 ${large} 1 ${x1} ${y1}`; };
  return (
    <svg width={size} height={size / 2 + 18} viewBox={`0 0 ${size} ${size / 2 + 18}`} style={{ flexShrink: 0 }}>
      <path d={arc(a0, a1, r)} fill="none" stroke={INK[200]} strokeWidth={9} />
      <path d={arc(a0, ang, r)} fill="none" stroke={INK[800]} strokeWidth={9} />
      <text x={cx} y={cy - 1} textAnchor="middle" fontSize={27} fontWeight={700} fill={INK[900]} fontFamily={SERIF}>{Math.round(v)}</text>
      <text x={cx} y={cy + 13} textAnchor="middle" fontSize={9} fill={INK[400]} fontFamily={SERIF}>{label || '정답률'}</text>
    </svg>
  );
}

// ── N축 레이더 ──
function Radar({ axes, size = 132 }) {
  const cx = size / 2, cy = size / 2, rad = size / 2 - 24, N = axes.length || 1;
  const ang = (i) => -Math.PI / 2 + (2 * Math.PI * i) / N;
  const pt = (a, rr) => [cx + rr * Math.cos(a), cy + rr * Math.sin(a)];
  const poly = axes.map((a, i) => pt(ang(i), rad * Math.max(0.03, clamp(a.val) / 100)).join(',')).join(' ');
  const ring = (f) => axes.map((a, i) => pt(ang(i), rad * f).join(',')).join(' ');
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ flexShrink: 0 }}>
      {[0.5, 1].map((f, i) => <polygon key={i} points={ring(f)} fill="none" stroke={INK[200]} strokeWidth={0.8} />)}
      {axes.map((a, i) => { const [x, y] = pt(ang(i), rad); return <line key={i} x1={cx} y1={cy} x2={x} y2={y} stroke={INK[200]} strokeWidth={0.8} />; })}
      <polygon points={poly} fill="rgba(38,35,27,0.13)" stroke={INK[700]} strokeWidth={1.3} />
      {axes.map((a, i) => { const [lx, ly] = pt(ang(i), rad + 12); return <text key={i} x={lx} y={ly + 3} textAnchor="middle" fontSize={7.5} fontWeight={700} fill={INK[500]}>{a.label}</text>; })}
    </svg>
  );
}

function SubHead({ children, hint }) {
  return (
    <div style={{ fontFamily: SERIF, fontSize: '0.86rem', fontWeight: 800, color: INK[900], marginTop: 18, marginBottom: 6 }}>
      {children}{hint ? <span style={{ fontSize: '0.62rem', fontWeight: 600, color: INK[400], marginLeft: 7 }}>{hint}</span> : null}
    </div>
  );
}

function FocusCard({ n, kind, label, answered, total, acc, untouched, rx, actLabel, onAct }) {
  const p = pct(acc);
  return (
    <div style={{ display: 'flex', gap: 10, padding: '10px 0', borderTop: `1px solid ${INK[200]}` }}>
      <div style={{ flexShrink: 0, width: 20, height: 20, borderRadius: '50%', border: `1.5px solid ${INK[800]}`, color: INK[900], fontFamily: SERIF, fontWeight: 800, fontSize: '0.72rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{n}</div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 7, flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.56rem', fontWeight: 800, color: INK[500], border: `1px solid ${INK[300]}`, padding: '0 4px' }}>{kind}</span>
          <span style={{ fontFamily: SERIF, fontSize: '0.9rem', fontWeight: 800, color: INK[900] }}>{label}</span>
          <span style={{ fontSize: '0.78rem', fontWeight: 700, color: untouched ? INK[400] : INK[700], ...NUM }}>{answered ? `${p}%` : '미학습'}</span>
          <span style={{ fontSize: '0.62rem', color: INK[400], ...NUM }}>{answered}/{total}</span>
        </div>
        {rx ? <div style={{ fontSize: '0.76rem', color: INK[700], lineHeight: 1.6, marginTop: 3 }}><b style={{ color: INK[800] }}>합격자 </b>{rx}</div> : null}
      </div>
      {onAct ? <button onClick={onAct} style={{ flexShrink: 0, alignSelf: 'center', fontFamily: SERIF, fontSize: '0.72rem', fontWeight: 700, color: INK[800], background: INK[50], border: `1px solid ${INK[400]}`, borderRadius: 2, padding: '5px 11px', cursor: 'pointer', whiteSpace: 'nowrap' }}>{actLabel} ›</button> : null}
    </div>
  );
}

const inkBtn = { fontFamily: SERIF, fontSize: '0.74rem', fontWeight: 700, color: INK[800], background: INK[50], border: `1px solid ${INK[400]}`, borderRadius: 2, padding: '6px 13px', cursor: 'pointer' };

// 형광펜 색(명조 리포트에 어울리는 옅은 노랑)
const HL = '#f3e3a3';
// 인라인 리치 렌더 — **굵게**, ==형광펜==. 표시 없으면 실측 수치·앱기능을 자동 강조.
function renderInline(raw, keyBase) {
  let t = raw || '';
  if (/==|\*\*/.test(t)) {
    t = t.replace(/\*\*([^*]+)\*\*/g, '⟦B⟧$1⟦/B⟧').replace(/==([^=]+)==/g, '⟦H⟧$1⟦/H⟧');
  } else {
    t = t.replace(/(\d+\s?%|\d+\s?문항|저빈출|미학습|과락)/g, '⟦H⟧$1⟦/H⟧');
    t = t.replace(/(AI학습 이론 모드|AI학습 심화 모드|AI학습 진단 모드|문제풀이 모드|드릴 인출|백지쓰기|채점평|목차집|단권화|AI학습|문제풀이|드릴)/g, '⟦B⟧$1⟦/B⟧');
  }
  const parts = t.split(/(⟦B⟧|⟦\/B⟧|⟦H⟧|⟦\/H⟧)/);
  let b = false, h = false; const out = [];
  parts.forEach((p, i) => {
    if (p === '⟦B⟧') { b = true; return; } if (p === '⟦/B⟧') { b = false; return; }
    if (p === '⟦H⟧') { h = true; return; } if (p === '⟦/H⟧') { h = false; return; }
    if (!p) return;
    out.push(<span key={`${keyBase}-${i}`} style={{ fontWeight: b ? 800 : undefined, color: b ? INK[900] : undefined, background: h ? HL : undefined, padding: h ? '0 2px' : undefined, borderRadius: h ? 2 : undefined }}>{p}</span>);
  });
  return out;
}

// ## 소제목 마크다운 → 구역별 박스(좌측 먹색 바 + 옅은 종이) + 리치 인라인
function ProseBody({ text }) {
  const parts = (text || '').split(/\n(?=##\s)/).map((s) => s.trim()).filter(Boolean);
  return (
    <div style={{ fontFamily: SERIF }}>
      {parts.map((p, i) => {
        const m = p.match(/^##\s*(.+?)\s*\n([\s\S]*)$/) || p.match(/^##\s*(.+?)\s*$/);
        const h = m ? m[1].trim() : null; const body = (m ? (m[2] || '') : p).trim();
        const paras = body.split(/\n+/).map((s) => s.trim()).filter(Boolean);
        return (
          <div key={i} style={{ border: `1px solid ${INK[200]}`, borderLeft: `3px solid ${INK[700]}`, borderRadius: 3, padding: '8px 12px 9px', marginBottom: 9, background: INK[50] }}>
            {h && <div style={{ fontSize: '0.78rem', fontWeight: 800, color: INK[900], marginBottom: 4 }}>{h}</div>}
            {paras.map((pa, j) => {
              const bullet = /^[-·•]\s+/.test(pa); const clean = pa.replace(/^[-·•]\s+/, '');
              return (
                <div key={j} style={{ fontSize: '0.82rem', color: INK[700], lineHeight: 1.8, marginBottom: 2, display: 'flex', gap: 6 }}>
                  {bullet && <span style={{ color: INK[500], flexShrink: 0 }}>·</span>}
                  <span style={{ flex: 1 }}>{renderInline(clean, `${i}-${j}`)}</span>
                </div>
              );
            })}
          </div>
        );
      })}
    </div>
  );
}

// 정보 박스 / 경고(흔한 실패) 박스
function InfoBox({ title, children }) {
  return (
    <div style={{ border: `1px solid ${INK[200]}`, borderLeft: `3px solid ${INK[600]}`, borderRadius: 3, padding: '8px 12px', marginTop: 8, background: INK[50], fontFamily: SERIF }}>
      {title && <div style={{ fontSize: '0.72rem', fontWeight: 800, color: INK[900], marginBottom: 3 }}>{title}</div>}
      <div style={{ fontSize: '0.82rem', color: INK[800], lineHeight: 1.75 }}>{children}</div>
    </div>
  );
}
function WarnBox({ children }) {
  return (
    <div style={{ border: '1px solid #e6d6a6', borderLeft: '3px solid #c99a2e', borderRadius: 3, padding: '7px 12px', marginTop: 7, background: '#fbf3df', fontFamily: SERIF }}>
      <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#8a6a1e', marginBottom: 2 }}>⚠ 흔한 실패</div>
      <div style={{ fontSize: '0.78rem', color: '#6b5a2e', lineHeight: 1.65 }}>{children}</div>
    </div>
  );
}

// 과목별 AI 맞춤 진단 프롬프트(1차·2차) — 실측 데이터 + 합격수기 근거.
function buildPrompt(sid, diag, ctx, essay) {
  const rx = RX[sid] || {};
  if (isS2(sid)) {
    const s = S2.find((x) => x.id === sid);
    const nUnits = ((ctx && ctx.leavesBySubject && ctx.leavesBySubject[sid]) || []).length;
    const user = `[${s?.title} — 상태] 2차 논술·답안형(기출 정오 데이터 없음). 논점(단원) ${nUnits}개. 답안 연습 ${essay.n}개${essay.avg != null ? `(자기채점 평균 ${essay.avg}점)` : ''}.`;
    const system = `너는 감정평가사 2차 ${s?.title} 진단 전문가다. 2차는 논술·답안형이라 기출 정오 데이터가 없으니 합격 전략과 답안 연습 상태를 근거로 맞춤 진단을 한국어로 써라.\n[이 과목 특성·합격전략(합격수기 78건)] ${rx.strat || ''} (흔한 실패: ${rx.pitfall || ''}) 팁: ${(rx.tips || []).join(', ')}\n[출력] 마크다운. '## '로 아래 5개 소제목만, 순서대로: ## 진단 / ## 강점과 약점 / ## 답안 작성 전략 / ## 우선순위 처방 / ## 이번 주 실행\n[규칙] ${s?.title}의 답안작성 특성(목차 암기·법전/판례 암기·채점평 복습·백지쓰기 등)을 구체적으로 짚어라. 처방은 앱 기능(2차 논술 답안작성·AI학습 논점/양식/답안 모드·드릴 인출)과 합격자 방법으로 연결. 각 소제목 2~4문장, 전체 550~750자. 진단서 문체(응원·군더더기 금지).\n[강조 표기] 핵심 용어·앱기능은 **굵게**, 각 소제목에서 가장 중요한 한 구절만 ==형광펜==으로 감싸라(소제목당 1~2곳, 과용 금지).`;
    return { system, user };
  }
  const d = diag[sid]; if (!d) return null;
  const user = (() => {
    const L = [`[${d.title} — 실측 데이터]`];
    if (!d.answered) L.push(`전체 미학습(기출 ${d.total}문항 미풀이). 전 영역 최저.`);
    else {
      L.push(`정답률 ${Math.round(d.acc * 100)}% (푼 ${d.answered}/${d.total}).`);
      L.push('특성별(문항수=빈출): ' + d.byDim.map((b) => `${b.key} ${b.total}문항 ${b.answered ? Math.round(b.acc * 100) + '%' : '미학습'}`).join(', '));
      if (d.byDiv && d.byDiv.length) L.push('분야별(문항수=빈출): ' + d.byDiv.map((b) => `${b.key} ${b.total}문항 ${b.answered ? Math.round(b.acc * 100) + '%' : '미학습'}`).join(', '));
      const wa = d.byArea.slice(0, 5).map((b) => `${b.key} ${b.total}문항 ${b.answered ? Math.round(b.acc * 100) + '%' : '미학습'}`);
      if (wa.length) L.push('약점 단원: ' + wa.join(', '));
    }
    return L.join('\n');
  })();
  const hot = HOT[sid] || [];
  const system = `너는 감정평가사 1차 ${d.title} 진단 전문가다. 아래 '실측 데이터'만 근거로 이 과목 맞춤 진단을 한국어로 써라.\n[이 과목 특성·합격전략(합격수기 78건)] ${rx.stratShort || ''} — ${rx.strat || ''} (흔한 실패: ${rx.pitfall || ''})${hot.length ? `\n[빈출 A급 논점(우선 공략)] ${hot.join(', ')}` : ''}\n[중요·빈출 가중] 데이터의 '문항수'가 곧 출제 빈출(비중)이다. 문항수 많은 분야·특성·단원을 우선 공략하고, 문항수 적은 분야(예: 재정학·국제경제처럼 소수 문항)는 '저빈출·가성비 낮음'으로 후순위·최소화하라고 명시하라(합격수기의 '빈출 집중·저빈출 버리기' 원칙).\n[출력] 마크다운. '## '로 아래 5개 소제목만, 순서대로: ## 진단 / ## 강점과 약점 / ## 유형·특성별 전략 / ## 우선순위 처방 / ## 이번 주 실행\n[규칙] 데이터에 없는 사실 창작 금지. ${d.title}의 문제 특성(계산·그래프·판례·조문·개념 등)과 분야별(예: 미시/거시), 실측 약점 수치를 구체 인용. '유형·특성별 전략'에서는 계산/그래프/개념 등 특성마다 다른 공부법을 각각 짚어라. '우선순위 처방'은 빈출(문항수)이 큰 것부터 순서를 매기고 위 '빈출 A급 논점'을 이름 그대로 배치하라. 앱 기능(드릴 인출·문제풀이·AI학습 이론/심화/진단 모드)과 합격자 방법으로 연결. 각 소제목 2~4문장, 전체 600~800자. 진단서 문체(응원·군더더기 금지). 미학습이면 '어디부터 어떻게 시작'을 콕 집어라.\n[강조 표기] 핵심 용어·앱기능은 **굵게**, 각 소제목에서 가장 중요한 한 구절만 ==형광펜==으로 감싸라(소제목당 1~2곳, 과용 금지).`;
  return { system, user };
}

const AI_KEY = 'subjdiag-ai-v1';
const loadAi = () => { try { return JSON.parse(localStorage.getItem(AI_KEY) || '{}') || {}; } catch { return {}; } };

export default function SubjectDiagnostic({ ctx, onReview, onOpen, sel = 'all', onSel }) {
  const diag = useMemo(() => buildSubjectDiag(ctx), [ctx && ctx.classifiedList, ctx && ctx.progress]);
  const setSel = onSel || (() => {});
  const [ai, setAi] = useState(loadAi);
  const [aiProg, setAiProg] = useState(null); // null | { done, total, cur }
  const [aiErr, setAiErr] = useState('');
  const [excl, setExcl] = useState(() => new Set()); // 재생성에서 제외할 과목
  const toggleExcl = (id) => setExcl((prev) => { const n = new Set(prev); if (n.has(id)) n.delete(id); else n.add(id); return n; });
  const inclCount = ALL_SUBS.length - excl.size;
  const essay = useMemo(() => {
    let ep = {}; try { ep = JSON.parse(localStorage.getItem('quiz-essay-progress') || '{}') || {}; } catch { ep = {}; }
    const entries = Object.values(ep).filter((e) => e && e.attempts && e.attempts.length);
    const scores = entries.map((e) => e.attempts[e.attempts.length - 1].selfScore).filter((x) => typeof x === 'number');
    return { n: entries.length, avg: scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null };
  }, []);

  // 🖊 전과목 AI 진단 (재)생성 — 8과목을 순차 생성, 완료되는 대로 채움.
  const genAll = async () => {
    if (aiProg) return;
    const model = (getPrefs() && getPrefs().model) || 'moonshot:kimi-k2.6';
    const { apiKey, baseUrl, needsKey } = resolveCall(model);
    if (needsKey && !apiKey) { setAiErr('AI 진단은 클라우드 모델 키가 필요해요 — AI 학습 ⚙️ 설정에서 등록하세요.'); return; }
    setAiErr('');
    const subs = ALL_SUBS.map((s) => s.id).filter((id) => !excl.has(id)); // 체크 해제된 과목은 재생성 제외
    if (!subs.length) { setAiErr('재생성할 과목을 하나 이상 체크하세요.'); return; }
    const acc = { ...loadAi() };
    for (let i = 0; i < subs.length; i++) {
      const sid = subs[i];
      const meta = SUBJECTS.find((s) => s.id === sid);
      setAiProg({ done: i, total: subs.length, cur: meta ? meta.short : sid });
      try {
        const p = buildPrompt(sid, diag, ctx, essay); if (!p) continue;
        const { text } = await sendMessagesUnified({ apiKey, model, system: p.system, messages: [{ role: 'user', content: p.user }], maxTokens: 1000, baseUrl });
        acc[sid] = { text: (text || '').trim(), ts: Date.now() };
        setAi({ ...acc }); try { localStorage.setItem(AI_KEY, JSON.stringify(acc)); } catch { /* quota */ }
      } catch (e) { setAiErr(`일부 생성 실패: ${(e && e.message) || ''}`); }
    }
    setAiProg(null);
  };
  const aiCount = Object.keys(ai).length;

  const totals = S1.reduce((t, s) => { const d = diag[s.id]; if (d) { t.answered += d.answered; t.correct += d.correct; } return t; }, { answered: 0, correct: 0 });
  const allAcc = totals.answered ? totals.correct / totals.answered : null;

  const th = { fontFamily: SERIF, fontSize: '0.72rem', fontWeight: 700, color: INK[600], padding: '6px 6px', borderBottom: `1.5px solid ${INK[700]}`, whiteSpace: 'nowrap' };
  const td = { fontSize: '0.78rem', color: INK[800], padding: '8px 6px', borderBottom: `1px solid ${INK[200]}`, ...NUM };
  const chip = (on) => ({ fontFamily: SERIF, background: 'none', border: 'none', cursor: 'pointer', padding: '2px 0', fontWeight: 800, fontSize: '0.88rem', color: on ? INK[900] : INK[400], borderBottom: `2px solid ${on ? INK[900] : 'transparent'}` });

  return (
    <DocSection title="과목별 학습 진단" hint={`약점 → 합격자 처방 · 1차 정답률 ${allAcc == null ? '미학습' : Math.round(allAcc * 100) + '%'}`}>
      {/* 과목 선택 — 전과목 + 제1차·제2차 */}
      <div style={{ display: 'flex', gap: 13, flexWrap: 'wrap', alignItems: 'center', marginBottom: 8 }}>
        <button onClick={() => setSel('all')} style={chip(sel === 'all')}>전과목</button>
        <span style={{ width: 1, height: 14, background: INK[300], alignSelf: 'center' }} />
        <button onClick={() => setSel('1차')} style={{ ...chip(sel === '1차'), fontSize: '0.8rem', color: sel === '1차' ? INK[900] : INK[500] }}>제1차</button>
        {S1.map((s) => <button key={s.id} onClick={() => setSel(s.id)} style={chip(sel === s.id)}>{s.short}</button>)}
        <span style={{ width: 1, height: 14, background: INK[300], alignSelf: 'center' }} />
        <button onClick={() => setSel('2차')} style={{ ...chip(sel === '2차'), fontSize: '0.8rem', color: sel === '2차' ? INK[900] : INK[500] }}>제2차</button>
        {S2.map((s) => <button key={s.id} onClick={() => setSel(s.id)} style={chip(sel === s.id)}>{s.short}</button>)}
      </div>

      {/* 🖊 AI 진단 재생성 — 한 버튼 + 과목별 체크(해제 시 그 과목 재생성 제외) */}
      <div style={{ marginBottom: 10 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
          <button onClick={genAll} disabled={!!aiProg || inclCount === 0} style={{ ...inkBtn, opacity: (aiProg || inclCount === 0) ? 0.6 : 1 }}>
            {aiProg ? `AI 진단 생성 중… ${aiProg.done}/${aiProg.total} (${aiProg.cur})`
              : `${inclCount === ALL_SUBS.length ? '전과목' : `선택 ${inclCount}과목`} AI 진단 ${aiCount > 0 ? '재생성' : '생성'}`}
          </button>
          {aiCount > 0 && !aiProg && <span style={{ fontFamily: SERIF, fontSize: '0.66rem', color: INK[400] }}>{aiCount}개 생성됨 · 과목을 누르면 그 소견이 보입니다</span>}
          {aiErr && <span style={{ fontFamily: SERIF, fontSize: '0.66rem', color: INK[600] }}>{aiErr}</span>}
        </div>
        {/* 재생성 포함 과목 체크 (체크 해제 = 제외) */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap', marginTop: 7 }}>
          <span style={{ fontFamily: SERIF, fontSize: '0.62rem', color: INK[400], letterSpacing: '0.04em' }}>재생성 포함</span>
          {ALL_SUBS.map((s) => {
            const on = !excl.has(s.id); const has = !!ai[s.id];
            return (
              <button key={s.id} onClick={() => toggleExcl(s.id)} title={on ? '재생성에 포함' : '제외됨(기존 소견 유지)'} disabled={!!aiProg}
                style={{ display: 'inline-flex', alignItems: 'center', gap: 5, fontFamily: SERIF, fontSize: '0.72rem', fontWeight: 700, background: 'none', border: 'none', cursor: aiProg ? 'default' : 'pointer', padding: 0, color: on ? INK[800] : INK[300] }}>
                <span style={{ width: 13, height: 13, border: `1.3px solid ${on ? INK[800] : INK[300]}`, background: on ? INK[800] : '#fff', color: '#fff', fontSize: '0.6rem', display: 'flex', alignItems: 'center', justifyContent: 'center', lineHeight: 1 }}>{on ? '✓' : ''}</span>
                {s.short}{has ? <span title="이미 생성됨" style={{ color: on ? INK[400] : INK[300], fontSize: '0.58rem' }}>·완료</span> : null}
              </button>
            );
          })}
        </div>
      </div>

      {(sel === 'all' || sel === '1차' || sel === '2차') ? (
        <div>
          {(sel === 'all' || sel === '1차') && (
            <>
              {/* 전과목 시각 그래프 — 과목별 정답률 레이더(막대X) */}
              {(() => {
                const axes = S1.map((s) => ({ label: s.short, val: diag[s.id]?.answered ? diag[s.id].acc * 100 : 0 }));
                return (
                  <div style={{ display: 'flex', gap: 18, alignItems: 'center', flexWrap: 'wrap', margin: '2px 0 10px' }}>
                    <Radar axes={axes} size={150} />
                    <div style={{ flex: 1, minWidth: 180, fontFamily: SERIF, fontSize: '0.74rem', color: INK[600], lineHeight: 1.7 }}>
                      〈그림〉 1차 과목별 정답률 프로필. 안쪽일수록 취약합니다.<br />
                      {S1.map((s) => { const d = diag[s.id]; return <span key={s.id} style={{ marginRight: 10, whiteSpace: 'nowrap' }}>{s.short} <b style={{ color: d?.answered ? INK[800] : INK[400] }}>{d?.answered ? Math.round(d.acc * 100) + '%' : '미학습'}</b></span>; })}
                    </div>
                  </div>
                );
              })()}
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead><tr>
                  <th style={{ ...th, textAlign: 'left' }}>제1차 과목</th>
                  <th style={{ ...th, textAlign: 'right' }}>정답률</th>
                  <th style={{ ...th, textAlign: 'left' }}>가장 약한 곳</th>
                  <th style={{ ...th, textAlign: 'left' }}>합격 전략</th>
                </tr></thead>
                <tbody>
                  {S1.map((s) => {
                    const d = diag[s.id]; if (!d) return null;
                    const w = d.byDim[0];
                    const wtxt = w ? `${w.key}${w.untouched ? ' 미학습' : ` ${Math.round(w.acc * 100)}%`}` : '–';
                    return (
                      <tr key={s.id} onClick={() => setSel(s.id)} style={{ cursor: 'pointer' }}>
                        <td style={{ ...td, textAlign: 'left', fontFamily: SERIF, fontWeight: 700, color: INK[900] }}>{s.short} ›</td>
                        <td style={{ ...td, textAlign: 'right', fontWeight: 700, color: d.answered ? INK[900] : INK[400] }}>{d.answered ? `${Math.round(d.acc * 100)}%` : '미학습'}</td>
                        <td style={{ ...td, textAlign: 'left', color: w && w.untouched ? INK[400] : INK[800] }}>{wtxt}</td>
                        <td style={{ ...td, textAlign: 'left', color: INK[600], fontFamily: SERIF }}>{RX[s.id]?.stratShort || ''}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </>
          )}
          {(sel === 'all' || sel === '2차') && (
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: sel === '2차' ? 0 : 16 }}>
              <thead><tr>
                <th style={{ ...th, textAlign: 'left' }}>제2차 과목</th>
                <th style={{ ...th, textAlign: 'left' }}>유형</th>
                <th style={{ ...th, textAlign: 'left' }}>합격 전략</th>
              </tr></thead>
              <tbody>
                {S2.map((s) => (
                  <tr key={s.id} onClick={() => setSel(s.id)} style={{ cursor: 'pointer' }}>
                    <td style={{ ...td, textAlign: 'left', fontFamily: SERIF, fontWeight: 700, color: INK[900] }}>{s.short} ›</td>
                    <td style={{ ...td, textAlign: 'left', color: INK[500] }}>논술·답안형</td>
                    <td style={{ ...td, textAlign: 'left', color: INK[600], fontFamily: SERIF }}>{RX[s.id]?.stratShort || ''}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {essay.n > 0 && (sel === 'all' || sel === '2차') && <div style={{ fontSize: '0.68rem', color: INK[400], marginTop: 6, ...NUM }}>2차 답안 연습 {essay.n}개 작성{essay.avg != null ? ` · 자기채점 평균 ${essay.avg}점` : ''}</div>}
        </div>
      ) : isS2(sel) ? (() => {
        const s = S2.find((x) => x.id === sel); const rx = RX[sel] || {};
        const nUnits = ((ctx && ctx.leavesBySubject && ctx.leavesBySubject[sel]) || []).length;
        return (
          <div>
            <div style={{ fontFamily: SERIF, fontSize: '0.94rem', color: INK[900], lineHeight: 1.65, margin: '4px 0 2px', fontWeight: 700 }}>2차 논술형 — 합격자는 “{rx.stratShort}”로 뚫었습니다.</div>
            <div style={{ fontSize: '0.68rem', color: INK[400], ...NUM }}>논점(단원) {nUnits}개{essay.n > 0 ? ` · 답안 연습 ${essay.n}개(자기채점 평균 ${essay.avg ?? '–'}점)` : ' · 답안 연습 기록 없음'}</div>
            <SubHead hint={`합격수기 78건 · ${s?.short}`}>합격자는 이렇게 공부했다</SubHead>
            <InfoBox>{renderInline(rx.strat, `strat-${sel}`)}</InfoBox>
            {rx.pitfall && <WarnBox>{renderInline(rx.pitfall, `pit-${sel}`)}</WarnBox>}
            {Array.isArray(rx.tips) && rx.tips.length > 0 && (<><SubHead hint="합격자 공부법 체크리스트">지금 할 것</SubHead><div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>{rx.tips.map((t, i) => <div key={i} style={{ fontFamily: SERIF, fontSize: '0.8rem', color: INK[800], lineHeight: 1.6 }}>· {t}</div>)}</div></>)}
            <div style={{ display: 'flex', gap: 8, marginTop: 14, flexWrap: 'wrap' }}>
              {onOpen && <button onClick={() => onOpen({ type: 'essay', subjectId: sel })} style={inkBtn}>답안 연습 ›</button>}
              {onOpen && <button onClick={() => onOpen({ type: 'study', subjectId: sel })} style={inkBtn}>논점 학습 ›</button>}
            </div>
            <SubHead hint="실측·합격수기 기반 AI 소견">AI 진단 보충</SubHead>
            {ai[sel] ? <ProseBody text={ai[sel].text} /> : <div style={{ fontFamily: SERIF, fontSize: '0.78rem', color: INK[400], lineHeight: 1.6 }}>위 ‘전과목 AI 진단 생성’을 누르면 이 과목 맞춤 소견이 채워집니다.</div>}
          </div>
        );
      })() : (() => {
        const d = diag[sel]; if (!d) return null;
        const rx = RX[sel] || {};
        const wd = d.byDim[0];
        const strong = [...d.byDim].reverse().find((b) => b.answered && b.acc >= 0.7);
        const wdiv = d.byDiv && d.byDiv[0];
        const focus = [];
        if (wd) focus.push({ kind: '특성', b: wd, rx: rxDim(sel, wd.key) });
        if (wdiv) focus.push({ kind: '분야', b: wdiv, rx: `${wdiv.key} 분야를 ${wdiv.untouched ? '기출부터 시작해' : '약한 것 위주로'} 집중 회독하세요.` });
        d.byArea.slice(0, 3).filter((a) => !wd || a.key !== wd.key).slice(0, 1).forEach((a) =>
          focus.push({ kind: '단원', b: a, rx: `이 장을 ${a.untouched ? '기출부터 시작' : '약한 지문 위주로 다시'} 회독하세요.` }));
        // 레이더 축 — 특성(≥3 보장) + 분야(있으면 별도 레이더)
        const dimAxes = d.byDim.map((b) => ({ label: b.key, val: b.answered ? b.acc * 100 : 0 }));
        const radarAxes = dimAxes.slice();
        if (radarAxes.length < 3) radarAxes.push({ label: '종합', val: d.answered ? d.acc * 100 : 0 });
        if (radarAxes.length < 3) radarAxes.push({ label: '도전량', val: d.total ? Math.min(100, (d.answered / d.total) * 100) : 0 });
        const divAxes = (d.byDiv || []).map((b) => ({ label: b.key, val: b.answered ? b.acc * 100 : 0 }));

        return (
          <div>
            <div style={{ fontFamily: SERIF, fontSize: '0.94rem', color: INK[900], lineHeight: 1.65, margin: '4px 0 2px', fontWeight: 700 }}>
              {d.answered
                ? <>정답률 <b>{Math.round(d.acc * 100)}%</b> · 가장 약한 건 <b>{wd?.key}{wd && !wd.untouched ? ` ${Math.round(wd.acc * 100)}%` : ''}</b>{strong ? <> · 강점은 <b>{strong.key} {Math.round(strong.acc * 100)}%</b></> : ''}.</>
                : <>아직 시작 전 — <b>전 영역 최저 상태</b>. 합격자는 이 과목을 “{rx.stratShort}”로 뚫었습니다.</>}
            </div>
            <div style={{ fontSize: '0.68rem', color: INK[400], ...NUM }}>푼 기출 {d.answered} / {d.total}문항</div>

            {/* 시각 그래프 — 게이지 + 특성 레이더 + 분야 레이더(막대X) */}
            <div style={{ display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap', margin: '10px 0 4px' }}>
              <Gauge value={d.answered ? d.acc * 100 : 0} />
              <figure style={{ margin: 0, textAlign: 'center' }}>
                <Radar axes={radarAxes} size={130} />
                <figcaption style={{ fontFamily: SERIF, fontSize: '0.6rem', color: INK[400], marginTop: -2 }}>유형·특성</figcaption>
              </figure>
              {divAxes.length >= 3 && (
                <figure style={{ margin: 0, textAlign: 'center' }}>
                  <Radar axes={divAxes} size={130} />
                  <figcaption style={{ fontFamily: SERIF, fontSize: '0.6rem', color: INK[400], marginTop: -2 }}>분야</figcaption>
                </figure>
              )}
              <div style={{ flex: 1, minWidth: 150, fontFamily: SERIF, fontSize: '0.74rem', color: INK[600], lineHeight: 1.7 }}>
                <div style={{ color: INK[400], fontSize: '0.62rem', marginBottom: 2 }}>특성별 <span style={{ fontSize: '0.56rem' }}>(정답률 · 문항수=빈출)</span></div>
                <div style={{ marginBottom: 6 }}>{d.byDim.map((b) => <span key={b.key} style={{ display: 'inline-block', marginRight: 12, whiteSpace: 'nowrap' }}>{b.key} <b style={{ color: b.answered ? INK[800] : INK[400] }}>{b.answered ? Math.round(b.acc * 100) + '%' : '미학습'}</b> <span style={{ color: INK[400], fontSize: '0.6rem' }}>{b.total}문항</span></span>)}</div>
                {divAxes.length > 0 && <>
                  <div style={{ color: INK[400], fontSize: '0.62rem', marginBottom: 2 }}>분야별</div>
                  <div>{d.byDiv.map((b) => { const low = d.total && b.total < d.total * 0.1; return <span key={b.key} style={{ display: 'inline-block', marginRight: 12, whiteSpace: 'nowrap' }}>{b.key} <b style={{ color: b.answered ? INK[800] : INK[400] }}>{b.answered ? Math.round(b.acc * 100) + '%' : '미학습'}</b> <span style={{ color: INK[400], fontSize: '0.6rem' }}>{b.total}문항{low ? ' · 저빈출' : ''}</span></span>; })}</div>
                </>}
              </div>
            </div>

            {focus.length > 0 && (
              <>
                <SubHead hint="약한 순 · 합격수기 근거 처방">지금 집중할 것</SubHead>
                {focus.map((f, i) => {
                  const b = f.b; const acts = b.answered ? (b.wrongIds || []) : (b.ids || []);
                  return <FocusCard key={f.kind + b.key} n={i + 1} kind={f.kind} label={b.key} answered={b.answered} total={b.total} acc={b.acc} untouched={b.untouched} rx={f.rx}
                    actLabel={b.answered ? '틀린 것 풀기' : '문제 풀기'} onAct={onReview && acts.length ? () => onReview(acts.slice(0, 30), `${b.key} ${b.answered ? '오답' : ''} 풀기`) : null} />;
                })}
              </>
            )}

            {rx.strat && (
              <>
                <SubHead hint={`합격수기 78건 · ${d.short}`}>합격자는 이렇게 공부했다</SubHead>
                <InfoBox>{renderInline(rx.strat, `strat-${sel}`)}</InfoBox>
                {rx.pitfall && <WarnBox>{renderInline(rx.pitfall, `pit-${sel}`)}</WarnBox>}
              </>
            )}

            <SubHead hint="실측 데이터 + 합격수기 기반 AI 소견">AI 진단 보충</SubHead>
            {ai[sel] ? <ProseBody text={ai[sel].text} /> : <div style={{ fontFamily: SERIF, fontSize: '0.78rem', color: INK[400], lineHeight: 1.6 }}>위 ‘전과목 AI 진단 생성’을 누르면 이 과목 맞춤 진단·처방이 채워집니다.</div>}
          </div>
        );
      })()}
    </DocSection>
  );
}
