# Common Errors & Fixes

---

## PDF-001: `require() of ES Module not supported`

**Error:**
```
Error [ERR_REQUIRE_ESM]: require() of ES Module
.../node_modules/@react-pdf/renderer/lib/index.js not supported
```

**Cause:** Next.js bundles `@react-pdf/renderer` into the server bundle and tries to `require()` an ESM-only package.

**Fix:** Add to `next.config.ts`:
```ts
serverExternalPackages: ["@react-pdf/renderer"]
```

---

## PDF-002: `PDFViewer is a web specific API`

**Error:**
```
Error: PDFViewer is a web specific API.
You're either using this component on Node, or your bundler is not loading
react-pdf from the appropriate web build.
```

**Cause:** `PDFViewer` uses browser APIs (iframe, Blob URL) and cannot render on the server.

**Fix:** Use dynamic import with `ssr: false`:
```ts
const PDFViewer = dynamic(
  () => import("@react-pdf/renderer").then((mod) => mod.PDFViewer),
  { ssr: false }
)
```

---

## PDF-003: `Font family not registered`

**Error:**
```
Error: Font family not registered: BeVietnamPro
```

**Cause:** `Font.register()` was not called before rendering, or the family name does not match.

**Fix:**
1. Ensure `registerFonts()` is called before `renderToBuffer()`.
2. Verify the `family` string in `Font.register()` matches `fontFamily` in styles.
3. For server-side, call registration in the API route handler.

---

## PDF-004: `ba.Component is not a constructor`

**Error:**
```
TypeError: ba.Component is not a constructor
```

**Cause:** Next.js App Router bug (pre-14.1.1) corrupting the react-pdf bundle.

**Fix:** Upgrade to Next.js 14.1.1+. For Next.js 16, ensure `serverExternalPackages` is set.

---

## PDF-005: `Buffer is not assignable to type BodyInit`

**Error:**
```
Type 'Buffer' is not assignable to type 'BodyInit | null'.
```

**Cause:** `NextResponse` body does not accept Node.js `Buffer` directly.

**Fix:** Wrap in `Uint8Array`:
```ts
return new NextResponse(new Uint8Array(buffer), { ... })
```

---

## PDF-006: `renderToBuffer()` type mismatch with React 19

**Error:**
```
Argument of type 'ReactElement<...>' is not assignable to parameter of type '...'
```

**Cause:** Type definitions lag behind React 19 reconciler changes.

**Fix:** Cast component as `any`:
```ts
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const component: any = createElement(Template, { data })
const buffer = await renderToBuffer(component)
```

---

## PDF-007: `DOMMatrix is not defined`

**Error:**
```
ReferenceError: DOMMatrix is not defined
```

**Cause:** Browser-only API accessed during SSR.

**Fix:** This is typically from `react-pdf` (viewer library, not renderer). Ensure no viewer components are imported server-side. Use `ssr: false` for all client-side PDF components.

---

## PDF-008: `document is not defined`

**Error:**
```
ReferenceError: document is not defined
```

**Cause:** Client-side PDF components imported during SSR.

**Fix:** Dynamic import with `ssr: false` for `PDFViewer`, `PDFDownloadLink`, and `BlobProvider`.

---

## PDF-009: Vietnamese text renders as `?` or boxes

**Error:** Vietnamese characters like "Gi?i thi?u" instead of "Gioi thieu" (with proper diacritics).

**Cause:** Using built-in Helvetica/Courier/Times-Roman fonts which do not support Vietnamese glyphs.

**Fix:** Register a Vietnamese-compatible font:
```ts
Font.register({
  family: "BeVietnamPro",
  src: "https://fonts.gstatic.com/s/bevietnampro/v12/QdVPSTAyLFyeg_IDWvOJmVES_Hw4BX8.ttf",
})
```

---

## PDF-010: OpenType Variable font not rendering

**Error:** Font loads but text renders incorrectly or with wrong weight.

**Cause:** PDF 2.0 specification does not support OpenType Variable fonts.

