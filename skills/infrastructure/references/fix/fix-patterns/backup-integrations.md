# Fix Patterns: Backup/DR + Third-Party Integrations

## Backup & Disaster Recovery Fixes

### Neon PostgreSQL Backup (Provider-Managed)

Neon provides:
- **Point-in-time recovery**: Built-in via branching
- **Daily backups**: Included in plan
- **Branch for testing**: Create branch to test restore

Document in `docs/runbooks/backup.md`:
```markdown
## Backup Strategy

### Provider: Neon PostgreSQL
- Automatic daily backups (provider-managed)
- Point-in-time recovery via Neon branching
- Region: ap-southeast-1

### Restore Procedure
1. Go to Neon Console > Project > Branches
2. Create branch from specific timestamp
3. Update DATABASE_URL to branch endpoint
4. Verify data integrity
5. Promote branch to main (or migrate data)

### RTO/RPO
- RPO: ~1 hour (Neon continuous backup)
- RTO: ~15 minutes (branch creation + env update)
```

### Migration Strategy

```bash
# Prisma migrations are version-controlled
prisma/migrations/
  20260118095132_baseline/migration.sql
  20260208180000_add_enums_indexes_columns/migration.sql
```

Ensure:
- All migrations in git
- `prisma db seed` works for fresh environments
- Migration rollback documented (manual SQL if needed)

### Seed Script

```typescript
// prisma/seed.ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  // Create test data for development
  await prisma.user.upsert({
    where: { email: "test@example.com" },
    update: {},
    create: {
      email: "test@example.com",
      name: "Test User",
      // ... minimal required fields
    },
  });
}

main()
  .then(() => prisma.$disconnect())
  .catch((e) => {
    console.error(e);
    prisma.$disconnect();
    process.exit(1);
  });
```

---

## Third-Party Integration Fixes

### Timeout on External Calls

```typescript
// Pattern: withTimeout wrapper
async function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  return Promise.race([
    promise,
    new Promise<never>((_, reject) =>
      setTimeout(
        () => reject(new Error(`Operation timed out after ${ms}ms`)),
        ms
      )
    ),
  ]);
}

// Usage with Stripe
const session = await withTimeout(
  stripe.checkout.sessions.create({ ... }),
  10_000
);

// Usage with GitHub API
const response = await withTimeout(
  fetch("https://api.github.com/...", { headers }),
  10_000
);

// Usage with Resend
const { data } = await withTimeout(
  resend.emails.send({ ... }),
  10_000
);
```

### Webhook Signature Verification

```typescript
// Stripe webhook
import Stripe from "stripe";

const event = stripe.webhooks.constructEvent(
  body,
  signature,
  process.env.STRIPE_WEBHOOK_SECRET
);
// Throws if signature invalid — handle in catch
```

### Webhook Idempotency

```typescript
// Check-before-create pattern
const existing = await prisma.purchase.findUnique({
  where: { stripePaymentId: paymentIntentId },
});

if (existing) {
  // Already processed — return success (idempotent)
  return NextResponse.json({ received: true });
}

// Process for first time
await prisma.purchase.create({ ... });
```

### Graceful Degradation

```typescript
// Non-fatal side effect pattern
try {
  await inviteToGitHub(username);
} catch (error) {
  // Log but don't fail the main operation
  logger.error("GitHub invite failed (non-fatal)", {
    username,
    error: error instanceof Error ? error.message : "Unknown",
  });
}
```

### Error Logging for Integrations

```typescript
// Always log integration failures with context
try {
  await externalApiCall();
} catch (error) {
  logger.error("Integration failure", {
    service: "stripe",
    operation: "create_checkout",
    error: error instanceof Error ? error.message : "Unknown",
    // Never log full error object (may contain secrets)
  });
  throw new Error("Payment service unavailable");
}
```
