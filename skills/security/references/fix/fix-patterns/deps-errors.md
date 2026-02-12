# Fix Patterns: Dependencies + Error Handling

## Dependency Security Fixes

### Run audit and fix

```bash
pnpm audit          # Check for vulnerabilities
pnpm audit --fix    # Auto-fix where possible
pnpm update         # Update to latest compatible versions
```

### Pin versions (remove wildcards)

```json
// Before
"some-package": "*"
"other-package": "latest"

// After
"some-package": "^2.1.0"
"other-package": "^1.5.3"
```

### Remove unnecessary dependencies

Check if a dependency is actually used:
```bash
# Search for imports of the package
grep -r "from ['\"]package-name" src/
```

### Ensure lockfile committed

```bash
git ls-files pnpm-lock.yaml  # Should show the file
```

## Error Handling Fixes

### Replace raw error with safe response

```typescript
// Before: leaks error details
catch (error) {
  return NextResponse.json({ error: error.message }, { status: 500 });
}

// After: safe error response
catch (error) {
  logger.error("Operation failed", { error, route: "/api/xxx" });
  return errorResponse("INTERNAL_ERROR", "An unexpected error occurred", 500);
}
```

### Remove console.log/error from API routes

```typescript
// Before
console.error("Webhook failed:", error);

// After
import { logger } from "@/lib/api/logger";
logger.error("Webhook failed", { error, eventId });
```

### Wrap external API calls

```typescript
// Before: Stripe error details leak
const session = await stripe.checkout.sessions.create(params);

// After: caught and wrapped
try {
  const session = await stripe.checkout.sessions.create(params);
} catch (error) {
  logger.error("Stripe checkout creation failed", { error });
  return errorResponse("PAYMENT_ERROR", "Unable to create checkout session", 500);
}
```

### Use consistent error response shape

All errors should use `errorResponse()` from `src/lib/api/response.ts`:
```typescript
import { errorResponse, validationError } from "@/lib/api/response";

// Validation error
return validationError(zodError);

// Auth error
return errorResponse("UNAUTHORIZED", "Authentication required", 401);

// Not found
return errorResponse("NOT_FOUND", "Resource not found", 404);

// Server error
return errorResponse("INTERNAL_ERROR", "An unexpected error occurred", 500);
```

### Don't forward external errors

```typescript
// Before: GitHub API error details leaked
catch (error) {
  return errorResponse("GITHUB_ERROR", error.message, 500);
}

// After: generic message
catch (error) {
  logger.error("GitHub invite failed", { error, username });
  return errorResponse("INVITE_ERROR", "Unable to send repository invite", 500);
}
```
