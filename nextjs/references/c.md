# C

## Cache Components

A feature that enables component and function-level caching using the [`"use cache"` directive](/docs/app/api-reference/directives/use-cache). Cache Components allows you to mix static, cached, and dynamic content within a single route by prerendering a static HTML shell that's served immediately, while dynamic content streams in when ready. Configure cache duration with [`cacheLife()`](/docs/app/api-reference/functions/cacheLife), tag cached data with [`cacheTag()`](/docs/app/api-reference/functions/cacheTag), and invalidate on-demand with [`updateTag()`](/docs/app/api-reference/functions/updateTag). Learn more in the [Cache Components guide](/docs/app/getting-started/cache-components).

## Catch-all Segments

Dynamic route segments that can match multiple URL parts using the `[...folder]/page.js` syntax. These segments capture all remaining URL segments and are useful for implementing features like documentation sites or file browsers. Learn more in [Dynamic Route Segments](/docs/app/api-reference/file-conventions/dynamic-routes#catch-all-segments).

## Client Bundles

JavaScript bundles sent to the browser. Next.js splits these automatically based on the [module graph](#module-graph) to reduce initial payload size and load only the necessary code for each page.

## Client Component

A React component that runs in the browser. In Next.js, Client Components can also be rendered on the server during initial page generation. They can use state, effects, event handlers, and browser APIs, and are marked with the [`"use client"` directive](#use-client-directive) at the top of a file. Learn more in [Server and Client Components](/docs/app/getting-started/server-and-client-components).

## Client-side navigation

A navigation technique where the page content updates dynamically without a full page reload. Next.js uses client-side navigation with the [`<Link>` component](/docs/app/api-reference/components/link), keeping shared layouts interactive and preserving browser state. Learn more in [Linking and Navigating](/docs/app/getting-started/linking-and-navigating#client-side-transitions).

## Code Splitting

The process of dividing your application into smaller JavaScript chunks based on routes. Instead of loading all code upfront, only the code needed for the current route is loaded, reducing initial load time. Next.js automatically performs code splitting based on routes. Learn more in the [Package Bundling guide](/docs/app/guides/package-bundling).