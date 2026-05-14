---
name: branch-upstream-tracking
description: Agent never sets upstream tracking after branch/worktree creation — recurring manual fix
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fb0eccff-9cbe-4ed0-9736-b8cf9df06464
---

After creating any branch or entering any worktree, immediately run `git branch --set-upstream-to=origin/<branch> <branch>`. Do not wait for the first `git push -u`.

**Why:** Every worktree and new branch session required the user to manually ask for upstream tracking to be set. The agent never does it proactively because no instruction mandated it — `git checkout -b` and worktree creation don't set upstream by default.

**How to apply:** Immediately after `git checkout -b <branch>` or entering a worktree, set upstream. This is a mechanical step, not a judgment call — always do it.
