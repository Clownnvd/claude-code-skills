# Security Fix — Implementation Workflow

## Step 1: Parse Scorecard

Extract from security-scoring output:
- Per-category scores (which are below target?)
- Issues list sorted by severity
- File:line references for each issue

## Step 2: Prioritize

Sort issues by: `severity_rank * category_weight`

Severity ranks: CRITICAL=4, HIGH=3, MEDIUM=2, LOW=1

Example: HIGH issue in Input Validation (15%) = 3 × 15 = 45
Example: MEDIUM issue in Supply Chain (7%) = 2 × 7 = 14

Fix score=45 before score=14.

## Step 3: Fix (batch by file)

Group issues by file to minimize edits. For each file:
1. Read the file
2. Apply all fixes for that file
3. Verify with typecheck

### Fix Order Within File
1. Security-critical (data leaks, injection)
2. Validation gaps
3. Header/config issues
4. Logging improvements

## Step 4: Verify Each Fix

After each batch:
```bash
pnpm typecheck   # 0 errors
pnpm test        # all pass
```

## Step 5: Re-score

Run security-scoring again to verify improvements.

## Step 6: Loop or Complete

- If score >= target → done
- If score < target → return to Step 1 with new scorecard

## Common Fix Sequences

### Input Validation Fix
1. Create/update Zod schema in `src/lib/validations/`
2. Import schema in API route
3. Replace `req.json()` with `schema.safeParse(await req.json())`
4. Handle validation errors with `validationError()`

### Secrets Fix
1. Move hardcoded value to `.env`
2. Add to `.env.example` with description
3. Add to `src/lib/env.ts` Zod schema
4. Update `env.d.ts` type declaration
5. Import from `env.ts` instead of hardcoded

### CSP Fix
1. Open `src/proxy.ts`
2. Add/update CSP directives in header construction
3. Test page still renders correctly
4. Verify with browser DevTools CSP tab

### Error Handling Fix
1. Replace `throw error` with `errorResponse()` from response.ts
2. Remove `console.error(error)` — use structured logger
3. Ensure no stack trace or internal path in response body
4. Wrap external API calls in try/catch with generic error

### Webhook Fix
1. Verify signature before any processing
2. Add idempotency check (lookup by event/payment ID)
3. Add timeout to external API calls
4. Catch and log (not forward) external errors