**Fix:** Use static TTF files. Register each weight separately:
```ts
Font.register({
  family: "MyFont",
  fonts: [
    { src: "Regular.ttf", fontWeight: 400 },
    { src: "Bold.ttf", fontWeight: 700 },
  ],
})
```

---

## PDF-011: `Cannot find module 'zlib'`

**Error:**
```
Module not found: Can't resolve 'zlib'
```

**Cause:** Client-side bundle trying to include Node.js built-in modules used by react-pdf internals.

**Fix:** Ensure `serverExternalPackages` is configured. For client-side usage, use dynamic import. In webpack config, add fallbacks:
```ts
// next.config.ts (if needed for client bundle)
webpack: (config, { isServer }) => {
  if (!isServer) {
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      zlib: false,
    }
  }
  return config
}
```

---

## PDF-012: `usePDF` stuck in loading state

**Error:** `instance.loading` is always `true`, PDF never renders.

**Cause:** Custom fonts fail to load silently (404, CORS, wrong format).

**Fix:**
1. Check font URLs are accessible (no CORS issues).
2. Verify font format is TTF or WOFF (not WOFF2).
3. Test with built-in Helvetica first to isolate the issue.
4. Check browser console for network errors.

---

## PDF-013: `PDFDocument is not a constructor`

**Error:**
```
TypeError: PDFDocument is not a constructor
```

**Cause:** Module resolution conflict in App Router. The bundler imports the wrong build.

**Fix:** Ensure `serverExternalPackages: ["@react-pdf/renderer"]` in next.config. For App Router API routes, use `export const dynamic = "force-dynamic"`.

---

## PDF-014: ESM/CJS conflict in Jest tests

**Error:**
```
SyntaxError: Cannot use import statement outside a module
```

**Cause:** `@react-pdf/renderer` v4+ is ESM-only; Jest defaults to CJS.

**Fix:** Migrate to Vitest, or add Jest ESM configuration:
```json
// package.json
{ "jest": { "transformIgnorePatterns": ["node_modules/(?!@react-pdf)"] } }
```

Better: Use Vitest (recommended by react-pdf team):
```ts
// vitest.config.ts
export default defineConfig({
  test: { environment: "jsdom" },
})
```

---

## PDF-015: Page wrapping cuts content mid-element

**Error:** Text or views get cut off at page boundaries without proper continuation.

**Cause:** `wrap` is disabled or `minPresenceAhead` is not set.

**Fix:**
```tsx
<View wrap={true} minPresenceAhead={50}>
  {/* Content that should not be orphaned */}
</View>

{/* Force page break */}
<Text break>This starts on a new page</Text>
```

---

## PDF-016: `__dirname is not defined` (esbuild/ESM)

**Error:**
```
ReferenceError: __dirname is not defined in ES module scope
```

**Cause:** Yoga layout dependency uses `__dirname` which is not available in ESM.

**Fix:** This is handled by `serverExternalPackages` in Next.js. If using esbuild directly, create a CJS shim and inject it.

---

## PDF-017: Font weight fallback renders wrong weight

**Error:** Bold text renders as regular, or thin text renders as bold.

**Cause:** The exact font weight is not registered; react-pdf's fallback algorithm picks the nearest registered weight.

**Fix:** Register all weights you use:
```ts
Font.register({
  family: "BeVietnamPro",
  fonts: [
    { src: "...", fontWeight: 400 },  // Regular
    { src: "...", fontWeight: 600 },  // SemiBold
    { src: "...", fontWeight: 700 },  // Bold
  ],
})
```

---

## PDF-018: `Minified React error #31` in production

**Error:**
```
Error: Minified React error #31
Objects are not valid as a React child
```

**Cause:** Passing non-serializable objects as children in PDF components, or React version mismatch between react-pdf reconciler and project React.

**Fix:**
1. Ensure all Text children are strings or numbers.
2. Ensure `@react-pdf/renderer` is v4.1.0+ for React 19.
3. Stringify any objects before rendering.
