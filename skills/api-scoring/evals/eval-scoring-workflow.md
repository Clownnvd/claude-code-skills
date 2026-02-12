# API Scoring — Scoring Workflow Eval

Verify the API scoring process produces correct, complete output.

## Test 1: Valid Codebase Produces Score 0-100

- Run api-scoring against a codebase with API routes
- Verify output contains a numeric score between 0 and 100
- Verify all 10 categories (Security, Auth & AuthZ, Input Validation, Error Handling, Rate Limiting, Response Design, Performance, Observability, Documentation & DX, Testing) have individual scores
- Each raw score must be 0-10

## Test 2: Each Criterion Scored Individually With Weight

- Verify Security is weighted at 20%, Auth & AuthZ at 15%, Input Validation at 12%
- Verify Error Handling at 10%, Rate Limiting at 10%, Response Design at 8%
- Verify Performance at 8%, Observability at 7%, Documentation at 5%, Testing at 5%
- Confirm weighted score = raw score x weight x 10
- Confirm total = sum of all weighted scores

## Test 3: Output Includes Scorecard AND Issues List

- Verify output contains a scorecard table with all 10 categories
- Verify output contains a prioritized issues list with columns: Severity, Category, Issue, Fix
- Verify each issue references a specific file or code pattern
- Verify quick wins section is present

## Test 4: Grade Letter Matches Score Range

- Score 90-100 produces A-range grade (A+/A/A-)
- Score 75-89 produces B-range grade (B+/B/B-)
- Score 60-74 produces C-range or D grade
- Score 40-59 produces D grade
- Score 0-39 produces F grade
- Verify grade string appears in the scorecard header

## Test 5: Issues Sorted by Severity

- CRITICAL issues (score 0-3 or security hole) appear first
- HIGH issues (score 4-5, weight >= 12%) appear second
- MEDIUM issues (score 4-5, weight < 12%) appear third
- LOW issues (score 7-8, improvement suggestions) appear last
- Verify no CRITICAL issues are listed below HIGH issues
