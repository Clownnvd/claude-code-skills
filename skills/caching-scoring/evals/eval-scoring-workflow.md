# Caching Scoring — Scoring Workflow Eval

Verify the caching scoring process produces correct, complete output.

## Test 1: Valid Codebase Produces Score 0-100

- Run caching-scoring against a Next.js codebase
- Verify output contains a numeric score between 0 and 100
- Verify all 10 categories (Cache-Control Headers, Revalidation Strategy, Static vs Dynamic, ISR, React cache(), "use cache", CDN & Edge, Request Dedup, Proxy Caching, Cache Monitoring) have individual scores
- Each raw score must be 0-10

## Test 2: Each Criterion Scored Individually With Weight

- Verify Cache-Control Headers at 15%, Revalidation at 15%, Static/Dynamic at 12%
- Verify ISR at 8%, React cache() at 10%, "use cache" at 10%
- Verify CDN at 8%, Request Dedup at 7%, Proxy at 7%, Monitoring at 8%
- Confirm weighted score = raw score x weight x 10
- Confirm total = sum of all weighted scores

## Test 3: Output Includes Scorecard AND Issues List

- Verify output contains a scorecard table with all 10 categories
- Verify output contains a prioritized issues list with Severity, Category, Issue, Fix
- Verify each issue references affected files (routes, pages, proxy)
- Verify quick wins section is present

## Test 4: Grade Letter Matches Score Range

- Score 90-100 produces A-range grade (A+/A/A-)
- Score 75-89 produces B-range grade (B+/B/B-)
- Score 60-74 produces C-range or D grade
- Score 40-59 produces D grade
- Score 0-39 produces F grade

## Test 5: Issues Sorted by Severity

- CRITICAL issues (score 0-3 or stale data risk) appear first
- HIGH issues (score 4-5, weight >= 12%) appear second
- MEDIUM issues (score 4-5, weight < 12%) appear third
- LOW issues (score 7-8) appear last
