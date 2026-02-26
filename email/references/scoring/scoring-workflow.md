# Email Scoring -- Workflow

6-step audit process. Follow in order.

## Step 1: Gather Files

Collect all email-related files from the codebase:

| File Type | Typical Paths | Purpose |
|-----------|--------------|---------|
| Email service | `src/lib/email.ts`, `src/lib/resend.ts` | Client init, send functions |
| Templates | `src/emails/*.tsx`, `src/emails/components/*` | React Email components |
| Queue config | `src/lib/queue.ts` | QStash client, enqueue functions |
| Queue workers | `src/app/api/queue/*/route.ts` | Worker endpoints |
| Webhooks | `src/app/api/webhooks/resend/route.ts` | Event handling |
| API routes | `src/app/api/*/route.ts` | Email-triggering endpoints |
| Environment | `.env.example`, `.env.local` | Required env vars |
| Package config | `package.json` | Dependencies and versions |
| DNS docs | `README.md`, `docs/email-setup.md` | Domain verification docs |

If a file type does not exist, note it. Missing files affect scoring.

## Step 2: Score Each Category

For each of the 10 categories, assign a raw score 0-10:

| Raw Score | Meaning |
|-----------|---------|
| 0 | Not implemented at all |
| 1-3 | Minimal or broken implementation |
| 4-5 | Partial implementation with significant gaps |
| 6-7 | Working implementation with room for improvement |
| 8 | Good implementation with minor gaps |
| 9-10 | Excellent or best-practice implementation |

Use criteria from `scoring/criteria/` files for point breakdowns per category.

### Category -> Criteria File Mapping

| Categories | Criteria File |
|-----------|--------------|
| Transactional Email (15%), Notification Queue (12%) | `criteria/transactional-delivery.md` |
| Email Templates (12%), Testing & Preview (6%) | `criteria/templates-rendering.md` |
| Email Provider (12%), Analytics (7%) | `criteria/provider-integration.md` |
| Deliverability (10%), Bounce (10%), Auth (8%), Rate Limiting (8%) | `criteria/security-compliance.md` |

## Step 3: Calculate Weighted Scores

For each category:
```
weighted = raw_score * weight_percent * 10
```

Example: Transactional Email raw 7, weight 15%
```
weighted = 7 * 0.15 * 10 = 10.5
```

Sum all 10 weighted scores for total (0-100).

## Step 4: Assign Grade

| Range | Grade | Range | Grade |
|-------|-------|-------|-------|
| 97-100 | A+ | 80-82 | B- |
| 93-96 | A | 77-79 | C+ |
| 90-92 | A- | 73-76 | C |
| 87-89 | B+ | 60-72 | D |
| 83-86 | B | 0-59 | F |

## Step 5: Generate Issues List

For each category with raw score <= 8, generate an issue:

| Field | Source |
|-------|--------|
| Severity | CRITICAL (0-3), HIGH (4-5), MEDIUM (6-7), LOW (8) |
| Category | Category name |
| Issue | Specific problem description |
| Affected Files | Actual file paths from Step 1 |
| Fix | Actionable recommendation |

Sort issues: CRITICAL first, then HIGH, MEDIUM, LOW.
Within same severity, sort by weight (highest weight first).

## Step 6: Output Scorecard

Fill `assets/templates/scorecard.md.template` with all values:

1. Replace all `{{VARIABLE}}` placeholders
2. Populate issues list sorted by severity
3. Fill Provider Notes section:
   - Resend SDK version from `package.json`
   - Domain verification status
   - Queue provider (QStash / none / other)
   - Webhook endpoint path or "not configured"
4. List 3-5 quick wins (fixable in < 30 minutes)

### Quick Win Criteria

A quick win must be:
- Fixable in a single file change
- No breaking changes
- Immediate score improvement
- Low risk

Examples: add env var validation, add plain text fallback, add rate limit middleware.

## Cross-Reference Checklist

After scoring, verify:
- [ ] All 10 categories have a raw score 0-10
- [ ] Weighted scores sum to total
- [ ] Grade matches total score range
- [ ] Every category with score <= 8 has an issue
- [ ] Issues sorted by severity then weight
- [ ] Provider Notes section filled
- [ ] Quick wins are actionable and specific
