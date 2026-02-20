#!/usr/bin/env python3
"""
Scaffold Prisma + Better Auth + Next.js auth files.

Creates all required files for production-grade authentication:
- prisma.config.ts (with DIRECT_URL fallback)
- src/lib/db/index.ts (Neon adapter + slow query logging)
- src/lib/auth.ts (trustedOrigins, session/cookie config)
- src/lib/auth-client.ts (with 2FA client plugin)
- src/lib/auth/audit-log.ts (structured event logging)
- src/app/api/auth/[...all]/route.ts
- src/app/sign-up/page.tsx
- src/app/sign-in/page.tsx
- src/app/dashboard/page.tsx

Usage:
    python scaffold.py [target-dir]

If target-dir is omitted, uses current working directory.
"""

import os
import sys

FILES = {
    "prisma.config.ts": '''\
import "dotenv/config";
import { defineConfig } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  datasource: {
    // Migrations use DIRECT_URL (bypasses pgbouncer) — falls back to DATABASE_URL
    url: process.env["DIRECT_URL"] || process.env["DATABASE_URL"],
  },
});
''',
    "src/lib/db/index.ts": '''\
import { PrismaClient } from "@prisma/client";
import { PrismaNeon } from "@prisma/adapter-neon";

// Append statement_timeout (10s) to prevent long-running queries
const dbUrl = new URL(process.env.DATABASE_URL!);
if (!dbUrl.searchParams.has("options")) {
  dbUrl.searchParams.set("options", "-c statement_timeout=10000");
}
const adapter = new PrismaNeon({ connectionString: dbUrl.toString() });

const globalForPrisma = global as unknown as {
  prisma: PrismaClient;
};

const SLOW_QUERY_THRESHOLD_MS = 1000;

const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    adapter,
    log: [
      { emit: "event", level: "query" },
      { emit: "stdout", level: "warn" },
      { emit: "stdout", level: "error" },
    ],
  });

// @ts-expect-error -- Prisma event typing varies by adapter
prisma.$on("query", (e: { duration: number; query: string }) => {
  if (e.duration > SLOW_QUERY_THRESHOLD_MS) {
    const sanitized = e.query.replace(/\\$\\d+/g, "?");
    if (process.env.NODE_ENV === "production") {
      console.warn(JSON.stringify({
        level: "warn", event: "slow_query",
        durationMs: e.duration, threshold: SLOW_QUERY_THRESHOLD_MS,
        timestamp: new Date().toISOString(),
      }));
    } else {
      console.warn(`[SLOW QUERY] ${e.duration}ms: ${sanitized.slice(0, 200)}`);
    }
  }
});

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export default prisma;
''',
    "src/lib/auth.ts": '''\
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { twoFactor } from "better-auth/plugins";
import prisma from "@/lib/db";

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),

  trustedOrigins: process.env.BETTER_AUTH_URL
    ? [process.env.BETTER_AUTH_URL]
    : ["http://localhost:3000"],

  session: {
    expiresIn: 60 * 60 * 24 * 7,  // 7 days
    updateAge: 60 * 60 * 24,       // Refresh daily
    cookieCache: { enabled: true, maxAge: 5 * 60 },
  },

  advanced: {
    cookiePrefix: "app",
    useSecureCookies: process.env.NODE_ENV === "production",
    defaultCookieSameSite: "lax" as const,
  },

  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },

  plugins: [
    twoFactor({ issuer: "My App" }),
  ],
});

export type Session = typeof auth.$Infer.Session;
''',
    "src/lib/auth-client.ts": '''\
import { createAuthClient } from "better-auth/react";
import { twoFactorClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [twoFactorClient()],
});

export const { signIn, signUp, signOut, useSession, twoFactor } = authClient;
''',
    "src/lib/auth/audit-log.ts": '''\
type AuditEvent =
  | "sign_in" | "sign_up" | "sign_out" | "login_failed"
  | "password_changed" | "password_reset_request"
  | "email_verified" | "oauth_link" | "oauth_unlink"
  | "session_revoked" | "2fa_enabled" | "2fa_disabled";

interface AuditEntry {
  level: "info" | "warn";
  event: AuditEvent;
  userId: string;
  provider?: string;
  ip?: string;
  timestamp: string;
}

const WARN_EVENTS: AuditEvent[] = ["password_reset_request", "login_failed", "session_revoked"];

export function logAuthEvent(
  event: AuditEvent,
  userId: string,
  extra?: { provider?: string; ip?: string }
): void {
  const entry: AuditEntry = {
    level: WARN_EVENTS.includes(event) ? "warn" : "info",
    event, userId,
    provider: extra?.provider,
    ip: extra?.ip,
    timestamp: new Date().toISOString(),
  };

  if (process.env.NODE_ENV === "production") {
    console.info(JSON.stringify(entry));
  } else {
    console.info(
      `[AUTH] ${entry.event} user=${entry.userId}` +
      `${entry.provider ? ` provider=${entry.provider}` : ""}`
    );
  }
}
''',
    "src/app/api/auth/[...all]/route.ts": '''\
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { POST, GET } = toNextJsHandler(auth);
''',
    "src/app/sign-up/page.tsx": '''\
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signUp } from "@/lib/auth-client";

export default function SignUpPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);

    const formData = new FormData(e.currentTarget);

    const res = await signUp.email({
      name: formData.get("name") as string,
      email: formData.get("email") as string,
      password: formData.get("password") as string,
    });

    if (res.error) {
      setError(res.error.message || "Something went wrong.");
    } else {
      router.push("/dashboard");
    }
  }

  return (
    <main className="max-w-md mx-auto p-6 space-y-4 text-white">
      <h1 className="text-2xl font-bold">Sign Up</h1>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="name"
          placeholder="Full Name"
          required
          className="w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2"
        />
        <input
          name="email"
          type="email"
          placeholder="Email"
          required
          className="w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2"
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          required
          minLength={8}
          className="w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2"
        />
        <button
          type="submit"
          className="w-full bg-white text-black font-medium rounded-md px-4 py-2 hover:bg-gray-200"
        >
          Create Account
        </button>
      </form>
    </main>
  );
}
''',
    "src/app/sign-in/page.tsx": '''\
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "@/lib/auth-client";

export default function SignInPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);

    const formData = new FormData(e.currentTarget);

    const res = await signIn.email({
      email: formData.get("email") as string,
      password: formData.get("password") as string,
    });

    if (res.error) {
      setError(res.error.message || "Something went wrong.");
    } else {
      router.push("/dashboard");
    }
  }

  return (
    <main className="max-w-md h-screen flex items-center justify-center flex-col mx-auto p-6 space-y-4 text-white">
      <h1 className="text-2xl font-bold">Sign In</h1>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="email"
          type="email"
          placeholder="Email"
          required
          className="w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2"
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          required
          className="w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2"
        />
        <button
          type="submit"
          className="w-full bg-white text-black font-medium rounded-md px-4 py-2 hover:bg-gray-200"
        >
          Sign In
        </button>
      </form>
    </main>
  );
}
''',
    "src/app/dashboard/page.tsx": '''\
"use client";

import { useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";
import { useEffect } from "react";

export default function DashboardPage() {
  const router = useRouter();
  const { data: session, isPending } = useSession();

  useEffect(() => {
    if (!isPending && !session?.user) {
      router.push("/sign-in");
    }
  }, [isPending, session, router]);

  if (isPending)
    return <p className="text-center mt-8 text-white">Loading...</p>;
  if (!session?.user)
    return <p className="text-center mt-8 text-white">Redirecting...</p>;

  const { user } = session;

  return (
    <main className="max-w-md h-screen flex items-center justify-center flex-col mx-auto p-6 space-y-4 text-white">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p>Welcome, {user.name || "User"}!</p>
      <p>Email: {user.email}</p>
      <button
        onClick={() => signOut()}
        className="w-full bg-white text-black font-medium rounded-md px-4 py-2 hover:bg-gray-200"
      >
        Sign Out
      </button>
    </main>
  );
}
''',
}


