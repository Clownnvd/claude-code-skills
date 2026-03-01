# Polar Free/Pro Tier Gating

> Section 7 from the Polar Payment SDK Comprehensive Reference.
> Covers server-side plan checks, CV limits, AI enhancement limits, template gating, plan tiers, and customer state gating.

---

## 7. Free/Pro Tier Gating

### 7.1 Server-Side Plan Check (Prisma)

```typescript
// src/lib/plan.ts
import { db } from "@/lib/db"

export async function getUserPlan(userId: string) {
  const user = await db.user.findUnique({
    where: { id: userId },
    select: { plan: true },
  })
  return user?.plan ?? "FREE"
}

export async function requirePro(userId: string) {
  const plan = await getUserPlan(userId)
  if (plan !== "PRO") {
    throw new Error("Pro plan required")
  }
}
```

### 7.2 CV Limit Enforcement

```typescript
// In CV creation route handler
const plan = await getUserPlan(session.user.id)
if (plan === "FREE") {
  const cvCount = await db.cv.count({ where: { userId: session.user.id } })
  if (cvCount >= 1) {
    return NextResponse.json(
      { error: "Free plan limited to 1 CV. Upgrade to Pro for unlimited." },
      { status: 403 }
    )
  }
}
```

### 7.3 AI Enhancement Limit

```typescript
// In AI enhance route handler
const plan = await getUserPlan(session.user.id)
if (plan === "FREE") {
  const thisMonth = new Date()
  thisMonth.setDate(1)
  thisMonth.setHours(0, 0, 0, 0)

  const aiCount = await db.aiUsage.count({
    where: {
      userId: session.user.id,
      createdAt: { gte: thisMonth },
    },
  })

  if (aiCount >= 3) {
    return NextResponse.json(
      { error: "Free plan limited to 3 AI enhancements/month." },
      { status: 403 }
    )
  }
}
```

### 7.4 Template Gating

```typescript
const PREMIUM_TEMPLATES = ["modern", "creative"]

function isTemplateAllowed(template: string, plan: string): boolean {
  if (plan === "PRO") return true
  return !PREMIUM_TEMPLATES.includes(template)
}
```

### 7.5 CViet Plan Tiers

| Feature | Free | Pro ($5/month) |
|---------|------|----------------|
| CV count | 1 | Unlimited |
| Templates | Classic only | Classic, Modern, Creative |
| AI enhancements | 3/month | Unlimited |
| Bilingual export | No | Yes (VI/EN) |
| PDF export | Yes | Yes |
| Priority support | No | Yes |

### 7.6 Using Customer State for Gating (Alternative)

Instead of storing plan in your DB, query Polar directly:

```typescript
async function hasActivePro(externalUserId: string): Promise<boolean> {
  try {
    const state = await polar.customers.getStateExternal(externalUserId)
    return state.activeSubscriptions.some(
      (sub) => sub.productId === process.env.POLAR_PRO_PRODUCT_ID
    )
  } catch {
    return false
  }
}
```

**Trade-off:** Real-time accuracy vs. latency (API call per check). For CViet, storing `plan` in the DB (updated via webhooks) is recommended.
