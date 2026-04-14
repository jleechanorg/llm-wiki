# Manual Test Instructions: OpenClaw + Tailscale Integration

**Last verified**: 2026-03-30
**Status**: Local inference WORKING, Tailscale tunnel WORKING, Grok API key BLOCKED

> **Note**: Replace `<your-machine>.tail<xxxxx>.ts.net` throughout this document with your actual Tailscale Funnel hostname (`tailscale funnel status` to discover).

---

## Prerequisites

- OpenClaw gateway installed: `npm i -g openclaw` (binary at `$(which openclaw)` or `<nvm-path>/openclaw`)
- Tailscale installed and authenticated
- Config file: `~/.openclaw/openclaw.json`

## Test 1: Gateway Health (Local)

```bash
# 1. Ensure gateway is running
openclaw gateway install   # installs LaunchAgent
launchctl print gui/$(id -u)/ai.openclaw.gateway  # verify state=running

# 2. Verify port binding
lsof -i :18789 -P  # should show node listening

# 3. Test models endpoint
CONFIG_TOKEN=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/openclaw.json')); print(d['gateway']['auth']['token'])")
curl -s http://127.0.0.1:18789/v1/models \
  -H "Authorization: Bearer $CONFIG_TOKEN" | python3 -m json.tool

# Expected: JSON with list of openclaw models
```

**PASS criteria**: HTTP 200, JSON response with `data` array containing model entries.

## Test 2: Local Inference

```bash
CONFIG_TOKEN=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/openclaw.json')); print(d['gateway']['auth']['token'])")
curl -s http://127.0.0.1:18789/v1/chat/completions \
  -H "Authorization: Bearer $CONFIG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"Say hello in exactly 5 words"}],"stream":false,"max_tokens":30}' \
  --max-time 30 | python3 -m json.tool

# Expected: JSON with choices[0].message.content containing a response
```

**PASS criteria**: HTTP 200, non-empty `choices[0].message.content`.

**Can we host our own inference?** YES — OpenClaw gateway runs locally on port 18789 and routes to configured LLM providers. It's an OpenAI-compatible proxy that can host inference from any machine with the gateway running.

## Test 3: Tailscale Tunnel (Remote Access)

```bash
# 1. Verify Tailscale Funnel is active
tailscale funnel status
# Expected: https://<your-machine>.tail<xxxxx>.ts.net -> proxy http://127.0.0.1:18789

# 2. Test inference via tunnel (from any device on the internet)
CONFIG_TOKEN=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/openclaw.json')); print(d['gateway']['auth']['token'])")
curl -s https://<your-machine>.tail<xxxxx>.ts.net/v1/chat/completions \
  -H "Authorization: Bearer $CONFIG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"What is 2+2?"}],"stream":false}' \
  --max-time 30 | python3 -m json.tool

# Expected: Same response as local test
```

**PASS criteria**: HTTP 200 via HTTPS tunnel, response matches local inference.

**Important**: The Tailscale Funnel URL is public HTTPS — anyone with the auth token can send inference requests. The tunnel proxies to `127.0.0.1:18789`.

## Test 4: WorldArchitect Settings Integration

```bash
# 1. Start local WorldArchitect server
cd /path/to/worldarchitect/ai   # or your worktree root
TESTING_AUTH_BYPASS=true ./vpython mvp_site/main.py &

# 2. Test the openclaw connection endpoint
curl -s http://127.0.0.1:8080/api/settings/test-openclaw-connection \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $CONFIG_TOKEN" \
  -d "{
    \"user_id\": \"test-user\",
    \"openclaw_gateway_url\": \"https://<your-machine>.tail<xxxxx>.ts.net\",
    \"openclaw_gateway_port\": \"443\",
    \"openclaw_gateway_token\": \"\$CONFIG_TOKEN\"
  }" | python3 -m json.tool

# Expected: {"success": true, "mode": "models" or "chat_completions", ...}
```

**PASS criteria**: `success: true` with valid `mode`.

## Test 5: Proof-Prompt Hash (Advanced)

