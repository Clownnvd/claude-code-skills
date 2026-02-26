# Criteria: Migration + Monitoring + Backup + DevEx

## Category 6: Migration & Versioning (10%)

### Migration Hygiene (4 points)

| Score | Criteria |
|-------|---------|
| +1 | All schema changes go through migration files (not manual SQL) |
| +1 | Each migration is a single, focused change (not mega-migrations) |
| +1 | Migration files committed to git and never edited after creation |
| +1 | `prisma migrate dev` used locally, `prisma migrate deploy` in CI/CD |
| -1 | Manual schema changes applied directly to production |
| -1 | Existing migrations edited instead of creating new ones |

### Rollback Capability (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Destructive changes (drop column/table) have documented rollback plan |
| +1 | Data migrations preserve original data during transition |
| +1 | Migration tested on staging/copy before production deployment |
| -1 | `DROP TABLE` without backup or migration plan |

### Seeding (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Seed script exists for development environment (`prisma/seed.ts`) |
| +1 | Seed data is realistic (not "test123", "foo@bar.com") |
| +1 | Seed script is idempotent (safe to run multiple times) |
| -1 | No seed script — developers start with empty database |

---

## Category 7: Monitoring & Observability (8%)

### Query Logging (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Slow query logging enabled (queries > 1s flagged) |
| +1 | Prisma `log: ['query', 'warn', 'error']` in development |
| +1 | Production logging excludes query params (prevents PII leaks) |
| -1 | No query logging at all |
| -1 | Full query logging in production (PII risk + performance) |

### Metrics (4 points)

| Score | Criteria |
|-------|---------|
| +1 | Connection pool utilization tracked |
| +1 | Query latency metrics collected (p50, p95, p99) |
| +1 | Active connections count monitored |
| +1 | Database size and growth rate tracked |
| -1 | No database metrics beyond "it works or doesn't" |

### Alerting (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Alert on connection pool exhaustion |
| +1 | Alert on slow queries (> threshold) |
| +1 | Alert on migration failures in CI/CD |
| -1 | No alerting — failures discovered by users |

---

## Category 8: Backup & Recovery (8%)

### Backup Strategy (4 points)

| Score | Criteria |
|-------|---------|
| +1 | Automated backups configured (daily minimum) |
| +1 | Point-in-Time Recovery (PITR) enabled |
| +1 | Backup retention period defined (7+ days) |
| +1 | Backups stored in different region/zone than primary |
| -1 | No automated backups |
| -1 | Backups only on same server as database |

### Recovery Testing (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Restore from backup tested at least once |
| +1 | Recovery time objective (RTO) documented |
| +1 | Recovery point objective (RPO) documented |
| -1 | Backups exist but never tested |

### Disaster Recovery (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Failover strategy documented (even if manual) |
| +1 | Database branching used for risky changes (Neon branches) |
| +1 | Production data is never used directly for testing |
| -1 | Production is single point of failure with no recovery plan |

---

## Category 10: Developer Experience (5%)

### Type Safety (3 points)

| Score | Criteria |
|-------|---------|
| +1 | `prisma generate` in build pipeline (types always fresh) |
| +1 | Generated Prisma types used in application code (not manual interfaces) |
| +1 | TypeScript strict mode enabled in project |
| -1 | Manual type definitions that drift from actual schema |

### Documentation (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Schema has comments on non-obvious fields (`/// Stripe payment intent ID`) |
| +1 | Entity Relationship diagram exists (even text-based) |
| +1 | Database setup instructions in README or CONTRIBUTING.md |
| -1 | No documentation on how to set up local database |

### Local Dev Workflow (4 points)

| Score | Criteria |
|-------|---------|
| +1 | `prisma migrate dev` works out of the box after clone |
| +1 | `.env.example` has all required database env vars |
| +1 | Seed script populates enough data to test all features |
| +1 | Database reset command documented (`prisma migrate reset`) |
| -1 | Complex manual setup required to get database running |

## Scoring Summary

| Sub-area | Max Points |
|----------|-----------|
| Migration Hygiene | 4 |
| Rollback Capability | 3 |
| Seeding | 3 |
| **Migration Total** | **10** |
| Query Logging | 3 |
| Metrics | 4 |
| Alerting | 3 |
| **Monitoring Total** | **10** |
| Backup Strategy | 4 |
| Recovery Testing | 3 |
| Disaster Recovery | 3 |
| **Backup Total** | **10** |
| Type Safety | 3 |
| Documentation | 3 |
| Local Dev Workflow | 4 |
| **DevEx Total** | **10** |
