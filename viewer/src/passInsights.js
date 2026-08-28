// 🎓 합격 방법론 주입 — 합격수기 78건에서 증류한 과목별 공부법(pass_insights.json)을
// AI 학습 튜터·드릴의 시스템 프롬프트에 얹어, '합격자처럼' 강조점·암기법·우선순위를 반영한다.
// 사실(교재 내용)은 그대로, 이건 '어떻게 공부/강조할지' 전략 지침이다.

let _cache; // undefined=미로드, null=로드했으나 없음, object=로드됨

export async function loadPassInsights() {
  if (_cache !== undefined) return _cache;
  try {
    const r = await fetch('/data/pass-stories/pass_insights.json');
    _cache = r.ok ? await r.json() : null;
  } catch { _cache = null; }
  return _cache;
}

// 현재 과목/단계에 맞는 '합격자 공부법' 프롬프트 블록(문자열). 없으면 ''.
// 강사·교재 이름은 광고성이라 프롬프트에서 제외하고, 방법론(회독·암기·목차·완주·함정)만 넣는다.
export function passInsightBlock(insights, subjectId, stage) {
  if (!insights) return '';
  const s = insights.subjects && insights.subjects[subjectId];
  const o = insights.overall || {};
  const L = ['\n\n[합격자 공부법 — 실제 합격수기 78건에서 정리한 이 과목 학습 전략. 교재 사실이 우선이고, 아래는 "무엇을 강조하고 어떻게 외우고 어디에 힘줄지"에 대한 지침이다.]'];
  if (s) {
    if (s.rounds) L.push(`· 목표 회독/분량: ${s.rounds}`);
    if (s.how) L.push(`· 핵심 공부법: ${s.how}`);
    if (s.memorize) L.push(`· 암기 전략: ${s.memorize}`);
    if (s.pitfall) L.push(`· 흔한 실패(경계): ${s.pitfall}`);
    if (Array.isArray(s.tips) && s.tips.length) L.push(`· 실행 팁: ${s.tips.join(' / ')}`);
  }
  const stageStrat = stage === 2 ? o.stage2 : o.stage1;
  if (stageStrat) L.push(`· ${stage === 2 ? '2차' : '1차'} 전략: ${stageStrat}`);
  if (Array.isArray(o.cross_cutting) && o.cross_cutting.length) {
    L.push(`· 공통 원칙: ${o.cross_cutting.slice(0, stage === 2 ? 4 : 2).join(' / ')}`);
  }
  L.push('학생이 "이 과목/부분 어떻게 공부해?"라고 물으면 위 방법론을 근거로 회독·암기법·우선순위·함정을 구체적으로 안내하라. 평소 설명·확인질문에도 이 강조점을 자연스럽게 녹여라(장황한 훈수는 금지, 지금 배우는 내용에 맞게).');
  L.push('[근거 톤] 공부법·학습전략을 안내할 때는 "실제 합격자들은 ~했다", "합격자 다수가 ~한다"처럼 합격수기 근거를 밝혀 신뢰를 줘라. 단, 교재 내용(사실) 설명 자체에는 붙이지 마라(사실은 사실대로).');
  return L.join('\n');
}

// 계획 생성기(오늘의 계획·달력)용 — 순서·배분에 반영할 합격 전략 요약.
export function planStrategyText(insights) {
  if (!insights) return '';
  const o = insights.overall || {};
  const subj = insights.subjects || {};
  const L = ['[합격수기 78건 기반 전략 — 과목 순서·일수 배분과 과목별 강조에 반영하라]'];
  if (o.tracks && o.tracks.동차) L.push(`· 동차: ${o.tracks.동차}`);
  if (o.stage1) L.push(`· 1차: ${o.stage1}`);
  if (o.stage2) L.push(`· 2차: ${o.stage2}`);
  if (Array.isArray(o.common_failures) && o.common_failures.length) L.push(`· 피해야 할 실패: ${o.common_failures.slice(0, 3).join(' / ')}`);
  const rounds = ['economics', 'civil', 'accounting', 'realestate', 'law']
    .map((s) => (subj[s] ? `${subj[s].label} ${subj[s].rounds || ''}`.trim() : ''))
    .filter(Boolean);
  if (rounds.length) L.push(`· 과목별 목표 회독: ${rounds.join(' · ')}`);
  return L.join('\n');
}

// 과목별 한 줄 합격 팁(오늘의 계획·달력 UI 표기용).
export function subjectTip(insights, subjectId) {
  if (!insights) return '';
  const s = insights.subjects && insights.subjects[subjectId];
  if (!s) return '';
  if (Array.isArray(s.tips) && s.tips.length) return s.tips.slice(0, 2).join(' · ');
  return (s.how || '').split('.')[0];
}

// 드릴(인출 연습)용 짧은 인출법 힌트 — 목차/두문자/판례번호 등 합격 암기방식.
export function drillInsightHint(insights, subjectId, stage) {
  if (!insights) return '';
  const s = insights.subjects && insights.subjects[subjectId];
  const bits = [];
  if (s && s.memorize) bits.push(s.memorize);
  if (stage === 2) bits.push('목차·두문자·판례번호까지 스스로 인출하게 유도(합격자 암기방식).');
  else bits.push('정형 유형·핵심 조문/개념을 스스로 떠올리게(기출 반복 인출).');
  return bits.length ? `\n[합격자 인출법] ${bits.join(' ')}` : '';
}
