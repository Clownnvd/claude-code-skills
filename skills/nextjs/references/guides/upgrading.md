# Upgrading

> Source: https://nextjs.org/docs/app/guides/upgrading (v16.1.6)

Guides for upgrading Next.js between major versions.

## Available Upgrade Guides

| From | To | Guide |
|---|---|---|
| v13 | v14 | `/docs/app/guides/upgrading/version-14` |
| v14 | v15 | `/docs/app/guides/upgrading/version-15` |
| v15 | v16 | `/docs/app/guides/upgrading/version-16` |

## Codemods

Next.js provides codemods to automatically update your codebase when new features or breaking changes are released.

**Guide:** `/docs/app/guides/upgrading/codemods`

### Usage

```bash
npx @next/codemod@latest <transform> <path>
```

Codemods handle common migration patterns such as:
- API changes between versions
- Deprecated feature replacements
- Import path updates

## Upgrade Workflow

1. Read the version-specific upgrade guide for your target version
2. Run applicable codemods to automate mechanical changes
3. Review and fix any remaining manual migration items
4. Test thoroughly (unit, integration, E2E)
5. Deploy

## Quick Reference

| Task | Command / Resource |
|---|---|
| Run codemods | `npx @next/codemod@latest <transform> <path>` |
| Upgrade to v14 | See version-14 guide |
| Upgrade to v15 | See version-15 guide |
| Upgrade to v16 | See version-16 guide |
| Codemods reference | `/docs/app/guides/upgrading/codemods` |
