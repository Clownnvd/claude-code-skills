# distDir

@router: Pages Router

You can specify a name to use for a custom build directory to use instead of `.next`.

Open `next.config.js` and add the `distDir` config:

```js filename="next.config.js"
module.exports = {
  distDir: 'build',
}
```

Now if you run `next build` Next.js will use `build` instead of the default `.next` folder.

> `distDir` **should not** leave your project directory. For example, `../build` is an **invalid** directory.


--------------------------------------------------------------------------------
title: "env"
description: "Learn to add and access environment variables in your Next.js application at build time."
source: "https://nextjs.org/docs/pages/api-reference/config/next-config-js/env"
--------------------------------------------------------------------------------