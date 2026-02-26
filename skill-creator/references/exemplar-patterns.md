# Exemplar Patterns — Gold Standard Skills

## payment-integration (Best Reference)

**Why it's the gold standard:**
- SKILL.md = 103 lines (well under 150)
- Acts as pure index: purpose → when to use → platform table → reference directory
- Deep reference hierarchy: subdirectories per provider
- Scripts with tests, .env.example, package.json
- No info duplication between SKILL.md and references

### Structure
```
payment-integration/
├── SKILL.md                          # 103 lines — pure index
├── scripts/
│   ├── checkout-helper.js            # Reusable checkout session code
│   ├── sepay-webhook-verify.js       # SePay webhook verification
│   ├── polar-webhook-verify.js       # Polar webhook verification
│   ├── test-scripts.js               # Tests for all scripts
│   ├── package.json                  # Dependencies + test command
│   └── .env.example                  # Required env vars
└── references/
    ├── implementation-workflows.md   # Step-by-step per platform
    ├── multi-provider-order-management-patterns.md
    ├── sepay/                        # Subdirectory per provider
    │   ├── overview.md
    │   ├── api.md
    │   ├── webhooks.md
    │   ├── sdk.md
    │   ├── qr-codes.md
    │   └── best-practices.md
    ├── polar/                        # 8 files
    ├── stripe/                       # 5 files
    ├── paddle/                       # 7 files
    └── creem/                        # 7 files
```

### SKILL.md Pattern
```markdown
# Heading + brief purpose (1-2 lines)
## When to Use (bullet list of triggers)
## Platform Selection (decision table)
## Quick Reference (organized per-category with file paths)
## Key Capabilities (comparison table)
## Implementation (pointer to workflow reference)
```

## Key Patterns to Copy

### 1. SKILL.md as Pure Index
SKILL.md contains NO detailed documentation. It only has:
- Brief purpose
- Trigger conditions
- Decision tables (which path to take)
- Directory of all references and scripts

### 2. Subdirectory Organization
For complex skills with 5+ reference files per topic, use subdirectories:
```
references/
├── topic-a/
│   ├── overview.md
│   ├── api.md
│   └── best-practices.md
└── topic-b/
    ├── overview.md
    └── webhooks.md
```

### 3. Implementation Workflows Reference
Separate file that sequences which references to load in which order:
```markdown
## Platform A Implementation
1. Load `references/a/overview.md` for auth
2. Load `references/a/api.md` for endpoints
3. Load `references/a/webhooks.md` for events
4. Use `scripts/verify.js` for verification
```

### 4. Scripts with Full Toolchain
```
scripts/
├── main-script.js        # Core functionality
├── helper-script.js       # Utilities
├── test-scripts.js        # Tests for ALL scripts
├── package.json           # { "scripts": { "test": "node test-scripts.js" } }
└── .env.example           # API_KEY=\nSECRET=
```

### 5. Decision Tables in SKILL.md
Quick selection guidance without forcing user to read all references:
```markdown
| Platform | Best For |
|----------|----------|
| SePay | Vietnamese market, VND, bank transfers |
| Stripe | Enterprise, Connect platforms |
```

## verification-before-completion (Simple Skill)

**Why it's a good simple exemplar:** ~40-line SKILL.md, no scripts/assets, single-purpose.

### Structure
```
verification-before-completion/
├── SKILL.md                    # ~40 lines — workflow + checklist
└── references/
    └── verification-steps.md   # Detailed verification process
```

### Key Pattern: Minimal Viable Skill
Not every skill needs scripts, assets, or complex reference trees. A skill can be just SKILL.md + 1 reference if that's all the domain needs.

## api-scoring + api-fix (Scoring/Fix Pair)

**Why it's a good paired exemplar:**
- Two skills that work as audit → remediate pipeline
- Scoring produces scorecard, Fix consumes it
- Mirrored `references/criteria/` ↔ `references/fix-patterns/` structure

### Structure
```
api-scoring/                    api-fix/
├── SKILL.md                    ├── SKILL.md
├── references/                 ├── references/
│   ├── overview.md             │   ├── overview.md
│   ├── scoring-workflow.md     │   ├── implementation-workflow.md
│   └── criteria/               │   └── fix-patterns/
│       ├── authentication.md   │       ├── authentication.md
│       └── error-handling.md   │       └── error-handling.md
└── evals/                      └── evals/
```

### Key Pattern: Paired Skills
- Scoring defines criteria; Fix mirrors them as fix patterns
- Fix SKILL.md references the scoring skill by name
- Both share domain vocabulary and severity definitions

## Anti-Patterns to Avoid

| Anti-Pattern | Fix |
|-------------|-----|
| SKILL.md as documentation (300+ lines) | Move to references, keep SKILL.md as index |
| Flat references (15+ files in root) | Group into subdirectories by topic |
| Repeated info across files | Single source of truth |
| No implementation workflow | Add `implementation-workflows.md` |
| Scripts without tests | Always include test file + runner |
