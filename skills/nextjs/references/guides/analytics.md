# Analytics

> Source: https://nextjs.org/docs/app/guides/analytics (v16.1.6)

## Overview

Next.js has built-in support for measuring and reporting Web Vitals via `useReportWebVitals`. Vercel also offers a managed analytics service.

## Client Instrumentation

Create `instrumentation-client.ts` in your app root to run code before the frontend starts:

```typescript
// instrumentation-client.ts
console.log('Analytics initialized')
window.addEventListener('error', (event) => {
  reportError(event.error)
})
```

## useReportWebVitals

Create a dedicated client component (keeps client boundary minimal):

```typescript
// app/_components/web-vitals.tsx
'use client'
import { useReportWebVitals } from 'next/web-vitals'

export function WebVitals() {
  useReportWebVitals((metric) => {
    switch (metric.name) {
      case 'FCP': { /* handle FCP */ }
      case 'LCP': { /* handle LCP */ }
      // ...
    }
  })
}
```

```typescript
// app/layout.tsx
import { WebVitals } from './_components/web-vitals'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html><body><WebVitals />{children}</body></html>
  )
}
```

## Web Vitals Metrics

| Metric | Full Name                  | Measures                    |
|--------|----------------------------|-----------------------------|
| TTFB   | Time to First Byte         | Server response time        |
| FCP    | First Contentful Paint     | First visible content       |
| LCP    | Largest Contentful Paint   | Largest visible element     |
| FID    | First Input Delay          | Input responsiveness        |
| CLS    | Cumulative Layout Shift    | Visual stability            |
| INP    | Interaction to Next Paint  | Overall responsiveness      |

## Sending to External Systems

```typescript
useReportWebVitals((metric) => {
  const body = JSON.stringify(metric)
  const url = 'https://example.com/analytics'

  if (navigator.sendBeacon) {
    navigator.sendBeacon(url, body)
  } else {
    fetch(url, { body, method: 'POST', keepalive: true })
  }
})
```

### Google Analytics Integration

```typescript
useReportWebVitals((metric) => {
  window.gtag('event', metric.name, {
    value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
    event_label: metric.id,
    non_interaction: true,
  })
})
```

## Quick Reference

| Feature                    | API / File                        | Notes                              |
|----------------------------|-----------------------------------|------------------------------------|
| Report Web Vitals          | `useReportWebVitals`              | Requires `'use client'`           |
| Client instrumentation     | `instrumentation-client.ts`       | Runs before app starts            |
| Send to endpoint           | `navigator.sendBeacon` / `fetch`  | Use `keepalive: true` for fetch   |
| Managed analytics          | Vercel Analytics                  | Zero-config on Vercel             |
