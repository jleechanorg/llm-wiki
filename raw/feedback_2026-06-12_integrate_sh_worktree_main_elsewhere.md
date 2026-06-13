---
name: integrate-sh-fails-in-worktree-when-main-is-checked-out-elsewhere
description: "/integrate hard-stops on local-only commits AND on `git checkout main` when main lives in another worktree; branch from origin/main directly"
metadata: 
  node_type: memory
  bead: rev-d6qgj
  type: feedback
  originSessionId: a47bec93-bd6f-4b07-9f57-282f53690a84
---

`./integrate.sh` assumes a single-repo layout. In the worldarchitect.ai
worktree fleet (`git worktree list` shows ~10 worktrees of
`~/projects/worldarchitect.ai`), it fails two ways during `/integrate`:

1. **Local-only commits → HARD STOP.** The script refuses if the current
   branch is ahead of its remote tracking branch. Fix: commit your work, then
   `git push origin HEAD:<current-branch>` (non-destructive fast-forward) before
   re-running. Verify `git rev-parse HEAD == git rev-parse origin/<branch>`.

2. **`main` checked out in another worktree → `git checkout main` fatal.**
   `fatal: 'main' is already checked out at '/Users/jleechan/projects/worktree_prompt_ignore'`.
   The script cannot switch to main, so it aborts with "Failed to switch to main".

**Worktree-correct equivalent of `/integrate`** (do this manually when in a
worktree and main is elsewhere):

```bash
git fetch origin main --quiet
git checkout -b "dev$(date +%s)" origin/main   # matches integrate.sh dev{epoch} naming
git branch --set-upstream-to=origin/main "$(git branch --show-current)"  # auto-set when branching off origin/main
git status --short --branch                     # confirm clean, tracking origin/main
```

This produces the same outcome /integrate intends: a fresh `dev{timestamp}`
branch off latest `origin/main` with a clean tree. The script still runs its
test-server-stop step before failing, so that cleanup is already done.

**Why:** integrate.sh's `git checkout main` is unsafe under `git worktree`
because a ref can only be checked out in one worktree at a time. Branching
directly off `origin/main` sidesteps the conflict and is the canonical
worktree pattern. Related: [[feedback_2026-06-11_bash_cwd_does_not_persist_across_invocations]].

**How to apply:** When `/integrate` reports "Failed to switch to main / already
checked out at <path>", do NOT use `--force` blindly — branch off `origin/main`
directly with the snippet above. When it reports "unsynced commits with
remote", push the current branch to its own remote first, then re-run.
