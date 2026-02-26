# L

## Layout

UI that is shared between multiple pages. Layouts preserve state, remain interactive, and do not re-render on navigation. Defined by exporting a React component from a [`layout.js` file](/docs/app/api-reference/file-conventions/layout). Learn more in [Layouts and Pages](/docs/app/getting-started/layouts-and-pages).

## Loading UI

Fallback UI shown while a [route segment](#route-segment) is loading. Created by adding a [`loading.js` file](/docs/app/api-reference/file-conventions/loading) to a folder, which automatically wraps the page in a [Suspense boundary](#suspense-boundary). Learn more in [Loading UI](/docs/app/api-reference/file-conventions/loading).