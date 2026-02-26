# I

## Import Aliases

Custom path mappings that provide shorthand references for frequently used directories. Import aliases reduce the complexity of relative imports and make code more readable and maintainable. Learn more in [Absolute Imports and Module Path Aliases](/docs/app/getting-started/installation#set-up-absolute-imports-and-module-path-aliases).

## Incremental Static Regeneration (ISR)

A technique that allows you to update static content without rebuilding the entire site. ISR enables you to use static generation on a per-page basis while revalidating pages in the background as traffic comes in. Learn more in the [ISR guide](/docs/app/guides/incremental-static-regeneration).

> **Good to know**: In Next.js, ISR is also known as [Revalidation](#revalidation).

## Intercepting Routes

A routing pattern that allows loading a route from another part of your application within the current layout. Useful for displaying content (like modals) without the user switching context, while keeping the URL shareable. Learn more in [Intercepting Routes](/docs/app/api-reference/file-conventions/intercepting-routes).

## Image Optimization

Automatic image optimization using the [`<Image>` component](/docs/app/api-reference/components/image). Next.js optimizes images on-demand, serves them in modern formats like WebP, and automatically handles lazy loading and responsive sizing. Learn more in [Images](/docs/app/getting-started/images).