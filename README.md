# Claude Code Skills

Enterprise-grade skills for [Claude Code](https://claude.com/claude-code) — audit, score, and fix Next.js applications across 8 domains.

## What's Inside

### Scoring & Fix Pairs (8 domains, 16 skills)

Each domain has a **scoring** skill (audit + scorecard) and a **fix** skill (auto-fix from scorecard).

| Domain | Scoring | Fix | Categories |
|--------|---------|-----|------------|
| **API** | `api-scoring` | `api-fix` | Security, auth, validation, errors, rate limiting, response design, performance, observability, docs, testing |
| **Auth** | `auth-scoring` | `auth-fix` | Better Auth, sessions, OAuth, RBAC, passwords, email verification, rate limiting, CSRF, headers, audit logging |
| **Caching** | `caching-scoring` | `caching-fix` | Cache headers, revalidation, static/dynamic, ISR, React cache(), unstable_cache, CDN, request dedup, middleware, monitoring |
| **Dataflow** | `dataflow-scoring` | `dataflow-fix` | RSC, Prisma, API routes, caching, state, types, errors, forms, DTOs, loading |
| **Database** | `db-scoring` | `db-fix` | Schema, security, indexing, performance, migration, monitoring, backup, scalability, DevEx |
| **Infrastructure** | `infra-scoring` | `infra-fix` | CI/CD, containerization, monitoring, backup/DR, third-party integrations, IaC, deploy security |
| **Scalability** | `scalability-scoring` | `scalability-fix` | Bundle size, images, RSC, DB queries, API perf, client rendering, edge/CDN, memory, concurrency, monitoring |
| **Security** | `security-scoring` | `security-fix` | Input validation, secrets, dependencies, info disclosure, CSP, data protection, redirects, webhooks, monitoring, supply chain |

### UI/UX Skills (3 skills)

| Skill | Description |
|-------|-------------|
| `ui` | UI quality system — 4 modes: research, score (10-category audit), fix, pipeline (end-to-end) |
| `ui-ux-pro-max` | Design intelligence — 67 styles, 96 palettes, 57 font pairings, stack-specific guidelines |
| `research-sites` | Research UI by page type (landing, dashboard, auth, billing) with direct component links |

### Tooling (1 skill)

| Skill | Description |
|-------|-------------|
| `skill-creator` | Create or update Claude Code skills — templates, validation, packaging |

---

## Installation

### Option 1: Copy specific skills (recommended)

Copy only the skills you need into your project's `.claude/skills/` directory:

```bash
# Clone the repo
git clone https://github.com/Clownnvd/claude-code-skills.git

# Copy a specific skill pair into your project
cp -r claude-code-skills/skills/security-scoring your-project/.claude/skills/
cp -r claude-code-skills/skills/security-fix your-project/.claude/skills/
```

### Option 2: Copy all skills

```bash
# Clone the repo
git clone https://github.com/Clownnvd/claude-code-skills.git

# Copy all skills into your project
cp -r claude-code-skills/skills/* your-project/.claude/skills/
```

### Option 3: Symlink (for development)

```bash
# Clone once, symlink into any project
git clone https://github.com/Clownnvd/claude-code-skills.git ~/claude-code-skills

# Symlink specific skills
ln -s ~/claude-code-skills/skills/api-scoring your-project/.claude/skills/api-scoring
ln -s ~/claude-code-skills/skills/api-fix your-project/.claude/skills/api-fix
```

### Verify Installation

After copying, your project structure should look like:

```
your-project/
  .claude/
    skills/
      api-scoring/
        SKILL.md
        references/
          criteria/
          ...
      api-fix/
        SKILL.md
        references/
          fix-patterns/
          ...
      ...
```

Claude Code will automatically detect skills in `.claude/skills/`.

---

## Usage

### Run a scoring audit

Tell Claude Code to use the skill:

```
Score my API routes using api-scoring
```

or

```
Run security-scoring on this project
```

Claude will produce a scorecard like:

```
| # | Category        | Weight | Score | Weighted | Issues |
|---|-----------------|--------|-------|----------|--------|
| 1 | Input Validation| 15%    | 8/10  | 12.0     | ...    |
| ...                                                      |
| Total             | 100%   |       | 87.5/100 |        |
| Grade             |        |       | B+       |        |
```

### Fix all issues

Pass the scorecard to the fix skill:

```
Run security-fix to reach A+
```

Claude will:
1. Parse the scorecard
2. Prioritize by severity x weight
3. Apply code changes
4. Verify (tsc + tests)
5. Re-score until target reached

### Score -> Fix pipeline (example)

```
1. Run caching-scoring        → 65/100 (D)
2. Run caching-fix             → fixes applied
3. Re-score                    → 97/100 (A+)
```

---

## Skill Structure

Each skill follows the same pattern:

```
skill-name/
  SKILL.md                          # Entry point — when to use, categories, grade scale
  references/
    overview.md                     # Scope, output format
    scoring-workflow.md             # Step-by-step audit process
    best-practices.md              # Do/Don't tables
    criteria/                      # 5 files covering 10 categories (scoring only)
      category-pair-1.md
      category-pair-2.md
      ...
    fix-patterns/                  # 5 files covering 10 categories (fix only)
      category-pair-1.md
      category-pair-2.md
      ...
```

### Grade Scale (all scoring skills)

| Grade | Score | Meaning |
|-------|-------|---------|
| A+ | 97-100 | Exceptional |
| A | 93-96 | Enterprise-grade |
| A- | 90-92 | Near-enterprise |
| B+ | 87-89 | Professional |
| B | 83-86 | Production-ready |
| B- | 80-82 | Acceptable |
| C+ | 77-79 | Needs improvement |
| C | 70-76 | Minimum viable |
| D | 60-69 | Below standard |
| F | <60 | Critical issues |

---

## Tech Stack Compatibility

These skills are optimized for:

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **ORM**: Prisma
- **Auth**: Better Auth
- **Payments**: Stripe
- **Styling**: Tailwind CSS
- **Testing**: Vitest

Most scoring criteria are framework-agnostic (security, API design, caching patterns). Platform-specific adjustments are documented in each skill.

---

## License

MIT
