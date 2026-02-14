# Resend SDK Patterns

Reference for Resend API integration with Next.js 16 App Router and Upstash QStash.

## Client Initialization

```typescript
// src/lib/resend.ts
import { Resend } from "resend";
if (!process.env.RESEND_API_KEY) { throw new Error("RESEND_API_KEY is required"); }
export const resend = new Resend(process.env.RESEND_API_KEY);
```

## Send Single Email

```typescript
import { resend } from "@/lib/resend";
import { render } from "@react-email/render";
import { WelcomeEmail } from "@/emails/welcome";

const html = await render(WelcomeEmail({ name: user.name }));
const { data, error } = await resend.emails.send({
  from: process.env.EMAIL_FROM!, to: user.email, subject: "Welcome", html,
});
if (error) { throw new Error(`Failed to send: ${error.message}`); }
```

## Batch Send

```typescript
const { data, error } = await resend.batch.send(
  users.map((user) => ({
    from: process.env.EMAIL_FROM!, to: user.email, subject: "Weekly digest",
    html: render(DigestEmail({ items: user.items })),
  }))
); // Batch limit: 100 emails per call
```

## Domain Verification

```typescript
const { data } = await resend.domains.list();
const verified = data?.data?.find((d) => d.name === "yourdomain.com" && d.status === "verified");
```

DNS records required: MX (`feedback-smtp.us-east-1.amazonses.com`), TXT SPF (`v=spf1 include:amazonses.com ~all`), 3 CNAME DKIM (from Resend dashboard), TXT DMARC (`v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com`).

## QStash Queue Integration

```typescript
// src/lib/queue.ts
import { Client } from "@upstash/qstash";
if (!process.env.QSTASH_TOKEN) { throw new Error("QSTASH_TOKEN is required"); }
export const qstash = new Client({ token: process.env.QSTASH_TOKEN });

export async function enqueueEmail(payload: EmailPayload) {
  return qstash.publishJSON({
    url: `${process.env.NEXT_PUBLIC_APP_URL}/api/queue/email`,
    body: payload, retries: 3, delay: 0,
  });
}
```

## QStash Worker Endpoint

```typescript
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

## Webhook Handler

```typescript
// src/app/api/webhooks/resend/route.ts
import { Webhook } from "svix";
const webhookSecret = process.env.RESEND_WEBHOOK_SECRET!;

export async function POST(req: Request) {
  const body = await req.text();
  const headers = {
    "svix-id": req.headers.get("svix-id")!,
    "svix-timestamp": req.headers.get("svix-timestamp")!,
    "svix-signature": req.headers.get("svix-signature")!,
  };
  const wh = new Webhook(webhookSecret);
  const event = wh.verify(body, headers) as ResendWebhookEvent;

  switch (event.type) {
    case "email.delivered": /* track delivery */ break;
    case "email.bounced": /* add to suppression list */ break;
    case "email.complained": /* unsubscribe + suppress */ break;
    case "email.opened": /* track open */ break;
    case "email.clicked": /* track click */ break;
  }
  return Response.json({ received: true });
}
```

## Environment Variables

```env
RESEND_API_KEY=re_xxxxxxxxxxxxx
RESEND_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
EMAIL_FROM=notifications@yourdomain.com
QSTASH_TOKEN=xxxxxxxxxxxxx
QSTASH_CURRENT_SIGNING_KEY=sig_xxxxx
QSTASH_NEXT_SIGNING_KEY=sig_xxxxx
NEXT_PUBLIC_APP_URL=https://yourdomain.com
```