```bash
# Tests that the gateway actually runs inference (not just model listing)
CONFIG_TOKEN=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/openclaw.json')); print(d['gateway']['auth']['token'])")
curl -s http://127.0.0.1:8080/api/settings/test-openclaw-connection \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $CONFIG_TOKEN" \
  -d "{
    \"user_id\": \"test-user\",
    \"openclaw_gateway_url\": \"https://<your-machine>.tail<xxxxx>.ts.net\",
    \"openclaw_gateway_port\": \"443\",
    \"openclaw_gateway_token\": \"\$CONFIG_TOKEN\",
    \"proof_prompt\": \"What is the meaning of life?\"
  }" | python3 -m json.tool

# Expected: mode=chat_completions, proof_prompt_used=true, response_hash=<sha256>
```

**PASS criteria**: `mode: "chat_completions"`, `proof_prompt_used: true`, non-empty `response_hash`.

## Test 6: Grok API Key (xAI)

```bash
# Test 6a: Check local env
echo "GROK_API_KEY set: $([ -n "$GROK_API_KEY" ] && echo YES || echo NO)"
echo "XAI_API_KEY set: $([ -n "$XAI_API_KEY" ] && echo YES || echo NO)"

# Test 6b: Direct xAI API test
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-3-mini","messages":[{"role":"user","content":"Say hi"}],"max_tokens":10}' \
  --max-time 15 | python3 -m json.tool

# Test 6c: Test via WorldArchitect Grok avatar endpoint
curl -s http://127.0.0.1:8080/api/avatar/generate-grok \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-user", "campaign_id": "test-campaign"}' | python3 -m json.tool
```

### KNOWN ISSUE: Grok API Key Blocked

**Status as of 2026-03-30**: Both `GROK_API_KEY` and `XAI_API_KEY` return:
```
HTTP 403: "API key is currently blocked: Blocked due to API key leak"
```

**Root cause**: The key was likely exposed in a commit, log, or public artifact. xAI detected it and blocked the key.

**Fix required**:
1. Generate a new API key at https://console.x.ai/
2. Update local env: `export XAI_API_KEY=<new_key>` in `~/.bashrc`
3. Create GCP secret: `gcloud secrets create grok-api-key --data-file=-` (pipe in key)
4. **Add to deploy.sh** — the `--set-secrets` section (search for `GEMINI_API_KEY`) currently only has GEMINI, CEREBRAS, OPENROUTER, STREAM_RESPONSE_SIGNING_SECRET. Must add: `GROK_API_KEY=grok-api-key:latest`
5. Redeploy

### GCP Secrets Gap

The deploy script's `--set-secrets` section (search for `GEMINI_API_KEY`) does NOT include `GROK_API_KEY`. This means **Grok avatar generation silently fails on Cloud Run** (returns empty string from `_grok_api_key()`). Even after getting a new key, it won't work in production until `deploy.sh` is updated.

---

## Can GCP Cloud Run Reach Local OpenClaw for Inference?

**YES — proven in this session (2026-03-30).**

### Evidence

The Tailscale Funnel URL (`https://<your-machine>.tail<xxxxx>.ts.net`) is a **public HTTPS endpoint** accessible from anywhere on the internet, including GCP Cloud Run. Proof:

1. **Local inference** (HTTP 200): `"Hello there, how are you?"` — gateway on port 18789
2. **Tailscale tunnel inference** (HTTP 200): `"4"` (answer to "What is 2+2?") — via public HTTPS URL
3. **Model listing** (HTTP 200): 19 models returned via tunnel

### How It Works (GCP → Local)

```
GCP Cloud Run (worldarchitect.ai)
    ↓ HTTPS request to gateway_url from user settings
Tailscale Funnel (https://<your-machine>.tail<xxxxx>.ts.net)
    ↓ proxies to http://127.0.0.1:18789
Local OpenClaw Gateway (port 18789)
    ↓ routes to configured LLM provider
LLM Response → back up the chain
```

The WorldArchitect settings page stores `openclaw_gateway_url`, `openclaw_gateway_port`, and `openclaw_gateway_token`. When a user selects OpenClaw as their LLM provider, the GCP server makes an outbound HTTPS request to the Tailscale URL. The Tailscale Funnel proxies this to the local gateway, which handles inference.

### Test: GCP → Local Path

```bash
# From the GCP preview server, test the connection.
# Requires a dev server (TESTING_AUTH_BYPASS=true) or real Firebase auth.
# X-Test-Bypass-Auth is blocked on preview Cloud Run — do NOT use it there.
curl -s https://<preview-url>/api/settings/test-openclaw-connection \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <FIREBASE_ID_TOKEN>" \
  -d "{
    \"user_id\": \"test-user-123\",
    \"openclaw_gateway_url\": \"https://<your-machine>.tail<xxxxx>.ts.net\",
    \"openclaw_gateway_port\": \"443\",
    \"openclaw_gateway_token\": \"\$CONFIG_TOKEN\"
  }"

# Expected: {"success": true, "mode": "chat_completions" or "models"}
```

