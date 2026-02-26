# Data Flow Generate Workflow

## Process

1. **Parse Request** — Extract: component type (page, component, data loader), data source, client/server split
2. **Load Criteria** — Read all 10 dataflow scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| Server Component Fetching (15%) | Direct Prisma/DB call in server component, no client fetch |
| Server/Client Composition (10%) | Server component parent, client children only for interactivity |
| Prisma Optimization (12%) | `select` on all queries, no N+1, include only when needed |
| API Route Design (15%) | `{ success, data, error }` envelope, Zod validation, auth |
| State Management (8%) | Zustand for client state, URL state with nuqs, no duplication |
| Caching (10%) | `cache()` for dedup, revalidateTag/Path after mutations |
| Type Safety (10%) | Shared types from `@/types/`, no `any`, Zod infer for forms |
| Error Propagation (8%) | error.tsx per route, graceful fallbacks, toast on client errors |
| Form Handling (7%) | react-hook-form + Zod, loading state, field-level errors |
| DTOs & Serialization (5%) | Dates as ISO strings, no Prisma types crossing boundary |

4. **Generate** — Write server component + client component + types + loading state
5. **Self-Check** — Verify all 10 categories
6. **Output** — Code + compliance checklist

## Quality Contract

- All 10 categories addressed
- Score >= 90 (A-) if audited with dataflow scoring
- Server components for data fetching, client only for interactivity
- No Date objects crossing server/client boundary
