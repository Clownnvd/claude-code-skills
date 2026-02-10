# Security Fix — Best Practices

## Fix Discipline

### DO
- Fix one category at a time, verify, then move on
- Read the file before editing
- Run typecheck after every batch
- Test webhook changes with actual webhook test
- Keep error response format backward-compatible
- Document why a CSP directive was added

### DON'T
- Don't fix everything in one giant commit
- Don't change error format without updating tests
- Don't add CSP directives blindly (test page rendering)
- Don't remove `console.error` without adding structured logging
- Don't tighten redirect validation without testing auth flow
- Don't update dependencies without running full test suite

## Common Mistakes

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| CSP too strict | Page won't load | Test each directive in browser |
| Missing Zod type export | TypeScript errors | Always export: `type X = z.infer<typeof xSchema>` |
| Error format change | Client code breaks | Keep same response shape |
| Redirect validation blocks auth | Users can't log in | Test OAuth callback flows |
| Remove console.error | Silent failures | Replace with structured logger first |

## Framework-Specific Notes

### Next.js App Router
- CSP goes in middleware (not next.config.js headers)
- `poweredByHeader: false` in next.config.js
- Server Components can't leak client secrets by design
- Use `headers()` from next/headers for request inspection

### Prisma
- Parameterized queries are default (no SQL injection)
- Use `select` to prevent over-fetching fields
- Never use `$queryRawUnsafe` with user input

### Better Auth
- Handles password hashing internally
- Session management is built-in
- Rate limiting config in auth options
- CSRF covered by auth-scoring, not here

## When to Stop

- Score >= 97 (A+): Enterprise-grade, stop
- Score >= 93 (A): Excellent, stop unless enterprise requirement
- Score >= 90 (A-): Good, remaining items likely LOW severity
- Remaining items are infrastructure (CI, alerting) not code
