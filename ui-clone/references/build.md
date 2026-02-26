# Workflow 02: Analyze and Build Implementation

## Prerequisites

- Completed capture (`manifest.json` + screenshots exist)
- `pnpm dev` running at `http://localhost:3000`
- `pip install -r scripts/requirements.txt`

---

## Phase A: Find Shared Components (DO FIRST)

```bash
python scripts/find_shared_components.py --manifest .tmp/[app]/manifest.json
# → .tmp/[app]/component-map.json
```

Output tells you which regions (sidebar, topbar, chat-input, etc.) are consistent across screens.
**Read `component-map.json` before building anything.** Build shared components first — they appear everywhere.

---

## Phase B: Extract Design Tokens

```bash
python scripts/analyze_screen.py --image screenshots/[app]/[flow]/01-[name].png
```

From the color output, create `src/app/globals.css`:

```css
@theme inline {
  --color-background: #...;  /* dominant color */
  --color-brand: #...;       /* accent color */
  --color-border: #...;      /* border color */
}
```

**Do not skip** — tokens are used across all components.

---

## Phase C: Build Shared Components

Order from `component-map.json → build_order.shared_first`:

For each shared component:
1. Read ALL screenshots where it appears (Read tool reads images directly)
2. Identify states: collapsed/expanded, hover, active items
3. Build `src/components/[app]/[component].tsx`
4. Run visual diff:

```bash
python scripts/visual_diff.py \
  --original screenshots/[app]/[flow]/01.png \
  --url http://localhost:3000 \
  --output .tmp/[app]/diffs/[component].png
```

5. Target **≥80% match**. Read both images → fix → re-diff.

**Typical build order:** layout.tsx → sidebar → topbar → chat-input (or main input) → others

---

## Phase D: Build Each Screen

For each screen in `manifest.json` order:
1. Read screenshot: `Read tool → screenshots/[app]/[flow]/[N]-[name].png`
2. Identify layout + unique elements (not in shared components)
3. Build `src/app/(clone)/[flow]/page.tsx`
4. Visual diff: `--original [screen].png --url http://localhost:3000/[route]`

---

## Visual Validation Loop

```
diff shows 65% match
  → Read both images (original + .tmp/[app]/diffs/output.png)
  → Identify the specific region that differs
  → Fix the CSS/layout
  → Re-run visual_diff
  → ≥80% = pass → document fix in component ref
```

---

## Edge Cases

| Situation | Approach |
|-----------|----------|
| Font-heavy screen | Use `--threshold 70` |
| Screen shows open dropdown/modal | Build default state first, note interaction |
| Component looks different across flows | Add props for variants |
| Visual diff fails but looks correct | Font rendering differs — focus on layout/spacing/colors |

---

## Expected Output

```
src/
  app/globals.css         ← Design tokens
  (clone)/
    layout.tsx            ← App shell
    [flow]/page.tsx       ← Each screen
  components/[app]/
    sidebar.tsx
    topbar.tsx
.tmp/[app]/
  component-map.json
  diffs/                  ← Review these
```

## Next

```bash
python scripts/generate_skill_refs.py --app [app] --component-map .tmp/[app]/component-map.json
# Then: references/package-skill.md
```
