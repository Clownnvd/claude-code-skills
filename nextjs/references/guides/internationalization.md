# Internationalization

> Source: https://nextjs.org/docs/app/guides/internationalization (v16.1.6)

Next.js supports multiple languages via locale-based routing and content localization.

## Locale Detection (Middleware/Proxy)

Use `@formatjs/intl-localematcher` and `negotiator` to detect locale from `Accept-Language` header:

```typescript
// proxy.ts
import { match } from '@formatjs/intl-localematcher'
import Negotiator from 'negotiator'
import { NextResponse } from 'next/server'

const locales = ['en-US', 'nl-NL', 'nl']
const defaultLocale = 'en-US'

function getLocale(request: Request): string {
  const headers = { 'accept-language': request.headers.get('accept-language') ?? '' }
  const languages = new Negotiator({ headers }).languages()
  return match(languages, locales, defaultLocale)
}

export function proxy(request: Request) {
  const { pathname } = new URL(request.url)
  const hasLocale = locales.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  )
  if (hasLocale) return

  const locale = getLocale(request)
  const url = new URL(`/${locale}${pathname}`, request.url)
  return NextResponse.redirect(url)
}
```

## Route Structure

Nest all files under `app/[lang]/`:

```
app/
  [lang]/
    layout.tsx
    page.tsx
    dictionaries.ts
    dictionaries/
      en.json
      nl.json
```

### Page with Locale Param

```typescript
// app/[lang]/page.tsx
export default async function Page({ params }: PageProps<'/[lang]'>) {
  const { lang } = await params
  return <div>Locale: {lang}</div>
}
```

## Dictionary-Based Localization

```typescript
// app/[lang]/dictionaries.ts
import 'server-only'

const dictionaries = {
  en: () => import('./dictionaries/en.json').then((m) => m.default),
  nl: () => import('./dictionaries/nl.json').then((m) => m.default),
}

export type Locale = keyof typeof dictionaries

export const hasLocale = (locale: string): locale is Locale =>
  locale in dictionaries

export const getDictionary = async (locale: Locale) => dictionaries[locale]()
```

### Using in a Page

```typescript
// app/[lang]/page.tsx
import { notFound } from 'next/navigation'
import { getDictionary, hasLocale } from './dictionaries'

export default async function Page({ params }: PageProps<'/[lang]'>) {
  const { lang } = await params
  if (!hasLocale(lang)) notFound()
  const dict = await getDictionary(lang)
  return <button>{dict.products.cart}</button>
}
```

## Static Rendering

```typescript
// app/[lang]/layout.tsx
export async function generateStaticParams() {
  return [{ lang: 'en-US' }, { lang: 'de' }]
}

export default async function RootLayout({
  children, params,
}: LayoutProps<'/[lang]'>) {
  return (
    <html lang={(await params).lang}>
      <body>{children}</body>
    </html>
  )
}
```

## Quick Reference

| Item | Detail |
|------|--------|
| Strategy | Sub-path (`/fr/products`) or domain (`my-site.fr/products`) |
| Detection | `negotiator` + `@formatjs/intl-localematcher` |
| Route pattern | `app/[lang]/page.tsx` |
| Type helpers | `PageProps<'/[lang]'>`, `LayoutProps<'/[lang]'>` |
| Dictionary | Server-only dynamic imports, no client bundle impact |
| Validation | `hasLocale()` guard + `notFound()` |
| Libraries | `next-intl`, `next-international`, `lingui`, `paraglide-next` |
