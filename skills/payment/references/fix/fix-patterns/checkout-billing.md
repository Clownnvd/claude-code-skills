# Fix Patterns: Checkout & Billing + Customer Portal + Pricing

## Missing Success/Cancel URLs

### Before
```typescript
const session = await stripe.checkout.sessions.create({
  mode: "subscription", line_items: [{ price: priceId, quantity: 1 }],
}) // user gets stuck after checkout
```

### After
```typescript
const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing?success=true&session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing?canceled=true`,
  metadata: { userId },
  customer_email: userEmail,
})
```

## No Error Handling on Checkout

### Before
```typescript
export async function POST(request: Request) {
  const { priceId } = await request.json()
  const session = await stripe.checkout.sessions.create({ ... }) // crashes on error
  return NextResponse.json({ url: session.url })
}
```

### After
```typescript
export async function POST(request: Request) {
  try {
    const { priceId, userId } = await request.json()
    if (!priceId || !userId) {
      return NextResponse.json({ error: "Missing required fields" }, { status: 400 })
    }
    const session = await stripe.checkout.sessions.create({
      mode: "subscription",
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing?success=true`,
      cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing?canceled=true`,
      metadata: { userId },
    })
    return NextResponse.json({ url: session.url })
  } catch (error) {
    if (error instanceof Stripe.errors.StripeInvalidRequestError) {
      return NextResponse.json({ error: "Invalid checkout configuration" }, { status: 400 })
    }
    console.error("Checkout error:", error)
    return NextResponse.json({ error: "Failed to create checkout session" }, { status: 500 })
  }
}
```

## Missing Metadata

### Before
```typescript
const session = await stripe.checkout.sessions.create({
  mode: "payment", line_items: [{ price: priceId, quantity: 1 }],
}) // webhook cannot identify who paid
```

### After
```typescript
const session = await stripe.checkout.sessions.create({
  mode: "payment",
  line_items: [{ price: priceId, quantity: 1 }],
  metadata: { userId: user.id, productType: "KING_TEMPLATE", source: "billing_page" },
})
```

## No Customer Portal Endpoint

### After: Create portal route
```typescript
// src/app/api/stripe/portal/route.ts
export async function POST(request: Request) {
  try {
    const session = await auth.api.getSession({ headers: request.headers })
    if (!session?.user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    const user = await prisma.user.findUnique({
      where: { id: session.user.id }, select: { stripeCustomerId: true },
    })
    if (!user?.stripeCustomerId) {
      return NextResponse.json({ error: "No billing account" }, { status: 404 })
    }
    const portalSession = await stripe.billingPortal.sessions.create({
      customer: user.stripeCustomerId,
      return_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing`,
    })
    return NextResponse.json({ url: portalSession.url })
  } catch (error) {
    console.error("Portal error:", error)
    return NextResponse.json({ error: "Failed to create portal session" }, { status: 500 })
  }
}
```

## Hardcoded Prices

### Before
```typescript
const plans = [{ name: "Pro", price: "$29/mo", priceId: "price_xxx" }] // drifts from Stripe
```

### After: Fetch from Stripe API
```typescript
export default async function BillingPage() {
  const prices = await stripe.prices.list({
    active: true, expand: ["data.product"], type: "recurring",
  })
  return (
    <div>
      {prices.data.map((price) => (
        <PricingCard key={price.id}
          name={(price.product as Stripe.Product).name}
          amount={price.unit_amount! / 100}
          interval={price.recurring!.interval}
          priceId={price.id} />
      ))}
    </div>
  )
}
```
