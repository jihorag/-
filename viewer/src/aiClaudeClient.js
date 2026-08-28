// Claude(Anthropic) Messages API 직호출 클라이언트 (브라우저 BYOK).
// - 사용자의 API 키는 localStorage에만 보관 (ailearn-byok).
// - 'anthropic-dangerous-direct-browser-access' 헤더로 CORS 우회 (Anthropic 공식 지원).
// - prompt caching: system 블록에 cache_control 적용해 인수인계 + 단원 본문을 재사용.
// - 스트리밍: SSE를 fetch 본문 reader로 파싱.
//
// 위험·검토(#8): 환각 방지 — system 프롬프트에 "교재 인용만, 일반지식 금지" 강제.

import { buildCatalog as _buildVizCatalog } from './viz/vizRegistry';

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
4. [강의 필기]는 강의에서 뽑아 교재 문체로 다듬은 보충 본문입니다. 교재와 같은 급의 근거로 쓰세요.
   · \`[43강 39:45]\` 는 나중에 그 대목을 되짚기 위한 표시일 뿐입니다.
     학생에게 답할 때 **굳이 인용 시각을 붙이지 마세요** — 읽는 흐름만 끊습니다.
     학생이 "몇 강에서 나왔냐"고 물을 때만 알려주면 됩니다.
   · "강사가 ~라고 했다", "강의에서는 ~" 같은 표현도 쓰지 마세요. 그냥 교재 내용처럼 설명하세요.
5. \`> 🐶 복습 메이트\` 블록은 **내용 설명이 아니라 학습 조언**입니다(무엇을 외우고 무엇은 넘길지).
   설명의 근거로 인용하지 말고, 조언이 필요할 때만 그대로 전하세요.

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

[수식·그래프·마크다운]
- 수식은 **KaTeX 인라인 \`$...$\`만** 사용 (예: \`$Q_d = 100 - 2P$\`).
- **디스플레이 \`$$...$$\` 형식은 절대 사용하지 마세요** — 인라인으로 작성하고, 강조가 필요하면 마크다운 줄바꿈으로.
- **굵게 강조 \`**...**\`는 반드시 한 줄 안에서 닫으세요** — \`**\` 뒤나 안에 줄바꿈을 절대 넣지 마세요. 잘못: \`**\\n텍스트**\`. 올바름: \`**텍스트**\`.
- 수식 등장 시 각 기호의 의미를 한 글자씩 풀어 설명.
- 화살표는 일반 텍스트로 (→ 또는 =>). 수식 화살표가 꼭 필요하면 인라인 \`$\\rightarrow$\` 안에서만.
- 표는 마크다운 표.
- 조문 인용 시 "○○법 제X조"로 정확히 + 조문이 무슨 말인지 일상 언어로 다시 풀어 설명.

[⭐ 시각자료 — 4계층 우선순위]
시각자료가 필요할 때 다음 순서로 시도. **위 계층이 가능하면 아래 계층 절대 사용 X**.

**Tier 1 (최우선)**: 인수인계서 [VIZ_CATALOG] 의 named 템플릿
  - 형식: \`\`\`viz <template-name> ... JSON ... \`\`\`
  - 좌표·색·축 라벨은 컴포넌트가 처리. AI는 의미적 파라미터만 채움.
  - 카탈로그에 있는 도식이면 무조건 이걸 사용.

**Tier 2 (자유 흐름도)**: Mermaid
  - 형식: \`\`\`mermaid ... \`\`\`
  - Tier 1 에 적합한 템플릿이 없고 흐름도/시퀀스도/관계도가 필요할 때만.
  - flowchart, sequenceDiagram, classDiagram, erDiagram 등 지원.
  - 한글 노드 라벨 OK. 라벨이 길면 큰따옴표로 감싸기.

**Tier 3 (마지막 폴백)**: freeform SVG
  - 형식: \`\`\`svg <svg>...</svg> \`\`\`
  - Tier 1·2 둘 다 안 되는 5% 케이스에서만.
  - 보안상 \`<script>\`, on* 핸들러, \`<iframe>\` 자동 제거됨.
  - viewBox 명시 권장 (없으면 자동 추가).

**Tier 4**: 마크다운 표
  - 일반 데이터 표는 마크다운 표 그대로.

[시각자료 공통 규칙]
- viz/mermaid/svg 펜스 안엔 해당 형식만. 주석·trailing comma 금지.
- 차트 뒤엔 본문 해설을 마크다운으로 이어 작성 — 차트만 단독 X.
- 한 메시지에 시각자료 1개만 (학습 부담 줄이기).
- **카탈로그에 있는데도 SVG/Mermaid 쓰는 행동 금지** — 일관성·품질이 핵심.

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

export const STUDY_RULES = `

