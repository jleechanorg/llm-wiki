---
name: integrate-sh-behind-origin-main-hard-stop-2026-07-04
description: "integrate.sh hard-stops when current branch is N commits behind origin/main (4th case not covered by jleechan-9o99 decision matrix). Workaround: `git reset --hard origin/main` is safe when 0 local-only commits. Alternative when main is in another worktree: skip script's checkout-main step."
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 6003f954-c94f-4e89-937c-d5f1d78ab1a2
---

# integrate.sh Hard-Stop on Branch Behind origin/main

## When
2026-07-04, after `/integrate` on `fix/health-alert-false-alarms` which was **16 commits behind `origin/main`** (the merged PRs #734, #736, #737 plus 13 prior commits). User wanted everything on origin/main.

## Symptom

`integrate.sh` reports:
```
HARD STOP: Branch 'fix/health-alert-false-alarms' is not synced with remote 'origin/main':
  • Local commits ahead: 0
  • Remote commits ahead: 16
```

`--force` mode stashes uncommitted but still hard-stops on the sync gap (verified).

## Context (gap in jleechan-9o99 memory)

The existing memory `feedback_2026-06-19_integrate_hard_stop_uncommitted_state.md` lists 4 hard-stops:
1. Uncommitted changes (M, ??)
2. Local-only commits ahead
3. Unmerged integration PRs
4. `git checkout main` failure (when main is in another worktree)

It does NOT explicitly cover **the reverse case**: branch N commits behind origin/main. The script's hard-stop message is the same shape ("not synced") so operators can confuse it with #2 (ahead).

## Lesson: Safe reset workflow for jleechanclaw

When the local branch is behind origin/main AND you have no local-only commits, the safe integration path is:

```bash
# Step 1: Confirm zero local-only commits (REQUIRED before reset)
git log --oneline origin/main..HEAD   # MUST be empty
git status --short | grep -v "^??"    # MUST show no uncommitted (untracked rtk/ kanban.db.lock are runtime, can stay)

# Step 2: Reset branch to origin/main (drops the sync gap; local-only commits would be lost here)
git reset --hard origin/main

# Step 3: Re-run integrate.sh (now passes the sync check)
./integrate.sh
```

**Why this is safe**: when `git log --oneline origin/main..HEAD` is empty, the branch has zero commits not on main. The reset only moves the branch pointer forward to origin/main — no data loss because every commit on the branch is already on main.

## Lesson: Alternative when main is in another worktree

If `/integrate.sh` errors with `fatal: 'main' is already checked out at '/Users/jleechan/.worktrees/jleechanclaw/...'` (which happens because `~/.hermes/.claude/worktrees/` already has a watchdog or scratch worktree holding main), skip the script's checkout-main step and run directly:

```bash
# In current worktree (which is reset to origin/main):
git checkout -b dev$(date +%s) origin/main
# Result: fresh dev{timestamp} branch tracking origin/main
```

This produces the same outcome as `./integrate.sh` (a fresh `dev` branch from main) without needing to switch worktrees.

## Lesson: The "Remote commits ahead: 16" line is the trigger

The integrate.sh hard-stop message format is:
```
Local commits ahead: N
Remote commits ahead: N
```

When **Local commits ahead: 0 + Remote commits ahead > 0**, that's the "behind main" case. The reset workflow above applies.

When **Local commits ahead > 0 + Remote commits ahead: 0**, that's the "local-only commits" case (covered by jleechan-9o99 memory).

## Verification (2026-07-04)

1. `git log --oneline origin/main..HEAD` → empty (no local-only commits) ✓
2. `git reset --hard origin/main` → "HEAD is now at 55484bb386" (PR #737 merge commit) ✓
3. `./integrate.sh` → hard-stop cleared, but blocked again on `git checkout main` because main lives in another worktree
4. Workaround: `git checkout -b dev1783187611 origin/main` → fresh dev branch created, tracking origin/main
5. Discarded `M cron/jobs.json` (runtime churn: cron execution counter + last_run_at)
6. Final state: clean working tree on `dev1783187611` branch tracking `origin/main` at 55484bb386

## Reusable pattern

```bash
# Pattern 1: Reset + integrate.sh (when main is in current worktree)
git log --oneline origin/main..HEAD || true   # must be empty
git reset --hard origin/main
./integrate.sh

# Pattern 2: Direct branch creation (when main is in another worktree)
git log --oneline origin/main..HEAD || true   # must be empty
git reset --hard origin/main
git checkout -b dev$(date +%s) origin/main
git checkout -- <runtime-churn-file>            # e.g., cron/jobs.json
```

## Cross-refs
- memory `feedback_2026-06-19_integrate_hard_stop_uncommitted_state.md` (bead jleechan-9o99) — original 4-case hard-stop decision matrix
- memory `feedback_2026-06-12_integrate_sh_worktree_main_elsewhere.md` — earlier case of "main in another worktree" blocker
- memory `feedback_2026-05-14_integrate_branch_mismatch.md` — verify branch name after integrate.sh completes
- CLAUDE.md "Worktree Isolation — Edit Your Copy, Not ~/.hermes/ Directly"

## Open follow-ups
1. **integrate.sh enhancement**: explicitly handle the "behind origin/main" case in the error message, distinguishing it from "local commits ahead". One-line change: rephrase the message to "Branch X is N commits BEHIND origin/main — run \`git reset --hard origin/main\` if safe (verify no local-only commits first)".
2. **integrate.sh enhancement**: skip the `git checkout main` step if main lives in another worktree and instead create the new dev branch directly via `git checkout -b dev$(date +%s) origin/main` from the current (already-reset) state.
3. **Consider re-naming hard-stops**: distinguish "case A (behind)" vs "case B (ahead)" in script output so operators don't conflate.