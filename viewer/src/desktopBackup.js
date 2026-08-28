// 백업/복원 — 웹앱용.
//
// PC앱(Tauri)에서는 WKWebView 의 Blob 다운로드가 불안정해 네이티브 저장/열기 대화상자를
// 썼다. 웹앱에는 그 패키지가 없고 필요하지도 않다(브라우저 다운로드·파일 선택이 정상 동작).
// 호출부는 `isDesktop()` 이 거짓이면 기존 Blob/파일입력 경로로 폴백하도록 이미 짜여 있으므로,
// 여기서는 false 를 돌려주고 네이티브 함수는 쓰이지 않는 자리만 채운다.
import { isTauri, saveTextFile, openTextFile } from './tauriShim';

export function isDesktop() {
  return isTauri();
}

// 웹에서는 호출되지 않지만(위 폴백), 혹시 불려도 브라우저 방식으로 동작하게 둔다.
export async function saveBackupNative(jsonString, suggestedName) {
  return saveTextFile(suggestedName, jsonString);
}

export async function loadBackupNative() {
  return openTextFile();
}
