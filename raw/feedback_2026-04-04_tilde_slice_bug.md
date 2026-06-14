---
name: tilde-path-expansion-use-slice-2-not-slice-1
description: slice(1) on ~/.foo gives /.foo which is treated as absolute
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 139d26f8-35c9-4878-b214-fa47bc59b2dd
---

When expanding ~ in config paths, use `slice(2)` not `slice(1)` to skip the `~/`
two-character prefix. `slice(1)` only skips the `~` and leaves a leading `/`.

**Why**: `"~/.foo".slice(1)` = `"/.foo"` (treated as absolute path by Node.js),
but `"~/.foo".slice(2)` = `".foo"` which is relative. The correct approach is
`path.join(os.homedir(), dir.slice(2))` or `os.homedir() + dir.slice(1)` —
both handle `~/` prefix correctly.

**How to apply**: When implementing tilde expansion, use:
  `dir.startsWith("~/") ? join(os.homedir(), dir.slice(2)) : dir`
Never: `dir.slice(1)` alone.

**Reference**: `packages/core/src/config.ts` applyEvolveLoopPaths() function.

**Recurrence**: This same class of bug re-surfaced 64 days later in `packages/plugins/agent-antigravity/src/index.ts` (PR #654, commit 97b51e6ff) — the fix at line 305 correctly uses `slice(2)`. See `[[project_2026-06-07_tilde_systemic]]` for the broader pattern: 14 tilde-related defects across 8 files, with a canonical `expandHome` helper in `packages/core/src/paths.ts:186` that should be the only accepted mechanism.
