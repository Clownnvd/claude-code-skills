# poweredByHeader

@router: Pages Router

By default Next.js will add the `x-powered-by` header. To opt-out of it, open `next.config.js` and disable the `poweredByHeader` config:

```js filename="next.config.js"
module.exports = {
  poweredByHeader: false,
}
```


--------------------------------------------------------------------------------
title: "productionBrowserSourceMaps"
description: "Enables browser source map generation during the production build."
source: "https://nextjs.org/docs/pages/api-reference/config/next-config-js/productionBrowserSourceMaps"
--------------------------------------------------------------------------------