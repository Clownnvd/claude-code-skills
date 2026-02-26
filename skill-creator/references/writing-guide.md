# Writing Guide — Style & Anatomy

## Skill Anatomy

```
.claude/skills/skill-name/
├── SKILL.md              # Required. Quick reference index. < 150 lines.
├── scripts/              # Optional. Executable code (Python/Node.js).
│   ├── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── references/           # Optional. Documentation loaded as needed.
│   ├── topic-a.md        # Each < 150 lines
│   └── subtopic/         # Subdirectories for complex skills
│       ├── overview.md
│       └── api.md
└── assets/               # Optional. Files used in output, not context.
    └── template.html
```

## Progressive Disclosure (3 Levels)

| Level | When Loaded | Size Limit |
|-------|-------------|------------|
| 1. Metadata (name + description) | Always in context | < 200 characters |
| 2. SKILL.md body | When skill triggers | < 150 lines |
| 3. References/Scripts | As Claude decides needed | < 150 lines each (scripts unlimited) |

## SKILL.md Structure Pattern

Follow this order (modeled after payment-integration gold standard):

```markdown
---
name: skill-name
description: Specific action verbs + use cases. Under 200 chars.
---
# Skill Name
Brief purpose (1-2 sentences).

## When to Use
- Trigger scenario 1
- Trigger scenario 2

## [Core Content — tables, rules, decision trees]
Keep brief. Point to references for details.

## Quick Reference
### Category A
- `references/topic-a.md` — Brief description
- `references/topic-b.md` — Brief description

### Scripts
- `scripts/main.py` — What it does
```

## Writing Style

### Imperative form (DO)
- "To accomplish X, do Y"
- "Load `references/api.md` for endpoint details"
- "Run `scripts/validate.py` to check structure"

### NOT second person (DON'T)
- ~~"You should do X"~~
- ~~"If you need to..."~~

### Metadata: Third-person (DO)
- "Integrate payments with Stripe, Paddle. Checkout, webhooks, subscriptions."

### NOT first-person or vague (DON'T)
- ~~"A skill for working with payments"~~
- ~~"This helps you understand payments"~~

## Reference File Style

- Sacrifice grammar for concision
- Tables over paragraphs
- Code blocks over prose
- Each file < 150 lines — split if larger
- Can reference other files: "See `references/api.md` for details"
- Organize in subdirectories for 5+ files per topic

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| SKILL.md > 150 lines | Move details to references |
| Description > 200 chars | Cut to action verbs + key use cases |
| Info in SKILL.md AND references | Single source of truth — pick one |
| Bash scripts | Use Python or Node.js (Windows compat) |
| No tests for scripts | Write tests, run them, verify passing |
| Generic description | Include specific trigger phrases |
| `version` in frontmatter | Removed in newer specs — optional only |
