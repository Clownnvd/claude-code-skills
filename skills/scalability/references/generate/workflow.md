# Scalability Generate Workflow

## Process

1. **Parse Request** — Extract: component type, performance requirements, expected load
2. **Load Criteria** — Read all 10 scalability scoring categories from SKILL.md
3. **Map Criteria to Code**:

| Category | Code Pattern |
|----------|-------------|
| Bundle Size & Code Splitting (15%) | Dynamic imports, tree shaking, lazy components |
| Image & Asset Optimization (12%) | next/image, WebP/AVIF, responsive sizes, lazy loading |
| Server Component Architecture (12%) | RSC by default, minimal "use client", streaming |
| Database Query Performance (12%) | No N+1, connection pooling, indexed queries, select |
| API Response Performance (10%) | Small payloads, pagination, compression, no over-fetch |
| Client-Side Performance (10%) | Minimal re-renders, memoization, no layout thrash |
| Edge & CDN Optimization (8%) | Static generation, ISR, CDN-friendly headers |
| Memory & Resource Management (8%) | No leaks, connection cleanup, bounded caches |
| Concurrent Processing (7%) | Promise.all for independent fetches, streaming |
| Performance Monitoring (6%) | Web Vitals, bundle budgets, lighthouse CI |

4. **Generate** — Write code with all scalability patterns
5. **Self-Check** — Verify all 10 categories
6. **Output** — Code + compliance checklist

## Quality Contract

- All 10 categories addressed
- Score >= 90 (A-) if audited with scalability scoring
- No barrel re-exports, no over-fetching, no layout thrash
- Dynamic imports for heavy components
