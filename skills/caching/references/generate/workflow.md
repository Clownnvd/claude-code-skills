# Caching Generate Workflow

## Process

1. **Parse Request** — Extract: component type (API route, page, data loader), caching requirements
2. **Load Criteria** — Read all 10 caching scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| Cache-Control Headers (15%) | `NO_CACHE_HEADERS` for auth, `max-age` + `s-maxage` for public |
| Revalidation Strategy (15%) | `revalidatePath`/`revalidateTag` after mutations |
| Static/Dynamic Classification (12%) | `export const dynamic` or `"use cache"` directive |
| React cache() (10%) | Wrap repeated lookups with `cache()` |
| "use cache" Directive (10%) | Component/function-level caching with `cacheLife` profiles |
| Cache Monitoring (8%) | HIT/MISS logging, cache key inspection |
| CDN & Edge (8%) | `Vary` headers, CDN-friendly response shape |
| ISR (8%) | `revalidate` export for semi-static pages |
| Request Dedup (7%) | `cache()` for auth/session, Promise dedup for fetches |
| Proxy (7%) | Static asset bypass, auth cookie check only |

4. **Generate** — Write code with all caching patterns integrated
5. **Self-Check** — Verify all 10 categories addressed
6. **Output** — Code + compliance checklist

## Quality Contract

- All 10 categories addressed with concrete code
- Score >= 90 (A-) if audited with caching scoring
- No stale auth data cached, no private data in CDN
- Proper `Vary` headers on all personalized responses
