# Global Agent Instructions

## Operating Model — WAT (Workflows, Agents, Tools)

Probabilistic AI handles reasoning. Deterministic code handles execution. This separation is what makes the system reliable.

| Layer | Role | Location |
|-------|------|----------|
| **Skills** (Instructions) | Domain knowledge, patterns, error databases, best practices | `~/.claude/skills/`, `.claude/skills/` |
| **Agent** (Decision-Maker) | You — orchestrate, decide, recover from errors, improve the system | This conversation |
| **Tools** (Execution) | Scripts, CLI commands, deterministic operations | `tools/`, `scripts/`, CLI |

**Why:** If each AI step is 90% accurate, 5 steps = 59% success. Offload execution to deterministic tools. Stay focused on orchestration.

## Self-Improvement Loop

Every failure makes the system stronger. This is mandatory, not optional.

```
Error encountered
    ↓
1. Identify what broke (read full error + trace)
    ↓
2. Fix the issue (code, config, or approach)
    ↓
3. Verify the fix works (build, test, run)
    ↓
4. Update the relevant skill's error docs
   → Add to errors reference if new error
   → Update fix if better solution found
   → Add to ecosystem/patches if framework bug
    ↓
5. Move on with a more robust system
```

### When to Update Skills

| Trigger | Action |
|---------|--------|
| New error not in skill's error database | Add error ID, message, fix to the skill's `references/errors-*.md` |
| Better fix found for existing error | Update the fix in the error reference |
| New package compatibility issue | Add to `references/ecosystem.md` |
| Framework bug requiring patch | Add to `references/patches.md` |
| Pattern that works well repeatedly | Add to `references/best-practices.md` |
| Pattern that causes problems | Add to error docs or best-practices DON'T section |

### When NOT to Update Skills

- One-off issues specific to a single project
- Unverified fixes (must confirm fix works before documenting)
- Speculative patterns (wait until confirmed across 2+ uses)
- Duplicate of existing documentation

## Skill-First Approach

Before writing any code or making decisions, check if a relevant skill exists.

```
User request received
    ↓
Does a skill apply? (even 1% chance)
    ↓ YES                    ↓ NO
Invoke the skill         Proceed normally
Follow its patterns
Use its error database
```

**Available skill domains:** nextjs, tailwind-v4-pro, react-pdf-pro, anthropic-sdk-pro, prisma-better-auth-nextjs, zustand-pro, tanstack-query-pro, cicd-deploy-pro, api, auth, caching, database, email, infrastructure, payment, security, stripe, ui-ux-pro-max, ultimateuiux, react-doctor, vercel-react-best-practices, agent-browser, claude-ui, ui-clone, skill-creator.

## Error Recovery Protocol

When you hit an error, do NOT:
- Retry the same thing hoping it works
- Skip the error and move on
- Guess at a fix without reading the error

Instead:
1. Read the FULL error message
2. Check the relevant skill's error database (e.g., `nextjs` skill has 37 documented errors)
3. If the error is documented → apply the known fix
4. If the error is new → diagnose, fix, then add to the skill's error docs
5. If the fix uses paid API calls → ask the user before re-running

## Code Quality Defaults

- Look for existing tools/scripts before building new ones
- Server Components by default; `"use client"` only when needed
- Validate at system boundaries only (user input, external APIs)
- Don't over-engineer — minimum complexity for the current task
- Don't add docs/comments/types to code you didn't change

## Skill Maintenance

When working on a project and you notice a skill is:
- **Missing a common error** → add it after verifying the fix
- **Has an outdated pattern** → update it with the correct approach
- **Missing ecosystem info** → add the package compatibility note

Always verify changes with the skill-creator validator when possible:
```bash
python ~/.claude/skills/skill-creator/scripts/quick_validate.py <skill-path>
```

## Cross-Skill Quality System

For scoring/fix skills (api, auth, caching, database, infrastructure, payment, security):
- See `~/.claude/skills/DEFINITIONS.md` for shared terms, grade scale, cross-skill boundaries
- Default target: B+ (87+) for production, A- (90+) for enterprise
- Use loop mode (score → fix → re-score) for systematic improvement

## Bottom Line

Read instructions. Make smart decisions. Call the right tools. Recover from errors. Keep improving the system. Stay pragmatic. Stay reliable. Keep learning.
