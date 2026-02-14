# Fix Patterns: Email Templates & Rendering + Testing & Preview

## Pattern 1: Raw HTML Instead of React Email Components

**Issue**: Hardcoded HTML strings with no component system. **Category**: Templates (12%)

### Before
```typescript
await resend.emails.send({
  from: process.env.EMAIL_FROM!, to: user.email, subject: "Welcome",
  html: `<html><body><h1>Welcome ${user.name}</h1><p>Click <a href="${url}">here</a></p></body></html>`,
});
```

### After
```tsx
// src/emails/components/layout.tsx
import { Html, Head, Body, Container, Preview, Tailwind, Hr, Text } from "@react-email/components";
interface LayoutProps { preview: string; children: React.ReactNode; }
export function EmailLayout({ preview, children }: LayoutProps) {
  return (
    <Html><Head /><Preview>{preview}</Preview>
      <Tailwind><Body className="bg-gray-100 font-sans">
        <Container className="mx-auto max-w-[600px] bg-white p-8">
          {children}
          <Hr className="my-6 border-gray-300" />
          <Text className="text-xs text-gray-500">You received this because you have an account.</Text>
        </Container>
      </Body></Tailwind>
    </Html>);
}

// src/emails/welcome.tsx
import { Text, Button, Section } from "@react-email/components";
import { EmailLayout } from "./components/layout";
interface WelcomeEmailProps { name: string; loginUrl: string; }
export function WelcomeEmail({ name, loginUrl }: WelcomeEmailProps) {
  return (
    <EmailLayout preview={`Welcome, ${name}!`}><Section>
      <Text className="text-2xl font-bold">Welcome, {name}!</Text>
      <Text>Your account has been created.</Text>
      <Button href={loginUrl} className="rounded bg-blue-600 px-6 py-3 text-white">Log In</Button>
    </Section></EmailLayout>);
}
WelcomeEmail.PreviewProps = { name: "Jane", loginUrl: "https://example.com/login" } satisfies WelcomeEmailProps;
export default WelcomeEmail;

// Usage: render() for HTML + plain text
const html = await render(WelcomeEmail({ name, loginUrl }));
const text = await render(WelcomeEmail({ name, loginUrl }), { plainText: true });
```
**Verification**: All emails use React Email components. `render()` called for HTML + plain text.

---

## Pattern 2: No Responsive Design

**Issue**: Fixed pixel widths break on mobile. **Category**: Templates (12%)

### Before
```tsx
<div style={{ width: "800px" }}><table style={{ width: "100%" }}>...</table></div>
```

### After
```tsx
import { Container, Section, Row, Column, Text, Tailwind } from "@react-email/components";
<Tailwind><Container className="mx-auto max-w-[600px] bg-white p-4">
  <Section>{items.map((item) => (
    <Row key={item.id} className="border-b border-gray-200 py-2">
      <Column className="w-3/4"><Text>{item.name}</Text></Column>
      <Column className="w-1/4 text-right"><Text>${item.price}</Text></Column>
    </Row>
  ))}</Section>
</Container></Tailwind>
```
**Verification**: `Container` max-width set. `Tailwind` wrapper present. No fixed widths > 600px.

---

## Pattern 3: No Template Tests or Preview

**Issue**: No automated tests. No preview props. **Category**: Testing & Preview (6%)

### After
```typescript
// src/emails/__tests__/welcome.test.ts
import { render } from "@react-email/render";
import { WelcomeEmail } from "../welcome";

describe("WelcomeEmail", () => {
  it("renders HTML with user name", async () => {
    const html = await render(WelcomeEmail({ name: "Jane", loginUrl: "https://example.com" }));
    expect(html).toContain("Welcome, Jane!");
    expect(html).toContain("https://example.com");
  });
  it("renders plain text version", async () => {
    const text = await render(WelcomeEmail({ name: "Jane", loginUrl: "https://example.com" }), { plainText: true });
    expect(text).toContain("Welcome, Jane!");
  });
  it("has PreviewProps", () => { expect(WelcomeEmail.PreviewProps).toBeDefined(); });
});
```
**Verification**: `pnpm test` passes. Each template has render test. `PreviewProps` defined.
