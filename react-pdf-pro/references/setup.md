# Setup -- Version Compatibility & Installation

> Next.js 16 App Router + React 19 + Vietnamese font support
> Tested with: `@react-pdf/renderer@^4.1.6`, `react@19.2.3`, `next@16.1.6`

---

## 1. Version Compatibility

### Compatibility Matrix

| Package | Minimum | Recommended | Notes |
|---------|---------|-------------|-------|
| `@react-pdf/renderer` | 4.1.0 | 4.1.6+ | React 19 support added in 4.1.0 |
| React | 16.8.0 | 19.x | React 19 supported since v4.1.0 |
| Next.js | 14.1.1 | 16.x | Pre-14.1.1 has fatal App Router bug |
| Node.js | 18 | 20 or 21 | Tested against 18, 20, 21 |
| Bun | -- | -- | Unofficially works |

### v4.0.0 Breaking Changes

- **ESM-only**: Dropped CommonJS build. All common bundlers (webpack, Vite, Turbopack) support ESM. Jest users must migrate to Vitest.
- **React 19**: Support added in v4.1.0 via updated react-reconciler.

### What Does NOT Work

| Feature | Status | Reason |
|---------|--------|--------|
| Edge Runtime | Not supported | Relies on Node.js APIs (Buffer, fs, zlib) |
| OpenType Variable fonts | Not supported | PDF 2.0 spec does not support them |
| WOFF2 fonts | Not supported | Only TTF and WOFF are accepted |
| `cacheComponents: true` | Breaks | SWC path errors in Next.js 16 |
| `reactCompiler: true` | Breaks | SWC path errors in Next.js 16 |

---

## 2. Setup Patterns

### 2.1 next.config.ts

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  serverExternalPackages: ["@react-pdf/renderer"],
  compiler: {},  // Required -- prevents undefined access in Next.js 16
  // Do NOT add: cacheComponents: true, reactCompiler: true
}

export default nextConfig
```

**Why `serverExternalPackages`?** Without it, Next.js bundles `@react-pdf/renderer` into the server bundle, causing `require() of ES Module not supported` errors. This setting tells Next.js to use native Node.js `require()` instead.

### 2.2 Installation

```bash
pnpm add @react-pdf/renderer
```

No additional peer dependencies needed -- it bundles its own yoga-layout, fontkit, and pdfkit.

### 2.3 Import Patterns

**Server-side (API routes, Server Components):**
```ts
import { renderToBuffer, renderToStream } from "@react-pdf/renderer"
import { createElement } from "react"
```

**Client-side (dynamic import with SSR disabled):**
```ts
import dynamic from "next/dynamic"

const PDFViewer = dynamic(
  () => import("@react-pdf/renderer").then((mod) => mod.PDFViewer),
  { ssr: false, loading: () => <p>Loading preview...</p> }
)

const PDFDownloadLink = dynamic(
  () => import("@react-pdf/renderer").then((mod) => mod.PDFDownloadLink),
  { ssr: false }
)
```

### 2.4 Font Registration File

Create a singleton font registration module:

```ts
// src/lib/pdf/fonts.ts
import { Font } from "@react-pdf/renderer"

let registered = false

export function registerFonts() {
  if (registered) return
  registered = true

  // Disable hyphenation for Vietnamese text
  Font.registerHyphenationCallback((word) => [word])

  // Register Be Vietnam Pro (see vietnamese-fonts.md for full example)
  Font.register({
    family: "BeVietnamPro",
    fonts: [
      { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVPSTAyLFyeg_IDWvOJmVES_Hw4BX8.ttf" },
      { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVMSTAyLFyeg_IDWvOJmVES_HSMIG86Rbg.ttf", fontWeight: 700 },
      { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVNSTAyLFyeg_IDWvOJmVES_HwyNXcSZQ.ttf", fontStyle: "italic" },
      { src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVKSTAyLFyeg_IDWvOJmVES_HwyPcM3dbADcg.ttf", fontStyle: "italic", fontWeight: 700 },
    ],
  })
}
```
