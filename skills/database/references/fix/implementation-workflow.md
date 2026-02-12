# Implementation Workflow

## Step 1: Parse Scorecard

Extract from the db-scoring output:
- **Scorecard table** — 10 category scores + weighted total + grade
- **CRITICAL issues** — must fix before deploy (score 0-3 or security hole)
- **HIGH issues** — fix this sprint (score 4-5, weight >= 12%)
- **MEDIUM issues** — fix next sprint
- **LOW issues** — backlog
- **Quick wins** — highest delta per effort

## Step 2: Prioritize

Fix order: CRITICAL → HIGH → MEDIUM → LOW.

Within each severity, prioritize by:
1. **Weight** — higher-weight categories first (Security 15% > DevEx 5%)
2. **Blast radius** — fixes affecting multiple files/queries before single-file fixes
3. **Dependencies** — fixes that unblock other fixes first (e.g., migration sync before monitoring)

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
- Read the target file(s) — schema, config, API route, service
- Read `src/lib/env.ts` if fix involves env vars
- Read `prisma.config.ts` if fix involves connection config

### 3b. Apply Fix
- Use Edit tool for surgical changes (prefer over full Write)
- Follow project coding style (immutable patterns, < 800 lines)
- Load the relevant `references/fix-patterns/` file for the category

### 3c. Verify Each Fix
- Run `pnpm typecheck` after schema/type changes
- Run `pnpm test` after logic changes
- Read the modified file to confirm correctness

## Step 4: Migration Sync (if schema changed)

If any schema.prisma changes were made:
1. Run `npx prisma migrate dev --name <descriptive_name>`
2. Verify migration SQL is correct (read the generated file)
3. Run `npx prisma generate` to regenerate types

## Step 5: Batch Verification

After all fixes:
1. `pnpm typecheck` — 0 errors
2. `pnpm test` — all pass, no regressions
3. `pnpm build` — builds successfully

## Step 6: Re-Score

Invoke `db-scoring` skill to produce new scorecard.

### Before/After Comparison Template

```
## Fix Results: Database Audit

| # | Category | Weight | Before | After | Delta |
|---|----------|--------|--------|-------|-------|
| 1 | Schema Design | 15% | X/10 | Y/10 | +Z |
| 2 | Data Integrity | 12% | X/10 | Y/10 | +Z |
| 3 | Indexing Strategy | 12% | X/10 | Y/10 | +Z |
| 4 | Security | 15% | X/10 | Y/10 | +Z |
| 5 | Query Performance | 10% | X/10 | Y/10 | +Z |
| 6 | Migration | 10% | X/10 | Y/10 | +Z |
| 7 | Monitoring | 8% | X/10 | Y/10 | +Z |
| 8 | Backup | 8% | X/10 | Y/10 | +Z |
| 9 | Scalability | 5% | X/10 | Y/10 | +Z |
| 10 | DevEx | 5% | X/10 | Y/10 | +Z |
| **Total** | | | **XX/100** | **YY/100** | **+ZZ** |
| **Grade** | | | **C+** | **B+** | |

### Fixes Applied (N total)
1. [Fix description] — [files changed]

### Remaining Issues
1. [Issue] — [reason: needs prod access / design decision / external dependency]
```

## Which Fix-Pattern References to Load

| Scorecard Category | Load |
|-------------------|------|
| Schema Design, Data Integrity | `fix-patterns/schema-integrity.md` |
| Security | `fix-patterns/security.md` |
| Indexing, Query Performance, Scalability | `fix-patterns/performance-scaling.md` |
| Migration, Monitoring, Backup, DevEx | `fix-patterns/operations.md` |
