# Implementation Workflow

## Step 1: Parse Scorecard

Extract from the ui-scoring output:
- **Scorecard table** — 10 category scores + overall grade
- **Critical Issues** — must fix (score 0-3 or blocking usability)
- **Improvements** — should fix (score 4-6 or quality gaps)
- **Nice-to-have** — polish items (score 7-8)

## Step 2: Prioritize

Fix order: Critical → Improvements → Nice-to-have.

Within each severity, prioritize by:
1. **Weight** — higher-weight categories first (Visual Hierarchy 15% > Performance 5%)
2. **Blast radius** — fixes affecting multiple sections before single-component fixes
3. **Dependencies** — fixes that unblock other fixes first (e.g., responsive grid before mobile typography)

### Priority Matrix

| Severity × Weight | Action |
|-------------------|--------|
| Critical + high weight (≥10%) | Fix immediately, block other work |
| Critical + low weight (<10%) | Fix immediately after high-weight criticals |
| Improvement + high weight | Fix next, these move the score most |
| Improvement + low weight | Fix after high-weight improvements |
| Nice-to-have | Fix last, skip if time-constrained |

## Step 3: Execute Fixes

For each fix:

### 3a. Read Before Edit
- Read the target component file(s)
- Read `globals.css` if fix involves design tokens
- Read related UI primitives if fix involves shared components

### 3b. Apply Fix
- Use Edit tool for surgical changes (prefer over full Write)
- Follow project coding style (immutable patterns, < 800 lines)
- Load the relevant `references/fix-patterns/` file for the fix category

### 3c. Verify Fix
- Run `npx tsc --noEmit` after each fix to catch type errors
- Read the modified file to confirm the change is correct
- If fix touches multiple files, verify all before moving on

## Step 4: Batch Verification

After all fixes:
1. Run TypeScript check: `npx tsc --noEmit`
2. Run tests: `pnpm test` (if available)
3. Run build: `pnpm build` (if all tests pass)

## Step 5: Re-Score

Invoke `ui-scoring` skill on the same page to produce a new scorecard.

### Before/After Comparison Template

```
## Fix Results: [Page Name]

| # | Category | Before | After | Delta |
|---|----------|--------|-------|-------|
| 1 | Visual Hierarchy | 6/10 | 8/10 | +2 |
| ... | ... | ... | ... | ... |
| **Total** | | **62/100** | **81/100** | **+19** |

### Fixes Applied
1. [Fix description] — [files changed]
2. ...

### Remaining Issues
1. [Issue not fixed] — [reason: external dependency / out of scope / needs design decision]
```

## Which Fix-Pattern References to Load

| Scorecard Category | Load |
|-------------------|------|
| Visual Hierarchy, Color, Typography, Spacing | `fix-patterns/visual-polish.md` |
| Responsiveness | `fix-patterns/responsiveness.md` |
| Interactions, Accessibility | `fix-patterns/accessibility.md` |
| Content, Conversion | `fix-patterns/content-copy.md` |
| Performance | `fix-patterns/performance.md` |
