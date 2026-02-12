# Eval: Infrastructure Fix Patterns

Verify specific fix patterns from `references/fix-patterns/` produce correct code changes.

## Pattern 1: GitHub Actions CI Workflow (ci-cd.md)

**Setup**: No CI pipeline. Code pushed directly to main without lint, typecheck, or test gates.

**Steps**:
1. Apply CI Workflow pattern.
2. Verify `.github/workflows/ci.yml` created.
3. Verify parallel jobs for lint, typecheck, test.
4. Verify build job depends on all three gates (`needs: [lint, typecheck, test]`).
5. Verify `pnpm install --frozen-lockfile` used (not `pnpm install`).

**Pass**: CI runs on push and PR to main. Jobs run in parallel. Build blocked until gates pass. Concurrency cancels in-progress runs. Each job has `timeout-minutes`.

**Fail**: Jobs run sequentially, or no `needs` dependency, or `frozen-lockfile` missing.

## Pattern 2: Env Validation with Zod (env-monitoring.md)

**Setup**: No runtime validation of environment variables. App crashes with cryptic errors when env vars missing.

**Steps**:
1. Apply Env Validation pattern.
2. Verify `src/lib/env.ts` created with `serverSchema` and `clientSchema`.
3. Verify schema uses format checks (e.g., `z.string().startsWith("sk_")` for Stripe key).
4. Verify validation runs at import time (module-level `parse()`).

**Pass**: App fails fast at startup with clear message when env vars missing. Stripe key validated with prefix. `NEXT_PUBLIC_` vars validated separately. `.env.example` in sync with schema.

**Fail**: Validation only at request time, or no format checks, or client vars validated server-side only.

## Pattern 3: Health and Readiness Endpoints (env-monitoring.md)

**Setup**: No health check endpoint. Deployment platform cannot verify app is running.

**Steps**:
1. Apply Health/Readiness endpoint pattern.
2. Verify `/api/health` returns `{ status: "healthy", timestamp, uptime }`.
3. Verify `/api/ready` checks database connectivity with `SELECT 1`.
4. Verify readiness returns 503 when database unreachable.

**Pass**: Health endpoint returns 200 always. Readiness endpoint returns 200 when DB connected, 503 when not. Both return JSON. Docker HEALTHCHECK or deployment platform can use these.

**Fail**: No readiness check, or readiness doesn't test DB, or returns 200 when DB is down.

## Pattern 4: Webhook Idempotency (backup-integrations.md)

**Setup**: Stripe webhook creates duplicate purchases when same event delivered twice.

**Steps**:
1. Apply Idempotency pattern.
2. Verify check-before-create: `findUnique` by `stripePaymentId` before `create`.
3. Verify duplicate returns `{ received: true }` without error.
4. Verify side effects (email, GitHub invite) not re-triggered on duplicate.

**Pass**: Second delivery of same webhook event returns 200 without creating duplicate purchase. Logged as "Duplicate webhook, already processed". Side effects skipped.

**Fail**: Duplicate purchase created, or duplicate returns error status, or side effects fire again.
