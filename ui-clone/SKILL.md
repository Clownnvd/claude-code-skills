---
name: ui-clone
description: "Clone any app UI from PageFlows. WAT framework: capture screenshots → analyze+build with visual diff → package as reusable skill. Works for any app."
---

# UI Clone — WAT Framework

Clone any app's UI from PageFlows screenshots into Next.js (Tailwind v4).
**WAT = Workflows + Agent + Tools.**

---

## Quick Start

```bash
# 1. Capture all screens
python scripts/pageflows_capture.py --app [app-name]

# 2. Find shared components
python scripts/find_shared_components.py --manifest .tmp/[app]/manifest.json

# 3. Extract design tokens
python scripts/analyze_screen.py --image screenshots/[app]/[flow]/01-[name].png

# 4. Visual diff (after building a screen)
python scripts/visual_diff.py \
  --original screenshots/[app]/[flow]/01.png \
  --url http://localhost:3000/[route]

# 5. Generate skill scaffold
python scripts/generate_skill_refs.py --app [app] --component-map .tmp/[app]/component-map.json
```

**Install deps:** `pip install -r scripts/requirements.txt`

---

## Three Workflows

| Phase | Goal | Reference |
|-------|------|-----------|
| **01 Capture** | Get all screenshots from PageFlows | `references/capture.md` |
| **02 Build** | Analyze + implement with visual diff loop | `references/build.md` |
| **03 Package** | Create reusable skill for future sessions | `references/package-skill.md` |

---

## Scripts

| Script | Purpose | Key Args |
|--------|---------|----------|
| `pageflows_capture.py` | Capture all flows/screens from PageFlows | `--app [name]` |
| `find_shared_components.py` | Detect shared UI regions via perceptual hash | `--manifest [path]` |
| `analyze_screen.py` | Extract dominant colors → design tokens | `--image [path]` |
| `visual_diff.py` | Compare original vs implementation screenshot | `--original [path] --url [url]` |
| `generate_skill_refs.py` | Generate skeleton skill reference files | `--app [name] --component-map [path]` |

---

## Output Structure

```
screenshots/[app]/
  [flow]/
    01-[screen].png
    02-[screen].png
.tmp/[app]/
  manifest.json           ← All flows + screen metadata
  component-map.json      ← Shared vs unique regions (build order)
  diffs/                  ← Visual diff outputs (review these)
src/
  app/
    globals.css           ← Design tokens
    (clone)/
      layout.tsx          ← App shell
      [flow]/page.tsx     ← Each screen
  components/
    [app]/
      sidebar.tsx
      topbar.tsx
```

---

## Visual Diff Loop

```
diff shows 65% match
  → Read both images (original + diff output) with Read tool
  → Identify the specific region that differs
  → Fix the CSS/layout
  → Re-run visual_diff
  → Pass at ≥80%
  → Document fix in component ref
```

---

## PageFlows Auth

```bash
# First time (manual login):
agent-browser --headed open https://pageflows.com
# After login:
agent-browser state save pageflows-auth.json
```

Pro account: `magicduy56@gmail.com` — saved in `pageflows-auth.json`.

---

## Critical Rules

| Rule | Detail |
|------|--------|
| Run `find_shared_components` BEFORE building | Avoids reimplementing the same sidebar 10 times |
| Build shared components FIRST | They appear on every screen |
| Visual diff target: ≥80% | Use `--threshold 70` for font-heavy screens |
| Auth expires ~1 day | Re-auth if screenshots look like login page |
| Never close browser mid-capture | `agent-browser close` loses session |
| Use `eval + data-url` for screen URLs | PageFlows click interactions reliably timeout |
