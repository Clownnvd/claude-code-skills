# Fix Patterns: Subscription Lifecycle + Metered/Usage Billing

## Missing Cancel Handling

### Before: Only immediate cancel
```typescript
export async function POST(request: Request) {
  const { subscriptionId } = await request.json()
  await stripe.subscriptions.cancel(subscriptionId) // user loses remaining time
  return NextResponse.json({ success: true })
}
```

### After: Both immediate and end-of-period
```typescript
export async function POST(request: Request) {
  try {
    const { subscriptionId, cancelImmediately = false } = await request.json()
    const session = await auth.api.getSession({ headers: request.headers })
    if (!session?.user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })

    const subscription = cancelImmediately
      ? await stripe.subscriptions.cancel(subscriptionId)
      : await stripe.subscriptions.update(subscriptionId, { cancel_at_period_end: true })

    await prisma.subscription.update({
      where: { stripeSubscriptionId: subscriptionId },
      data: {
        status: subscription.status,
        cancelAtPeriodEnd: subscription.cancel_at_period_end,
        canceledAt: subscription.canceled_at ? new Date(subscription.canceled_at * 1000) : null,
      },
    })
    return NextResponse.json({ subscription })
  } catch (error) {
    console.error("Cancel error:", error)
    return NextResponse.json({ error: "Failed to cancel" }, { status: 500 })
  }
}
```

## No Proration Config

### Before
```typescript
await stripe.subscriptions.update(subId, {
  items: [{ id: itemId, price: newPriceId }], // no proration
})
```

### After
```typescript
await stripe.subscriptions.update(subId, {
  items: [{ id: itemId, price: newPriceId }],
  proration_behavior: "create_prorations",
  payment_behavior: "default_incomplete",
})
```

## Missing Subscription Status Checks

### Before
```typescript
export async function checkAccess(userId: string) {
  const sub = await prisma.subscription.findFirst({ where: { userId } })
  return !!sub // canceled/past_due subs still grant access
}
```

### After
```typescript
export async function checkAccess(userId: string): Promise<boolean> {
  const sub = await prisma.subscription.findFirst({
    where: { userId, status: { in: ["active", "trialing"] } },
    select: { id: true, status: true, currentPeriodEnd: true },
  })
  if (!sub) return false
  if (sub.currentPeriodEnd && sub.currentPeriodEnd < new Date()) return false
  return true
}
```

## Webhook Subscription Status Sync

### Before: No webhook handler, database stale

### After
```typescript
async function handleSubscriptionUpdated(subscription: Stripe.Subscription) {
  const userId = subscription.metadata.userId
  if (!userId) { console.error("No userId in metadata:", subscription.id); return }

  await prisma.subscription.upsert({
    where: { stripeSubscriptionId: subscription.id },
    update: {
      status: subscription.status,
      currentPeriodStart: new Date(subscription.current_period_start * 1000),
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
      cancelAtPeriodEnd: subscription.cancel_at_period_end,
      priceId: subscription.items.data[0]?.price.id,
    },
    create: {
      userId,
      stripeSubscriptionId: subscription.id,
      stripeCustomerId: subscription.customer as string,
      status: subscription.status,
      priceId: subscription.items.data[0]?.price.id,
      currentPeriodStart: new Date(subscription.current_period_start * 1000),
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  })
}
```

## Missing Usage Reporting

### After
```typescript
export async function reportUsage(subscriptionItemId: string, quantity: number) {
  try {
    return await stripe.subscriptionItems.createUsageRecord(
      subscriptionItemId,
      { quantity, timestamp: Math.floor(Date.now() / 1000), action: "increment" },
      { idempotencyKey: `usage_${subscriptionItemId}_${Date.now()}` }
    )
  } catch (error) {
    console.error("Usage reporting error:", error)
    throw error
  }
}
```
