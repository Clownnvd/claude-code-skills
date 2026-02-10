# Output Format

## Per-Page Table Template

For EACH page, output a separate table. Every row MUST include a clickable link.

```markdown
## [Page Name]

| # | Section | Component | Style | Link | Complexity |
|---|---------|-----------|-------|------|------------|
| 1 | [section] | [Name] | [style] | [Source](https://full-url-to-component) | Simple |
| 2 | [section] | [Name] | [style] | [Source](https://full-url-to-component) | Medium |
```

### After each page table, add one-line descriptions:

```markdown
**1. [Name]** — [what it looks like, why it's beautiful]
**2. [Name]** — [description]
```

## Link Format Rules

- ALWAYS use markdown links: `[Site Name](https://full-url)`
- Link directly to the component page, NOT the homepage
- Good: `[Aceternity](https://ui.aceternity.com/components/floating-dock)`
- Bad: `[Aceternity](https://ui.aceternity.com)`
- If component is from 21st.dev, link to the specific component page
- If from a gallery site (Godly, Awwwards), link to the specific showcase

## End Prompt

After ALL page tables:

> Pick numbers to implement (e.g. Landing #1, #3 + Dashboard #2), or ask me to search deeper for a specific page.

## Complexity Levels

| Level | Meaning |
|-------|---------|
| Simple | CSS-only or minimal JS, <50 lines |
| Medium | Hooks/animation, 50-150 lines |
| Advanced | Complex animation/3D/interaction, 150+ lines |

## Style Labels

Glassmorphism, Neumorphism, Brutalism, Minimalism, Bento, Masonry,
Gradient Mesh, Aurora, Particle, Kinetic, Scroll-driven, Parallax,
Floating, Magnetic, Morphing, macOS-style, Spotlight, Glow

## Follow-up Handling

### User picks numbers:
1. WebFetch the source URL for code/implementation
2. Adapt to project stack (check package.json, globals.css)
3. Build component in correct directory
4. Show result, ask for adjustments

### User asks for more on a page:
1. Search deeper with more specific queries for that page
2. Continue numbering from where previous table left off
3. Present additional table

### User asks for a specific section:
1. Find 5-8 variants of that section
2. Present comparison with more detail per entry
