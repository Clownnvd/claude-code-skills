# Pipeline Workflow

## Full Pipeline (research → build → score → fix)

### Phase 1: Research (invoke ui-research)

1. Define scope: page type, target audience, design vibe
2. Search 3+ gallery sites for inspiration
3. Fetch 3-5 real product pages
4. Extract patterns (layout, color, typography, components)
5. Output: **Design Brief** (see handoff-contracts.md)

**Skip condition**: User provides design brief or existing mockup → jump to Phase 2.

### Phase 2: Build (implement design brief)

1. Read existing codebase structure (`globals.css`, components dir, layout)
2. Create/modify components following the design brief
3. Apply design tokens from project theme (never hardcoded colors)
4. Ensure both light/dark mode work
5. Output: **Component file paths** for all created/modified files

**Parallel opportunity**: If multiple independent sections, build in parallel using Task agents.

### Phase 3: Score (invoke ui-scoring)

1. Read all component files from Phase 2
2. Read `globals.css` for design token verification
3. Score all 10 categories (0-10 each)
4. Output: **Scorecard** with per-category scores + issues list

**Decision point**:
- Score >= target? → Phase 5 (Ship)
- Score < target? → Phase 4 (Fix)

### Phase 4: Fix Loop (invoke ui-fix)

1. Parse scorecard → prioritize by severity × weight
2. Fix all issues (Critical → Improvement → Nice-to-have)
3. Verify: `npx tsc --noEmit`
4. Re-score (back to Phase 3)
5. Repeat until score >= target OR 5 iterations OR plateau

**Plateau detection**: If score delta = 0 for 2 consecutive iterations, stop and report remaining issues as "design decisions needed".

### Phase 5: Ship

1. Run full verification: TypeScript + tests + build
2. Run Lighthouse audit (if available): `references/measurement.md`
3. Output final scorecard comparison (first score → final score)
4. Suggest commit message

## Audit Pipeline (score → fix only)

Skip Phases 1-2. Start at Phase 3 with existing code.

1. Identify all component files for the page
2. Score → Fix loop until target
3. Ship

## Research Pipeline (research only)

Run Phase 1 only. Output design brief without implementing.

## Polish Pipeline (quick fix)

1. Score (Phase 3)
2. Fix only Critical + Improvement issues (skip Nice-to-have)
3. Re-score once
4. Ship

## Error Handling

| Error | Recovery |
|-------|----------|
| TypeScript fails after fix | Revert fix, try alternative approach |
| Score decreases after fix | Revert iteration, investigate root cause |
| WebSearch rate limited | Fall back to existing `inspiration-sources.md` |
| Build fails | Fix build error before continuing pipeline |
| 5 iterations without target | Stop, output "design decisions needed" report |

## Timing Expectations

| Phase | Typical Duration |
|-------|-----------------|
| Research | 2-3 min (web searches) |
| Build | 5-15 min (depends on scope) |
| Score | 1-2 min (code analysis) |
| Fix iteration | 3-5 min per iteration |
| Full pipeline | 15-30 min total |
