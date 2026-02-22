# Radar — Fraud Detection

Stripe Radar provides machine-learning fraud detection included with every Stripe account.

## Default Protection

Radar is enabled automatically. It blocks high-risk payments and flags suspicious ones.

## Custom Rules (Radar for Fraud Teams)

Configure in Dashboard → Radar → Rules:

```
# Block rule examples
Block if :card_country: != :ip_country:
Block if :risk_level: = 'highest'
Block if :is_disposable_email:

# Review rule examples
Review if :risk_level: = 'elevated'
Review if :amount_in_usd: > 500

# Allow rule examples
Allow if :is_recurring_customer:
```

## 3D Secure Triggers

```typescript
// Request 3D Secure for high-risk payments
const paymentIntent = await stripe.paymentIntents.create({
  amount: 5000,
  currency: "usd",
  payment_method_options: {
    card: {
      request_three_d_secure: "any", // or "automatic" (default)
    },
  },
});
```

| Value | Behavior |
|-------|----------|
| `automatic` | Stripe decides based on risk (recommended) |
| `any` | Always request 3D Secure |

## Risk Evaluation in Webhooks

```typescript
async function handlePaymentSucceeded(pi: Stripe.PaymentIntent) {
  const charge = pi.latest_charge as Stripe.Charge;

  if (charge.outcome?.risk_level === "elevated") {
    // Flag for manual review
    await flagOrderForReview(pi.metadata.orderId);
  }

  if (charge.outcome?.risk_level === "highest") {
    // Auto-refund high-risk payments
    await stripe.refunds.create({ payment_intent: pi.id });
    return;
  }
}
```

## Dispute Handling

```typescript
// Webhook: charge.dispute.created
async function handleDispute(dispute: Stripe.Dispute) {
  // Alert team
  await notifyTeam(`Dispute: ${dispute.id} — $${dispute.amount / 100}`);

  // Submit evidence (within 7-21 days depending on network)
  await stripe.disputes.update(dispute.id, {
    evidence: {
      customer_email_address: "customer@example.com",
      product_description: "Digital subscription service",
      uncategorized_text: "Customer used service for 3 months before dispute",
    },
  });
}
```

## Dispute Webhook Events

| Event | When |
|-------|------|
| `charge.dispute.created` | Customer filed dispute |
| `charge.dispute.updated` | Evidence submitted or status changed |
| `charge.dispute.closed` | Resolved (won or lost) |

## Key Points
- Radar is included free — no extra setup needed
- Use `automatic` 3D Secure (Stripe optimizes conversion vs fraud)
- Monitor `charge.outcome.risk_level` in webhooks
- Respond to disputes within deadline (evidence submission)
- Block rules in Radar Dashboard for known fraud patterns
