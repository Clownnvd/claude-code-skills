# M

## Module Graph

A graph of file dependencies in your app. Each file (module) is a node, and import/export relationships form the edges. Next.js analyzes this graph to determine optimal bundling and code-splitting strategies. Learn more in [Server and Client Components](/docs/app/getting-started/server-and-client-components#reducing-js-bundle-size).

## Metadata

Information about a page used by browsers and search engines, such as title, description, and Open Graph images. In Next.js, define metadata using the [`metadata` export](/docs/app/api-reference/functions/generate-metadata) or [`generateMetadata` function](/docs/app/api-reference/functions/generate-metadata) in layout or page files. Learn more in [Metadata and OG Images](/docs/app/getting-started/metadata-and-og-images).

## Memoization

Caching the return value of a function so that calling the same function multiple times during a render pass (request) only executes it once. In Next.js, fetch requests with the same URL and options are automatically memoized. Learn more about [React Cache](https://react.dev/reference/react/cache).

## Middleware

See [Proxy](#proxy).