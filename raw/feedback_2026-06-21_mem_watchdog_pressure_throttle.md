---
name: mem-watchdog-pressure-kill-throttle-bumped-30-to-300-seconds
description: mem-watchdog pressure-kill was firing every 30s on sustained WARN-level swap pressure; bumped PRESSURE_KILL_THROTTLE_SECONDS 30→300 in ~/bin/mem-watchdog.sh because all 11 Comet kills in 24h were under 800MB and well below the 2GB per-process cap.
metadata:
  node_type: memory
  type: feedback
  bead: bd-bg6
  originSessionId: 0939970f-6148-433f-bd95-fd431591447d
---

# mem-watchdog pressure-kill throttle: 30s → 300s

**Classification:** Best Practice (tuning fix-on-discovery)
**Date:** 2026-06-21 · Mac (48 GB, Darwin 24.5.0)
**FIX:** `~/bin/mem-watchdog.sh:43` — `PRESSURE_KILL_THROTTLE_SECONDS=300` (was 30).
Daemon restart: kill old PID 90410 → launchd respawned PID 55153 at 20:19:17 (23s after edit). Health: `healthy: pid=55153 heartbeat_age=17s`.

## Context — the symptom the user reported
"my memory watchdog killing my comet/chrome process too much."

## What was actually happening
A 24h slice of `~/Library/Logs/mem-watchdog/mem-watchdog.log`:

| Killed | Count | Reason |
|---|---:|---|
| ollama | 23 | memory-pressure (level 2) |
| **Comet** | **11** | **memory-pressure (level 1–2, swap 12–19 GB)** |
| python | 11 | memory-pressure |
| Python | 7 | memory-pressure |
| cmux | 3 | memory-pressure |

Every single Comet kill was under 800 MB RSS — **way below the 2 GB per-process cap** (`threshold_for_proc_mb` line 130-132). The kills came exclusively from `check_memory_pressure()` (the aggregate signal added 2026-06-20) at the **CRITICAL** threshold (`kern.memorystatus_vm_pressure_level >= 4` OR `swap_used >= 16384 MB`). The watchdog was shedding the largest monitored process to head off the jetsam/panic the 2026-06-20 postmortem documented.

A burst at 19:42–19:47 PDT killed 6 Comet renderers in 6 minutes (one per ~30 s — the old throttle). The pressure was WARN-level (level 2, sustained), not critical; the CRITICAL threshold was crossed only briefly, but the post-kill `largest_target_proc()` immediately picked the next biggest renderer, and the loop kept firing.

## Why this was the wrong shape of fix
The 2026-06-20 fix ([[project_2026-06-20_browser_compressor_oom]]) added the pressure-guard precisely **because** per-process RSS misses compressor-driven OOM. The kill itself is correct — the **frequency** was wrong. With 30 s between kills, the OS had no time to settle; with sustained WARN pressure + 30 s throttle, the watchdog becomes a nuisance rather than a safety net, and the user reasonably concluded it was "killing my Comet/Chrome too much."

## What I did NOT change (deliberately)
- **Per-process caps** (Comet 2 GB, Chrome 8 GB, ollama 16 GB, monitored total 45 GB) — these are the actual safety net. Don't touch.
- **CRITICAL threshold** (`PRESSURE_CRITICAL_LEVEL=4` / `SWAP_USED_CRITICAL_MB=16384`) — calibrated for the 2026-06-20 incident. Don't lower.
- **The pressure-guard itself** — the design is right; only the throttle was wrong.
- **Memory Saver policy** — `defaults find MemorySaver` already showed `ai.perplexity.comet` and `com.google.Chrome` both at `MemorySaverModeSavings = 2` (Maximum). The 2026-06-20 fix is in place; no additional work needed there.

## What I checked but ruled out
- **Rogue subagents.** Scanned PPID-1 (launchd) processes — `hermes gateway run` (93 MB), `mem0_server.py` (38 MB), normal macOS agents. Nothing spawning renderers.
- **Comet extensions as the *direct* cause.** `~/Library/Application Support/Comet/Default/Extensions/` has 25+ entries; a 12-extension batch was installed on 2026-06-18. Heaviest: **Adblock Plus 332 MB**, **Comet Web Resources 157 MB** (installed 2026-06-21 19:52, **after** the first kill at 13:54), **Grammarly 82 MB**, **LastPass 58 MB**, **Ghostery 32 MB**, **Honey 23 MB**, **Bardeen 20 MB**. These raise the renderer's working-set baseline but are not the *trigger* — the trigger is the renderer count × baseline, not any single extension. The extension install that would have been a smoking gun is `mjdcklhepheaaemphcopihnmjlmjpcnh` ("Comet Web Resources"), but its mtime (19:52) is after the first kill (13:54), so the 19:42 burst is renderer-fleet pressure, not this single extension.

## How to apply
- The 30 s throttle was a *conservative default* intended for acute events (one kill, OS settles, throttle resets via the epoch file). It under-performs on **sustained** pressure where the OS never settles before the next check.
- 300 s (5 min) gives the kernel time to actually reclaim — jetsam runs on its own schedule, the compressor's `occupied` count needs seconds-to-minutes to drain, and the post-kill free-pages count needs to climb before the next victim selection is meaningful.
- Re-tune if you see **zero** kills in a week despite 16+ GB swap (means pressure is real but not crossing CRITICAL — the watchdog is the wrong layer) vs. **multiple per-hour** kills of small processes (means OS pressure is real AND the throttle is too tight again).
- When the user reports "watchdog is killing X too much," **first** check `grep "KILLING" log | awk '{print $6}' | sort | uniq -c` to see if it's the per-process or pressure path. The 30 s pressure-kill throttle is the one that over-fires; per-process kills (which use 4-minute default) rarely bother users.

## Reusable pattern
- **Aggregate-pressure signal + tight throttle = nuisance, not safety net.** A watchdog that kills faster than the OS can settle is functionally just a renderer-crasher. Throttle should be **at least** an order of magnitude longer than the time-to-reclaim for the killed process's footprint. For a 500 MB renderer on 48 GB, 30 s is too short; 5 min matches jetsam's own settle window.
- **Diagnose "watchdog killing X too much" by separating the two kill paths** (per-process cap vs. pressure-guard). Different causes, different fixes. Per-process is a tuning issue on a specific process cap; pressure is a throttle issue + a downstream question of "is the OS really under pressure or is our pressure heuristic too sensitive?"
- **Fix-on-discovery rule triggered:** user-managed config (`~/bin/mem-watchdog.sh`) + 1-line fix + currently blocking. Applied immediately, then captured here as a memory. Did not write a workaround.

## References
- `~/bin/mem-watchdog.sh` (deployed), `~/bin/mem-watchdog.sh.bak.20260313T000132` (prior backup)
- `~/Library/Logs/mem-watchdog/mem-watchdog.log` (598 KB as of 2026-06-21 19:54)
- `~/Library/LaunchAgents/com.jleechan.mem-watchdog.plist`
- Prior memory: [[project_2026-06-20_browser_compressor_oom]] (bd-o18) — added the pressure-guard; this learning tunes the throttle that came with it.
- Bead: bd-bg6 (this learning)
