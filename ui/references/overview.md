# UI Quality System — Overview

## What This Skill Does

A 4-mode system for researching, auditing, fixing, and shipping production-grade UI. Each mode operates independently or chains into a pipeline.

## How It Works

```
User says "score my landing page"
  → Claude loads SKILL.md → identifies mode: score
  → Loads scoring-workflow.md + relevant criteria
  → Reads component files → Scores 10 categories
  → Outputs scorecard (score, grade, issues list)

User says "fix it"
  → Claude identifies mode: fix
  → Loads implementation-workflow.md
  → Parses scorecard → Prioritizes → Applies fixes
  → Re-scores → Loops until target met
```

## 4 Modes

| Mode | Input | Output | Key Reference |
|------|-------|--------|---------------|
| **research** | Page type + project CSS | Design Brief (tokens, patterns, sources) | `research/research-workflow.md` |
| **score** | Component files | Scorecard (0-100, 10 categories, issues) | `scoring/scoring-workflow.md` |
| **fix** | Scorecard | Fixed code + verification report | `fix/implementation-workflow.md` |
| **pipeline** | Page type or existing page | Ship-ready page with score > target | `pipeline/pipeline-workflow.md` |

## Architecture

### Data Flow Between Modes

```
Research → Design Brief (JSON)
  ↓
Build (manual or pipeline)
  ↓
Score → Scorecard (JSON)
  ↓
Fix → Fixed code + new Scorecard
  ↓ (loop if score < target)
Ship
```

Handoff contracts define the exact data shape between modes. See `pipeline/handoff-contracts.md`.

### File Organization

```
ui/
├── SKILL.md                     — Entry point, mode router
├── LICENSE.txt                  — Apache 2.0
├── references/
│   ├── overview.md              — This file
│   ├── best-practices.md        — Do/Don't for UI development
│   ├── research/                — Design research workflow
│   │   ├── research-workflow.md
│   │   ├── inspiration-sources.md
│   │   ├── anti-ai-patterns.md
│   │   ├── research-templates.md
│   │   └── stack-patterns.md
│   ├── scoring/                 — Quality audit system
│   │   ├── scoring-workflow.md
│   │   ├── criteria/            — 4 weighted criteria files
│   │   ├── page-specific.md
│   │   ├── nielsen-heuristics.md
│   │   └── measurement.md
│   ├── fix/                     — Issue resolution
│   │   ├── implementation-workflow.md
│   │   ├── verification.md
│   │   └── fix-patterns/        — 5 category-specific fix guides
│   └── pipeline/                — End-to-end orchestration
│       ├── pipeline-workflow.md
│       ├── handoff-contracts.md
│       └── measurement.md
```

### Scoring System

10 categories, weighted by impact:

| Weight | Categories |
|--------|-----------|
| 15% | Visual Hierarchy |
| 12% | Spacing & Layout, Responsiveness |
| 10% | Color & Theme, Typography, Accessibility, Conversion & CTA |
| 8% | Interactions, Content & Copy |
| 5% | Performance |

**Grades**: A+ (97-100) → F (<60). Production target: B (83+). Premium target: A- (90+).

### Fix Priority Matrix

| Priority | Criteria | Action |
|----------|----------|--------|
| P0 | Score 0-3, any weight | Fix immediately |
| P1 | Score 4-6, weight >= 10% | Fix next |
| P2 | Score 4-6, weight < 10% | Fix after P1 |
| P3 | Score 7-8 | Fix last or skip |

### Pipeline Variants

| Variant | Flow | Use When |
|---------|------|----------|
| `full` | Research → Build → Score → Fix loop | New page from scratch |
| `audit` | Score → Fix loop | Existing page needs improvement |
| `polish` | Score → Fix criticals → Re-score once | Quick quality pass |

Loop stops when: target score reached, delta=0 for 2 rounds, or 5 iterations max.

## Integration Points

- **globals.css**: Source of truth for design tokens (colors, spacing, typography)
- **Tailwind CSS 4**: `bg-linear-to-r` not `bg-gradient-to-r`
- **cn() utility**: `src/utils/cn.ts` for class merging
- **product config**: `src/config/product.ts` for pricing/copy
- **Dark mode**: All components must support both light and dark themes
