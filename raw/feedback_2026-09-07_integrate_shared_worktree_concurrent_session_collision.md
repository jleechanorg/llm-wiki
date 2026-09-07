---
name: integrate-shared-worktree-concurrent-session-collision
description: "Before running /integrate (or any branch-deleting/creating script) in a worktree, check for live concurrent processes — git status can't distinguish your uncommitted work from another session's"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b4a55059-2bd9-411c-b475-e2d049bc830e
  modified: 2026-09-07T09:01:30.863Z
---

Never run `/integrate` (or any other branch-switching/deleting automation) in a
worktree without first checking whether another process is actively using that
same directory. `git status` cannot tell you "these uncommitted changes belong
to a different, currently-running session" — it just reports what's on disk.

**What happened**: ran `/integrate` in `/Users/jleechan/projects/worktree_beads_fix_again`
after a long, unrelated beads-harness session (PR #9459/#9765/#9766 work). The
canonical `integrate.sh` correctly hard-stopped on "Uncommitted changes must be
handled before integration" — but the changes it found were not mine: a
`.claude/hooks` archival rename set (`2026-09-06-fake-and-commands-parser`) and
a large pile of untracked `docs/superpowers/`, `roadmap/`, `mvp_site/` research
files belonging to an entirely different initiative (two-tier-core-memory /
prompt-cache work). `lsof +D <worktree>` showed live `claude.ex`, `aside`,
`bash`, and `node` processes with the directory open, and a repeat `git diff --
CLAUDE.md` returned different output seconds apart — proof another session was
actively editing files in the same worktree in real time.

**Why this matters**: had the hard stop not existed (or had `--force` been
used to push past it), `/integrate`'s stash/commit/checkout path would have
operated on someone else's live, uncommitted, in-progress work in a directory
neither owned nor understood. This is a variant of the shared-worktree/shared-stash-stack
hazard already known from [[feedback_2026-08-18_severe_shared_worktree_collision_ci_deletion_and_fabrication]]
and [[feedback_2026-08-17_subagent_worktree_delete_and_no_auto_flush_bead_loss]], but
the new, reusable detection technique is: `lsof +D <worktree-path> | awk '{print $1,$2}' | sort -u`
to enumerate live holders before trusting `git status` as "my" state.

**Rule**: before running any worktree-mutating command (`/integrate`, a branch
delete, a forced checkout, a stash) in a directory you didn't just create
yourself this turn, run `lsof +D <path>` and re-run `git status`/`git diff`
twice a few seconds apart. If either shows live external activity or changing
output, STOP — do not commit, stash, or force past the safety gate on
unrecognized changes. Report the finding and ask which worktree to use instead,
rather than guessing whose work it is.

**Verification**: `integrate.sh`'s own hard-stop protected against actual data
loss here (exit code, no state change) — the lesson is about not overriding
that gate with `--force`, and about recognizing the collision instead of
treating the hard-stop as a nuisance to route around.
