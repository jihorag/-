// 웹 배포용 Tauri 셰임.
//
// 소스는 PC앱(gampyeong-desktop)과 공유한다. PC앱에는 @tauri-apps/* 패키지가 있지만
// 웹앱에는 없다. 원래 코드는 `isTauri()` 로 분기해 웹에서는 실행되지 않지만,
// **import 는 실행 여부와 무관하게 번들러가 해석**하므로 패키지가 없으면 깨진다
// (dev 서버는 동적 import 까지 미리 해석한다).
// 그래서 데스크톱 전용 기능은 전부 여기를 거치게 하고, 웹에서는 안전한 기본값을 준다.

export function isTauri() {
  return false;
}

/** 데스크톱에서는 네이티브 HTTP(CORS 우회), 웹에서는 표준 fetch. */
export async function nativeFetch(url, init) {
  return fetch(url, init);
}

/** 파일 저장/열기 — 웹에서는 브라우저 다운로드·파일 선택으로 대신한다. */
export async function saveTextFile(defaultName, text) {
  const blob = new Blob([text], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = defaultName || 'backup.json';
  a.click();
  URL.revokeObjectURL(a.href);
  return true;
}

export async function openTextFile() {
  return new Promise((resolve) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/json,.json';
    input.onchange = () => {
      const f = input.files?.[0];
      if (!f) return resolve(null);
      const r = new FileReader();
      r.onload = () => resolve(String(r.result));
      r.readAsText(f);
    };
    input.click();
  });
}
