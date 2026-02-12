# Skill Creator Evals

Test cases for validating the skill-creator workflow. Excluded from `.skill` packages.

## Running Evals

Each eval file describes a scenario with expected inputs and outputs.
Run manually or use as reference for automated testing.

## Eval Files

| File | Tests | Pass Criteria |
|------|-------|---------------|
| `eval-init-skill.md` | `init_skill.py` creates valid structure | All dirs + files exist, SKILL.md has valid frontmatter |
| `eval-validate-skill.md` | `quick_validate.py` catches errors | Rejects invalid names, missing fields, oversized files |
| `eval-package-skill.md` | `package_skill.py` creates valid zip | Zip contains all files, excludes evals/, validates first |
| `eval-quality-gates.md` | Quality rules enforced | Size limits, no duplication, correct writing style |
