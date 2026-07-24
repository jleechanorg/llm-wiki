---
name: capture-chain-wired-end-to-end-claude-code-9000-8000-anthropic
description: "Full chain works as of 2026-06-26; documents the 4 gotchas discovered and the install/launchd plist architecture. Reference for any future \"proxy returns 4xx\" debugging."
metadata: 
  node_type: memory
  type: project
  bead: none
  originSessionId: 467fa320-c605-44a9-ae9a-876c00f8d204
---

# Capture chain wired end-to-end (2026-06-26)

After three sessions of debugging, the capture chain is working:

```
Claude Code → :9000 (llm-inspector capture) → :8000 (ccproxy-api OAuth) → api.anthropic.com
```

Verified via direct curl → `HTTP 200` with Anthropic-format response (`usage.input_tokens`, `output_tokens`, `model`, `id`).

## What landed (commits on main)

```
0ebd4c8 chore(gitignore): exclude .claude/ (local AO worktree state)
72fbf44 fix(cli): status falls back to port-check when PID file is stale
f1a4be8 fix(cli+proxy): probe ccproxy-api by OpenAPI title; rewrite path to /claude
85dbdf5 feat(scripts+cli): install + launchd auto-start ccproxy-api alongside llm-inspector
```

## Gotcha 1 — ccproxy-api 0.2.x routes are NOT what older docs say

ccproxy-api 0.2.7 (current) exposes:

- `POST /claude/v1/messages` — Claude OAuth (used by Claude Code) ✓
- `POST /codex/v1/messages` — Codex OAuth
- `POST /copilot/v1/messages` — Copilot

It does **NOT** serve `/api/v1/messages` (returns 404) or `/sdk/v1/messages` (sdk route uses local Claude SDK, slower + session-bound).

The old `~/.ccproxy/ccproxy.yaml` referenced `/api/v1/messages` via the LiteLLM-based ccproxy. That config is **stale** — current ccproxy has its own OAuth plugin (`oauth_claude`) that reads `~/.claude/.credentials.json` directly.

**FIX in proxy.ts**: `src/proxy.ts:545-557` rewrites the path from `/v1/messages` to `/claude/v1/messages` when no `--upstream` override is set. Direct upstreams (Wafer, Anthropic) bypass the rewrite.

**How to verify**: `curl http://127.0.0.1:8000/openapi.json | jq '.paths | keys'` — lists every route ccproxy serves. If a route is missing, the rewrite is wrong.

## Gotcha 2 — Claude Code OAuth credentials live in macOS Keychain, not the JSON file

Newer Claude Code (2.x) writes OAuth tokens to **macOS Keychain** under `Claude Code-credentials-<uuid>`, not to `~/.claude/.credentials.json`. The JSON file is the old format from Claude Code 1.x and only contains backups.

When the JSON file is missing, ccproxy-api **blocks during startup** — it logs `server_starting` but never binds to the port. Symptom: `lsof -ti:8000 -sTCP:LISTEN` returns nothing despite `launchctl print` showing `state=running, pid=N`.

**Recovery path**:

```bash
# 1. List Claude Code keychain entries (cull by cdat field — pick most recent)
security dump-keychain 2>/dev/null | grep -B1 -A3 "Claude Code" | grep -E "(svce|cdat)"

# 2. Read the freshest entry (account=jleechan)
security find-generic-password -s "Claude Code-credentials-8aadb663" -a "jleechan" -w \
  > ~/.claude/.credentials.json
chmod 600 ~/.claude/.credentials.json

# 3. Restart ccproxy so it picks up the new file
launchctl kickstart -k "gui/$(id -u)/com.jleechan.ccproxy-api"

# 4. Wait ~12s for plugin initialization, then verify port 8000 is bound
lsof -ti:8000 -sTCP:LISTEN
```

Backup files at `~/.claude/.credentials.json.YYYYMMDD-HHMMSS.bak` are 2-month-old in this environment — refreshToken may still work but accessToken is long expired. Always restore from Keychain.

## Gotcha 3 — mem0_server occupies port 8000 (collides with ccproxy default)

`/Users/jleechan/.hermes_prod/mem0_server.py:236` hardcodes `uvicorn.run(app, host="0.0.0.0", port=8000)`. It also binds `0.0.0.0`, so it accepts connections from any interface — Claude-format POSTs get a `{"detail":"Not Found"}` FastAPI response.

