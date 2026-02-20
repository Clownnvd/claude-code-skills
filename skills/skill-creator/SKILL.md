---
name: skill-creator
description: Create, update, validate Claude skills. Triggers on: new skill from scratch, optimize existing skill, add references/scripts, package for distribution, audit skill quality.
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

## Skill Types

| Type | Template | Best For |
|------|----------|----------|
| General | `SKILL.md.template` | Custom workflows, guidelines |
| Scoring | `scoring-skill.md.template` | Audit/grade against criteria |
| Fix | `fix-skill.md.template` | Implement fixes from scoring |
| Generate | `generate-skill.md.template` | Create new code/content |
| Migrate | `migrate-skill.md.template` | Version upgrades |
| Review | `review-skill.md.template` | Code review/audit |
| Test | `test-skill.md.template` | Testing workflows |

To select type: see `references/skill-type-selection.md`

## Creation Process

Follow steps in order. See `references/creation-workflow.md` for detailed guidance.

1. **Understand** — Gather trigger phrases, use cases, concrete examples
2. **Research** — Search web for best practices, existing CLI tools, edge cases
3. **Plan** — Identify scripts (deterministic tasks), references (docs), assets (templates)
4. **Initialize** — `scripts/init_skill.py <skill-name> --path <output-directory>`
5. **Edit** — Write references/scripts first, then SKILL.md last (see `references/writing-guide.md`)
6. **Validate** — `scripts/quick_validate.py <path>` then `scripts/package_skill.py <path>`
7. **Iterate** — Use on real tasks → notice gaps → update → re-validate

## Quick Reference

### Overview & Guides
- `references/overview.md` — What skills are, 3-level loading, anatomy, quality gates
- `references/writing-guide.md` — Writing style, progressive disclosure
- `references/creation-workflow.md` — Detailed step-by-step creation process
- `references/exemplar-patterns.md` — Gold standard patterns (payment-integration, simple, paired)
- `references/end-to-end-example.md` — Full walkthrough: code-review skill from scratch

### Skill Type Guides
- `references/skill-type-selection.md` — Decision tree for choosing skill type
- `references/skill-type-patterns.md` — Architecture patterns per type

### Validation Criteria
- `references/validation-checklist.md` — Quick pre-package checklist
- `references/metadata-quality-criteria.md` — Name/description quality + examples
- `references/token-efficiency-criteria.md` — Size limits, no-duplication rule
- `references/script-quality-criteria.md` — Testing, env vars, cross-platform
- `references/structure-organization-criteria.md` — Directory layout, naming

### Plugin Marketplaces
- `references/plugin-marketplace/overview.md` — Distribution overview
- `references/plugin-marketplace/schema.md` — Manifest schema
- `references/plugin-marketplace/sources.md` — Source registries
- `references/plugin-marketplace/hosting.md` — Hosting options
- `references/plugin-marketplace/troubleshooting.md` — Common issues

### Scripts
- `scripts/init_skill.py` — Initialize new skill directory
- `scripts/quick_validate.py` — Fast validation (metadata, size, tests)
- `scripts/package_skill.py` — Validate + package into zip

### Skill Templates
Templates in `assets/templates/` — fill `{{VARIABLE}}` placeholders:
- `SKILL.md.template` — General skill definition
- `scoring-skill.md.template` / `fix-skill.md.template` — Scoring/fix pair
- `generate-skill.md.template` — Generate-type skill
- `migrate-skill.md.template` — Migration-type skill
- `review-skill.md.template` — Review-type skill
- `test-skill.md.template` — Test-type skill
- `reference.md.template` / `script.py.template` — Reference doc / Python script
