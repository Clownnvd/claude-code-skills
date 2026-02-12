# Data Flow Scoring — Scoring Workflow Eval

Verify the data flow scoring process produces correct, complete output.

## Test 1: Valid Codebase Produces Score 0-100

- Run dataflow-scoring against a Next.js + Prisma codebase
- Verify output contains a numeric score between 0 and 100
- Verify all 10 categories (RSC Fetching, Server/Client Composition, Prisma Optimization, API Route Design, State Management, Caching, Type Safety, Error Propagation, Form Handling, DTOs) have individual scores
- Each raw score must be 0-10

## Test 2: Each Criterion Scored Individually With Weight

- Verify RSC Fetching at 15%, Composition at 10%, Prisma at 12%, API Routes at 15%
- Verify State Management at 8%, Caching at 10%, Type Safety at 10%
- Verify Error Propagation at 8%, Form Handling at 7%, DTOs at 5%
- Confirm weighted score = raw score x weight x 10
- Confirm total = sum of all weighted scores

## Test 3: Output Includes Scorecard AND Issues List

- Verify output contains a scorecard table with all 10 categories
- Verify output contains a prioritized issues list with Severity, Category, Issue, Fix
- Verify each issue references specific component, route, or service files
- Verify quick wins section is present

## Test 4: Grade Letter Matches Score Range

- Score 90-100 produces A-range grade (A+/A/A-)
- Score 75-89 produces B-range grade (B+/B/B-)
- Score 60-74 produces C-range or D grade
- Score 40-59 produces D grade
- Score 0-39 produces F grade

## Test 5: Issues Sorted by Severity

- CRITICAL issues (score 0-3 or data leak risk) appear first
- HIGH issues (score 4-5, weight >= 12%) appear second
- MEDIUM issues (score 4-5, weight < 12%) appear third
- LOW issues (score 7-8) appear last
