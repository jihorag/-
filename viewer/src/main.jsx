import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './resetRecords' // 학습 기록 1회 초기화(사용자 요청) — 앱 렌더 전에 실행
import './styles/tokens.css' // 토큰이 먼저 로드돼야 아래 CSS 가 var() 를 쓸 수 있다
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
