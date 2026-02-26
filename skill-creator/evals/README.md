# Skill Creator Evals

Test cases for validating the skill-creator workflow. Excluded from `.skill` packages.

## Running Evals

```bash
# Run automated eval runner
python scripts/run_evals.py

# Run unit tests (pytest)
python -m pytest scripts/tests/ -v
```

## Eval Files

| File | Tests | Pass Criteria |
|------|-------|---------------|
| `eval-init-skill.json` | `init_skill.py` creates valid structure | All dirs + files exist, SKILL.md has valid frontmatter |
| `eval-validate-skill.json` | `quick_validate.py` catches errors | Rejects invalid names, missing fields, oversized files |
| `eval-package-skill.json` | `package_skill.py` creates valid zip | Zip contains all files, excludes evals/, validates first |
| `eval-quality-gates.json` | Quality rules enforced | Size limits, no duplication, correct writing style |
| `eval-skill-types.json` | `--type` flag produces correct templates | Each type generates matching SKILL.md structure |
| `eval-enhanced-validation.json` | Enhanced quality checks | Description length, file sizes, test coverage, name match |