**Resolution (moved mem0 to :8100)**:

1. `~/.hermes_prod/mem0_server.py:236` → `port=8100`
2. `~/.hermes_prod/mem0.json:2` → `"host": "http://localhost:8100"`
3. `launchctl kickstart -k gui/$UID/ai.hermes-mem0-server`
4. Verify: `curl http://127.0.0.1:8100/health` → `{"status":"ok"}`

**Side effect (harmless)**: `claude_start.sh` (hermes_prod) checks `curl localhost:8000/health` to detect a "Qwen API proxy." After this move, that check fails for everyone → script falls through to its default branch. The "Qwen API proxy" feature appears to be dead code (no Qwen proxy is installed).

## Gotcha 4 — `lsof -ti:PORT` is NOT a service discriminator

Both `start` and `status` commands in `src/cli.ts` used `lsof -ti:8000` to detect ccproxy. Any listener passes — mem0_server, ccproxy, jupyter, anything. So if mem0 occupied 8000, cli.ts reported "ccproxy already running" without actually starting ccproxy.

**FIX**: Probe the service-specific endpoint. For ccproxy, `GET /openapi.json` returns `{info.title: "CCProxy API Server"}` — that's the discriminator. See `src/cli.ts:62-79, 320-353`.

**Pattern**: `lsof -ti:PORT` is fine for *whether anything is listening*; for *whether the right thing is listening*, hit a known endpoint and assert shape. Apply this to all service-detection logic in this repo (and other repos).

## Gotcha 5 — launchd-started worker bypasses `cli start`, breaks PID file

`com.jleechan.llm-inspector.plist` runs `node dist/cli.js _proxy-worker` directly. It never goes through `cli start`, so the PID file is never written by the launchd-managed worker. Then a subsequent `cli start` from the shell overwrites the PID file with the parent `cli` process PID (17531), not the grandchild worker PID (98652). Result: `status` reports STOPPED while `:9000` answers requests.

**FIX**: `src/cli.ts:312-334` falls back to `lsof -ti:9000 -sTCP:LISTEN` when the PID file check fails. Worst case shows the listener's PID; best case the existing PID-file path still works.

## Install + launchd architecture

`scripts/llm-inspector-install.sh` regenerates both plists idempotently:

- `~/Library/LaunchAgents/com.jleechan.llm-inspector.plist` — runs `_proxy-worker --port 9000`
- `~/Library/LaunchAgents/com.jleechan.ccproxy-api.plist` — runs `ccproxy serve --port 8000`

Both have `KeepAlive=true` and `RunAtLoad=true`. After install:

```bash
launchctl start com.jleechan.ccproxy-api    # OAuth proxy first
launchctl start com.jleechan.llm-inspector  # capture proxy second
```

ccproxy takes ~3-12s to initialize OAuth plugins before binding — don't expect instant port binding.

## Known open issues (tracked as tasks #66, #67)

- **#66**: Capture files record `status: None` and empty response body for successful streaming requests. The proxy captures request bytes but not response bytes.
- **#67**: Real Claude Code 2.1.193 → :9000 returns 400 `context_management: Extra inputs are not permitted`. Claude Code sends `context_management: {edits: [{type: clear_thinking_20251015, keep: all}]}` without the matching beta header (`context-management-2025-06-27`). Direct curl works (HTTP 200). Need to either strip the field in the proxy or set the right beta header.

## Bashrc wrappers

`~/.bashrc` (added 2026-06-24, around line 939+):

```bash
LLM_INSPECTOR_BIN="/Users/jleechan/projects_other/llm_inspector/dist/cli.js"
llm-inspector() { node "$LLM_INSPECTOR_BIN" "$@"; }
llm-inspector-start() { node "$LLM_INSPECTOR_BIN" start --port 9000 --upstream http://127.0.0.1:8000; }
llm-inspector-stop() { node "$LLM_INSPECTOR_BIN" stop; }
llm-inspector-status() { node "$LLM_INSPECTOR_BIN" status; }
claudelocal() {
  ANTHROPIC_BASE_URL="http://127.0.0.1:9000" \
  claude --dangerously-skip-permissions --teammate-mode=tmux "$@"
}
claudelocalc() { claudelocal --continue "$@"; }
```

Note `llm-inspector-start` passes `--upstream http://127.0.0.1:8000`. The default (no override) also resolves to 8000, but explicit override is more robust against env-var drift.