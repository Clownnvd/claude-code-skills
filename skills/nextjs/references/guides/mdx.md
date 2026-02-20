# MDX

> Source: https://nextjs.org/docs/app/guides/mdx (v16.1.6)

MDX is a superset of Markdown that lets you write JSX and embed React components in `.mdx` files.

## Setup

```bash
npm install @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```

```typescript
// next.config.mjs
import createMDX from '@next/mdx'

const nextConfig = {
  pageExtensions: ['js', 'jsx', 'md', 'mdx', 'ts', 'tsx'],
}

const withMDX = createMDX({
  // extension: /\.(md|mdx)$/,  // uncomment to also handle .md files
})

export default withMDX(nextConfig)
```

Create `mdx-components.tsx` at project root (**required** for App Router):

```typescript
// mdx-components.tsx
import type { MDXComponents } from 'mdx/types'

export function useMDXComponents(): MDXComponents {
  return {}
}
```

## Rendering MDX

**File-based routing:** Place `page.mdx` in `app/` routes (e.g., `app/mdx-page/page.mdx`).

**Import in a page:**

```typescript
// app/mdx-page/page.tsx
import Welcome from '@/markdown/welcome.mdx'
export default function Page() { return <Welcome /> }
```

**Dynamic imports:**

```typescript
// app/blog/[slug]/page.tsx
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const { default: Post } = await import(`@/content/${slug}.mdx`)
  return <Post />
}
export function generateStaticParams() {
  return [{ slug: 'welcome' }, { slug: 'about' }]
}
export const dynamicParams = false
```

## Custom Components

**Global** -- override HTML elements in `mdx-components.tsx`:

```typescript
import type { MDXComponents } from 'mdx/types'
import Image, { ImageProps } from 'next/image'

const components = {
  h1: ({ children }: { children: React.ReactNode }) => (
    <h1 style={{ fontSize: '48px' }}>{children}</h1>
  ),
  img: (props: ImageProps) => (
    <Image sizes="100vw" style={{ width: '100%', height: 'auto' }} {...props} />
  ),
} satisfies MDXComponents

export function useMDXComponents(): MDXComponents { return components }
```

**Local override** -- pass `components` prop: `<Welcome components={{ h1: CustomH1 }} />`

## Frontmatter

No native YAML frontmatter. Use MDX exports instead:

```mdx
export const metadata = { author: 'John Doe' }
# Blog post
```

```typescript
import BlogPost, { metadata } from '@/content/blog-post.mdx'
```

For YAML: use `remark-frontmatter` or `gray-matter`.

## Plugins

```typescript
// next.config.mjs -- standard (webpack)
const withMDX = createMDX({
  options: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [],
  },
})

// Turbopack -- use string names (no function refs)
const withMDX = createMDX({
  options: {
    remarkPlugins: ['remark-gfm', ['remark-toc', { heading: 'TOC' }]],
    rehypePlugins: ['rehype-slug'],
  },
})
```

## Rust MDX Compiler (Experimental)

```typescript
module.exports = withMDX({
  experimental: { mdxRs: true },  // or { mdxType: 'gfm' | 'commonmark' }
})
```

## Quick Reference

| Item | Detail |
|------|--------|
| Packages | `@next/mdx`, `@mdx-js/loader`, `@mdx-js/react`, `@types/mdx` |
| Required file | `mdx-components.tsx` at project root |
| Page extensions | Add `'md'`, `'mdx'` to `pageExtensions` |
| File routing | `app/route/page.mdx` |
| Frontmatter | Use MDX exports or `remark-frontmatter` |
| Turbopack plugins | Pass plugin names as strings, not imports |
| Rust compiler | `experimental.mdxRs: true` (experimental) |
| Tailwind styling | Use `@tailwindcss/typography` with `prose` classes |
