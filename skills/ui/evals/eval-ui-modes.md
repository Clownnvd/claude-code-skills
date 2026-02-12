# Eval: UI Modes

Validate all 4 modes of the ui skill produce correct output.
## Mode: Research

### Test 1: Design Brief Output

**Input**: "Research UI for a SaaS landing page"
**Expected**:
- Output contains all required sections: Direction, Component Plan, Design Tokens, Anti-Patterns
- Direction includes vibe, layout, primary color from CSS variables, 3+ inspiration URLs
- Component Plan table has >= 3 rows with Component, Pattern, Source columns
- Design Tokens extracted from `globals.css` (not hardcoded)
- Anti-Patterns lists >= 2 items with reasons

**Pass criteria**: All 5 required sections present. No placeholder text.

### Test 2: Token Extraction

**Input**: Project with `globals.css` containing custom properties
**Expected**:
- Design Tokens table references `var(--primary)`, `var(--accent)`, etc.
- Values match actual `globals.css` content
- No hardcoded hex or oklch values outside of the Value column

**Pass criteria**: Every color in Component Plan uses CSS variable references.

## Mode: Score

### Test 3: 10-Category Scorecard

**Input**: "Score my landing page" (with existing component files)
**Expected**:
- Scorecard table has exactly 10 rows matching the weighted categories
- Each row has: #, Category, Score (0-10), Grade, Key Issues
- Total score is weighted sum (not simple average)
- Grade matches the score using the defined scale (A+ 97-100 ... F <60)
- Issues classified into Critical / Improvements / Nice-to-have

**Pass criteria**: Weighted total correct. Grade matches scale. All 10 categories scored.

### Test 4: Anti-Bias Baseline

**Input**: Score a well-built page with standard components
**Expected**:
- Baseline starts at 7/10 per category (not inflated 9-10)
- Scores of 9-10 require specific evidence cited in the issues column
- No category gets 10/10 without explicit justification

**Pass criteria**: Average score <= 8.0 for a standard page. No unjustified 9+ scores.

## Mode: Fix

### Test 5: Scorecard-Driven Fixes

**Input**: Scorecard with Visual Hierarchy 4/10, Accessibility 3/10
**Expected**:
- Fixes prioritized: Accessibility (Critical, 10% weight) before Visual Hierarchy (Major, 15% weight)
- Each fix references the specific scorecard issue
- Files modified with Edit tool (not full rewrites)
- `npx tsc --noEmit` run after each fix
- Before/after comparison table output

**Pass criteria**: Critical issues fixed first. TypeScript check passes. Delta shown.

### Test 6: Fix Loop Iteration

**Input**: "Fix until score reaches 85+"
**Expected**:
- Loop runs: fix -> verify -> re-score -> check target
- Stops when score >= 85, or delta=0 for 2 rounds, or 5 iterations max
- Each iteration tracked in iteration log
- Final output shows full before/after comparison

**Pass criteria**: Loop terminates correctly. No infinite iteration.

## Mode: Pipeline

### Test 7: Full Pipeline (research -> build -> score -> fix)

**Input**: "Run full UI pipeline for pricing page, target 83+"
**Expected**:
- Phase 1: Design Brief produced
- Phase 2: Components built following the brief
- Phase 3: Scorecard generated
- Phase 4: Fix loop until 83+ or plateau
- Phase 5: Final verification (tsc, tests, build) and commit suggestion

**Pass criteria**: All 5 phases execute. Final score >= 83 or plateau report.

### Test 8: Audit Pipeline Variant

**Input**: "Audit my existing dashboard page"
**Expected**:
- Skips research and build phases
- Starts directly at scoring existing component files
- Proceeds to fix loop if below target
- Outputs before/after comparison

**Pass criteria**: No research phase. Score + fix only.
