---
title: "or-anthropic-proxy"
type: concept
tags: [tooling, proxy, claude-code, openrouter]
last_updated: 2026-07-20
---

# or-anthropic-proxy

The local Python proxy (`~/.local/bin/or-anthropic-proxy.py`) that sits between Claude Code and OpenRouter. Listens on port **8767** (chosen because the original default 8765 collides with `MCP_AGENT_MAIL_PORT=8765`). Log at `/tmp/or-anthropic-proxy.log`.

## Why it exists

Direct `ANTHROPIC_BASE_URL=https://openrouter.ai/api` breaks Claude Code's `-p` print mode: exit 0, zero stdout (raw curl works fine). The proxy fixes this by:
1. Buffering SSE responses with proper `Content-Length` headers.
2. Stripping thinking blocks (load-bearing for reasoning models like kimi-k3).

## Operational rules

- All OpenRouter-backed wrappers (`claudeor`/`claudeorop`/`claudeg`/`claudek`) must set `ANTHROPIC_BASE_URL="$(_or_proxy_base)"`. Never hardcode the OpenRouter URL.
- `OR_PROXY_DISABLED=1` bypasses the proxy and reverts to direct OpenRouter (which breaks `-p`).
- The proxy reads `OPENROUTER_API_KEY` at STARTUP. Restarting from a shell holding a stale/dead key causes upstream 401 "User not found" retry loops. Always restart from an interactive shell or after sourcing `~/.bashrc`.

## Prior bug (2026-07-17)

`_rewrite_data_line` passed `json.dumps` output (with `\uXXXX` escapes) as `re.sub`'s repl string → `re.error: bad escape \u` on any unicode → unhandled exception → TUI "API error · Retrying". Fixed with `lambda _m: new_data` as repl.

## See also

- [[openrouter-claude-wrappers]] — the wrappers that consume this proxy
- [[claude-code-cli]] — the CLI that requires the proxy
- [[openrouter]] — the upstream provider
