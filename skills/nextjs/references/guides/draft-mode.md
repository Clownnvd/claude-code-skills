# Draft Mode

> Source: https://nextjs.org/docs/app/guides/draft-mode (v16.1.6)

Draft Mode lets you preview draft content from a headless CMS without rebuilding. It switches static pages to dynamic rendering and sets a `__prerender_bypass` cookie.

## Step 1: Create Route Handler

```ts
// app/api/draft/route.ts
import { draftMode } from 'next/headers'
import { redirect } from 'next/navigation'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const secret = searchParams.get('secret')
  const slug = searchParams.get('slug')

  // Validate secret token and slug
  if (secret !== process.env.DRAFT_SECRET || !slug) {
    return new Response('Invalid token', { status: 401 })
  }

  // Verify slug exists in CMS
  const post = await getPostBySlug(slug)
  if (!post) {
    return new Response('Invalid slug', { status: 401 })
  }

  // Enable draft mode (sets cookie)
  const draft = await draftMode()
  draft.enable()

  // Redirect to the fetched post path (not raw slug -- prevents open redirect)
  redirect(post.slug)
}
```

## Step 2: Configure CMS Draft URL

Set your CMS draft URL to:

```
https://<your-site>/api/draft?secret=<token>&slug=<path>
```

## Step 3: Read Draft State in Pages

```tsx
// app/page.tsx
import { draftMode } from 'next/headers'

async function getData() {
  const { isEnabled } = await draftMode()
  const url = isEnabled
    ? 'https://draft.example.com'
    : 'https://production.example.com'
  const res = await fetch(url)
  return res.json()
}

export default async function Page() {
  const { title, desc } = await getData()
  return (
    <main>
      <h1>{title}</h1>
      <p>{desc}</p>
    </main>
  )
}
```

## API Summary

| Method | Description |
|---|---|
| `draftMode()` | Returns draft mode object (must `await`) |
| `draft.enable()` | Enables draft mode, sets `__prerender_bypass` cookie |
| `draft.disable()` | Disables draft mode, removes cookie |
| `draft.isEnabled` | `boolean` -- whether draft mode is active |

## How It Works

| Step | Detail |
|---|---|
| 1. Visit `/api/draft?secret=...&slug=...` | Route handler validates secret + slug |
| 2. Cookie set | `__prerender_bypass` cookie enables draft mode |
| 3. Page renders dynamically | `isEnabled = true`, fetches draft data |
| 4. Disable | Call `draft.disable()` or clear cookie |

## Security Notes

- Use a secret token known only to your app and CMS
- Always validate the slug against your data source before redirecting
- Redirect to the fetched post path, not raw `searchParams.slug` (prevents open redirect)

## Quick Reference

| Task | How |
|---|---|
| Enable draft mode | `(await draftMode()).enable()` |
| Disable draft mode | `(await draftMode()).disable()` |
| Check if drafting | `(await draftMode()).isEnabled` |
| Draft URL format | `/api/draft?secret=TOKEN&slug=/path` |
| Cookie name | `__prerender_bypass` |
| Rendering behavior | Switches from static to dynamic when enabled |
