# UI Scoring — Scoring Workflow Eval

Verify the UI scoring process produces correct, complete output.

## Test 1: Valid Page Produces Score 0-100

- Run ui score mode against a page with UI components
- Verify output contains a numeric score between 0 and 100
- Verify all 10 categories (Visual Hierarchy, Color & Theme, Typography, Spacing & Layout, Responsiveness, Interactions, Accessibility, Content & Copy, Conversion & CTA, Performance) have individual scores
- Each raw score must be 0-10, starting from 7/10 anti-bias baseline

## Test 2: Each Criterion Scored Individually With Weight

- Verify Visual Hierarchy at 15%, Color at 10%, Typography at 10%
- Verify Spacing at 12%, Responsiveness at 12%, Interactions at 8%
- Verify Accessibility at 10%, Content at 8%, Conversion at 10%, Performance at 5%
- Confirm weighted score = raw score x weight x 10
- Confirm total = sum of all weighted scores

## Test 3: Output Includes Scorecard AND Issues List

- Verify output contains a scorecard table with all 10 categories
- Verify output contains a prioritized issues list with Severity, Category, Issue, Fix
- Verify each issue references specific component files
- Verify quick wins section is present
- Verify Nielsen heuristic cross-check is included

## Test 4: Grade Letter Matches Score Range

- Score 90-100 produces A-range grade (A+/A/A-)
- Score 75-89 produces B-range grade (B+/B/B-)
- Score 60-74 produces C-range or D grade
- Score 40-59 produces D grade
- Score 0-39 produces F grade

## Test 5: Issues Sorted by Severity

- CRITICAL issues (severe usability or accessibility failures) appear first
- HIGH issues (high-weight categories scoring below 5) appear second
- MEDIUM issues (lower-weight categories needing improvement) appear third
- LOW issues (polish and nice-to-have improvements) appear last
