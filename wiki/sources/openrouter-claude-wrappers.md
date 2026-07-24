---
title: "OpenRouter Claude Code Wrappers — Unified Proxy Architecture (Both Machines)"
type: source
tags: [claude-code, openrouter, bashrc, proxy, tooling, reference]
date: 2026-07-20
source_file: raw/openrouter-claude-wrappers.md
---

## Summary

The jeff-ubuntu (Linux) and MacBook setups run a family of Claude Code CLI wrappers defined in `~/.bashrc`. As of 2026-07-20, all OpenRouter-backed wrappers on both machines delegate to a shared `_or_proxy_base()` helper that auto-starts `~/.local/bin/or-anthropic-proxy.py` on port 8767. The proxy is load-bearing: direct `ANTHROPIC_BASE_URL=https://openrouter.ai/api` silently breaks `claude -p` print mode (exit 0, zero stdout). Three wrapper families exist: OpenRouter-proxy (claudeor/claudeorop/claudeg/claudek), direct-provider (claudew/claudem), and host-local direct-opus (claudeo, whose meaning differs cross-machine).

## Key Claims

- **Family A (OpenRouter-backed)** MUST route via `_or_proxy_base` → 127.0.0.1:8767. Hardcoding the OpenRouter URL silently breaks `-p` mode (Content-Length buffering + thinking-block stripping are required).
- **Family B (direct provider — wafer.ai, minimax.io)** sets `ANTHROPIC_BASE_URL` directly. These providers return Anthropic-shaped SSE that Claude Code consumes without buffering; do NOT route them via 8767.
- **Family C (`claudeo`)** is a cross-machine gotcha: on Linux it's the `claudedo` opus alias (NOT OpenRouter); on Mac it's its own OpenRouter/GLM-5.2 wrapper.
- **`claudek` (moonshotai/kimi-k3)** is a reasoning model that always emits thinking blocks; the proxy's stripping is load-bearing or the SDK chokes. Future thinking-block-capable reasoning models inherit this requirement.
- **Proxy restart discipline**: `or-anthropic-proxy.py` reads `OPENROUTER_API_KEY` at startup. Restarting from a shell holding a stale/dead key causes upstream 401 "User not found" retry loops in the TUI.
- **Port 8767** was chosen because the original default 8765 collides with `MCP_AGENT_MAIL_PORT=8765`.
- **Verified 2026-07-20**: `claudeor`, `claudeg`, `claudek` all work in `-p` print mode (fibonacci write+run) on BOTH machines.
- **Prior proxy bug (2026-07-17)**: `_rewrite_data_line` passed `json.dumps` output (with `\uXXXX` escapes) as `re.sub`'s repl string → `re.error: bad escape \u` on any unicode → unhandled exception. Fixed with `lambda _m: new_data`.

## Key Quotes

> "Direct `ANTHROPIC_BASE_URL=https://openrouter.ai/api` breaks Claude Code `-p` print mode — exit 0 but zero stdout (verified on both machines 2026-07-17; raw curl works fine). The local proxy buffers responses with Content-Length and strips thinking blocks, fixing it."

> "On Linux, `claudeo` is NOT an OpenRouter alias (it's the pre-existing `claudedo` opus alias); on Mac `claudeo` is its own OpenRouter/GLM-5.2 wrapper (back-compat)."

> "All wrappers must call `_or_proxy_base` — never point at OpenRouter directly."

## Connections

- [[claude-code-cli]] — the underlying CLI all wrappers invoke
- [[or-anthropic-proxy]] — the load-bearing local proxy on port 8767
- [[openrouter]] — upstream provider for Family A
- [[bashrc-config]] — where all wrappers live on both machines
- [[kimi-k3]] — reasoning model that requires thinking-block stripping
- [[minimax-m3]] — Family B backend
- [[glm-5.2]] — z-ai model used by `claudeg` (and `claudeo` on Mac)
- [[wafer-ai]] — Family B backend for `claudew`
