# Handoff Contracts

Exact data formats passed between pipeline stages. Each skill must output in this format for the next skill to consume.

## Research → Build: Design Brief

```markdown
## Design Brief: [Page Name]

### Direction
- **Vibe**: [professional / minimal / bold / luxury]
- **Layout**: [described structure]
- **Primary color**: [value from globals.css token]
- **Inspiration sources**: [3+ URLs with notes]

### Component Plan
| Component | Pattern | Source |
|-----------|---------|--------|
| Hero | text-left + image-right, dual CTAs | [URL] |
| Features | bento grid, 3-col | [URL] |
| ... | ... | ... |

### Design Tokens (from project theme)
- Primary: `var(--primary)` — [oklch value]
- Accent: `var(--accent)` — [oklch value]
- Font: [system/custom] — [weights used]

### Anti-Patterns to Avoid
- [Specific items from anti-ai-patterns.md check]
```

**Validation rules**:
- Must include 3+ inspiration URLs
- Must reference project design tokens (not hardcoded)
- Must include component plan table
- Must include anti-patterns section

## Build → Scoring: File Manifest

```markdown
## Files to Score

### Page: [page name]
- `src/app/(landing)/page.tsx`
- `src/components/landing/hero-section.tsx`
- `src/components/landing/features-section.tsx`
- ...

### Shared Dependencies
- `src/app/globals.css`
- `src/utils/cn.ts`
- `src/config/product.ts`
```

**Validation rules**:
- All file paths must exist (Read-verified)
- Must include globals.css / theme config
- Must include page entry point

## Scoring → Fix: Scorecard

```markdown
## UI Scorecard: [Page Name]

| # | Category | Weight | Score | Issues |
|---|----------|--------|-------|--------|
| 1 | Visual Hierarchy | 15% | 8/10 | [specific issue] |
| ... | ... | ... | ... | ... |
| **Total** | | 100% | **XX/100** | |

### Critical (0-3)
1. [Issue] → [Suggested fix] → [Files affected]

### Improvement (4-6)
1. [Issue] → [Suggested fix] → [Files affected]

### Nice-to-have (7-8)
1. [Issue] → [Suggested fix] → [Files affected]
```

**Validation rules**:
- All 10 categories must have scores
- Each issue must have: description, suggested fix, affected files
- Severity classification must be present
- Weighted total must be mathematically correct

## Fix → Scoring: Fix Report

```markdown
## Fixes Applied: [Page Name] — Iteration N

### Changes
1. [Fix description] → [files modified]
2. ...

### Verification
- TypeScript: PASS / FAIL
- Tests: PASS / FAIL / SKIPPED
- Build: PASS / FAIL / SKIPPED

### Files Modified
- `src/components/landing/hero-section.tsx`
- ...
```

**Validation rules**:
- TypeScript must PASS before re-scoring
- All modified files must be listed
- Fix descriptions must map back to scorecard issues

## Cross-Skill Validation

Before each handoff, verify:
1. Output format matches contract above
2. All required sections present
3. No placeholder/TODO text remaining
4. File paths verified to exist
