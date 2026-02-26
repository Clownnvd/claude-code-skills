# Or in CI workflows for type checking without building
next typegen && npm run type-check
```

The following options are available for the `next typegen` command:

| Option        | Description                                                                                  |
| ------------- | -------------------------------------------------------------------------------------------- |
| `-h, --help`  | Show all available options.                                                                  |
| `[directory]` | A directory on which to generate types. If not provided, the current directory will be used. |

Output files are written to `<distDir>/types` (typically: `.next/dev/types` or `.next/types`, see [`isolatedDevBuild`](/docs/app/api-reference/config/next-config-js/isolatedDevBuild)):

```bash filename="Terminal"
next typegen