---
name: hermes-iteration-cap-commit-recovery
description: "When Hermes hits 60-iteration cap with uncommitted work in a worktree, commit the diff directly without spawning a new AO worker"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 7fb93c82-6491-4f2c-9a75-6a996471316c
---

When Hermes hits its 60-iteration limit and leaves uncommitted changes in a worktree, commit and push the diff immediately from the main session — do NOT spawn a new AO worker to redo the work.

**Why:** Hermes ran 60 iterations fully analyzing `gemini_provider.py` streaming BQ gaps (agent=None, finish_reason=None, json.dumps silent exception) but hit the cap before committing. The diff was already correct and tests passed. A new AO worker would have re-derived the same patch, wasting tokens.

**How to apply:** When an AO worker hits iteration cap:
1. Identify the worktree path from the session JSON or Slack thread.
2. Run `git -C <worktree_path> diff --stat` to see what was done.
3. If the diff is correct and tests pass, commit directly: `git -C <worktree_path> add -u && git -C <worktree_path> commit -m "..."`.
4. Push and create the PR normally.
Only spawn a new AO worker if the diff is incomplete or incorrect.

**Applies to:** Slack MCP thread `C0AH3RY3DK6/1781291497.121039`, worktree `wa-7496-streaming-bq`, PR [#7509](https://github.com/jleechanorg/worldarchitect.ai/pull/7509).
