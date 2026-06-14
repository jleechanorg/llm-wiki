---
name: codex-full-auto-flag-broken
description: codex CLI no longer accepts --full-auto; use --dangerously-bypass-approvals-and-sandbox instead
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 8dfc5e2f-2a26-4883-b6e0-f4e4556ad19b
---

## Context

When spawning a Codex AO worker via `ao spawn --agent codex`, the worker pane immediately exits with:

```
error: unexpected argument '--full-auto' found
```

The `packages/plugins/agent-codex/src/index.ts` `appendApprovalFlags()` function was using `--full-auto` for `permissionless` mode. The installed version of the Codex CLI no longer accepts this flag.

## Fix

Replace `--full-auto` with `--dangerously-bypass-approvals-and-sandbox` in `packages/plugins/agent-codex/src/index.ts:840` and the corresponding tests in `src/index.test.ts`.

**Files changed:**
- `packages/plugins/agent-codex/src/index.ts` — line 840: `parts.push("--dangerously-bypass-approvals-and-sandbox")`
- `packages/plugins/agent-codex/src/index.test.ts` — all `--full-auto` → `--dangerously-bypass-approvals-and-sandbox`; removed duplicate `.not.toContain` assertions on lines 281 and 305

Rebuild required after source edit:
```bash
pnpm --filter @jleechanorg/ao-plugin-agent-codex build
pnpm --filter @jleechanorg/ao-cli build
```

**Why:** Codex CLI introduced `--dangerously-bypass-approvals-and-sandbox` as the replacement for `--full-auto` at some point post-plugin authorship. The plugin dist was not updated.

**How to apply:** Any time `ao spawn --agent codex` exits immediately in the tmux pane with the `unexpected argument '--full-auto'` error, apply this fix and rebuild.
