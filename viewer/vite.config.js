import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg', 'apple-touch-icon.png'],
      workbox: {
        // 빌드 자산만 프리캐시. 거대 데이터(24MB)·이미지는 런타임 캐시로 처리해
        // 설치형/오프라인에서도 데이터가 비지 않게 함.
        // 새 SW 즉시 활성화(skipWaiting/clientsClaim) — 사용자가 탭 다시 안 닫아도 갱신.
        skipWaiting: true,
        clientsClaim: true,
        globPatterns: ['**/*.{js,css,html,woff2,svg}'],
        globIgnores: ['**/data/**', '**/images/**'],
        navigateFallbackDenylist: [/^\/data\//, /^\/images\//],
        runtimeCaching: [
          {
            urlPattern: ({ url }) => url.pathname.startsWith('/data/'),
            handler: 'StaleWhileRevalidate',
            options: {
              cacheName: 'quiz-data',
              // manifest + 시험별 chunk(13) + taxonomy + 통암기(과목별 3) 등 — 여유 있게
              expiration: { maxEntries: 40, maxAgeSeconds: 60 * 60 * 24 * 30 },
              cacheableResponse: { statuses: [0, 200] },
            },
          },
          {
            urlPattern: ({ url }) => url.pathname.startsWith('/images/'),
            handler: 'CacheFirst',
            options: {
              cacheName: 'quiz-images',
              expiration: { maxEntries: 4000, maxAgeSeconds: 60 * 60 * 24 * 60 },
              cacheableResponse: { statuses: [0, 200] },
            },
          },
        ],
      },
      manifest: {
        name: '감정평가사 1차 기출정복',
        short_name: '감평기출',
        description: '감정평가사 1차 합격을 위한 기출문제 정복 PWA',
        lang: 'ko',
        start_url: '/',
        scope: '/',
        display: 'standalone',
        orientation: 'portrait',
        theme_color: '#1e293b',
        background_color: '#f1f5f9',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any maskable'
          }
        ]
      }
    })
  ],
  server: {
    fs: {
      allow: ['..']
    }
  },
  // 소스는 PC앱(gampyeong-desktop)과 공유한다. 그쪽에는 데스크톱 전용 `@tauri-apps/*` 가
  // 있지만 웹앱에는 설치돼 있지 않다. 현재 src/ 안의 참조는 전부 `./tauriShim` 으로 바꿔
  // 두었으므로 아래 설정 없이도 빌드된다 — PC앱에서 코드를 다시 가져올 때 놓친 import 가
  // 섞여 들어와도 빌드가 통째로 깨지지 않게 하는 안전망으로 남겨 둔다.
  // (dev 서버는 external 을 보지 않으므로, 동적 import 라도 반드시 셰임으로 바꿔야 한다.)
  build: {
    rollupOptions: {
      external: [/^@tauri-apps\//],
    },
  },
  optimizeDeps: {
    exclude: ['@tauri-apps/api', '@tauri-apps/plugin-http',
              '@tauri-apps/plugin-fs', '@tauri-apps/plugin-dialog'],
  },
})
