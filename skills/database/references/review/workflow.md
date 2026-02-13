# Database Review Workflow

## Process

1. **Read** — Load target file(s): schema.prisma, query files, migration files
2. **Classify** — Determine applicable categories:
   - schema.prisma → Schema Design, Integrity, Indexing, Security, Scalability, DX
   - Query file → Query Performance, Security, Monitoring
   - Migration file → Migration & Versioning, Backup
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — Cite line numbers, explain issues
5. **Suggest** — Concrete fixes with Prisma syntax
6. **Summarize** — Score, priorities, quick wins

## Common Database Issues

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | No indexes on foreign keys | Indexing Strategy | CRITICAL |
| 2 | Raw SQL without parameterization | Security | CRITICAL |
| 3 | Missing unique constraints | Data Integrity | HIGH |
| 4 | No soft delete | Schema Design | MEDIUM |
| 5 | Missing timestamps | Schema Design | MEDIUM |
| 6 | No @@index on composite queries | Indexing Strategy | HIGH |
| 7 | findMany without select | Query Performance | MEDIUM |
| 8 | No migration versioning | Migration | MEDIUM |
