---
title: "Uncommitted State Decision Matrix (4 options)"
type: concept
tags: [git, branch, decision-matrix, worktree-isolation]
last_updated: 2026-06-19
---

# Uncommitted State Decision Matrix

When integrate.sh (or any branch-aware operation like merge-readiness checks) hard-stops on uncommitted changes, work through this matrix in order.

## The 4 options

| Option | Action | When to use | Risk |
|---|---|---|---|
| **A. Split into scoped PRs** | `git checkout -b feat/X` for each subset; commit each; merge each separately | Changes span 3+ unrelated areas | Lowest — preserves intent, no data loss |
| **B. Commit as-is on same branch** | `git add -A && git commit -m "..."` | Changes are coherent and match the branch name (no scope creep) | Medium — commits scope creep into branch name; harder to review/revert |
| **C. Stash** | `git stash` (with a message); integrate later | Changes are WIP you want to preserve but not commit yet | Low — fully reversible; but stash can be lost if not reapplied |
| **D. Discard** | `git restore .` for tracked; `rm` for untracked | Changes are wrong/obsolete; live files would NOT be affected (except `workspace/SOUL.md` — see warning) | High — irreversible; live symlink files silently change runtime behavior |

## Special warning: `workspace/SOUL.md`

Per memory `reference_2026-06-12_hermes_soul_symlink_and_autocommit_branch.md`, `~/.hermes/workspace/SOUL.md` is a **symlink to the live policy file**. `M workspace/SOUL.md` means the live Hermes policy has been edited directly, which violates CLAUDE.md "Worktree Isolation".

**Discarding the `M workspace/SOUL.md` would silently revert live policy.** If the user wanted those changes, they need to be committed + PR'd + merged + `git pull`ed in `~/.hermes/` + `scripts/deploy.sh` to promote to prod.

## Decision tree

```
uncommitted changes detected
  │
  ├─ scope creep across 3+ areas? ──────► Option A: split
  │
  ├─ coherent single concern? ────────────► Option B: commit as-is
  │
  ├─ WIP to preserve? ───────────────────► Option C: stash
  │
  └─ wrong/obsolete + no symlink? ───────► Option D: discard
```

## Anti-pattern: jumping to Option D

The most common mistake is jumping to Option D (discard) when:
- The changes touch live symlinks (e.g. `workspace/SOUL.md`)
- The user might not have intended to discard everything
- There are untracked `??` files (deleted files are subtle; new files might be important)

When in doubt, prefer Option C (stash) — fully reversible, preserves all intent.

## Sources

- [feedback-2026-06-19-integrate-hard-stop-uncommitted-state](../sources/feedback-2026-06-19-integrate-hard-stop-uncommitted-state.md) — primary source
- CLAUDE.md "Worktree Isolation — Edit Your Copy, Not ~/.hermes/ Directly"

## Connections

- [IntegrateHardStopPattern](IntegrateHardStopPattern.md) — the trigger (hard-stop)
- [MergeReadinessGate](MergeReadinessGate.md) — sibling protocol (gate 1 is "git status --short empty")
- [[WorktreeIsolation]] — context: symlink warning
- [HermesLivenessProtocol](HermesLivenessProtocol.md) — companion protocol in same session