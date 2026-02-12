# Database Scoring — Scoring Workflow Eval

Verify the database scoring process produces correct, complete output.

## Test 1: Valid Codebase Produces Score 0-100

- Run db-scoring against a codebase with schema.prisma and migrations
- Verify output contains a numeric score between 0 and 100
- Verify all 10 categories (Schema Design, Data Integrity, Indexing, Security, Query Performance, Migration, Monitoring, Backup, Scalability, Developer Experience) have individual scores
- Each raw score must be 0-10

## Test 2: Each Criterion Scored Individually With Weight

- Verify Schema Design at 15%, Data Integrity at 12%, Indexing at 12%
- Verify Security at 15%, Query Performance at 10%, Migration at 10%
- Verify Monitoring at 8%, Backup at 8%, Scalability at 5%, DX at 5%
- Confirm weighted score = raw score x weight x 10
- Confirm total = sum of all weighted scores

## Test 3: Output Includes Scorecard AND Issues List

- Verify output contains a scorecard table with all 10 categories
- Verify output contains a prioritized issues list with Severity, Category, Issue, Fix
- Verify each issue references specific schema files, migrations, or query locations
- Verify quick wins section is present

## Test 4: Grade Letter Matches Score Range

- Score 90-100 produces A-range grade (A+/A/A-)
- Score 75-89 produces B-range grade (B+/B/B-)
- Score 60-74 produces C-range or D grade
- Score 40-59 produces D grade
- Score 0-39 produces F grade

## Test 5: Issues Sorted by Severity

- CRITICAL issues (score 0-3 or data loss risk) appear first
- HIGH issues (score 4-5, weight >= 12%) appear second
- MEDIUM issues (score 4-5, weight < 12%) appear third
- LOW issues (score 7-8) appear last
