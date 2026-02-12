# Input Validation + Error Handling

Covers categories 3 (Input Validation, 12%) and 4 (Error Handling, 10%).

## Category 3: Input Validation (12%)

### Checklist (subtract 1 per missing item from baseline 5)

- [ ] Schema validation on ALL request bodies (Zod, JSON Schema, Joi)
- [ ] Reject requests with extraneous/unknown fields
- [ ] Content-Type enforcement (reject mismatched types)
- [ ] Format validation: email, URL, UUID, ISO 8601 dates, enums
- [ ] Semantic validation: ranges, cross-field rules, business constraints
- [ ] Parameterized queries only (no string concatenation for SQL/NoSQL)
- [ ] Query parameter validation: pagination limits, sort fields allowlisted
- [ ] Path parameter validation: type + format (no traversal `../`)

### Bonus

- [ ] Single source of truth for schemas (shared validation module)
- [ ] File upload: MIME verification, size limit, virus scan
- [ ] OpenAPI schema used as runtime validator (not just docs)

### Evidence Patterns (what to look for in code)

```typescript
// GOOD: Schema validation at route entry
const body = schema.parse(await req.json());

// BAD: No validation
const body = await req.json();
await db.create({ data: body }); // mass assignment!
```

```typescript
// GOOD: Allowlist query params
const ALLOWED_SORTS = ["createdAt", "amount"] as const;
if (!ALLOWED_SORTS.includes(sort)) return error(400);

// BAD: Pass-through
const { sort } = req.query;
await db.find({ orderBy: { [sort]: "asc" } }); // injection risk
```

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | No validation; raw req.body passed to DB; SQL injection possible |
| 4-5 | Some validation but inconsistent; some endpoints unvalidated |
| 6-7 | All bodies validated; parameterized queries; basic format checks |
| 8-9 | Shared schema module; semantic validation; query params validated |
| 10 | All above + OpenAPI runtime validation + file upload hardened |

---

## Category 4: Error Handling (10%)

### Checklist

- [ ] Consistent error envelope on ALL error responses (same structure)
- [ ] Correct HTTP status codes (400, 401, 403, 404, 409, 422, 429, 500)
- [ ] No info leakage: no stack traces, internal paths, DB errors in production
- [ ] Field-level validation errors for 400/422 (field name + message)
- [ ] Machine-readable error codes (stable strings, not just messages)
- [ ] Global error handler catches unhandled exceptions
- [ ] Error messages are actionable (tell developer how to fix)

### Bonus

- [ ] RFC 7807 Problem Details format
- [ ] Error catalog documented with all codes
- [ ] Idempotent error responses (same key = same error)

### Evidence Patterns

```typescript
// GOOD: Consistent envelope
return NextResponse.json(
  { success: false, error: "Validation failed", code: "VALIDATION_ERROR",
    details: { email: ["Must be a valid email"] } },
  { status: 400 }
);

// BAD: Inconsistent, leaks info
return NextResponse.json({ message: err.message }, { status: 500 });
// Could leak: "relation 'users' does not exist"
```

### Scoring Guide

| Score | Criteria |
|-------|----------|
| 0-3 | Raw errors exposed; inconsistent formats; wrong status codes |
| 4-5 | Some error handling but leaks info; inconsistent envelope |
| 6-7 | Consistent envelope; correct codes; no leaks; global handler |
| 8-9 | Field-level errors; machine-readable codes; actionable messages |
| 10 | All above + RFC 7807 + error catalog + idempotent errors |
