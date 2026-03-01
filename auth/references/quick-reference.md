# Better Auth -- Quick Reference Card & Sources

> Quick Reference Card and Sources from the comprehensive reference.

---

## Quick Reference Card

### Minimum Viable Better Auth Setup (Next.js 16)

```
1. pnpm add better-auth
2. Create src/lib/auth.ts (betterAuth config + prismaAdapter)
3. Create src/lib/auth-client.ts (createAuthClient)
4. Create src/app/api/auth/[...all]/route.ts (toNextJsHandler)
5. Add Prisma models: User, Session, Account, Verification
6. Create src/proxy.ts (getSessionCookie + redirect)
7. Set env: BETTER_AUTH_SECRET, BETTER_AUTH_URL, DATABASE_URL
8. pnpm db:push
```

### Debug Checklist

- [ ] `BETTER_AUTH_SECRET` is set and >= 32 characters
- [ ] `BETTER_AUTH_URL` matches your actual URL
- [ ] API route exists at `/api/auth/[...all]/route.ts`
- [ ] Route handler exports both `GET` and `POST`
- [ ] Prisma schema has all 4 required models (User, Session, Account, Verification)
- [ ] Client uses `"better-auth/react"` (not `"better-auth/client"`)
- [ ] `proxy.ts` (not `middleware.ts`) with `export function proxy()` (not `middleware()`)
- [ ] `headers()` is awaited in Next.js 16
- [ ] TypeScript strict mode is enabled
- [ ] No duplicate `better-auth` installations (`pnpm why @better-auth/core`)

---

## Sources

- [Better Auth - Introduction](https://www.better-auth.com/docs/introduction)
- [Better Auth - Installation](https://www.better-auth.com/docs/installation)
- [Better Auth - Session Management](https://www.better-auth.com/docs/concepts/session-management)
- [Better Auth - Email & Password](https://www.better-auth.com/docs/authentication/email-password)
- [Better Auth - Next.js Integration](https://www.better-auth.com/docs/integrations/next)
- [Better Auth - Prisma Adapter](https://www.better-auth.com/docs/adapters/prisma)
- [Better Auth - Security Reference](https://www.better-auth.com/docs/reference/security)
- [Better Auth - Rate Limiting](https://www.better-auth.com/docs/concepts/rate-limit)
- [Better Auth - Errors Reference](https://www.better-auth.com/docs/reference/errors)
- [Better Auth - FAQ](https://www.better-auth.com/docs/reference/faq)
- [Better Auth - Google OAuth](https://www.better-auth.com/docs/authentication/google)
- [Better Auth - Cookies](https://www.better-auth.com/docs/concepts/cookies)
- [Prisma ORM - Better Auth Guide](https://www.prisma.io/docs/guides/betterauth-nextjs)
- [Next.js 16 - Proxy File Convention](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)
- [GitHub - better-auth/better-auth Issues](https://github.com/better-auth/better-auth/issues)
- [GitHub - State mismatch since v1.4.4 #7023](https://github.com/better-auth/better-auth/issues/7023)
- [GitHub - CLI broken zod import #3614](https://github.com/better-auth/better-auth/issues/3614)
- [GitHub - nextCookies issue #2434](https://github.com/better-auth/better-auth/issues/2434)
- [GitHub - OAuth redirect_uri #6326](https://github.com/better-auth/better-auth/issues/6326)
