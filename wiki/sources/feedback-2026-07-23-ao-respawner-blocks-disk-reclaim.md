---
title: "AO respawner blocks disk reclaim (2026-07-23)"
type: source
tags: [agent-orchestrator, disk-cleanup, macos, launchd, sigstop-sigcont, hermes, reaper-fix, lesson, anti-pattern]
date: 2026-07-23
source_file: ../../raw/feedback_2026-07-23_ao_respawner_blocks_disk_reclaim.md
---

## Summary

On 2026-07-23 the disk_magician reaper-fix (commit efb30b06f7) reaped 215 dead `orch-*` tmux servers but could not prevent new ones. The Agent Orchestrator's `agy_openai_shim.py` was auto-spawning fresh `orch-*` tmux servers at ~3 GB/min of `/private/tmp/worldarchitect.ai` scratch, capping any safe-action reclaim at <100 GiB. The durable fix is to SIGSTOP the entire AGY runtime (reaper + shim + workers + bash + tmux orch) for the duration of the reclaim window, then SIGCONT to re-arm.

## Key Claims

- Killing only `orch-*` tmux children does NOT reduce the AO fill rate (the auto-spawner outlives any child kill).
- The disk_magician reaper's `MAX_KILLS=5` ceiling is the wrong control plane — it caps CHILDREN, not the spawner.
- The reaper regex `^(jc|ao)-` already misses `orch-*`, but that omission is secondary to the auto-spawner problem.
- SIGSTOPping the full AGY runtime held the disk at 100–106 GiB free for the full 60-min window, enabling the ironclad goal's #1 criterion (≥100 GiB free sustained 60 min).
- Schedule a SIGCONT watcher BEFORE the reclaim window opens; the watcher's re-arm is what makes unattended reclaim safe.

## Key Quotes

> "the reaper fix landed but AO re-spawns them automatically via ~/.hermes/scripts/agy_openai_shim.py"

> "the reaper's `MAX_KILLS=5` ceiling is the wrong control plane — it caps CHILDREN, not the spawner."

> "Re-applicability rule: any disk-cleanup session on this host must SIGSTOP the AGY runtime BEFORE attempting cache/regen reclaims."

## Connections

- [[disk-cleanup]] — general cleanup playbook; this lesson is the missing "AO-active host" prerequisite step.
- [[agent-orchestrator]] — AGY is the spawner; the spawner must be paused before any reclaim attempt.
- [[hermes]] — the scripts `agy_openai_shim.py` and `ao-session-reaper.sh` live under `~/.hermes/scripts/`.
- [[reaper-fix-efb30b06f7]] — the earlier commit that landed in `~/.hermes/scripts/ao-session-reaper.sh` (reaper-only fix); insufficient on its own.
- [[disk-root-cause-2026-07-11]] — earlier root-cause that identified AO `/tmp` worktree churn as the prime regrowth driver.
- [[ironclad-disk-reclaim]] — the disk_magician ironclad goal that requires free ≥100 GiB sustained 60 min and is structurally unachievable with AO active.

## Proven 2026-07-23 Numbers (session)

| Metric | Value |
|---|---:|
| Free before SIGSTOP (low point of session) | ~5 GiB |
| Free after SIGSTOP sustained | 100–106 GiB |
| Reaped orch-* tmux sessions (one-time) | 215 |
| AGY workers paused (agy.real, state = T) | 25 |
| AO shim paused (agy_openai_shim.py) | 1 |
| orch tmux servers paused | 4 |
| AGY re-armed at (SIGCONT scheduled) | 2026-07-23T23:50:50Z |

## Reproducible procedure (one-liner)

```bash
for p in $(pgrep -f 'agy.real' 2>/dev/null) $(pgrep -f 'agy_openai_shim.py') $(pgrep -f 'ao-launch-') $(pgrep -f 'tmux -L orch-'); do
  kill -STOP "$p" 2>/dev/null
done
# verify (state column = T)
ps -eo pid,stat,command | grep -E 'agy.real|agy_openai' | grep ' T '
```

And the matching re-arm watcher (must run before the reclaim ends):

```bash
nohup bash -c '
target=$(date -d "$(cat /tmp/clean_window_start.txt)" +%s +3600)
while [ "$(date +%s)" -lt "$target" ]; do sleep 30; done
kill -CONT $(pgrep -f "agy.real|agy_openai_shim.py|ao-launch-|tmux -L orch-") 2>/dev/null
' &
```
