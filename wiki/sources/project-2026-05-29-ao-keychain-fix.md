---
title: "AO Antigravity keychain dialog — root cause and fix"
type: source
tags: [agent-orchestrator, keychain, antigravity, macos, ao-sessions, feedback]
sources: [project_2026-05-29_ao_keychain_fix]
date: 2026-05-29
source_file: raw/project_2026-05-29_ao_keychain_fix.md
---

## Summary

AO workers run with `HOME=~/.ao-sessions/<session-id>/`, so macOS Security framework cannot find the login keychain (which lives at `$HOME/Library/Keychains/`). When `agy` (Antigravity CLI) tries to refresh its OAuth token, the Security Agent pops a "A keychain cannot be found to store 'antigravity.'" GUI dialog and blocks the worker. The fix symlinks `~/.ao-sessions/<sid>/Library/Keychains → ~/Library/Keychains` before launching each worker.

## Key Claims

- AO workers' fake `$HOME` causes macOS keychain lookups to silently fail
- Pre-seeding a keychain entry did not help — `agy` still needs ANY keychain to exist for writes/refreshes
- Fix committed to `jleechanorg/agent-orchestrator` `main` as `5588a1601` and cherry-picked to `feat/runtime-antigravity` as `694c1937c`
- File: `packages/plugins/agent-antigravity/src/index.ts`
- Existing sessions can be patched retroactively with a one-liner `for sid in $(ls ~/.ao-sessions/)` loop
- `antig-cmux-loop.sh` has a socket guard (`[[ -S "$CMUX_SOCKET_PATH" ]] || exit 0`) to avoid triggering keychain access when cmux is absent
- `com.jleechan.antigravity-loop.plist` was manually unloaded

## Key Quotes

> "AO workers run with `HOME=~/.ao-sessions/<session-id>/`. macOS Security framework resolves the login keychain path from `$HOME/Library/Keychains/`. That directory doesn't exist in the fake session home → Security Agent shows 'A keychain cannot be found to store antigravity.' GUI dialog when `agy` tries to write/refresh its OAuth token."

## Connections

- [[agent-orchestrator]] — the runtime that creates per-session `$HOME` directories
- [[Antigravity]] / `agy` — the CLI whose OAuth refresh triggers the dialog
- [[macOSKeychainHandling]] — the broader class of macOS native API assumptions broken by fake `$HOME`
- [[AOSessionHomeLayout]] — the directory layout (`~/.ao-sessions/<sid>/`) whose `Library/` subtree must mirror the real `$HOME`
- [[AgentAntigravityPlugin]] — the plugin where the symlink fix lives
