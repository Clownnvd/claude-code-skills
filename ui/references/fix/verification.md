# Verification & Re-Scoring

## Pre-Flight Checks (run BEFORE fixing UI)

These catch environment/config issues that break UI at runtime but pass typecheck:

### 0a. Dependency Version Alignment
```bash
pnpm ls --depth 0 | grep -E "prisma|next|react"
```
Check for version mismatches between related packages:
- `@prisma/client`, `@prisma/adapter-neon`, `prisma` — MUST be same major.minor
- `react`, `react-dom` — MUST be same version
- `next`, `eslint-config-next` — MUST be same major

If mismatched: `pnpm add <package>@<aligned-version>`

### 0b. Dev Server Smoke Test
```bash
pnpm dev &
sleep 15
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
```
Must return **200**. Common failures:
- `EvalError: Code generation from strings disallowed` — `--webpack` flag + Edge runtime. Fix: remove `--webpack`, use Turbopack (Next.js 16+ default)
- `TypeError: generate is not a function` — leaked `__NEXT_PRIVATE_*` env vars from agent terminals. Fix: unset them or clear via `cross-env` in build script
- `500` on page load — check terminal output for the actual error

### 0c. Leaked Environment Variables
```bash
env | grep __NEXT_PRIVATE
```
If `__NEXT_PRIVATE_STANDALONE_CONFIG`, `__NEXT_PRIVATE_ORIGIN`, or `NEXT_OTEL_FETCH_DISABLED` are set, the build/dev will break. Fix:
```json
"build": "cross-env __NEXT_PRIVATE_STANDALONE_CONFIG= __NEXT_PRIVATE_ORIGIN= NEXT_OTEL_FETCH_DISABLED= next build"
```

---

## Post-Fix Verification Checklist

### 1. TypeScript
```bash
npx tsc --noEmit
```
Must pass with zero errors. Fix type errors before proceeding.

### 2. Tests
```bash
pnpm test
```
All existing tests must pass. No regressions.

### 3. Build
```bash
pnpm build
```
Build must succeed. Watch for:
- Missing imports (deleted/moved components)
- CSS class name typos
- Dynamic import errors

### 4. Visual Spot-Check

For each fix, mentally verify:
- Does the fix address the specific issue from the scorecard?
- Does it introduce new issues? (e.g., mobile fix breaking desktop)
- Does it maintain dark mode compatibility?
- Does it respect the design system? (tokens, not hardcoded values)

## Re-Scoring Protocol

After all fixes pass verification, invoke `ui-scoring` skill on the same page.

### Comparison Template

```markdown
## Fix Results: [Page Name]

### Score Comparison
| # | Category | Before | After | Delta |
|---|----------|--------|-------|-------|
| 1 | Visual Hierarchy (15%) | X/10 | Y/10 | +Z |
| 2 | Color & Theme (10%) | X/10 | Y/10 | +Z |
| 3 | Typography (10%) | X/10 | Y/10 | +Z |
| 4 | Spacing & Layout (12%) | X/10 | Y/10 | +Z |
| 5 | Responsiveness (12%) | X/10 | Y/10 | +Z |
| 6 | Interactions (8%) | X/10 | Y/10 | +Z |
| 7 | Accessibility (10%) | X/10 | Y/10 | +Z |
| 8 | Content & Copy (8%) | X/10 | Y/10 | +Z |
| 9 | Conversion & CTA (10%) | X/10 | Y/10 | +Z |
| 10 | Performance (5%) | X/10 | Y/10 | +Z |
| **Total** | | **XX/100** | **YY/100** | **+ZZ** |
| **Grade** | | **C+** | **B+** | |

### Fixes Applied (N total)
1. [Description] — [files changed]
2. ...

### Remaining Issues
1. [Issue] — [reason not fixed]

### Score Target Met?
- [ ] Target: ≥ B (83+)
- [ ] All criticals resolved
- [ ] No new issues introduced
```

## Score Targets

| Target | Score | When |
|--------|-------|------|
| Minimum viable | 70+ (C) | Internal/prototype |
| Production-ready | 83+ (B) | Public launch |
| Premium | 90+ (A-) | Premium product |
| Showcase | 95+ (A+) | Portfolio / showcase |

## Iteration Decision

After re-scoring:

| Result | Action |
|--------|--------|
| Score ≥ target | Done. Output final comparison and stop. |
| Score improved but < target | **Auto-iterate**: go to Step 1 with new scorecard |
| Score didn't improve after 2 iterations | Stop. Report remaining items as "design decisions needed". |
| Score decreased | Revert. Fix introduced new issues. |

### Loop Mode Protocol

When "fix until 100%" is requested:
1. Each iteration: parse new scorecard → fix remaining deductions → verify → re-score
2. Track iteration count (max 5)
3. Track score delta per iteration — if delta = 0 for 2 consecutive iterations, stop
4. Final output: full before/after comparison across ALL iterations

## Commit Message Template

```
fix(ui): improve [page] UI score from XX to YY

- [Fix 1 description]
- [Fix 2 description]
- [Fix N description]

Score: XX/100 (C+) → YY/100 (B+)
```
