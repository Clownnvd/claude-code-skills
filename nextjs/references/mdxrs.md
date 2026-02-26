# mdxRs

> This feature is currently experimental and subject to change, it is not recommended for production.

For experimental use with `@next/mdx`. Compiles MDX files using the new Rust compiler.

```js filename="next.config.js"
const withMDX = require('@next/mdx')()

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ['ts', 'tsx', 'mdx'],
  experimental: {
    mdxRs: true,
  },
}

module.exports = withMDX(nextConfig)
```


--------------------------------------------------------------------------------
title: "onDemandEntries"
description: "Configure how Next.js will dispose and keep in memory pages created in development."
source: "https://nextjs.org/docs/app/api-reference/config/next-config-js/onDemandEntries"
--------------------------------------------------------------------------------