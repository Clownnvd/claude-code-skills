# Database Generate Workflow

## Process

1. **Parse Request** — Extract: entity names, relationships, business rules, constraints
2. **Load Criteria** — Read all 10 database scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| Schema Design (15%) | Normalized tables, proper relations, naming conventions |
| Data Integrity (12%) | Unique constraints, check constraints, NOT NULL, cascades |
| Indexing Strategy (12%) | Indexes on FKs, query fields, composite indexes |
| Security (15%) | RLS policies, field encryption, no raw SQL exposure |
| Query Performance (10%) | Select fields, no N+1, connection pooling |
| Migration & Versioning (10%) | Migration file, seed data, rollback plan |
| Monitoring (8%) | Query logging, slow query detection |
| Backup & Recovery (8%) | PITR config, backup schedule notes |
| Scalability (5%) | Partition strategy, read replicas notes |
| Developer Experience (5%) | Clear naming, type exports, helper functions |

4. **Generate** — Write Prisma schema + migration + seed + query helpers
5. **Self-Check** — Verify all 10 categories
6. **Output** — Code + compliance checklist

## Code Structure

```prisma
// Schema with all quality patterns
model Entity {
  id        String   @id @default(cuid())
  // ... fields with constraints
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  deletedAt DateTime? // soft delete

  @@index([foreignKey, createdAt(sort: Desc)])
  @@index([status, category])
}
```

## Quality Contract

- All 10 categories addressed
- Score >= 90 (A-) if audited with database scoring
- Indexes on all foreign keys and common query fields
- Soft delete pattern, timestamps on all models
