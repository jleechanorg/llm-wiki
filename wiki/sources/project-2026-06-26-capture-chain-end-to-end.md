---
title: "llm-inspector capture chain wired end-to-end (2026-06-26)"
type: source
tags: [llm-inspector, ccproxy-api, claude-code, hermes_prod, oauth, launchd, port-conflict, false-positive-detection]
date: 2026-06-26
source_file: ../../raw/project_2026-06-26_capture-chain-end-to-end.md
---

## Summary

After three sessions of debugging, the `llm-inspector` capture chain `Claude Code → :9000 → :8000 (ccproxy-api OAuth) → api.anthropic.com` works end-to-end. Verified via direct curl returning HTTP 200 with Anthropic-format response (`11×13 → "143"`). The session uncovered 4 critical gotchas: (1) ccproxy 0.2.x routes are NOT `/api/v1/messages` but `/claude/v1/messages`, (2) Claude Code OAuth lives in macOS Keychain (not `~/.claude/.credentials.json`), (3) `mem0_server.py` hardcodes port 8000 and must be moved to 8100, (4) `lsof -ti:PORT` is not a service discriminator — must probe service-specific endpoint shape. 3 commits landed on main: f1a4be8, 72fbf44, 0ebd4c8.

## Key Claims

- ccproxy-api 0.2.x exposes `POST /claude/v1/messages` (Claude OAuth), `POST /codex/v1/messages`, `POST /copilot/v1/messages` — NOT `/api/v1/messages` (returns 404) and NOT `/sdk/v1/messages` (uses local Claude SDK).
- When `~/.claude/.credentials.json` is missing, ccproxy-api **blocks during startup** — logs `server_starting` but never binds. OAuth tokens for Claude Code 2.x live in macOS Keychain under `Claude Code-credentials-<uuid>`.
- `~/.hermes_prod/mem0_server.py:236` hardcodes `uvicorn.run(app, host="0.0.0.0", port=8000)`. Move to 8100 and update `~/.hermes_prod/mem0.json:2` host to `localhost:8100`.
- `lsof -ti:8000` is NOT a service discriminator (any listener passes). Probe service endpoint and assert shape: `GET /openapi.json` returns `{info.title: "CCProxy API Server"}`.
- Launchd-started worker (`com.jleechan.llm-inspector.plist` runs `_proxy-worker` directly) bypasses `cli start`, so PID file may be stale. `status` must fall back to `lsof -ti:9000 -sTCP:LISTEN` when PID-file check fails.

## Key Quotes

> **Gotcha 2** — "When the JSON file is missing, ccproxy-api blocks during startup — it logs `server_starting` but never binds to the port. Symptom: `lsof -ti:8000 -sTCP:LISTEN` returns nothing despite `launchctl print` showing `state=running, pid=N`."

> **Gotcha 4** — "Both `start` and `status` commands in `src/cli.ts` used `lsof -ti:8000` to detect ccproxy. Any listener passes — mem0_server, ccproxy, jupyter, anything. So if mem0 occupied 8000, cli.ts reported 'ccproxy already running' without actually starting ccproxy."

> **Pattern** — "`lsof -ti:PORT` is fine for *whether anything is listening*; for *whether the right thing is listening*, hit a known endpoint and assert shape. Apply this to all service-detection logic in this repo (and other repos)."

## Connections

- [[llm_inspector]] — the project this capture chain serves; `src/proxy.ts`, `src/cli.ts`, `scripts/llm-inspector-install.sh` all touched this session
- [[ccproxy_api]] — OAuth-injecting proxy at port 8000; OpenAPI route surface verified via `/openapi.json`
- [[Claude_Code]] — the Claude CLI client; OAuth credentials now stored in macOS Keychain under `Claude Code-credentials-<uuid>`
- [[mem0_server]] — Hermes Prod FastAPI service that hardcoded port 8000; moved to 8100 to free 8000 for ccproxy
- [[ServiceDiscrimination]] — concept: `lsof -ti:PORT` is insufficient; must probe service-specific endpoint and assert response shape
- [[LaunchdWorkerPIDRace]] — concept: launchd-started workers bypass `cli start` so PID file can be stale; status needs port-check fallback
- [[MacOSKeychainOAuthStorage]] — concept: Claude Code 2.x stores OAuth tokens in Keychain, not in `~/.claude/.credentials.json`
- [[CaptureVsModifyModeArchitecture]] — pre-existing project design contract (2026-06-24) describing observe vs modify modes

## Source

- `/Users/jleechan/.claude/projects/-Users-jleechan-projects-other-llm-inspector/memory/project_2026-06-26_capture-chain-end-to-end.md`
- Commits on `jleechanorg/llm_inspector` main: `f1a4be8` (proxy path rewrite + cli openapi probe), `72fbf44` (cli status port-check fallback), `0ebd4c8` (.gitignore), `85dbdf5` (install.sh + launchd plists, prior session)

## Open issues

- Capture files record `status: None` and empty response body for successful streaming requests. Proxy captures request bytes but not response bytes. (Tracked as task #66.)
- Real Claude Code 2.1.193 → :9000 returns 400 `context_management: Extra inputs are not permitted`. Direct curl works. Need to strip `context_management` field or set the matching beta header. (Tracked as task #67.)