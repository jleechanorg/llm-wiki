# PR #8: feat: add hybrid client metadata rate limiting

**Repo:** jleechanorg/ai_universe
**Merged:** 2025-09-20
**Author:** jleechan2015
**Stats:** +2548/-208 in 17 files
**Labels:** codex

## Summary
- add a `RateLimitContext` so the rate limiter can build hashed identifiers from IP address, device fingerprint, user agent, and session metadata
- update the second opinion agent and types to accept client metadata and feed it into rate-limit status checks
- expand regression and integration tests plus Jest setup to cover the hybrid identifier flow and ensure CI skips Secret Manager calls

## Raw Body
## Summary
- add a `RateLimitContext` so the rate limiter can build hashed identifiers from IP address, device fingerprint, user agent, and session metadata
- update the second opinion agent and types to accept client metadata and feed it into rate-limit status checks
- expand regression and integration tests plus Jest setup to cover the hybrid identifier flow and ensure CI skips Secret Manager calls

## Testing
- npm test

------
https://chatgpt.com/codex/tasks/task_e_68ccaf894c18832fa9d60d2bbd0f3135