[이론 학습 모드 — 매 턴 구조 (반드시 지킬 것)]
이 단원을 처음 배우는 학생과의 1:1 과외다. 매 답변은 아래 5단 구조를 따른다:

1. **📍 진도 표시** (첫 답변에만): 이 단원의 소제목 흐름을 3~6개로 먼저 보여주고
   "지금은 ①" 처럼 현재 위치를 찍는다. 이후 턴에서는 생략하되 소제목이 바뀔 때
   "② ○○로 넘어갈게요" 한 줄로 위치를 알린다.
2. **개념 1개만**: 이번 턴에서 가르칠 개념은 정확히 1개. 교재 순서를 따른다.
3. **구체 예시 의무**: 추상 설명만으로 끝내지 말 것. 반드시
   — 구체적 숫자가 들어간 사례 1개 (예: "아파트 전세가 3억에서 3.3억으로 오르면…")
   — 또는 감정평가·부동산 실무 상황 1개
   를 포함한다. "예를 들어"가 없는 답변은 실패다.
4. **⭐ 시험 포인트**: 이 개념이 기출에서 **어떤 함정으로 나오는지** 1줄.
   (예: "⭐ 기출은 '항상'을 끼워 옳지 않은 선지로 만듭니다 — 원칙·예외 구분이 출제 포인트")
   유사 개념이 있으면 2~3행 비교표로 차이를 못 박는다.
5. **확인 질문 1개**: OX 또는 단답. 학생이 답하면 맞아도 틀려도 "왜 그런지"를
   한 번 더 짚고 다음 개념으로.

[분량·리듬]
- 한 턴 250~450자(표 제외). 길면 쪼개라.
- 서론·인사·"오늘은 ~를 배워볼게요" 같은 채움말 금지. 바로 본론.
- 학생이 같은 개념에서 2회 연속 헤매면: 같은 설명 반복 금지 →
  더 쉬운 비유 + 더 작은 단위로 재설명.
- 학생이 빨리 이해하면 확인 질문을 건너뛰고 진도를 당겨도 된다.

[단원 마무리]
모든 소제목이 끝나면: ① 전체 흐름 한 줄 요약 ② 핵심 용어 3~5개 목록
③ "이제 문제풀이 탭에서 이 단원 기출을 풀어보세요" 안내.`;

export const CONCEPT_S2_RULES = `

[2차 개념 학습 모드 — 답안에 쓸 수 있는 형태로]
2차는 백지에 논술하는 시험이다. 개념을 "이해"시키는 데서 멈추지 말고
**답안지에 그대로 옮겨 쓸 수 있는 형태**로 가르친다:

1. 개념마다 **답안용 정의 문장** 1개를 따옴표로 제시 — "감정평가에서 ○○란 …를 말한다."
   학생이 이 문장을 외우면 답안 서두가 된다.
2. **목차 뼈대**: 이 논점이 출제되면 답안 목차가 어떻게 되는지
   (Ⅰ.의의 → Ⅱ.근거 → Ⅲ.요건/기준 → Ⅳ.효과/한계 식) 번호 목차로 제시.
