# Pre-Launch Roadmap for mvp_site

**Created**: 2026-03-18  
**Review Scope**: Production launch readiness for WorldArchitect.AI MVP site  
**Review Method**: Static code analysis of all files in mvp_site/ directory

---

## Executive Summary

This document outlines the findings from a comprehensive security and production readiness review of the WorldArchitect.AI mvp_site codebase. The application is a Flask-based API gateway with Firebase Authentication, Firestore database, and Google Gemini AI integration. Overall, the codebase demonstrates solid security practices, but several items require attention before external launch.

**Overall Readiness Assessment**: 🟡 MEDIUM-HIGH (Address items in this roadmap for production)

---

## 1. Security Issues Found

### 1.1 Authentication & Authorization

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| Auth bypass in non-production mode | 🟡 Medium | main.py:1334-1449 | TESTING_AUTH_BYPASS and SMOKE_TOKEN allow authentication bypass. Must ensure PRODUCTION_MODE=true is enforced in production |
| Hardcoded test email in rate limit exempt | 🟡 Low | rate_limiting.py:39 | `jleechan@gmail.com` hardcoded as exempt. Consider environment-based configuration |
| Token expiry tolerance too generous | 🟡 Low | main.py:1525 | Extended token tolerance (12 min) could allow expired tokens to be accepted |

**Action Items**:
- [ ] **P1**: Ensure `PRODUCTION_MODE=true` environment variable is set in production deployments
- [ ] **P2**: Add validation that TESTING_AUTH_BYPASS cannot be enabled in production
- [ ] **P3**: Move hardcoded exempt emails to environment variable configuration

### 1.2 API Security

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| CORS origins limited | 🟢 Good | main.py:316-326 | CORS restricted to specific origins (localhost:3000, localhost:5000, worldarchitect.ai) |
| Rate limiting implemented | 🟢 Good | main.py + rate_limiting.py | Flask-Limiter + custom rate limiting with BYOK elevated limits |
| CSP headers present | 🟢 Good | main.py:1104-1120 | Strict CSP with script-src whitelist, frame-ancestors: none |

**Action Items**:
- [ ] **P2**: Review CORS origins - currently missing preview/subdomain variations

### 1.3 Data Validation

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| Input validation on settings | 🟢 Good | settings_validation.py | Comprehensive validation for LLM providers, models, gateway URLs |
| Schema validation for game state | 🟢 Good | schemas/validation.py | JSON Schema validation with Draft202012012Validator |
| Campaign ID validation | 🟡 Low | main.py:1619 | Sort fields are whitelisted but campaign_id validation could be stricter |

**Action Items**:
- [ ] **P3**: Add explicit campaign_id format validation (e.g., UUID pattern)

### 1.4 LLM Security (Prompt Injection)

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| LLM outputs not sanitized before display | 🟡 Medium | Multiple locations | AI-generated content rendered to users without output sanitization |
| No prompt injection detection | 🟡 Medium | agent_prompts.py | No systematic detection/monitoring for prompt injection attempts |

**Action Items**:
- [ ] **P2**: Add output sanitization for AI-generated content before rendering
- [ ] **P3**: Implement prompt injection detection and logging

---

## 2. Bugs & Gaps

### 2.1 Authentication Flow

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| Token refresh race condition | 🟡 Medium | frontend_v1/api.js:130-145 | Potential race condition between token refresh and API calls |
| Clock skew compensation | 🟡 Low | frontend_v1/api.js:1-90 | Client-side clock skew detection but limited server-side tolerance |

### 2.2 Error Handling

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| Generic error messages | 🟡 Low | main.py:2947 | Error responses sanitized but could provide more actionable guidance |
| No structured error codes | 🟡 Low | Multiple locations | Error handling uses string messages rather than structured error codes |

### 2.3 Missing Error Handling

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| MCP server unavailable | 🟡 Medium | mcp_client.py | No graceful degradation if MCP server is down |
| Firestore connection failures | 🟡 Medium | firestore_service.py | Limited retry logic for transient failures |

**Action Items**:
- [ ] **P2**: Add MCP server health check and graceful degradation
- [ ] **P2**: Implement Firestore retry with exponential backoff
- [ ] **P3**: Add structured error codes for common failure scenarios

---

## 3. Performance Considerations

### 3.1 Cold Start Issues

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| Lazy module loading | 🟢 Good | main.py:116-145 | Implemented lazy loading for heavy imports (google.genai, firestore) |
| Firestore warmup | 🟢 Good | main.py:147-175 | Background thread for Firestore warmup |

### 3.2 Database Performance

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| Query pagination | 🟡 Low | firestore_service.py | Implemented but could benefit from cursor-based pagination for large datasets |
| Connection pooling | 🟢 Good | mcp_client.py:118-145 | HTTP connection pooling configured with appropriate pool sizes |

### 3.3 Rate Limiting Performance

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| In-memory cache for rate limits | 🟢 Good | rate_limiting.py:62-73 | TTLCache with bounded size for user settings |
| Lock contention | 🟡 Low | rate_limiting.py:75 | Thread lock on cache operations could be optimized |

**Action Items**:
- [ ] **P3**: Consider Redis-based rate limiting for distributed deployments

---

## 4. Missing Features for Production

### 4.1 Monitoring & Observability

| Feature | Priority | Description |
|---------|----------|-------------|
| Metrics export | 🟡 Medium | No Prometheus/DataDog integration for metrics |
| Distributed tracing | 🟡 Medium | No request tracing across MCP calls |
| Uptime monitoring | 🟡 Low | Health check endpoint exists (/health) but no comprehensive monitoring |

### 4.2 Backup & Recovery

