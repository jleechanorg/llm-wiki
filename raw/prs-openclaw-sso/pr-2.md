# PR #2: feat: OpenClaw SSO Gateway — full TDD implementation (commits 1–9)

**Repo:** jleechanorg/openclaw_sso
**Merged:** 2026-03-31
**Author:** jleechan2015
**Stats:** +475/-0 in 2 files

## Summary
Complete implementation of the OpenClaw SSO Gateway — a BYOI (Bring Your Own Inference) relay system that lets users expose their local inference server (Ollama, LM Studio, etc.) to any browser or mobile client through a cloud relay, with Firebase as the single auth source.

**Architecture:**
```
Browser → Gateway (port 2003) → Relay (port 2004) → [WebSocket] → Agent binary → OpenClaw (localhost)
```
No VPN, no port forwarding — the agent connects **outbound** to the relay.

## Raw Body
## Summary

Complete implementation of the OpenClaw SSO Gateway — a BYOI (Bring Your Own Inference) relay system that lets users expose their local inference server (Ollama, LM Studio, etc.) to any browser or mobile client through a cloud relay, with Firebase as the single auth source.

**Architecture:**
```
Browser → Gateway (port 2003) → Relay (port 2004) → [WebSocket] → Agent binary → OpenClaw (localhost)
```
No VPN, no port forwarding — the agent connects **outbound** to the relay.

## What's in this PR

### Implementation (9 commits, ~3,600 delta lines)

| Commit | Contents |
|--------|----------|
| 1 | Monorepo scaffold (4 packages: gateway, relay, agent, shared) + wire protocol types |
| 2 | Firebase JWT middleware + Redis node registry |
| 3 | ACL middleware + atomic Lua token bucket rate limiter |
| 4 | Relay WebSocket server + agent registry + `POST /forward` streaming |
| 5 | Agent config + macOS launchd plist template |
| 6 | Agent WsClient (exponential backoff reconnection) + ForwardMessage request handler |
| 7 | Gateway relay client + `POST /v1/chat/completions` route |
| 8 | Audit logging with HMAC-SHA256 integrity signatures |
| 9 | Browser/mobile TypeScript contracts + full-stack E2E test |

### Documentation

- `docs/design.md` — architecture diagram, wire protocol, auth flow, rate limiting, audit logging, security boundaries, full env var reference
- `docs/tdd-impl-plan.md` — 9-commit plan with delta counts, file descriptions, test summaries, and key implementation decisions

### Test coverage (86 tests total, all real local servers)

| Package | Tests |
|---------|-------|
| gateway | 56 |
| relay | 9 |
| agent | 21 |

No mock libraries. All tests use real Redis, real WebSocket connections, real HTTP servers.

The E2E test (`packages/gateway/tests/e2e/fullStack.test.ts`) spins up all four components in-process and verifies a streaming completion request traverses the full path: gateway → relay → agent → mock OpenClaw → back.

## Key technical de
