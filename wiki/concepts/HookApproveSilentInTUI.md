---
title: "HookApproveSilentInTUI"
type: concept
tags: [claude-code, hooks, tui, silent-approve, feedback]
date: 2026-06-23
sources: [hook-tui-exit-codes-2026-06-23]
---

## Hook Approve Must Be Silent in TUI

When a PreToolUse hook decides to approve (no conflict), it must produce **zero visible TUI output**. The `{"decision":"approve"}` payload with NO `systemMessage` field is the contract.

## TUI Behavior

- `{"decision":"approve"}` alone → silent; tool runs; user sees nothing
- `{"decision":"approve", "systemMessage":"..."}` → TUI banner shown; routine edits become noisy

## Rule of Thumb

If the hook has nothing actionable to say, say nothing. The systemMessage field is for non-routine information, not confirmations.

## Related

- [[PreToolUseHookExitCodes]] — full three-mode contract
- [[hook-approve-silent-in-tui]] — feedback memory (related alias)
