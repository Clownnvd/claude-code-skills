# Caching Migrate Workflow

## Process

1. **Detect Versions** — Identify Next.js version, cache library versions
2. **Map Breaking Changes**:

| From → To | Category Affected | Breaking Change | Migration Action |
|-----------|------------------|-----------------|-----------------|
| Next.js 14 → 15 | Revalidation | `revalidatePath` behavior change | Verify revalidation still works |
| Next.js 15 → 16 | Static/Dynamic | `dynamicIO` default, `"use cache"` | Add explicit cache directives |
| Next.js 15 → 16 | Proxy | Middleware → proxy for auth | Update cache bypass logic |
| Next.js 15 → 16 | React cache() | Expanded `cache()` support | Migrate manual dedup to cache() |
| Any | ISR | `revalidate` API changes | Update revalidation config |

3. **Apply Migrations** — Preserve cache correctness (never cache auth data)
4. **Verify** — Check static/dynamic build output, test revalidation
5. **Re-score** — Ensure no caching regression

## Safety Rules

- NEVER cache authenticated responses during migration
- Verify `NO_CACHE_HEADERS` still applied after changes
- Test revalidation flows after every migration step
