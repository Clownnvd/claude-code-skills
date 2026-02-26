# Implementation Workflow

## Step 1: Parse Scorecard

Extract from the api-scoring output:
- **Scorecard table** — 10 category scores + weighted total + grade
- **CRITICAL issues** — must fix before deploy (score 0-3 or security hole)
- **HIGH issues** — fix this sprint (score 4-5, weight >= 12%)
- **MEDIUM issues** — fix next sprint
- **LOW issues** — backlog
- **Quick wins** — highest delta per effort

## Step 2: Prioritize

Fix order: CRITICAL → HIGH → MEDIUM → LOW.

Within each severity, prioritize by:
1. **Weight** — higher-weight categories first (Security 20% > Testing 5%)
2. **Blast radius** — fixes affecting multiple routes before single-route fixes
3. **Dependencies** — fixes that unblock other fixes first (e.g., response helpers before testing)

### Priority Matrix

| Severity x Weight | Action |
|-------------------|--------|
| CRITICAL + any weight | Fix immediately, block other work |
| HIGH + weight >= 12% | Fix next, these move the score most |
| HIGH + weight < 12% | Fix after high-weight items |
| MEDIUM | Fix if time allows |
| LOW | Skip unless targeting A+ |

## Step 3: Execute Fixes

For each fix:

### 3a. Read Before Edit
- Read the target file(s) — route handler, proxy, helper
- Read `src/lib/api/response.ts` if fix involves error handling
- Load the relevant `references/fix-patterns/` file for the category

### 3b. Apply Fix
- Use Edit tool for surgical changes (prefer over full Write)
- Follow project coding style (immutable patterns, < 800 lines)
- Maintain existing patterns (Zod validation, centralized helpers)

### 3c. Verify Each Fix
- Run `pnpm typecheck` after type changes
- Run `pnpm test` after logic changes
- Read the modified file to confirm correctness

## Step 4: Test Updates (if tests added/changed)

If new test files were created:
1. Run `pnpm test` — all pass, no regressions
2. Check coverage: `pnpm test --coverage` if available

## Step 5: Batch Verification

After all fixes:
1. `pnpm typecheck` — 0 errors
2. `pnpm test` — all pass, no regressions
3. `pnpm build` — builds successfully (optional for quick iteration)

## Step 6: Re-Score

Invoke `api-scoring` skill to produce new scorecard.

## Which Fix-Pattern References to Load

| Scorecard Category | Load |
|-------------------|------|
| Security, Auth & AuthZ | `fix-patterns/security-auth.md` |
| Input Validation, Error Handling | `fix-patterns/input-errors.md` |
| Rate Limiting, Response Design, Performance | `fix-patterns/ratelimit-response-perf.md` |
| Observability, Documentation, Testing | `fix-patterns/observability-docs-testing.md` |