def scaffold(target_dir: str) -> list[str]:
    """Create all auth scaffold files in target_dir. Returns list of created paths."""
    created = []
    for rel_path, content in FILES.items():
        full_path = os.path.join(target_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if os.path.exists(full_path):
            print(f"  SKIP (exists): {rel_path}")
            continue

        with open(full_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        created.append(rel_path)
        print(f"  CREATED: {rel_path}")

    return created


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    target = os.path.abspath(target)

    if not os.path.isdir(target):
        print(f"Error: {target} is not a directory")
        return 1

    print(f"Scaffolding Better Auth files in: {target}\n")
    created = scaffold(target)

    print(f"\n{len(created)} files created, {len(FILES) - len(created)} skipped (already exist).")
    print("\nNext steps:")
    print("  1. npm install prisma tsx --save-dev")
    print("  2. npm install @prisma/client @prisma/adapter-neon better-auth")
    print("  3. npx prisma init --db --output ../src/generated/prisma")
    print("  4. npx @better-auth/cli@latest secret")
    print("  5. npx @better-auth/cli generate  (adds auth models to schema)")
    print("  6. npx prisma migrate dev --name add-auth-models")
    print("  7. npx prisma generate")
    print("  8. npm run dev")
    return 0


if __name__ == "__main__":
    sys.exit(main())
