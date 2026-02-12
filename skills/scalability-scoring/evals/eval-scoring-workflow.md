# Scalability Scoring — Scoring Workflow Eval

Verify the scalability scoring process produces correct, complete output.

## Test 1: Valid Codebase Produces Score 0-100

- Run scalability-scoring against a Next.js App Router codebase
- Verify output contains a numeric score between 0 and 100
- Verify all 10 categories (Bundle Size, Image Optimization, RSC Architecture, DB Query Perf, API Response Perf, Client-Side Perf, Edge/CDN, Memory Mgmt, Concurrency, Perf Monitoring) have individual scores
- Each raw score must be 0-10

## Test 2: Each Criterion Scored Individually With Weight

- Verify Bundle Size at 15%, Images at 12%, RSC at 12%, DB Perf at 12%
- Verify API Perf at 10%, Client Perf at 10%, Edge/CDN at 8%
- Verify Memory at 8%, Concurrency at 7%, Monitoring at 6%
- Confirm weighted score = raw score x weight x 10
- Confirm total = sum of all weighted scores

## Test 3: Output Includes Scorecard AND Issues List

- Verify output contains a scorecard table with all 10 categories
- Verify output contains a prioritized issues list with Severity, Category, Issue, Fix
- Verify each issue references specific components, routes, or config files
- Verify quick wins section is present

## Test 4: Grade Letter Matches Score Range

- Score 90-100 produces A-range grade (A+/A/A-)
- Score 75-89 produces B-range grade (B+/B/B-)
- Score 60-74 produces C-range or D grade
- Score 40-59 produces D grade
- Score 0-39 produces F grade

## Test 5: Issues Sorted by Severity

- CRITICAL issues (score 0-3 or severe perf bottleneck) appear first
- HIGH issues (score 4-5, weight >= 12%) appear second
- MEDIUM issues (score 4-5, weight < 12%) appear third
- LOW issues (score 7-8) appear last
