# Error Handling

## Stripe Error Types

| Type | Cause | Action |
|------|-------|--------|
| `StripeCardError` | Card declined | Show user message, ask for different card |
| `StripeRateLimitError` | Too many requests | Retry with exponential backoff |
| `StripeInvalidRequestError` | Invalid parameters | Fix code, check params |
| `StripeAPIError` | Stripe server error | Retry with same idempotency key |
| `StripeConnectionError` | Network failure | Retry with same idempotency key |
| `StripeAuthenticationError` | Invalid API key | Check STRIPE_SECRET_KEY |
| `StripePermissionError` | Insufficient permissions | Check account permissions |
| `StripeIdempotencyError` | Conflicting idempotency key | Generate new key |

## Try/Catch Pattern

```typescript
import Stripe from "stripe";

async function safeStripeCall<T>(fn: () => Promise<T>): Promise<
  { data: T; error: null } | { data: null; error: string }
> {
  try {
    const data = await fn();
    return { data, error: null };
  } catch (err) {
    if (err instanceof Stripe.errors.StripeCardError) {
      return { data: null, error: err.message }; // User-friendly
    }
    if (err instanceof Stripe.errors.StripeRateLimitError) {
      return { data: null, error: "Too many requests. Please try again." };
    }
    if (err instanceof Stripe.errors.StripeAuthenticationError) {
      console.error("Stripe auth error — check API key");
      return { data: null, error: "Payment service configuration error." };
    }
    if (err instanceof Stripe.errors.StripeAPIError) {
      console.error("Stripe API error:", err.message);
      return { data: null, error: "Payment service temporarily unavailable." };
    }
    console.error("Unknown Stripe error:", err);
    return { data: null, error: "An unexpected error occurred." };
  }
}
```

## Usage

```typescript
const result = await safeStripeCall(() =>
  stripe.checkout.sessions.create({ /* ... */ })
);

if (result.error) {
  return { error: result.error }; // Return to client
}

redirect(result.data.url!);
```

## Retry with Exponential Backoff

```typescript
async function retryStripe<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (err instanceof Stripe.errors.StripeRateLimitError && attempt < maxRetries) {
        const delay = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s
        await new Promise((r) => setTimeout(r, delay));
        continue;
      }
      if (err instanceof Stripe.errors.StripeAPIError && attempt < maxRetries) {
        const delay = Math.pow(2, attempt) * 1000;
        await new Promise((r) => setTimeout(r, delay));
        continue;
      }
      throw err; // Non-retryable or max retries reached
    }
  }
  throw new Error("Max retries exceeded");
}
```

## Declined Payment Recovery

```typescript
async function handlePaymentFailed(invoice: Stripe.Invoice) {
  const customerId = invoice.customer as string;
  const customer = await stripe.customers.retrieve(customerId);

  if (customer.deleted) return;

  // Notify user
  await sendEmail({
    to: (customer as Stripe.Customer).email!,
    subject: "Payment failed — action required",
    body: `Update your payment method: ${portalUrl}`,
  });

  // Update user status in database
  await db.user.update({
    where: { stripeCustomerId: customerId },
    data: { paymentStatus: "past_due" },
  });
}
```

## Card Decline Codes

| Code | Meaning | User Message |
|------|---------|-------------|
| `card_declined` | Generic decline | Card was declined. Try another card. |
| `insufficient_funds` | Not enough balance | Insufficient funds. Try another card. |
| `expired_card` | Card expired | Card has expired. Use a different card. |
| `incorrect_cvc` | Wrong CVC | Incorrect security code. Try again. |
| `processing_error` | Processing issue | Processing error. Please try again. |
| `lost_card` | Reported lost | Card cannot be used. Try another card. |

## Key Points
- Never expose raw Stripe errors to users — map to friendly messages
- Retry only `StripeRateLimitError` and `StripeAPIError`
- `StripeCardError` is user-recoverable (different card)
- `StripeAuthenticationError` means wrong API key — alert ops
- Log all errors server-side for debugging
