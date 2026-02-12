# Auth Scoring — Scoring Workflow Eval

Verify the auth scoring process produces correct, complete output.

## Test 1: Valid Codebase Produces Score 0-100

- Run auth-scoring against a codebase with auth implementation
- Verify output contains a numeric score between 0 and 100
- Verify all 10 categories (Session Management, Password Security, OAuth, Email Verification, CSRF, Security Headers, Rate Limiting, Audit Logging, Authorization, 2FA) have individual scores
- Each raw score must be 0-10

## Test 2: Each Criterion Scored Individually With Weight

- Verify Session Management at 15%, Password Security at 12%, OAuth at 10%
- Verify Email Verification at 8%, CSRF at 12%, Security Headers at 10%
- Verify Rate Limiting at 12%, Audit Logging at 8%, Authorization at 8%, 2FA at 5%
- Confirm weighted score = raw score x weight x 10
- Confirm total = sum of all weighted scores

## Test 3: Output Includes Scorecard AND Issues List

- Verify output contains a scorecard table with all 10 categories
- Verify output contains a prioritized issues list with columns: Severity, Category, Issue, Fix
- Verify each issue references specific auth config or middleware files
- Verify quick wins section is present

## Test 4: Grade Letter Matches Score Range

- Score 90-100 produces A-range grade (A+/A/A-)
- Score 75-89 produces B-range grade (B+/B/B-)
- Score 60-74 produces C-range or D grade
- Score 40-59 produces D grade
- Score 0-39 produces F grade
- Verify grade string appears in the scorecard header

## Test 5: Issues Sorted by Severity

- CRITICAL issues (score 0-3 or auth vulnerability) appear first
- HIGH issues (score 4-5, weight >= 12%) appear second
- MEDIUM issues (score 4-5, weight < 12%) appear third
- LOW issues (score 7-8, improvement suggestions) appear last
- Verify no CRITICAL issues are listed below HIGH issues
