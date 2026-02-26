# React Email Patterns

Reference for React Email components, templates, rendering, and preview in Next.js 16.

## Base Template Layout

```tsx
// src/emails/components/layout.tsx
import { Html, Head, Body, Container, Text, Hr, Preview, Tailwind } from "@react-email/components";

interface LayoutProps { preview: string; children: React.ReactNode; }

export function EmailLayout({ preview, children }: LayoutProps) {
  return (
    <Html><Head /><Preview>{preview}</Preview>
      <Tailwind>
        <Body className="bg-gray-100 font-sans">
          <Container className="mx-auto max-w-[600px] bg-white p-8">
            {children}
            <Hr className="my-6 border-gray-300" />
            <Text className="text-xs text-gray-500">You received this because you have an account.</Text>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  );
}
```

## Transactional Email Template

```tsx
// src/emails/welcome.tsx
import { Text, Button, Section } from "@react-email/components";
import { EmailLayout } from "./components/layout";

interface WelcomeEmailProps { name: string; loginUrl: string; }

export function WelcomeEmail({ name, loginUrl }: WelcomeEmailProps) {
  return (
    <EmailLayout preview={`Welcome, ${name}!`}>
      <Section>
        <Text className="text-2xl font-bold">Welcome, {name}!</Text>
        <Text>Your account has been created. Get started by logging in.</Text>
        <Button href={loginUrl} className="rounded bg-blue-600 px-6 py-3 text-white">Log In</Button>
      </Section>
    </EmailLayout>
  );
}
WelcomeEmail.PreviewProps = { name: "Jane Doe", loginUrl: "https://example.com/login" } satisfies WelcomeEmailProps;
export default WelcomeEmail;
```

## Rendering Templates

```typescript
import { render } from "@react-email/render";
import { WelcomeEmail } from "@/emails/welcome";

const html = await render(WelcomeEmail({ name: "Jane", loginUrl: "/login" }));
const text = await render(WelcomeEmail({ name: "Jane", loginUrl: "/login" }), { plainText: true });

await resend.emails.send({ from: process.env.EMAIL_FROM!, to: "user@example.com", subject: "Welcome", html, text });
```

## Email Service Layer

```typescript
// src/lib/email.ts
import { render } from "@react-email/render";
import { enqueueEmail } from "@/lib/queue";
import { WelcomeEmail } from "@/emails/welcome";

export async function sendWelcomeEmail(user: { name: string; email: string }) {
  const html = await render(WelcomeEmail({
    name: user.name, loginUrl: `${process.env.NEXT_PUBLIC_APP_URL}/login`,
  }));
  return enqueueEmail({ from: process.env.EMAIL_FROM!, to: user.email, subject: `Welcome, ${user.name}!`, html });
}
```

## Preview Server

Run `npx email dev` to start the React Email preview server at `localhost:3030`.
Each email file must export a default component with optional `PreviewProps`.

## Component Reference

| Component | Use | Component | Use |
|-----------|-----|-----------|-----|
| `Html` | Root wrapper | `Text` | Paragraph text |
| `Head` | Email head | `Link` | Hyperlink |
| `Preview` | Preview text | `Button` | CTA button |
| `Body` | Body wrapper | `Img` | Image (absolute URL) |
| `Container` | Centered wrapper | `Hr` | Horizontal rule |
| `Section` | Content grouping | `Tailwind` | Tailwind CSS wrapper |
| `Row`/`Column` | Grid layout | `CodeInline` | Inline code |
