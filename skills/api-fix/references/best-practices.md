# Best Practices for API Fixes

## Fix Discipline

### Do
- Read the file completely before editing — understand surrounding code
- Fix one issue at a time — verify after each fix
- Run `pnpm typecheck` after type/interface changes
- Run `pnpm test` after logic changes
- Use Edit tool for surgical changes (prefer over full Write)
- Maintain consistency with existing patterns (Zod, centralized helpers)
- Update tests when changing response shapes or validation schemas

### Don't
- Don't batch unrelated fixes into one giant edit
- Don't add features while fixing — stick to the scorecard issues
- Don't refactor working code that isn't in the scorecard
- Don't break existing API contracts (response shapes consumed by frontend)
- Don't add dependencies unless the fix specifically requires one
- Don't over-engineer — fix the gap, not more

## Response Helper Changes

### Safe to change
- Adding new fields to error envelope (`code` field)
- Adding new helper functions (`requireJsonBody`, `logRequest`)
- Replacing inline `NextResponse.json` with existing helpers

### Dangerous — check frontend first
- Changing `success` field name/type
- Changing error shape (`error` string → object)
- Removing fields from success responses

## Middleware Changes

### Safe to change
- Adding headers (X-Request-Id, CORS)
- Tightening CSP (removing unsafe-inline)
- Adding logging

### Dangerous — may break app
- Changing matcher patterns (can block routes)
- Adding auth checks (can 403 public pages)
- Modifying CSP too aggressively (can break Stripe.js, OAuth redirects)

## Test Writing Guidelines

### API Route Test Template
```typescript
describe("METHOD /api/path", () => {
  it("returns 401 when not authenticated", async () => { ... });
  it("returns 400 for invalid input", async () => { ... });
  it("returns 200 with correct data", async () => { ... });
  it("returns 429 when rate limited", async () => { ... });
});
```

### What to mock
- `auth.api.getSession` — return null (401) or mock session (200)
- `prisma.*` — mock DB calls via prisma mock
- `stripe.*` — mock Stripe calls via stripe mock
- `global.fetch` — mock external API calls (GitHub)

### What NOT to mock
- Validation schemas — test with real Zod parsing
- Response helpers — test real output shapes
- Rate limit logic — test with real in-memory store

## Common Fix Mistakes

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Change error envelope without updating frontend | UI breaks | Search `error`, `success` usage in hooks |
| Add strict CSP without testing Stripe | Checkout broken | Test payment flow after CSP change |
| Add Content-Type check to webhook routes | Webhooks fail | Webhooks may send non-JSON content types |
| Add X-Request-Id but not to log entries | ID exists but useless | Include requestId in all structured logs |
| Write tests that test mocks, not logic | False confidence | Assert on business logic, not mock call counts |
| Add audit logging with PII | Privacy violation | Log event type + userId only, never email/name |

## Env Var Sync Checklist

When adding a new env var, update ALL of these:
1. `.env.example` — with placeholder value
2. `src/lib/env.ts` — Zod schema validation
3. `src/types/env.d.ts` — TypeScript type declaration
4. `vitest.config.ts` — test environment (if needed)

## Fix Verification Order

Always verify in this order:
1. `pnpm typecheck` — catches type mismatches
2. `pnpm test` — catches logic regressions
3. `pnpm build` — catches build-time issues (optional for quick iteration)
4. Manual test — critical paths (auth, payment, webhook) if changes are significant
