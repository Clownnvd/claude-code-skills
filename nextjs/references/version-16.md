# Version 16

## Upgrading from 15 to 16

### Using AI Agents with Next.js DevTools MCP

If you're using an AI coding assistant that supports the [Model Context Protocol (MCP)](https://modelcontextprotocol.io), you can use the **Next.js DevTools MCP** to automate the upgrade process and migration tasks.

#### Setup

Add the following configuration to your MCP client, for each coding agent you can read [this section](https://github.com/vercel/next-devtools-mcp#mcp-client-configuration) for configuration details.

**example:**

```json filename=".mcp.json"
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

For more information, visit the [`next-devtools-mcp`](https://github.com/vercel/next-devtools-mcp) documentation to configure with your MCP client.

> **Note:** Using `next-devtools-mcp@latest` ensures that your MCP client will always use the latest version of the Next.js DevTools MCP server.

#### Example Prompts

Once configured, you can use natural language prompts to upgrade your Next.js app:

**To upgrade to Next.js 16:**

Connect to your coding agent and then prompt:

```txt
Next Devtools, help me upgrade my Next.js app to version 16
```

**To migrate to Cache Components (after upgrading to v16):**

Connect to your coding agent and then prompt:

```txt
Next Devtools, migrate my Next.js app to cache components
```

Learn more in the documentation [here](/docs/app/guides/mcp).

### Using the Codemod

To update to Next.js version 16, you can use the `upgrade` [codemod](/docs/app/guides/upgrading/codemods#160):

```bash filename="Terminal"
npx @next/codemod@canary upgrade latest
```

The [codemod](/docs/app/guides/upgrading/codemods#160) is able to:

* Update `next.config.js` to use the new `turbopack` configuration
* Migrate from `next lint` to the ESLint CLI
* Migrate from deprecated `middleware` convention to `proxy`
* Remove `unstable_` prefix from stabilized APIs
* Remove `experimental_ppr` Route Segment Config from pages and layouts

If you prefer to do it manually, install the latest Next.js and React versions:

```bash filename="Terminal"
npm install next@latest react@latest react-dom@latest
```

If you are using TypeScript, ensure you also upgrade `@types/react` and `@types/react-dom` to their latest versions.

## Node.js runtime and browser support

| Requirement   | Change / Details                                                   |
| ------------- | ------------------------------------------------------------------ |
| Node.js 20.9+ | Minimum version now `20.9.0` (LTS); Node.js 18 no longer supported |
| TypeScript 5+ | Minimum version now `5.1.0`                                        |
| Browsers      | Chrome 111+, Edge 111+, Firefox 111+, Safari 16.4+                 |

## Turbopack by default

Starting with **Next.js 16**, Turbopack is stable and used by default with `next dev` and `next build`

Previously you had to enable Turbopack using `--turbopack`, or `--turbo`.

```json filename="package.json"
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build --turbopack",
    "start": "next start"
  }
}
```

This is no longer necessary. You can update your `package.json` scripts:

```json filename="package.json"
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

If your project has a [custom `webpack`](/docs/app/api-reference/config/next-config-js/webpack) configuration and you run `next build` (which now uses Turbopack by default), the build will **fail** to prevent misconfiguration issues.

You have a few different ways to address this:

* **Use Turbopack anyway:** Run with `next build --turbopack` to build using Turbopack and ignore your `webpack` config.
* **Switch to Turbopack fully:** Migrate your `webpack` config to Turbopack-compatible options.
* **Keep using Webpack:** Use the `--webpack` flag to opt out of Turbopack and build with Webpack.

> **Good to know**: If you see failing builds because a `webpack` configuration was found, but you don't define one yourself, it is likely that a plugin is adding a `webpack` option

### Opting out of Turbopack

If you need to continue using Webpack, you can opt out with the `--webpack` flag. For example, to use Turbopack in development but Webpack for production builds:

```json filename="package.json"
{
  "scripts": {
    "dev": "next dev",
    "build": "next build --webpack",
    "start": "next start"
  }
}
```

