---
title: "PreToolUseHookExitCodes"
type: concept
tags: [claude-code, hooks, pretooluse, tui, exit-codes, harness]
date: 2026-06-23
sources: [hook-tui-exit-codes-2026-06-23]
---

## PreToolUse Hook Exit Codes — TUI Visibility Contract

Claude Code PreToolUse hooks have three exit-code behaviors that determine what the user sees in the TUI. Each maps to a specific conflict-handling intent.

## Three Modes

### 1. Silent Approve (Exit 0, no systemMessage)

```python
# Inside hook
_emit({"decision": "approve"})  # NO systemMessage
sys.exit(0)
```

**Result:** Tool runs; TUI shows nothing.

**Use for:** No-conflict paths. Routine edits where the hook found nothing to flag.

### 2. Warn-Only (Exit 1)

```python
_emit({"decision": "allow", "reason": "<human-readable warning>"})
sys.stderr.write("<warning>\n")
sys.exit(1)
```

**Result:** Tool runs; TUI shows non-blocking "hook error" banner with first stderr line. Claude sees the reason in tool result.

**Use for:** Warn-only conflicts. "I noticed X but let you proceed."

### 3. Block (Exit 2)

```python
_emit({"decision": "deny", "reason": "<block reason>"})
sys.exit(2)  # OR `return` if hook function exits itself
```

**Result:** Tool does NOT run; stderr shown as block reason.

**Use for:** Hard blocks. "This would cause X damage; abort."

## Common Anti-Patterns

- **Silent warn-only** — emitting `_emit("allow", reason)` and returning with exit 0: Claude Code shows NOTHING. User never sees the conflict.
- **Noisy no-conflict** — emitting a full `systemMessage` payload on every routine check: causes "no conflicts found" banner spam.

## Cache Collision Gotcha

Hook caches keyed by `repo_name` and stored at `/tmp/merge_train_cache_{repo_name}.json` collide across test fixtures that all use `tmp_path / "repo"`. Mitigation: use unique subdir names (`"norepo"`, `"warnrepo"`) and call `Path(f"/tmp/merge_train_cache_{name}.json").unlink(missing_ok=True)` at test start.

## Why This Matters

Hooks are the L1 constraint layer of the [[Harness5LayerModel]]. Silent failures in this layer mean user-visible conflicts go unnoticed — the harness fails open without the user knowing. Getting the exit-code contract right is a precondition for hook-mediated governance.

## Connections

- [[hook-approve-silent-in-tui]] — feedback memory capturing the silent-approve TUI requirement
- [[Harness5LayerModel]] — L1 constraint layer where hooks live
- [[MergeTrain]] — reference implementation
- [[PR34]] — the PR that codified this contract
