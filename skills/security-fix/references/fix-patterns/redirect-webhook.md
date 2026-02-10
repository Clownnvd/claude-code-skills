# Fix Patterns: Redirects + Webhooks

## Open Redirect Fixes

### Block dangerous redirect patterns

```typescript
function isValidRedirectUrl(url: string): boolean {
  // Block protocol-relative URLs and backslash tricks
  if (url.startsWith("//") || url.startsWith("/\\")) {
    return false;
  }
  // Only allow relative paths
  if (!url.startsWith("/")) {
    return false;
  }
  // Block encoded variants
  const decoded = decodeURIComponent(url);
  if (decoded.startsWith("//") || decoded.startsWith("/\\")) {
    return false;
  }
  return true;
}
```

### Validate callbackUrl parameters

```typescript
// In middleware or auth handler
const callbackUrl = searchParams.get("callbackUrl") ?? "/dashboard";

if (!isValidRedirectUrl(callbackUrl)) {
  return NextResponse.redirect(new URL("/dashboard", req.url));
}
```

### Use URL constructor for safe parsing

```typescript
// Before: string concatenation
const redirectUrl = baseUrl + userPath;

// After: safe URL construction
const redirectUrl = new URL(userPath, baseUrl);
```

### Allowlist for external redirects

```typescript
const ALLOWED_EXTERNAL_HOSTS = [
  "github.com",
  "accounts.google.com",
];

function isAllowedExternalUrl(url: string): boolean {
  try {
    const parsed = new URL(url);
    return ALLOWED_EXTERNAL_HOSTS.includes(parsed.hostname);
  } catch {
    return false;
  }
}
```

## Webhook Security Fixes

### Verify Stripe webhook signature

```typescript
import Stripe from "stripe";

const rawBody = await req.text();
const signature = req.headers.get("stripe-signature");

if (!signature) {
  return errorResponse("UNAUTHORIZED", "Missing signature", 401);
}

let event: Stripe.Event;
try {
  event = stripe.webhooks.constructEvent(
    rawBody, signature, env.STRIPE_WEBHOOK_SECRET
  );
} catch (error) {
  logger.warn("Invalid webhook signature", { error });
  return errorResponse("UNAUTHORIZED", "Invalid signature", 401);
}
```

### Add idempotency check

```typescript
// Check-before-create by payment/event ID
const existing = await prisma.purchase.findUnique({
  where: { stripePaymentId: session.payment_intent as string },
});

if (existing) {
  logger.info("Duplicate webhook, already processed", { paymentId });
  return successResponse({ received: true });
}
```

### Add timeout to external API calls

```typescript
// GitHub API with timeout
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 10000);

try {
  const response = await fetch(githubApiUrl, {
    signal: controller.signal,
    headers: { Authorization: `token ${env.GITHUB_TOKEN}` },
  });
} finally {
  clearTimeout(timeout);
}
```

### Don't forward external API errors

```typescript
// Before
catch (error) {
  return NextResponse.json({ error: error.message }, { status: 500 });
}

// After
catch (error) {
  logger.error("External API call failed", {
    service: "github",
    error: error instanceof Error ? error.message : "Unknown error",
  });
  return errorResponse("EXTERNAL_ERROR", "Service temporarily unavailable", 502);
}
```
