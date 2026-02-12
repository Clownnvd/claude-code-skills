# Eval: quick_validate.py

## Test 1: Valid Skill Passes

**Input:** Skill with correct `name: my-skill`, `description: Does X when Y` (<200 chars)

**Expected:** Exit 0, "Skill is valid!"

---

## Test 2: Missing SKILL.md

**Input:** Directory with no SKILL.md

**Expected:** Exit 1, "SKILL.md not found"

---

## Test 3: Missing Frontmatter

**Input:** SKILL.md without `---` YAML block

**Expected:** Exit 1, "No YAML frontmatter found"

---

## Test 4: Missing Name Field

**Input:** Frontmatter with `description:` but no `name:`

**Expected:** Exit 1, "Missing 'name' in frontmatter"

---

## Test 5: Invalid Name Format

**Input cases:**
| Name | Expected Error |
|------|---------------|
| `MySkill` | "should be hyphen-case" |
| `my_skill` | "should be hyphen-case" |
| `-leading` | "cannot start/end with hyphen" |
| `trailing-` | "cannot start/end with hyphen" |
| `double--hyphen` | "cannot contain consecutive hyphens" |

---

## Test 6: Angle Brackets in Description

**Input:** `description: Use <this> for that`

**Expected:** Exit 1, "Description cannot contain angle brackets"

---

## Test 7: Valid Edge Cases

**Input cases that SHOULD pass:**
| Name | Description |
|------|-------------|
| `a` | Single char name |
| `a-b-c-d` | Multiple hyphens |
| `skill123` | Digits in name |
| `my-skill-v2` | Version in name |
