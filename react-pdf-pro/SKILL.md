---
name: react-pdf-pro
description: "@react-pdf/renderer for Next.js 16. Vietnamese font support, PDF CV templates, server/client rendering, live preview, 18 documented errors. Triggers: react-pdf, pdf, pdf export, pdf template, cv template, vietnamese font, renderToBuffer, PDFViewer."
---

# React PDF Pro -- PDF Generation for Next.js 16

## When to Use

Trigger on any mention of: react-pdf, @react-pdf/renderer, pdf export, pdf template, cv template, pdf download, vietnamese font, renderToBuffer, PDFViewer, PDFDownloadLink, pdf styling.

## Reference Files

| File | Description |
|------|-------------|
| `references/setup.md` | Version compatibility matrix, next.config.ts setup, installation, import patterns, font registration singleton |
| `references/vietnamese-fonts.md` | Be Vietnam Pro registration (9 weights + italics), practical 4-weight setup, hyphenation callback, self-hosting |
| `references/components.md` | Document, Page, View, Text, Image, Link, Note, Canvas, PDFViewer, PDFDownloadLink, BlobProvider, SVG primitives |
| `references/styling.md` | StyleSheet API, valid units, flexbox, dimensions, spacing, colors, text, borders, transforms, media queries |
| `references/cv-templates.md` | Classic (single column), Modern (accent bar), Creative (2-column sidebar) layouts with ASCII diagrams |
| `references/server-rendering.md` | renderToBuffer, renderToStream, renderToFile, renderToString, API route patterns |
| `references/client-preview.md` | PDFViewer dynamic import, usePDF hook, PDFDownloadLink patterns |
| `references/errors.md` | 18 error entries (PDF-001 through PDF-018) with exact messages, causes, and fixes |
| `references/performance.md` | Font subsetting, image optimization, memoization, large documents, LRU caching strategy |
| `references/testing.md` | Vitest mocking, template output tests, font registration tests, API route tests, visual regression |
| `references/code-examples.md` | Complete font registration, full export API route, CV template with Vietnamese font |
| `references/advanced-examples.md` | Live preview with template switching, export button, two-column sidebar CV, react-pdf vs Puppeteer, sources |

## Error Quick Lookup

| ID | Error | Fix |
|----|-------|-----|
| PDF-001 | `require() of ES Module not supported` | `serverExternalPackages: ["@react-pdf/renderer"]` |
| PDF-002 | `PDFViewer is a web specific API` | `dynamic(() => import(...), { ssr: false })` |
| PDF-003 | `Font family not registered` | Call `registerFonts()` before render; match family name |
| PDF-004 | `ba.Component is not a constructor` | Upgrade Next.js to 14.1.1+; set `serverExternalPackages` |
| PDF-005 | `Buffer is not assignable to BodyInit` | `new Uint8Array(buffer)` |
| PDF-006 | `renderToBuffer()` type mismatch | Cast: `component as any` |
| PDF-007 | `DOMMatrix is not defined` | Use `ssr: false` for all client PDF components |
| PDF-008 | `document is not defined` | Dynamic import with `ssr: false` |
| PDF-009 | Vietnamese chars as boxes/`?` | Register Unicode font (Be Vietnam Pro) |
| PDF-010 | Variable font wrong weight | Use static TTF files, register each weight |
| PDF-011 | `Cannot find module 'zlib'` | `serverExternalPackages` + dynamic import |
| PDF-012 | `usePDF` stuck loading | Check font URLs (CORS, 404, format) |
| PDF-013 | `PDFDocument is not a constructor` | `serverExternalPackages` + `dynamic = "force-dynamic"` |
| PDF-014 | ESM/CJS conflict in Jest | Migrate to Vitest |
| PDF-015 | Page wrapping cuts content | `wrap={true} minPresenceAhead={50}` |
| PDF-016 | `__dirname is not defined` | Handled by `serverExternalPackages` |
| PDF-017 | Font weight fallback wrong | Register all weights you use |
| PDF-018 | `Minified React error #31` | Ensure Text children are strings; use v4.1.0+ |

## Key Patterns

### Vietnamese Font Registration
```tsx
import { Font } from '@react-pdf/renderer'

Font.register({
  family: 'BeVietnamPro',
  fonts: [
    { src: 'https://fonts.gstatic.com/s/bevietnampro/v12/...400.ttf' },
    { src: 'https://fonts.gstatic.com/s/bevietnampro/v12/...700.ttf', fontWeight: 700 },
  ]
})

Font.registerHyphenationCallback((word) => [word])  // Prevent Vietnamese splitting
```

### Export API Route
```tsx
// app/api/export/[id]/route.ts
import { renderToBuffer } from '@react-pdf/renderer'

export async function GET(req, { params }) {
  const { id } = await params
  const buffer = await renderToBuffer(<CVTemplate data={cvData} /> as any)
  return new Response(new Uint8Array(buffer), {
    headers: { 'Content-Type': 'application/pdf' }
  })
}
```

### Client Preview (Dynamic Import)
```tsx
const PDFViewer = dynamic(
  () => import("@react-pdf/renderer").then((mod) => mod.PDFViewer),
  { ssr: false }
)
```
