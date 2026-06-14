---
title: "Project 2026 06 10 Orphan Lifecycle Workers Reaped"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan-project-agento-agent-orchestrator/memory/project_2026-06-10_orphan_lifecycle_workers_reaped.md
---

## Summary

During the 2026-06-10 recovery session (after the 4-PR batch merge at 21:34Z), 16 orphan lifecycle-workers were reaped via `kill <pid>`. PIDs: 19185, 20014, 21327, 22246, 23575, 24148, 24867, 25421, 27083, 28237, 29575, 31067, 31959, 32659, 34178, 35626. All were processes that survived their parent coordinator — `tmux` panes were gone (or never created in the case of failed spawns), but the `node ao lifecycle-worker` process kept running, holding ports and writing to `~/.agent-orchestrator/<pro...

## Original

During the 2026-06-10 recovery session (after the 4-PR batch merge at 21:34Z), 16 orphan lifecycle-workers were reaped via `kill <pid>`. PIDs: 19185, 20014, 21327, 22246, 23575, 24148, 24867, 25421, 27083, 28237, 29575, 31067, 31959, 32659, 34178, 35626. All were processes that survived their parent coordinator — `tmux` panes were gone (or never created in the case of failed spawns), but the `node ao lifecycle-worker` process kept running, holding ports and writing to `~/.agent-orchestrator/<project-hash>/lifecycle-worker.log`.

**Root cause:** The startup race in `lifecycle-manager.ts` (tracked as [bd-85r](https://github.com/jleechanorg/agent-orchestrator/issues)) — `isProcessRunning` fallback kills sessions during CLI boot. The race is: when a new `ao start` boots, the lifecycle-manager walks the session list and uses `isProcessRunning(pid)` to decide whether to reap. The fallback is "if we can't tell, kill it" — which races with the new coordinator's own startup, killing its own children before they register. Workers that were started by an older coordinator generation survive (their tmux pane died but the node process kept running) and accumulate.

**Why this matters:**
- Each orphan holds a port slot and writes to the lifecycle-worker log, polluting diagnostic signal.
- The 16 reaped today were the most recent crop; the same race will keep generating new orphans on every restart cycle until bd-85r is fixed.
- `bd-linf` (skeptic chain 0 verdicts + 16 stale workers) was closed today on the assumption that the orphans were the cause. They were a *symptom*; bd-85r is the structural fix.

**How to apply:**
- After restarting the coordinator, check `ps aux | grep "lifecycle-worker" | grep -v grep` and reap any PIDs not associated with the current `running.json` generation. Use `kill <pid>` (SIGTERM, not SIGKILL — let them write a clean shutdown line to the log).
- When investigating "skeptic chain silent" symptoms, check for orphan workers *first* — they may be holding the lifecycle log and writing garbage, masking real activity.
- The next time the coordinator dies and is restarted, expect another 5-15 orphans to accumulate. This is normal until bd-85r lands.

**References:**
- Recovery evidence: `~/roadmap/nextsteps-2026-06-10-coordinator-recovery-and-guardaudit.md`.
- Root-cause bead: [bd-85r](https://github.com/jleechanorg/agent-orchestrator/issues).
- Closed symptom bead: [bd-linf](https://github.com/jleechanorg/agent-orchestrator/issues).
- Related memory: `project_2026-06-09_lifecycle_workers_running_broken.md` (earlier incident, same root cause).
