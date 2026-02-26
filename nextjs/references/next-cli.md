# next CLI

The Next.js CLI allows you to develop, build, start your application, and more.

Basic usage:

```bash filename="Terminal"
npx next [command] [options]
```

## Reference

The following options are available:

| Options             | Description                        |
| ------------------- | ---------------------------------- |
| `-h` or `--help`    | Shows all available options        |
| `-v` or `--version` | Outputs the Next.js version number |

### Commands

The following commands are available:

| Command                                                      | Description                                                                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| [`dev`](#next-dev-options)                                   | Starts Next.js in development mode with Hot Module Reloading, error reporting, and more.                      |
| [`build`](#next-build-options)                               | Creates an optimized production build of your application. Displaying information about each route.           |
| [`start`](#next-start-options)                               | Starts Next.js in production mode. The application should be compiled with `next build` first.                |
| [`info`](#next-info-options)                                 | Prints relevant details about the current system which can be used to report Next.js bugs.                    |
| [`telemetry`](#next-telemetry-options)                       | Allows you to enable or disable Next.js' completely anonymous telemetry collection.                           |
| [`typegen`](#next-typegen-options)                           | Generates TypeScript definitions for routes, pages, layouts, and route handlers without running a full build. |
| [`upgrade`](#next-upgrade-options)                           | Upgrades your Next.js application to the latest version.                                                      |
| [`experimental-analyze`](#next-experimental-analyze-options) | Analyzes bundle output using Turbopack. Does not produce build artifacts.                                     |

> **Good to know**: Running `next` without a command is an alias for `next dev`.

### `next dev` options

`next dev` starts the application in development mode with Hot Module Reloading (HMR), error reporting, and more. The following options are available when running `next dev`:

| Option                                   | Description                                                                                                                                          |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-h, --help`                             | Show all available options.                                                                                                                          |
| `[directory]`                            | A directory in which to build the application. If not provided, current directory is used.                                                           |
| `--turbopack`                            | Force enable [Turbopack](/docs/app/api-reference/turbopack) (enabled by default). Also available as `--turbo`.                                       |
| `--webpack`                              | Use Webpack instead of the default [Turbopack](/docs/app/api-reference/turbopack) bundler for development.                                           |
| `-p` or `--port <port>`                  | Specify a port number on which to start the application. Default: 3000, env: PORT                                                                    |
| `-H`or `--hostname <hostname>`           | Specify a hostname on which to start the application. Useful for making the application available for other devices on the network. Default: 0.0.0.0 |
| `--experimental-https`                   | Starts the server with HTTPS and generates a self-signed certificate.                                                                                |
| `--experimental-https-key <path>`        | Path to a HTTPS key file.                                                                                                                            |
| `--experimental-https-cert <path>`       | Path to a HTTPS certificate file.                                                                                                                    |
| `--experimental-https-ca <path>`         | Path to a HTTPS certificate authority file.                                                                                                          |
| `--experimental-upload-trace <traceUrl>` | Reports a subset of the debugging trace to a remote HTTP URL.                                                                                        |

### `next build` options

`next build` creates an optimized production build of your application. The output displays information about each route. For example:

```bash filename="Terminal"
Route (app)
┌ ○ /_not-found
└ ƒ /products/[id]

○  (Static)   prerendered as static content
ƒ  (Dynamic)  server-rendered on demand
```

The following options are available for the `next build` command:

| Option                             | Description                                                                                                                                                                        |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-h, --help`                       | Show all available options.                                                                                                                                                        |
| `[directory]`                      | A directory on which to build the application. If not provided, the current directory will be used.                                                                                |
| `--turbopack`                      | Force enable [Turbopack](/docs/app/api-reference/turbopack) (enabled by default). Also available as `--turbo`.                                                                     |
| `--webpack`                        | Build using Webpack.                                                                                                                                                               |
| `-d` or `--debug`                  | Enables a more verbose build output. With this flag enabled additional build output like rewrites, redirects, and headers will be shown.                                           |
|                                    |
| `--profile`                        | Enables production [profiling for React](https://react.dev/reference/react/Profiler).                                                                                              |
| `--no-lint`                        | Disables linting. *Note: linting will be removed from `next build` in Next 16. If you're using Next 15.5+ with a linter other than `eslint`, linting during build will not occur.* |
| `--no-mangling`                    | Disables [mangling](https://en.wikipedia.org/wiki/Name_mangling). This may affect performance and should only be used for debugging purposes.                                      |
| `--experimental-app-only`          | Builds only App Router routes.                                                                                                                                                     |
| `--experimental-build-mode [mode]` | Uses an experimental build mode. (choices: "compile", "generate", default: "default")                                                                                              |
| `--debug-prerender`                | Debug prerender errors in development.                                                                                                                                             |
| `--debug-build-paths=<patterns>`   | Build only specific routes for debugging.                                                                                                                                          |

### `next start` options

`next start` starts the application in production mode. The application should be compiled with [`next build`](#next-build-options) first.

The following options are available for the `next start` command:

| Option                                  | Description                                                                                                     |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `-h` or `--help`                        | Show all available options.                                                                                     |
| `[directory]`                           | A directory on which to start the application. If no directory is provided, the current directory will be used. |
| `-p` or `--port <port>`                 | Specify a port number on which to start the application. (default: 3000, env: PORT)                             |
| `-H` or `--hostname <hostname>`         | Specify a hostname on which to start the application (default: 0.0.0.0).                                        |
| `--keepAliveTimeout <keepAliveTimeout>` | Specify the maximum amount of milliseconds to wait before closing the inactive connections.                     |

### `next info` options

`next info` prints relevant details about the current system which can be used to report Next.js bugs when opening a [GitHub issue](https://github.com/vercel/next.js/issues). This information includes Operating System platform/arch/version, Binaries (Node.js, npm, Yarn, pnpm), package versions (`next`, `react`, `react-dom`), and more.

The output should look like this:

```bash filename="Terminal"
Operating System:
  Platform: darwin
  Arch: arm64
  Version: Darwin Kernel Version 23.6.0
  Available memory (MB): 65536
  Available CPU cores: 10
Binaries:
  Node: 20.12.0
  npm: 10.5.0
  Yarn: 1.22.19
  pnpm: 9.6.0
Relevant Packages:
  next: 15.0.0-canary.115 // Latest available version is detected (15.0.0-canary.115).
  eslint-config-next: 14.2.5
  react: 19.0.0-rc
  react-dom: 19.0.0
  typescript: 5.5.4
Next.js Config:
  output: N/A
```

The following options are available for the `next info` command:

| Option           | Description                                    |
| ---------------- | ---------------------------------------------- |
| `-h` or `--help` | Show all available options                     |
| `--verbose`      | Collects additional information for debugging. |

### `next telemetry` options

Next.js collects **completely anonymous** telemetry data about general usage. Participation in this anonymous program is optional, and you can opt-out if you prefer not to share information.

The following options are available for the `next telemetry` command:

| Option       | Description                             |
| ------------ | --------------------------------------- |
| `-h, --help` | Show all available options.             |
| `--enable`   | Enables Next.js' telemetry collection.  |
| `--disable`  | Disables Next.js' telemetry collection. |

Learn more about [Telemetry](/telemetry).

### `next typegen` options

`next typegen` generates TypeScript definitions for your application's routes without performing a full build. This is useful for IDE autocomplete and CI type-checking of route usage.

Previously, route types were only generated during `next dev` or `next build`, which meant running `tsc --noEmit` directly wouldn't validate your route types. Now you can generate types independently and validate them externally:

```bash filename="Terminal"