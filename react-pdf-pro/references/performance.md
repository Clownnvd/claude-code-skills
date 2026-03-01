# Performance Optimization

---

## 10.1 Font Loading

```ts
// Preload fonts to avoid cold-start delay
Font.register({
  family: "BeVietnamPro",
  fonts: [/* ... */],
})

// Force font loading before first render
// (async, call during app initialization)
// Note: Font.load() is internal; fonts load on first use.
// The singleton pattern in registerFonts() handles this.
```

## 10.2 Font Subsetting

react-pdf uses Fontkit internally, which automatically performs font subsetting -- only glyphs used in the document are embedded in the PDF. This reduces file size significantly, especially for CJK/Vietnamese fonts.

**No manual configuration needed.** Subsetting is automatic.

## 10.3 Image Optimization

```ts
// Use smaller image dimensions (avoid 4K photos for CV thumbnails)
<Image
  src={avatarUrl}
  style={{ width: 80, height: 80 }}  // PDF only needs display-size image
  cache={true}                        // Enable caching (default)
/>

// For base64 images, compress before embedding
// Use JPEG for photos, PNG only for graphics with transparency
```

## 10.4 Memoization

```tsx
import { memo } from "react"

// Memoize template components to prevent unnecessary re-renders
export const ClassicTemplate = memo(function ClassicTemplate({ data }: Props) {
  // ... template JSX
})

// usePDF does not auto-update -- this is by design for performance
// Call updateInstance() only when data actually changes
```

## 10.5 Large Documents (30+ pages)

For documents with many pages, use web workers to prevent UI blocking:

```tsx
// Client-side only
const [instance] = usePDF({
  document: <LargeDocument data={data} />,
})
// The PDF is generated in a separate thread automatically
// when using usePDF or PDFViewer
```

## 10.6 Server-Side Performance

```ts
// Use renderToStream for large PDFs instead of renderToBuffer
// Streams start sending bytes immediately; buffers wait for full generation
const stream = await renderToStream(component)

// Set appropriate timeouts for large PDFs
export const maxDuration = 30  // seconds (Vercel-specific)
```

## 10.7 Caching Strategy

```ts
// For identical CVs, cache the PDF buffer
// Use Redis, filesystem, or in-memory cache

import { LRUCache } from "lru-cache"

const pdfCache = new LRUCache<string, Buffer>({
  max: 100,      // Cache 100 PDFs
  ttl: 1000 * 60 * 5,  // 5 minute TTL
})

const cacheKey = `${cv.id}-${cv.updatedAt.getTime()}`
let buffer = pdfCache.get(cacheKey)
if (!buffer) {
  buffer = await renderToBuffer(component)
  pdfCache.set(cacheKey, buffer)
}
```
