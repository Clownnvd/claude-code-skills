# Auth Scoring — Overview

## Purpose

Systematic audit of authentication & authorization implementation. Produces actionable scorecard with weighted scores, letter grades, and prioritized fix list.

## Scoring System

- 10 categories, each scored 0-10
- Weighted by security impact (session management 15% > 2FA 5%)
- Final score: weighted sum mapped to 0-100

## Grade Scale

| Grade | Range | Meaning |
|-------|-------|---------|
| A+ | 97-100 | Best-in-class |
| A | 93-96 | Enterprise-grade |
| A- | 90-92 | Excellent |
| B+ | 87-89 | Production-ready |
| B | 83-86 | Good |
| B- | 80-82 | Acceptable |
| C+ | 77-79 | Needs work |
| C | 73-76 | Below standard |
| D | 60-72 | Poor |
| F | <60 | Failing |

## Quality Gates

| Context | Minimum Grade |
|---------|---------------|
| Internal tool | C+ (77) |
| Public SaaS | B+ (87) |
| Enterprise / finance | A- (90) |
| Healthcare / compliance | A (93) |

## Issue Severity

| Severity | Criteria | Action |
|----------|----------|--------|
| CRITICAL | Score 0-3 or auth bypass possible | Fix immediately — blocks deploy |
| HIGH | Score 4-5 | Fix in current sprint |
| MEDIUM | Score 6-7 | Fix next sprint |
| LOW | Score 8 | Backlog |

## Output Format

```markdown
## Auth Scorecard — [Project Name]

| # | Category | Weight | Score | Weighted | Issues |
|---|----------|--------|-------|----------|--------|
| 1 | Session Management | 15% | X/10 | X.XX | ... |
| ... | | | | | |
| **Total** | | **100%** | | **XX.X/100** | |
| **Grade** | | | | **B+** | |

### Issues (Priority Order)
1. [CRITICAL] ...
2. [HIGH] ...

### Quick Wins
- ...
```