3. **키워드 강조**: 채점자가 찾는 득점 키워드를 **굵게** 표시하고
   "이 단어가 빠지면 감점"임을 알린다.
4. 관련 법령·규칙 조문 번호를 정확히 (감정평가법·감칙 제X조).
5. 확인 질문은 "○○의 답안용 정의를 외워서 써보세요" 형태의 인출 연습.`;

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
- **완주율(completion_pct)**: 합격 답안의 핵심은 "잘 쓰기보다 다 쓰기"다. 요구되는 목차·분량 대비 학생이 실제로 채운 정도를 0~100%로 평가하라. 빈 목차·미작성 논점이 많으면 낮게.
- **득점/감점 지점은 '어느 목차·논점에서'인지 구체적으로** 짚어라(합격생은 채점평의 득점/감점 지점을 답안지에 옮겨 반복 학습한다). 추상적("내용 부족") 금지, "Ⅱ.2 최유효이용 판단 누락" 처럼 위치를 명시.
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
  "completion_pct": 75,
  "scored_points": ["Ⅰ.개요 감칙 근거 정확", "Ⅱ.1 거래사례비교법 산식·단위 정확"],
  "lost_points": ["Ⅱ.2 최유효이용 판단 목차 누락", "Ⅲ.결론 유의사항 미기재 → 완주 미달"],
  "strengths": ["목차 명확", "키워드 포함"],
  "missed": ["분량 부족", "결론 약함"],
  "rewrite_hint": "Ⅲ.결론에 유의사항 3가지 추가",
  "time_used_min": 18,
  "time_target_min": 20
}
\`\`\`
- scored_points·lost_points는 각 2~4개, '목차/논점 위치 + 사유'로. completion_pct는 정수.
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

// ── 1차 과목별 규칙 ─────────────────────────────────────
// 합격수기(회계사·세무사·감평) 만장일치: 회계는 '설명 듣는 과목'이 아니라
// '분개와 와꾸로 손이 기억하게' 만드는 과목. 튜터가 이걸 강제해야 한다.
export const ACCOUNTING_RULES = `

[💰 회계학 학습 규칙 — 분개와 와꾸로 '손이 기억하게' 만드는 시험]
- 감평 회계학은 재무회계 30 / 원가관리 10, **과락(40점) 방지**가 목표다(2026년 과락률 57%·평균 36.7점의 최대 난관). 깊이보다 '풀 문제를 시간 안에 푸는' 훈련이 핵심. 고급회계·리스·현금흐름표·종합예산 등 저효율 유형은 후순위로 안내하라.
- 재무회계는 **말로만 설명하고 끝내지 마라.** 개념을 짚은 뒤 반드시 **"이 거래를 분개해보세요"**로 학생이 직접 차변/대변을 쓰게 하고, 그 분개가 재무제표(B/S·I/S)로 어떻게 흘러가는지 보여줘라. "회계의 처음과 끝은 분개"다.
- 원가·계산 유형은 **정형 풀이틀('와꾸')을 먼저** 제시하라(예: 종합원가 = ①물량흐름 ②완성품환산량 ③원가배분). 학생이 그 틀의 빈칸을 채우게 하고, 와꾸마다 '왜 그렇게 푸는지' 한 줄 근거를 붙여라(와꾸만 외우면 변형문제에서 무너진다).
- 계산은 한 번에 답 주지 말고 **한 단계씩**(식→대입→계산→단위). 막히면 다음 단계 힌트만.
- **휘발성 경고**: 회계는 앞을 배우면 뒤에서 잊는 게 정상. 학생이 이전 개념을 잊었으면 짧게 복습시키고 "N회독으로 덮어야 한다"고 알려라.
- **선행 결손 역추적**: 학생이 중급회계 등에서 계속 막히면 원인이 앞 단원(회계원리·기초 분개·계정 분류) 결손인 경우가 많다. 증상만 고치지 말고 "어느 선행 개념부터 다시 봐야 하는지"를 콕 집어 되짚어 줘라. 되짚을 땐 메시지 끝에 아래 JSON을 붙여 학생이 그 단원으로 바로 이동하게 하라(화면엔 숨겨지고 이동 버튼이 뜬다):
\`\`\`json
{"prereq": true, "unit": "계정과 분개", "reason": "이 계산의 토대라 먼저 다져야 함"}
\`\`\`
unit은 앞 단원 제목의 핵심어(교재 단원명과 겹치게), reason은 한 줄.
- 실수는 **유형으로** 짚어라: 부호(+/-), 기간 안분(월할), 취득원가 포함여부(→감가상각·처분손익까지 연쇄 오류). 검산은 '같은 방식 재계산'은 무효 → **다른 경로**로 확인시켜라.
- 예시는 반드시 회계 숫자로(예: "기계 취득원가 1,000,000·잔존 100,000·5년 정액 → 연 감가상각 180,000").`;

