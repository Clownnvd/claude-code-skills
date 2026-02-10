---
name: skill-creator
description: Create or update Claude skills. Use for new skills, skill references, skill scripts, optimizing existing skills, extending Claude's capabilities.
license: Complete terms in LICENSE.txt
---

# Skill Creator

Create effective, token-efficient skills that extend Claude's capabilities with specialized workflows, scripts, and domain knowledge.

## When to Use

- Creating a new skill from scratch
- Updating or optimizing an existing skill
- Adding references, scripts, or assets to a skill
- Packaging a skill for distribution
- Auditing skill quality (metadata, structure, token efficiency)

## Critical Rules

| Rule | Limit |
|------|-------|
| `description` in frontmatter | **< 200 characters**, specific triggers, not generic |
| `SKILL.md` body | **< 150 lines** |
| Each reference file | **< 150 lines** (split if larger) |
| No duplication | Info lives in SKILL.md OR references, never both |
| Writing style | Imperative form ("To accomplish X, do Y"), third-person metadata |
| Scripts | Node.js or Python (not bash). Must have tests. Must respect `.env` hierarchy. |
| Consolidation | Combine related topics into one skill (e.g., mongodb + postgresql → databases) |

## Creation Process

Follow steps in order. See `references/creation-workflow.md` for detailed guidance.

### 1. Understand
Gather concrete examples of how the skill will be used. Ask user for trigger phrases and use cases.

### 2. Research
Search the web for best practices, existing CLI tools (`npx`/`bunx`/`pipx`), workflows, and edge cases.

### 3. Plan
Identify reusable resources: scripts (deterministic tasks), references (documentation), assets (templates/images).

### 4. Initialize
```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```
Creates SKILL.md template + example directories. Delete unused example files after.

### 5. Edit
Write references and scripts first, then SKILL.md last. See `references/writing-guide.md` for style.
- SKILL.md = quick reference index (purpose, when to use, reference directory)
- References = detailed documentation, split by topic
- Scripts = tested, cross-platform code with `.env.example`

### 6. Package & Validate
```bash
scripts/package_skill.py <path/to/skill-folder>
```
Auto-validates (frontmatter, description length, structure) then creates distributable zip.

### 7. Iterate
Use skill on real tasks → notice gaps → update SKILL.md or resources → re-validate.

## Quick Reference

### Overview & Concepts
- `references/overview.md` — What skills are, 3-level loading, anatomy, quality gates, lifecycle

### Skill Anatomy & Writing
- `references/writing-guide.md` — Skill anatomy, writing style, progressive disclosure
- `references/exemplar-patterns.md` — Gold standard patterns from payment-integration skill
- `references/creation-workflow.md` — Detailed step-by-step creation process

### Validation Criteria
- `references/validation-checklist.md` — Quick pre-package checklist
- `references/metadata-quality-criteria.md` — Name/description quality + examples
- `references/token-efficiency-criteria.md` — Size limits, no-duplication rule
- `references/script-quality-criteria.md` — Testing, env vars, cross-platform
- `references/structure-organization-criteria.md` — Directory layout, naming

### Plugin Marketplaces
- `references/plugin-marketplace-overview.md` — Distribution overview
- `references/plugin-marketplace-schema.md` — Manifest schema
- `references/plugin-marketplace-sources.md` — Source registries
- `references/plugin-marketplace-hosting.md` — Hosting options
- `references/plugin-marketplace-troubleshooting.md` — Common issues

### Scripts
- `scripts/init_skill.py` — Initialize new skill directory
- `scripts/quick_validate.py` — Fast validation check
- `scripts/package_skill.py` — Validate + package into zip
