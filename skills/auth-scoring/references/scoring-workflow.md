# Auth Scoring Workflow

## Step 1: Gather Auth Files

Read these files (adapt paths to project):

| File Pattern | What to Check |
|---|---|
| `src/lib/auth.ts` | Better Auth config, plugins, providers, hooks |
| `src/lib/auth/*.ts` | Audit logging, helpers, types |
| `src/middleware.ts` | Route protection, security headers, CSRF |
| `src/lib/csrf.ts` | CSRF origin/referer validation |
| `src/lib/rate-limit.ts` | Auth route rate limiting config |
| `src/lib/validations/*.ts` | Password schema, input validation |
| `src/app/api/auth/**` | Auth API routes |
| `src/app/(auth)/**` | Auth pages (sign-in, sign-up, forgot-password) |
| `prisma/schema.prisma` | User, Session, Account models |
| `.env.example` | Required auth env vars |

## Step 2: Score Each Category

Start each category at 5 (neutral). Adjust up/down based on criteria.

Load the relevant `criteria/*.md` file for each pair:
- Categories 1-2: `criteria/sessions-passwords.md`
- Categories 3-4: `criteria/oauth-email.md`
- Categories 5-6: `criteria/csrf-headers.md`
- Categories 7-8: `criteria/ratelimit-audit.md`
- Categories 9-10: `criteria/authz-2fa.md`

### Scoring Adjustments

| Finding | Adjustment |
|---------|------------|
| Industry best practice implemented | +1 to +2 |
| Meets minimum standard | 0 (stays at 5) |
| Missing expected feature | -1 to -2 |
| Security vulnerability | -3 to -5 |
| Complete absence | Score = 0 |

## Step 3: Calculate Weighted Score

```
total = sum(score[i] * weight[i]) for each category
grade = lookup(total) from grade scale
```

## Step 4: Identify Issues

For each category scoring < 8:
1. List specific issues found
2. Assign severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Sort by: CRITICAL first, then by weight × gap descending

## Step 5: Generate Quick Wins

Quick wins = fixes that:
- Take < 30 minutes
- Move score by >= 2 points in a category
- Require no architectural changes

## Step 6: Output Report

Use the template from `references/overview.md`. Include:
- Full scorecard table
- Issues list sorted by priority
- Quick wins section
- Framework-specific notes (load `references/better-auth-patterns.md`)
