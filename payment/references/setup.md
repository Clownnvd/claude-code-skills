# Polar Setup -- SDK Compatibility & Configuration

> Sections 1-2 from the Polar Payment SDK Comprehensive Reference.
> Covers SDK versions, known conflicts, breaking changes, installation, environment variables, and rate limits.

---

## 1. SDK Compatibility Matrix

### Package Versions

| Package | CViet Version | Latest (Feb 2026) | Notes |
|---------|--------------|-------------------|-------|
| `@polar-sh/sdk` | `0.29.0` | `0.38.x+` | Breaking changes at v0.6.0 (new generator). Pin versions. |
| `@polar-sh/nextjs` | `0.4.1` | `0.9.3` | Peer-depends on `@polar-sh/sdk`. 49 versions published. |
| `@polar-sh/better-auth` | Not installed | `0.0.5+` | Optional -- unifies auth + payments |
| `@polar-sh/checkout` | Not installed | Latest | For embedded checkout only |
| `zod` | `3.24.0` | `3.24.x` | Required peer dep for `@polar-sh/nextjs` |

### Known Version Conflicts

| SDK Version | nextjs Adapter Version | Compatibility |
|-------------|----------------------|---------------|
| `@polar-sh/sdk@0.29.0` | `@polar-sh/nextjs@0.4.1` | Type mismatch -- webhook handler payload types don't align. Use `payload: any`. |
| `@polar-sh/sdk@0.38.x` | `@polar-sh/nextjs@0.9.x` | Full compatibility. Types align. |
| `@polar-sh/sdk@<0.6.0` | Any | NOT compatible. SDK generator changed at v0.6.0. |

### Breaking Changes Timeline

| Date | Change | Migration |
|------|--------|-----------|
| v0.6.0 | SDK generator rewrite | Not backward compatible. Upgrade all usages. |
| 2025-03-14 | `Subscription.price_id` deprecated | Use `Subscription.prices` array |
| 2025-03-14 | `Order.amount` deprecated | Use `Order.net_amount` |
| 2025-03-14 | `Order.product_price_id` deprecated | Use `Order.items` array |
| 2025-03-25 | `checkout.subtotal_amount` deprecated | Use `checkout.net_amount` |
| 2025-03-25 | `product_id`/`product_price_id` in checkout deprecated | Use `products` array |
| 2025-06-02 | Invoice generation changed to explicit | Must call `POST /v1/orders/{id}/invoice` |
| 2025-06-18 | `customer_external_id` renamed | Use `external_customer_id` in Checkout + Customer Session APIs |

---

## 2. Setup Guide

### 2.1 Installation

```bash
pnpm add @polar-sh/sdk @polar-sh/nextjs zod
```

### 2.2 Environment Variables

```env
# Required
POLAR_ACCESS_TOKEN=polar_oat_xxxxxxxxxxxxx   # Organization Access Token
POLAR_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx     # Webhook signing secret

# Product IDs (from Polar dashboard)
POLAR_PRO_PRODUCT_ID=prod_xxxxxxxxxxxxx      # Pro plan product ID

# Optional
POLAR_ORGANIZATION_ID=org_xxxxxxxxxxxxx      # Org ID (for some API calls)
NEXT_PUBLIC_APP_URL=http://localhost:3000     # For success/cancel URLs
```

**Where to get these:**
- Access Token: Polar dashboard > Organization Settings > Developers > Access Tokens
- Webhook Secret: Polar dashboard > Organization Settings > Webhooks > Add Endpoint > Generated secret
- Product ID: Polar dashboard > Products > Click product > Copy ID from URL
- Sandbox tokens: `https://sandbox.polar.sh/dashboard/{org-slug}/settings#developers`

### 2.3 SDK Initialization

```typescript
// src/lib/polar.ts
import { Polar } from "@polar-sh/sdk"

export const polar = new Polar({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  // server: "sandbox",  // Uncomment for development
  // server: "production", // Default -- omit for production
})
```

**CViet actual file** (`src/lib/polar.ts`):
```typescript
import { Polar } from "@polar-sh/sdk"

export const polar = new Polar({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
})
```

### 2.4 API Base URLs

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.polar.sh/v1` |
| Sandbox | `https://sandbox-api.polar.sh/v1` |

### 2.5 Rate Limits

| Scope | Limit |
|-------|-------|
| Per organization/customer/OAuth2 client | 300 requests/minute |
| Per IP address | 100 requests/second |
| Unauthenticated license key ops | 3 requests/second |

Exceeding returns `429 Too Many Requests` with `Retry-After` header.
