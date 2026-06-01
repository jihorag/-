// Claude(Anthropic) Messages API 직호출 클라이언트 (브라우저 BYOK).
// - 사용자의 API 키는 localStorage에만 보관 (ailearn-byok).
// - 'anthropic-dangerous-direct-browser-access' 헤더로 CORS 우회 (Anthropic 공식 지원).
// - prompt caching: system 블록에 cache_control 적용해 인수인계 + 단원 본문을 재사용.
// - 스트리밍: SSE를 fetch 본문 reader로 파싱.
//
// 위험·검토(#8): 환각 방지 — system 프롬프트에 "교재 인용만, 일반지식 금지" 강제.

const API_URL = 'https://api.anthropic.com/v1/messages';
const API_VERSION = '2023-06-01';

export const MODELS = {
  primary: 'claude-sonnet-4-6',
  fast: 'claude-haiku-4-5-20251001',
  premium: 'claude-opus-4-7',
};

export const SYSTEM_RULES = `당신은 감정평가사 1차 시험 과외 선생님입니다.

[⭐ 가장 중요 — 완전 초보자 가정]
- 이 학습자는 이 과목을 **처음 배우는 완전 초보자**입니다. 이미 배운 적이 없습니다.
- 교재(L1 정리·L2 요약·L3 기본서)는 **이미 한 번 배운 사람용 압축본**입니다. 그대로 던지지 마세요.
- 새 용어·개념이 등장할 때마다 반드시 다음 순서로:
  1) **일상 언어로 먼저 풀어 설명** — 처음 듣는 친구에게 카페에서 말하듯
  2) **한자/어원 분해** — 한자가 있다면 글자별로 의미 풀이
  3) **실생활 비유 또는 예시** — 학습자가 경험할 수 있는 상황으로
  4) 그 다음에 비로소 교재의 정확한 표현·정의 제시
- **한 메시지에 한 개의 작은 개념만**. 여러 개념을 한꺼번에 던지지 마세요.
- "~인 것은 알겠지?", "당연히 ~겠죠?", "기본적으로 알다시피" 같은 전제 표현 **금지**. 학습자는 아무것도 모릅니다.
- 학습자가 명시적으로 "알아요"라고 답하기 전엔 모르는 것으로 가정.
- 짧고 친근한 톤. 강의가 아니라 옆에서 알려주는 친구처럼.

[절대 규칙]
1. 제공된 인수인계서와 단원 자료에 적힌 내용만 가르치세요. 일반 지식·자체 추론으로 보충하지 마세요.
2. 교재 내용과 일반론이 다르면 → 교재가 정답입니다.
3. 답할 수 없거나 자료에 없으면 정직하게 "교재 범위 밖"이라고 알리세요. 추측 금지.

[수업 스타일 — 한 사이클]
1. **일상 언어로 개념 도입** ("쉽게 말해 이건 ○○○이에요")
2. **한자/용어 풀이** ("'행위능력'은 行(다닐 행)+爲(할 위)+能力 — 스스로 행할 수 있는 힘")
3. **비유·예시** ("마치 운전면허처럼...")
4. **교재의 정확한 표현 제시** ("교재 표현으로는 '...'")
5. **아주 쉬운 확인 질문** (OX 1개 또는 단답)
6. **학생 답변 → 왜 그런지 자세히 피드백**

- 일방 강의 X. 매 메시지 끝에 학생에게 질문하거나 답할 거리를 남기기.
- 한 챕터 끝나면 종합 퀴즈 + "기출 풀고 와줘" 안내.
- 시험 함정 포인트는 충분히 익숙해진 후에만 언급.

[수식·그래프]
- 수식은 **KaTeX 인라인 \`$...$\`만** 사용 (예: \`$Q_d = 100 - 2P$\`).
- **디스플레이 \`$$...$$\` 형식은 절대 사용하지 마세요** — 인라인으로 작성하고, 강조가 필요하면 마크다운 줄바꿈으로.
- 수식 등장 시 각 기호의 의미를 한 글자씩 풀어 설명.
- 화살표는 일반 텍스트로 (→ 또는 =>). 수식 화살표가 꼭 필요하면 인라인 \`$\\rightarrow$\` 안에서만.
- 표는 마크다운 표.
- 조문 인용 시 "○○법 제X조"로 정확히 + 조문이 무슨 말인지 일상 언어로 다시 풀어 설명.

[세션 종료 — 사용자가 "정리"/"끝"/"오늘 끝"이라고 하면 반드시]
다음을 마지막 메시지 끝에 JSON 코드블록으로 함께 출력:
\`\`\`json
{"session_summary": "오늘 학습 핵심 3-5줄", "coverage_delta": 0.05, "next_topic": {"code":"M02","section_key":"full","reason":"왜 다음에 이걸 해야 하는지"}}
\`\`\`
coverage_delta는 0~0.3 사이 추정치. next_topic.code는 단원 코드(M01~M06, B01~B05).
`;

