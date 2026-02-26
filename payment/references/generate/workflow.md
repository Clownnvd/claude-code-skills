# Payment Generate Workflow

## Process

1. **Parse Request** — Extract: payment type (checkout, subscription, portal), features, integrations
2. **Load Criteria** — Read all 10 payment scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| Checkout & Billing (15%) | Session creation, URLs, metadata, line items, UX |
| Subscription Lifecycle (15%) | Create, cancel, status checks, DB sync |
| Webhook Integration (12%) | Signature verification, event routing, idempotency |
| Payment Security (12%) | Env validation, key management, amount validation |
| Pricing & Plans (10%) | Products/Prices, plan switching, proration |
| Customer Portal (8%) | Portal session, self-service features |
| Error Handling (8%) | Stripe error types, retry logic, user messaging |
| Metered Billing (8%) | Usage records, metered prices, visibility |
| Testing (6%) | Test mode, Stripe CLI, test clocks |
| Monitoring (6%) | Payment logging, failure alerts, metrics |

4. **Generate** — Write route handlers + Stripe config + webhook handler + billing page
5. **Self-Check** — Verify all 10 categories
6. **Output** — Code + compliance checklist

## Code Structure

```typescript
// Webhook handler with all quality patterns
export async function POST(request: Request) {
  const body = await request.text()
  const signature = (await headers()).get("stripe-signature")
  // Signature verification, event routing, idempotency, error handling
}
```

## Quality Contract

- All 10 categories addressed
- Score >= 90 (A-) if audited with payment scoring
- Webhook signature verification included
- Error handling with Stripe-specific error types
- Env var validation for all Stripe keys
