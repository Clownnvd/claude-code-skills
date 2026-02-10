# Scoring Workflow

6-step process: gather → score → calculate → issues → report → (optional) re-score.

## Step 1: Gather Files

Collect ALL API-related files before scoring. Do not score from memory.

| File Type | What to look for |
|-----------|-----------------|
| API routes | `src/app/api/**/route.ts` — every handler |
| Middleware | `src/middleware.ts` — auth, headers, CORS |
| Auth config | Auth library setup (Better Auth, NextAuth, etc.) |
| Validation | Zod schemas, validation modules |
| Error handling | Response helpers, error envelope |
| Rate limiting | Rate limit config, presets |
| CSRF | CSRF protection module |
| DB client | Connection config, query patterns |
| Env validation | Env schema, `.env.example` |
| Tests | API test files, mocks, coverage config |
| Package.json | Dependencies, scripts |
| Docs | README, OpenAPI spec, API docs |

## Step 2: Score Each Category (0-10)

For each of the 10 categories:

1. Load the relevant criteria file from `criteria/`
2. Start at **baseline 5** (neutral — not bad, not good)
3. Walk through the checklist:
   - **Missing critical item**: subtract 1
   - **Present with evidence**: keep or add 1
   - **Bonus item present**: add 1 (cap at 10)
4. Require concrete file:line evidence for scores 9-10
5. Never give 10 without checking all bonus items

### Category → Criteria File Mapping

| Categories | Criteria File |
|-----------|--------------|
| 1 Security, 2 Auth & AuthZ | `criteria/security-auth.md` |
| 3 Input Validation, 4 Error Handling | `criteria/input-errors.md` |
| 5 Rate Limiting, 6 Response Design, 7 Performance | `criteria/ratelimit-response-perf.md` |
| 8 Observability, 9 Docs & DX, 10 Testing | `criteria/observability-docs-testing.md` |

### Framework-specific adjustments

| Stack | Additional Reference |
|-------|---------------------|
| Next.js App Router | `nextjs-patterns.md` |

## Step 3: Calculate Weighted Score

```
total = sum(score[i] * weight[i] * 10) for i in 1..10
```

Weights: Security 20%, Auth 15%, Input 12%, Errors 10%, Rate Limit 10%, Response 8%, Performance 8%, Observability 7%, Docs 5%, Testing 5%.

## Step 4: Generate Issues List

For each category scoring < 10:
1. Identify specific gaps (what's missing from the checklist)
2. Assign severity based on score + weight (see overview.md)
3. Include file:line reference
4. Suggest concrete fix

Sort: CRITICAL → HIGH → MEDIUM → LOW.

## Step 5: Output Scorecard

Use the format from `overview.md`. Include:
- Scorecard table with all 10 categories
- Issues list (ordered by severity)
- Quick wins (highest score-per-effort items)
- Path to next grade (what to fix for +X points)

## Step 6: Re-Score (after fixes)

After applying fixes:
1. Re-gather changed files
2. Re-score only changed categories
3. Output comparison table (before → after)
4. Verify no regressions in unchanged categories
