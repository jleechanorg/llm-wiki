# PR #4: [openclaw_sso] fix: critical bugs in auth, rate limiter, relay auth

**Repo:** jleechanorg/openclaw_sso
**Merged:** 2026-03-31
**Author:** jleechan2015
**Stats:** +60/-14 in 5 files

## Summary
OpenClaw SSO acts as a cloud relay for agent nodes. Several critical bugs in the middleware and relay codebase prevent it from functioning correctly based on the design document.

## Background
OpenClaw SSO acts as a cloud relay for agent nodes. Several critical bugs in the middleware and relay codebase prevent it from functioning correctly based on the design document.

## Raw Body
## Background
OpenClaw SSO acts as a cloud relay for agent nodes. Several critical bugs in the middleware and relay codebase prevent it from functioning correctly based on the design document.

## Goals
Fix identified bugs in the gateway middleware (auth, rate limiting) and relay functionality (authentication strategy, headers processing) to strictly adhere to the `docs/design.md` specifications.

## Tenets
- Follow `docs/design.md` accurately.
- No silent failures — errors should be returned explicitly instead of being swallowed.

## High-level description
- **Gateway `auth.ts`**: Moved `next()` outside the `try/catch` block so valid downstream errors process normally and don't mistakenly get recast as 401 unauthenticated errors.
- **Gateway `rateLimiter.ts`**: Implemented distinct atomic Lua scripts (`LUA_CONSUME` and `LUA_CONSUME_CONCURRENCY`) to ensure per-node currency limitations do not erroneously roll back token window TTLs, fixing the read-then-write race condition by switching to proper atomic Lua operations for tracking capacity. 
- **Relay `wsServer.ts`**: Switched from Firebase JWT validation to matching SHA256 hashed node tokens against Redis `NodeRecord` properties, matching the documented Relay design. 
- **Relay `app.ts`**: Explicitly handled checking `res.headersSent` to prevent HTTP context crashes caused by re-assigning status codes or writing when headers have already been sent mid-stream. 

## Testing
- Performed `npm test` successfully passing all 93 tests across 16 test suites.

## Low-level details
- `packages/gateway/src/middleware/auth.ts`: Adjusted execution flow for `next()`.
- `packages/gateway/src/services/rateLimiter.ts`: Split Lua functionality and incorporated `isConcurrency` param for node limiting logic.
- `packages/gateway/src/middleware/rateLimit.ts`: Corrected call schema for `consume`. 
- `packages/relay/src/wsServer.ts`: Revised `validateToken` function to query Redis for `NodeRecord` hashes instead of invoking Firebase SDK l
