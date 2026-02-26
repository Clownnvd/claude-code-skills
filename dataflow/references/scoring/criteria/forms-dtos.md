# Criteria: Form Handling (7%) + Data Transformation / DTOs (5%)

## 9. Form Handling (7%)

### Score 9-10: Enterprise-grade
- Server Actions for form submissions (or API routes with full pipeline)
- `useActionState` for submission state tracking
- Progressive enhancement (forms work without JS)
- Zod validation in server action/route handler
- `useOptimistic` for instant UI feedback
- `useFormStatus` for loading states
- CSRF handled (automatic via Server Actions or explicit via `verifyCsrf`)
- Field-level error display from Zod validation

### Score 7-8: Production-ready
- Validation on both client and server
- Loading states during submission
- Field-level error display
- CSRF protection present
- Forms use react-hook-form with zodResolver (client) + Zod on server

### Score 5-6: Minimum
- Some validation (client or server, not both)
- Loading states present but ad-hoc
- Generic error display
- Forms require JavaScript

### Score 3-4: Below minimum
- `onSubmit` + `preventDefault` + `fetch` with no validation
- No loading states or error display
- Client-only validation (bypassable)
- No CSRF protection

### Checklist
- [ ] Validation on both client and server
- [ ] Loading states during form submission
- [ ] Field-level error display
- [ ] CSRF protection (Server Actions or explicit)
- [ ] Zod schema shared between client and server
- [ ] Accessible form markup (labels, aria attributes)

### Scoring Note
For apps using API routes (not Server Actions), full marks still achievable with:
- react-hook-form + zodResolver on client
- Zod `.safeParse()` on server route
- CSRF via `verifyCsrf()`
- Loading states via `useState` or `useTransition`

## 10. Data Transformation / DTOs (5%)

### Score 9-10: Enterprise-grade
- Clear separation: Prisma model → Service layer → DTO → API response
- DTOs strip sensitive/internal fields before crossing boundaries
- Transformation functions are pure (no side effects)
- Zod schemas define DTO shape
- Database models never leak directly to client
- Consistent naming conventions (`avatarUrl` not `image`)
- Null handling explicit and documented

### Score 7-8: Production-ready
- `select` in Prisma acts as implicit DTO (acceptable)
- Internal fields filtered before response
- Date serialization consistent (`.toISOString()`)
- Some explicit field renaming/transformation

### Score 5-6: Minimum
- Some transformation but inconsistent
- Some routes return raw Prisma objects
- Date serialization handled most of the time
- `select` used sometimes

### Score 3-4: Below minimum
- Raw Prisma objects returned from API routes
- Internal fields (userId, stripeCustomerId) exposed to client
- Dates as Date objects (serialization issues)
- No consistent transformation pattern

### Checklist
- [ ] `select` on Prisma queries (implicit DTO)
- [ ] Date fields serialized with `.toISOString()`
- [ ] Internal/sensitive fields stripped from responses
- [ ] Consistent field naming across API responses
- [ ] No raw Prisma types in client-side code
