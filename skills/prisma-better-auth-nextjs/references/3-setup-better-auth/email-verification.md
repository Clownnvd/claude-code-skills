# Step 3.6: Email Verification

> Source: King Template codebase — Resend + React Email templates

## Dependencies

```bash
npm install resend react-email @react-email/components
```

## Environment Variables

```env
RESEND_API_KEY=re_xxx
RESEND_FROM=noreply@yourdomain.com
```

## Email Service (`src/lib/email/resend.ts`)

```typescript
import { Resend } from "resend";
import type React from "react";

const resend = new Resend(process.env.RESEND_API_KEY);

type SendReactEmailParams = {
  to: string;
  subject: string;
  react: React.ReactElement;
};

export async function sendReactEmail(params: SendReactEmailParams) {
  const from = process.env.RESEND_FROM;
  if (!process.env.RESEND_API_KEY) throw new Error("Missing RESEND_API_KEY");
  if (!from) throw new Error("Missing RESEND_FROM");

  return resend.emails.send({
    from,
    to: [params.to],
    subject: params.subject,
    react: params.react,
  });
}

// Fire-and-forget variant (non-critical emails)
export function sendReactEmailSafe(params: SendReactEmailParams) {
  void sendReactEmail(params).catch((err) => {
    console.error("email_send_failed", err instanceof Error ? err.message : "Unknown");
  });
}
```

## Auth Config (`src/lib/auth.ts`)

```typescript
export const auth = betterAuth({
  // ...

  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    maxPasswordLength: 128,
    requireEmailVerification: Boolean(process.env.RESEND_API_KEY),

    sendResetPassword: async ({ user, url }) => {
      await sendReactEmail({
        to: user.email,
        subject: "Reset your password",
        react: ResetPasswordTemplate({ name: user.name ?? undefined, url }),
      });
    },
  },

  emailVerification: {
    sendOnSignUp: true,
    sendOnSignIn: true,
    autoSignInAfterVerification: true,

    sendVerificationEmail: async ({ user, url }) => {
      await sendReactEmail({
        to: user.email,
        subject: "Verify your email",
        react: VerifyEmailTemplate({ name: user.name ?? undefined, url }),
      });
    },
  },
});
```

## Key Patterns

| Pattern | Details |
|---------|---------|
| Auto-enable | `requireEmailVerification: Boolean(process.env.RESEND_API_KEY)` |
| Templates | React Email components (`.tsx` files) |
| Fire-and-forget | `sendReactEmailSafe` for non-critical emails |
| Password rules | min 8, max 128 characters |
| Verification flow | Sign up → email sent → click link → auto sign-in |
| Reset flow | Request → email sent → click link → new password form |