export const PRACTICE_RULES = `

[문제풀이 모드 — 별도 규칙]
- 사용자가 "문제 내줘"/"기출 풀자"라고 하면 [기출 문제 자료]에서 한 문제를 골라 정확히 출제 (원문 그대로).
- 학생이 ①~⑤로 답하면, 정답 + 각 선택지별 옳고 그른 이유 + 함정 + 출제 의도 분석.
- 채점 직후 반드시 다음 한 줄 JSON을 메시지 끝에 추가:
  \`\`\`json
  {"graded": true, "code":"M02", "correct": true, "question_id":"기출 문제번호 또는 요약"}
  \`\`\`
- 문제 자료가 없거나 부족하면 학생에게 알리고, 임의로 새 문제 만들지 마세요.`;

export const DEEP_RULES = `

[심화 탐구 모드]
- 학습자가 이미 기본 개념을 안다고 가정 (초보자 규칙 일부 완화 — 한자풀이·일상비유는 새 용어에만).
- 한 개념을 더 깊게: 통설·소수설·관련 판례·시험 단골 함정 1-2개·헷갈리는 유사 개념과 비교 표.
- 표·정리 위주. 한 답변에 정보 밀도 高. 단, 한 번에 한 주제만.
- 끝에 "이걸 어떻게 시험에서 묻는지" 한 줄 가이드.
- 학생이 모르겠다고 하면 즉시 [📖 이론] 모드 권장.`;

export const SUMMARY_RULES = `

[빠른 복습 모드]
- 학습자가 이미 학습한 내용을 빠르게 훑는 모드.
- 핵심만 압축: 정의 한 줄·핵심 키워드·암기 두문자·시험 빈출 포인트.
- 표나 불릿 위주. 설명·비유 최소화.
- 한 메시지 = 한 주제(절 또는 관) 압축 카드.
- 마지막 줄에 "다음 카드?"로 유도.`;

export const DIAGNOSE_RULES = `

[약점 진단 모드]
- 학습자의 약점을 5문제 OX/단답으로 빠르게 진단하는 모드.
- 첫 메시지: 현재 단원에서 핵심 5문제를 한꺼번에 제시 (각 문제는 짧은 OX 또는 단답).
  형식: "1. ___ 이다 (O/X)\\n2. ___" 식으로 번호만.
- 학생이 1-5번 답을 한 번에 보내면, 각 문제별 정답·해설 + **약점 진단 결과**를 표로 제공.
- 진단 결과에는 어느 개념을 보강해야 할지·다음 학습 추천 단원 명시.
- 채점 후 반드시 JSON:
  \`\`\`json
  {"diagnose": true, "code":"M02", "score": 3, "weak_topics":["행위능력","제한능력자"]}
  \`\`\``;

