# Eval: Research Workflow

Validate the core research-sites workflow produces correct, structured output.

---

## Test 1: Per-Page Component Table

**Input**: "Research components for a landing page"
**Expected**:
- Output contains a `## Landing Page` section
- Table has columns: #, Section, Component, Style, Link, Complexity
- Table contains at least 3 rows covering different sections (hero, nav, features, etc.)
- Each row has a non-empty value in every column
- Below the table, numbered descriptions explain each component

**Pass criteria**: Table renders valid markdown with no empty cells.

---

## Test 2: Direct URL Links

**Input**: "Research dashboard components"
**Expected**:
- Every Link cell contains a markdown link: `[Source](https://full-url)`
- Links point to specific component pages, not site homepages
- Good: `[Aceternity](https://ui.aceternity.com/components/floating-dock)`
- Bad: `[Aceternity](https://ui.aceternity.com)`
- All URLs are reachable HTTPS links

**Pass criteria**: Zero homepage-only links. All links contain a path beyond the domain.

---

## Test 3: Multiple Sources

**Input**: "Research auth page components"
**Expected**:
- Results include components from at least 3 different sources
- Sources drawn from: 21st.dev, Aceternity, Magic UI, Origin UI, shadcn, Godly
- No single source dominates more than 50% of results
- Source names match the actual site (not fabricated)

**Pass criteria**: >= 3 distinct source domains across the table.

---

## Test 4: Per-Page Organization

**Input**: "Research all pages" (landing, dashboard, auth, billing)
**Expected**:
- Output has 4 separate `## [Page] Page` sections
- Each section has its own table with independent numbering starting at 1
- Sections cover page-appropriate components (hero for landing, sidebar for dashboard)
- Ends with the pick prompt: "Pick numbers to implement..."
- No mixing of page types within a single table

**Pass criteria**: 4 distinct sections, each with own table, correct section types.

---

## Test 5: Complexity and Style Labels

**Input**: "Research landing page hero sections"
**Expected**:
- Complexity column uses only: Simple, Medium, Advanced
- Style column uses labels from the defined set (Glassmorphism, Aurora, Parallax, etc.)
- Simple = CSS-only or <50 lines; Medium = hooks/animation 50-150; Advanced = 150+
- No invented complexity levels or unlabeled entries

**Pass criteria**: All rows use valid complexity and style labels.
