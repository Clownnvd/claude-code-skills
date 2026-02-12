# Eval: Data Flow Fix Patterns

Verify specific fix patterns from `references/fix-patterns/` produce correct code changes.

## Pattern 1: Convert Client Page to Server Component (rsc-composition.md)

**Setup**: Dashboard page uses `"use client"` with `useEffect` + `fetch("/api/user/purchase")` to load data. No interactivity requires client-side rendering.

**Steps**:
1. Apply RSC conversion pattern.
2. Verify `"use client"` removed from page component.
3. Verify `useEffect`/`useState` replaced with `async function` and direct Prisma query.
4. Verify interactive elements extracted to separate client components.

**Pass**: Page is an async Server Component. Data fetched via Prisma `select`. No client-side fetch for initial data. Interactive parts (buttons, forms) in separate `"use client"` files.

**Fail**: Page still has `"use client"`, or data fetching broken, or event handlers left in server component.

## Pattern 2: Add select to Prisma Queries (prisma-api.md)

**Setup**: Multiple `prisma.user.findUnique()` calls without `select`, returning all columns including sensitive fields.

**Steps**:
1. Apply "Add select" pattern.
2. Verify every `findUnique`/`findFirst`/`findMany` call has explicit `select`.
3. Verify no password hash, tokens, or internal IDs returned to client.

**Pass**: All Prisma queries use `select` with only needed fields (id, name, email, image). No `include` used where `select` suffices. Sensitive fields never selected.

**Fail**: Some queries still return full model, or `select` only added to some queries.

## Pattern 3: Shared Zod Schemas (types-errors.md)

**Setup**: Client form uses inline validation. API route uses separate inline validation. Types duplicated between client and server.

**Steps**:
1. Apply Shared Zod Schemas pattern.
2. Verify schema defined once in `src/lib/validations/`.
3. Verify client form uses `zodResolver(schema)`.
4. Verify API route uses `schema.safeParse(body)`.
5. Verify type inferred via `z.infer<typeof schema>`.

**Pass**: Single schema source of truth. Both client and server import it. No duplicate `interface` or `type` for the same data shape. `z.infer` used instead of manual types.

**Fail**: Schema still duplicated, or client/server use different validation rules.

## Pattern 4: error.tsx Per Route Segment (types-errors.md)

**Setup**: No error boundaries. Unhandled Prisma or Stripe errors crash the page with a generic Next.js error.

**Steps**:
1. Apply error.tsx pattern.
2. Verify `src/app/dashboard/error.tsx` created with `"use client"` directive.
3. Verify component accepts `error` and `reset` props.
4. Verify error digest shown (not raw message) in production.

**Pass**: Error boundary catches runtime errors in dashboard. Displays "Something went wrong" with retry button. Production shows `error.digest`, not stack trace. Non-fatal side effects wrapped in try/catch.

**Fail**: No error.tsx created, or component missing `"use client"`, or raw error message displayed.