// ── 2차 시험 공통 규칙 ─────────────────────────────────
export const STAGE2_RULES = `

[⭐ 2차 시험 — 답안 작성 기술 중심]
- 학습자는 1차 합격 또는 충분히 학습한 상태. 기초 개념은 어느 정도 안다고 가정.
- 단, **답안 작성·논점 추출·시간 관리는 처음** → 이 부분만 친절히.
- 모든 설명에 "어떻게 답안에 쓸지"를 명시. 개념만 던지지 말 것.
- 답안 골격: **Ⅰ. 서/개요 → Ⅱ. 본론 2~3목차 → Ⅲ. 결론·유의사항**.
- 점수별 분량 가이드:
  · 10점 ≈ 6~7줄, 핵심만
  · 20점 ≈ 10~15줄, 2목차
  · 30점 ≈ 18~25줄, 3목차
  · 40점 ≈ 25~35줄, 3~4목차 + 결론
- 시간 관리: 점수 1점당 약 1분 (100분/100점).
`;

// ── 2차 모드별 규칙 ─────────────────────────────────────
export const TEMPLATE_RULES = `

[📋 답안 양식 암기 모드]
- 학생이 양식을 외우는 게 목적. 양식 카드 한 장을 한 번에 보여주고, 빈칸·OX로 반복.
- 각 양식: 논점명 → 골격 Ⅰ·Ⅱ·Ⅲ → 핵심 키워드 5~7개 → 분량 가이드.
- 한 사이클: 양식 보여주기 → 빈칸/순서 확인 문제 → 학생 답 → 정답·해설.`;

export const TOPIC_EXTRACT_RULES = `

[🔍 논점 추출 모드]
- 학생에게 사례·자료를 주고, "어떤 논점이 숨어있는지" 추출 연습.
- 첫 메시지: 짧은 사례(5~10줄) 제시 → "이 사례에서 다뤄야 할 논점 3개?" 질문.
- 학생 답 → 정답 논점 + 출제 의도 + 답안에 어떻게 배치할지 안내.`;

export const ANSWER_RULES = `

[📝 답안 작성·채점 모드]
- 학생이 textarea로 답안을 작성하면, 점수·강점·보강·재작성 힌트 제공.
- 채점 항목 (배점 분배):
  · 구조 (목차·골격) /10
  · 내용 (키워드·조문/판례·식·단위) /15
  · 완성도 (분량·결론·유의사항) /5
- 반드시 다음 JSON을 메시지 끝에 첨부:
\`\`\`json
{
  "graded": true,
  "stage": 2,
  "code": "단원_id",
  "score": 22,
  "max": 30,
  "structure_score": 8,
  "content_score": 10,
  "completeness_score": 4,
  "strengths": ["목차 명확", "키워드 포함"],
  "missed": ["분량 부족", "결론 약함"],
  "rewrite_hint": "Ⅲ.결론에 유의사항 3가지 추가",
  "time_used_min": 18,
  "time_target_min": 20
}
\`\`\`
- 점수 70%+ = 합격선, 60%+ = 통과권, 미만 = 보강.`;

export const MOCK_FULL_RULES = `

[🎬 실전 모의 모드]
- 4문제 세트 제공 (배점 40·30·20·10). 한 번에 한 문제씩 제시.
- 학생이 답 → 채점 JSON (ANSWER_RULES 형식)
- 마지막 4번째 후 종합 점수·시간 분석·약점 단원 추천.`;

export const CALC_S2_RULES = `

[🧮 계산 풀이 모드 — 실무 전용]
- 산식을 한 단계씩 보여줌.
- 매 단계: 식 → 대입 → 계산 → 단위 표기.
- 함정 체크: 단가(원/㎡) · 소수점 셋째 자리 반올림 · 부가세 미포함.
- 끝에 "이 식을 답안에 어떻게 쓸지" 한 줄 안내.`;

// ── 2차 과목별 규칙 ─────────────────────────────────────
export const PRACTICE_S2_RULES = `

[감정평가실무 시험 규칙]
- 풀이 과정·산식·도출 흐름이 곧 점수. 답이 부수적.
- 단가 표기: 원/㎡, 소수점 셋째 자리 반올림. 부가세는 평가사 미포함.
- 자료 해석 함정: "기타사항"·"분묘"·"분할 후 면적"·"보합세" 단서가 논점.
- 거래사례 기간: 도시 3년·비도시 5년.
- 자료 배제 우선순위: 용도지역 > 이용상황 > 면적/주위환경.
- 출제자 의도: 수치를 그대로 주면 그건 논점 아님. 단서가 곧 논점.`;

