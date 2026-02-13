# Data Flow Review Workflow

## Process

1. **Read** — Load target file(s), determine if server/client component, API route, or utility
2. **Classify** — Which dataflow categories apply:
   - Server component page → RSC Fetching, Composition, Prisma, Caching, Types, Errors, DTOs
   - Client component → State Management, Form Handling, Types, Error Propagation
   - API route → API Route Design, Types, Caching, Error Propagation
   - Data utility → Prisma Optimization, Caching, Types, DTOs
3. **Score** — Rate each applicable category 0-10
4. **Annotate** — Cite line numbers and issues
5. **Suggest** — Concrete fixes
6. **Summarize** — Score, priorities, quick wins

## Common Data Flow Issues

| Priority | Issue | Category | Severity |
|----------|-------|----------|----------|
| 1 | Client-side fetch when server component works | RSC Fetching | CRITICAL |
| 2 | No loading.tsx for route | Error Propagation | HIGH |
| 3 | findMany without select | Prisma Optimization | HIGH |
| 4 | Date objects passed to client | DTOs & Serialization | MEDIUM |
| 5 | Duplicated state (server + client) | State Management | MEDIUM |
| 6 | No Zod on form inputs | Form Handling | HIGH |
| 7 | Missing error.tsx | Error Propagation | HIGH |
| 8 | Types not shared from @/types/ | Type Safety | MEDIUM |
