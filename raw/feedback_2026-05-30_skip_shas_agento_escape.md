---
name: skip-shas-agento-escape
description: "SKIP_SHAS circular dependency fixed by using [agento] prefix on update commits; spawnOrchestrator test requires isAlive=false"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: d1759262-c2bc-40df-804a-adaa3e48ac4b
---

## SKIP_SHAS Circular Dependency — Break with [agento] Prefix

### Problem

`wholesome.test.ts` checks that all non-merge commits on a branch have `[agento]` prefix.
`SKIP_SHAS` is a Set of commit SHAs that bypass this check.

Adding a commit to `SKIP_SHAS` without an `[agento]` prefix creates an infinite chain:
- SKIP_SHAS-update commit lacks `[agento]` → fails wholesome
- Must add that commit to SKIP_SHAS → another non-`[agento]` commit
- Repeat indefinitely

### Fix

Use `[agento]` prefix on SKIP_SHAS-update commits. `[agento]` commits pass wholesome without needing to be in SKIP_SHAS. The escape hatch is the prefix, not the set.

```bash
git commit -m "[agento] fix(wholesome): add <sha> to SKIP_SHAS"
```

### Why: Apply

Whenever you need to retroactively register a commit SHA into SKIP_SHAS (e.g. after soft-reset squash reveals a baseline SHA that has no prefix), always use `[agento]` prefix on the SKIP_SHAS-update commit itself.

---

## `spawnOrchestrator` Test Requires `isAlive=false`

### Problem

`beforeEach` writes orchestrator metadata with a valid `runtimeHandle`. Default `orchestratorSessionStrategy="reuse"` makes `spawnOrchestrator()` return the existing live session early — `runtime.create` is never called, `onIdle` callback is never captured.

### Fix

```typescript
vi.mocked(mockRuntime.isAlive).mockResolvedValue(false);
```

This causes the existing orchestrator session to be cleaned up and `runtime.create` to be invoked, giving access to the `onIdle` callback.

### `restore()` Test Requirements

- Write killed session metadata with `requestedTask` field (otherwise throws on missing prompt)
- Create the workspace directory (`mkdirSync(join(tmpDir, "my-app"))`) for `existsSync(workspacePath)` check
- Status must be a terminal status (`"killed"`, `"failed"`, `"completed"`) so `isRestorable` returns `true`

---

## References

- PR [#645](https://github.com/jleechanorg/agent-orchestrator/pull/645) `feat/runtime-antigravity` — merged 2026-05-30T02:04:42Z
- Merge commit: `d5bb0eae599d117d679e612c42ac241fa287b14e`
- Test file: `packages/core/src/__tests__/session-manager-on-idle-session-id.test.ts`
- Bug: `bd-5o1` — `onIdle` used tmuxName instead of sessionId for `updateMetadata`
