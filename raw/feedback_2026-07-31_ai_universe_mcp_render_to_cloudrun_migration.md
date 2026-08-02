---
name: ai-universe-mcp-migrated-render-cloud-run-consensus-ml-ai
description: "2026-07-31 — AI Universe hosting retired Render; MCP now lives at ai-universe-backend-114133832173.us-central1.run.app, consensus-ml.ai is the public SPA, tool renamed get_second_opinion → agent.second_opinion with _stubMode flag"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-eboni
  originSessionId: 2646dc53-9580-4545-943b-7c345e44c27f
  modified: 2026-07-31T10:42:37.604Z
---

## Context

On 2026-07-31 the `ai-universe-backend-final.onrender.com` Render service was
suspended by its owner (`x-render-routing: suspend-by-user`, page title
"Service Suspended"). `/secondo` started failing with HTTP 503. The original
diagnosis conflated two separate failures:

1. **Auth token rotation** — `auth-cli.mjs status` reported EXPIRED because
   Firebase idTokens expire every 1 hour.
2. **Backend suspension** — the MCP host itself was dead.

The two have to be probed independently. Probing them together led to a
"re-login via headless browser" recommendation when the real fix was a 4-line
URL change in `~/.claude/scripts/auth-cli.mjs`.

**Why:** Future agents (and `/advice` reviews) should not recommend browser
re-login when both probes are not independently demonstrated to fail.

**How to apply:** Before recommending re-login for AI Universe auth, run
`auth-cli.mjs token` first — it silently refreshes via the 30-day refreshToken
in `~/.ai-universe/auth-token-<project-id>.json`. If that returns a non-empty
JWT, auth is fine and the real problem is downstream (backend host, tool name,
schema).

## The migration

| Old | New |
|---|---|
| `https://ai-universe-backend-final.onrender.com/mcp` | `https://ai-universe-backend-114133832173.us-central1.run.app/mcp` |
| Public frontend: ai-universe-frontend-final.onrender.com | `https://consensus-ml.ai/` (Vite SPA, Firebase project `ai-universe-b3551`) |
| Tool: `get_second_opinion` | Tool: `agent.second_opinion` (with `_stubMode: true` for connectivity checks) |

The Cloud Run URL was discovered by grepping the Vite bundle
`https://consensus-ml.ai/assets/index-BjXa0Y5B.js` for HTTP URLs — the SPA
hardcodes the MCP backend URL, no public docs needed.

## Tool schema changes

Old schema (still in some legacy code paths):
```json
{"name": "get_second_opinion", "arguments": {"feedback_type": "...", "question": "..."}}
```

New schema (Cloud Run):
```json
{
  "name": "agent.second_opinion",
  "arguments": {
    "question": "...",
    "_authenticatedUserUid": "...",
    "_authenticatedUserEmail": "...",
    "_authenticatedUserName": "...",
    "primaryModel": "gemini|cerebras|grok|claude|perplexity|openai",
    "maxOpinions": 0..10,
    "_stubMode": true
  }
}
```

`_stubMode: true` returns a stubbed response (gemini primary + perplexity
secondary + multi-model synthesis) without burning a real model call — useful
for auth-connectivity probes.

## Fix applied (FIX-2026-07-31)

`~/.claude/scripts/auth-cli.mjs` line 36:
- `mcpUrl: 'https://ai-universe-backend-final.onrender.com/mcp'`
- → `mcpUrl: 'https://ai-universe-backend-114133832173.us-central1.run.app/mcp'`

`worldarchitecture-ai` project in the same file:
- `mcpUrl: 'https://worldarchitecture-ai-backend.onrender.com/mcp'` → `null`
  with TODO comment (WorldAI MCP replacement URL is pending — flag this for the
  user when they hit `auth-cli test --project worldarchitecture-ai`).

Custom-project template (line 99):
- `${projectOverride}.onrender.com/mcp` → throws with a clear error (Render
  auto-hosting retired; custom projects must supply MCP host explicitly).

`productionMcpUrl` fallback (line 122): removed the silent fallback to AI
Universe URL when `ACTIVE_PROJECT.mcpUrl` is null — downstream commands now
fail with a clear missing-URL error rather than silently hitting the wrong
backend.

Test command (line ~698): renamed `get_second_opinion` → `agent.second_opinion`
and added `_stubMode: true` to avoid burning real model calls during
connectivity checks.

## Verification

```bash
node ~/.claude/scripts/auth-cli.mjs status
# → Status: ✅ VALID  (expires 2026-07-31 4:20:07 AM)

node ~/.claude/scripts/auth-cli.mjs test
# → ✅ Authentication successful!
# → Returns stubbed multi-model synthesis with proper rate-limit metadata
#   (rateLimitRemaining=998, rateLimitLimit=1000)
```

## What still references Render (out of session scope, intentionally untouched)

- `~/.claude/settings.json.bak-*` — historical backups (CLAUDE.md: never rewrite
  historical logs).
- `~/.claude/plugins/marketplaces/claude-commands-marketplace/` — plugin
  marketplace code (out of session scope; would affect other consumers).
- `docs/ai-universe-frontend-test-report.md` and `docs/pr-guidelines/1782/guidelines.md`
  — dated historical artifacts (snapshot test report + PR #1782 guidelines).

## Out of scope

Worktree `scripts/mcp_common.sh`, `.claude/scripts/mcp_common.sh`, and
`tests/test_second_opinion_mcp_server.py` had their `setup_render_mcp_server`
function / Render-ordering test reverted by the user/linter after this
migration. The user accepted the test reversion as intentional (system reminder
2026-07-31 confirmed). Do NOT re-apply those edits without explicit user
direction — the global `auth-cli.mjs` change is sufficient for `/secondo` to
work and the user has clean-up preferences that supersede broader sweeps.

## References

- MCP endpoint probe: `curl -X POST https://ai-universe-backend-114133832173.us-central1.run.app/mcp` with `Accept: application/json, text/event-stream` (returns 406 without both — MCP transport requirement)
- Auth status probe: `node ~/.claude/scripts/auth-cli.mjs status`
- Auth token probe: `node ~/.claude/scripts/auth-cli.mjs token`
- Vite bundle URL extraction: `curl -s https://consensus-ml.ai/assets/index-BjXa0Y5B.js | grep -oE 'https?://[a-zA-Z0-9._/-]+'`
- Related memory: `feedback_2026-07-25_probe_the_blocker_before_declaring_blocked.md` (BLOCKED requires a failed probe, not an inferred constraint — same lesson applies here)