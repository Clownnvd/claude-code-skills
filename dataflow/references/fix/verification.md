# Data Flow Fix — Verification & Re-Scoring

## Post-Fix Verification Checklist

### 1. TypeScript
```bash
npx tsc --noEmit
```
Must pass with zero errors.

### 2. Tests
```bash
pnpm test
```
All existing tests must pass. No regressions.

### 3. Build
```bash
pnpm build
```
Build must succeed.

### 4. Data Flow Spot-Check
- Do API routes return consistent `{ success, data, error }` shapes?
- Are Prisma queries using `select`?
- Do error boundaries catch route-level errors?
- Are dates serialized as ISO strings?
- Do forms show loading states and field-level errors?

## Re-Scoring Protocol

After all fixes pass verification, invoke `dataflow-scoring` skill.

### Comparison Template
```markdown
## Data Flow Fix Results

| # | Category | Before | After | Delta |
|---|----------|--------|-------|-------|
| 1 | Server Component Fetching (15%) | X/10 | Y/10 | +Z |
| 2 | Server/Client Composition (10%) | X/10 | Y/10 | +Z |
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
