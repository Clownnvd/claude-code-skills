# Bundle Size & Code Splitting (15%) + Image & Asset Optimization (12%)

## Category 1: Bundle Size & Code Splitting (15%)

### Criteria (10 items, each worth 1 point)

1. **Route-level code splitting** — Next.js App Router auto-splits per route (free +1 if using App Router)
2. **Dynamic imports for heavy libraries** — Libraries >50KB gzipped use `next/dynamic` or `dynamic(() => import(...))`. Check: chart libs, editors, syntax highlighters, date-fns/moment
3. **No barrel re-exports** — No `export * from` in index.ts files that pull entire modules. Check `src/components/index.ts`, `src/lib/index.ts`
4. **Tree-shakeable imports** — Named imports (`import { specific } from 'lib'`), not default/namespace (`import * as lib`)
5. **Lazy below-fold components** — Components not visible on initial viewport use `React.lazy` or `next/dynamic`
6. **No duplicate dependencies** — No multiple versions of same library (check `pnpm ls --depth=0` for duplicates)
7. **Minimal client JS** — Pages with `'use client'` should be leaf components, not entire pages
8. **No unused dependencies** — All `dependencies` in package.json are actually imported somewhere
9. **Production build optimized** — No `devDependencies` leaking into production bundle
10. **Bundle budget exists** — Either `next.config.js` experimental.outputFileTracingExcludes, or CI bundle size check, or documented budget

### Deduction Examples
- `-3` Large library imported at top level without dynamic import (e.g., `import MonacoEditor from 'monaco-editor'`)
- `-2` Barrel re-export pulling unused modules
- `-1` Missing bundle size monitoring

---

## Category 2: Image & Asset Optimization (12%)

### Criteria (10 items, each worth 1 point)

1. **next/image for all images** — No raw `<img>` tags. All images use `next/image` or `Image` component
2. **Explicit width/height** — All `Image` components have `width`+`height` or `fill` prop (prevents CLS)
3. **Priority for above-fold** — Hero/banner images have `priority` prop
4. **Responsive sizes** — Images use `sizes` prop for responsive breakpoints (`sizes="(max-width: 768px) 100vw, 50vw"`)
5. **WebP/AVIF serving** — Next.js image optimization enabled (default config or explicit `formats: ['image/avif', 'image/webp']`)
6. **Lazy loading below-fold** — Images below fold use default lazy loading (no `priority` or `loading="eager"`)
7. **No oversized assets in public/** — No images >500KB in `public/` directory. Use optimized formats
8. **SVG optimization** — SVGs are inline components or use SVGR, not loaded as images
9. **Font optimization** — Uses `next/font` for web fonts (no layout shift from font loading)
10. **No unoptimized flag** — `next.config.js` does not have `images.unoptimized: true`

### Deduction Examples
- `-3` Raw `<img>` tags for content images
- `-2` Missing width/height causing CLS
- `-2` Large unoptimized images in public/
- `-1` Missing `sizes` prop on responsive images

### Small App Adjustment
If app has no public-facing images (e.g., SaaS dashboard), redistribute Image weight (12%) → Bundle (9%) + Client (3%).
