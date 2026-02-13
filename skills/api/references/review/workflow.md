# API Review Workflow

## Process

1. **Read** — Load target route file(s), identify exports (GET/POST/PUT/DELETE), imports, patterns
2. **Classify** — All 10 api categories typically apply to route files. Mark N/A only if truly irrelevant.
3. **Score** — Rate each category 0-10:
   - 0-3 CRITICAL: Missing auth, no validation, security hole
   - 4-5 HIGH: Partial implementation, inconsistent patterns
   - 6-7 MEDIUM: Basic implementation, room for improvement
   - 8 LOW: Solid, minor optimizations possible
   - 9-10 PASS: Excellent, best practices followed
4. **Annotate** — For each deduction, cite exact line + explain + severity
5. **Suggest** — Concrete code fix for each issue (copy-paste ready)
6. **Summarize** — Score, top 3 priorities, quick wins

## Common API Route Issues (check these first)

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | No auth check | Auth & AuthZ | CRITICAL |
| 2 | No Zod validation | Input Validation | CRITICAL |
| 3 | No rate limiting | Rate Limiting | HIGH |
| 4 | Generic error response | Error Handling | HIGH |
| 5 | No structured logging | Observability | MEDIUM |
| 6 | Missing Cache-Control header | Response Design | MEDIUM |
| 7 | No TypeScript return type | Documentation | LOW |
| 8 | No select on Prisma query | Performance | MEDIUM |

## Multi-File Review

When reviewing 2 files (e.g., route.ts + its test file):
- Review each independently
- Check type alignment between request/response shapes
- Verify test coverage matches route complexity
