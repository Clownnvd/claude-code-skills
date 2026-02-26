# End-to-End Example: Creating a code-review Skill

Complete walkthrough from user request to packaged skill.

## Step 1: Understand

User says: "I need a skill that reviews TypeScript code quality"

Questions asked:
- "What should it check?" — naming conventions, error handling, type safety, imports
- "What triggers it?" — "review this code", "check code quality", "audit PR"
- "Scoring or qualitative?" — Qualitative (issues list, not numerical score)
- "Framework-specific?" — React + Node.js backend

**Decision:** Use `review-skill.md.template` (qualitative review, not scoring).

## Step 2: Research

Search for: TypeScript best practices, ESLint rules, common code smells.
Found: eslint recommended rules, TypeScript strict mode checks, React hooks rules.
Decision: No scripts needed (review is heuristic-based, not automated).

## Step 3: Plan Resources

```
code-review/
├── SKILL.md                      # Criteria overview + output format
├── references/
│   ├── review-criteria.md        # All 8 criteria detailed
│   ├── common-issues.md          # Top 20 issues with fix examples
│   └── output-format.md          # Review report structure
└── evals/
    └── eval-review.json          # 5 test cases
```

No scripts (review is context-based). No assets. 3 references.

## Step 4: Initialize

```bash
python scripts/init_skill.py code-review --path skills/public
```

Output:
```
Created skill directory: skills/public/code-review/
Created SKILL.md
Created LICENSE.txt (Apache 2.0)
Created scripts/example.py
Created references/api_reference.md
Created references/best-practices.md
Created assets/example_asset.txt
```

Delete unused files: `scripts/`, `assets/`, example references.

## Step 5: Edit

### SKILL.md (45 lines)
```markdown
---
name: code-review
description: Review TypeScript code quality. Check naming, error handling, type safety, imports, React patterns. Output issues list with severity.
---

# Code Review

Review TypeScript/React code and produce actionable feedback.

## When to Use
- Pre-merge code review
- Reviewing TypeScript/React pull requests
- Auditing existing code quality

## Review Process
1. Read `references/review-criteria.md` for all 8 criteria
2. Scan each file against criteria
3. Classify issues by severity (critical/high/medium/low)
4. Output report following `references/output-format.md`

## Review Criteria
| # | Criterion | Checks |
|---|-----------|--------|
| 1 | Naming | Variables, functions, files follow conventions |
| 2 | Type safety | No `any`, strict null checks, proper generics |
| 3 | Error handling | Try/catch, typed errors, no silent failures |
| 4 | Imports | No circular deps, barrel exports, tree-shaking |
| 5 | React patterns | Hooks rules, memo usage, key props |
| 6 | Security | Input validation, XSS prevention, env vars |
| 7 | Performance | N+1 queries, unnecessary re-renders, bundle size |
| 8 | Testing | Coverage, meaningful assertions, no flaky tests |

## Quick Reference
- `references/review-criteria.md` — Detailed criteria + examples
- `references/common-issues.md` — Top 20 issues with fix patterns
- `references/output-format.md` — Report structure template
```

### references/review-criteria.md (excerpt, ~120 lines)
Each criterion gets: description, what to check, good/bad examples, severity guide.

### references/common-issues.md (excerpt, ~100 lines)
Top 20 issues: `any` type usage, missing error boundaries, circular imports, etc.

## Step 6: Validate & Package

```bash
python scripts/quick_validate.py skills/public/code-review
# Output: Skill is valid!

python scripts/package_skill.py skills/public/code-review ./dist
# Output: Successfully packaged to ./dist/code-review.zip
```

## Step 7: Iterate

After using the skill on 3 PRs:
- Added criterion #9: "Accessibility" (a11y attributes, ARIA roles)
- Split `common-issues.md` into `common-issues-react.md` + `common-issues-node.md`
- Added `references/fix-patterns.md` for automated fix suggestions

## Key Takeaways

| Principle | Applied How |
|-----------|------------|
| SKILL.md as index | 45 lines, no detailed docs — just criteria table + references |
| Right template | Used `review-skill.md.template` for qualitative output |
| Minimal structure | No scripts (not needed), no assets, 3 focused references |
| Iterate from real use | Added criterion after 3 real reviews |
