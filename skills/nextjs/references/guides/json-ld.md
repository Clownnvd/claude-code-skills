# JSON-LD Structured Data

> Source: https://nextjs.org/docs/app/guides/json-ld (v16.1.6)

JSON-LD is a structured data format used by search engines and AI to understand page content (products, events, organizations, etc.).

## Implementation

Render as a `<script type="application/ld+json">` tag in `layout.tsx` or `page.tsx`. **Sanitize** `<` characters to prevent XSS:

```typescript
// app/products/[id]/page.tsx
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const product = await getProduct(id)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    image: product.image,
    description: product.description,
  }

  return (
    <section>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c'),
        }}
      />
      {/* page content */}
    </section>
  )
}
```

## TypeScript Typing with `schema-dts`

```typescript
import { Product, WithContext } from 'schema-dts'

const jsonLd: WithContext<Product> = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: 'Next.js Sticker',
  image: 'https://nextjs.org/imgs/sticker.png',
  description: 'Dynamic at the speed of static.',
}
```

## Quick Reference

| Item | Detail |
|------|--------|
| Format | `<script type="application/ld+json">` |
| Location | `layout.tsx` or `page.tsx` (Server Components) |
| XSS prevention | `.replace(/</g, '\\u003c')` on `JSON.stringify` output |
| TypeScript types | `schema-dts` package (`WithContext<Product>`) |
| Alternative sanitizer | `serialize-javascript` package |
| Validation tools | [Rich Results Test](https://search.google.com/test/rich-results), [Schema Markup Validator](https://validator.schema.org/) |
