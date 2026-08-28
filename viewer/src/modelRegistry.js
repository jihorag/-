// 다중 LLM 모델 레지스트리 — 클라우드 카탈로그 + 로컬(Ollama) 자동감지 통합.
// 모델 식별자(ref): 클라우드는 기존 id 그대로(claude-*, gpt-*, gemini-*),
//                   로컬/문샷은 provider:modelId (local:qwen3.6:latest, moonshot:kimi-k2.6).
import { isTauri } from './tauriShim';
import { ALL_MODELS, LOCAL_BASE, MOONSHOT_BASE, getProviderForModel } from './aiProviders';
import { getApiKey, getBaseUrls, getRoles, setRoleModel } from './aiLearningStore';

// 네이티브 우선 fetch — 데스크톱에서는 plugin-http 로 CORS 없이 localhost 를 부를 수 있다.
// 웹앱에는 그 경로가 없으므로(isTauri() 항상 false) 표준 fetch 만 쓴다.
async function nativeFetch(url, init) {
  return fetch(url, init);
}

// 프로바이더 메타(설정 UI·라우팅 공용)
export const PROVIDERS = {
  anthropic: { id: 'anthropic', label: 'Claude', kind: 'anthropic', keyId: 'anthropic', cloud: true },
  openai:    { id: 'openai',    label: 'GPT',    kind: 'openai',    keyId: 'openai',    cloud: true },
  google:    { id: 'google',    label: 'Gemini', kind: 'gemini',    keyId: 'google',    cloud: true },
  moonshot:  { id: 'moonshot',  label: 'Kimi',   kind: 'openai',    keyId: 'moonshot',  cloud: true },
  local:     { id: 'local',     label: '로컬(Ollama)', kind: 'openai', keyId: null,      cloud: false },
};

// 로컬(Ollama) 설치 모델 감지 — 데스크톱 전용. 미실행/미설치/웹이면 [].
export async function discoverLocalModels() {
  try {
    const res = await nativeFetch(`${LOCAL_BASE}/api/tags`, { method: 'GET' });
    if (!res || !res.ok) return [];
    const data = await res.json();
    return (data.models || []).map((m) => ({
      ref: `local:${m.name}`,
      provider: 'local',
      label: m.name,
      sizeGB: m.size ? Math.round((m.size / 1e9) * 10) / 10 : null,
      free: true,
      local: true,
    }));
  } catch {
    return []; // Ollama 미실행 등 — 조용히 빈 목록
  }
}

// 클라우드 카탈로그(기존 ALL_MODELS를 ref 형태로)
export function cloudModels() {
  return ALL_MODELS.map((m) => ({
    ref: m.id,
    provider: m.provider,
    label: m.label,
    tier: m.tier,
    free: false,
    local: false,
  }));
}

// 통합 카탈로그 = 로컬(감지) + 클라우드. 설정·드롭다운용.
export async function allModels() {
  const local = await discoverLocalModels();
  return [...local, ...cloudModels()];
}

// Ollama 실행 여부(온보딩·상태표시용)
export async function isLocalAvailable() {
  const m = await discoverLocalModels();
  return m.length > 0;
}

// 모델 ref → 호출 파라미터 해석 { provider, model, apiKey, baseUrl, needsKey }.
// 어떤 역할/화면이든 이 하나로 provider·키·baseUrl 을 얻어 sendMessagesUnified 에 넘긴다.
export function resolveCall(modelRef) {
  const provider = getProviderForModel(modelRef);
  const baseUrls = getBaseUrls();
  const apiKey = getApiKey(provider); // local → 'ollama' 더미
  let baseUrl = baseUrls[provider];
  if (provider === 'local' && !baseUrl) baseUrl = LOCAL_BASE;
  if (provider === 'moonshot' && !baseUrl) baseUrl = MOONSHOT_BASE;
  return { provider, model: modelRef, apiKey, baseUrl, needsKey: provider !== 'local' };
}

// 역할 기본 모델 시드 — 현재는 no-op. 기본 모델은 클라우드(Kimi K2.6)이고,
// 로컬(Ollama)은 36B라 실시간엔 느려서 자동 지정하지 않음(사용자가 드롭다운/설정에서 선택).
// (setRoleModel/getRoles 는 4.5-c 역할 설정 UI 에서 사용)
export async function seedRoleDefaults() {
  return getRoles();
}
