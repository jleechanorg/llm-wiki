---
title: "Feedback 2026 06 10 Spurious Coordinator Project Removed"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan-project-agento-agent-orchestrator/memory/feedback_2026-06-10_spurious_coordinator_project_removed.md
---

## Summary

When `ao start /Users/jleechan/.worktrees/agent-orchestrator/coordinator` was invoked (as an attempted workaround for the `guardMainRepo` check), the CLI added a new project entry called "coordinator" to `~/.hermes/agent-orchestrator.yaml` because the path didn't match any registered project. The entry was 48 lines (lines 1026-1073 in the post-edit file), including `name: coordinator`, `repo: jleechanorg/agent-orchestrator`, `path: /Users/jleechan/.worktrees/agent-orchestrator/coordinator`, `def...

## Original

When `ao start /Users/jleechan/.worktrees/agent-orchestrator/coordinator` was invoked (as an attempted workaround for the `guardMainRepo` check), the CLI added a new project entry called "coordinator" to `~/.hermes/agent-orchestrator.yaml` because the path didn't match any registered project. The entry was 48 lines (lines 1026-1073 in the post-edit file), including `name: coordinator`, `repo: jleechanorg/agent-orchestrator`, `path: /Users/jleechan/.worktrees/agent-orchestrator/coordinator`, `defaultBranch: main`, `sessionPrefix: coo`, and a `coo` agentRules block.

**Why this happened:**
- `ao start` with a path arg that doesn't resolve to a registered project calls `addProjectToConfig` to register it. The check is on the path matching a project, not on whether the path is a "valid" project root.
- The intent was probably: "use this path as the main repo for the guard check." The actual behavior was: "create a new project here."

**Why it matters:**
- This is a config-drift class. A 48-line spurious block in `~/.hermes/agent-orchestrator.yaml` would have (a) confused future `ao start <name>` invocations (ambiguous "coordinator" name), (b) caused the AO daemon to spawn workers against the wrong worktree path, (c) required manual cleanup.
- The structural fix is in [bd-st2r](https://github.com/jleechanorg/agent-orchestrator/issues): canonicalize the AO user config to `~/.openclaw_prod` with symlinked aliases, so config is single-source-of-truth and accidental additions are detectable.

**How to apply:**
- The fix: revert was done within minutes — the `coordinator:` block (lines 1026-1073) was deleted, and a backup was created at `~/.hermes/agent-orchestrator.yaml.bak-2026-06-10` (41141 bytes).
- When the same "Refusing to operate on the main repo" error happens again, the *correct* workaround is the `AO_MAIN_REPO` env var, NOT `ao start <worktree-path>`. The env var bypasses the guard without creating a project entry.
- Before any `ao start <path>` invocation, check `git -C <path> rev-parse --show-toplevel` and compare to registered project paths in `~/.hermes/agent-orchestrator.yaml`. If the path is a worktree of a registered project, use the project name (`ao start <name>`), not the path.

**References:**
- Recovery evidence: `~/roadmap/nextsteps-2026-06-10-coordinator-recovery-and-guardaudit.md` (Context section).
- Structural fix bead: [bd-st2r](https://github.com/jleechanorg/agent-orchestrator/issues).
- Backup file: `~/.hermes/agent-orchestrator.yaml.bak-2026-06-10` (41141 bytes, pre-coordinator-block).
- Related memory: `feedback_2026-06-10_guard_main_repo_aom_env_var.md` (the correct workaround pattern).
