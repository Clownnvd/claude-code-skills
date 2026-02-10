# Infrastructure Scoring Workflow

## Step 1: Gather Files

Read these files (minimum set):
```
.github/workflows/**           # CI/CD pipelines
Dockerfile                     # Container config
docker-compose.yml             # Multi-container setup
vercel.json / fly.toml         # Platform config
package.json                   # Build/test/lint scripts
src/lib/env.ts                 # Env validation
.env.example                   # Env documentation
src/app/api/health/route.ts    # Health checks
src/app/api/ready/route.ts     # Readiness probes
src/lib/api/logger.ts          # Structured logging
prisma/schema.prisma           # DB schema
prisma/migrations/             # Migration history
```

## Step 2: Score Each Category

For each category:
1. Read the criteria checklist (10 items per category)
2. Check how many items are met
3. Note deductions with specific file:line references
4. Assign score 0-10

## Step 3: Calculate Weighted Total

```
total = sum(score[i] * weight[i]) for i in 1..10
```

Weights: CI(15) + CD(12) + Deploy(10) + Container(12) + Env(10) + Monitor(15) + Backup(10) + Integrations(8) + IaC(4) + DeploySec(4) = 100%

## Step 4: Assign Grade

Use grade scale from SKILL.md.

## Step 5: List Issues

For each deduction:
- **Severity**: CRITICAL (blocks production), HIGH (significant risk), MEDIUM (best practice), LOW (nice-to-have)
- **Category**: Which scoring category
- **File:Line**: Exact location or missing file
- **Issue**: What's wrong or missing
- **Fix**: How to fix it

## Step 6: Output Scorecard

Use the template from overview.md.

## Platform-Specific Adjustments

### Vercel Deployment
- Automatic preview deploys = +1 to CD
- Built-in CI = +1 to CI if no custom pipeline
- Serverless = Container category redistributes: +6% to CI, +6% to Monitoring
- Built-in analytics = +1 to Monitoring

### Self-Hosted (Docker/VPS)
- Full container scoring applies
- No free preview deploys = standard CD scoring
- Must provide own monitoring = standard Monitoring scoring

### Small Project (<5 devs)
- IaC weight (4%) redistributes to Environment Management (+4%)
- Deployment Security weight (4%) redistributes to Monitoring (+4%)
