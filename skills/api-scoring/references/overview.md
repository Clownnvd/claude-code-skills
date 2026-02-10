# API Scoring — Overview

## Purpose

Score any REST/HTTP API codebase against 10 enterprise-grade criteria. Produce a weighted 0-100 score with letter grade, prioritized issues list, and actionable quick wins.

## Scoring System

- **10 categories**, each scored 0-10
- **Weighted sum** → 0-100 total → letter grade
- **Baseline**: start at 5/10 per category (neutral). Subtract 1 for each missing critical item. Add 1 for evidence of best practices. Require concrete code evidence for 9-10.

## Grade Scale

| Grade | Range | Production Ready? |
|-------|-------|-------------------|
| A+    | 97-100 | World-class (Stripe-level) |
| A     | 93-96  | Enterprise-grade |
| A-    | 90-92  | Enterprise-grade |
| B+    | 87-89  | Production-ready |
| B     | 83-86  | Production-ready |
| B-    | 80-82  | Acceptable with caveats |
| C+    | 77-79  | Needs work |
| C     | 73-76  | Needs work |
| D     | 60-72  | Not ready |
| F     | < 60   | Critical gaps |

## Quality Gates

- **Production deploy**: B+ (87+)
- **Enterprise / public API**: A- (90+)

## Issue Severity

| Severity | Criteria | Action |
|----------|----------|--------|
| CRITICAL | Score 0-3 or security hole | Fix before deploy |
| HIGH     | Score 4-5, category weight >= 12% | Fix in current sprint |
| MEDIUM   | Score 4-5, category weight < 12% | Fix next sprint |
| LOW      | Score 7-8 | Backlog |

## Scorecard Output Format

```
# API Scorecard — [Project Name]
Date: YYYY-MM-DD | Stack: [framework + runtime]

| # | Category | Weight | Score | Weighted | Status |
|---|----------|--------|-------|----------|--------|
| 1 | Security | 20% | X/10 | X.X | SEVERITY |
...
| Total | | 100% | | XX.X | Grade |

## Issues (ordered by severity + weight)
### 1. [Issue title] (Category, SEVERITY)
[file:line] — description + fix suggestion

## Quick Wins (items that move score most per effort)
```

## OWASP API Top 10 Cross-Reference

Every category maps to at least one OWASP risk. Full mapping in `criteria/security-auth.md`.

| OWASP Risk | Covered By |
|---|---|
| API1: BOLA | Auth & AuthZ |
| API2: Broken Auth | Security, Auth & AuthZ |
| API3: BOPLA | Auth & AuthZ, Input Validation |
| API4: Resource Consumption | Rate Limiting, Performance |
| API5: BFLA | Auth & AuthZ |
| API6: Sensitive Flows | Security, Rate Limiting |
| API7: SSRF | Security, Input Validation |
| API8: Misconfiguration | Security, Error Handling, Observability |
| API9: Inventory Mgmt | Observability, Documentation |
| API10: Unsafe API Consumption | Rate Limiting, Input Validation |
