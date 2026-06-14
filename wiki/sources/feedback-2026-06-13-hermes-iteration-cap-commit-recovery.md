---
title: "Hermes 60-iteration cap: commit uncommitted work directly, do not respawn AO worker"
type: source
tags: [hermes, agent-orchestrator, worktree, iteration-cap, commit-recovery]
date: 2026-06-13
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-13_hermes_iteration_cap_commit_recovery.md
---

## Summary
When an AO worker hits Hermes's 60-iteration cap mid-task with a correct, tested diff sitting in a worktree, the parent session should commit and push the diff itself rather than spawn a new worker that would re-derive the same patch. This pattern was validated on Slack MCP thread `C0AH3RY3DK6/1781291497.121039`, worktree `wa-7496-streaming-bq`, and PR [#7509](https://github.com/jleechanorg/worldarchitect.ai/pull/7509).

## Key Claims
- Hermes's 60-iteration cap can fire mid-task even when the diff is already correct and tests pass — respawning wastes tokens re-deriving the same patch.
- Recovery flow: locate the worktree path from the session JSON or Slack thread, run `git -C <worktree_path> diff --stat`, then commit + push + create the PR from the main session.
- Only spawn a new AO worker when the diff is incomplete or incorrect.

## Key Quotes
> "When Hermes hits its 60-iteration limit and leaves uncommitted changes in a worktree, commit and push the diff immediately from the main session — do NOT spawn a new AO worker to redo the work."

> "Hermes ran 60 iterations fully analyzing `gemini_provider.py` streaming BQ gaps (agent=None, finish_reason=None, json.dumps silent exception) but hit the cap before committing. The diff was already correct and tests passed. A new AO worker would have re-derived the same patch, wasting tokens."

## Connections
- [[HermesGateway]] — the 60-iteration cap is a Hermes enforcement boundary
- [[WorktreeWorkflow]] — recovery requires locating and operating on the worktree path
- [[AgentOrchestrator]] — alternative recovery path that this pattern explicitly avoids when diff is correct
- [[PR7509]] — the validation PR for this recovery pattern