We recommend using Turbopack for development and production. Submit a comment to this [thread](https://github.com/vercel/next.js/discussions/77721), if you are unable to switch to Turbopack.

### Turbopack configuration location

The `experimental.turbopack` configuration is out of experimental.

```ts filename="next.config.ts"
import type { NextConfig } from 'next'

// Next.js 15 - experimental.turbopack
const nextConfig: NextConfig = {
  experimental: {
    turbopack: {
      // options
    },
  },
}

export default nextConfig
```

You can use it as a top-level `turbopack` option:

```ts filename="next.config.ts"
import type { NextConfig } from 'next'

// Next.js 16 - turbopack at the top level of nextConfig
const nextConfig: NextConfig = {
  turbopack: {
    // options
  },
}

export default nextConfig
```

Make sure to review the `Turbopack` configuration [options](/docs/app/api-reference/config/next-config-js/turbopack). **Next.js 16** introduces various improvements and new options, for example:

* [Advanced Webpack loader conditions](/docs/app/api-reference/config/next-config-js/turbopack#advanced-webpack-loader-conditions)
* [debugIds](/docs/app/api-reference/config/next-config-js/turbopack#debug-ids)

### Resolve alias fallback

In some projects, client-side code may import files containing Node.js native modules. This will cause `Module not found: Can't resolve 'fs'` type of errors.

When this happens, you should refactor your code so that your client-side bundles do not reference these Node.js native modules.

However, in some cases, this might not be possible. In Webpack the `resolve.fallback` option was typically used to **silence** the error. Turbopack offers a similar option, using `turbopack.resolveAlias`. In this case, tell Turbopack to load an empty module when `fs` is requested for the browser.

```ts filename="next.config.ts"
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  turbopack: {
    resolveAlias: {
      fs: {
        browser: './empty.ts', // We recommend to fix code imports before using this method
      },
    },
  },
}

export default nextConfig
```

It is preferable to refactor your modules so that client code doesn't ever import from modules using Node.js native modules.

### Sass node\_modules imports

Turbopack fully supports importing Sass files from `node_modules`. Note that while Webpack allowed the legacy tilde (`~`) prefix, Turbopack does not support this syntax.

In Webpack:

```scss filename="styles/globals.scss"
@import '~bootstrap/dist/css/bootstrap.min.css';
```

In Turbopack:

```scss filename="styles/globals.scss"
@import 'bootstrap/dist/css/bootstrap.min.css';
```

If changing the imports is not possible, you can use `turbopack.resolveAlias`. For example:

```ts filename="next.config.ts"
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  turbopack: {
    resolveAlias: {
      '~*': '*',
    },
  },
}

export default nextConfig
```

### Turbopack File System Caching (beta)

Turbopack now supports filesystem caching in development, storing compiler artifacts on disk between runs for significantly faster compile times across restarts.

Enable filesystem caching in your configuration:

```ts filename="next.config.ts" switcher
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    turbopackFileSystemCacheForDev: true,
  },
}

export default nextConfig
```

```js filename="next.config.js" switcher
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    turbopackFileSystemCacheForDev: true,
  },
}

module.exports = nextConfig
```

## Async Request APIs (Breaking change)

Version 15 introduced [Async Request APIs](https://nextjs.org/docs/app/guides/upgrading/version-15#async-request-apis-breaking-change) as a breaking change, with **temporary** synchronous compatibility.

Starting with **Next.js 16**, synchronous access is fully removed. These APIs can only be accessed asynchronously.

* [`cookies`](/docs/app/api-reference/functions/cookies)
* [`headers`](/docs/app/api-reference/functions/headers)
* [`draftMode`](/docs/app/api-reference/functions/draft-mode)
* `params` in [`layout.js`](/docs/app/api-reference/file-conventions/layout), [`page.js`](/docs/app/api-reference/file-conventions/page), [`route.js`](/docs/app/api-reference/file-conventions/route), [`default.js`](/docs/app/api-reference/file-conventions/default), [`opengraph-image`](/docs/app/api-reference/file-conventions/metadata/opengraph-image#opengraph-image), [`twitter-image`](/docs/app/api-reference/file-conventions/metadata/opengraph-image#twitter-image), [`icon`](/docs/app/api-reference/file-conventions/metadata/app-icons#icon), and [`apple-icon`](/docs/app/api-reference/file-conventions/metadata/app-icons#apple-icon).
* `searchParams` in [`page.js`](/docs/app/api-reference/file-conventions/page)

Use the [codemod](/docs/app/guides/upgrading/codemods#migrate-to-async-dynamic-apis) to migrate to async Dynamic APIs.

### Migrating types for async Dynamic APIs

To help migrate to async `params` and `searchParams`, you can run [`npx next typegen`](/docs/app/api-reference/cli/next#next-typegen-options) to automatically generate these globally available types helpers:

* [`PageProps`](/docs/app/api-reference/file-conventions/page#page-props-helper)
* [`LayoutProps`](/docs/app/api-reference/file-conventions/layout#layout-props-helper)
* [`RouteContext`](/docs/app/api-reference/file-conventions/route#route-context-helper)

> **Good to know**: `typegen` was introduced in Next.js 15.5

This simplifies type-safe migration to the new async API pattern, and enables you to update your components with full type safety, for example:

```tsx filename="/app/blog/[slug]/page.tsx"
export default async function Page(props: PageProps<'/blog/[slug]'>) {
  const { slug } = await props.params
  const query = await props.searchParams
  return <h1>Blog Post: {slug}</h1>
}
```

This approach gives you fully type-safe access to `props.params`, including the `slug`, and to `searchParams`, directly within your page.

## Async parameters for icon, and open-graph Image (Breaking change)

> The props passed to the image generating functions in `opengraph-image`, `twitter-image`, `icon`, and `apple-icon`, are now Promises.

In previous versions, both the `Image` (image generation function), and the `generateImageMetadata` received a `params` object. The `id` returned by `generateImageMetadata` was passed as a string to the image generation function.

```js filename="app/shop/[slug]/opengraph-image.js"
// Next.js 15 - synchronous params access
export function generateImageMetadata({ params }) {
  const { slug } = params
  return [{ id: '1' }, { id: '2' }]
}

// Next.js 15 - synchronous params and id access
export default function Image({ params, id }) {
  const slug = params.slug
  const imageId = id // string
  // ...
}
```

Starting with **Next.js 16**, to align with the [Async Request APIs](#async-request-apis-breaking-change) change, the image generating function now receives `params` and `id` as promises. The `generateImageMetadata` function continues to receive synchronous `params`.

```js filename="app/shop/[slug]/opengraph-image.js"
export async function generateImageMetadata({ params }) {
  const { slug } = params
  return [{ id: '1' }, { id: '2' }]
}

// Next.js 16 - asynchronous params and id access
export default async function Image({ params, id }) {
  const { slug } = await params // params now async
  const imageId = await id // id is now Promise<string> when using generateImageMetadata
  // ...
}
```

## Async `id` parameter for `sitemap` (Breaking change)

Previously, the `id` values returned from [`generateSitemaps`](/docs/app/api-reference/functions/generate-sitemaps) were passed directly to the `sitemap` generating function.

```js filename="app/product/sitemap.js"
export async function generateSitemaps() {
  return [{ id: 0 }, { id: 1 }, { id: 2 }, { id: 3 }]
}

// Next.js 15 - synchronous id access
export default async function sitemap({ id }) {
  const start = id * 50000 // id is a number
  // ...
}
```

Starting with **Next.js 16**, the `sitemap` generating function now receives `id` as a promise.

```js filename="app/product/sitemap.js"
export async function generateSitemaps() {
  return [{ id: 0 }, { id: 1 }, { id: 2 }, { id: 3 }]
}

// Next.js 16 - asynchronous id access
export default async function sitemap({ id }) {
  const resolvedId = await id // id is now Promise<string>
  const start = Number(resolvedId) * 50000
  // ...
}
```

## React 19.2

The App Router in **Next.js 16** uses the latest React [Canary release](https://react.dev/blog/2023/05/03/react-canaries), which includes the newly released React 19.2 features and other features being incrementally stabilized. Highlights include:

* **[View Transitions](https://react.dev/reference/react/ViewTransition)**: Animate elements that update inside a Transition or navigation
* **[`useEffectEvent`](https://react.dev/reference/react/useEffectEvent)**: Extract non-reactive logic from Effects into reusable Effect Event functions
* **[Activity](https://react.dev/reference/react/Activity)**: Render "background activity" by hiding UI with `display: none` while maintaining state and cleaning up Effects

Learn more in the [React 19.2 announcement](https://react.dev/blog/2025/10/01/react-19-2).

## React Compiler Support

Built-in support for the React Compiler is now stable in **Next.js 16** following the React Compiler's 1.0 release. The React Compiler automatically memoizes components, reducing unnecessary re-renders with zero manual code changes.

The `reactCompiler` configuration option has been promoted from `experimental` to stable. It is not enabled by default as we continue gathering build performance data across different application types.

```ts filename="next.config.ts" switcher
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactCompiler: true,
}

export default nextConfig
```

```js filename="next.config.js" switcher
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactCompiler: true,
}

module.exports = nextConfig
```

Install the latest version of the React Compiler plugin:

```bash filename="Terminal"
npm install -D babel-plugin-react-compiler
```

> **Good to know:** Expect compile times in development and during builds to be higher when enabling this option as the React Compiler relies on Babel.

## Caching APIs

### revalidateTag

[`revalidateTag`](/docs/app/api-reference/functions/revalidateTag) has a new function signature. You can pass a [`cacheLife`](/docs/app/api-reference/functions/cacheLife#reference) profile as the second argument.

```ts filename="app/actions.ts" switcher
'use server'

import { revalidateTag } from 'next/cache'

export async function updateArticle(articleId: string) {
  // Mark article data as stale - article readers see stale data while it revalidates
  revalidateTag(`article-${articleId}`, 'max')
}
```

```js filename="app/actions.js" switcher
'use server'

import { revalidateTag } from 'next/cache'

export async function updateArticle(articleId) {
  // Mark article data as stale - article readers see stale data while it revalidates
  revalidateTag(`article-${articleId}`, 'max')
}
```

Use `revalidateTag` for content where a slight delay in updates is acceptable, such as blog posts, product catalogs, or documentation. Users receive stale content while fresh data loads in the background.

### updateTag

[`updateTag`](/docs/app/api-reference/functions/updateTag) is a new [Server Actions](/docs/app/getting-started/updating-data#what-are-server-functions)-only API that provides **read-your-writes** semantics, where a user makes a change and the UI immediately shows the change, rather than stale data.

It does this by expiring and immediately refreshing data within the same request.

```ts filename="app/actions.ts" switcher
'use server'

import { updateTag } from 'next/cache'

export async function updateUserProfile(userId: string, profile: Profile) {
  await db.users.update(userId, profile)

  // Expire cache and refresh immediately - user sees their changes right away
  updateTag(`user-${userId}`)
}
```

```js filename="app/actions.js" switcher
'use server'

import { updateTag } from 'next/cache'

export async function updateUserProfile(userId, profile) {
  await db.users.update(userId, profile)

  // Expire cache and refresh immediately - user sees their changes right away
  updateTag(`user-${userId}`)
}
```

This ensures interactive features reflect changes immediately. Perfect for forms, user settings, and any workflow where users expect to see their updates instantly.

Learn more about when to use `updateTag` or `revalidateTag` [here](/docs/app/api-reference/functions/updateTag#when-to-use-updatetag).

### refresh

[`refresh`](/docs/app/api-reference/functions/refresh) allows you to refresh the client router from within a Server Action.

```ts filename="app/actions.ts" switcher
'use server'

import { refresh } from 'next/cache'

export async function markNotificationAsRead(notificationId: string) {
  // Update the notification in the database
  await db.notifications.markAsRead(notificationId)

  // Refresh the notification count displayed in the header
  refresh()
}
```

```js filename="app/actions.js" switcher
'use server'

import { refresh } from 'next/cache'

export async function markNotificationAsRead(notificationId) {
  // Update the notification in the database
  await db.notifications.markAsRead(notificationId)

  // Refresh the notification count displayed in the header
  refresh()
}
```

Use it when you need to refresh the client router after performing an action.

### cacheLife and cacheTag

[`cacheLife`](/docs/app/api-reference/functions/cacheLife) and [`cacheTag`](/docs/app/api-reference/functions/cacheTag) are now stable. The `unstable_` prefix is no longer needed.

Wherever you had aliased imports like:

```ts
import {
  unstable_cacheLife as cacheLife,
  unstable_cacheTag as cacheTag,
} from 'next/cache'
```

You can update your imports to:

```ts
import { cacheLife, cacheTag } from 'next/cache'
```

## Enhanced Routing and Navigation

**Next.js 16** includes a complete overhaul of the routing and navigation system, making page transitions leaner and faster. This optimizes how Next.js prefetches and caches navigation data:

* **Layout deduplication**: When prefetching multiple URLs with a shared layout, the layout is downloaded once.
* **Incremental prefetching**: Next.js only prefetches parts not already in cache, rather than entire pages.

These changes require **no code modifications** and are designed to improve performance across all apps.

However, you may see more individual prefetch requests with much lower total transfer sizes. We believe this is the right trade-off for nearly all applications.

If the increased request count causes issues, please let us know by creating an [issue](https://github.com/vercel/next.js/issues) or [discussion](https://github.com/vercel/next.js/discussions) item.

## Partial Pre-Rendering (PPR)

**Next.js 16** removes the experimental **Partial Pre-Rendering (PPR)** flag and configuration options, including the route level segment `experimental_ppr`.

Starting with **Next.js 16**, you can opt into PPR using the [`cacheComponents`](/docs/app/api-reference/config/next-config-js/cacheComponents) configuration.

```js filename="next.config.js"
/** @type {import('next').NextConfig} */
const nextConfig = {
  cacheComponents: true,
}

module.exports = nextConfig
```

PPR in **Next.js 16** works differently than in **Next.js 15** canaries. If you are using PPR today, stay in the current Next.js 15 canary you are using. We will follow up with a guide to migrate to Cache Components.

```js filename="next.config.js"
/** @type {import('next').NextConfig} */
const nextConfig = {
  // If you are using PPR today
  // stay in the current Next.js 15 canary
  experimental: {
    ppr: true,
  },
}

module.exports = nextConfig
```

## `middleware` to `proxy`

The `middleware` filename is deprecated, and has been renamed to `proxy` to clarify network boundary and routing focus.

The `edge` runtime is **NOT** supported in `proxy`. The `proxy` runtime is `nodejs`, and it cannot be configured. If you want to continue using the `edge` runtime, keep using `middleware`. We will follow up on a minor release with further `edge` runtime instructions.

```bash filename="Terminal"