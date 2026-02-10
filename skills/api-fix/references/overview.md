# API Fix — Overview

## Purpose

Take an api-scoring scorecard (10-category audit) and systematically implement all fixes. Prioritize by severity + weight, apply code changes, verify, and re-score.

## How It Works

```
api-scoring output → parse scorecard → prioritize issues → apply fixes → verify → re-score
```

### Input: api-scoring Scorecard

The scorecard contains:
- **10 category scores** (0-10 each, weighted to 0-100 total)
- **Letter grade** (A+ to F)
- **Issues list** with severity (CRITICAL / HIGH / MEDIUM / LOW)
- **Quick wins** (highest impact, lowest effort)

### Output: Fixed Codebase + Before/After Comparison

## Fix Priority Order

| Priority | Severity | Score Range | Action |
|----------|----------|-------------|--------|
| 1 | CRITICAL | 0-3 or security hole | Fix immediately — blocks deploy |
| 2 | HIGH + high weight (>=12%) | 4-5 | Fix next — moves score most |
| 3 | HIGH + low weight (<12%) | 4-5 | Fix after high-weight items |
| 4 | MEDIUM | 6-7 | Fix next sprint |
| 5 | LOW | 8 | Backlog or skip |

## Category → Fix Pattern Reference

| Scorecard Category | Fix Pattern Reference |
|-------------------|----------------------|
| Security, Auth & AuthZ | `fix-patterns/security-auth.md` |
| Input Validation, Error Handling | `fix-patterns/input-errors.md` |
| Rate Limiting, Response Design, Performance | `fix-patterns/ratelimit-response-perf.md` |
| Observability, Documentation, Testing | `fix-patterns/observability-docs-testing.md` |

## Files Touched During Fix

| File Type | Examples |
|-----------|---------|
| API routes | `src/app/api/**/*.ts` |
| Proxy | `src/proxy.ts` |
| Auth config | `src/lib/auth.ts` |
| Response helpers | `src/lib/api/response.ts` |
| Rate limiting | `src/lib/rate-limit.ts` |
| CSRF | `src/lib/csrf.ts` |
| Validations | `src/lib/validations/*.ts` |
| Tests | `src/app/api/**/__tests__/*.test.ts` |
| Docs | `README.md` |

## Score Targets

| Target | Score | When |
|--------|-------|------|
| Minimum viable | 73+ (C+) | Internal/prototype |
| Production-ready | 87+ (B+) | Public launch |
| Enterprise-grade | 90+ (A-) | Enterprise/public API |
| Perfect | 100 (A+) | Best-in-class |

## Integration with api-scoring

1. Run `api-scoring` → get scorecard
2. Run `api-fix` → implement fixes from scorecard
3. Run `api-scoring` again → verify improvement
4. Repeat if score < target (max 3 iterations)
