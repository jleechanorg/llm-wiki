# PR #1: Add OpenClaw gateway, relay, and agent services with full integration

**Repo:** jleechanorg/openclaw_sso
**Merged:** 2026-03-31
**Author:** jleechan2015
**Stats:** +13536/-0 in 67 files

## Summary
This PR introduces the complete OpenClaw inference platform consisting of three core services (gateway, relay, agent) plus a shared protocol library. The system enables users to register local inference endpoints and route requests through a centralized gateway with authentication, rate limiting, and audit logging.

## Raw Body
## Summary

This PR introduces the complete OpenClaw inference platform consisting of three core services (gateway, relay, agent) plus a shared protocol library. The system enables users to register local inference endpoints and route requests through a centralized gateway with authentication, rate limiting, and audit logging.

## Key Changes

### New Services

- **Gateway** (`packages/gateway/`) — HTTP API server that authenticates requests via Firebase, enforces ACL/rate limits, and forwards inference requests to the relay
- **Relay** (`packages/relay/`) — WebSocket server that maintains persistent connections to agent instances and routes inference requests bidirectionally
- **Agent** (`packages/agent/`) — Daemon binary that connects to the relay and proxies requests to local OpenClaw/Ollama servers
- **Shared** (`packages/shared/`) — Protocol definitions and type contracts for browser/mobile clients

### Gateway Features

- `POST /v1/chat/completions` endpoint with full middleware chain:
  - Firebase ID token authentication
  - ACL enforcement (endpoint ownership validation)
  - Token bucket rate limiting (per-user and per-node)
  - Request sanitization (strips internal headers)
  - Audit logging with HMAC-SHA256 signatures
- Redis-backed rate limiter with atomic Lua scripts
- Node registry for managing endpoint metadata
- Streaming NDJSON responses from agents

### Relay Features

- WebSocket server at `/agent` for agent registration and request routing
- Token validation (injectable for testing)
- Pending request registry for bidirectional message routing
- Health check endpoint
- Automatic agent presence tracking in Redis

### Agent Features

- Persistent WebSocket client with exponential backoff reconnection
- HTTP request proxying to local OpenClaw/Ollama endpoints
- Chunked response streaming back to relay
- CLI configuration via flags or environment variables
- macOS launchd daemon support (plist included)

### Shared Protocol

- `RegisterMessage` / `Regi
