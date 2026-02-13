# Data Flow Scoring — Overview

## Purpose
Objectively score data flow quality in Next.js App Router applications. Framework: React 19 + Prisma + TypeScript.

## Scoring System
- 10 categories, each scored 0-10
- Weighted sum produces 0-100 total
- Each deduction must cite specific file + line + reason

## Grade Scale

| Grade | Score | Deploy? |
|-------|-------|---------|
| A+/A/A- | 90-100 | Yes — enterprise-grade |
| B+/B/B- | 80-89 | Yes — production-ready |
| C+/C | 73-79 | Conditional — fix HIGH items first |
| D | 60-72 | No — major issues |
| F | <60 | No — critical issues |

## Quality Gates

| Gate | Minimum | Blocking Categories |
|------|---------|-------------------|
| Production | B+ (87) | No category below 6 |
| Enterprise | A- (90) | No category below 8 |

## Output Format

```markdown
## Data Flow Scorecard — [Project Name]

| # | Category | Weight | Score | Weighted | Issues |
|---|----------|--------|-------|----------|--------|
| 1 | Server Component Fetching | 15% | X/10 | Y | ... |
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

1. `src/app/**/page.tsx` — page-level data fetching
2. `src/app/api/**/route.ts` — API route handlers
3. `src/hooks/**` — client-side data hooks
4. `src/lib/**` — services, DB client, utilities
5. `src/lib/validations/**` — Zod schemas
6. `src/types/**` — shared type definitions
7. `src/components/**` — data consumption
8. `prisma/schema.prisma` — indexes, relations
9. `src/proxy.ts` — request pipeline
10. `src/lib/api/response.ts` — response envelope
