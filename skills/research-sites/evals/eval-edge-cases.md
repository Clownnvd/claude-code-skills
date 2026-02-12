# Eval: Edge Cases — research-sites

Validate graceful handling of unusual inputs and failure conditions.

---

## Test 1: Unknown Page Type

**Input**: "Research components for an onboarding wizard page"
**Expected**:
- Skill does NOT refuse or error out
- Maps to nearest known type or creates a reasonable section list
- Output still follows per-page table format with #, Section, Component, Style, Link, Complexity
- Asks clarifying question if page type is truly ambiguous

**Pass criteria**: Valid table output or clarifying question. Never a refusal.

---

## Test 2: Unreachable Source Site

**Input**: Research triggers WebFetch on a URL that returns 404 or timeout
**Expected**:
- Skip the unreachable source and continue with remaining sources
- Do NOT include broken links in the output table
- Do NOT hallucinate component details from an unreachable page
- Output contains results from at least 2 other working sources

**Pass criteria**: No broken links in final table. Research completes with available sources.

---

## Test 3: Framework-Specific Filtering

**Input**: "Research landing page components for Vue/Nuxt (not React)"
**Expected**:
- Prioritize Vue-compatible sources (Inspira UI, general CSS solutions)
- Exclude React-only libraries (Aceternity, Magic UI) or note incompatibility
- Still follow the standard table format
- Link column points to Vue-compatible component pages

**Pass criteria**: No React-only components presented without a compatibility note.

---

## Test 4: Single Section Deep Dive

**Input**: "Find 5 hero section variants for my landing page"
**Expected**:
- Output is a single table focused on hero sections only
- Contains at least 5 rows, all Section = "Hero"
- Each row shows a distinct variant (Aurora, Parallax, Video, 3D, Kinetic, etc.)
- Descriptions below the table differentiate each variant clearly

**Pass criteria**: >= 5 hero variants, all distinct styles, single-section table.

---

## Test 5: Follow-Up Numbering Continuity

**Input**: User first requests landing page research (gets #1-#6), then asks "show me more"
**Expected**:
- Additional results continue numbering from #7 onward
- No duplicate components from the first batch
- New results come from deeper or different search queries
- Table format remains identical to the first batch

**Pass criteria**: Numbering continues without gaps or duplicates.

---

## Test 6: Empty Search Results

**Input**: Research a very niche section type, e.g., "3D product configurator component"
**Expected**:
- If no results found from standard sources, report honestly
- Suggest alternative search terms or related components
- Do NOT fabricate component names or URLs
- Offer to broaden the search

**Pass criteria**: No fabricated links. Honest "no results" with suggestions.
