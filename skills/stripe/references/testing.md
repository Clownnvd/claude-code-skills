# Testing

## Test Card Numbers

| Card | Result |
|------|--------|
| `4242 4242 4242 4242` | Success |
| `4000 0000 0000 0002` | Generic decline |
| `4000 0000 0000 9995` | Insufficient funds |
| `4000 0000 0000 0069` | Expired card |
| `4000 0000 0000 0127` | CVC check fails |
| `4000 0000 0000 3220` | 3D Secure 2 (auth required) |
| `4000 0025 0000 3155` | 3D Secure (auth required) |
| `4000 0000 0000 3055` | 3D Secure (supported, not required) |
| `4000 0000 0000 0341` | Attach succeeds, charge fails |
| `5555 5555 5555 4444` | Mastercard success |
| `3782 822463 10005` | Amex success |

All test cards use any future expiry (e.g., `12/34`) and any 3-digit CVC (4-digit for Amex).

## Stripe CLI Setup

```bash
# Install
brew install stripe/stripe-cli/stripe    # macOS
scoop install stripe                      # Windows
# Or download from https://github.com/stripe/stripe-cli

# Authenticate
stripe login

# Forward webhooks to local dev
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Print webhook signing secret (add to .env.local)
stripe listen --print-secret
```

## Trigger Events

```bash
# One-time payment
stripe trigger checkout.session.completed
stripe trigger payment_intent.succeeded
stripe trigger payment_intent.payment_failed

# Subscriptions
stripe trigger customer.subscription.created
stripe trigger customer.subscription.updated
stripe trigger customer.subscription.deleted
stripe trigger invoice.paid
stripe trigger invoice.payment_failed

# Custom event with data
stripe trigger payment_intent.succeeded --add payment_intent:metadata[orderId]=test123
```

## API Commands

```bash
# Customers
stripe customers create --email="test@example.com" --name="Test User"
stripe customers list --limit=5

# Products & Prices
stripe products create --name="Test Product"
stripe prices create --product=prod_xxx --unit-amount=2900 --currency=usd

# Subscriptions
stripe subscriptions create --customer=cus_xxx --items[0][price]=price_xxx

# View recent events
stripe events list --limit=10
stripe logs tail
stripe logs tail --filter-status-code=400
```

## Test Clocks (Subscription Time Travel)

```typescript
// Create test clock
const testClock = await stripe.testHelpers.testClocks.create({
  frozen_time: Math.floor(Date.now() / 1000),
  name: "Subscription test",
});

// Create customer attached to test clock
const customer = await stripe.customers.create({
  email: "test@example.com",
  test_clock: testClock.id,
});

// Create subscription (starts in test clock time)
const sub = await stripe.subscriptions.create({
  customer: customer.id,
  items: [{ price: priceId }],
});

// Advance time by 32 days (triggers invoice + payment)
await stripe.testHelpers.testClocks.advance(testClock.id, {
  frozen_time: Math.floor(Date.now() / 1000) + 32 * 24 * 60 * 60,
});
```

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Stripe CLI
  run: |
    stripe listen --forward-to localhost:3000/api/webhooks/stripe &
    sleep 2
    npm run test:e2e
    kill %1
  env:
    STRIPE_API_KEY: ${{ secrets.STRIPE_TEST_SECRET_KEY }}
```

## Key Points
- Always use `sk_test_` keys in development and CI
- `stripe listen` must run during local webhook testing
- Test Clocks simulate subscription lifecycle without waiting
- Use `stripe trigger` to test webhook handlers
- Never use live keys (`sk_live_`) in test environments
