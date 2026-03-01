# Rollback Strategies

## Vercel Instant Rollback

**Dashboard:**
1. Go to Project -> Deployments
2. Find the last known good deployment
3. Click the three dots menu (...)
4. Select "Instant Rollback"

**CLI:**
```bash
# List recent deployments
vercel ls

# Rollback to specific deployment
vercel rollback [deployment-url]

# Undo rollback (re-enable auto-promotion)
vercel promote
```

**Important notes:**
- Hobby plan: can only rollback to the immediately previous deployment
- Pro/Enterprise: can rollback to any previous production deployment
- After rollback, auto-promotion is disabled -- new pushes to main do NOT automatically become production
- To re-enable: click "Undo Rollback" in dashboard or run `vercel promote`
- Environment variables are NOT updated during rollback (uses the deployment's original env vars)

## Docker Rollback

```bash
# Tag-based rollback
docker pull ghcr.io/your-org/cviet:v1.2.3  # Previous version
docker compose down
docker compose up -d

# SHA-based rollback
docker pull ghcr.io/your-org/cviet:abc1234  # Previous commit SHA
docker compose down
docker compose up -d
```

## Git-Based Rollback

```bash
# Revert the problematic commit(s)
git revert HEAD         # Revert last commit
git revert HEAD~3..HEAD # Revert last 3 commits
git push origin main    # Triggers new deployment

# OR: force deploy a specific commit (Vercel)
vercel --prod --force
```

## Database Rollback Considerations

**Prisma Migrate does NOT support automatic rollback.** If a migration breaks production:

1. **Forward fix:** Create a new migration that undoes the changes
2. **Neon time travel:** Neon supports point-in-time restore (PITR) up to 7 days (Free) or 30 days (Pro)
3. **Manual SQL:** Connect directly and run corrective SQL

```bash
# Neon PITR (restore to 5 minutes ago)
# Done via Neon Console: Project -> Branches -> Restore
```

## Rollback Decision Matrix

| Scenario | Strategy | Time to Recover |
|----------|----------|----------------|
| Bad code, data OK | Vercel Instant Rollback | < 30 seconds |
| Bad code, need rebuild | Git revert + push | 2-5 minutes |
| Bad migration, data OK | Forward migration fix | 5-15 minutes |
| Data corruption | Neon PITR + redeploy | 15-30 minutes |
| Complete failure | Restore from backup + DNS switch | 30-60 minutes |
