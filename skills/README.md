# Claude Code Skills

10 quality-system skills for Next.js full-stack applications. Each domain skill has 7 modes: score, fix, loop, generate, review, migrate, test.

## Skills Overview

| Skill | Domain | Categories | Modes |
|-------|--------|-----------|-------|
| **api** | API route quality | Security, Auth, Input, Error, Rate Limit, Response, Perf, Observability, Docs, Testing | score, fix, loop, generate, review, migrate, test |
| **auth** | Authentication & authorization | Sessions, Passwords, OAuth, Email, CSRF, Headers, Rate Limit, Audit, RBAC, 2FA | score, fix, loop, generate, review, migrate, test |
| **caching** | Cache strategy | Headers, Revalidation, Static/Dynamic, ISR, cache(), "use cache", CDN, Dedup, Proxy, Monitoring | score, fix, loop, generate, review, migrate, test |
| **database** | Database design & operations | Schema, Integrity, Indexing, Security, Query Perf, Migration, Monitoring, Backup, Scale, DX | score, fix, loop, generate, review, migrate, test |
| **dataflow** | Server-client data flow | RSC Fetching, Composition, Prisma, API Routes, State, Caching, Types, Errors, Forms, DTOs | score, fix, loop, generate, review, migrate, test |
| **infrastructure** | Deploy & infrastructure | Docker, CI/CD, Env Config, Monitoring, Logging, CDN, DNS, SSL, Scaling, Disaster Recovery | score, fix, loop, generate, review, migrate, test |
| **scalability** | Scale & performance | Load Handling, DB Scaling, Cache Scaling, Queue, Microservices, Edge, Storage, Monitoring, Cost, Capacity | score, fix, loop, generate, review, migrate, test |
| **security** | Application security | OWASP Top 10, Input Sanitization, Auth Security, Data Protection, Headers, CORS, CSP, Secrets, Deps, Logging | score, fix, loop, generate, review, migrate, test |
| **ui** | UI quality | Visual Hierarchy, Color, Typography, Spacing, Responsive, Interactions, A11y, Content, Conversion, Perf | research, score, fix, pipeline |
| **skill-creator** | Create new skills | — | create |

## Directory Structure

```
skills/
├── DEFINITIONS.md          # Shared terms across all skills
├── README.md               # This file
└── {skill}/
    ├── SKILL.md             # Entry point (<150 lines)
    ├── LICENSE.txt           # Apache 2.0
    ├── assets/templates/    # Output templates (scorecard, fix-report, generated-code, review-report, migration-report, test-suite)
    ├── evals/               # 9 JSON eval files per skill
    └── references/
        ├── scoring/         # Criteria, workflow, best practices
        │   └── criteria/    # Per-category scoring criteria
        ├── fix/             # Fix patterns, workflow, verification
        │   └── fix-patterns/ # Per-category fix patterns
        ├── generate/        # Code generation workflow
        ├── review/          # Quick file review workflow
        ├── migrate/         # Framework migration workflow
        └── test/            # Test generation workflow
```

## Modes

| Mode | Trigger | Flow |
|------|---------|------|
| **score** | "score {domain}", "audit {domain}" | Read code → Score 10 categories → Weighted total → Grade + issues |
| **fix** | "fix {domain}", provide scorecard | Parse scorecard → Prioritize by severity×weight → Apply fixes → Verify |
| **loop** | "{domain} loop", "score and fix until B+" | Score → Fix → Re-score → Repeat (max 5, stop on plateau) |
| **generate** | "generate {type} for {domain}" | Load criteria → Generate code meeting all 10 → Self-check |
| **review** | "review {file}" | Read 1-2 files → Score applicable categories → Annotate + suggest fixes |
| **migrate** | "migrate {domain} to {version}" | Detect versions → Map breaking changes → Migrate → Verify |
| **test** | "generate tests for {domain}" | Map categories to assertions → Generate test files + coverage matrix |
| **research** | (ui only) "research {page}" | Extract tokens → Search → Fetch → Design Brief |
| **pipeline** | (ui only) "ui pipeline" | Research → Build → Score → Fix loop → Ship |

## Scoring System

- **Scale**: 0-100 weighted score, letter grade A+ to F
- **Baseline**: 7/10 raw = meets basic expectations
- **Anti-bias**: Start at 7, penalize missing items, 9-10 requires evidence
- **Weights**: 10 categories per skill, weights sum to 100%

## Quality Gates

| Context | Grade | Score |
|---------|-------|-------|
| Prototype | C+ | 77+ |
| Production | B+ | 87+ |
| Enterprise | A- | 90+ |

## License

Apache License 2.0. See individual skill `LICENSE.txt` files.
