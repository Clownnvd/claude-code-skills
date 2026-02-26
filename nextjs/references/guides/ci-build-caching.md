# CI Build Caching

> Source: https://nextjs.org/docs/app/guides/ci-build-caching (v16.1.6)

## Overview

Next.js saves a build cache to `.next/cache` shared between builds. CI workflows must persist this directory to improve build performance. Without it, you get a [No Cache Detected] error.

## Provider Configurations

### Vercel

Automatic -- no configuration needed. For Turborepo, see Vercel monorepo docs.

### GitHub Actions

```yaml
uses: actions/cache@v4
with:
  path: |
    ~/.npm
    ${{ github.workspace }}/.next/cache
  key: ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-${{ hashFiles('**/*.js', '**/*.jsx', '**/*.ts', '**/*.tsx') }}
  restore-keys: |
    ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-
```

### CircleCI

```yaml
steps:
  - save_cache:
      key: dependency-cache-{{ checksum "yarn.lock" }}
      paths:
        - ./node_modules
        - ./.next/cache
```

### Travis CI

```yaml
cache:
  directories:
    - $HOME/.cache/yarn
    - node_modules
    - .next/cache
```

### GitLab CI

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .next/cache/
```

### AWS CodeBuild

```yaml
cache:
  paths:
    - 'node_modules/**/*'
    - '.next/cache/**/*'
```

### Netlify

Use `@netlify/plugin-nextjs` plugin -- handles caching automatically.

### Bitbucket Pipelines

```yaml
definitions:
  caches:
    nextcache: .next/cache

# In step:
- step:
    caches:
      - node
      - nextcache
```

### Azure Pipelines

```yaml
- task: Cache@2
  displayName: 'Cache .next/cache'
  inputs:
    key: next | $(Agent.OS) | yarn.lock
    path: '$(System.DefaultWorkingDirectory)/.next/cache'
```

### Jenkins

```groovy
cache(caches: [
    arbitraryFileCache(
        path: ".next/cache",
        includes: "**/*",
        cacheValidityDecidingFile: "next-lock.cache"
    )
]) {
    sh "npm run build"
}
```

### Heroku

```json
{
  "cacheDirectories": [".next/cache"]
}
```

Add to top-level `package.json`.

## Quick Reference

| Provider         | Cache Path        | Key Strategy                          |
|------------------|-------------------|---------------------------------------|
| Vercel           | Automatic         | N/A                                   |
| GitHub Actions   | `.next/cache`     | OS + lockfile + source hash           |
| CircleCI         | `.next/cache`     | Lockfile checksum                     |
| GitLab CI        | `.next/cache/`    | Commit ref slug                       |
| Travis CI        | `.next/cache`     | Directory-based                       |
| AWS CodeBuild    | `.next/cache/**/*`| Path-based                            |
| Netlify          | Plugin-managed    | `@netlify/plugin-nextjs`              |
| Bitbucket        | `.next/cache`     | Custom cache definition               |
| Azure Pipelines  | `.next/cache`     | OS + lockfile                         |
| Jenkins          | `.next/cache`     | Git commit hash file                  |
| Heroku           | `.next/cache`     | `cacheDirectories` in package.json    |
