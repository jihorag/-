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
  }
})
