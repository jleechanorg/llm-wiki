---
title: "openrouter"
type: concept
tags: [provider, llm-gateway]
last_updated: 2026-07-20
---

# openrouter

LLM gateway aggregator (`https://openrouter.ai/api`) that exposes an Anthropic-compatible `/v1/messages` endpoint. Used as the upstream for `[[claudeor]]`, `[[claudeorop]]`, `[[claudeg]]`, `[[claudek]]`.

## Key facts

- Raw `curl` to OpenRouter works fine. But pointing Claude Code at it directly (`ANTHROPIC_BASE_URL=https://openrouter.ai/api`) silently breaks `claude -p` print mode — exit 0, zero stdout. Requires routing via `[[or-anthropic-proxy]]` (port 8767).
- `OPENROUTER_API_KEY` lives in `~/.bashrc` (Linux: `~/.bashrc:256` = `sk-or-v1-79e8d4ff…`, replaced 2026-07-20 after the Linux key was dead/401).
- `openrouter-check` shell function verifies the key returns HTTP 200.

## Models in use (2026-07-20)

| Slug | Vendor | Wrapper |
|---|---|---|
| anthropic/claude-sonnet-4.5 | Anthropic | claudeor |
| anthropic/claude-opus-4.7 | Anthropic | claudeorop |
| z-ai/glm-5.2 | Zhipu | claudeg, claudeo (Mac) |
| moonshotai/kimi-k3 | Moonshot | claudek (reasoning model) |

## See also

- [[openrouter-claude-wrappers]] — the wrappers
- [[or-anthropic-proxy]] — required proxy
