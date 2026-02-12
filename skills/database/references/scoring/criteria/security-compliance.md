# Criteria: Security + Compliance

## Category 4: Security (15%)

### Connection Security (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Connection string uses SSL (`?sslmode=require`) |
| +1 | Connection string in env var, NOT hardcoded in schema or config |
| -1 | `DATABASE_URL` contains plaintext credentials in committed files |
| -1 | SSL disabled or not enforced |

### Access Control (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Database user has minimum required privileges (not superuser) |
| +1 | Different credentials per environment (dev/staging/production) |
| +1 | Row-Level Security (RLS) or application-level auth checks on every query |
| -1 | Single database user with full access across all environments |
| -1 | API routes query database without verifying user session |

### Secrets Management (2 points)

| Score | Criteria |
|-------|---------|
| +1 | `.env` in `.gitignore`, `.env.example` committed with placeholder values |
| +1 | Env vars validated at startup with Zod (`z.string().min(1)`) |
| -1 | Real credentials in `.env.example` or committed `.env` |
| -1 | No validation — app starts with empty `DATABASE_URL` and crashes later |

### Query Safety (2 points)

| Score | Criteria |
|-------|---------|
| +1 | All queries use parameterized ORM methods (no string interpolation) |
| +1 | Raw SQL (if any) uses `$queryRaw` with tagged templates, never `$queryRawUnsafe` |
| -1 | User input interpolated into query strings (SQL injection risk) |
| -1 | `$queryRawUnsafe` used with external input |

### Data Protection (1 point)

| Score | Criteria |
|-------|---------|
| +1 | Sensitive fields (password hash, tokens) never returned in API responses |
| -1 | `select: *` or full model returned including password hash |

---

## Compliance Considerations (bonus, not scored separately)

These don't have their own category but affect Security score:

### GDPR / Data Privacy
| Check | Description |
|-------|------------|
| Soft delete | User deletion marks as `deletedAt` rather than hard delete (data retention) |
| Data export | Ability to export user's data on request |
| Consent tracking | `consentedAt` timestamp if collecting personal data |
| Retention policy | Old data automatically purged after defined period |

### Audit Trail
| Check | Description |
|-------|------------|
| Who changed what | `updatedBy` field or separate audit log table |
| When it changed | `updatedAt` with `@updatedAt` directive |
| What changed | Before/after values logged for sensitive operations |

### PCI Compliance (if handling payments)
| Check | Description |
|-------|------------|
| No card data | Credit card numbers NEVER stored in your database |
| Stripe/provider IDs | Store only `stripeCustomerId`, `stripePaymentId` — not card details |
| Payment amount validation | Server-side amount check before granting access |

## Scoring Summary

| Sub-area | Max Points |
|----------|-----------|
| Connection Security | 2 |
| Access Control | 3 |
| Secrets Management | 2 |
| Query Safety | 2 |
| Data Protection | 1 |
| **Security Total** | **10** |
