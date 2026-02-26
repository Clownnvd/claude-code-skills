# Skill Type Selection Guide

## Decision Tree

```
What does the skill need to do?
│
├─ Audit/grade quality against criteria?
│  → scoring-skill.md.template
│
├─ Fix issues from an audit/scoring output?
│  → fix-skill.md.template (pairs with scoring)
│
├─ Create new code/content from specifications?
│  → generate-skill.md.template
│
├─ Upgrade/migrate between versions?
│  → migrate-skill.md.template
│
├─ Review/audit code without numerical scoring?
│  → review-skill.md.template
│
├─ Create or run tests?
│  → test-skill.md.template
│
└─ None of the above?
   → SKILL.md.template (general)
```

## Type Comparison

| Type | Key Sections | Output | Pairs With |
|------|-------------|--------|------------|
| General | When to Use, Process, Quick Ref | Varies | Any |
| Scoring | Criteria table, Grade scale | Scorecard (0-100) | Fix |
| Fix | Severity table, Fix patterns | Applied code changes | Scoring |
| Generate | Output specs, Conventions | New code/content | Test |
| Migrate | Breaking changes, Codemods | Migrated codebase | Test |
| Review | Criteria checklist, Output format | Issues list | Fix |
| Test | Strategy table, Patterns | Test files + coverage | Any |

## Common Combinations

### Audit → Remediate Pipeline
1. `scoring` — Grade the codebase, produce scorecard
2. `fix` — Take scorecard, implement fixes by severity
3. Re-run `scoring` to verify improvement

### Create → Verify Pipeline
1. `generate` — Scaffold new code from specs
2. `test` — Write and run tests for generated code

### Review → Implement Pipeline
1. `review` — Audit code, produce issues list
2. `fix` — Take issues list, implement fixes

### Full Lifecycle
1. `generate` — Create initial implementation
2. `test` — Add test coverage
3. `scoring` — Audit quality
4. `fix` — Address issues
5. `review` — Final review before merge

## Choosing Between Similar Types

### Scoring vs Review
- **Scoring**: Produces a numerical 0-100 scorecard with weighted criteria. Use when you need a repeatable, quantitative quality gate.
- **Review**: Produces an issues list with severity labels. Use for qualitative code review, PR feedback, or one-time audits.

### Generate vs General
- **Generate**: Has output specification tables, convention rules, and scaffolding scripts. Use when the skill's primary job is creating new artifacts.
- **General**: Flexible structure. Use when the skill is a guideline, workflow, or tool collection that doesn't fit other types.

### Fix vs General
- **Fix**: Designed to consume output from scoring/review skills. Has severity priority table and fix pattern references.
- **General**: Use when fixes aren't driven by a paired audit skill.
