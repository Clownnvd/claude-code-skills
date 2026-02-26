# Rate Limiting + Response Design + Performance

Covers categories 5 (Rate Limiting, 10%), 6 (Response Design, 8%), 7 (Performance, 8%).

## Category 5: Rate Limiting & Resource Protection (10%)

### Checklist (subtract 1 per missing item from baseline 5)

- [ ] Rate limiting on ALL endpoints (not just auth)
- [ ] Tiered limits by sensitivity: strict (auth/checkout), standard (CRUD), relaxed (reads)
- [ ] Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- [ ] 429 response with `Retry-After` header
- [ ] Per-IP limits for unauthenticated; per-user for authenticated
- [ ] Pagination enforced on all list endpoints (max page size)

### Bonus

- [ ] Distributed rate limiting (Redis-backed, not per-instance)
- [ ] Cost-based limiting (expensive ops count more)
- [ ] Circuit breaker on outbound API calls

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | No rate limiting; unbounded queries possible |
| 4-5 | Rate limiting on some endpoints; no headers; no pagination caps |
| 6-7 | All endpoints rate-limited; 429 + Retry-After; pagination enforced |
| 8-9 | Tiered limits; distributed store; rate limit headers on all responses |
| 10 | All above + cost-based + circuit breakers + per-user + per-IP |

---

## Category 6: Response Design (8%)

### Checklist

- [ ] Consistent response envelope across ALL endpoints (e.g. `{ success, data, error }`)
- [ ] Pagination on collection endpoints (cursor-based or offset-based)
- [ ] Consistent data types: ISO 8601 dates, integer cents for money, string IDs
- [ ] HTTP caching headers where appropriate (`Cache-Control`, `ETag`)
- [ ] Sensitive data stripped from responses (no internal IDs, tokens, secrets)
- [ ] Proper `Content-Type: application/json` on all JSON responses

### Bonus

- [ ] `select` / field filtering support (`?fields=id,name`)
- [ ] Filtering + sorting with allowlisted fields
- [ ] HATEOAS / hypermedia links for discoverability

### Evidence Patterns

```typescript
// GOOD: Consistent envelope
return successResponse({ users, meta: { total, page, limit } });

// BAD: Inconsistent
// Route A: { data: [...] }
// Route B: { users: [...] }
// Route C: [...]  (raw array)
```

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | No consistent format; raw arrays; no pagination; dates as strings |
| 4-5 | Some consistency but mixed formats; basic pagination |
| 6-7 | Consistent envelope; pagination; proper data types; caching headers |
| 8-9 | Field filtering; sorting; select support; all collections paginated |
| 10 | All above + HATEOAS + content negotiation + ETag support |

---

## Category 7: Performance (8%)

### Checklist

- [ ] No N+1 queries (eager/batch loading for related resources)
- [ ] Database queries use indexes (WHERE/ORDER BY on indexed columns)
- [ ] Connection pooling configured (not open/close per request)
- [ ] `select` clause on DB queries (no `SELECT *` equivalent)
- [ ] Timeouts at every boundary (DB, external APIs, request-level)
- [ ] Long operations return 202 + polling (never block > 30s)

### Bonus

- [ ] Application-level caching (Redis/memory) for hot data
- [ ] Response compression (gzip/brotli for > 1KB)
- [ ] Slow query detection and logging
- [ ] p95 < 500ms documented/measured

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | N+1 queries; no connection pooling; SELECT * everywhere |
| 4-5 | Basic pooling; some select clauses; no timeout config |
| 6-7 | No N+1; indexed queries; connection pool; select clauses |
| 8-9 | Caching; compression; slow query detection; timeouts configured |
| 10 | All above + p95 measured < 500ms + async for heavy ops |
