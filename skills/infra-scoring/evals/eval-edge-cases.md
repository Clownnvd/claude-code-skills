# Infrastructure Scoring — Edge Cases Eval

Verify correct behavior for infrastructure-specific edge cases.

## Test 1: No CI/CD Pipeline Configured

- Run against a codebase with no GitHub Actions or CI config files
- Verify CI Pipeline and CD Pipeline both score 0
- Verify CRITICAL issue flags absence of automated testing
- Verify Production Deploy also penalized (no automated path)

## Test 2: Dockerfile Without Multi-Stage Build

- Provide a single-stage Dockerfile including dev dependencies in final image
- Verify Containerization scores <= 4
- Verify issue flags bloated image size
- Verify fix recommends multi-stage build with separate builder stage

## Test 3: Hardcoded Secrets in CI Config

- Provide workflow YAML with hardcoded API keys or passwords
- Verify Environment Management scores <= 1 (CRITICAL)
- Verify Security in Deployment also penalized
- Verify issue recommends GitHub Secrets or vault injection

## Test 4: No Health Check Endpoints

- Provide deployed service with no `/health` or readiness probe
- Verify Monitoring & Observability scores <= 3
- Verify issue recommends health check endpoint with dependency checks
- Verify Backup/DR also checked for recovery detection

## Test 5: No Rollback Strategy

- Provide deployment config with no rollback mechanism
- Verify Production Deploy scores <= 3
- Verify issue flags risk of stuck bad deployments
- Verify fix recommends blue-green, canary, or version pinning

## Test 6: Third-Party Calls Without Timeout

- Provide code calling external APIs without timeout or retry logic
- Verify Third-Party Integrations scores <= 3
- Verify issue recommends timeout, retry with backoff, and circuit breaker
- Verify affected external call sites listed

## Test 7: Missing .dockerignore

- Provide Docker setup with no `.dockerignore` file
- Verify Containerization penalized for including node_modules, .git, .env
- Verify Security in Deployment also flagged for secret leak risk
