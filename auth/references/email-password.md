# Better Auth -- Email & Password Authentication

> Section 5 from the comprehensive reference.

---

## 5. Email & Password Authentication

### 5.1 Configuration

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,           // default
    maxPasswordLength: 128,         // default
    autoSignIn: true,               // auto sign-in after signup (default)
    // disableSignUp: false,        // set to true to prevent new registrations
    // requireEmailVerification: false,
  },
})
```

### 5.2 Sign-Up Flow

**Client-side:**
```typescript
const { data, error } = await authClient.signUp.email({
  name: "Nguyen Van A",
  email: "user@example.com",
  password: "SecurePass123",
  callbackURL: "/dashboard",  // optional - redirect after email verification
})

if (error) {
  console.error(error.message)  // e.g., "User already exists"
}
```

**Server-side (in server actions):**
```typescript
const result = await auth.api.signUpEmail({
  body: {
    name: "Nguyen Van A",
    email: "user@example.com",
    password: "SecurePass123",
  },
})
```

### 5.3 Sign-In Flow

```typescript
const { data, error } = await authClient.signIn.email({
  email: "user@example.com",
  password: "SecurePass123",
  rememberMe: true,          // optional -- if false, session ends when browser closes
  callbackURL: "/dashboard", // optional
})

if (error) {
  // Handle specific errors
  if (error.status === 403) {
    // Email not verified
  } else if (error.status === 401) {
    // Invalid credentials
  } else if (error.status === 429) {
    // Rate limited
  }
}
```

### 5.4 Sign-Out

```typescript
await authClient.signOut({
  fetchOptions: {
    onSuccess: () => {
      router.push("/login")
    },
  },
})
```

### 5.5 Email Verification

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
  },
  emailVerification: {
    sendOnSignUp: true,
    sendVerificationEmail: async ({ user, url, token }, request) => {
      // IMPORTANT: Do NOT await email sending -- prevents timing attacks
      sendEmail({
        to: user.email,
        subject: "Verify your email",
        text: `Click to verify: ${url}`,
      })
    },
  },
})
```

### 5.6 Password Reset Flow

**Server config:**
```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    sendResetPassword: async ({ user, url, token }, request) => {
      sendEmail({
        to: user.email,
        subject: "Reset your password",
        text: `Reset link: ${url}`,
      })
    },
    resetPasswordTokenExpiresIn: 3600, // 1 hour (default)
  },
})
```

**Client - Request Reset:**
```typescript
await authClient.requestPasswordReset({
  email: "user@example.com",
  redirectTo: "/reset-password",
})
```

**Client - Complete Reset:**
```typescript
await authClient.resetPassword({
  newPassword: "NewSecurePass456",
  token: tokenFromUrl,
})
```

### 5.7 Password Change (Authenticated)

```typescript
await authClient.changePassword({
  currentPassword: "OldPass123",
  newPassword: "NewPass456",
  revokeOtherSessions: true,  // recommended for security
})
```

### 5.8 Custom Password Hashing

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    password: {
      hash: async (password) => {
        // Use argon2 or bcrypt
        return await argon2.hash(password)
      },
      verify: async ({ hash, password }) => {
        return await argon2.verify(hash, password)
      },
    },
  },
})
```
