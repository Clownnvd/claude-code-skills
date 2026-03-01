# Polar Subscription Management

> Section 4 from the Polar Payment SDK Comprehensive Reference.
> Covers subscription lifecycle, creation, cancellation, updates, trials, and renewal detection.

---

## 4. Subscription Management

### 4.1 Subscription Lifecycle

```
checkout.created -> checkout.updated -> order.created (pending) -> order.paid
    -> subscription.created -> subscription.active
    -> [subscription.updated (renewals)]
    -> subscription.canceled (cancel_at_period_end: true)
    -> subscription.revoked (access actually removed)
```

**Key principle:** Do NOT revoke access on `subscription.canceled`. Wait for `subscription.revoked`.

### 4.2 Creating Subscriptions

For **paid products**: Always use checkout flows (see checkout.md sections 3.1-3.3).

For **free products** only: Direct API creation is allowed.

```typescript
const subscription = await polar.subscriptions.create({
  productId: "free_product_id",
  customerId: "customer_id",
})
// Note: No initial order or confirmation email is sent
```

### 4.3 Canceling Subscriptions

**Deferred cancellation** (cancel at period end -- recommended):
```typescript
await polar.subscriptions.update(subscriptionId, {
  cancelAtPeriodEnd: true,
})
// subscription.canceled webhook fires
// subscription.revoked fires at end of period
```

**Immediate cancellation:**
```typescript
await polar.subscriptions.delete(subscriptionId)
// subscription.canceled + subscription.revoked fire simultaneously
// Benefits automatically revoked
```

### 4.4 Updating Subscriptions

```typescript
await polar.subscriptions.update(subscriptionId, {
  // Update discount
  discountId: "discount_id",
  // OR change seat count (proration applied automatically)
  // OR update interval end date
})
```

### 4.5 Subscription Trials

Configure in Polar dashboard or at checkout time:
- Duration: days, weeks, months, or years
- Customer not charged during trial
- Automatic charge after trial ends
- Abuse prevention: email normalization + payment fingerprinting

### 4.6 Detecting Renewals

No dedicated renewal event. Detect via:
```typescript
onOrderCreated: async (payload) => {
  if (payload.data.billing_reason === "subscription_cycle") {
    // This is a renewal
  }
}
```
