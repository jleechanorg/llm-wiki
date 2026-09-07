---
title: "/integrate hard-stopped on a live concurrent-session collision, not my own uncommitted work"
type: source
tags: [integrate, git, worktree, safety, concurrency, lsof]
date: 2026-09-07
source_file: feedback_2026-09-07_integrate_shared_worktree_concurrent_session_collision.md
---

## Summary

Ran `/integrate` in `worktree_beads_fix_again` after finishing unrelated beads-harness work (PR #9459/#9765/#9766). `integrate.sh` correctly hard-stopped on "Uncommitted changes must be handled before integration," but the flagged changes belonged to a different, unrelated, **live concurrent session** — not this session's own drift. `lsof +D <worktree>` showed live `claude.ex`/`aside`/`bash`/`node` processes holding the directory open, and a repeated `git diff -- CLAUDE.md` returned different output seconds apart, proving active concurrent edits in real time.

## Key Claims

- `git status` cannot distinguish "my own stale uncommitted work" from "another currently-running session's live in-progress work" — both look identical on disk.
- `lsof +D <worktree-path>` is a cheap, reliable way to detect live external process activity on a shared worktree directory before trusting `git status` as authoritative.
- Re-running `git status`/`git diff` twice a few seconds apart and observing *changing* output is independent corroborating evidence of concurrent editing.
- The correct response to this sub-case is the same as any other hard-stop: do not `--force`, do not manually commit/stash unrecognized changes — report the collision and ask which worktree to use instead.
- `integrate.sh`'s existing hard-stop protected against actual data loss here; no `--force` was used, no state was changed.

## Key Quotes

> "lsof +D /Users/jleechan/projects/worktree_beads_fix_again" showed live `claude.ex 27096`, `aside 3024`, `bash 17556`, `node 3025` processes with the directory open — evidence another session was actively using the exact same worktree path.

## Connections

- [[IntegrateHardStopPattern]] — this is a new sub-case added to the existing 4-hard-stop taxonomy (uncommitted changes, unpushed commits, unmerged PRs, main-in-worktree)
- [[WorktreeWorkflow]] — sibling worktree-safety conventions
- [[SameAuthorConcurrentSessionCollision]] — same underlying hazard (same-account concurrent sessions colliding silently) one layer down: filesystem/worktree instead of PR/merge
- [feedback-2026-06-13-shared-worktree-subagent-race](feedback-2026-06-13-shared-worktree-subagent-race.md) — prior shared-worktree race between concurrent agents
- [feedback-2026-07-12-shared-checkout-daemon-collision-use-worktree](feedback-2026-07-12-shared-checkout-daemon-collision-use-worktree.md) — prior shared-checkout collision, resolved by using dedicated worktrees
