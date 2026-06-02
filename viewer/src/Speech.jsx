// Web Speech API 기반 TTS — 외부 의존성 0.
// AI 메시지 옆 🔊 버튼 → 한국어 음성으로 읽기. 재생/일시정지/중지.
// 마크다운·KaTeX·viz JSON 등 비-음성 토큰 자동 제거.

import { useEffect, useRef, useState } from 'react';

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

  if (state === 'idle') {
    return <button onClick={start} title="음성으로 듣기" style={btnStyle()}>🔊</button>;
  }
  if (state === 'speaking') {
    return (
      <span style={{ display: 'inline-flex', gap: 2 }}>
        <button onClick={pause} title="일시정지" style={btnStyle('#fbbf24')}>⏸</button>
        <button onClick={stop} title="중지" style={btnStyle()}>⏹</button>
      </span>
    );
  }
  return (
    <span style={{ display: 'inline-flex', gap: 2 }}>
      <button onClick={resume} title="재개" style={btnStyle('#10b981')}>▶</button>
      <button onClick={stop} title="중지" style={btnStyle()}>⏹</button>
    </span>
  );
}

function btnStyle(bg = '#fff') {
  return {
    padding: '3px 8px', background: bg, color: '#374151',
    border: '1px solid #e5e7eb', borderRadius: 4,
    fontSize: '0.74rem', fontWeight: 700, cursor: 'pointer',
  };
}
