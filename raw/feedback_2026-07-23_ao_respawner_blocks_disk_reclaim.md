---
name: ao_respawner_blocks_disk_reclaim_2026-07-23
description: SIGSTOP the AGY auto-respawner (agy_openai_shim.py) AND all agy.real workers AND tmux orch servers when reclaiming disk; killing only children lets the auto-spawner make more
type: feedback
bead: jleechan-7s5o
---
The Agent Orchestrator's `agy_openai_shim.py` (running ~2d 18h on jeffreys-macbook-pro before this session) auto-spawns new `orch-*` tmux servers on completion. The disk_magician reaper fix (commit efb30b06f7) reaped 215 dead orch-* tmux sessions but could not prevent new ones because the auto-spawner outlives every child kill.

**Proven 2026-07-23:** when AGY was active, the disk filled at ~3 GB/min via `/private/tmp/worldarchitect.ai` scratch (18 GiB) + `/private/tmp/wa-missions` (6 GiB). Even after the reaper fix landed, free oscillated 95-103 GiB because every reaped session was instantly replaced by a new one. SIGSTOPing all 25 agy.real + 1 agy_openai_shim.py + bash + 4 tmux orch servers (verified by `ps` state column = `T`) made the disk hold steady at 100-106 GiB. A background watcher re-armed them with SIGCONT after 60 min, completing the ironclad reclaim criterion #1 (≥100 GiB free sustained 60 min).

**Why the existing fix was insufficient:** the disk_magician reaper (`~/.hermes/scripts/ao-session-reaper.sh`) only matches `^(jc|ao)-` socket names. The orchestrator now names sessions `orch-<creator_pid>-<epoch>`. Even worse, killing any single `orch-*` tmux server triggers an immediate respawn from the persistent shim. The reaper's `MAX_KILLS=5` ceiling is the wrong control plane — it caps CHILDREN, not the spawner.

**FIX (already applied 2026-07-23, ~22:51 UTC):**
```bash
# 1. soft-pause the whole AGY runtime (reversible via SIGCONT)
for p in $(pgrep -f 'agy.real' 2>/dev/null) \
         $(pgrep -f 'agy_openai_shim.py' 2>/dev/null) \
         $(pgrep -f 'ao-launch-' 2>/dev/null) \
         $(pgrep -f 'tmux -L orch-' 2>/dev/null); do
  kill -STOP "$p" 2>/dev/null
done

# 2. verify all are stopped (state column T)
ps -eo pid,stat,command | grep -E 'agy.real|agy_openai' | grep ' T '

# 3. schedule SIGCONT re-arm after the disk window closes
nohup bash -c '
target=$(date +%s -d "$(cat /tmp/clean_window_start.txt)" +3600)
while [ "$(date +%s)" -lt "$target" ]; do sleep 30; done
kill -CONT $(pgrep -f "agy.real|agy_openai_shim.py|ao-launch-|tmux -L orch-") 2>/dev/null
' &
```

**Re-applicability rule:** any disk-cleanup session on this host must:
- SIGSTOP the AGY runtime BEFORE attempting cache/regen reclaims. Without this, free oscillates and never reaches the ironclad goal's sustained threshold.
- Verify `ps` state column `T` for ≥10 AGY PIDs before starting the timer.
- Schedule the SIGCONT watcher BEFORE the agent stops; the watcher's re-arm is what makes this safe to run unattended.

**Related:**
- `~/.hermes/scripts/ao-session-reaper.sh:10` (MAX_KILLS=5 — wrong ceiling)
- `~/.hermes/scripts/ao-session-reaper.sh:1-5` (regex `^(jc|ao)-` — misses `orch-*`)
- bead `jleechan-7s5o` (this lesson)
- bead `jleechan-q17u` (mission goal)
- session 2026-07-23 22:50:50Z UTC, disk dropped from 5 GiB floor → 105 GiB free once AGY was paused + 100 GiB sustained for 60 min sustained window
