# Step 3.2: Add Better Auth Models to Schema

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Generate Auth Models

```bash
npx @better-auth/cli generate
```

When prompted to overwrite `schema.prisma`, confirm with `y`.

## Models Added

This adds 4 models to `prisma/schema.prisma`:

| Model | Purpose |
|-------|---------|
| `User` | User accounts (id, name, email, image, timestamps) |
| `Session` | Active sessions (token, expiresAt, IP, user agent) |
| `Account` | OAuth/credential accounts (provider, tokens) |
| `Verification` | Email verification tokens |

## Generated Schema (excerpt)

> **Critical**: Models MUST include `@@map("lowercase")` annotations. Better Auth expects lowercase table names. Without `@@map`, Prisma creates PascalCase tables which causes auth failures.

```prisma
model User {
  id            String    @id
  name          String
  email         String    @unique
  emailVerified Boolean
  image         String?
  createdAt     DateTime
  updatedAt     DateTime
  sessions      Session[]
  accounts      Account[]

  @@map("user")
}

model Session {
  id        String   @id
  expiresAt DateTime
  token     String   @unique
  ipAddress String?
  userAgent String?
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("session")
}

model Account {
  id                    String    @id
  accountId             String
  providerId            String
  userId                String
  user                  User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  accessToken           String?
  refreshToken          String?
  idToken               String?
  accessTokenExpiresAt  DateTime?
  refreshTokenExpiresAt DateTime?
  scope                 String?
  password              String?
  createdAt             DateTime
  updatedAt             DateTime

  @@map("account")
}

model Verification {
  id         String    @id
  identifier String
  value      String
  expiresAt  DateTime
  createdAt  DateTime?
  updatedAt  DateTime?

  @@map("verification")
}
```

## Key Annotations

| Annotation | On | Purpose |
|------------|-----|---------|
| `@@map("user")` | All models | Lowercase table name for Better Auth |
| `@unique` | `email`, `token` | Unique constraints |
| `onDelete: Cascade` | Session, Account | Clean up on user delete |

## Next Step

Proceed to [migrate-database.md](migrate-database.md).