export const STAGE1_SUBJECT_RULES = {
  accounting: ACCOUNTING_RULES,
};

export const JOURNAL_RULES = `

[✍️ 분개 채점 모드 — 재무회계 체화]
- 목적: 학생이 거래를 스스로 분개하고 재무제표 영향을 이해하게 한다. "직접 분개해 재무제표 영향 확인"이 최고의 재무회계 학습 행동이다.
- 한 사이클: ① 짧은 거래 상황 1개(구체 숫자) 제시 → "차변/대변으로 분개해보세요" → ② 학생 분개 입력 → ③ 채점: 맞으면 인정+한 줄 근거, 틀리면 **어느 계정·어느 방향이 틀렸는지 정확히** 짚고 올바른 분개 제시 → ④ 이 분개의 B/S·I/S 영향 1~2줄 → ⑤ 다음 거래(난이도 조절).
- 분개는 '차변 계정 XXX / 금액,  대변 계정 XXX / 금액' 형식으로. 자산·비용 증가는 차변, 부채·자본·수익 증가는 대변.
- 한 번에 거래 1개. 3개 연속 정답이면 난이도를 올리거나 관련 계산(감가상각·처분손익·유효이자 등)으로 확장하라.
- 첫 메시지는 인사 없이 바로 첫 거래 제시.
- **매 채점(③) 뒤 메시지 맨 끝에** 다음 JSON을 붙여라(화면엔 자동으로 숨겨지고, 틀린 분개는 복습 큐로 들어간다):
\`\`\`json
{"journal": true, "correct": true, "topic": "감가상각 분개"}
\`\`\`
correct는 학생 분개의 정오(boolean), topic은 거래 유형 5~15자.`;

export const CALC_S1_RULES = `

[🧮 계산 코칭 모드 (1차) — 한 단계씩]
- 목적: 회계·경제 계산을 학생이 스스로 단계를 밟게 한다. **정답만 주지 마라**(기존 학습앱 최대 불만이 "정답만 보여주고 끝").
- 진행: 문제 1개 제시 → "먼저 무슨 식을 써야 할까요?"부터 한 단계씩 학생에게 물어라. 매 단계 식→대입→계산→단위.
- 막히면 답을 주지 말고 **다음 한 단계 힌트만**. 계산 실수면 어느 단계에서 틀렸는지 짚어라.
- 계산형은 정형 풀이틀(와꾸)을 먼저 상기시켜라.
- 끝나면 검산 유도: "같은 방식 재계산 말고 **다른 경로**로 확인해보자"(예: 총액↔단가 역산, 대차평균).`;

