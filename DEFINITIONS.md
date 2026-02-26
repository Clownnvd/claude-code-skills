# Shared Definitions

Common terms used across all skills.

## Scoring Terms

| Term | Definition |
|------|-----------|
| **Raw Score** | Per-category score, 0-10 scale. 7 = baseline (meets basic expectations). |
| **Weighted Score** | Raw × weight%. Sum of all weighted scores = total (0-100). |
| **Grade** | Letter grade from total score. See Grade Scale. |
| **Severity** | Issue priority: CRITICAL (0-3, security hole), HIGH (4-5), MEDIUM (6-7), LOW (8). |
| **Weight** | Category importance as percentage. All weights sum to 100%. |
| **Scorecard** | Full audit output: category scores, grade, issues list, quick wins. |

## Grade Scale (Standard)

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 73-76 |
| A- | 90-92 | B- | 80-82 | D | 60-72 |
| | | | | F | <60 |

## Fix Terms

| Term | Definition |
|------|-----------|
| **Fix Report** | Output of fix mode: before/after code, re-score comparison. |
| **Priority Matrix** | Severity × weight ordering. CRITICAL first, then HIGH+high-weight. |
| **Plateau** | Score unchanged after a full fix cycle. Triggers loop stop. |
| **Re-score** | Running score mode again after fixes to measure improvement. |
| **Delta** | Score difference: after - before. Positive = improvement. |

## Loop Terms

| Term | Definition |
|------|-----------|
| **Loop Mode** | Automated score → fix → re-score cycle until target grade. |
| **Target Grade** | Grade to reach before stopping. Default: B+ (87+) production, A- (90+) enterprise. |
| **Max Iterations** | Hard stop at 5 iterations to prevent infinite loops. |
| **Regression Guard** | Halt if any category score drops between iterations. |

## Quality Gates

| Context | Minimum Grade | Score |
|---------|--------------|-------|
| Prototype | C+ | 77+ |
| Production | B+ | 87+ |
| Enterprise | A- | 90+ |
| Showcase | A+ | 97+ |

## Cross-Skill Boundaries

When categories overlap between skills, each skill audits its own perspective. Use this table to decide which skill to run.

| Overlap Area | Skill A | Skill B | Boundary |
|-------------|---------|---------|----------|
| Prisma queries | dataflow | database | dataflow = app-code query patterns; database = schema & indexing |
| API routes | dataflow | api | dataflow = data flow through routes; api = route architecture |
| Cache strategy | dataflow | caching | dataflow = cache in pipelines; caching = cache config & headers |
| Auth in routes | api | auth | api = auth middleware pattern; auth = auth system design |
| Security headers | auth | security | auth = auth-specific headers (CSRF, session); security = all headers (CSP, HSTS) |
| Input validation | api | security | api = request schema validation (Zod); security = sanitization & injection defense |
| Error handling | api | security | api = error response format; security = info disclosure prevention |
| Rate limiting | api | auth | api = general rate limit architecture; auth = auth-route-specific limits |
| Monitoring | api | infrastructure | api = API observability; infrastructure = system monitoring & alerting |
| Security (broad) | api | security | api = route-level security (20%); security = full OWASP audit (10 categories) |
| Query performance | database | scalability | database = indexing & schema optimization; scalability = query patterns & caching |
| Server components | dataflow | scalability | dataflow = RSC data fetching; scalability = RSC architecture for bundle/perf |
| CDN & edge | caching | scalability | caching = CDN cache config & headers; scalability = edge runtime optimization |
| Backup & recovery | database | infrastructure | database = data backup & PITR; infrastructure = system-level DR & RTO/RPO |
| Security in deploy | infrastructure | security | infrastructure = container/CI security (4%); security = full security posture |
