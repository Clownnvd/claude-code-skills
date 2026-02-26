# Review Mode -- Email System

Quick 1-2 file review against applicable email categories.

## Process

1. **Read files** -- Load the specified file(s) for review
2. **Identify categories** -- Determine which of the 10 categories apply to the file(s)
3. **Score** -- Rate each applicable category 0-10 using criteria files
4. **Annotate** -- Reference specific line numbers for issues
5. **Suggest fixes** -- Provide concrete code changes with before/after
6. **Output** -- Fill `assets/templates/review-report.md.template`

## File -> Category Mapping

| File Pattern | Applicable Categories |
|-------------|----------------------|
| `src/lib/resend.ts`, `src/lib/email.ts` | Provider Integration, Transactional Email |
| `src/emails/*.tsx` | Templates & Rendering, Testing & Preview |
| `src/lib/queue.ts`, `src/app/api/queue/*` | Queue & Delivery, Rate Limiting |
| `src/app/api/webhooks/resend/*` | Bounce Handling, Analytics, Auth |
| `src/app/api/*/route.ts` (with email triggers) | Transactional, Rate Limiting |
| `.env.example` | Provider Integration, Auth |

## Scoring

Only score categories that apply to the reviewed file(s). Report applicable score:
```
Applicable Score = (sum of weighted scores for applicable categories) / (sum of weights) * 100
```
