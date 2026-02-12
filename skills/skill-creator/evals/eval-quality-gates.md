# Eval: Quality Gate Enforcement

## Test 1: SKILL.md Size Limit

**Input:** SKILL.md with 160 lines (over 150 limit)

**Expected:** Validation warns about size. Packager should flag as issue.

---

## Test 2: Reference File Size Limit

**Input:** Single reference file with 200 lines (over 150 limit)

**Expected:** Should recommend splitting into 2 files of ~100 lines each.

---

## Test 3: Description Length

**Input cases:**
| Length | Expected |
|--------|----------|
| 50 chars | Pass |
| 199 chars | Pass |
| 200 chars | Fail — over limit |
| 250 chars | Fail — over limit |

---

## Test 4: No Duplication Rule

**Input:** Same paragraph appears in both SKILL.md and `references/overview.md`

**Expected:** Should be flagged. Info lives in ONE place only.

---

## Test 5: Writing Style Check

**Pass examples:**
- "To configure auth, set the `AUTH_SECRET` environment variable"
- "Run `scripts/init.py` to scaffold the project"

**Fail examples:**
- "You should configure auth by setting the variable" (second person)
- "This document explains how to..." (meta-language, not actionable)

---

## Test 6: Script Test Requirement

**Input:** `scripts/main.py` exists but no `scripts/test_main.py`

**Expected:** Flag as issue — all scripts must have corresponding tests.

---

## Test 7: Consolidated Topics

**Input:** Two separate skills: `mongodb-scoring` and `postgresql-scoring`

**Expected:** Should recommend consolidating into `db-scoring` with subdirectories.
