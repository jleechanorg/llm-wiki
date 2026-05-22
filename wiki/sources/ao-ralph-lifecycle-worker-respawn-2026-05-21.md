---
title: "AO ralph lifecycle-worker: involuntary injection respawns after kill"
type: source
date: 2026-05-21
tags: ["ao", "lifecycle-worker", "ralph", "launchd", "stop-hook", "orchestration", "incident"]
raw: "raw/learnings/feedback_2026-05-21_ao_ralph_lifecycle_worker_respawn.md"
bead: rev-3ey45
---

## Summary

The AO lifecycle-worker for the project named "ralph" (`node lifecycle-worker ralph`) is the
Agent Orchestrator's polling daemon for the `jleechanorg/ralph` GitHub repo — it is NOT the
ralph-wiggum in-session stop-hook plugin. The two systems share the word "ralph" but are
completely separate.

Killing the OS process alone is insufficient: a launchd LaunchAgent (`com.ao-runner.plist`,
StartInterval=3600) and a 2-minute cron watchdog (`lifecycle-watchdog.sh`) both respawn it.

## Key facts

- AO project config ID: `ralph` in `~/projects/jleechanclaw/agent-orchestrator.yaml`
- Repo monitored: `jleechanorg/ralph`, local path `~/projects/ralph`
- Poll interval: 75 s (default)
- Injection mechanism: `sessionManager.send()` → `runtime-tmux sendMessage()` → `tmux send-keys`
- The "Stop hook feedback:" text comes from AO `reactions:` message templates in the config

## Correct stop commands

```bash
ao stop ralph                        # SIGTERM + PID file clear
launchctl unload ~/Library/LaunchAgents/com.ao-runner.plist   # suppress respawn
ao session kill <sessionId>          # remove PR session from AO tracking
```

## Contrast with ralph-wiggum

| System | Trigger | Stop command | Respawns? |
|--------|---------|--------------|-----------|
| AO `lifecycle-worker ralph` | `ao start` / launchd | `ao stop ralph` | YES |
| ralph-wiggum stop hook | `/ralph-loop` | `/cancel-ralph` | NO |

## Source

- Memory file: `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-05-21_ao_ralph_lifecycle_worker_respawn.md`
- Roadmap: `~/roadmap/learnings-2026-05.md` (2026-05-21 entry)
- Bead: rev-3ey45 (closed)

## Concepts

- [[Ralph-Loop-Method]] — updated (AO lifecycle-worker vs wiggum stop-hook distinction added)
- [[LifecycleReactions]] — updated (send-to-agent injection mechanism)
- [[AO-Daemon-Incident]] — related
