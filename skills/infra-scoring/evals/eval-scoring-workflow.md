# Infrastructure Scoring — Scoring Workflow Eval

Verify the infrastructure scoring process produces correct, complete output.

## Test 1: Valid Codebase Produces Score 0-100

- Run infra-scoring against a codebase with CI/CD and deployment config
- Verify output contains a numeric score between 0 and 100
- Verify all 10 categories (CI Pipeline, CD Pipeline, Production Deploy, Containerization, Environment Mgmt, Monitoring, Backup/DR, Third-Party, IaC, Deployment Security) have individual scores
- Each raw score must be 0-10

## Test 2: Each Criterion Scored Individually With Weight

- Verify CI Pipeline at 15%, CD Pipeline at 12%, Production Deploy at 10%
- Verify Containerization at 12%, Environment Mgmt at 10%, Monitoring at 15%
- Verify Backup/DR at 10%, Third-Party at 8%, IaC at 4%, Deploy Security at 4%
- Confirm weighted score = raw score x weight x 10
- Confirm total = sum of all weighted scores

## Test 3: Output Includes Scorecard AND Issues List

- Verify output contains a scorecard table with all 10 categories
- Verify output contains a prioritized issues list with Severity, Category, Issue, Fix
- Verify each issue references specific config files (CI YAML, Dockerfile, env files)
- Verify quick wins section is present

## Test 4: Grade Letter Matches Score Range

- Score 90-100 produces A-range grade (A+/A/A-)
- Score 75-89 produces B-range grade (B+/B/B-)
- Score 60-74 produces C-range or D grade
- Score 40-59 produces D grade
- Score 0-39 produces F grade

## Test 5: Issues Sorted by Severity

- CRITICAL issues (score 0-3 or deployment risk) appear first
- HIGH issues (score 4-5, weight >= 12%) appear second
- MEDIUM issues (score 4-5, weight < 12%) appear third
- LOW issues (score 7-8) appear last
