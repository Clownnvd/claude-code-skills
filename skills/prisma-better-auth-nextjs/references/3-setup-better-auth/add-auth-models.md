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

```prisma
model User {
  id            String    @id
  name          String
  email         String
  emailVerified Boolean
  image         String?
  createdAt     DateTime
  updatedAt     DateTime
  sessions      Session[]
  accounts      Account[]
}

model Session {
  id        String   @id
  expiresAt DateTime
  token     String   @unique
  ipAddress String?
  userAgent String?
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
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
}

model Verification {
  id         String    @id
  identifier String
  value      String
  expiresAt  DateTime
  createdAt  DateTime?
  updatedAt  DateTime?
}
```

## Next Step

Proceed to [migrate-database.md](migrate-database.md).
