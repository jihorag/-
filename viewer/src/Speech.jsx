// Web Speech API 기반 TTS — 외부 의존성 0.
// AI 메시지 옆 🔊 버튼 → 한국어 음성으로 읽기. 재생/일시정지/중지.
// 마크다운·KaTeX·viz JSON 등 비-음성 토큰 자동 제거.

import { useEffect, useRef, useState } from 'react';
import { Volume2, Pause, Play, Square } from 'lucide-react';

const SUPPORTED = typeof window !== 'undefined' && 'speechSynthesis' in window;

// 마크다운/KaTeX/viz fence 등을 음성용 평문으로 변환
export function speechifyText(raw) {
  if (!raw) return '';
  let t = String(raw);
  // viz/mermaid/svg/json 코드블록 제거
  t = t.replace(/```(viz\s+\S+|mermaid|svg|json)[\s\S]*?```/g, ' [도식·표는 화면 참조] ');
  // 일반 코드블록 제거
  t = t.replace(/```[\s\S]*?```/g, ' ');
  // 인라인 KaTeX $...$ → 안에 내용만 (한자/숫자/기호 일부 유지)
  t = t.replace(/\$\$([\s\S]*?)\$\$/g, ' ');
  t = t.replace(/\$([^$\n]+?)\$/g, (_, inner) => ' ' + inner.replace(/\\(rightarrow|to)/g, '에서').replace(/\\[a-z]+/g, '') + ' ');
  // 굵게/이탤릭
  t = t.replace(/\*\*(.+?)\*\*/g, '$1');
  t = t.replace(/\*(.+?)\*/g, '$1');
  // 이미지 토큰
  t = t.replace(/\[IMAGE:[^\]]+\]/g, ' [이미지] ');
  // 마크다운 표 → 짧게
  t = t.replace(/^\|.+\|$/gm, ' [표는 화면 참조] ');
  // 헤더 #
  t = t.replace(/^#{1,6}\s+/gm, '');
  // 리스트 · - * → 줄바꿈
  t = t.replace(/^\s*[-*•]\s+/gm, '');
  // 다중 공백·줄바꿈 정리
  t = t.replace(/\n+/g, '. ').replace(/\s{2,}/g, ' ').trim();
  return t;
}

let _voicesPromise = null;
function loadVoices() {
  if (!SUPPORTED) return Promise.resolve([]);
  if (_voicesPromise) return _voicesPromise;
  _voicesPromise = new Promise((resolve) => {
    const tryLoad = () => {
      const v = window.speechSynthesis.getVoices();
      if (v && v.length) { resolve(v); return true; }
      return false;
    };
    if (tryLoad()) return;
    window.speechSynthesis.onvoiceschanged = () => tryLoad();
    setTimeout(() => resolve(window.speechSynthesis.getVoices() || []), 1500);
  });
  return _voicesPromise;
}

function pickKoreanVoice(voices) {
  if (!voices || !voices.length) return null;
  // 우선순위: ko-KR > ko 시작 > Korean 명칭 > 기본
  return voices.find((v) => v.lang === 'ko-KR')
      || voices.find((v) => v.lang?.startsWith('ko'))
      || voices.find((v) => /korean|korea|한국/i.test(v.name))
      || voices[0];
}

export function SpeakButton({ text, rate = 1.0, pitch = 1.0 }) {
  const [state, setState] = useState('idle'); // 'idle' | 'speaking' | 'paused'
  const utterRef = useRef(null);

  useEffect(() => () => {
    if (SUPPORTED) window.speechSynthesis.cancel();
  }, []);

  if (!SUPPORTED) return null;

  const start = async () => {
    if (!text) return;
    const voices = await loadVoices();
    const voice = pickKoreanVoice(voices);
    const cleanText = speechifyText(text);
    if (!cleanText) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(cleanText);
    if (voice) u.voice = voice;
    u.lang = 'ko-KR';
    u.rate = rate;
    u.pitch = pitch;
    u.onend = () => setState('idle');
    u.onerror = () => setState('idle');
    utterRef.current = u;
    window.speechSynthesis.speak(u);
    setState('speaking');
  };

  const pause = () => {
    window.speechSynthesis.pause();
    setState('paused');
  };
  const resume = () => {
    window.speechSynthesis.resume();
    setState('speaking');
  };
  const stop = () => {
    window.speechSynthesis.cancel();
    setState('idle');
  };

  // 아이콘은 lucide 로 통일한다 — 이 앱의 다른 버튼이 전부 lucide 라 이모지만 튄다.
  if (state === 'idle') {
    return (
      <button type="button" onClick={start} title="음성으로 듣기"
        aria-label="음성으로 듣기" className="speak-btn">
        <Volume2 size={14} strokeWidth={1.75} />
      </button>
    );
  }
  if (state === 'speaking') {
    return (
      <span className="speak-group">
        <button type="button" onClick={pause} title="일시정지" aria-label="일시정지" className="speak-btn">
          <Pause size={14} strokeWidth={1.75} />
        </button>
        <button type="button" onClick={stop} title="중지" aria-label="중지" className="speak-btn">
          <Square size={14} strokeWidth={1.75} />
        </button>
      </span>
    );
  }
  return (
    <span className="speak-group">
      <button type="button" onClick={resume} title="재개" aria-label="재개" className="speak-btn">
        <Play size={14} strokeWidth={1.75} />
      </button>
      <button type="button" onClick={stop} title="중지" aria-label="중지" className="speak-btn">
        <Square size={14} strokeWidth={1.75} />
      </button>
    </span>
  );
}
