# S

## Server Component

The default component type in the App Router. Server Components render on the server, can fetch data directly, and don't add to the client JavaScript bundle. They cannot use state or browser APIs. Learn more in [Server and Client Components](/docs/app/getting-started/server-and-client-components).

## Server Action

A [Server Function](#server-function) that is passed to a Client Component as a prop or bound to a form action. Server Actions are commonly used for form submissions and data mutations. Learn more in [Server Actions and Mutations](/docs/app/getting-started/updating-data).

## Server Function

An asynchronous function that runs on the server, marked with the [`"use server"` directive](/docs/app/api-reference/directives/use-server). Server Functions can be invoked from Client Components. When passed as a prop to a Client Component or bound to a form action, they are called [Server Actions](#server-action). Learn more in [React Server Functions](https://react.dev/reference/rsc/server-functions).

## Static Export

A deployment mode that generates a fully static site with HTML, CSS, and JavaScript files. Enabled by setting `output: 'export'` in `next.config.js`. Static exports can be hosted on any static file server without a Node.js server. Learn more in [Static Exports](/docs/app/guides/static-exports).

## Static rendering

See [Prerendering](#prerendering).

## Static Assets

Files such as images, fonts, videos, and other media that are served directly without processing. Static assets are typically stored in the `public` directory and referenced by their relative paths. Learn more in [Static Assets](/docs/app/api-reference/file-conventions/public-folder).

## Static Shell

The prerendered HTML structure of a page that's served immediately to the browser. With [Partial Prerendering](#partial-prerendering-ppr), the static shell includes all statically renderable content plus [Suspense boundary](#suspense-boundary) fallbacks for dynamic content that streams in later.

## Streaming

A technique that allows the server to send parts of a page to the client as they become ready, rather than waiting for the entire page to render. Enabled automatically with [`loading.js`](/docs/app/api-reference/file-conventions/loading) or manual `<Suspense>` boundaries. Learn more in [Linking and Navigating - Streaming](/docs/app/getting-started/linking-and-navigating#streaming).

## Suspense boundary

A React [`<Suspense>`](https://react.dev/reference/react/Suspense) component that wraps async content and displays fallback UI while it loads. In Next.js, Suspense boundaries define where the [static shell](#static-shell) ends and [streaming](#streaming) begins, enabling [Partial Prerendering](#partial-prerendering-ppr).