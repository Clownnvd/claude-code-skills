# Scoring Workflow — Step-by-Step Audit

## Step 1: Identify Target

- Determine page type: landing, dashboard, auth, billing, settings, or custom
- Read all relevant component files for the page
- Read `globals.css` or theme config for design tokens
- Check `references/page-specific.md` for bonus criteria matching the page type

## Step 2: Load Relevant Criteria

Per page type, prioritize these references:

| Page Type | Primary References | Secondary |
|-----------|-------------------|-----------|
| Landing | content-conversion, visual-design | responsive-perf, page-specific |
| Dashboard | ux-interactions, visual-design | responsive-perf, page-specific |
| Auth | ux-interactions, visual-design | content-conversion, page-specific |
| Billing | content-conversion, ux-interactions | visual-design, page-specific |

All criteria files in `references/criteria/`:
1. `visual-design.md` — Categories 1-4 (hierarchy, color, typography, spacing)
2. `ux-interactions.md` — Categories 6-7 (states, accessibility)
3. `content-conversion.md` — Categories 8-9 (copy, CTA)
4. `responsive-perf.md` — Categories 5, 10 (responsiveness, performance)

## Step 3: Score Each Category (0-10)

For each of the 10 categories:
1. Review the checklist items in the criteria reference
2. Check the scoring guide for calibration
3. Note specific issues found
4. Assign a score 0-10

## Step 4: Calculate Final Score

Weighted sum formula: `Σ (category_score × weight) × 10`

Example: Visual Hierarchy 8/10 × 0.15 = 1.2, Color 7/10 × 0.10 = 0.7, ... → sum × 10 = final

## Step 5: Output Scorecard

```
## UI Scorecard: [Page Name]

| # | Category | Score | Grade | Key Issues |
|---|----------|-------|-------|------------|
| 1 | Visual Hierarchy | 8/10 | B+ | ... |
| 2 | Color & Theme | 7/10 | B | ... |
| ... | ... | ... | ... | ... |
| **Total** | | **85/100** | **B+** | |

### Critical Issues (must fix)
1. [Issue] → [Fix]

### Improvements (should fix)
1. [Issue] → [Fix]

### Nice-to-have
1. [Issue] → [Fix]
```

## Step 6: Severity Classification

| Score Range | Severity | Action |
|-------------|----------|--------|
| 0-3 | Critical | Blocks usability/conversion. Fix immediately. |
| 4-6 | Major | Noticeable quality gap. Fix next iteration. |
| 7-8 | Minor | Polish items. Fix when time allows. |
| 9-10 | Good | Meets or exceeds standards. |

## Step 7: Nielsen Cross-Check

After scoring, cross-check against Nielsen's 10 heuristics as sanity check.
Load `references/nielsen-heuristics.md` for the full checklist (severity 0-4 per heuristic).

Report heuristic failures alongside the main scorecard.
