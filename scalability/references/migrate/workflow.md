# Scalability Migrate Workflow

## Process

1. **Detect Versions** — Identify Next.js, React, bundler, image optimization config
2. **Map Breaking Changes**:

| From → To | Category Affected | Breaking Change | Migration Action |
|-----------|------------------|-----------------|-----------------|
| Next.js 14 → 15 | RSC Architecture | Async request APIs | Update component async patterns |
| Next.js 15 → 16 | Bundle Size | Turbopack default | Verify tree shaking still works |
| Next.js 15 → 16 | Edge/CDN | dynamicIO changes | Update cache/static config |
| React 18 → 19 | Client Perf | Compiler auto-memoization | Remove manual useMemo/useCallback |
| Webpack → Turbopack | Bundle Size | Different splitting strategy | Verify chunk sizes |
| Any | Image Optimization | next/image API changes | Update Image component props |

3. **Apply Migrations** — Preserve performance characteristics
4. **Verify** — Bundle analysis, lighthouse, Web Vitals before/after
5. **Re-score** — Ensure no scalability regression

## Safety Rules

- Run bundle analysis before AND after migration
- Compare Web Vitals metrics pre/post
- Test under load if changing connection pooling
- Verify dynamic imports still split correctly
