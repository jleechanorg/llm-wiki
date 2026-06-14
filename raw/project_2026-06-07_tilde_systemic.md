---
name: tilde-expansion-is-systemic-not-a-one-off-bug
description: 14 tilde-related defects across 8 files; canonical expandHome exists in core/paths.ts:186 but is not used by 5 per-plugin copies and 7 inline regexes in start.ts
metadata: 
  node_type: memory
  type: project
  originSessionId: 139d26f8-35c9-4878-b214-fa47bc59b2dd
---

The antigravity tilde bug in PR #654 (commit 97b51e6ff) is a **symptom**, not the disease. The same class of defect exists in 14 locations across 8 files. The canonical `expandHome` helper in `packages/core/src/paths.ts:186-191` is exported and is used by `lifecycle-worker.ts`, `spawn.ts`, `config.ts:466,1013`, and `env-source.ts:104` — but the plugin authors and the CLI author rolled their own instead of importing it.

**Why this keeps recurring:** there is no enforcement that user-supplied paths must pass through a single chokepoint. `config.ts:466` expands `ProjectConfig.path` but does NOT expand `worktreeDir`, `cloneDir`, or the runtime-resolved `workspacePath` (which the plugins build themselves from these fields). Each plugin re-implements `expandPath` with a slight variant, and each `start.ts` call site uses its own inline `path.replace(/^~/, process.env["HOME"] || "")` regex.

**The two anti-patterns to look for:**

1. `path.replace(/^~/, process.env["HOME"] || "")` — 7 instances in `packages/cli/src/commands/start.ts:361,524,743,986,1029,1121,1221`. Defects: (a) only strips `^~` (1 char), not `^~/` (2 chars), so `~/foo` becomes `/home/foo` correctly but `~weird` becomes `/homeweird` incorrectly; (b) `process.env["HOME"]` is unset in Windows shells and certain sandboxed envs; (c) `|| ""` silently produces a leading-slash-broken path when HOME is unset instead of erroring.

2. Per-plugin local `expandPath(p)` functions — 5 near-copies in:
   - `packages/plugins/workspace-worktree/src/index.ts:393-398`
   - `packages/plugins/workspace-clone/src/index.ts:40-45`
   - `packages/plugins/scm-github/src/index.ts:988-993`
   - `packages/core/src/backfill-extensions.ts:64-69`
   - `packages/core/src/recovery/workspacePolicy.ts:9-14`
   
   Only the `workspacePolicy.ts` copy handles bare `~` (the canonical `expandHome` does not — it's a latent bug in the helper itself). All 5 should be deleted and replaced with `import { expandHome } from "@jleechanorg/ao-core"`.

**The shipped fix is correct but narrow:** `packages/plugins/agent-antigravity/src/index.ts:304-315` handles `~/` and bare `~` correctly with `path.join(userHome, p.slice(2))` and a 6-assertion TDD test at `index.test.ts:647-690`. It uses `slice(2)` per existing memory.

**How to apply:**

- Before adding any new `path.replace(/^~/, ...)`, `path.startsWith("~")` expansion, or local `expandPath` function, **import `expandHome` from `@jleechanorg/ao-core`**. The chokepoint is `packages/core/src/paths.ts:186`.
- If the call site is downstream of `config.ts:466` (i.e., receives a `ProjectConfig.path`), the expansion is already done — do not re-expand.
- If the call site is upstream (e.g., a raw CLI arg or env-var-supplied path), it MUST go through `expandHome` before being stored, compared, or passed to `realpathSync`/`writeFileSync`/`fs.readFileSync`.
- The canonical helper is missing one case (bare `~`); a follow-up should extend it: `if (filepath === "~" || filepath.startsWith("~/")) return join(homedir(), filepath.slice(filepath === "~" ? 1 : 2));`
- A unit test matrix for `expandHome` should cover: `~`, `~/`, `/abs/path`, `relative/path`, empty string, `process.env.HOME` unset, and `~user/` (documented unsupported on POSIX in Node).

**Why:** This is the second time the same defect class was caught in production (the first was `packages/core/src/config.ts` `applyEvolveLoopPaths()` 64 days ago, see `[[feedback_2026-04-04_tilde_slice_bug]]`). The pattern will keep recurring as long as the canonical helper is not the only accepted mechanism. A follow-up PR that does the 4-step centralization (extend `expandHome`, replace 5 plugin copies, replace 7 inline regexes, add test matrix) eliminates the entire class.

**Source:** Audit report at `/tmp/tilde-audit-report.md` (2026-06-07, agent a535c080e82721181). Bead: `bd-3m1t`. PR: [#654](https://github.com/jleechanorg/agent-orchestrator/pull/654). Commit: 97b51e6ff. Follow-up PR target: a separate `chore(core): centralize tilde expansion via expandHome` after PR #654 unblocks.

**How to apply:** See `[[feedback_2026-04-04_tilde_slice_bug]]` for the underlying `slice(1)` vs `slice(2)` rule.
