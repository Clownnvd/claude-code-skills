# bundlePagesRouterDependencies

@router: Pages Router

Enable automatic server-side dependency bundling for Pages Router applications. Matches the automatic dependency bundling in App Router.

```js filename="next.config.js"
/** @type {import('next').NextConfig} */
const nextConfig = {
  bundlePagesRouterDependencies: true,
}

module.exports = nextConfig
```

Explicitly opt-out certain packages from being bundled using the [`serverExternalPackages`](/docs/pages/api-reference/config/next-config-js/serverExternalPackages) option.

## Version History

| Version   | Changes                                                                                                   |
| --------- | --------------------------------------------------------------------------------------------------------- |
| `v15.0.0` | Moved from experimental to stable. Renamed from `bundlePagesExternals` to `bundlePagesRouterDependencies` |


--------------------------------------------------------------------------------
title: "compress"
description: "Next.js provides gzip compression to compress rendered content and static files, it only works with the server target. Learn more about it here."
source: "https://nextjs.org/docs/pages/api-reference/config/next-config-js/compress"
--------------------------------------------------------------------------------