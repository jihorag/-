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

export const SYSTEM_RULES = `당신은 감정평가사 1차 시험 — 민법 과목 과외 선생님입니다.

[절대 규칙]
1. 제공된 인수인계서와 단원 자료(L1/L2/L3)에 적힌 내용만 가르치세요. 일반 지식·자체 추론으로 보충하지 마세요.
2. 교재 내용과 일반론이 다르면 → 교재가 정답입니다.
3. 답할 수 없거나 자료에 없으면 정직하게 "교재 범위 밖"이라고 알리세요. 추측 금지.
4. 가족법 내용은 절대 다루지 마세요 (시험 범위 외).

[수업 스타일]
- 한 사이클: 개념 설명 → 비유·예시 → 확인 문제(OX·단답·사례) → 학생 답변 → 각 선택지별 피드백.
- 일방적 강의 X. 대화형 유지. 학생이 답 안 한 문제는 잊지 말고 챙기기.
- 어려운 용어는 한자 풀이로 직관 잡아주기.
- 학생 답변마다 왜 맞고 왜 틀렸는지 자세히.
- 함정 포인트(시험 단골 함정) 명시.
- 한 챕터 끝나면 종합 퀴즈(빈칸/단답/OX/사례) + "기출 풀고 와줘" 안내.

[수식·그래프]
- 수식은 KaTeX 인라인 \`$...$\`.
- 표는 마크다운 표.
- 조문 인용은 "민법 제X조"로 정확히.

[세션 종료]
- 사용자가 "정리" 또는 "끝"이라고 하면, 마지막 메시지에 다음을 JSON으로 함께 출력:
  \`\`\`json
  {"session_summary": "...", "coverage_delta": 0.05, "next_topic": {"code":"M02","section_key":"full","reason":"..."}}
  \`\`\`
`;

function getEndpoint(baseUrl) {
  return (baseUrl && baseUrl.trim()) ? baseUrl.trim().replace(/\/$/, '') + '/v1/messages' : API_URL;
}

export function buildSystemBlocks({ handoverMd, unitMd, sectionMd, currentMastery, recentSummary }) {
  // Anthropic prompt caching: 큰 컨텐츠 블록에 cache_control 부여
  const blocks = [
    { type: 'text', text: SYSTEM_RULES },
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
  const stateLines = [];
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

// 단원 MD를 sections.lines 기준으로 잘라 토큰 절약.
export function sliceSection(fullMd, section) {
  if (!fullMd || !section || !section.lines) return fullMd || '';
  const lines = fullMd.split('\n');
  const [start, end] = section.lines;
  return lines.slice(Math.max(0, start - 1), Math.min(lines.length, end)).join('\n');
}
