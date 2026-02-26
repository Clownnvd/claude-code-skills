# Observability + Documentation + Testing

Covers categories 8 (Observability, 7%), 9 (Documentation & DX, 5%), 10 (Testing, 5%).

## Category 8: Observability (7%)

### Checklist (subtract 1 per missing item from baseline 5)

- [ ] Structured logging (JSON in production with timestamp, level, request_id, method, path, status, duration_ms)
- [ ] No `console.log` in production API routes (use structured logger)
- [ ] Health check endpoint (`GET /api/health`) that verifies DB connectivity
- [ ] No sensitive data in logs (PII, tokens, passwords sanitized)
- [ ] Log levels used correctly (ERROR = needs action, WARN = degraded, INFO = events)
- [ ] Slow query / slow request detection with threshold alerts

### Bonus

- [ ] Request/correlation ID generated and propagated (`X-Request-Id`)
- [ ] Distributed tracing (OpenTelemetry spans)
- [ ] RED metrics (Rate, Errors, Duration) per endpoint
- [ ] Audit logging for security-sensitive actions
- [ ] Readiness probe separate from liveness (`/ready` checks DB + dependencies)

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | No logging; console.log everywhere; no health check |
| 4-5 | Basic logging but unstructured; health check exists but naive |
| 6-7 | Structured JSON logs; health check with DB ping; no PII in logs |
| 8-9 | Request IDs; slow query detection; audit logging; proper levels |
| 10 | All above + distributed tracing + RED metrics + alerting rules |

---

## Category 9: Documentation & Developer Experience (5%)

### Checklist

- [ ] All endpoints documented (method, path, params, body, responses)
- [ ] Example requests and responses for each endpoint
- [ ] Authentication flow documented (how to get + use credentials)
- [ ] Error codes documented with causes and fixes
- [ ] Environment setup guide (.env.example with comments)
- [ ] Consistent naming: camelCase or snake_case everywhere (not mixed)

### Bonus

- [ ] OpenAPI 3.1 spec file (auto-validated in CI)
- [ ] Interactive docs (Swagger UI / Redoc)
- [ ] Versioning strategy documented (path-based or header-based)
- [ ] Rate limit documentation per endpoint
- [ ] SDK generation from spec

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | No docs; no examples; no .env.example; mixed naming |
| 4-5 | Some docs but incomplete; .env.example exists; inconsistent naming |
| 6-7 | All endpoints documented; examples; auth guide; consistent naming |
| 8-9 | OpenAPI spec; interactive docs; error catalog; versioning strategy |
| 10 | All above + SDK generation + < 5min onboarding + changelog |

---

## Category 10: Testing (5%)

### Checklist

- [ ] Unit tests for business logic and validation schemas (> 80% on critical paths)
- [ ] Integration tests for every endpoint (happy path + error paths)
- [ ] Auth tests: 401 unauthenticated, 403 unauthorized, BOLA prevention
- [ ] Input validation tests: empty, null, wrong type, boundary values, injection payloads
- [ ] Rate limiting tests: 429 returned, Retry-After header present
- [ ] Tests run in CI on every PR

### Bonus

- [ ] Contract tests (responses match OpenAPI spec)
- [ ] Performance regression tests (p95 latency threshold)
- [ ] Security scanning in CI (SAST/DAST)
- [ ] Idempotency tests for POST/PUT with duplicate keys
- [ ] Mock isolation (external APIs mocked, DB mocked or test-container)

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | No tests; or tests exist but don't cover API endpoints |
| 4-5 | Some unit tests; no integration tests; no auth/validation tests |
| 6-7 | Unit + integration tests; auth tests; validation tests; CI runs |
| 8-9 | Contract tests; rate limit tests; idempotency tests; > 80% coverage |
| 10 | All above + perf regression + security scanning + test-containers |
