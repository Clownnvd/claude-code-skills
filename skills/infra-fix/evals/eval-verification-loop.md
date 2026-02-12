# Eval: Infrastructure Fix Verification Loop

Verify the compile-test-rescore cycle, regression detection, and fix idempotency for infra-fix.

## Test 1: Compile + Test Verification

**Setup**: Scorecard with CRITICAL issue: no CI pipeline (CI Pipeline 2/10). Apply the GitHub Actions CI Workflow fix from `ci-cd.md` which creates `.github/workflows/ci.yml` with lint, typecheck, test, and build jobs.

**Steps**:
1. Create `.github/workflows/ci.yml` with parallel jobs for lint, typecheck, test, build.
2. Run `npx tsc --noEmit`. Verify the project itself still compiles (no broken imports from new env files).
3. Run `pnpm test`. Verify all existing tests still pass.
4. Validate workflow YAML syntax (correct `on:` triggers, valid `runs-on`, proper `actions/checkout` version).

**Pass**: `tsc --noEmit` exits 0. All tests pass. CI YAML parses without syntax errors. Workflow defines cache keys for `node_modules`. Docker build step (if added) succeeds with `docker build --dry-run .` or equivalent.

**Fail**: YAML syntax error, missing required workflow keys, or new env validation module breaks existing imports.

## Test 2: Re-Score Improvement Verification

**Setup**: Initial infra-scoring scorecard: CI Pipeline 2/10, Environment Mgmt 4/10, Monitoring 3/10. Total 35/100 (D-). Apply fixes for CI workflow (CI Pipeline) and Zod env validation (Environment Mgmt).

**Steps**:
1. Run infra-fix for both issues.
2. Invoke `infra-scoring` to produce a new scorecard.
3. Compare per-category scores: CI Pipeline, Environment Mgmt must increase.
4. Verify Monitoring, Docker, Backup, Integrations, and all other categories remain at or above pre-fix scores.

**Pass**: CI Pipeline >= 6/10 (was 2). Environment Mgmt >= 7/10 (was 4). No category dropped below its pre-fix score. Total weighted score increased. Comparison uses `references/verification.md` format.

**Fail**: Any unfixed category score decreased, or fixed categories show no improvement.

## Test 3: Regression Detection

**Setup**: Initial scorecard: CI Pipeline 8/10, Docker 7/10, Environment Mgmt 7/10. Apply a Docker fix that adds a multi-stage build but removes the `.dockerignore`, causing `node_modules` and `.env` to leak into the image. Docker drops from 7/10 to 3/10.

**Steps**:
1. Apply Docker multi-stage build that deletes `.dockerignore`.
2. Run `infra-scoring` re-score.
3. Verify pipeline detects Docker dropped from 7 to 3 (delta -4).
4. Verify pipeline halts and recommends restoring `.dockerignore`.

**Pass**: Pipeline detects the Docker regression. Output flags: `.dockerignore` removed, image includes `node_modules` and `.env`, before/after delta shown, recommendation to restore ignore file. Pipeline does not continue.

**Fail**: Pipeline ignores the Docker security regression and continues, or reports net improvement without flagging the per-category drop.

## Test 4: Fix Idempotency

**Setup**: Scorecard with CRITICAL issue: no CI pipeline. The `.github/workflows/ci.yml` already exists with lint, typecheck, test, and build jobs from a previous fix run.

**Steps**:
1. Run infra-fix with the same CI pipeline issue.
2. Check `git diff` after the fix attempt.
3. Run `infra-scoring` and compare scores to the post-first-fix scorecard.

**Pass**: No files modified (`git diff` is empty). Score remains identical. Skill reports "already applied" or "no changes needed." No duplicate workflow file or duplicate jobs within the existing file.

**Fail**: Second workflow file created, duplicate jobs appended, existing caching config overwritten, or score changes from the second application.
