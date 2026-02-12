# Criteria: Prisma Query Optimization (12%) + API Route Design (15%)

## 3. Prisma Query Optimization (12%)

### Score 9-10: Enterprise-grade
- `select` on every query (no `SELECT *`)
- `findUnique` for unique fields (not `findFirst`)
- `@@index` on all frequently queried non-PK fields
- `$transaction` for atomic multi-step writes
- Singleton PrismaClient (globalThis pattern)
- Connection pooling configured (Neon adapter, PgBouncer)
- Statement timeout configured
- Slow query logging/monitoring
- No N+1 queries (use `include` for relations)

### Score 7-8: Production-ready
- `select` used on most queries
- Singleton client with connection pooling
- Indexes on key lookup fields
- No obvious N+1 patterns

### Score 5-6: Minimum
- Some `select` usage, some bare queries
- `findFirst` on unique columns
- Indexes on PKs and FKs only
- No explicit connection pooling config

### Score 3-4: Below minimum
- No `select` — all queries return all columns
- Sequential queries in loops (N+1)
- Multiple PrismaClient instances
- No statement timeouts
- No indexes beyond PKs

### Checklist
- [ ] `select` on every Prisma query
- [ ] `findUnique` for unique field lookups
- [ ] `@@index` on lookup fields in schema
- [ ] `$transaction` for atomic writes
- [ ] Singleton PrismaClient with globalThis
- [ ] Connection pooling (Neon adapter or similar)
- [ ] Statement timeout configured
- [ ] Slow query logging in place

## 4. API Route Design (15%)

### Score 9-10: Enterprise-grade
- Consistent response envelope: `{ success, data, error, code }`
- Zod validation on every input-accepting endpoint
- Auth check first (fail fast pattern)
- Rate limiting on all endpoints (strict on mutations)
- CSRF protection on state-changing endpoints
- Content-Type validation before JSON parsing
- Machine-readable error codes (`ErrorCodes` enum)
- Request logging with timing
- Proper HTTP status codes (400, 401, 403, 409, 429, 500)
- Service layer separation (no Prisma in route handlers)
- JSDoc documenting auth, rate limits, purpose

### Score 7-8: Production-ready
- Response envelope consistent across most routes
- Validation on all mutation endpoints
- Auth + rate limiting present
- Service layer for complex logic

### Score 5-6: Minimum
- Some validation, inconsistent response shapes
- Auth checks present but not always first
- Rate limiting on some routes
- Business logic mixed in route handlers

### Score 3-4: Below minimum
- No input validation
- Inconsistent response shapes
- No rate limiting or CSRF
- `try/catch` with generic 500 errors
- Business logic directly in route handler

### Checklist
- [ ] Consistent `{ success, data, error, code }` response envelope
- [ ] Zod `.safeParse()` on all inputs
- [ ] Auth check as first step in protected routes
- [ ] Rate limiting on all endpoints
- [ ] CSRF on POST/PATCH/DELETE
- [ ] Content-Type validation
- [ ] Service layer separation
- [ ] Machine-readable error codes
- [ ] Request logging with timing
