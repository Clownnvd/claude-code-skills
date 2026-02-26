# Step 5.4: Home Page

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Update `src/app/page.tsx`

```typescript
"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <main className="flex items-center justify-center h-screen bg-neutral-950 text-white">
      <div className="flex gap-4">
        <button
          onClick={() => router.push("/sign-up")}
          className="bg-white text-black font-medium px-6 py-2 rounded-md hover:bg-gray-200"
        >
          Sign Up
        </button>
        <button
          onClick={() => router.push("/sign-in")}
          className="border border-white text-white font-medium px-6 py-2 rounded-md hover:bg-neutral-800"
        >
          Sign In
        </button>
      </div>
    </main>
  );
}
```

## Key Patterns

| Pattern | Details |
|---------|---------|
| Purpose | Landing page with auth navigation |
| Navigation | `router.push()` to sign-up/sign-in |
| Layout | Full-screen centered with dark background |

## Next Step

Proceed to [6-test/test-app.md](../6-test/test-app.md).
