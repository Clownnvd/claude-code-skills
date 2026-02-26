# Fix Patterns: Transactional Email + Notification Queue & Delivery

## Pattern 1: Missing Email Service Layer

**Issue**: Send calls scattered across routes. **Category**: Transactional Email (15%)

### Before
```typescript
// src/app/api/auth/signup/route.ts -- direct Resend call, no abstraction
const resend = new Resend(process.env.RESEND_API_KEY);
await resend.emails.send({
  from: "noreply@example.com", to: email, subject: "Welcome",
  html: `<h1>Welcome ${name}</h1>`,
});
```

### After
```typescript
// src/lib/email.ts -- service layer with typed functions
import { render } from "@react-email/render";
import { enqueueEmail } from "@/lib/queue";
import { WelcomeEmail } from "@/emails/welcome";

export async function sendWelcomeEmail(user: { name: string; email: string }) {
  const html = await render(WelcomeEmail({ name: user.name, loginUrl: `${process.env.NEXT_PUBLIC_APP_URL}/login` }));
  return enqueueEmail({ from: process.env.EMAIL_FROM!, to: user.email, subject: `Welcome, ${user.name}!`, html });
}

// src/app/api/auth/signup/route.ts -- clean trigger
import { sendWelcomeEmail } from "@/lib/email";
// ... after user creation:
await sendWelcomeEmail({ name, email });
```
**Verification**: No direct `resend.emails.send()` in routes. All triggers call service layer.

---

## Pattern 2: Synchronous Email Sending (No Queue)

**Issue**: Emails sent synchronously, blocking request. **Category**: Queue & Delivery (12%)

### Before
```typescript
// Blocks request until Resend API responds
const { data, error } = await resend.emails.send({ from, to, subject, html });
```

### After
```typescript
// src/lib/queue.ts
import { Client } from "@upstash/qstash";
if (!process.env.QSTASH_TOKEN) { throw new Error("QSTASH_TOKEN is required"); }
export const qstash = new Client({ token: process.env.QSTASH_TOKEN });

export async function enqueueEmail(payload: EmailPayload) {
  return qstash.publishJSON({
    url: `${process.env.NEXT_PUBLIC_APP_URL}/api/queue/email`,
    body: payload, retries: 3,
  });
}

// src/app/api/queue/email/route.ts
import { verifySignatureAppRouter } from "@upstash/qstash/nextjs";
import { resend } from "@/lib/resend";

async function handler(req: Request) {
  const payload = await req.json();
  const { data, error } = await resend.emails.send(payload);
  if (error) return Response.json({ error: error.message }, { status: 500 });
  return Response.json({ id: data?.id });
}
export const POST = verifySignatureAppRouter(handler);
```
**Verification**: `resend.emails.send()` only in worker. Routes use `enqueueEmail()`.

---

## Pattern 3: No Retry Logic or Dead Letter Queue

**Issue**: Failed queue messages silently dropped. **Category**: Queue & Delivery (12%)

### Before
```typescript
return qstash.publishJSON({ url: workerUrl, body: payload }); // No retries
```

### After
```typescript
return qstash.publishJSON({
  url: workerUrl, body: payload, retries: 3,
  callback: `${process.env.NEXT_PUBLIC_APP_URL}/api/queue/email/callback`,
  failureCallback: `${process.env.NEXT_PUBLIC_APP_URL}/api/queue/email/dlq`,
});

// src/app/api/queue/email/dlq/route.ts
import { verifySignatureAppRouter } from "@upstash/qstash/nextjs";
async function handler(req: Request) {
  const failed = await req.json();
  console.error("[DLQ] Email failed after retries:", failed);
  return Response.json({ received: true });
}
export const POST = verifySignatureAppRouter(handler);
```
**Verification**: Retries >= 3. Dead letter endpoint exists and logs failures.
