# Caching Strategy Scoring — Overview

## Purpose
Objectively score caching quality in Next.js App Router applications. Framework: Next.js 16 + React 19 + Prisma + Vercel.

## Scoring System
- 10 categories, each scored 0-10
- Weighted sum produces 0-100 total
- Each deduction must cite specific file + line + reason

## Grade Scale

| Grade | Score | Deploy? |
|-------|-------|---------|
| A+/A/A- | 90-100 | Yes — enterprise-grade |
| B+/B/B- | 80-89 | Yes — production-ready |
| C+/C | 70-79 | Conditional — fix HIGH items first |
| D | 60-69 | No — major issues |
| F | <60 | No — critical issues |

## Quality Gates

| Gate | Minimum | Blocking Categories |
|------|---------|-------------------|
| Production | B- (80) | No category below 6 |
| Enterprise | A- (90) | No category below 8 |

## Output Format

```markdown
## Caching Strategy Scorecard — [Project Name]

| # | Category | Weight | Score | Weighted | Issues |
|---|----------|--------|-------|----------|--------|
| 1 | Cache-Control Headers | 15% | X/10 | Y | ... |
| ... | | | | | |
| **Total** | | **100%** | | **XX/100** | |
| **Grade** | | | | **B+** | |

### Issues List
| # | Severity | Category | File:Line | Issue | Fix |
|---|----------|----------|-----------|-------|-----|
| 1 | CRITICAL | ... | ... | ... | ... |

### Files Audited
- [list of files reviewed]
```

## Files to Audit (ordered by priority)

1. `src/app/api/**/route.ts` — Cache-Control headers on responses
2. `src/app/**/page.tsx` — static vs dynamic, ISR config
3. `src/app/**/layout.tsx` — layout caching behavior
4. `src/proxy.ts` — proxy perf, static bypass
5. `src/lib/auth.ts` + `src/lib/auth/server.ts` — session dedup
6. `src/lib/db/index.ts` — DB client, query cache
7. `src/app/api/webhooks/**/route.ts` — revalidation after mutations
8. `src/hooks/**` — client-side cache usage
9. `src/lib/api/response.ts` — NO_CACHE_HEADERS utility
10. `next.config.ts` — static/dynamic config, headers
