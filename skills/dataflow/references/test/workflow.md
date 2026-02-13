# Data Flow Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| RSC Fetching (15%) | Integration | Data loads server-side, no client fetch |
| Composition (10%) | Component | Server parent renders, client child interactive |
| Prisma Optimization (12%) | Unit | select used, no N+1, correct includes |
| API Route Design (15%) | Integration | Envelope shape, validation, auth, status codes |
| State Management (8%) | Component | State updates correctly, URL sync works |
| Caching (10%) | Integration | Cache hit/miss, revalidation after mutation |
| Type Safety (10%) | Static | No any types, shared types used |
| Error Propagation (8%) | Integration | error.tsx renders, toast on client error |
| Form Handling (7%) | Component | Validation works, loading state shows, errors display |
| DTOs (5%) | Unit | Dates serialized, no Prisma types in response |

2. **Generate Test Files**:
   - `__tests__/dataflow/server-fetch.test.tsx` — RSC data loading
   - `__tests__/dataflow/api-routes.test.ts` — API response shapes
   - `__tests__/dataflow/forms.test.tsx` — Form validation + submission
   - `__tests__/dataflow/serialization.test.ts` — DTO serialization

3. **Output** — Test files + coverage matrix
