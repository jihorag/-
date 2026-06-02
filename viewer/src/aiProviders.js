// 멀티-프로바이더 클라이언트 라우터
// - Anthropic Claude (브라우저 직호출 공식 지원)
// - OpenAI GPT (CORS 차단 → baseUrl 프록시 필수)
// - Google Gemini (CORS 차단 → baseUrl 프록시 필수)
//
// 모델 ID prefix 로 자동 라우팅:
//   claude-*  → Anthropic
//   gpt-*     → OpenAI
//   gemini-*  → Google
//
// Anthropic system blocks(cache_control 포함)를 각 프로바이더 포맷으로 변환.
// OpenAI/Gemini 는 prompt caching 이 자동(implicit) — cache_control 메타는 drop.

import { sendMessages as sendAnthropic } from './aiClaudeClient';

// 모든 모델 카탈로그
export const ALL_MODELS = [
  // Anthropic — 브라우저 직호출 가능
  { id: 'claude-sonnet-4-6',     provider: 'anthropic', label: 'Claude Sonnet 4.6',  icon: '🎯', tier: 'balanced' },
  { id: 'claude-haiku-4-5-20251001', provider: 'anthropic', label: 'Claude Haiku 4.5', icon: '⚡', tier: 'fast' },
  { id: 'claude-opus-4-7',       provider: 'anthropic', label: 'Claude Opus 4.7',   icon: '🧠', tier: 'premium' },
  // OpenAI — 프록시 필요
  { id: 'gpt-5.4',               provider: 'openai',    label: 'GPT-5.4',           icon: '🔵', tier: 'balanced', requiresProxy: true },
  { id: 'gpt-5.4-mini',          provider: 'openai',    label: 'GPT-5.4 mini',      icon: '🔵', tier: 'fast',     requiresProxy: true },
  // Google — 프록시 필요
  { id: 'gemini-3.1-pro',        provider: 'google',    label: 'Gemini 3.1 Pro',    icon: '🟢', tier: 'balanced', requiresProxy: true },
  { id: 'gemini-3.1-flash',      provider: 'google',    label: 'Gemini 3.1 Flash',  icon: '🟢', tier: 'fast',     requiresProxy: true },
];

export function getProviderForModel(modelId) {
  const m = ALL_MODELS.find((x) => x.id === modelId);
  return m?.provider || 'anthropic';
}

export function modelRequiresProxy(modelId) {
  return !!ALL_MODELS.find((x) => x.id === modelId)?.requiresProxy;
}

// ── system blocks 평탄화: Anthropic 포맷 → 단일 string ───────────
function flattenSystem(systemBlocks) {
  if (!systemBlocks) return '';
  if (typeof systemBlocks === 'string') return systemBlocks;
  return systemBlocks
    .map((b) => (typeof b === 'string' ? b : (b.text || '')))
    .join('');
}

// ── 메시지 content 평탄화: 배열(cache_control 포함) → string ─────
function flattenMessageContent(content) {
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) {
    return content.map((b) => (typeof b === 'string' ? b : (b.text || ''))).join('');
  }
  return '';
}

// ── OpenAI Chat Completions ──────────────────────────────────────
async function sendOpenAI({ apiKey, model, system, messages, maxTokens, baseUrl, signal, onDelta }) {
  if (!apiKey) throw new Error('OpenAI API 키가 필요합니다');
  const endpoint = (baseUrl && baseUrl.trim() ? baseUrl.trim().replace(/\/$/, '') : 'https://api.openai.com') + '/v1/chat/completions';
  const stream = typeof onDelta === 'function';
  const apiMsgs = [];
  const sysText = flattenSystem(system);
  if (sysText) apiMsgs.push({ role: 'system', content: sysText });
  for (const m of messages) {
    apiMsgs.push({ role: m.role, content: flattenMessageContent(m.content) });
  }
  const body = {
    model,
    messages: apiMsgs,
    max_tokens: maxTokens,
    stream,
  };
  if (stream) body.stream_options = { include_usage: true };
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify(body),
    signal,
  });
  if (!res.ok) {
    let detail = '';
    try { detail = (await res.json()).error?.message || ''; } catch { /* noop */ }
    throw new Error(`OpenAI API ${res.status} ${res.statusText}${detail ? ': ' + detail : ''}`);
  }
  if (!stream) {
    const data = await res.json();
    const text = data.choices?.[0]?.message?.content || '';
    return {
      text,
      usage: {
        input_tokens: data.usage?.prompt_tokens || 0,
        output_tokens: data.usage?.completion_tokens || 0,
        cache_read_input_tokens: data.usage?.prompt_tokens_details?.cached_tokens || 0,
        cache_creation_input_tokens: 0,
      },
      stop_reason: data.choices?.[0]?.finish_reason,
      raw: data,
    };
  }
  // SSE 파싱
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
      const delta = evt.choices?.[0]?.delta?.content || '';
      if (delta) {
        text += delta;
        try { onDelta(delta, text); } catch { /* noop */ }
      }
      if (evt.choices?.[0]?.finish_reason) stop_reason = evt.choices[0].finish_reason;
      if (evt.usage) {
        usage = {
          input_tokens: evt.usage.prompt_tokens || 0,
          output_tokens: evt.usage.completion_tokens || 0,
          cache_read_input_tokens: evt.usage.prompt_tokens_details?.cached_tokens || 0,
          cache_creation_input_tokens: 0,
        };
      }
    }
  }
  return { text, usage, stop_reason };
}

