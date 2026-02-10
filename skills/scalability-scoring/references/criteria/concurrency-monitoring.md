# Concurrent & Parallel Processing (7%) + Performance Monitoring & Budgets (6%)

## Category 9: Concurrent & Parallel Processing (7%)

### Criteria (10 items, each worth 1 point)

1. **Promise.all for independent fetches** — Multiple unrelated async operations run in parallel, not sequential `await`
2. **Promise.allSettled for partial OK** — When some failures are acceptable, use `allSettled` instead of `all`
3. **No waterfall data fetching** — Page data requirements fetched in parallel at layout/page level, not sequentially in nested components
4. **Streaming for large data** — Large responses use `ReadableStream` / streaming instead of buffering everything
5. **Parallel DB queries** — Independent database queries run concurrently via `Promise.all`
6. **No blocking sequential awaits** — Code review shows no `await a; await b;` where a and b are independent
7. **Concurrent route handlers** — API routes that need multiple data sources fetch them in parallel
8. **Efficient webhook processing** — Webhook handlers process quickly, offload heavy work if needed
9. **Non-blocking side effects** — Non-critical operations (logging, analytics, emails) don't block the response
10. **Proper error handling in parallel** — `Promise.all` wrapped in try/catch, partial failures handled gracefully

### Deduction Examples
- `-3` Sequential `await` chain for 3+ independent operations
- `-2` Webhook handler doing synchronous heavy processing
- `-2` No Promise.all where multiple DB queries could run in parallel
- `-1` Missing error handling on Promise.all

---

## Category 10: Performance Monitoring & Budgets (6%)

### Criteria (10 items, each worth 1 point)

1. **Web Vitals tracking** — LCP, FID/INP, CLS tracked (via `next/web-vitals`, analytics, or custom reporting)
2. **Bundle size monitoring** — Bundle size tracked in CI or documented budget threshold
3. **API response time logging** — Request duration logged for API routes (structured logging with duration field)
4. **Error rate tracking** — Errors logged with structured data for aggregation and alerting
5. **Performance budget documented** — Target metrics documented (e.g., LCP < 2.5s, bundle < 200KB)
6. **Lighthouse CI** — Lighthouse or similar performance tool runs in CI pipeline
7. **Database query monitoring** — Slow queries identifiable through logging or Prisma query events
8. **Custom performance marks** — Key operations timed with `performance.mark`/`measure` or equivalent
9. **Health check endpoint** — `/api/health` or similar endpoint for uptime monitoring
10. **Structured logging** — All logs are structured (JSON in production) for log aggregation tools

### Deduction Examples
- `-3` No performance monitoring at all
- `-2` No structured logging for API routes
- `-1` No health check endpoint
- `-1` No documented performance budgets

### Framework Adjustment
Next.js built-in Web Vitals reporting = +1 if `reportWebVitals` configured or using Vercel Analytics.
