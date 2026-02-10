# Research Workflow — Step-by-Step

## Step 1: Define Scope

Before searching, establish:
- **What**: Component, page, or flow being built
- **Stack**: Framework, component library, CSS approach
- **Vibe**: Professional, playful, minimal, bold, luxury
- **Constraints**: Existing brand, colors, tech stack

## Step 2: Extract Design Tokens

Before searching externally, read the project's existing theme to ground decisions.

### Files to read
1. `src/app/globals.css` — CSS variables, `@theme` block, utility classes
2. `tailwind.config.ts` / `tailwind.config.js` (if present)
3. Brand/product config (e.g., `src/config/product.ts`)

### Token extraction table
| Token | What to capture |
|-------|-----------------|
| Primary color | `--primary` value (oklch/hsl/hex) |
| Accent color | `--accent` value |
| Font family | `--font-sans`, `--font-mono` |
| Font weights | Which weights are used (400, 500, 600, 700) |
| Border radius | `--radius` value |
| Gradient utilities | `bg-gradient-*`, `text-gradient` custom classes |
| Custom utilities | `card-hover`, `shine-effect`, `glass`, `border-gradient` |
| Animation classes | `animate-slide-up`, `animate-fade-in`, etc. |

Carry extracted tokens into the Design Brief. Never propose colors/fonts that conflict with existing tokens.

## Step 3: Search Real Products

Use `WebSearch` to find live inspiration. Always search **3+ queries**.

### Query patterns
```
"[type] [industry] website 2026"       → e.g., "SaaS pricing page 2026"
"best [component] design examples"     → e.g., "best dashboard sidebar design"
"[competitor] website redesign"        → find specific companies
site:awwwards.com [type]               → award-winning
site:godly.website [keyword]           → landing pages
site:dribbble.com [component] UI       → visual concepts
```

See `references/inspiration-sources.md` for full gallery list and search templates.

## Step 4: Fetch & Analyze

Use `WebFetch` on **3-5 promising URLs**. For each, extract:
- Layout structure (grid, spacing, hierarchy)
- Color palette and contrast approach
- Typography (fonts, scale, weights)
- Component patterns (buttons, cards, forms)
- Micro-interactions and motion

## Step 5: Pattern Recognition

After collecting 5+ examples, identify:
- **Repeated patterns** — what 3+ sites do the same way (adopt these)
- **Unique differentiators** — standout elements worth adopting
- **Anti-patterns** — what feels dated or generic

Check `references/anti-ai-patterns.md` to flag AI-look red flags.

## Step 6: Create Design Brief

Output a **Design Brief** in the exact format specified in `references/research-templates.md`.

This brief is the handoff contract to the next pipeline stage (build or scoring). It must include:
- Direction (vibe, layout, primary color from tokens)
- Component plan table (component × pattern × source)
- Design tokens extracted in Step 2
- Inspiration sources (3+ URLs with notes)
- Anti-patterns to avoid

## Quality Gates

Before handing off, verify:
- [ ] Read project theme files (globals.css, config) — tokens extracted
- [ ] Searched 3+ queries, fetched 3+ real sites
- [ ] Identified repeating patterns across examples
- [ ] Checked for AI-look red flags (`references/anti-ai-patterns.md`)
- [ ] Design Brief follows the handoff contract format
- [ ] All tokens reference CSS variables (no hardcoded colors)
- [ ] Planned responsive + dark mode approach

## Which References to Load

| Phase | Load |
|-------|------|
| Token extraction | Read `globals.css` + theme config directly |
| Searching | `inspiration-sources.md` for gallery sites + query templates |
| Analyzing | `anti-ai-patterns.md` for red flag checks |
| Briefing | `research-templates.md` for output contract template |
| Implementing | `stack-patterns.md` for Next.js/React/Tailwind patterns |
