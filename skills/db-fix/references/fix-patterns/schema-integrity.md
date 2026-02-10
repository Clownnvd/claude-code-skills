# Fix Patterns: Schema Design + Data Integrity

## String Fields → Enums

### Problem: String where enum fits
```prisma
// Before: no type safety
model Purchase {
  paymentMethod String @default("stripe")
  productType   String @default("KING_TEMPLATE")
}
```

### Fix: Create enum + migrate
```prisma
enum PaymentMethod {
  STRIPE
  SEPAY
}

enum ProductType {
  KING_TEMPLATE
}

model Purchase {
  paymentMethod PaymentMethod @default(STRIPE)
  productType   ProductType   @default(KING_TEMPLATE)
}
```

After schema change: `npx prisma migrate dev --name add_payment_enums`

### Update application code
```typescript
// Before
data: { paymentMethod: "stripe" }

// After: use generated enum
import { PaymentMethod } from "@prisma/client"
data: { paymentMethod: PaymentMethod.STRIPE }
// OR keep string literal — Prisma accepts both for enums
data: { paymentMethod: "STRIPE" }
```

## Duplicate Timestamps

### Problem: purchasedAt duplicates createdAt
```prisma
model Purchase {
  purchasedAt DateTime @default(now())  // same as createdAt?
  createdAt   DateTime @default(now())
}
```

### Options
1. **Remove `purchasedAt`** if always equals `createdAt`
2. **Keep both** if `purchasedAt` can differ (e.g., backdated imports)
3. **Document why** with schema comment if keeping both

```prisma
model Purchase {
  /// Actual payment confirmation time (may differ from createdAt for imports)
  purchasedAt DateTime @default(now())
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}
```

## Missing Schema Comments

### Add doc comments on non-obvious fields
```prisma
model Purchase {
  id                 String         @id @default(cuid())
  userId             String
  /// "STRIPE" or "SEPAY" — which payment gateway processed this
  paymentMethod      PaymentMethod  @default(STRIPE)
  /// Stripe PaymentIntent ID (pi_xxx) — null for SePay purchases
  stripePaymentId    String?        @unique
  /// Stripe Customer ID (cus_xxx) — reused across purchases
  stripeCustomerId   String?
  /// SePay transaction ID from webhook callback
  sepayTransactionId String?        @unique
  /// Unique code for SePay QR payment matching (e.g., KT-abc123)
  paymentCode        String?        @unique
  /// Amount in smallest currency unit (cents for USD, dong for VND)
  amount             Int
}
```

## Missing Composite Unique

### Problem: User can create duplicate purchases
```prisma
// No constraint preventing 2 COMPLETED purchases for same product
model Purchase {
  userId      String
  productType String
  status      PurchaseStatus
}
```

### Fix: Add composite unique (if business rule requires)
```prisma
model Purchase {
  // ... fields ...
  @@unique([userId, productType], name: "one_purchase_per_product")
}
```

**Warning**: Only add if business logic truly prevents duplicates. If refunds + re-purchase is allowed, use application-level check instead.

## ID Strategy Fixes

### Auto-increment → cuid/uuid
```prisma
// Before: leaks entity count, guessable
model User {
  id Int @id @default(autoincrement())
}

// After: globally unique, non-sequential
model User {
  id String @id @default(cuid())
}
```

**Impact**: Changes all foreign keys, all API route params, all client-side ID references. Requires full migration + data migration.

## Missing Timestamps

### Add createdAt/updatedAt to every model
```prisma
// Before
model WebhookEvent {
  id          String   @id
  type        String
  processedAt DateTime @default(now())
}

// After: add updatedAt for consistency
model WebhookEvent {
  id          String   @id
  type        String
  processedAt DateTime @default(now())
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}
```

## Nullable Without Reason

### Audit all optional fields
For each `String?`, `DateTime?`, etc. — verify there's a valid business reason:

| Field | Nullable? | Reason |
|-------|-----------|--------|
| `user.name` | Yes | OAuth may not provide name |
| `user.image` | Yes | Not all users upload avatar |
| `purchase.stripePaymentId` | Yes | SePay purchases don't have Stripe ID |
| `purchase.expiresAt` | Yes | Only SePay pending purchases expire |

If no valid reason, make field required with default value.

## Cascade Rules

### Every relation needs explicit onDelete
```prisma
// Before: implicit default (Prisma default varies)
model Session {
  user User @relation(fields: [userId], references: [id])
}

// After: explicit cascade
model Session {
  user User @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

| Relation | Recommended onDelete |
|----------|---------------------|
| Session → User | Cascade (delete sessions when user deleted) |
| Account → User | Cascade |
| Purchase → User | Cascade or Restrict (keep purchase records?) |
| EmailLog → (none) | No relation — standalone |
