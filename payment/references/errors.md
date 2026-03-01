# Polar Errors and Fixes Database

> Section 12 from the Polar Payment SDK Comprehensive Reference.
> 25 documented errors organized by severity: CRITICAL, HIGH, MEDIUM, LOW.

---

## 12. Errors and Fixes Database

### CRITICAL

#### POL-001: Production Token Used in Sandbox (401)
```
Error: invalid_token
Status: 401 Unauthorized
```
**Cause:** Using production access token with `server: "sandbox"` or vice versa.
**Fix:** Create a separate sandbox token at `https://sandbox.polar.sh/dashboard/{org-slug}/settings#developers`. Tokens are environment-specific.

#### POL-002: Webhook Signature Verification Failed (403)
```
WebhookVerificationError: Invalid signature
```
**Cause:** Wrong `POLAR_WEBHOOK_SECRET`, or request body was parsed/modified before verification.
**Fix:**
1. Verify the secret matches what Polar dashboard shows
2. Ensure the raw body reaches the verifier (no JSON.parse before validation)
3. The `@polar-sh/nextjs` `Webhooks()` handler handles this automatically
4. **Gotcha:** Webhook secret must be base64 encoded for manual verification (SDKs handle this)

#### POL-003: Webhook Endpoint Auto-Disabled
```
No webhook deliveries received. Polar dashboard shows endpoint as "Disabled".
```
**Cause:** 10 consecutive failed deliveries (non-2xx responses).
**Fix:**
1. Check Polar dashboard > Webhooks > Delivery overview for error details
2. Common causes: endpoint returns 404 (wrong route path), 403 (auth middleware blocking), 3xx (redirect)
3. Fix the endpoint, then manually re-enable in Polar dashboard settings
4. Polar sends email notification when endpoint is disabled

#### POL-004: Type Mismatch Between SDK and Adapter
```
Type 'WebhookSubscriptionCreatedPayload' is not assignable to type '...'
TS2345: Argument of type '(payload: WebhookSubscriptionCreatedPayload) => ...'
```
**Cause:** `@polar-sh/sdk@0.29.0` types incompatible with `@polar-sh/nextjs@0.4.1` peer dependency (`@0.38.x`).
**Fix A (quick):** Use `payload: any` with eslint-disable:
```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any
onSubscriptionCreated: async (payload: any) => { ... }
```
**Fix B (proper):** Upgrade both packages to matching versions:
```bash
pnpm add @polar-sh/sdk@latest @polar-sh/nextjs@latest
```

### HIGH

