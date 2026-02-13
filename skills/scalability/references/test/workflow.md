# Scalability Test Generation Workflow

## Process

1. **Map Categories to Test Types**:

| Category | Test Type | What to Assert |
|----------|----------|---------------|
| Bundle Size (15%) | Build analysis | Chunk sizes under budget, no barrel imports |
| Image Optimization (12%) | Component | next/image used, responsive sizes, lazy loading |
| RSC Architecture (12%) | Component | Server components for data, minimal client |
| DB Query Performance (12%) | Performance | No N+1, queries use indexes, select fields |
| API Response Perf (10%) | Integration | Response size, pagination, response time |
| Client Perf (10%) | Component | Re-render count, no layout thrash |
| Edge/CDN (8%) | Build/Integration | Static pages generated, CDN headers correct |
| Memory Management (8%) | Integration | No leaks after N iterations, cleanup called |
| Concurrent Processing (7%) | Unit | Promise.all used, no sequential awaits |
| Performance Monitoring (6%) | Integration | Web Vitals reported, budgets enforced |

2. **Generate Test Files**:
   - `__tests__/perf/bundle.test.ts` — Bundle size analysis
   - `__tests__/perf/queries.test.ts` — Query performance
   - `__tests__/perf/rendering.test.tsx` — Component render performance
   - `__tests__/perf/memory.test.ts` — Memory leak detection

3. **Output** — Test files + coverage matrix
