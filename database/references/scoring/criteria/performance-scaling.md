# Criteria: Indexing + Query Performance + Scalability

## Category 3: Indexing Strategy (12%)

### Index Coverage (4 points)

| Score | Criteria |
|-------|---------|
| +1 | All foreign keys have indexes (`@@index([userId])`) |
| +1 | Fields used in `WHERE` clauses have indexes |
| +1 | Fields used in `ORDER BY` have indexes |
| +1 | Composite indexes match query patterns (`@@index([userId, createdAt])`) |
| -1 | Foreign key without index (full table scan on JOIN) |
| -1 | Frequently filtered field without index |

### Index Quality (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Unique indexes on business identifiers (`@@unique([email])`) |
| +1 | Composite index column order matches query selectivity (most selective first) |
| +1 | No redundant indexes (single-column index that's prefix of composite) |
| -1 | Index on low-cardinality column (boolean, enum with 2 values) |
| -1 | Too many indexes on write-heavy tables (> 5 indexes) |

### Index Monitoring (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Unused indexes identified and removed |
| +1 | Index size monitored (not growing unbounded) |
| +1 | `EXPLAIN ANALYZE` used to verify index usage on critical queries |
| -1 | Indexes created but never verified to be used |

---

## Category 5: Query Performance (10%)

### N+1 Prevention (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Relations loaded with `include` in single query, not loop |
| +1 | No `findMany` inside `map`/`forEach` (N+1 pattern) |
| +1 | Batch operations used (`createMany`, `updateMany`) where applicable |
| -1 | N+1 query pattern detected in API routes |

### Select Optimization (3 points)

| Score | Criteria |
|-------|---------|
| +1 | `select` used to fetch only needed columns |
| +1 | `include` depth limited (no 3+ level deep includes) |
| +1 | Large text/blob fields excluded from list queries |
| -1 | Full model fetched when only 2-3 fields needed |

### Transaction Usage (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Multi-step writes wrapped in `$transaction` |
| +1 | Transaction scope minimal (no external API calls inside transaction) |
| -1 | Related writes without transaction (partial failure possible) |

### Pagination (2 points)

| Score | Criteria |
|-------|---------|
| +1 | List endpoints use `take`/`skip` or cursor-based pagination |
| +1 | Default limit set (never returns unbounded results) |
| -1 | `findMany()` without `take` limit on user-facing endpoints |

---

## Category 9: Scalability (5%)

### Connection Management (4 points)

| Score | Criteria |
|-------|---------|
| +1 | Connection pooling configured (PgBouncer, Prisma pool, Neon pooler) |
| +1 | Pool size appropriate for deployment (serverless: 1-5, server: 10-20) |
| +1 | Idle connection timeout configured |
| +1 | Separate pooled URL (for queries) and direct URL (for migrations) |
| -1 | No connection pooling on serverless deployment |
| -1 | Pool size set to maximum without justification |

### Growth Readiness (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Read-heavy tables identified for future read replicas |
| +1 | Large tables have partition strategy documented |
| +1 | Caching layer for frequently-read, rarely-changed data |

### Edge/Serverless Compatibility (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Database driver compatible with edge runtime (if using Vercel Edge) |
| +1 | Cold start impact considered (connection pre-warming) |
| +1 | Stateless queries (no session-level state held across requests) |

## Scoring Summary

| Sub-area | Max Points |
|----------|-----------|
| Index Coverage | 4 |
| Index Quality | 3 |
| Index Monitoring | 3 |
| **Indexing Total** | **10** |
| N+1 Prevention | 3 |
| Select Optimization | 3 |
| Transaction Usage | 2 |
| Pagination | 2 |
| **Query Performance Total** | **10** |
| Connection Management | 4 |
| Growth Readiness | 3 |
| Edge Compatibility | 3 |
| **Scalability Total** | **10** |