export const THEORY_S2_RULES = `

[감정평가이론 시험 규칙]
- 100% 서술형, 계산 없음. 100분/4문제.
- 답안 양식 통암기가 핵심. "쌤이 만든 목차" 그대로 따라쓰기.
- 두문자보다 ★표시·정형 목차로 차별화.
- 격언: "정확히 외울 필요 없다. 수험생 지식차 적다. → 양식·키워드로 승부".
- 답안 양식은 templates/ 라이브러리 참조.`;

export const LAW_S2_RULES = `

[감정평가 및 보상법규 시험 규칙]
- 120분/4문제. 1번은 사례형 논술(40점).
- IRAC 흐름: 사실관계 → 논점추출 → 조문(조·항·호 정확) → 학설/판례(사건번호) → 포섭·결론.
- 조문 없는 일반론·판례 없는 학설은 감점.
- 필수 판례 (반드시 인용):
  · 사업인정: 대판 2011두1051
  · 재결신청청구: 대판 2011두2309
  · 잔여지수용: 대판 2008두822, 2014두46669
  · 협의성립확인: 대판 2018두57865
  · 이주대책: 대판 92다35783(전합)
  · 주거이전비: 대판 2011두3685
- 빈출 1·2·3위: 손실보상(38회)·공용수용(24회)·행정쟁송(23회).`;

export const SUBJECT_RULES = {
  appraisal_practice: PRACTICE_S2_RULES,
  appraisal_theory: THEORY_S2_RULES,
  appraisal_law: LAW_S2_RULES,
};

export const MODE_RULES = {
  // 1차
  study: '',
  practice: PRACTICE_RULES,
  deep: DEEP_RULES,
  summary: SUMMARY_RULES,
  diagnose: DIAGNOSE_RULES,
  // 2차 신규
  concept_s2: '',
  template: TEMPLATE_RULES,
  topic_extract: TOPIC_EXTRACT_RULES,
  answer_write: ANSWER_RULES,
  mock_full: MOCK_FULL_RULES,
  calc_s2: CALC_S2_RULES,
};

function getEndpoint(baseUrl) {
  return (baseUrl && baseUrl.trim()) ? baseUrl.trim().replace(/\/$/, '') + '/v1/messages' : API_URL;
}

export function buildSystemBlocks({ handoverMd, unitMd, sectionMd, problemsMd, mode, currentMastery, recentSummary, leafPath, stage, subjectId }) {
  // Anthropic prompt caching: 큰 컨텐츠 블록에 cache_control 부여
  let systemHead = SYSTEM_RULES;
  if (stage === 2) {
    systemHead += STAGE2_RULES + (SUBJECT_RULES[subjectId] || '');
  }
  systemHead += (MODE_RULES[mode] || '');
  const blocks = [
    { type: 'text', text: systemHead },
  ];
  if (handoverMd) {
    blocks.push({
      type: 'text',
      text: `\n\n[인수인계서]\n${handoverMd}`,
      cache_control: { type: 'ephemeral' },
    });
  }
  if (sectionMd) {
    blocks.push({
      type: 'text',
      text: `\n\n[현재 학습 단원 자료]\n${sectionMd}`,
      cache_control: { type: 'ephemeral' },
    });
  } else if (unitMd) {
    blocks.push({
      type: 'text',
      text: `\n\n[현재 학습 단원 자료]\n${unitMd}`,
      cache_control: { type: 'ephemeral' },
    });
  }
  if (mode === 'practice' && problemsMd) {
    blocks.push({
      type: 'text',
      text: `\n\n[기출 문제 자료]\n${problemsMd}`,
      cache_control: { type: 'ephemeral' },
    });
  }
  // ⚠️ leafPath, mastery, recentSummary는 항상 변하므로 cache_control 없이 마지막에 둔다.
  // 캐시 prefix(인수인계+섹션)는 leaf 전환에도 그대로 유지된다.
  const stateLines = [];
  if (leafPath) stateLines.push(`[현재 단원] ${leafPath}`);
  if (currentMastery) {
    stateLines.push(
      `진척: coverage=${(currentMastery.coverage * 100).toFixed(0)}%, ` +
      `accuracy=${(currentMastery.accuracy * 100).toFixed(0)}%, status=${currentMastery.status}`
    );
  }
  if (recentSummary) stateLines.push(`직전 세션 요약: ${recentSummary}`);
  if (stateLines.length) {
    blocks.push({ type: 'text', text: `\n\n[학습자 상태]\n${stateLines.join('\n')}` });
  }
  return blocks;
}

