# Criteria: Schema Design + Data Integrity

## Category 1: Schema Design (15%)

### Naming (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Models use PascalCase (`User`, `Purchase`), fields use camelCase (`createdAt`, `githubUsername`) |
| +1 | Table/field names are descriptive and consistent (no abbreviations like `usr`, `txn`, `amt`) |
| -1 | Mixed naming conventions across models |
| -1 | Reserved SQL keywords used as field names |

### Types & Fields (3 points)

| Score | Criteria |
|-------|---------|
| +1 | IDs use `String @id @default(cuid())` or UUID — not auto-increment Int |
| +1 | All models have `createdAt DateTime @default(now())` and `updatedAt DateTime @updatedAt` |
| +1 | Enums used for fixed value sets (`enum Role { USER ADMIN }`) |
| -1 | `String` used where `Int`, `Float`, `Boolean`, or `Enum` is more appropriate |
| -1 | Nullable fields without clear business reason (overuse of `?`) |

### Normalization & Relationships (3 points)

| Score | Criteria |
|-------|---------|
| +1 | No data duplication across tables (3NF minimum) |
| +1 | Relations defined with proper `@relation` directives and foreign keys |
| +1 | Cascade rules explicit (`onDelete: Cascade` vs `SetNull` vs `Restrict`) |
| -1 | Denormalized data without documented performance justification |
| -1 | Missing `@relation` on ambiguous foreign keys |

### Model Organization (2 points)

| Score | Criteria |
|-------|---------|
| +1 | Related models grouped together in schema file |
| +1 | Each model has a clear single responsibility |
| -1 | God model (> 20 fields) that should be split |

---

## Category 2: Data Integrity (12%)

### Constraints (4 points)

| Score | Criteria |
|-------|---------|
| +1 | `@unique` on business identifiers (email, stripePaymentId, slug) |
| +1 | `@@unique` composite constraints where needed (e.g., `[userId, productId]`) |
| +1 | `@db.VarChar(n)` length limits on string fields that face external input |
| +1 | Check constraints via `@default` or application-level Zod validation |
| -1 | No unique constraint on email field |
| -1 | Foreign keys allow orphaned records (missing cascade rules) |

### Validation Strategy (3 points)

| Score | Criteria |
|-------|---------|
| +1 | Zod schemas validate all API input before hitting database |
| +1 | Single source of truth for validation (one schema per entity in `src/lib/validations/`) |
| +1 | Validation error messages are user-friendly (not raw Prisma errors) |
| -1 | Direct Prisma calls with unvalidated user input |
| -1 | Duplicate validation logic across multiple files |

### Referential Integrity (3 points)

| Score | Criteria |
|-------|---------|
| +1 | All foreign keys reference existing primary keys |
| +1 | Delete cascades match business logic (user delete → purchase soft-delete?) |
| +1 | Idempotent operations use check-before-create pattern |
| -1 | Orphaned records possible due to missing constraints |
| -1 | Hard delete on entities that have dependent records |

## Scoring Summary

| Sub-area | Max Points |
|----------|-----------|
| Naming | 2 |
| Types & Fields | 3 |
| Normalization | 3 |
| Model Organization | 2 |
| **Schema Design Total** | **10** |
| Constraints | 4 |
| Validation Strategy | 3 |
| Referential Integrity | 3 |
| **Data Integrity Total** | **10** |
