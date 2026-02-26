# Caching Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| Cache-Control Headers (15%) | Integration | Correct headers on auth vs public responses |
| Revalidation Strategy (15%) | Integration | Cache cleared after mutation |
| Static/Dynamic (12%) | Build test | Correct classification in build output |
| React cache() (10%) | Unit | Same result for same args in same request |
| "use cache" (10%) | Integration | Component/function cached correctly |
| Cache Monitoring (8%) | Unit | HIT/MISS logged correctly |
| CDN & Edge (8%) | Integration | Vary headers present, CDN-safe responses |
| ISR (8%) | Integration | Page revalidates on schedule |
| Request Dedup (7%) | Unit | Single execution for duplicate calls |
| Proxy (7%) | Integration | Static assets bypass auth, auth routes checked |

2. **Generate Test Files**:
   - `__tests__/cache/headers.test.ts` — Cache-Control header tests
   - `__tests__/cache/revalidation.test.ts` — Mutation → revalidation tests
   - `__tests__/cache/static-dynamic.test.ts` — Build classification tests

3. **Output** — Test files + coverage matrix
