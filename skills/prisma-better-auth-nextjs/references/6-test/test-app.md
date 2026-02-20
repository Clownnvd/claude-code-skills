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
| Duplicate email | Sign up with same email shows error |
| Short password | Password < 8 chars rejected |

## Inspect Database

```bash
npx prisma studio
```

Opens a browser GUI to view/edit `user`, `session`, `account`, `verification` tables.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Database connection error | Wrong `DATABASE_URL` | Verify URL format: `postgresql://user:pass@host:5432/db?sslmode=require` |
| Auth secret missing | No `BETTER_AUTH_SECRET` | Run `npx @better-auth/cli@latest secret` |
| Schema out of sync | Models changed without migration | `npx prisma migrate dev` then `npx prisma generate` |
| Module not found (`@/generated/prisma`) | Client not generated | `npx prisma generate` |
| CORS error on sign-in/sign-up | App runs on non-3000 port | Add `trustedOrigins: ["http://localhost:PORT"]` to `auth.ts` |
| "Table not found" or auth 500 | Missing `@@map` annotations | Add `@@map("lowercase")` to all models, re-migrate |
| `prisma migrate dev` hangs | Shadow database permission issue | Check DB user has `CREATE DATABASE` permission |
| Password rejected | Too short | Better Auth requires min 8 characters |
| Session lost on refresh | Cookie issue | Verify `BETTER_AUTH_URL` matches actual origin |
| `Cannot find module 'better-auth'` | Not installed | `npm install better-auth` |

## Common Edge Cases

| Edge Case | Behavior |
|-----------|----------|
| Duplicate email sign-up | Returns error: "User already exists" |
| Invalid email format | Client-side `type="email"` validation |
| Empty form fields | `required` attribute prevents submission |
| Expired session | `useSession` returns null, auth guard redirects |
| Concurrent sign-ins | Each creates a separate session row |

## File Summary

| File | Purpose |
|------|---------|
| `prisma.config.ts` | Prisma datasource config |
| `prisma/schema.prisma` | Database models (with `@@map`) |
| `src/lib/prisma.ts` | Global Prisma Client singleton |
| `src/lib/auth.ts` | Better Auth server config |
| `src/lib/auth-client.ts` | Better Auth React client |
| `src/app/api/auth/[...all]/route.ts` | Auth API catch-all route |
| `src/app/page.tsx` | Home page |
| `src/app/sign-up/page.tsx` | Sign up form |
| `src/app/sign-in/page.tsx` | Sign in form |
| `src/app/dashboard/page.tsx` | Protected dashboard |
