# Workflow 03: Package Implementation as Reusable Skill

## Objective

Package the completed implementation as a skill.
Future sessions can clone any screen without scraping PageFlows again.

## Prerequisites

- Completed workflow 02 (all visual diffs ≥80%)
- `.tmp/[app]/manifest.json` and `component-map.json` exist

---

## Step 1: Generate Reference Scaffold

```bash
python scripts/generate_skill_refs.py \
  --app [app-name] \
  --component-map .tmp/[app]/component-map.json
```

Creates `.claude/skills/[app]-ui/`:
- `SKILL.md` — auto-generated index
- `references/components/[name].md` — one per shared component
- `references/pages/[flow]/[screen].md` — one per screen

---

## Step 2: Fill Component References

For each `references/components/[name].md`:
- Link to source: `**File:** src/components/[app]/[name].tsx`
- Add key states (collapsed/expanded, hover, active)
- Add important Tailwind classes (non-obvious ones)
- Add bugs fixed / non-obvious decisions

**Rule:** Don't copy the full component — just link + document the WHY.

What goes in refs = things you can't read from the code:
- Why a class was chosen
- Bugs that were non-obvious
- Design decisions (e.g., "New chat is a nav row, NOT a button")

---

## Step 3: Fill Page References

For each `references/pages/[flow]/[screen].md`:
- Link to screenshot
- Note unique elements (not in shared components)
- Add ASCII layout diagram if helpful
- Note bugs/quirks discovered

---

## Step 4: Write Design Tokens Reference

Read `src/app/globals.css` → extract to `references/design-tokens.md`:

```md
| Token | Value | Usage |
|-------|-------|-------|
| Background | #... | Page background |
| Brand | #... | Primary accent |
| Border | #... | All borders |
```

Also add typography and spacing conventions.

---

## Step 5: Write Critical Rules in SKILL.md

The most valuable part. From visual diff failures:

```md
| Bug | Correct |
|-----|---------|
| [mistake made] | [correct approach] |
```

Minimum 5 rules.

---

## Step 6: Validate Size

- `SKILL.md` must be **< 150 lines**
- Each reference file must be **< 150 lines**
- If exceeded: split into sub-files

---

## Step 7: Commit to GitHub

```bash
cd .claude/skills
git add [app]-ui/
git commit -m "feat: add [app]-ui skill (N flows, M screens)"
git push origin master
```

---

## Quality Checklist

- [ ] SKILL.md < 150 lines
- [ ] Each reference file < 150 lines
- [ ] All shared components have reference files
- [ ] Critical rules section has ≥5 entries
- [ ] `design-tokens.md` has color + typography table
- [ ] Screenshots referenced (path only, not embedded)
- [ ] Pushed to GitHub

---

## Reuse Pattern

Next time: "build [screen] of [app]":
1. Invoke `[app]-ui` skill
2. Read `references/pages/[flow]/[screen].md`
3. Read linked source file
4. Build immediately — no PageFlows scraping needed

## Self-Improvement Trigger

If a future session finds a bug or new screen:
1. Fix the component
2. Update the reference file
3. Add to Critical Rules if it was non-obvious
4. Commit to GitHub

The skill improves with every project.
