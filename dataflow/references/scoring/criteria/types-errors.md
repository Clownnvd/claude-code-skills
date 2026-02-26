# Criteria: Type Safety Across Boundaries (10%) + Error Propagation (8%)

## 7. Type Safety Across Boundaries (10%)

### Score 9-10: Enterprise-grade
- Zod schemas as single source of truth for validation + types
- `z.infer<typeof schema>` for all derived types
- Shared schemas in `validations/` directory (imported by client and server)
- `ApiResponse<T>` generic typed precisely per endpoint
- No `any` types in data flow code
- Prisma types in service layer, DTOs at API boundary
- Same validation schema on client and server (progressive enhancement)

### Score 7-8: Production-ready
- Zod used for server validation
- `ApiResponse<T>` exists and used consistently
- Most schemas shared between client and server
- Minimal `any` usage

### Score 5-6: Minimum
- Zod on server, types manually duplicated on client
- `ApiResponse<T>` sometimes typed, sometimes `unknown`
- Some inline schemas in route handlers
- Occasional Prisma type leaks to client

### Score 3-4: Below minimum
- No runtime validation (only TypeScript interfaces)
- `any` in API response handling
- Types duplicated and diverging
- `as SomeType` casts without validation
- No shared type system

### Checklist
- [ ] `z.infer<typeof schema>` for type derivation
- [ ] Schemas in `validations/` directory (shared)
- [ ] `ApiResponse<T>` used consistently
- [ ] No `any` in data flow code
- [ ] Same schema on client and server
- [ ] Prisma types don't leak to client

## 8. Error Propagation (8%)

### Score 9-10: Enterprise-grade
- `error.tsx` at appropriate route segments (not just root)
- `global-error.tsx` as ultimate fallback
- Error messages sanitized in production (no stack traces)
- External API errors wrapped with user-friendly messages
- `not-found.tsx` + `notFound()` for missing resources
- `reset` function offered in error boundaries
- Non-fatal errors handled gracefully (side effects don't crash main flow)
- Machine-readable error codes for programmatic handling

### Score 7-8: Production-ready
- Root-level `error.tsx` exists
- `global-error.tsx` present
- External errors don't leak internal details
- `not-found.tsx` exists

### Score 5-6: Minimum
- Root `error.tsx` exists but no segment-level boundaries
- Some external error wrapping
- `not-found.tsx` exists but `notFound()` not used consistently

### Score 3-4: Below minimum
- No `error.tsx` files
- External API errors leak raw messages
- `console.error` is the only error handling
- Side effect failures crash main operations
- Silent `catch {}` blocks

### Checklist
- [ ] `error.tsx` at route segments (dashboard, auth, etc.)
- [ ] `global-error.tsx` present
- [ ] External errors wrapped (Stripe, GitHub)
- [ ] `not-found.tsx` + `notFound()` used
- [ ] Non-fatal errors don't crash main flow
- [ ] No stack traces or internal details in production responses
- [ ] Machine-readable error codes in API responses
