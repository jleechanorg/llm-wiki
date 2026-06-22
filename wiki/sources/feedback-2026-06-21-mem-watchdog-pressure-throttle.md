---
title: "mem-watchdog pressure-kill throttle too aggressive — 30s → 300s"
type: source
tags: [macos, watchdog, throttle, mem-watchdog, oom, pressure, tuning, browser, comet, chrome]
date: 2026-06-21
source_file: ../raw/feedback_2026-06-21_mem_watchdog_pressure_throttle.md
---

## Summary
A 24h slice of `~/Library/Logs/mem-watchdog/mem-watchdog.log` showed 11 Comet
helper-renderer kills driven exclusively by the aggregate `check_memory_pressure()`
guard added on 2026-06-20 — every single one was under 800 MB RSS, well below
the 2 GB per-process cap. A 6-minute burst (19:42–19:47 PDT) killed 6 renderers
back-to-back, exposing that `PRESSURE_KILL_THROTTLE_SECONDS=30` was too tight to
let the OS reclaim between kills. Bumped to 300 s in `~/bin/mem-watchdog.sh:43`.
The per-process caps and CRITICAL threshold are unchanged; only the throttle
between successive pressure-driven kills is relaxed.

## Key Claims
- The 2026-06-20 [[MacCompressorOOMPressureSignal]] design is **right**; only the
  throttle interval needed tuning. Per-process caps stay as the safety net.
- 11 kills in 24h does not mean the watchdog is broken — it means the throttle is
  shorter than the OS reclaim window. On a 48 GB Mac killing one ~500 MB renderer
  via jetsam-style pressure, the kernel's compressor-segment drain takes seconds-
  to-minutes; 30 s is structurally too short.
- A **sustained WARN-level** pressure window (level 2, 13–19 GB swap, ~1.1 M
  compressor pages) is the trigger for the loop. CRITICAL (level 4) is only crossed
  briefly during the kill itself; the post-kill pressure drops back to WARN within
  one epoch but the largest-proc selector immediately re-fires.
- **Memory Saver Maximum is already on** for both `ai.perplexity.comet` and
  `com.google.Chrome` (verified via `defaults find MemorySaver` → 2 for both) — the
  2026-06-20 fix is in place; the throttle bump is the missing piece.
- Heavy Comet extensions (Adblock Plus 332 MB, Comet Web Resources 157 MB,
  Grammarly 82 MB, LastPass 58 MB, Bardeen 20 MB) raise the renderer baseline
  but are not the trigger — the trigger is renderer-count × baseline, not any
  single extension. No rogue subagents were running.

## Key Quotes
> "11 Comet kills in 24h at 30 s throttle is over-firing for what is sustained (not
> critical) pressure" — diagnosis, 2026-06-21
> "throttle should be at least an order of magnitude longer than the time-to-reclaim
> for the killed process's footprint. For a 500 MB renderer on 48 GB, 30 s is too
> short; 5 min matches jetsam's own settle window." — reusable pattern

## Connections
- [[MacCompressorOOMPressureSignal]] — the parent concept; this source tunes one
  parameter (the throttle) of the same guard
- [project-2026-06-20-browser-compressor-oom](../sources/project-2026-06-20-browser-compressor-oom.md) — the incident that produced the pressure-guard in the first place
- [WatchdogOfWatchdogsArchitecture](WatchdogOfWatchdogsArchitecture.md) — a different
  tier of the same problem class (watching the watchdogs)
- bd-bg6 — tracking bead (closed); follow-up to bd-o18
