# Codemods

@router: Pages Router

Codemods are transformations that run on your codebase programmatically. This allows a large number of changes to be programmatically applied without having to manually go through every file.

Next.js provides Codemod transformations to help upgrade your Next.js codebase when an API is updated or deprecated.

## Usage

In your terminal, navigate (`cd`) into your project's folder, then run:

```bash filename="Terminal"
npx @next/codemod <transform> <path>
```

Replacing `<transform>` and `<path>` with appropriate values.

* `transform` - name of transform
* `path` - files or directory to transform
* `--dry` Do a dry-run, no code will be edited
* `--print` Prints the changed output for comparison

## Upgrade

Upgrades your Next.js application, automatically running codemods and updating Next.js, React, and React DOM.

```bash filename="Terminal"
npx @next/codemod upgrade [revision]
```

### Options

* `revision` (optional): Specify the upgrade type (`patch`, `minor`, `major`), an NPM dist tag (e.g. `latest`, `canary`, `rc`), or an exact version (e.g. `15.0.0`). Defaults to `minor` for stable versions.
* `--verbose`: Show more detailed output during the upgrade process.

For example:

```bash filename="Terminal"