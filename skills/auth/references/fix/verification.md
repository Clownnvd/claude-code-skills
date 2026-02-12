# Verification & Re-Scoring

## Post-Fix Verification Checklist

### 1. TypeScript
```bash
npx tsc --noEmit
```
Must pass with zero errors.

### 2. Tests
```bash
pnpm test:run
```
All existing tests must pass. No regressions.

### 3. Build
```bash
pnpm build
```
Build must succeed.

### 4. Auth Flow Spot-Check
- Does login still work? (session created)
- Does logout invalidate session?
- Do protected routes redirect unauthenticated users?
- Does OAuth flow complete? (if applicable)

## Re-Scoring Protocol

After all fixes pass verification, invoke `auth-scoring` skill.

### Comparison Template
```markdown
## Auth Fix Results

| # | Category | Before | After | Delta |
|---|----------|--------|-------|-------|
| 1 | Session Management (15%) | X/10 | Y/10 | +Z |
| 2 | Password Security (12%) | X/10 | Y/10 | +Z |
| ... | | | | |
| **Total** | | **XX/100** | **YY/100** | **+ZZ** |
| **Grade** | | **C+** | **B+** | |

### Fixes Applied
1. [Fix description] — [files changed]

### Remaining Issues
1. [Issue] — [reason not fixed]
```

## Loop Mode Protocol

When "fix until 100" is requested:
1. Each iteration: parse new scorecard -> fix remaining deductions -> verify -> re-score
2. Track iteration count (max 5)
3. Track score delta per iteration — if delta = 0 for 2 consecutive iterations, stop
4. Final output: full before/after comparison across ALL iterations

## Commit Message Template
```
fix(auth): improve auth score from XX to YY

- [Fix 1 description]
- [Fix N description]

Score: XX/100 (C+) -> YY/100 (A+)
```
