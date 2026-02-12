# Verification & Re-Scoring

## Post-Fix Checklist

After applying all fixes, verify:

### 1. Build Integrity
```bash
pnpm typecheck    # 0 TypeScript errors
pnpm test:run     # All tests pass
pnpm build        # Builds successfully
```

### 2. CI Pipeline (if modified)
- [ ] Workflow YAML is valid (use `actionlint` or push to branch)
- [ ] All jobs defined (lint, typecheck, test, build)
- [ ] Caching configured correctly
- [ ] Timeout limits set
- [ ] Triggers correct (push, PR)

### 3. Docker (if modified)
- [ ] `docker build .` succeeds
- [ ] Image size is reasonable (< 500MB)
- [ ] Non-root user configured
- [ ] Health check works
- [ ] .dockerignore excludes node_modules, .git, .env

### 4. Environment
- [ ] All env vars validated at startup
- [ ] .env.example matches actual usage
- [ ] No secrets in source code
- [ ] .env in .gitignore

### 5. Monitoring
- [ ] `/api/health` returns 200
- [ ] `/api/ready` checks DB connection
- [ ] Structured logging in place
- [ ] Error tracking configured (or documented as TODO)

### 6. Backup
- [ ] Migration files versioned
- [ ] Seed script works
- [ ] Backup strategy documented

### 7. Integrations
- [ ] All external calls have timeout
- [ ] Webhook signature verification present
- [ ] Webhook idempotency implemented
- [ ] Error logging on integration failures

## Re-Scoring Protocol

1. Run `infra-scoring` skill again
2. Compare old vs new scores per category
3. Verify total score meets target
4. If target not met, identify remaining issues and loop

## Score Progression Tracking

```
Round 1: XX/100 (Grade) — N issues fixed
Round 2: XX/100 (Grade) — N issues fixed
Round 3: XX/100 (Grade) — Final
```

## When to Stop

- Target grade reached (B+ for production, A- for enterprise)
- Remaining issues are external dependencies (provider features, paid services)
- Remaining issues require infrastructure changes beyond code (DNS, firewall, etc.)
- User confirms acceptable score