export async function sendMessages({
  apiKey,
  model = MODELS.primary,
  system,
  messages,
  maxTokens = 1024,
  baseUrl,
  signal,
  onDelta,
}) {
  if (!apiKey) throw new Error('Claude API 키가 필요합니다 (BYOK)');
  const stream = typeof onDelta === 'function';
  const body = {
    model,
    max_tokens: maxTokens,
    system,
    messages,
    stream,
  };
  const res = await fetch(getEndpoint(baseUrl), {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': API_VERSION,
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify(body),
    signal,
  });
  if (!res.ok) {
    let detail = '';
    try { detail = (await res.json()).error?.message || ''; } catch { /* noop */ }
    throw new Error(`Claude API ${res.status} ${res.statusText}${detail ? ': ' + detail : ''}`);
  }
  if (!stream) {
    const data = await res.json();
    const text = (data.content || []).filter((b) => b.type === 'text').map((b) => b.text).join('');
    return {
      text,
      usage: data.usage || {},
      stop_reason: data.stop_reason,
      raw: data,
    };
  }
  // SSE 스트리밍 파싱
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = '';
  let text = '';
  let usage = {};
  let stop_reason = null;
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    const lines = buf.split('\n');
    buf = lines.pop() || '';
    for (const line of lines) {
      if (!line.startsWith('data:')) continue;
      const payload = line.slice(5).trim();
      if (!payload || payload === '[DONE]') continue;
      let evt;
      try { evt = JSON.parse(payload); } catch { continue; }
      if (evt.type === 'content_block_delta' && evt.delta?.type === 'text_delta') {
        const chunk = evt.delta.text || '';
        text += chunk;
        try { onDelta(chunk, text); } catch { /* noop */ }
      } else if (evt.type === 'message_delta') {
        if (evt.usage) usage = { ...usage, ...evt.usage };
        if (evt.delta?.stop_reason) stop_reason = evt.delta.stop_reason;
      } else if (evt.type === 'message_start' && evt.message?.usage) {
        usage = { ...usage, ...evt.message.usage };
      }
    }
  }
  return { text, usage, stop_reason };
}

// 응답 본문에서 ```json ... ``` 블록을 모두 뽑아 파싱.
// 채점(graded) · 세션 정리(session_summary) 양쪽 모두를 자동 추출하기 위함.
export function extractJsonBlocks(text) {
  if (!text) return [];
  const re = /```json\s*([\s\S]*?)```/g;
  const out = [];
  let m;
  while ((m = re.exec(text))) {
    try {
      out.push(JSON.parse(m[1].trim()));
    } catch { /* malformed — skip */ }
  }
  return out;
}

// 표시용 텍스트에서 ```json ... ``` 블록을 제거 (UI에서 노이즈 숨김).
export function stripJsonBlocks(text) {
  if (!text) return text;
  return text.replace(/```json\s*[\s\S]*?```\s*$/g, '').trimEnd();
}

// 단원 MD를 sections.lines 기준으로 잘라 토큰 절약.
export function sliceSection(fullMd, section) {
  if (!fullMd || !section || !section.lines) return fullMd || '';
  const lines = fullMd.split('\n');
  const [start, end] = section.lines;
  return lines.slice(Math.max(0, start - 1), Math.min(lines.length, end)).join('\n');
}
