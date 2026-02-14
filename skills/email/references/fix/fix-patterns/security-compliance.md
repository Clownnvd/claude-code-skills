# Fix Patterns: Deliverability + Bounce Handling + Auth + Rate Limiting

## Pattern 1: Missing SPF/DKIM/DMARC

**Issue**: No email auth DNS records; high spam risk. **Categories**: Auth (8%), Deliverability (10%)

### After
Document required DNS records in project:
```
SPF:   TXT  @        "v=spf1 include:amazonses.com ~all"
DKIM:  CNAME resend._domainkey  (value from Resend dashboard, 3 records)
DMARC: TXT  _dmarc   "v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com"
MX:    MX   @        feedback-smtp.us-east-1.amazonses.com (priority 10)
```

Add verification check:
```typescript
// src/lib/email-health.ts
import { resend } from "@/lib/resend";
export async function checkDomainVerification(): Promise<boolean> {
  const { data } = await resend.domains.list();
  const domain = process.env.EMAIL_FROM?.split("@")[1];
  return !!data?.data?.find((d) => d.name === domain && d.status === "verified");
}
```
**Verification**: DNS records documented. Domain "verified" in Resend dashboard.

---

## Pattern 2: No Bounce/Complaint Webhook Handler

**Issue**: Bounced addresses keep receiving emails. **Category**: Bounce Handling (10%)

### After
```typescript
// Extend webhook handler (see provider-integration.md Pattern 3)
// Add suppression list (use database in production)
const suppressionList = new Set<string>();
export function isEmailSuppressed(email: string): boolean {
  return suppressionList.has(email.toLowerCase());
}

// In webhook switch:
case "email.bounced":
  for (const addr of event.data.to) { suppressionList.add(addr.toLowerCase()); }
  break;
case "email.complained":
  for (const addr of event.data.to) { suppressionList.add(addr.toLowerCase()); }
  break;

// Check before sending (src/lib/email.ts):
export async function sendEmail(to: string, subject: string, html: string) {
  if (isEmailSuppressed(to)) {
    console.warn(`[Email] Skipped suppressed address: ${to}`);
    return { success: false, error: "Address suppressed" };
  }
  return enqueueEmail({ from: EMAIL_FROM, to, subject, html });
}
```
**Verification**: Bounced/complained addresses added to suppression. Suppressed addresses blocked before send.

---

## Pattern 3: No Rate Limiting on Email Endpoints

**Issue**: Password reset endpoint can be abused. **Category**: Rate Limiting (8%)

### Before
```typescript
export async function POST(req: Request) {
  const { email } = await req.json();
  await sendPasswordResetEmail(email); // No rate limit
  return Response.json({ success: true });
}
```

### After
```typescript
// src/lib/rate-limit.ts
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";
const redis = new Redis({ url: process.env.UPSTASH_REDIS_REST_URL!, token: process.env.UPSTASH_REDIS_REST_TOKEN! });
export const emailRateLimit = new Ratelimit({
  redis, limiter: Ratelimit.slidingWindow(3, "15 m"), prefix: "ratelimit:email",
});

// src/app/api/auth/forgot-password/route.ts
import { emailRateLimit } from "@/lib/rate-limit";
export async function POST(req: Request) {
  const { email } = await req.json();
  const ip = req.headers.get("x-forwarded-for") ?? "unknown";
  const { success, remaining } = await emailRateLimit.limit(`${ip}:${email}`);
  if (!success) {
    return Response.json({ error: "Too many requests" }, {
      status: 429, headers: { "Retry-After": "900", "X-RateLimit-Remaining": "0" },
    });
  }
  await sendPasswordResetEmail(email);
  return Response.json({ success: true }, { headers: { "X-RateLimit-Remaining": String(remaining) } });
}
```
**Verification**: Endpoint returns 429 after 3 requests in 15 min. Rate limit headers present.

---

## Pattern 4: Weak DMARC Policy

**Issue**: DMARC at `p=none`; domain spoofing possible. **Category**: Auth (8%)

### Before
```
_dmarc.yourdomain.com TXT "v=DMARC1; p=none"
```

### After
```
_dmarc.yourdomain.com TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; pct=100"
```
Upgrade path: `p=none` (2 weeks monitoring) -> `p=quarantine` -> `p=reject`.

**Verification**: DMARC shows `p=quarantine` or `p=reject`. Aggregate reports configured.
