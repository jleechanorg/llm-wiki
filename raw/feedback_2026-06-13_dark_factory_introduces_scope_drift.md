---
name: dark-factory-introduces-scope-drift
description: "/f pipeline not only can't fix scope violations — it INTRODUCES scope drift via autonomous commits. PR-4 #7531 worktree gained 21 divergent commits from a single /f rerun."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3c559681-688f-4e19-a369-9d9453805f13
---

**Stop signal from pr4 /f rerun #2 (2026-06-13):** A single corrected `--backend ao --ao-project worldarchitect` re-dispatch on PR-4 #7531 produced **21 commits in the worktree** that were NEVER pushed, but the worktree HEAD moved from `3f3f33a4a8` → `4a66c33be9`. The pipeline's `wa-2333` AO worker session did a full rebase + 14 new commits in 6 minutes, mixing in-scope PR-4 work with out-of-scope drift.

**Why this happens** (root cause):
- The dark-factory pipeline's `goal` parameter is a feature spec, NOT a file-ownership constraint.
- The `implement` and `fix` codergen nodes ask the LLM "implement this goal" — the LLM is free to touch any file it thinks is needed.
- The LLM also sees the worktree's existing state and may include commits from prior rebase (which can pull in main commits if `origin/feat/levelup-v2-world-logic` is behind `main`).
- The result: autonomous commits that look "themed" but violate the file-disjoint ownership rule from `docs/plans/2026-06-13-level-up-v2-immediate-commit.md:3, :48`.

**PR-4 commit pollution (21 ahead of `origin/feat/levelup-v2-world-logic`)**:
- ✅ In-scope: `apply_level_up atomic co-write reducer`, `route world_logic through v2 reducer; delete source=server 2nd writer`, `add is_review_open + close_review tests`, `migrate modal-lock tests to v2 contract`
- ⚠️ Questionable: `bypass non-finish invariant when god-mode admin commit dispatched` (PR-6 scope?), `add behavioral holdout — immediate-commit regression suite` (PR-1 scope?), `guard P0 empty-sheet ordering (commit→reducer)` (PR-5/A scope?)
- ❌ Scope drift: rebase brought in `#7540 Colima migration`, `#7535/#7534 mcp-smoke-tests fix`, `#7516 orphaned CCS flag suppression` (pre-existing on main, not new, but in the worktree's history)
- Untracked: `.dark-factory/` (the /f artifacts)

**Worktree state after the /f rerun** is **UNUSABLE** for any further lane work — any new commit on top of `4a66c33be9` will carry the divergent history.

**Recovery** (operator action required, destructive):
- `cd ~/.lvl-lanes/wt-lvl-pr4 && git reset --hard origin/feat/levelup-v2-world-logic && git clean -fdx`
- This drops the 21 commits and all untracked files. Clean worktree at `3f3f33a4a8`.

**Lessons**:
1. `/f` is a code-iteration tool. It is NOT scope-aware. The LLM implementing a goal will touch whatever files it deems necessary.
2. **Before any /f dispatch**, validate the diff against the lane's §C scope:
   ```bash
   git diff --name-only origin/main...feat/levelup-v2-<lane>  # 1. file-ownership check
   git diff --stat origin/main...feat/levelup-v2-<lane>        # 2. scope magnitude check
   ```
3. **After any /f run**, ALWAYS check:
   ```bash
   cd ~/.lvl-lanes/wt-lvl-<lane> && \
     git rev-parse --short HEAD && \
     git rev-list --count origin/<branch>..HEAD  # should be 0 unless intentionally pushing
   ```
   If `> 0`, the pipeline committed without pushing. Operator decision: keep, reset, or cherry-pick.
4. The hard rule "no `git push --force` without approval" protected origin in this case — but the LOCAL worktree state can still drift, which is a state-machine problem.
5. The `ao spawn` worker session (`wa-2333`) inherited full write access to the worktree. There's no per-PR file-ownership check in the worker.

**How to apply**:
- Treat `/f` runs as DESTRUCTIVE to worktree state (not just additive). The implement/fix nodes can and do create commits.
- Always do a `git rev-list --count origin/...<branch>..HEAD` post-run. If non-zero, surface to operator immediately.
- Consider adding a `pre-implement` gate that diff-checks against §C scope before allowing commits. Out of scope for now.
- For PR series with strict file-disjoint ownership, do NOT use `/f` for the implementation phase — use human-driven commits (1 commit per file, per lane). `/f` is fine for `explore`/`plan`/`review`/`holdout`/`es`/`er`/`cs` phases, NOT `implement`/`fix`.
