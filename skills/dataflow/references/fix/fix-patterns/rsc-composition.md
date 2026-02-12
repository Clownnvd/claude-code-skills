# Fix Patterns: RSC Fetching + Server/Client Composition

## RSC Data Fetching Fixes

### Fix: Convert Client Page to Server Component
```typescript
// BEFORE (client page — bad)
"use client";
export default function DashboardPage() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch("/api/user/purchase").then(r => r.json()).then(setData);
  }, []);
  return <div>{data?.name}</div>;
}

// AFTER (server page — good)
export default async function DashboardPage() {
  const purchase = await prisma.purchase.findFirst({
    where: { userId: session.user.id },
    select: { id: true, status: true },
  });
  return <div>{purchase?.status}</div>;
}
```
**Warning**: Only convert if the component has NO `useState`, `useEffect`, or event handlers.

### Fix: Add Suspense Boundaries
```typescript
export default async function DashboardPage() {
  return (
    <div>
      <DashboardHeader />
      <Suspense fallback={<PurchaseSkeleton />}>
        <PurchaseStatus />
      </Suspense>
    </div>
  );
}

async function PurchaseStatus() {
  const purchase = await getPurchase(); // Slow query
  return <PurchaseCard purchase={purchase} />;
}
```

### Fix: Parallel Data Fetching
```typescript
// BEFORE (waterfall)
const user = await getUser();
const purchase = await getPurchase(user.id);

// AFTER (parallel when independent)
const [user, purchases] = await Promise.all([
  getUser(),
  getRecentPurchases(),
]);
```

### Fix: Add loading.tsx
```typescript
// src/app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="flex items-center justify-center p-20">
      <Loader2 className="size-6 animate-spin text-muted-foreground" />
    </div>
  );
}
```

## Server/Client Composition Fixes

### Fix: Push "use client" to Leaves
```typescript
// BEFORE: "use client" at page level (bad)
"use client";
export default function SettingsPage() {
  const [tab, setTab] = useState("profile");
  return (
    <div>
      <h1>Settings</h1> {/* This doesn't need client */}
      <TabSwitcher tab={tab} onTabChange={setTab} />
      <SettingsForm />
    </div>
  );
}

// AFTER: Server page, client at leaves (good)
export default function SettingsPage() {
  return (
    <div>
      <h1>Settings</h1> {/* Server rendered */}
      <SettingsContent /> {/* Client component */}
    </div>
  );
}
```

### Fix: Children Pattern for Server-in-Client
```typescript
// Client wrapper that accepts server children
"use client";
function AnimatedSection({ children }: { children: React.ReactNode }) {
  return <motion.div animate={{ opacity: 1 }}>{children}</motion.div>;
}

// Server page uses it
export default async function Page() {
  const data = await fetchData();
  return (
    <AnimatedSection>
      <DataDisplay data={data} /> {/* Server Component */}
    </AnimatedSection>
  );
}
```
