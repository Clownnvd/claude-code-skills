# Database Sync — Stripe ↔ DB

Keep your database in sync with Stripe via webhooks (source of truth: Stripe).

## Schema (Prisma example)

```prisma
model User {
  id                  String  @id @default(cuid())
  email               String  @unique
  stripeCustomerId    String? @unique
  stripeSubscriptionId String?
  stripePriceId       String?
  stripeCurrentPeriodEnd DateTime?
  plan                String  @default("free") // free | pro | enterprise
}
```

## Webhook → DB Sync Handlers

```typescript
// In your webhook handler (app/api/webhooks/stripe/route.ts)
import { db } from "@/lib/db";

async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId;
  if (!userId) return;

  if (session.mode === "subscription") {
    const subscription = await stripe.subscriptions.retrieve(
      session.subscription as string
    );
    await db.user.update({
      where: { id: userId },
      data: {
        stripeCustomerId: session.customer as string,
        stripeSubscriptionId: subscription.id,
        stripePriceId: subscription.items.data[0]?.price.id,
        stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
        plan: mapPriceToPlan(subscription.items.data[0]?.price.id),
      },
    });
  }
}

async function handleSubscriptionChange(subscription: Stripe.Subscription) {
  await db.user.updateMany({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      stripePriceId: subscription.items.data[0]?.price.id,
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
      plan: mapPriceToPlan(subscription.items.data[0]?.price.id),
    },
  });
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  await db.user.updateMany({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      stripeSubscriptionId: null,
      stripePriceId: null,
      stripeCurrentPeriodEnd: null,
      plan: "free",
    },
  });
}

async function handleInvoicePaid(invoice: Stripe.Invoice) {
  const subscriptionId = invoice.subscription as string | null;
  if (!subscriptionId) return;

  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  await db.user.updateMany({
    where: { stripeSubscriptionId: subscriptionId },
    data: {
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  });
}
```

## Price → Plan Mapping

```typescript
const PRICE_TO_PLAN: Record<string, string> = {
  "price_abc123": "pro",
  "price_def456": "enterprise",
  // Add your price IDs from Stripe Dashboard
};

function mapPriceToPlan(priceId?: string): string {
  if (!priceId) return "free";
  return PRICE_TO_PLAN[priceId] ?? "free";
}
```

## Helper: Get or Create Stripe Customer

```typescript
export async function getOrCreateStripeCustomer(userId: string) {
  const user = await db.user.findUniqueOrThrow({ where: { id: userId } });

  if (user.stripeCustomerId) return user.stripeCustomerId;

  const customer = await stripe.customers.create({
    email: user.email,
    metadata: { userId: user.id },
  });

  await db.user.update({
    where: { id: userId },
    data: { stripeCustomerId: customer.id },
  });

  return customer.id;
}
```

## Check Subscription Status

```typescript
export async function hasActiveSubscription(userId: string): Promise<boolean> {
  const user = await db.user.findUnique({ where: { id: userId } });
  if (!user?.stripeCurrentPeriodEnd) return false;
  return user.stripeCurrentPeriodEnd > new Date();
}

export async function getUserPlan(userId: string): string {
  const user = await db.user.findUnique({ where: { id: userId } });
  return user?.plan ?? "free";
}
```

## Key Points
- Stripe is the source of truth — sync TO your DB via webhooks
- Never rely solely on client-side session checks for access control
- Always map Stripe price IDs to your plan names server-side
- Use `updateMany` with `stripeSubscriptionId` (works even if userId not in webhook)
- Handle `customer.subscription.deleted` to downgrade to free
- Store `stripeCurrentPeriodEnd` for quick access checks without API calls
