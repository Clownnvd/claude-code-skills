# Polar API Reference Quick Cards

> Section 11 from the Polar Payment SDK Comprehensive Reference.
> Covers pagination, customer CRUD, product listing, order invoices, and discounts.

---

## 11. API Reference Quick Cards

### 11.1 Pagination

```typescript
const products = await polar.products.list({
  page: 1,    // Default: 1
  limit: 100, // Default: 10, Max: 100
})
// products.pagination.totalCount
// products.pagination.maxPage
```

### 11.2 Customer CRUD via External ID

```typescript
// Get customer by your user ID
const customer = await polar.customers.getExternal(userId)

// Update customer
await polar.customers.updateExternal(userId, {
  email: "new@example.com",
  metadata: { plan: "pro" },
})

// Delete customer
await polar.customers.deleteExternal(userId)
```

### 11.3 Product Listing

```typescript
const products = await polar.products.list({
  isRecurring: true, // Only subscriptions
})
```

### 11.4 Order Invoice

```typescript
// Step 1: Update billing details FIRST (immutable after generation)
await polar.orders.update(orderId, {
  billingName: "Company Name",
  billingAddress: { country: "VN", city: "Ho Chi Minh" },
})

// Step 2: Generate invoice (async -- returns 202)
await polar.orders.invoice(orderId)

// Step 3: Retrieve invoice (poll or wait for webhook)
const invoice = await polar.orders.getInvoice(orderId)
```

### 11.5 Discounts

```typescript
const discount = await polar.discounts.create({
  name: "Launch 20%",
  type: "percentage",
  amount: 20,
  maxRedemptions: 100,
})

// Apply to checkout
const checkout = await polar.checkouts.create({
  products: [productId],
  discountId: discount.id,
  // ...
})
```
