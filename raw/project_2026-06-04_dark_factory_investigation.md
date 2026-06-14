---
name: dark-factory-deletion-investigation-2026-06-04
description: Investigation of reported dark-factory deletion — repo intact; root cause of May 29 incident confirmed as pruneStaleWorktrees bug in AO lifecycle worker
metadata: 
  node_type: memory
  type: project
  bead: bd-diq
  originSessionId: 8dfc5e2f-2a26-4883-b6e0-f4e4556ad19b
---

Session investigated a reported deletion of `~/projects/dark-factory`. Repo was confirmed intact (HEAD `49c2276`, clean). No deletion occurred today.

**May 29 root cause:** AO lifecycle worker's `pruneStaleWorktrees` deleted `~/projects/worldarchitect.ai` because `wa-orchestrator` session had `worktree=/Users/jleechan/projects/worldarchitect.ai` — i.e. the main clone path was the same as the worktree path. The lifecycle worker treated the main clone as a stale worktree and deleted it. dark-factory was not deleted by this mechanism.

**Fix:** [PR #647](https://github.com/jleechanorg/agent-orchestrator/pull/647) MERGED 2026-05-29 — added `pruneWorktrees` config flag + main-worktree guard.

**Gap:** [PR #642](https://github.com/jleechanorg/agent-orchestrator/pull/642) CLOSED 2026-06-02 without merge — "Pass 2" broader directory-skip logic. Verify this coverage is complete or re-open.

**Why:** `~/projects/dark-factory` is a protected AO project path. If any project config sets `worktreeDir == path`, the pruning guard from #647 is the only thing preventing deletion.

**How to apply:** Before setting up a new AO project, confirm `path != worktreeDir`. Run `ao doctor` after any new project config.
