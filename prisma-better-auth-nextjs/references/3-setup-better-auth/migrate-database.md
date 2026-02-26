# Step 3.3: Migrate the Database

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Run Migration

```bash
npx prisma migrate dev --name add-auth-models
```

This creates the tables in your PostgreSQL database matching the schema.

## Regenerate Client

```bash
npx prisma generate
```

Re-generate after migration to get updated types for the new auth models.

## Verify

Open Prisma Studio to inspect the created tables:

```bash
npx prisma studio
```

## Tables Created

| Table | Columns |
|-------|---------|
| `User` | id, name, email, emailVerified, image, createdAt, updatedAt |
| `Session` | id, expiresAt, token, ipAddress, userAgent, userId |
| `Account` | id, accountId, providerId, userId, tokens, password, timestamps |
| `Verification` | id, identifier, value, expiresAt, timestamps |

## Next Step

Proceed to [4-api-routes/setup-routes.md](../4-api-routes/setup-routes.md).
