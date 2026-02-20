# Progressive Web Apps (PWA)

> Source: https://nextjs.org/docs/app/guides/progressive-web-apps (v16.1.6)

## Overview

PWAs combine web reach with native app features: home screen install, push notifications, cross-platform single codebase, instant deploys without app store.

## 1. Web App Manifest

Create `app/manifest.ts` (Next.js has built-in support):

```typescript
import type { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Next.js PWA',
    short_name: 'NextPWA',
    description: 'A Progressive Web App built with Next.js',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#000000',
    icons: [
      { src: '/icon-192x192.png', sizes: '192x192', type: 'image/png' },
      { src: '/icon-512x512.png', sizes: '512x512', type: 'image/png' },
    ],
  }
}
```

Place icon files in `public/`. Use [realfavicongenerator.net](https://realfavicongenerator.net/) for icon sets.

## 2. Push Notifications

**Browser support:** iOS 16.4+ (home screen), Safari 16+, Chromium, Firefox.

### VAPID Keys Setup

```bash
npm install -g web-push
web-push generate-vapid-keys
```

Add to `.env`:
```
NEXT_PUBLIC_VAPID_PUBLIC_KEY=your_public_key
VAPID_PRIVATE_KEY=your_private_key
```

### Server Actions (`app/actions.ts`)

```typescript
'use server'
import webpush from 'web-push'

webpush.setVapidDetails(
  'mailto:your-email@example.com',
  process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY!,
  process.env.VAPID_PRIVATE_KEY!
)

let subscription: PushSubscription | null = null

export async function subscribeUser(sub: PushSubscription) {
  subscription = sub // production: store in DB
  return { success: true }
}

export async function unsubscribeUser() {
  subscription = null // production: delete from DB
  return { success: true }
}

export async function sendNotification(message: string) {
  if (!subscription) throw new Error('No subscription available')
  await webpush.sendNotification(
    subscription,
    JSON.stringify({ title: 'Notification', body: message, icon: '/icon.png' })
  )
  return { success: true }
}
```

## 3. Service Worker (`public/sw.js`)

```javascript
self.addEventListener('push', function (event) {
  if (event.data) {
    const data = event.data.json()
    event.waitUntil(
      self.registration.showNotification(data.title, {
        body: data.body,
        icon: data.icon || '/icon.png',
        badge: '/badge.png',
        vibrate: [100, 50, 100],
      })
    )
  }
})

self.addEventListener('notificationclick', function (event) {
  event.notification.close()
  event.waitUntil(clients.openWindow('/'))
})
```

## 4. Security Headers

Add to `next.config.ts` `headers()`: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin` on all routes. For `/sw.js`: set `Cache-Control: no-cache, no-store, must-revalidate` and `Content-Security-Policy: default-src 'self'; script-src 'self'`.

## 5. Install Requirements

| Requirement | Details |
|-------------|---------|
| Valid manifest | Created in step 1 |
| HTTPS | Required; use `next dev --experimental-https` locally |
| Offline support | Optional; use [Serwist](https://github.com/serwist/serwist) |

## Quick Reference

| Step | File / Action |
|------|---------------|
| Manifest | `app/manifest.ts` |
| Icons | `public/icon-*.png` |
| VAPID keys | `web-push generate-vapid-keys` |
| Push actions | `app/actions.ts` with `web-push` |
| Service worker | `public/sw.js` |
| Security | Headers in `next.config.ts` |
| Static export | Set `output: 'export'`; move Server Actions to external API |
