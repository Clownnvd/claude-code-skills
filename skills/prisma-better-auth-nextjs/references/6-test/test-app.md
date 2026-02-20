# Step 6: Test Your Application

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Start Development Server

```bash
npm run dev
```

Navigate to `http://localhost:3000`.

## Test Checklist

| Test | Expected |
|------|----------|
| Home page loads | Shows Sign Up + Sign In buttons |
| Sign Up | Creates account, redirects to dashboard |
| Dashboard | Shows user name + email |
| Sign Out | Clears session, back to sign-in |
| Sign In | Authenticates, redirects to dashboard |
| Auth guard | `/dashboard` without session redirects to `/sign-in` |

## Inspect Database

```bash
npx prisma studio
```

Opens a browser-based GUI to view/edit data in the `User`, `Session`, `Account`, and `Verification` tables.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Database connection error | Verify `DATABASE_URL` in `.env` |
| Auth secret missing | Run `npx @better-auth/cli@latest secret` |
| Schema out of sync | Run `npx prisma migrate dev` then `npx prisma generate` |
| Module not found | Run `npx prisma generate` to regenerate client |

## File Summary

| File | Purpose |
|------|---------|
| `prisma.config.ts` | Prisma datasource config |
| `prisma/schema.prisma` | Database models |
| `src/lib/prisma.ts` | Global Prisma Client singleton |
| `src/lib/auth.ts` | Better Auth server config |
| `src/lib/auth-client.ts` | Better Auth React client |
| `src/app/api/auth/[...all]/route.ts` | Auth API catch-all route |
| `src/app/page.tsx` | Home page |
| `src/app/sign-up/page.tsx` | Sign up form |
| `src/app/sign-in/page.tsx` | Sign in form |
| `src/app/dashboard/page.tsx` | Protected dashboard |
