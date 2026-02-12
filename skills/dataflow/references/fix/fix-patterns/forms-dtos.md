# Fix Patterns: Form Handling + Data Transformation (DTOs)

## Form Handling Fixes

### Fix: Client + Server Validation
```typescript
// CLIENT: react-hook-form with Zod
"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { signUpSchema, type SignUpInput } from "@/lib/validations/auth";

function SignUpForm() {
  const form = useForm<SignUpInput>({
    resolver: zodResolver(signUpSchema),
    defaultValues: { name: "", email: "", password: "", confirmPassword: "" },
  });

  const onSubmit = async (values: SignUpInput) => {
    // Submit to API or server action
  };

  return <form onSubmit={form.handleSubmit(onSubmit)}>...</form>;
}

// SERVER: Same schema validates again
export async function POST(req: NextRequest) {
  const body = await req.json();
  const result = signUpSchema.safeParse(body);
  if (!result.success) return validationError(result.error);
  // Proceed with validated data
}
```

### Fix: Loading States
```typescript
"use client";
function SubmitButton() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  return (
    <button type="submit" disabled={isSubmitting}>
      {isSubmitting ? (
        <span className="flex items-center gap-2">
          <Loader2 className="h-4 w-4 animate-spin" />
          Submitting...
        </span>
      ) : (
        "Submit"
      )}
    </button>
  );
}
```

### Fix: Field-Level Errors
```typescript
// Display Zod field errors in form
{form.formState.errors.email && (
  <p className="text-sm text-destructive">
    {form.formState.errors.email.message}
  </p>
)}
```

### Fix: CSRF on Form Submission
```typescript
// For API route forms (not Server Actions):
const response = await fetch("/api/user/profile", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "X-Requested-With": "fetch",  // CSRF indicator
  },
  body: JSON.stringify(data),
});
```

## Data Transformation (DTO) Fixes

### Fix: Date Serialization
```typescript
// BEFORE: Raw Date object (fails in JSON)
return successResponse({ createdAt: user.createdAt });

// AFTER: ISO string
return successResponse({ createdAt: user.createdAt.toISOString() });
```

### Fix: Field Renaming for Consistent API
```typescript
// BEFORE: Prisma field name leaks
return successResponse({
  image: user.image,  // Prisma column name

// AFTER: Consistent API naming
return successResponse({
  avatarUrl: user.image,  // API-friendly name
});
```

### Fix: Strip Internal Fields
```typescript
// BEFORE: Leaks internal IDs
return successResponse(purchase); // Includes stripeCustomerId, userId

// AFTER: Only public fields
return successResponse({
  id: purchase.id,
  status: purchase.status,
  amount: purchase.amount,
  productType: purchase.productType,
  purchasedAt: purchase.purchasedAt?.toISOString() ?? null,
});
```

### Fix: Use Prisma select as Implicit DTO
```typescript
// select acts as a DTO — only requested fields returned
const purchase = await prisma.purchase.findUnique({
  where: { id: purchaseId },
  select: {
    id: true,
    status: true,
    amount: true,
    productType: true,
    purchasedAt: true,
    // stripeCustomerId: NOT selected — not exposed
    // userId: NOT selected — not exposed
  },
});
```
