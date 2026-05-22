---
title: "Ralph Loop Method"
type: concept
tags: ["agents", "loop", "iteration", "ralph"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

Core mechanism for continuous agent iteration: agents pick tasks, implement code, validate changes, commit, update status, reset context for next iteration. Philosophy: "each improvement should make future improvements easier."

## Memory Persistence (Four Channels)
1. Git commit history — code changes visible via diffs
2. Progress logs — chronological records of attempts
3. Task state files — JSON tracking completion status
4. AGENTS.md — accumulated semantic wisdom

## CRITICAL: Two separate "ralph" systems — do not confuse

**ralph-wiggum stop hook** (in-session) — plugin at
`~/.claude/plugins/cache/claude-code-plugins/ralph-wiggum/1.0.0/`. Activated by
`/ralph-loop`. Uses Claude Code `Stop` hook. State file: `.claude/ralph-loop.local.md`.
Cancel: `/cancel-ralph`. Does NOT spawn external OS processes. Does NOT respawn.

**AO lifecycle-worker ralph** — `node lifecycle-worker ralph` is the AO polling daemon for
the AO project config ID `ralph` (monitors `jleechanorg/ralph` repo). Sends AO reaction
messages to tmux panes. Started by launchd (`com.ao-runner.plist`) + 2-min watchdog.
`kill <PID>` alone is insufficient — use `ao stop ralph`. To prevent respawn:
`launchctl unload ~/Library/LaunchAgents/com.ao-runner.plist`.

See: `sources/ao-ralph-lifecycle-worker-respawn-2026-05-21.md`, bead rev-3ey45 (2026-05-21).

## See Also
- [[Nested Agent Loops]]
- [[Self-Improving Coding Agents]]
- [[Orchestration Architecture Research]]
- [[LifecycleReactions]]
