# Fix Patterns: Email Provider Integration + Analytics & Tracking

## Pattern 1: Missing Resend Client Initialization

**Issue**: No env validation; crashes at runtime. **Category**: Provider Integration (12%)

### Before
```typescript
import { Resend } from "resend";
const resend = new Resend(process.env.RESEND_API_KEY); // No validation
```

### After
```typescript
// src/lib/resend.ts
import { Resend } from "resend";
if (!process.env.RESEND_API_KEY) { throw new Error("RESEND_API_KEY is required"); }
if (!process.env.EMAIL_FROM) { throw new Error("EMAIL_FROM is required"); }
export const resend = new Resend(process.env.RESEND_API_KEY);
export const EMAIL_FROM = process.env.EMAIL_FROM;
```
**Verification**: App fails fast if env vars missing. `.env.example` documents variables.

---

## Pattern 2: No Error Handling on Send Calls

**Issue**: Errors silently swallowed. **Category**: Provider Integration (12%)

### Before
```typescript
try { await resend.emails.send({ from, to, subject, html }); } catch { /* swallowed */ }
```

### After
```typescript
interface SendResult { success: boolean; id?: string; error?: string; }

export async function sendEmail(to: string, subject: string, html: string): Promise<SendResult> {
  const { data, error } = await resend.emails.send({
    from: EMAIL_FROM, to, subject, html,
  });
  if (error) {
    console.error(`[Email] Failed to send to ${to}:`, error.message);
    return { success: false, error: error.message };
  }
  return { success: true, id: data?.id };
}
```
**Verification**: Every `resend.emails.send()` destructures `{ data, error }`. Errors logged.

---

## Pattern 3: No Webhook for Delivery Events

**Issue**: No delivery tracking; blind to failures. **Category**: Analytics & Tracking (7%)

### After
```typescript
// src/app/api/webhooks/resend/route.ts
import { Webhook } from "svix";
if (!process.env.RESEND_WEBHOOK_SECRET) { throw new Error("RESEND_WEBHOOK_SECRET required"); }
const webhookSecret = process.env.RESEND_WEBHOOK_SECRET;

interface ResendEvent { type: string; data: { email_id: string; to: string[]; created_at: string }; }

export async function POST(req: Request) {
  const body = await req.text();
  const headers = {
    "svix-id": req.headers.get("svix-id") ?? "",
    "svix-timestamp": req.headers.get("svix-timestamp") ?? "",
    "svix-signature": req.headers.get("svix-signature") ?? "",
  };
  let event: ResendEvent;
  try { event = new Webhook(webhookSecret).verify(body, headers) as ResendEvent; }
  catch { return Response.json({ error: "Invalid signature" }, { status: 401 }); }

  console.log(`[Webhook] ${event.type}:`, event.data.email_id);
  switch (event.type) {
    case "email.delivered": /* record delivery */ break;
    case "email.opened": /* track open */ break;
    case "email.clicked": /* track click */ break;
    case "email.bounced": /* suppress address */ break;
    case "email.complained": /* unsubscribe */ break;
  }
  return Response.json({ received: true });
}
```
**Verification**: Webhook returns 200 on valid signatures, 401 on invalid.

---

## Pattern 4: Hardcoded From Address

**Issue**: From address hardcoded; breaks on domain change. **Category**: Provider (12%), Deliverability (10%)

### Before
```typescript
await resend.emails.send({ from: "noreply@example.com", to, subject, html });
```

### After
```typescript
import { EMAIL_FROM } from "@/lib/resend";
await resend.emails.send({ from: EMAIL_FROM, to, subject, html });
// EMAIL_FROM loaded from env var in src/lib/resend.ts
```
**Verification**: No hardcoded from addresses. Domain verified in Resend dashboard.