// ── Google Gemini generateContent ────────────────────────────────
async function sendGoogle({ apiKey, model, system, messages, maxTokens, baseUrl, signal, onDelta }) {
  if (!apiKey) throw new Error('Google AI API 키가 필요합니다');
  const stream = typeof onDelta === 'function';
  const method = stream ? 'streamGenerateContent' : 'generateContent';
  const base = (baseUrl && baseUrl.trim() ? baseUrl.trim().replace(/\/$/, '') : 'https://generativelanguage.googleapis.com');
  const endpoint = `${base}/v1beta/models/${encodeURIComponent(model)}:${method}${stream ? '?alt=sse' : ''}`;

  const contents = [];
  for (const m of messages) {
    contents.push({
      role: m.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: flattenMessageContent(m.content) }],
    });
  }
  const sysText = flattenSystem(system);
  const body = {
    contents,
    generationConfig: { maxOutputTokens: maxTokens },
  };
  if (sysText) body.systemInstruction = { parts: [{ text: sysText }] };

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-goog-api-key': apiKey,
    },
    body: JSON.stringify(body),
    signal,
  });
  if (!res.ok) {
    let detail = '';
    try { detail = (await res.json()).error?.message || ''; } catch { /* noop */ }
    throw new Error(`Gemini API ${res.status} ${res.statusText}${detail ? ': ' + detail : ''}`);
  }
  if (!stream) {
    const data = await res.json();
    const cand = data.candidates?.[0];
    const text = (cand?.content?.parts || []).map((p) => p.text || '').join('');
    return {
      text,
      usage: {
        input_tokens: data.usageMetadata?.promptTokenCount || 0,
        output_tokens: data.usageMetadata?.candidatesTokenCount || 0,
        cache_read_input_tokens: data.usageMetadata?.cachedContentTokenCount || 0,
        cache_creation_input_tokens: 0,
      },
      stop_reason: cand?.finishReason,
      raw: data,
    };
  }
  // SSE 파싱
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
      if (!payload) continue;
      let evt;
      try { evt = JSON.parse(payload); } catch { continue; }
      const cand = evt.candidates?.[0];
      const chunk = (cand?.content?.parts || []).map((p) => p.text || '').join('');
      if (chunk) {
        text += chunk;
        try { onDelta(chunk, text); } catch { /* noop */ }
      }
      if (cand?.finishReason) stop_reason = cand.finishReason;
      if (evt.usageMetadata) {
        usage = {
          input_tokens: evt.usageMetadata.promptTokenCount || 0,
          output_tokens: evt.usageMetadata.candidatesTokenCount || 0,
          cache_read_input_tokens: evt.usageMetadata.cachedContentTokenCount || 0,
          cache_creation_input_tokens: 0,
        };
      }
    }
  }
  return { text, usage, stop_reason };
}

// ── 통합 dispatch ─────────────────────────────────────────────────
export async function sendMessagesUnified(opts) {
  const provider = getProviderForModel(opts.model);
  if (provider === 'openai') return sendOpenAI(opts);
  if (provider === 'google') return sendGoogle(opts);
  return sendAnthropic(opts);
}
