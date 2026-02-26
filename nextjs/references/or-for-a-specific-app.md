# or for a specific app
next typegen ./apps/web
```

Additionally, `next typegen` generates a `next-env.d.ts` file. We recommend adding `next-env.d.ts` to your `.gitignore` file.

The `next-env.d.ts` file is included into your `tsconfig.json` file, to make Next.js types available to your project.

To ensure `next-env.d.ts` is present before type-checking run `next typegen`. The commands `next dev` and `next build` also generate the `next-env.d.ts` file, but it is often undesirable to run these just to type-check, for example in CI/CD environments.

> **Good to know**: `next typegen` loads your Next.js config (`next.config.js`, `next.config.mjs`, or `next.config.ts`) using the production build phase. Ensure any required environment variables and dependencies are available so the config can load correctly.

### `next upgrade` options

`next upgrade` upgrades your Next.js application to the latest version.

The following options are available for the `next upgrade` command:

| Option                  | Description                                                                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-h, --help`            | Show all available options.                                                                                                                        |
| `[directory]`           | A directory with the Next.js application to upgrade. If not provided, the current directory will be used.                                          |
| `--revision <revision>` | Specify a Next.js version or tag to upgrade to (e.g., `latest`, `canary`, `15.0.0`). Defaults to the release channel you have currently installed. |
| `--verbose`             | Show verbose output during the upgrade process.                                                                                                    |

### `next experimental-analyze` options

`next experimental-analyze` analyzes your application's bundle output using [Turbopack](/docs/app/api-reference/turbopack). This command helps you understand the size and composition of your bundles, including JavaScript, CSS, and other assets. This command doesn't produce an application build.

```bash filename="Terminal"
npx next experimental-analyze
```

By default, the command starts a local server after analysis completes, allowing you to explore your bundle composition in the browser. The analyzer lets you:

* Filter bundles by route and switch between client and server views
* View the full import chain showing why a module is included
* Trace imports across server-to-client component boundaries and dynamic imports

See [Package Bundling](/docs/app/guides/package-bundling#optimizing-large-bundles) for optimization strategies.

To write the analysis output to disk without starting the server, use the `--output` flag. The output is written to `.next/diagnostics/analyze` and contains static files that can be copied elsewhere or shared with others:

```bash filename="Terminal"