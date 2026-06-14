---
title: "running.json Missing Blocks `ao spawn`"
type: source
tags: ["ao-spawn", "agent-orchestrator", "running-state", "feedback"]
date: 2026-06-05
source_file: feedback_2026-06-05_running_json_missing_blocks_ao_spawn.md
---

## Summary
`ao spawn` fails with 'AO is not running' even when a lifecycle-worker process is alive, because `~/.agent-orchestrator/running.json` is only written by `ao start`, not by individual `ao lifecycle-worker <project>` processes.

## Key Claims
- `ao spawn` calls `ensureAOPollingProject()` → `getRunning()` which reads `~/.agent-orchestrator/running.json`
- running.json is only written by `ao start`; lifecycle-workers don't write it
- After machine reboot or before first `ao start`, running.json is absent and getRunning() returns null
- Workaround: manually write running.json with lifecycle-worker PID + correct config path/port

## Key Quotes
> Write `running.json` manually when `ao start` was never run

## Connections
- [[AgentOrchestrator]] — config + lifecycle
- [[AOSpawn]] — root cause of 'AO is not running'
