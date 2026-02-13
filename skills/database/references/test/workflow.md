# Database Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| Schema Design (15%) | Schema validation | Relations correct, naming consistent |
| Data Integrity (12%) | Integration | Constraints enforced, cascades work |
| Indexing Strategy (12%) | Performance | Queries use indexes (EXPLAIN) |
| Security (15%) | Integration | RLS active, no SQL injection, field encryption |
| Query Performance (10%) | Performance | No N+1, select fields, response time |
| Migration (10%) | Integration | Migrations apply cleanly, rollback works |
| Monitoring (8%) | Unit | Slow query logged, metrics collected |
| Backup (8%) | Integration | PITR configured, restore tested |
| Scalability (5%) | Load test | Connection pool holds under load |
| Developer Experience (5%) | Unit | Types exported, helpers work correctly |

2. **Generate Test Files**:
   - `__tests__/db/schema.test.ts` — Schema validation + constraints
   - `__tests__/db/queries.test.ts` — Query performance + N+1 detection
   - `__tests__/db/security.test.ts` — SQL injection prevention
   - `__tests__/db/migrations.test.ts` — Migration apply + rollback

3. **Output** — Test files + coverage matrix
