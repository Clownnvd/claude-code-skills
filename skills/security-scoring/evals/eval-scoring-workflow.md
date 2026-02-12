# Security Scoring — Scoring Workflow Eval

Verify the security scoring process produces correct, complete output.

## Test 1: Valid Codebase Produces Score 0-100

- Run security-scoring against a codebase with security controls
- Verify output contains a numeric score between 0 and 100
- Verify all 10 categories (Input Validation, Secrets Mgmt, Dependencies, Error Handling, CSP, Data Protection, Redirects, Webhooks, Security Monitoring, Supply Chain) have individual scores
- Each raw score must be 0-10

## Test 2: Each Criterion Scored Individually With Weight

- Verify Input Validation at 15%, Secrets at 12%, Dependencies at 10%
- Verify Error Handling at 12%, CSP at 10%, Data Protection at 10%
- Verify Redirects at 8%, Webhooks at 8%, Monitoring at 8%, Supply Chain at 7%
- Confirm weighted score = raw score x weight x 10
- Confirm total = sum of all weighted scores

## Test 3: Output Includes Scorecard AND Issues List

- Verify output contains a scorecard table with all 10 categories and OWASP column
- Verify output contains a prioritized issues list with Severity, Category, Issue, OWASP, Fix
- Verify each issue references specific files or code patterns
- Verify quick wins section is present

## Test 4: Grade Letter Matches Score Range

- Score 90-100 produces A-range grade (A+/A/A-)
- Score 75-89 produces B-range grade (B+/B/B-)
- Score 60-74 produces C-range or D grade
- Score 40-59 produces D grade
- Score 0-39 produces F grade

## Test 5: Issues Sorted by Severity

- CRITICAL issues (score 0-3 or exploitable vulnerability) appear first
- HIGH issues (score 4-5, weight >= 12%) appear second
- MEDIUM issues (score 4-5, weight < 12%) appear third
- LOW issues (score 7-8) appear last
