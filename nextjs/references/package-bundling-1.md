# Package Bundling

@router: Pages Router

Bundling is the process of combining your application code and its dependencies into optimized output files for the client and server. Smaller bundles load faster, reduce JavaScript execution time, improve [Core Web Vitals](https://web.dev/articles/vitals), and lower server cold start times.

Next.js automatically optimizes bundles by code splitting, tree-shaking, and other techniques. However, there are some cases where you may need to optimize your bundles manually.

There are two tools for analyzing your application's bundles:

* [Next.js Bundle Analyzer for Turbopack (experimental)](#nextjs-bundle-analyzer-experimental)
* [`@next/bundle-analyzer` plugin for Webpack](#nextbundle-analyzer-for-webpack)

This guide will walk you through how to use each tool and how to [optimize large bundles](#optimizing-large-bundles).

## Next.js Bundle Analyzer (Experimental)

> Available in v16.1 and later. You can share feedback in the [dedicated GitHub discussion](https://github.com/vercel/next.js/discussions/86731) and view the demo at [turbopack-bundle-analyzer-demo.vercel.sh](https://turbopack-bundle-analyzer-demo.vercel.sh/).

The Next.js Bundle Analyzer is integrated with Turbopack's module graph. You can inspect server and client modules with precise import tracing, making it easier to find large dependencies. Open the interactive Bundle Analyzer demo to explore the module graph.

### Step 1: Run the Turbopack Bundle Analyzer

To get started, run the following command and open up the interactive view in your browser.

```bash filename="Terminal" package="npm"
npx next experimental-analyze
```

```bash filename="Terminal" package="yarn"
yarn next experimental-analyze
```

```bash filename="Terminal" package="pnpm"
pnpm next experimental-analyze
```

```bash filename="Terminal" package="bun"
bunx next experimental-analyze
```

### Step 2: Filter and inspect modules

Within the UI, you can filter by route, environment (client or server), and type (JavaScript, CSS, JSON), or search by file:

### Step 3: Trace modules with import chains

The treemap shows each module as a rectangle. Where the size of the module is represented by the area of the rectangle.

Click a module to see its size, inspect its full import chain and see exactly where it’s used in your application:

![Image description missing](https://h8DxKfmAPhn8O0p3.public.blob.vercel-storage.com/docs/light/bundle-analyzer.png)

### Step 4: Write output to disk for sharing or diffing

If you want to share the analysis with teammates or compare bundle sizes before/after optimizations, you can skip the interactive view and save the analysis as a static file with the `--output` flag:

```bash filename="Terminal" package="npm"
npx next experimental-analyze --output
```

```bash filename="Terminal" package="yarn"
yarn next experimental-analyze --output
```

```bash filename="Terminal" package="pnpm"
pnpm next experimental-analyze --output
```

```bash filename="Terminal" package="bun"
bunx next experimental-analyze --output
```

This command writes the output to `.next/diagnostics/analyze`. You can copy this directory elsewhere to compare results:

```bash filename="Terminal"
cp -r .next/diagnostics/analyze ./analyze-before-refactor
```

> More options are available for the Bundle Analyzer, see Next.js CLI reference docs for the full list.

## `@next/bundle-analyzer` for Webpack

The [`@next/bundle-analyzer`](https://www.npmjs.com/package/@next/bundle-analyzer) is a plugin that helps you manage the size of your application bundles. It generates a visual report of the size of each package and their dependencies. You can use the information to remove large dependencies, split, or [lazy-load](/docs/app/guides/lazy-loading) your code.

### Step 1: Installation

Install the plugin by running the following command:

```bash
npm i @next/bundle-analyzer