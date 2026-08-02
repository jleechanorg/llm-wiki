---
title: "AI Universe MCP migrated Render → Cloud Run (consensus-ml.ai)"
type: source
tags: [migration, auth, mcp, render, cloud-run, ai-universe, secondo]
date: 2026-07-31
source_file: feedback_2026-07-31_ai_universe_mcp_render_to_cloudrun_migration.md
---

## Summary

On 2026-07-31 the `ai-universe-backend-final.onrender.com` Render service was suspended by its owner (`x-render-routing: suspend-by-user`), causing `/secondo` to fail with HTTP 503. The original "auth expired" diagnosis conflated two independent failures (idToken rotation + Render backend suspension). The real fix was a 4-line URL change in `auth-cli.mjs`; auth itself was already working via silent refresh-token rotation. AI Universe MCP now lives at `ai-universe-backend-114133832173.us-central1.run.app`, with the public SPA at `consensus-ml.ai`.

## Key Claims

- AI Universe hosting migrated from Render to Google Cloud Run; consensus-ml.ai is the new public front-end.
- Tool renamed `get_second_opinion` → `agent.second_opinion` (with `_stubMode: true` for connectivity checks).
- `auth-cli.mjs token` silently refreshes the idToken via the 30-day refreshToken in `~/.ai-universe/auth-token-<project>.json` — no browser needed when refresh token is valid.
- Auth-vs-backend must be probed independently: `auth-cli test` failure does not necessarily mean auth failure; it may be the backend host.

## Key Quotes

> "Probe `auth-cli.mjs token` before recommending browser re-login; the absence of an exception from `token` proves auth works and rules out auth as the cause."

> "The original 'auth expired' diagnosis conflated two separate failures (idToken rotation + Render service suspension). Probing them independently showed `auth-cli.mjs token` auto-refreshed silently via the 30-day refreshToken — no browser re-login was needed."

## Connections

- [[AIUniverseMCP]] — the migrated MCP service (referenced in this entry)
- [[RenderHostingRetirement]] — broader migration context (Render was retired)
- [[SecondOpinionAuthFlow]] — the auth flow affected by this migration
- [[AuthCLI]] — the script that was migrated
- [[MemoryEntry feedback_2026-07-25_probe_the_blocker_before_declaring_blocked]] — same lesson applies: BLOCKED requires a failed probe