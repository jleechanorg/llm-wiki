---
title: "Claude Code"
type: entity
tags: [tool, anthropic, cli, oauth, claude-sdk, keychain]
date: 2026-06-26
---

# Claude Code

**Definition**: Anthropic's official CLI client for Claude (the model family powering Claude Code sessions). The Anthropic-branded successor to the original "Claude" chatbot. Includes OAuth flow, system prompt construction, tool definitions, model routing, and the inference-side state machine. Version 2.1.193 verified 2026-06-26.

## Components

- **CLI binary** — `claude` (or `claude-code`), installable via npm (`npm install -g @anthropic-ai/claude-code`) or as a standalone binary
- **OAuth provider** — Anthropic's Max plan OAuth flow; tokens stored in macOS Keychain on Mac, Credential Manager on Windows, secret-tool on Linux
- **API client** — `@anthropic-ai/sdk` wrapped for CLI-specific tool rendering
- **Claude Code SessionStart hook** — runs `~/.claude/hooks/*.sh` on session start (used by [[llm_inspector]] for context-mode)

## Versions of interest

- **1.x** — original Claude Code release; stored OAuth tokens in `~/.claude/.credentials.json`
- **2.0+** — moved OAuth storage to OS keychain (Keychain / Credential Manager / secret-tool); `~/.claude/.credentials.json` now contains only dated backups
- **2.1.x** — current stable line; added `context_management` field to `/v1/messages` requests (requires beta header `context-management-2025-06-27` to be accepted by Anthropic API)

## OAuth storage

| OS | Storage location | Read command |
|---|---|---|
| macOS | Keychain `Claude Code-credentials-<uuid>` | `security find-generic-password -s "Claude Code-credentials-<uuid>" -a "<account>" -w` |
| Windows | Credential Manager `Claude Code-<uuid>` | `cmdkey /list:Claude Code-*` |
| Linux | secret-tool db `Claude Code-<uuid>` | `secret-tool search service "Claude Code"` |

See [[MacOSKeychainOAuthStorage]] for the macOS recovery procedure.

## Known issues affecting [[llm_inspector]]

- **#67** — Claude Code 2.1.193 sends `context_management: {edits: [{type: clear_thinking_20251015, keep: all}]}` without the required beta header `context-management-2025-06-27`. Anthropic API rejects with 400 `Extra inputs are not permitted`. Fix is either (a) strip the field in the proxy, or (b) add the beta header. Tracked as llm-inspector task #67.

## Primary use case for [[llm_inspector]]

Claude Code is the primary upstream client whose traffic llm-inspector captures. The capture chain:

```
Claude Code → llm-inspector :9000 → ccproxy-api :8000 → api.anthropic.com
```

allows forensic analysis of every prompt and response Claude Code sends, with optional token-saving transforms applied in-flight.

## Related entities

- [[llm_inspector]] — captures Claude Code traffic
- [[ccproxy_api]] — OAuth-injecting proxy between Claude Code and api.anthropic.com

## Related concepts

- [[MacOSKeychainOAuthStorage]] — where Claude Code 2.x keeps credentials
- [[ServiceDiscrimination]] — applies when checking whether Claude Code's OAuth plugin is responding