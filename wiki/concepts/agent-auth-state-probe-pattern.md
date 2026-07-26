---
title: "Agent Auth-State Two-Probe Pattern"
type: concept
tags: [auth, login, agent-process, anti-pattern, verification]
date: 2026-07-11
sources:
  - sources/feedback-2026-07-11-verify-auth-state-before-recommending-relogin.md
---

# Agent Auth-State Two-Probe Pattern

Operational rule that every Claude session (or other AI coding agent) must follow BEFORE recommending a fresh login, interactive re-auth, or TTY-prompt fix for any user auth failure.

## The pattern (priority order)

1. **Probe 1 — durable credential check.** `security find-generic-password -s <service> -a <account> -w` for the tool's macOS Keychain entry. Must return a non-empty string.
2. **Probe 2 — cheap non-UI invocation.** Run a non-bubbletea invocation that would surface real output if auth is working. Examples: `agy --print --prompt pong` returns model text; `claude -p "echo hi"` exits 0; `gemini -p "echo hi"` returns model text.
3. **Both pass?** Auth IS fine. The "needs re-login" recommendation is wrong. Look at file-side / config-side / network-side causes instead.
4. **Both fail?** Try non-login fixes first (rm broken symlinks, reinstall, refresh runtime home). Only if all of that fails should re-login be escalated.

## What this rule prevents

- Collapsing a single narrow signal (TTY error on `agy account list`, missing `oauth_creds.json`, sandbox HOME without token file) into the false-positive conclusion "needs re-login".
- Telling the user to do an interactive OAuth flow that may reset or overwrite their durable Keychain credential.
- Repeating a wrong conclusion across sessions via bead references, memory reads, and relayed transcripts.

## Distribution

Distributed to all 5 user-global CLI policy files via `/up` on 2026-07-11:
- `~/.claude/CLAUDE.md`
- `~/.codex/AGENTS.md`
- `~/.gemini/GEMINI.md`
- `~/.cursor/rules/env-preferences.mdc`
- `~/.hermes/workspace/SOUL.md`

And to `/up` itself (`~/.claude/commands/up.md`) so future invocations distribute it correctly.

## Related

- Source: [[feedback-2026-07-11-verify-auth-state-before-recommending-relogin]]
- Agy-specific instance: [[agy-keychain-durable-auth]]
- Inverse pole: [[feedback-2026-07-10-agy-provider-default-on-stale-belief]]
