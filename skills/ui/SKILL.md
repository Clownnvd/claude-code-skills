---
name: ui
description: UI quality system. 4 modes: research (design brief), score (10-category audit), fix (auto-fix from scorecard), pipeline (end-to-end chain).
license: Complete terms in LICENSE.txt
---

# UI Quality System

One skill, 4 modes. Research real products, score UI quality, fix issues, or run the full pipeline.

## Modes

| Mode | Use When | Workflow |
|------|----------|---------|
| **research** | Before building any page | Extract tokens → Search → Fetch → Design Brief |
| **score** | Audit existing UI quality | Read components → Score 10 categories → Scorecard |
| **fix** | Fix issues from scorecard | Parse → Prioritize → Fix → Verify → Re-score |
| **pipeline** | Full end-to-end cycle | Research → Build → Score → Fix loop → Ship |

## Mode: Research

Research real products before designing. Extract project design tokens, search live inspiration, output a structured Design Brief.

**When**: Before creating or redesigning any page, or when UI feels "generic AI."

**Steps**: Load `references/research/research-workflow.md`
1. Define scope → 2. Extract design tokens → 3. Search 3+ queries → 4. Fetch 3-5 sites → 5. Pattern recognition → 6. Output Design Brief

**Output contract** (required sections):
- Direction (vibe, layout, primary color from CSS tokens)
- Component Plan table (3+ rows)
- Design Tokens (from `globals.css`, no hardcoded colors)
- Inspiration Sources (3+ URLs)
- Anti-Patterns (2+ items)

## Mode: Score

Audit any UI page across 10 weighted categories (0-100).

**When**: Evaluating quality, comparing before/after, quality gate before shipping.

**Steps**: Load `references/scoring/scoring-workflow.md`

| # | Category | Weight | Criteria Reference |
|---|----------|--------|--------------------|
| 1 | Visual Hierarchy | 15% | `scoring/criteria/visual-design.md` |
| 2 | Color & Theme | 10% | `scoring/criteria/visual-design.md` |
| 3 | Typography | 10% | `scoring/criteria/visual-design.md` |
| 4 | Spacing & Layout | 12% | `scoring/criteria/visual-design.md` |
| 5 | Responsiveness | 12% | `scoring/criteria/responsive-perf.md` |
| 6 | Interactions | 8% | `scoring/criteria/ux-interactions.md` |
| 7 | Accessibility | 10% | `scoring/criteria/ux-interactions.md` |
| 8 | Content & Copy | 8% | `scoring/criteria/content-conversion.md` |
| 9 | Conversion & CTA | 10% | `scoring/criteria/content-conversion.md` |
| 10 | Performance | 5% | `scoring/criteria/responsive-perf.md` |

**Anti-Bias**: Start at 7/10 baseline. Penalize missing checklist items. 9-10 requires evidence. Cross-check with Lighthouse if available (`scoring/measurement.md`).

**Grades**: A+ (97-100), A (93-96), A- (90-92), B+ (87-89), B (83-86), B- (80-82), C+ (77-79), C (73-76), C- (70-72), D (60-69), F (<60)

## Mode: Fix

Take scorecard output and implement all fixes. Prioritize by severity × weight.

**When**: After scoring, when page is below target.

**Steps**: Load `references/fix/implementation-workflow.md`
1. Parse scorecard → 2. Prioritize (Critical → Improvement → Nice-to-have) → 3. Fix → 4. Verify (`tsc --noEmit`) → 5. Re-score

**Loop mode**: Auto-iterate until target score. Max 5 iterations. Stop on plateau (delta=0 for 2 rounds).

| Category | Fix Pattern Reference |
|----------|----------------------|
| Visual, Color, Typography, Spacing | `fix/fix-patterns/visual-polish.md` |
| Responsiveness | `fix/fix-patterns/responsiveness.md` |
| Interactions, Accessibility | `fix/fix-patterns/accessibility.md` |
| Content, Conversion | `fix/fix-patterns/content-copy.md` |
| Performance | `fix/fix-patterns/performance.md` |

## Mode: Pipeline

End-to-end orchestration. Load `references/pipeline/pipeline-workflow.md`.

| Variant | Steps | Use When |
|---------|-------|----------|
| `full` | Research → Build → Score → Fix loop | New page from scratch |
| `audit` | Score → Fix loop | Existing page |
| `polish` | Score → Fix (criticals only) → Re-score once | Quick pass |

**Score Targets**: Prototype 70+, Production 83+, Premium 90+, Showcase 95+

**Handoff contracts**: `references/pipeline/handoff-contracts.md`

## Quick Reference — All Files

### Overview & Best Practices
- `references/overview.md` — How the skill works, architecture, scoring system, fix priority matrix
- `references/best-practices.md` — Do/Don't for tokens, hierarchy, typography, color, responsive, a11y, performance

### Research
- `references/research/research-workflow.md` — 6-step process, token extraction
- `references/research/inspiration-sources.md` — Gallery sites, query templates
- `references/research/anti-ai-patterns.md` — Red flags + fixes
- `references/research/research-templates.md` — Design Brief contract
- `references/research/stack-patterns.md` — Next.js/React/Tailwind patterns

### Scoring
- `references/scoring/scoring-workflow.md` — Audit steps, scorecard template
- `references/scoring/criteria/` — 4 files: visual-design, ux-interactions, content-conversion, responsive-perf
- `references/scoring/page-specific.md` — Bonus criteria per page type
- `references/scoring/nielsen-heuristics.md` — 10 heuristics cross-check
- `references/scoring/measurement.md` — Lighthouse, contrast, bundle metrics

### Fix
- `references/fix/implementation-workflow.md` — Priority matrix, fix process
- `references/fix/verification.md` — Post-fix checklist, loop protocol
- `references/fix/fix-patterns/` — 5 files: visual-polish, responsiveness, accessibility, content-copy, performance

### Pipeline
- `references/pipeline/pipeline-workflow.md` — Full flow, error handling
- `references/pipeline/handoff-contracts.md` — Data formats between modes
- `references/pipeline/measurement.md` — Real metrics collection

## Output Templates

Use templates from `assets/templates/` matching the current mode:
- Research: `design-brief.md.template`
- Score: `scorecard.md.template` and `ui-scorecard.md.template`
- Fix: `fix-checklist.md.template`
Fill `{{VARIABLE}}` placeholders with actual values.
