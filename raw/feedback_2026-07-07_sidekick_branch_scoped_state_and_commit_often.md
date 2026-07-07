---
name: sidekick-branch-scoped-state-and-commit-often
description: "Branch/mission-scoped STATE.md path avoids the shared-file sidekick clobber, and the commit-often rule was proven when a crashed sidekick's finished fix was recovered from the uncommitted working tree"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: cfee38e7-2623-45d6-b7e1-87ba5e3a8d31
---

**1. Scope sidekick STATE.md by branch/mission, not one shared path per project.**
Why: [[feedback-2026-07-07-swarm-orchestration-learnings-pr8191]] (rule 3) already documented that two concurrently-running sidekicks sharing a single `/tmp/<repo>/sidekick/STATE.md` clobbered each other's `## Next Actions` section on 2026-07-06/07 — one sidekick reused the same generic heading a different live sidekick owned, requiring a manual revert. The namespaced-section workaround (each sidekick appends its own `## <mission> (session <id>, owner: sidekick — <scope>)` block) reduces collision risk but still leaves every sidekick writing into the same file, so a bad append or a stale read-then-write can still stomp a sibling's edit.
How to apply: prefer a fully separate path per sidekick — `/tmp/<project>/sidekick/<branch-or-mission>/STATE.md` — over a single shared file with internal namespacing. This removes the write-write race entirely instead of just labeling the sections; only reach for the shared-file-with-namespaced-sections pattern when multiple sidekicks must read each other's state (cross-mission coordination), and even then keep each sidekick's own mutable section in its own file with a shared index file linking them.

**2. Commit-often is not a platitude — it recovered a finished fix that would otherwise have been lost.**
Why: a sidekick working an overnight CI-fix mission crashed (process/session death) after finishing the code but before running `git commit`. Because the user-scope rule already mandates committing after every green unit of work (≤30 min uncommitted), the successor agent picked up the session, found the finished fix still present in the working tree (uncommitted, not lost), committed it, and shipped it as [PR #8198](https://github.com/jleechanorg/worldarchitect.ai/pull/8198) — see [[project_2026-07-07_pr8198_ci_workflow_regressions]]. Had the working tree also been lost (container recycle, disk cleanup, different machine), the fix would have had to be rediscovered from scratch.
How to apply: this is the empirical proof case for the standing "commit + push after EVERY green unit of work, never hold >30 minutes of uncommitted changes" rule — cite this incident when a sidekick or AO worker prompt needs justification for why commit-often is non-negotiable, not just good hygiene. Propagate the instruction verbatim into every sub-agent/worker prompt, per existing policy.