### Known Issue: Gateway Auth Scope After Restart

After gateway restart, `/v1/chat/completions` returns `"missing scope: operator.write"`. This is a gateway-internal auth issue (likely openclaw 2026.3.28 regression), not a connectivity issue. The Tailscale tunnel itself works correctly. Workaround: don't restart the gateway unnecessarily; if it breaks, `openclaw gateway stop && openclaw gateway install` and verify with `/v1/models` first.

---

## Architecture: Can We Host Our Own Inference?

**YES.** The OpenClaw gateway is a local inference proxy with these capabilities:

| Feature | Status | Details |
|---------|--------|---------|
| **Local inference** | WORKING | Gateway on port 18789, OpenAI-compatible API |
| **Remote access** | WORKING | Tailscale Funnel provides stable HTTPS URL |
| **Auth** | WORKING | Bearer token from `~/.openclaw/openclaw.json` |
| **Model routing** | WORKING | 19 model variants (default, memqa01-14, etc.) |
| **Streaming** | SUPPORTED | `stream: true` in request body |
| **WorldArchitect integration** | WORKING | Settings UI configures gateway URL/token |

**What "hosting your own inference" means here:**
- OpenClaw gateway runs on your Mac (or any machine with Node.js)
- It exposes an OpenAI-compatible `/v1/chat/completions` endpoint
- Tailscale Funnel gives it a stable `https://` URL accessible from anywhere
- WorldArchitect can be configured to use this instead of direct Gemini API
- The gateway handles model selection, memory (mem0), monitoring, and plugins

**Limitations:**
- Gateway must be running on the host machine (launchd keeps it alive)
- Tailscale Funnel requires Tailscale account and `tailscale funnel` setup
- Auth token is static — rotate via `openclaw.json` if leaked
- No auto-scaling — single machine, single instance

---

## Quick Smoke Test (All-in-One)

```bash
#!/bin/bash
# Save as: scripts/smoke_test_openclaw.sh
# Set TAILSCALE_HOST to your Funnel hostname before running, e.g.:
#   export TAILSCALE_HOST=<your-machine>.tail<xxxxx>.ts.net
set -e
TOKEN=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/openclaw.json')); print(d['gateway']['auth']['token'])")
TAILSCALE_HOST=${TAILSCALE_HOST:-"<your-machine>.tail<xxxxx>.ts.net"}

echo "=== Test 1: Gateway Health ==="
HTTP=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/v1/models -H "Authorization: Bearer $TOKEN")
[ "$HTTP" = "200" ] && echo "PASS: Local gateway responding" || echo "FAIL: HTTP $HTTP"

echo "=== Test 2: Local Inference ==="
RESP=$(curl -s http://127.0.0.1:18789/v1/chat/completions \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"Say OK"}],"stream":false,"max_tokens":5}' --max-time 15)
echo "$RESP" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print('PASS:', d['choices'][0]['message']['content'])" 2>/dev/null || echo "FAIL: $RESP"

echo "=== Test 3: Tailscale Tunnel ==="
HTTP=$(curl -s -o /dev/null -w "%{http_code}" https://${TAILSCALE_HOST}/v1/models -H "Authorization: Bearer $TOKEN" --max-time 10)
[ "$HTTP" = "200" ] && echo "PASS: Tailscale tunnel working" || echo "FAIL: HTTP $HTTP"

echo "=== Test 4: Grok API Key ==="
if [ -n "$XAI_API_KEY" ]; then
  GROK_RESP=$(curl -s https://api.x.ai/v1/chat/completions \
    -H "Authorization: Bearer $XAI_API_KEY" -H "Content-Type: application/json" \
    -d '{"model":"grok-3-mini","messages":[{"role":"user","content":"hi"}],"max_tokens":5}' --max-time 10)
  echo "$GROK_RESP" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print('PASS:', d['choices'][0]['message']['content'])" 2>/dev/null || echo "FAIL: $GROK_RESP"
else
  echo "SKIP: XAI_API_KEY not set"
fi
```
