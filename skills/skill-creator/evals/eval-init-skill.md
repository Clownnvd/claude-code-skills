# Eval: init_skill.py

## Test 1: Basic Initialization

**Input:**
```bash
python scripts/init_skill.py test-skill --path /tmp/skills
```

**Expected Output:**
- Directory `/tmp/skills/test-skill/` created
- `SKILL.md` exists with valid YAML frontmatter (`name: test-skill`)
- `LICENSE.txt` exists (Apache 2.0)
- `scripts/example.py` exists and is executable
- `references/api_reference.md` exists
- `references/best-practices.md` exists
- `assets/example_asset.txt` exists
- Exit code: 0

**Pass Criteria:** All files exist, SKILL.md frontmatter passes `quick_validate.py`

---

## Test 2: Duplicate Skill Rejection

**Input:**
```bash
python scripts/init_skill.py test-skill --path /tmp/skills  # run twice
```

**Expected Output:**
- Second run prints error: "Skill directory already exists"
- Exit code: 1
- Original directory unchanged

---

## Test 3: Invalid Arguments

**Input:**
```bash
python scripts/init_skill.py  # no args
```

**Expected Output:**
- Prints usage instructions
- Exit code: 1

---

## Test 4: Nested Path Creation

**Input:**
```bash
python scripts/init_skill.py deep-skill --path /tmp/a/b/c
```

**Expected Output:**
- All parent directories created (`/tmp/a/b/c/deep-skill/`)
- Full structure generated
- Exit code: 0
