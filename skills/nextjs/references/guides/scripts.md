# Script Optimization

> Source: https://nextjs.org/docs/app/guides/scripts (v16.1.6)

## Overview

The `next/script` component optimizes third-party script loading. Scripts load once even across navigations within the same layout.

## Usage Patterns

### Layout Scripts (scoped to route group)

```typescript
import Script from 'next/script'

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <section>{children}</section>
      <Script src="https://example.com/script.js" />
    </>
  )
}
```

### Application Scripts (all routes)

```typescript
import Script from 'next/script'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
      <Script src="https://example.com/script.js" />
    </html>
  )
}
```

## Loading Strategies

| Strategy | When | Use Case |
|----------|------|----------|
| `beforeInteractive` | Before any Next.js code / hydration | Critical scripts (bot detection, consent) |
| `afterInteractive` | **(default)** After some hydration | Analytics, tag managers |
| `lazyOnload` | During browser idle time | Low-priority scripts (chat, social) |
| `worker` | **(experimental)** In web worker | Offload from main thread |

### Web Worker Strategy (experimental)

```javascript
// next.config.js
module.exports = {
  experimental: {
    nextScriptWorkers: true,
  },
}
```

```typescript
<Script src="https://example.com/script.js" strategy="worker" />
```

Requires `@qwik.dev/partytown` package. Uses [Partytown](https://partytown.qwik.dev/).

## Inline Scripts

Must include `id` prop for tracking:

```typescript
// Using children
<Script id="show-banner">
  {`document.getElementById('banner').classList.remove('hidden')`}
</Script>

// Using dangerouslySetInnerHTML
<Script
  id="show-banner"
  dangerouslySetInnerHTML={{
    __html: `document.getElementById('banner').classList.remove('hidden')`,
  }}
/>
```

## Event Handlers

Require `'use client'` directive:

```typescript
'use client'
import Script from 'next/script'

export default function Page() {
  return (
    <Script
      src="https://example.com/script.js"
      onLoad={() => { /* script loaded */ }}
      onReady={() => { /* loaded + every mount */ }}
      onError={() => { /* failed to load */ }}
    />
  )
}
```

| Handler | Fires |
|---------|-------|
| `onLoad` | Once after script finishes loading |
| `onReady` | After load + every component mount |
| `onError` | If script fails to load |

## Additional Attributes

Standard DOM attributes (`nonce`, `data-*`) are forwarded to the rendered `<script>` element:

```typescript
<Script
  src="https://example.com/script.js"
  id="example-script"
  nonce="XUENAJFW"
  data-test="script"
/>
```

## Quick Reference

| Task | Approach |
|------|----------|
| All routes | `<Script>` in root layout |
| Route group | `<Script>` in nested layout |
| Defer loading | `strategy="lazyOnload"` |
| Critical script | `strategy="beforeInteractive"` |
| Inline script | Add `id` prop |
| Event handlers | `onLoad` / `onReady` / `onError` (client only) |
| Off main thread | `strategy="worker"` (experimental) |
