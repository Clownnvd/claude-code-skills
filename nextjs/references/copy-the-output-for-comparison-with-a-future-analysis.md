# Copy the output for comparison with a future analysis
cp -r .next/diagnostics/analyze ./analyze-before-refactor
```

The following options are available for the `next experimental-analyze` command:

| Option          | Description                                                                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `-h, --help`    | Show all available options.                                                                                                                   |
| `[directory]`   | A directory on which to analyze the application. If not provided, the current directory will be used.                                         |
| `--no-mangling` | Disables [mangling](https://en.wikipedia.org/wiki/Name_mangling). This may affect performance and should only be used for debugging purposes. |
| `--profile`     | Enables production [profiling for React](https://react.dev/reference/react/Profiler). This may affect performance.                            |
| `-o, --output`  | Write analysis files to disk without starting the server. Output is written to `.next/diagnostics/analyze`.                                   |
| `--port <port>` | Specify a port number to serve the analyzer on. (default: 4000, env: PORT)                                                                    |

## Examples

### Debugging prerender errors

If you encounter prerendering errors during `next build`, you can pass the `--debug-prerender` flag to get more detailed output:

```bash filename="Terminal"
next build --debug-prerender
```

This enables several experimental options to make debugging easier:

* Disables server code minification:
  * `experimental.serverMinification = false`
  * `experimental.turbopackMinify = false`
* Generates source maps for server bundles:
  * `experimental.serverSourceMaps = true`
* Enables source map consumption in child processes used for prerendering:
  * `enablePrerenderSourceMaps = true`
* Continues building even after the first prerender error, so you can see all issues at once:
  * `experimental.prerenderEarlyExit = false`

This helps surface more readable stack traces and code frames in the build output.

> **Warning**: `--debug-prerender` is for debugging in development only. Do not deploy builds generated with `--debug-prerender` to production, as it may impact performance.

### Building specific routes

You can build only specific routes in the App and Pages Routers using the `--debug-build-paths` option. This is useful for faster debugging when working with large applications. The `--debug-build-paths` option accepts comma-separated file paths and supports glob patterns:

```bash filename="Terminal"