---
title: "PreToolUse Hook Exit Codes — TUI Visibility Rules"
type: source
tags: [claude-code, hooks, pretooluse, tui, exit-codes, merge-train, feedback]
date: 2026-06-23
bead: orch-xqqu
originSessionId: 1bd4ff79-62dd-4cc5-9613-de7c50f21a2c
source_file: raw/hook-tui-exit-codes.md
last_updated: 2026-06-23
---

## Summary

Claude Code PreToolUse hooks have three distinct exit-code behaviors that determine TUI visibility. Getting them wrong silently hides conflicts from the user or causes noisy "no conflicts found" banners on every routine edit.

## Three Exit-Code Modes

| Exit | Decision payload | TUI Behavior | Use for |
|------|------------------|--------------|---------|
| 0 | `{"decision":"approve"}` **without** `systemMessage` | Completely silent (nothing shown) | No-conflict path (`_silent_approve()`) |
| 1 | (anything) | Non-blocking "hook error" notification; first stderr line shown as banner; tool still runs | Warn-only conflicts (`_emit("allow", reason)` then `sys.exit(1)`) |
| 2 | (anything) | Blocks the tool call; stderr shown as reason | Block path (`_emit("deny", reason)`) |

## Bug Fixed

Before the fix, warn-only conflicts called `_emit("allow", reason)` and returned with exit 0 — Claude Code showed nothing, so the user never saw the conflict. No-conflict cases emitted a full `systemMessage` payload which caused a "no conflicts found" banner on every routine edit.

## Cache Collision Gotcha

Hook cache lives at `/tmp/merge_train_cache_{repo_name}.json`. Tests using `tmp_path / "repo"` all share the same cache key. Use unique subdir names (e.g., `"norepo"`, `"warnrepo"`) and call `Path(f"/tmp/merge_train_cache_{name}.json").unlink(missing_ok=True)` at test start.

## Connections

- [[PreToolUseHookExitCodes]] — concept page for the three-mode pattern
- [[hook-approve-silent-in-tui]] — related feedback memory
- [[PR34]] — merge_train PR that fixed this
- [[MergeTrain]] — repo owning the hook
- Bead: `orch-xqqu`

## Test Coverage

- `tests/test_conflict_helper.py::test_warn_only_conflict_exits_nonzero`
- `tests/test_conflict_helper.py::test_no_conflict_silent_approve`