| Feature | Priority | Description |
|---------|----------|-------------|
| Database backup | 🟡 Medium | Firestore has built-in backup, but no application-level backup verification |
| Disaster recovery plan | 🟡 Low | No documented DR procedures for mvp_site |

### 4.3 Documentation

| Feature | Priority | Description |
|---------|----------|-------------|
| API documentation | 🟡 Medium | No OpenAPI/Swagger docs for API endpoints |
| Runbook | 🟡 Low | No operational runbook for common issues |

**Action Items**:
- [ ] **P2**: Add Prometheus metrics endpoint
- [ ] **P3**: Create API documentation with OpenAPI spec
- [ ] **P3**: Document operational runbook

---

## 5. Technical Debt

### 5.1 Code Quality

| Issue | Priority | Location | Description |
|-------|----------|----------|-------------|
| Large main.py file | 🟡 Medium | main.py (4000+ lines) | Consider splitting into route modules |
| Test coverage gaps | 🟡 Medium | tests/ | Some modules lack comprehensive tests |
| Magic numbers | 🟡 Low | Multiple locations | Hardcoded values should be in constants.py |

### 5.2 Dependencies

| Issue | Priority | Description |
|-------|----------|-------------|
| Outdated dependencies | 🟡 Low | Review requirements.txt for updates |
| Unused dependencies | 🟡 Low | Some imports may be unused |

### 5.3 Configuration

| Issue | Priority | Description |
|-------|----------|-------------|
| Environment configuration | 🟡 Medium | Some configuration in code rather than env vars |
| Secrets management | 🟡 Medium | API keys should use secret management service |

**Action Items**:
- [ ] **P2**: Extract remaining hardcoded values to configuration
- [ ] **P3**: Run dependency audit and remove unused packages

---

## 6. Testing Gaps

### 6.1 Security Testing

| Test | Priority | Description |
|------|----------|-------------|
| Penetration testing | 🟡 Medium | No external security audit performed |
| Auth flow testing | 🟡 Low | Test coverage exists but could be expanded |
| Rate limit bypass testing | 🟡 Low | Verify rate limits cannot be bypassed |

### 6.2 Integration Testing

| Test | Priority | Description |
|------|----------|-------------|
| End-to-end tests | 🟡 Medium | Limited E2E test coverage |
| Load testing | 🟡 Low | No load testing performed |

### 6.3 Frontend Testing

| Test | Priority | Description |
|------|----------|-------------|
| Browser automation | 🟡 Low | Playwright tests exist in testing_ui/ but limited |
| Cross-browser testing | 🟡 Low | No cross-browser matrix testing |

**Action Items**:
- [ ] **P2**: Conduct security audit/penetration testing before launch
- [ ] **P2**: Expand integration test coverage
- [ ] **P3**: Add load testing to CI/CD pipeline

---

## 7. Action Items Summary

### Priority 1 (Must Fix Before Launch)

| # | Action Item | Files Affected |
|---|-------------|----------------|
| 1.1 | Ensure PRODUCTION_MODE=true is enforced | main.py, deployment config |
| 1.2 | Validate TESTING_AUTH_BYPASS disabled in production | main.py |
| 1.3 | Add output sanitization for AI-generated content | frontend_v1/app.js, main.py |
| 1.4 | Add MCP server health check and graceful degradation | mcp_client.py, main.py |

### Priority 2 (Should Fix Before Launch)

| # | Action Item | Files Affected |
|---|-------------|----------------|
| 2.1 | Move hardcoded exempt emails to environment config | rate_limiting.py |
| 2.2 | Add explicit campaign_id format validation | main.py |
| 2.3 | Implement Firestore retry with exponential backoff | firestore_service.py |
| 2.4 | Add Prometheus metrics endpoint | main.py |
| 2.5 | Conduct security audit/penetration testing | N/A |
| 2.6 | Expand integration test coverage | tests/ |

### Priority 3 (Nice to Have Before Launch)

| # | Action Item | Files Affected |
|---|-------------|----------------|
| 3.1 | Create API documentation with OpenAPI spec | docs/ |
| 3.2 | Document operational runbook | docs/ |
| 3.3 | Add structured error codes | main.py, error handling |
| 3.4 | Consider Redis-based rate limiting | rate_limiting.py |
| 3.5 | Run dependency audit | requirements.txt |
| 3.6 | Add load testing to CI/CD | CI config |

---

## 8. Positive Security Observations

The codebase has several strong security practices:

1. **Firebase Authentication** - Enterprise-grade auth with proper token verification
2. **Rate Limiting** - Multi-layer rate limiting (Flask-Limiter + custom)
3. **CSP Headers** - Strict Content Security Policy implemented
4. **Input Validation** - Comprehensive validation for settings and schemas
5. **Security Headers** - X-Content-Type-Options, X-Frame-Options, HSTS
6. **Preventive Guards** - LLM output hardening to prevent state corruption
7. **API Key Redaction** - Logging sanitizes sensitive values
8. **Firestore Security Rules** - (Assumes Firestore rules properly configured)

---

## Appendix: Key Files Reviewed

| Category | Files |
|----------|-------|
| Authentication | main.py (check_token, auth routes), frontend_v1/auth.js, frontend_v1/api.js |
| Rate Limiting | rate_limiting.py, main.py (limiter configuration) |
| Data Validation | schemas/validation.py, settings_validation.py, entity_validator.py |
| Database | firestore_service.py |
| API Client | mcp_client.py |
| Security Guards | preventive_guards.py |
| Frontend | frontend_v1/app.js, frontend_v1/api.js, frontend_v1/auth.js |
| Configuration | constants.py, settings_validation.py |

---

*This document should be updated as issues are addressed and new findings emerge.*
