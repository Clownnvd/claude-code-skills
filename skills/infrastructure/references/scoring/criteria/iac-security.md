# Infrastructure as Code (4%) + Security in Deployment (4%)

## Category 9: Infrastructure as Code — 4%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Infra configs version-controlled | All deploy/infra configs in git (not manual console) |
| 2 | Reproducible environments | Can spin up new environment from code alone |
| 3 | IaC tool usage | Terraform, Pulumi, CDK, or platform config files |
| 4 | Plan before apply | Changes reviewed before applying (PR-based infra) |
| 5 | Environment parity | Dev, staging, prod use same infra definitions |
| 6 | Drift detection | Can detect manual changes that diverge from code |
| 7 | Modular configs | Reusable modules/templates, not monolithic config |
| 8 | State management | Remote state storage with locking (Terraform state) |
| 9 | Secrets separated | Infra secrets not in IaC files (use secret refs) |
| 10 | Documented architecture | Infrastructure diagram or documentation |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met — full IaC maturity |
| 8-9 | IaC tool + version control + reproducible + plan-before-apply |
| 6-7 | Platform config files versioned, mostly reproducible |
| 4-5 | Some configs in git, some manual setup |
| 2-3 | Mostly manual with a few config files |
| 0-1 | Entirely manual infrastructure |

### Platform Adjustments

**Vercel**: `vercel.json` in git = criterion 1. `git push` deploys = reproducible (criterion 2). Vercel project settings in dashboard = partial criterion 5. Score more leniently — serverless platforms handle most IaC concerns.

**Small Project (<5 devs)**: IaC weight (4%) may redistribute to Environment Management (+4%) per scoring-workflow.md.

---

## Category 10: Security in Deployment — 4%

Score 0-10 based on how many criteria are met:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Container image scanning | Trivy, Snyk, or GitHub Dependabot on images |
| 2 | Dependency vulnerability scanning | `npm audit`, Dependabot, or Snyk on packages |
| 3 | Secret injection at runtime | Secrets injected via env, not baked into images/bundles |
| 4 | Least privilege principle | Deploy roles have minimum required permissions |
| 5 | Network policies | Firewall rules, VPC, or platform-level restrictions |
| 6 | SBOM generation | Software Bill of Materials for deployed artifacts |
| 7 | Signed artifacts | Deploy artifacts are signed/verified |
| 8 | Audit logging for deploys | Who deployed what, when — tamper-resistant log |
| 9 | No secrets in logs | Log sanitization (no tokens/keys in output) |
| 10 | Compliance checks | Automated policy checks (OPA, Checkov) |

### Scoring Guide

| Score | Criteria Met |
|-------|-------------|
| 10 | All 10 criteria met — enterprise deployment security |
| 8-9 | Scanning + runtime secrets + least privilege + audit |
| 6-7 | Dependency scanning + runtime secrets |
| 4-5 | Basic scanning, secrets mostly handled |
| 2-3 | Minimal security in deployment |
| 0-1 | No deployment security measures |

### Platform Adjustments

**Vercel**: Secrets via Vercel env vars = criterion 3. Vercel handles network isolation = partial criterion 5. GitHub Dependabot = criterion 2. Score more leniently.

**Small Project (<5 devs)**: Deployment Security weight (4%) may redistribute to Monitoring (+4%) per scoring-workflow.md.

### Common Deductions

- No dependency scanning (npm audit, Dependabot) → -2
- Secrets in build output or client bundle → -3 (CRITICAL)
- Deploy with admin/root permissions → -1
- No audit trail for who deployed → -1
