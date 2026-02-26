# Step 2.1: Install Prisma and Dependencies

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Install Packages

```bash
# Dev dependencies
npm install prisma tsx @types/pg --save-dev

# Runtime dependencies
npm install @prisma/client @prisma/adapter-pg dotenv pg
```

## Initialize Prisma

```bash
npx prisma init --db --output ../src/generated/prisma
```

This command:
- Creates a `prisma/schema.prisma` file
- Creates a `.env` file with `DATABASE_URL`
- Sets output to `src/generated/prisma` for the Prisma Client

## Package Summary

| Package | Purpose |
|---------|---------|
| `prisma` | CLI for migrations, generate, studio |
| `@prisma/client` | Type-safe database client |
| `@prisma/adapter-pg` | PostgreSQL driver adapter |
| `pg` | PostgreSQL client for Node.js |
| `tsx` | TypeScript execution for scripts |
| `dotenv` | Load `.env` variables |

## Next Step

Proceed to [configure-prisma.md](configure-prisma.md).
