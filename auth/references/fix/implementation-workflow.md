# Implementation Workflow

## Step 1: Parse Scorecard

Extract from the auth-scoring output:
- **Scorecard table** — 10 category scores + overall grade
- **Critical Issues** — must fix (score 0-3 or auth bypass)
- **Improvements** — should fix (score 4-6)
- **Nice-to-have** — polish items (score 7-8)

## Step 2: Prioritize

Fix order: Critical -> Improvements -> Nice-to-have.

Within each severity, prioritize by:
1. **Weight** — higher-weight categories first (Session 15% > 2FA 5%)
2. **Blast radius** — fixes affecting multiple flows before single-page fixes
3. **Dependencies** — fixes that unblock other fixes first

### Priority Matrix

| Severity x Weight | Action |
|-------------------|--------|
| Critical + high weight (≥12%) | Fix immediately, block other work |
| Critical + low weight (<12%) | Fix immediately after high-weight |
| Improvement + high weight | Fix next, moves score most |
| Improvement + low weight | Fix after high-weight improvements |
| Nice-to-have | Fix last, skip if time-constrained |

## Step 3: Execute Fixes

For each fix:

### 3a. Read Before Edit
- Read the target file(s)
- Read `src/lib/auth.ts` if fix involves Better Auth config
- Read `src/proxy.ts` if fix involves route protection or headers
- Read related test files if they exist

### 3b. Apply Fix
- Use Edit tool for surgical changes (prefer over full Write)
- Load the relevant `references/fix-patterns/` file for the fix category
- Follow project coding style (immutable patterns, < 800 lines)

### 3c. Verify Fix
- Run `npx tsc --noEmit` after each fix
- Read the modified file to confirm correctness
- If fix touches auth flow, mentally trace the full flow

## Step 4: Batch Verification

After all fixes:
1. TypeScript: `npx tsc --noEmit`
2. Tests: `pnpm test:run`
3. Build: `pnpm build`

## Step 5: Re-Score

Invoke `auth-scoring` skill to produce new scorecard.

## Step 6: Compare & Iterate

Use comparison template from `references/verification.md`.

## Which Fix-Pattern References to Load

| Scorecard Category | Load |
|-------------------|------|
| Session Management, Password Security | `fix-patterns/sessions-passwords.md` |
| OAuth, Email Verification | `fix-patterns/oauth-email.md` |
| CSRF, Security Headers | `fix-patterns/csrf-headers.md` |
| Rate Limiting, Audit Logging | `fix-patterns/ratelimit-audit.md` |
| Authorization, 2FA | `fix-patterns/authz-2fa.md` |