#### POL-005: Webhook 404 -- Route Not Found
```
HTTP 404 in Polar webhook delivery log
```
**Cause:** Endpoint URL path doesn't match your API route file path.
**Fix:** Verify:
- Route file: `src/app/api/polar/route.ts` -> endpoint: `https://yourdomain.com/api/polar`
- Route file: `src/app/api/webhook/polar/route.ts` -> endpoint: `https://yourdomain.com/api/webhook/polar`
- Test with `curl -X POST https://yourdomain.com/api/polar`
- No trailing slash (Polar doesn't follow redirects)

#### POL-006: Webhook 403 -- Blocked by Auth/Proxy
```
HTTP 403 in Polar webhook delivery log
```
**Cause:** Auth middleware (proxy.ts in Next.js 16) or Cloudflare Bot Fight Mode blocking webhook requests.
**Fix:**
1. Exclude `/api/polar` from proxy.ts matcher:
   ```typescript
   export const config = {
     matcher: ["/dashboard/:path*", "/cv/:path*", "/billing/:path*"],
     // NOT "/api/:path*"
   }
   ```
2. If using Cloudflare, whitelist Polar IPs (see webhooks.md section 5.8)
3. Disable Bot Fight Mode for webhook endpoint path

#### POL-007: Webhook 3xx -- Redirect Not Followed
```
HTTP 301/302 in Polar webhook delivery log
```
**Cause:** Polar does not follow redirects. URL redirects to different path.
**Fix:** Configure the final destination URL directly in Polar dashboard. Common causes:
- Missing trailing slash or extra trailing slash
- HTTP -> HTTPS redirect (always use HTTPS URL)
- www -> non-www redirect

#### POL-008: Checkout URL is null/undefined
```
TypeError: Cannot read properties of undefined (reading 'url')
```
**Cause:** `polar.checkouts.create()` failed silently or returned unexpected shape.
**Fix:** Always check the response:
```typescript
const checkout = await polar.checkouts.create({ ... })
if (!checkout?.url) {
  console.error("Checkout creation returned no URL:", checkout)
  return NextResponse.json({ error: "Checkout failed" }, { status: 500 })
}
return NextResponse.json({ url: checkout.url })
```

#### POL-009: Rate Limit Exceeded (429)
```
Status: 429 Too Many Requests
Retry-After: 30
```
**Cause:** Exceeded 300 requests/minute per organization.
**Fix:** Implement exponential backoff:
```typescript
async function polarWithRetry<T>(fn: () => Promise<T>, retries = 3): Promise<T> {
  try {
    return await fn()
  } catch (error: any) {
    if (error.status === 429 && retries > 0) {
      const retryAfter = parseInt(error.headers?.["retry-after"] ?? "5", 10)
      await new Promise((r) => setTimeout(r, retryAfter * 1000))
      return polarWithRetry(fn, retries - 1)
    }
    throw error
  }
}
```

#### POL-010: Metadata Key Too Long
```
Validation error: Metadata key exceeds maximum length of 40 characters
```
**Cause:** Metadata key string > 40 characters or > 50 key-value pairs.
**Fix:** Keep metadata keys short. Max 40 chars per key, max 50 pairs per object.

### MEDIUM

#### POL-011: customer_external_id Deprecated
```
Warning: 'customer_external_id' is deprecated. Use 'external_customer_id'.
```
**Cause:** Field renamed on 2025-06-18 for API consistency.
**Fix:** Replace `customer_external_id` with `external_customer_id` in Checkout and Customer Session API calls.

#### POL-012: Subscription.price_id Deprecated
```
Warning: 'price_id' is deprecated. Use 'prices' array.
```
**Cause:** Deprecated on 2025-03-14 to support usage-based billing.
**Fix:** Access pricing via `subscription.prices` array instead of `subscription.priceId`.

#### POL-013: Order.amount Deprecated
```
Warning: 'amount' is deprecated. Use 'net_amount'.
```
**Cause:** Deprecated on 2025-03-14. New breakdown fields added.
**Fix:** Use `order.netAmount`. Also available: `order.subtotalAmount`, `order.discountAmount`, `order.totalAmount`.

#### POL-014: Revoking Access on subscription.canceled
```
User reports: "My access was removed immediately after I canceled, but I paid for the full month!"
```
**Cause:** Code revokes access in `onSubscriptionCanceled` instead of `onSubscriptionRevoked`.
**Fix:**
```typescript
// WRONG -- user loses access immediately
onSubscriptionCanceled: async (payload) => {
  await db.user.update({ where: { id: userId }, data: { plan: "FREE" } })
}

// CORRECT -- user keeps access until period ends
onSubscriptionCanceled: async (payload) => {
  // Optional: show "Canceling at period end" banner
  await db.user.update({ where: { id: userId }, data: { planCanceling: true } })
},
onSubscriptionRevoked: async (payload) => {
  // NOW revoke access
  await db.user.update({ where: { id: userId }, data: { plan: "FREE", planCanceling: false } })
}
```

#### POL-015: Duplicate Webhook Processing
```
Same order processed twice. User charged appears double in your DB.
```
**Cause:** No idempotency check. Webhook retried after timeout.
**Fix:** Use `webhook-id` header for deduplication:
```typescript
onOrderPaid: async (payload) => {
  const webhookId = payload.webhookId // or extract from headers
  const existing = await db.processedWebhook.findUnique({ where: { id: webhookId } })
  if (existing) return // Already processed

  await db.$transaction([
    db.processedWebhook.create({ data: { id: webhookId } }),
    // ... process order
  ])
}
```

#### POL-016: Webhook Handler Timeout
```
Webhook shows as "Failed" in Polar dashboard. Handler takes > 10 seconds.
```
**Cause:** Polar timeout is 10 seconds. Heavy processing in handler.
**Fix:** Acknowledge immediately, process async:
```typescript
onOrderPaid: async (payload) => {
  // Quick: store raw event
  await db.webhookEvent.create({
    data: { type: "order.paid", payload: JSON.stringify(payload) },
  })
  // Process asynchronously (cron job, queue, etc.)
}
```

#### POL-017: Invoice Not Available (202)
```
Expected invoice data but got 202 Accepted status
```
**Cause:** Invoice generation is async since 2025-06-02. Returns 202 = "processing".
**Fix:** Poll `GET /v1/orders/{id}/invoice` or listen for `order.updated` webhook with `is_invoice_generated: true`.

#### POL-018: Billing Details Immutable After Invoice
```
Error: Cannot update billing details after invoice generation
```
**Cause:** Once invoice is generated, it's permanent and immutable.
**Fix:** Always update billing details BEFORE generating invoice:
```typescript
// 1. Update billing details
await polar.orders.update(orderId, { billingName: "..." })
// 2. THEN generate invoice
await polar.orders.invoice(orderId)
```

#### POL-019: Product Pricing Cannot Be Changed
```
Error: Billing cycle and pricing type cannot be changed after product creation
```
**Cause:** Polar locks billing cycle (one-time vs recurring) and pricing type (fixed vs PWYW) after product creation.
**Fix:** Create a new product with the desired pricing. Archive the old one. Price amount CAN be changed (affects new customers only).

#### POL-020: Missing userId in Webhook Metadata
```
userId is undefined in subscription webhook handler
```
**Cause:** Metadata not passed during checkout creation, or wrong key name.
**Fix:** Ensure metadata is set in checkout:
```typescript
const checkout = await polar.checkouts.create({
  products: [productId],
  metadata: { userId: session.user.id }, // Ensure this is set
  // ...
})
```
And extract correctly in webhook:
```typescript
const userId = payload.data.metadata?.userId as string | undefined
if (!userId) {
  console.error("No userId in webhook metadata:", payload.data.metadata)
  return // Don't crash -- log and investigate
}
```

### LOW

#### POL-021: Sandbox vs Production Data Isolation
```
Products/customers from sandbox don't appear in production
```
**Cause:** Sandbox and production are fully isolated environments.
**Fix:** Expected behavior. Create separate products in each environment. Use `server: "sandbox"` during development, remove or set to `"production"` for deployment.

#### POL-022: Customer Portal Authentication
```
Customer says "I can't log in to the portal"
```
**Cause:** Customer using different email than purchase email.
**Fix:** Use pre-authenticated portal links instead:
```typescript
const session = await polar.customerSessions.create({
  customerId: user.polarCustomerId,
})
// Redirect to session.customerPortalUrl
```

#### POL-023: Webhook Secret Base64 Encoding
```
WebhookVerificationError when doing manual verification
```
**Cause:** Standard Webhooks spec requires base64-encoded secret for HMAC. SDKs handle this automatically.
**Fix:** Use `@polar-sh/sdk/webhooks` `validateEvent()` or `@polar-sh/nextjs` `Webhooks()`. If rolling your own, base64-decode the secret before HMAC:
```typescript
const decodedSecret = Buffer.from(webhookSecret, "base64")
```

#### POL-024: onSubscriptionUpdated Fires on Every Renewal
```
onSubscriptionUpdated handler triggered unexpectedly
```
**Cause:** Subscription renewals trigger `subscription.updated`. No dedicated renewal event.
**Fix:** Check the update type:
```typescript
onSubscriptionUpdated: async (payload) => {
  // Only handle actual changes, not renewals
  // Renewals also trigger order.created with billing_reason: "subscription_cycle"
}
```

#### POL-025: Embedded Checkout Wallet Payments Disabled
```
Apple Pay / Google Pay buttons not appearing in embedded checkout
```
**Cause:** Wallet payment methods disabled by default for embedded checkout. Requires domain validation.
**Fix:** Email Polar support with your organization slug and domain to enable. Not needed for hosted checkout (auto-enabled).