// 회독(phase)별 튜터 태도. 같은 관이라도 1회독 학생과 3회독 학생에게 같은 깊이로 말하면 안 된다.
// 모드 탭 = 회독 축이므로 MODE_RULES 와 짝을 이뤄 붙는다.
export const PHASE_RULES = {
  basic: `
[회독 — 1회독(기본이론)]
- 지금은 **뼈대를 세우는 단계**입니다. 정의와 용어부터 확실히.
- 예외·함정은 아직 꺼내지 마세요. 큰 그림이 먼저입니다.
- "이건 나중에 심화에서 다룹니다" 라고 미뤄도 좋습니다.`,
  deep: `
[회독 — 2회독(심화이론)]
- 1회독으로 정의는 아는 학생입니다. 정의만 반복하면 지루해집니다.
- **경계·예외·유사 개념 구별**에 집중하세요. "왜 그런가"를 설명하세요.
- A와 B가 어떻게 다른지 대조표를 적극 활용하세요.`,
  prac: `
[회독 — 3회독(문제풀이)]
- 이론은 이미 두 번 봤습니다. **기출 적용과 함정 식별**이 목표입니다.
- 선지가 왜 틀렸는지, 출제자가 어디를 비틀었는지를 짚으세요.
- 개념 설명은 짧게, 문제 안에서 설명하세요.`,
  mock: `
[회독 — 4회독(모의·핵심)]
- 마무리 단계입니다. **인출 속도**가 관건입니다.
- 길게 설명하지 말고 학생이 스스로 떠올리게 하세요. 먼저 묻고 나중에 확인.
- 자주 틀리는 포인트만 압축해서 짚으세요.`,
  final: `
[회독 — 마무리(특강)]
- 시험 직전 압축 정리입니다. 새 내용을 추가하지 마세요.
- 출제 가능성이 높은 것만, 표·요약 형태로 짧게.`,
};

export const MODE_RULES = {
  // 1차
  study: STUDY_RULES,
  practice: PRACTICE_RULES,
  deep: DEEP_RULES,
  summary: SUMMARY_RULES,
  diagnose: DIAGNOSE_RULES,
  journal: JOURNAL_RULES,
  calc: CALC_S1_RULES,
  // 2차 신규
  concept_s2: CONCEPT_S2_RULES,
  template: TEMPLATE_RULES,
  topic_extract: TOPIC_EXTRACT_RULES,
  answer_write: ANSWER_RULES,
  mock_full: MOCK_FULL_RULES,
  calc_s2: CALC_S2_RULES,
};

function getEndpoint(baseUrl) {
  return (baseUrl && baseUrl.trim()) ? baseUrl.trim().replace(/\/$/, '') + '/v1/messages' : API_URL;
}

// 1시간 캐시 TTL — extended-cache-ttl beta. 같은 단원 1시간 내 재방문 시 캐시 히트.
const CACHE_1H = { type: 'ephemeral', ttl: '1h' };

