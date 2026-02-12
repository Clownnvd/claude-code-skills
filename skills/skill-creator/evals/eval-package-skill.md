# Eval: package_skill.py

## Test 1: Valid Skill Packages Successfully

**Input:**
```bash
python scripts/package_skill.py /path/to/valid-skill
```

**Expected:**
- Runs validation first (prints "Skill is valid!")
- Creates `valid-skill.zip` in current directory
- Zip contains all files with correct relative paths
- Exit code: 0

---

## Test 2: Invalid Skill Rejects Packaging

**Input:** Skill with missing `name:` in frontmatter

**Expected:**
- Prints validation error
- No zip created
- Exit code: 1

---

## Test 3: Custom Output Directory

**Input:**
```bash
python scripts/package_skill.py /path/to/skill ./dist
```

**Expected:**
- `./dist/` created if not exists
- `./dist/skill.zip` created
- Exit code: 0

---

## Test 4: Nonexistent Skill Path

**Input:**
```bash
python scripts/package_skill.py /nonexistent/path
```

**Expected:** Exit 1, "Skill folder not found"

---

## Test 5: Zip Content Verification

**Input:** Package a skill with `SKILL.md`, `references/a.md`, `scripts/b.py`, `assets/c.txt`

**Expected zip structure:**
```
skill-name/
  SKILL.md
  references/a.md
  scripts/b.py
  assets/c.txt
```
All paths relative to skill parent directory.
