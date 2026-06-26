---
title: "ccproxy-api"
type: entity
tags: [project, python, oauth, anthropic, openai, fastapi, uvicorn, proxy]
date: 2026-06-26
local_path: ~/.hermes_prod/ccproxy-api (third-party)
---

# ccproxy-api

**Definition**: A Python FastAPI/uvicorn OAuth-injecting proxy that sits between Claude Code / Codex / Copilot and the upstream LLM APIs (api.anthropic.com, api.openai.com). Listens on port 8000 by default. Intercepts OAuth credentials from local storage, injects them as Bearer tokens in the upstream request, and forwards to the real API endpoint. Version 0.2.7 (verified 2026-06-26).

## Routes (verified via `GET /openapi.json` on 0.2.7)

| Path | Method | Notes |
|---|---|---|
| `/claude/v1/messages` | POST | Anthropic OAuth (Claude Code) — `info.title === "CCProxy API Server"` |
| `/claude/v1/chat/completions` | POST | OpenAI-compatible Anthropic |
| `/codex/v1/messages` | POST | OpenAI/Codex OAuth |
| `/copilot/v1/messages` | POST | GitHub Copilot OAuth |
| `/openapi.json` | GET | Service discriminator (returns `{info: {title: "CCProxy API Server"}}`) |
| `/health` | GET | Liveness probe |

**NOT exposed** (verified 2026-06-26):
- `/api/v1/messages` — returns 404
- `/sdk/v1/messages` — uses local Claude SDK instead of OAuth injection; slower, with session state

## Path rewrite (from llm-inspector)

When `llm-inspector` proxies to ccproxy-api (default, no `--upstream` override), it rewrites the incoming `/v1/messages` path to `/claude/v1/messages`:

```typescript
// src/proxy.ts:540-557
const rewrittenPath = upstreamOverride
  ? (req.url || "/")
  : "/claude" + (req.url || "/");
```

This is correct because ccproxy-api 0.2.x does NOT expose `/api/v1/messages` — only `/claude/v1/messages`.

## OAuth storage dependency

ccproxy-api's `oauth_claude` plugin reads `~/.claude/.credentials.json` at startup. If the file is missing, the plugin blocks during startup, logs `server_starting`, but never binds the port. See [[MacOSKeychainOAuthStorage]] for the recovery procedure.

## Service discriminator

`GET http://127.0.0.1:8000/openapi.json` returns `{info: {title: "CCProxy API Server", version: "0.2.7", ...}}`. The `info.title` assertion is the canonical service discriminator. See [[ServiceDiscrimination]].

## Startup latency

ccproxy-api takes 3-12 seconds to bind after `launchctl start` — the OAuth plugins initialize before uvicorn.bind(). Status checks must allow for this delay and re-probe.

## Known ports

- **8000** — default ccproxy-api port (also FastAPI default — port collision risk!)
- **8001** — alternate common config (port 8000 + 1)
- Port collision with [[mem0_server]] (which hardcoded 8000) required moving mem0 to 8100 in 2026-06-26.

## Related entities

- [[llm_inspector]] — primary client (port 9000 → ccproxy :8000)
- [[Claude_Code]] — OAuth credential source (Keychain)
- [[mem0_server]] — formerly port 8000, now 8100

## Related concepts

- [[ServiceDiscrimination]] — port 8000 must be probed, not just `lsof -ti:8000`-checked
- [[MacOSKeychainOAuthStorage]] — OAuth credentials location prerequisite
- [[LaunchdWorkerPIDRace]] — not directly affected, but ccproxy startup latency interacts with status checks