export function buildSystemBlocks({ handoverMd, unitMd, sectionMd, problemsMd, lectureMd, phase, mode, currentMastery, recentSummary, leafPath, stage, subjectId, passInsights }) {
  // 캐시 prefix는 [SYSTEM_RULES + 과목별 규칙 + 합격방법론] → [handover + viz_catalog] → [section] → [problems] 순.
  // 과목/단원이 바뀌지 않는 한 prefix는 안정. 모드 규칙은 prefix 뒤로 빼서 모드 전환에도 캐시 보존.
  let systemHead = SYSTEM_RULES;
  if (stage === 2) {
    systemHead += STAGE2_RULES + (SUBJECT_RULES[subjectId] || '');
  } else {
    systemHead += (STAGE1_SUBJECT_RULES[subjectId] || ''); // 1차 과목별(회계 등) 규칙
  }
  if (passInsights) systemHead += passInsights; // 합격수기 78건 기반 과목별 공부법(과목당 안정 → prefix 캐시 유지)
  const blocks = [
    { type: 'text', text: systemHead },
  ];
  // 인수인계서 + viz 카탈로그 자동 주입 — 둘이 한 블록으로 묶어서 캐시 효율
  // registry 가 단일 소스. handover.md 의 수동 카탈로그는 제거됨.
  let vizCatalog = '';
  try { vizCatalog = _buildVizCatalog(subjectId) || ''; } catch { /* noop */ }
  const handoverPlusCatalog = [
    handoverMd ? `\n\n[인수인계서]\n${handoverMd}` : '',
    vizCatalog ? `\n\n${vizCatalog}` : '',
  ].filter(Boolean).join('');
  if (handoverPlusCatalog) {
    blocks.push({
      type: 'text',
      text: handoverPlusCatalog,
      cache_control: CACHE_1H,
    });
  }
  if (sectionMd) {
    blocks.push({
      type: 'text',
      text: `\n\n[현재 학습 단원 자료]\n${sectionMd}`,
      cache_control: CACHE_1H,
    });
  } else if (unitMd) {
    blocks.push({
      type: 'text',
      text: `\n\n[현재 학습 단원 자료]\n${unitMd}`,
      cache_control: CACHE_1H,
    });
  }
  // 강의 필기 — 해당 관·해당 회독의 강의에서 뽑은 압축본.
  // 단원 자료 뒤·기출 앞에 둬야 모드를 바꿔도 앞쪽 prefix 캐시가 보존된다.
  if (lectureMd) {
    blocks.push({
      type: 'text',
      text: `\n\n[강의 필기 — 강사 설명]\n${lectureMd}`,
      cache_control: CACHE_1H,
    });
  }
  if (mode === 'practice' && problemsMd) {
    blocks.push({
      type: 'text',
      text: `\n\n[기출 문제 자료]\n${problemsMd}`,
      cache_control: CACHE_1H,
    });
  }
  // 모드 규칙은 캐시 뒤로 — 모드 전환에도 위쪽 캐시(인수인계+단원+기출) 보존.
  const modeRules = MODE_RULES[mode] || '';
  if (modeRules) {
    blocks.push({ type: 'text', text: modeRules });
  }
  // 회독 규칙도 캐시 뒤. 1차에서만 의미가 있다(2차는 회독 축을 쓰지 않는다).
  if (stage !== 2) {
    const phaseRules = PHASE_RULES[phase] || '';
    if (phaseRules) blocks.push({ type: 'text', text: phaseRules });
  }
  // 상태(leafPath/mastery/recentSummary)는 매번 변하므로 가장 뒤.
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
      'anthropic-beta': 'extended-cache-ttl-2025-04-11',
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

/** 강의 필기에서 이 관(leaf)의 구간만 잘라낸다.
 *
 * 필기 파일은 유닛(unit_code) 하나에 관 여러 개가 `<!-- leaf: … -->` 앵커로 이어져 있다.
 * 통째로 챗에 넣으면 지금 배우는 관과 무관한 내용까지 토큰을 먹고, 화면에도 엉뚱한 관이 보인다.
 * 앵커를 못 찾으면(예전 형식) 전체를 그대로 돌려준다.
 */
export function sliceLectureNote(fullMd, leafId) {
  if (!fullMd || !leafId) return fullMd || '';
  const anchor = `<!-- leaf: ${leafId} -->`;
  const start = fullMd.indexOf(anchor);
  if (start < 0) return fullMd;
  const rest = fullMd.slice(start);
  const next = rest.indexOf('<!-- leaf:', anchor.length);
  return (next > 0 ? rest.slice(0, next) : rest).trim();
}

/** 화면에 뿌릴 때 쓰는 형태 — HTML 주석(앵커·표기규칙)을 걷어낸다.
 *  마크다운 렌더러는 주석을 숨기지 않고 글자 그대로 찍는다. */
export function stripNoteComments(md) {
  return (md || '').replace(/<!--[\s\S]*?-->/g, '').trim();
}

/** 화면용으로 출처 표기를 지운다.
 *
 * `[43강 48:30]` 같은 인용 시각은 문장 사이에 끼면 읽는 흐름을 끊는다.
 * 다만 파일에는 남겨둔다 — 나중에 "이 대목 강의 다시 듣기"로 되짚어야 하고,
 * 챗은 필요할 때 근거로 쓸 수 있어야 한다. 그래서 **표시할 때만** 걷어낸다.
 */
export function stripLectureCitations(md) {
  return (md || '')
    .replace(/\s*\[\d+강\s*\d+:\d{2}(?:~\d+:\d{2})?\]/g, '')
    // 상단의 "> 📖 이 관의 강의: …" 출처 줄도 화면에서는 뺀다
    .replace(/^>\s*📖\s*이 관의 강의:.*$/gm, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/** 교재 소제목 한 줄이 어느 탭 소속인지 판정한다.
 *
 * 교재는 한 파일 안에 이론·OX·암기법·법전…이 소제목으로 섞여 있고, 화면에서는 탭으로
 * 갈라 보여준다. 그 갈라내는 규칙이 여기 한 곳에 있어야 한다 — 화면 분할(splitDocTabs)과
 * 강의 필기 배정(splitLectureByTab)이 서로 다른 기준을 쓰면 필기가 엉뚱한 탭으로 간다.
 */
export function classifyDocHeading(title) {
  const t = title || '';
  if (/\bOX\b|O\s*\/\s*X|확인문제|점검문제/i.test(t)) return 'ox';
  if (/암기|두문자|기억법/.test(t)) return 'mem';
  if (/법조문 원문|법전/.test(t)) return 'law';
  if (/계산 연습|연습문제|와꾸/.test(t)) return 'prac';
  if (/기준서 원문|기준서 근거/.test(t)) return 'std';
  return 'theory';
}

/** 강의 필기를 교재 **탭별로 나눈다**.
 *
 * 필기의 앵커가 `🧠 암기법` 처럼 이론이 아닌 소제목을 가리키는 경우가 있다.
 * 그런데 화면은 그 소제목 줄을 이론 본문에서 **떼어내 다른 탭으로 보내면서 줄 자체를 지운다**.
 * 그래서 앵커가 갈 곳을 잃고, 그 필기는 이론 탭 맨 뒤로 밀려 문맥과 동떨어져 놓인다.
 * (경제학·부동산학원론 기준 못 붙는 앵커 40개 중 37개가 이 경우였다.)
 *
 * 여기서는 앵커가 가리키는 소제목이 속한 탭을 찾아 그 탭 몫으로 넘긴다.
 * 짝을 못 찾은 블록과 `_top` 은 이론이 받는다.
 *
 * 예외 — **OX 탭은 받지 않는다.** OX 탭은 마크다운을 그대로 그리지 않고 지문을 파싱해
 * 퀴즈로 만들기 때문에, 필기를 섞으면 파싱이 깨지고 내용도 사라진다. 이론에 남긴다.
 */
export function splitLectureByTab(docMd, lectureMd) {
  const out = { theory: '', ox: '', mem: '', law: '', prac: '', std: '' };
  const { blocks } = stripNoteComments2(lectureMd);
  if (!blocks.length) return out;

  // 교재 소제목 → 소속 탭.
  // splitDocTabs 와 **똑같이** 상태를 이어가며 훑어야 한다. 탭을 가르는 건 2~4단계
  // 소제목뿐이고, 5~6단계는 직전 탭에 그대로 남기 때문이다. 단순히 소제목마다
  // 따로 판정하면 `##### 암기 포인트` 같은 줄이 이론에서 암기 탭으로 잘못 빠진다.
  const owner = [];
  let cur = 'theory';
  for (const ln of (docMd || '').split('\n')) {
    const h = ln.match(/^(#{2,6})\s*(.*)$/);
    if (!h) continue;
    const title = h[2].trim();
    if (h[1].length <= 4) cur = classifyDocHeading(title);
    owner.push({ heading: title, tab: cur });
  }

  const norm = (s) => (s || '').replace(/\s+/g, '');
  const per = { theory: [], ox: [], mem: [], law: [], prac: [], std: [] };
  for (const b of blocks) {
    let tab = 'theory';
    if (b.after && b.after !== '_top') {
      const hit = owner.find((o) => norm(o.heading).includes(norm(b.after)));
      // 소제목을 못 찾으면 앵커 문구 자체로 판정한다 — 지워진 소제목을 가리킨 경우가 있다.
      const t = hit ? hit.tab : classifyDocHeading(b.after);
      if (t !== 'ox') tab = t; // OX 탭은 위 사유로 받지 않는다
    }
    // 앵커를 그대로 살려서 되붙인다 — 받는 탭에서 다시 소제목 매칭을 하기 때문이다.
    per[tab].push(b.after ? `<!-- after: ${b.after} -->\n${b.body}` : b.body);
  }
  for (const k of Object.keys(out)) out[k] = per[k].join('\n\n');
  return out;
}

/** 교재 본문에 강의 설명을 **끼워 넣어** 하나의 흐름으로 만든다.
 *
 * 강의 필기를 교재 뒤에 통째로 붙이면 같은 주제를 두 번 읽게 되고 둘이 따로 논다.
 * 그래서 필기 쪽에 `<!-- after: 2. IS곡선의 도출 -->` 앵커를 달아두고,
 * 교재의 해당 소제목 단락이 끝나는 자리에 그 대목의 강의 설명을 꽂는다.
 *
 * · `<!-- after: _top -->`  → 교재 맨 앞(도입) 자리
 * · 짝을 못 찾은 블록은 유실되지 않도록 맨 뒤에 붙인다.
 */
export function mergeLectureIntoDoc(docMd, lectureMd) {
  const lecture = stripNoteComments2(lectureMd);
  if (!lecture.blocks.length) return docMd || '';
  if (!docMd) return lecture.blocks.map((b) => b.body).join('\n\n');

  const lines = docMd.split('\n');
  // 교재를 소제목 단위로 자른다(제목 줄 + 그 아래 본문).
  const chunks = [];
  let cur = { heading: '', body: [] };
  for (const ln of lines) {
    if (/^#{2,6}\s/.test(ln)) {
      chunks.push(cur);
      cur = { heading: ln.replace(/^#+\s*/, '').trim(), body: [ln] };
    } else {
      cur.body.push(ln);
    }
  }
  chunks.push(cur);

  const used = new Set();
  const pick = (heading) => lecture.blocks.filter((b, idx) => {
    if (used.has(idx) || !b.after || b.after === '_top') return false;
    const hit = heading && heading.replace(/\s+/g, '').includes(b.after.replace(/\s+/g, ''));
    if (hit) used.add(idx);
    return hit;
  });

  const out = [];
  lecture.blocks.forEach((b, idx) => {
    if (b.after === '_top') { out.push(b.body); used.add(idx); }
  });
  chunks.forEach((c) => {
    if (c.body.length) out.push(c.body.join('\n'));
    pick(c.heading).forEach((b) => out.push(b.body));
  });
  lecture.blocks.forEach((b, idx) => { if (!used.has(idx)) out.push(b.body); });

  return out.filter((s) => s && s.trim()).join('\n\n');
}

/** 필기 md → `<!-- after: … -->` 앵커 기준 블록 목록. 주석은 제거해 돌려준다. */
function stripNoteComments2(md) {
  const src = md || '';
  const re = /<!--\s*after:\s*(.+?)\s*-->/g;
  const marks = [];
  let m;
  while ((m = re.exec(src)) !== null) marks.push({ after: m[1], start: m.index, len: m[0].length });
  if (!marks.length) {
    const body = stripNoteComments(src);
    return { blocks: body ? [{ after: null, body }] : [] };
  }
  const blocks = [];
  // 첫 앵커 앞부분(제목·출처 줄)은 맨 앞에 둔다.
  const head = stripNoteComments(src.slice(0, marks[0].start));
  if (head) blocks.push({ after: '_top', body: head });
  marks.forEach((mk, i) => {
    const end = i + 1 < marks.length ? marks[i + 1].start : src.length;
    const body = stripNoteComments(src.slice(mk.start + mk.len, end));
    if (body) blocks.push({ after: mk.after, body });
  });
  return { blocks };
}
