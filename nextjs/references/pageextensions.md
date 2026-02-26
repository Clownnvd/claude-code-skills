# pageExtensions

By default, Next.js accepts files with the following extensions: `.tsx`, `.ts`, `.jsx`, `.js`. This can be modified to allow other extensions like markdown (`.md`, `.mdx`).

```js filename="next.config.js"
const withMDX = require('@next/mdx')()

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'md', 'mdx'],
}

module.exports = withMDX(nextConfig)
```


--------------------------------------------------------------------------------
title: "poweredByHeader"
description: "Next.js will add the `x-powered-by` header by default. Learn to opt-out of it here."
source: "https://nextjs.org/docs/app/api-reference/config/next-config-js/poweredByHeader"
--------------------------------------------------------------------------------