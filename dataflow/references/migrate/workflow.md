# Data Flow Migrate Workflow

## Process

1. **Detect Versions** — Identify Next.js, React, Prisma, TanStack Query versions
2. **Map Breaking Changes**:

| From → To | Category Affected | Breaking Change | Migration Action |
|-----------|------------------|-----------------|-----------------|
| Next.js 14 → 15 | RSC Fetching | Async request APIs | Update params/cookies/headers access |
| Next.js 15 → 16 | RSC Fetching | dynamicIO default | Add "use cache" or explicit dynamic |
| Next.js 15 → 16 | Caching | fetch() no longer cached by default | Add explicit cache directives |
| React 18 → 19 | Composition | `use()` hook for promises | Migrate Suspense patterns |
| Prisma 6 → 7 | Prisma Optimization | Query engine changes | Test query performance |
| TanStack Query v4 → v5 | State Management | API changes | Update hook signatures |

3. **Apply Migrations** — Preserve data flow patterns during upgrade
4. **Verify** — TypeScript check, test data flow end-to-end
5. **Re-score** — Ensure no regression

## Safety Rules

- Never convert server components to client during migration
- Preserve loading.tsx and error.tsx during route changes
- Test Prisma queries after any ORM version change
- Verify serialization still works (no Date object leaks)
