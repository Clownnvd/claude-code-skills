# Creation Workflow — Detailed

## Step 1: Understand the Skill

Gather concrete examples of skill usage. Use `AskUserQuestion` tool.

**Key questions:**
- "What tasks should this skill handle?"
- "Give examples of how it would be used"
- "What phrases should trigger this skill?"

**Example (image-editor skill):**
- "Remove red-eye from this image"
- "Rotate this photo 90 degrees"
- "Crop the background out"

Conclude when trigger phrases and use cases are clear.

## Step 2: Research

Effective skills codify real professional workflows. Research on the web:
- Best practices & industry standards
- Existing CLI tools (`npx`, `bunx`, `pipx`) — prefer these over custom code
- Workflows & success case studies
- Common patterns and edge cases

Use multiple `WebFetch`/`WebSearch` tools and `Explore` subagents in parallel.

## Step 3: Plan Resources

For each use case, identify what reusable resources to bundle:

| Resource Type | When to Include | Example |
|---------------|----------------|---------|
| `scripts/` | Same code rewritten repeatedly, deterministic tasks | `rotate_pdf.py` |
| `references/` | Documentation Claude needs while working | `schema.md`, `api.md` |
| `assets/` | Files used in output (not loaded into context) | `template.html`, `logo.png` |

Check existing skills catalog — avoid duplicating functionality.

## Step 4: Initialize

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates: SKILL.md template, scripts/, references/, assets/ with examples.
Delete unused example files immediately.

## Step 5: Edit — Order of Operations

**Write resources first, SKILL.md last.**

### 5a. Scripts (if needed)
- Node.js or Python (cross-platform, not bash)
- Include tests — run them, fix failures, repeat until green
- Add `.env.example` for required env vars
- Respect `.env` hierarchy: `process.env` > skill `.env` > global `.env`
- Manually test with real use cases

### 5b. References
- Each file < 150 lines — split by topic if larger
- Concise: sacrifice grammar for brevity
- Can cross-reference other references or scripts
- Organize in subdirectories for complex skills (see `references/exemplar-patterns.md`)

### 5c. SKILL.md (last)
- Purpose (2-3 sentences)
- "When to Use" trigger list
- Critical rules (table format)
- Brief process overview (pointers to references)
- Quick Reference directory (index ALL references and scripts)

See `references/writing-guide.md` for writing style.

## Step 6: Package & Validate

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Checks: YAML frontmatter, description < 200 chars, structure, naming.
Fix errors → re-run until clean.

## Step 7: Iterate

1. Use skill on real tasks
2. Notice struggles, missing info, or wasted tokens
3. Update SKILL.md or resources
4. Re-validate and re-package
