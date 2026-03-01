# Schema Design Patterns

> Sources: Prisma docs, CViet project experience.
> Date: 2026-02-27

---

## Relations

```prisma
// One-to-Many
model User {
  id    String @id @default(cuid())
  posts Post[]
}

model Post {
  id       String @id @default(cuid())
  userId   String
  user     User   @relation(fields: [userId], references: [id], onDelete: Cascade)
}

// Many-to-Many (implicit)
model Post {
  id         String     @id @default(cuid())
  categories Category[]
}

model Category {
  id    String @id @default(cuid())
  posts Post[]
}

// Many-to-Many (explicit join table)
model PostCategory {
  postId     String
  categoryId String
  post       Post     @relation(fields: [postId], references: [id])
  category   Category @relation(fields: [categoryId], references: [id])
  assignedAt DateTime @default(now())

  @@id([postId, categoryId])
}

// Self-Relation
model Employee {
  id         String     @id @default(cuid())
  managerId  String?
  manager    Employee?  @relation("ManagerReports", fields: [managerId], references: [id])
  reports    Employee[] @relation("ManagerReports")
}
```

## Enums

```prisma
enum Plan {
  FREE
  PRO
}

// Prisma 7: Mapped enums
enum Role {
  ADMIN   @map("admin")
  USER    @map("user")
  GUEST   @map("guest")
}
```

## Json Fields

```prisma
model CV {
  id   String @id @default(cuid())
  data Json   // Stores CVData object
}
```

**TypeScript typing for Json fields (see typescript.md for details):**
```typescript
// Double-cast pattern (works universally)
const typedData = cv.data as unknown as CVData

// Or use prisma-json-types-generator for compile-time safety
```

## Indexes

```prisma
model CV {
  id        String   @id @default(cuid())
  userId    String
  title     String
  template  String
  language  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  // Single-column index
  @@index([userId])

  // Composite index (for queries filtering on both)
  @@index([userId, template])

  // Composite index with sort order
  @@index([userId, createdAt(sort: Desc)])
}

// Unique constraints
model Account {
  id         String @id
  providerId String
  accountId  String

  @@unique([providerId, accountId])
}

// Full-text search index (PostgreSQL)
model Post {
  id      String @id
  title   String
  content String

  @@fulltext([title, content])
}
```

## Default Values

```prisma
model User {
  id        String   @id @default(cuid())       // CUID
  uuid      String   @id @default(uuid())        // UUID v4
  autoId    Int      @id @default(autoincrement()) // Auto-increment
  active    Boolean  @default(true)
  role      Role     @default(USER)
  plan      Plan     @default(FREE)
  count     Int      @default(0)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt                  // Auto-updated
  metadata  Json     @default("{}")              // JSON default
  tags      Json     @default("[]")              // Array default

  // Database-level default with dbgenerated
  tsVector  Unsupported("tsvector")? @default(dbgenerated("''::tsvector"))
}
```

## Column Mapping

```prisma
model User {
  id        String @id @default(cuid())
  firstName String @map("first_name")
  lastName  String @map("last_name")

  @@map("users") // Table name in database
}
```
