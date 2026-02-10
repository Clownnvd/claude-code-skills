# Skill Creator — Overview

## What is a Skill?

A skill is a self-contained package that extends Claude's capabilities with domain-specific knowledge, workflows, and executable scripts. Skills are loaded into Claude's context on demand via the Skill tool.

## How Skills Work

```
User request → Claude checks available skills → Matches trigger
  → Loads SKILL.md (always)
  → Loads references/* (on demand, when SKILL.md points to them)
  → Runs scripts/* (via Bash tool, for deterministic tasks)
  → Uses assets/* (copies into output, never loaded into context)
```

### 3-Level Progressive Disclosure

| Level | What Loads | When | Token Cost |
|-------|-----------|------|------------|
| 1. Metadata | `name` + `description` from frontmatter | Every conversation (skill list) | ~20 tokens each |
| 2. SKILL.md body | Full file content | When skill is invoked | < 150 lines |
| 3. References | Individual reference files | When SKILL.md says "load X for Y" | < 150 lines each |

Only Level 1 loads automatically. Levels 2-3 load only when needed. This keeps token usage minimal.

## Skill Anatomy

```
my-skill/
├── SKILL.md              — Entry point (< 150 lines)
├── LICENSE.txt            — Apache 2.0
├── references/            — Detailed docs loaded on demand
│   ├── setup.md           — Installation/configuration
│   ├── api.md             — API reference
│   └── best-practices.md  — Do/Don't/Pitfalls/Checklist
├── scripts/               — Executable code (Python/Node.js)
│   ├── helper.py          — Deterministic tasks
│   └── test_helper.py     — Tests for scripts
└── assets/                — Files for output (templates, images)
    └── template.html      — Copied into user's project
```

### What Goes Where

| Content Type | Location | Loaded Into Context? |
|-------------|----------|---------------------|
| Quick reference, index, when-to-use | `SKILL.md` | Yes (always on invoke) |
| Detailed docs, API refs, workflows | `references/*.md` | Yes (on demand) |
| Crypto, file I/O, validation, builds | `scripts/*.py|js` | No (executed via Bash) |
| Templates, images, boilerplate | `assets/*` | No (copied to output) |

## When to Use Scripts vs References

| Task | Use Script | Use Reference |
|------|-----------|--------------|
| HMAC signature verification | Yes | No |
| Scaffold new files/directories | Yes | No |
| Validate format/structure | Yes | No |
| Explain architecture patterns | No | Yes |
| Provide API endpoint docs | No | Yes |
| List best practices / pitfalls | No | Yes |
| Generate deterministic output | Yes | No |
| Guide decision-making | No | Yes |

**Rule of thumb**: If a human would use a calculator or a script for it, use a script. If a human would read a doc for it, use a reference.

## Quality Gates

### Metadata
- `name`: kebab-case, 3-40 chars, matches directory name
- `description`: < 200 chars, includes WHEN to use (trigger phrases)

### Size Limits
- `SKILL.md`: < 150 lines
- Each reference file: < 150 lines (split if larger)
- No duplication between SKILL.md and references

### Scripts
- Language: Python or Node.js (not bash — cross-platform)
- Must have tests
- Must use `.env` hierarchy (env var → config file → default)
- Must handle Windows encoding (`encoding_utils.py`)

## Lifecycle

```
1. Understand  → Gather use cases and trigger phrases
2. Research    → Search web for best practices, existing tools
3. Plan        → Identify what needs scripts vs references vs assets
4. Initialize  → `scripts/init_skill.py <name> --path <dir>`
5. Edit        → Write references first, then scripts, SKILL.md last
6. Validate    → `scripts/quick_validate.py <skill-dir>`
7. Package     → `scripts/package_skill.py <skill-dir>`
8. Iterate     → Use on real tasks → find gaps → update → re-validate
```

## Common Patterns

### Index Pattern (SKILL.md as pure router)
SKILL.md contains zero implementation detail — only:
- When to use
- Quick decision table
- Pointers to references

Example: `payment-integration` — 5 providers, SKILL.md just routes to the right reference.

### Workflow Pattern (sequential steps)
SKILL.md contains the high-level flow. Each step points to a reference for detail.

Example: `ui` skill — score → fix → verify → re-score pipeline.

### Guidelines Pattern (rules + checklist)
SKILL.md contains rules inline (they're short enough). References only for deep-dive topics.

Example: `verification-before-completion` — rules fit in SKILL.md, no references needed.
