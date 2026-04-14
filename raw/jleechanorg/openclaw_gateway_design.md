# OpenClaw Gateway Integration Design + Implementation Plan

_Last updated: 2026-02-18_

## 🎯 Goals
- Implement OpenClaw as a first-class LLM provider.
- Entry points:
  - `mvp_site/llm_providers/openclaw_provider.py`: `generate_content`, `generate_content_stream_sync`
  - `mvp_site/llm_service.py`: Provider dispatch and port retrieval
- Support configurable gateway port (local developer flow).

## Non-Goals

- No OpenClaw server modifications.
- No user-visible workflow changes to campaign/story semantics.
- No reduction in LLM context visibility (full request context continues to be sent).

## Existing Architecture Fit

`mvp_site/llm_service.py` already centralizes provider selection and dispatch via provider modules under `mvp_site/llm_providers/`. OpenClaw integration is implemented as another provider module with:

- `generate_content(...)`
- `generate_content_with_tool_requests(...)`
- `generate_content_stream_sync(...)`

This allows no callsite-level feature flags and preserves current request construction and parser flows.

## Protocol/Transport Design

### Connection lifecycle

- Single process-level OpenClaw client singleton.
- Lazy connect on first request.
- Handshake request:
  - `method=connect`
  - `minProtocol=3`
  - `maxProtocol=3`
  - role/scope/client metadata.
- Optional `connect.challenge` events are accepted and ignored for local setups.

### Request flow

- Use `agent.invoke` per request.
- Message payload uses complete prompt content as user message plus optional server system instruction.
- Support both non-streaming and streaming calls.

### Streaming flow

- Consume `event=stream.chunk` and emit chunk text progressively.
- Finish on matching `res` id.

### Reliability

- Keep-alive ping every 45s while socket is active.
- Hard inactivity timeout of 20 minutes closes idle socket.
- Reconnect on next request when idle-disconnected.
- Return explicit actionable errors when gateway unavailable.

## Part 1: Local Development (OpenClaw-first)

1. Add `openclaw` provider constants and selection support.
2. Implement OpenClaw provider module with persistent WS client.
3. Wire dispatch in `llm_service` for normal + tool-request flow.
4. Enable streaming for OpenClaw in the same event pipeline as Gemini.
5. Add tests for provider selection and transport protocol behavior.

## Part 2: GCP Runtime + Local OpenClaw Auth/Inference

1. Keep Cloud Run service as deployment target.
2. Continue standard API server operation; choose `openclaw` as provider in user settings.
3. Set `OPENCLAW_GATEWAY_URL` via environment so runtime points at reachable OpenClaw endpoint (local sidecar/tunnel/connector pattern as deployment requires).
4. Keep fallback provider settings available (Gemini/OpenRouter/Cerebras) for outage handling.
5. Add runbook validation checks:
   - handshake success logs
   - stream chunk throughput
   - inactivity timeout close/reconnect behavior

## TDD Plan

1. **Red**: Add failing tests for provider selection (`llm_provider=openclaw`) and model defaults.
2. **Red**: Add failing provider transport tests:
   - handshake payload protocol fields
   - non-stream response assembly
   - stream chunk aggregation
3. **Green**: Implement provider + llm_service dispatch updates.
4. **Refactor**: Keep provider API consistent with existing provider utils and tool request flow.

## Operational Notes

- Gateway unavailability should fail fast with guidance to run `openclaw gateway`.
- OpenClaw remains optional per user/provider setting; existing providers still supported.
- Server-side tool execution remains mandatory and unchanged.
