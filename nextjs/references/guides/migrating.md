# Migrating to Next.js

> Source: https://nextjs.org/docs/app/guides/migrating (v16.1.6)

## Available Migration Guides

| Source | Target | Guide URL |
|--------|--------|-----------|
| Pages Router | App Router | [App Router Migration](/docs/app/guides/migrating/app-router-migration) |
| Create React App (CRA) | Next.js | [From CRA](/docs/app/guides/migrating/from-create-react-app) |
| Vite | Next.js | [From Vite](/docs/app/guides/migrating/from-vite) |

## Pages Router to App Router

The most common migration path for existing Next.js apps. Key changes:

- `pages/` directory replaced by `app/` directory
- File-based routing uses folders with `page.tsx` files
- Layouts replace `_app.tsx` and `_document.tsx`
- Server Components are the default (no `'use client'` needed)
- Data fetching uses `async` components instead of `getServerSideProps`/`getStaticProps`
- Metadata API replaces `<Head>` component

## From Create React App

For React SPA apps built with CRA. Key changes:

- Add file-based routing (replace react-router)
- Server-side rendering enabled by default
- API routes replace separate backend if applicable
- Static assets move to `public/`

## From Vite

For React apps using Vite as build tool. Key changes:

- Replace `vite.config.ts` with `next.config.ts`
- Replace Vite plugins with Next.js equivalents
- Move from client-only to server-first architecture
- Update import aliases and environment variables

## Quick Reference

| Migration | Difficulty | Key Benefit |
|-----------|-----------|-------------|
| Pages Router to App Router | Medium | Server Components, layouts, streaming |
| CRA to Next.js | Medium | SSR/SSG, file routing, API routes |
| Vite to Next.js | Medium | SSR/SSG, file routing, optimizations |
