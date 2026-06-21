---
title: "macOS compressor-driven OOM + WindowServer watchdog panic (browser renderer fleet)"
type: source
tags: [macos, oom, memory, watchdog, browser, chrome, comet, vm-compressor, windowserver, kernel-panic]
date: 2026-06-20
source_file: ../raw/project_2026-06-20_browser_compressor_oom.md
---

## Summary
Two crashes on a 48 GB Mac (Darwin 24.5.0) on 2026-06-20 were both root-caused to the
Chrome + Comet browser/Electron renderer fleet maxing the macOS VM compressor. The first
was a jetsam mass-kill (`vm-compressor-space-shortage`) of ~37 Apple daemons; the second a
WindowServer userspace-watchdog kernel panic (164 s, AppleAVD video-decode path, Chrome
renderer high CPU) with the panic log showing `100% of segments limit (BAD)` and 47
swapfiles. The deployed `mem-watchdog.sh` watches per-process RSS only and never fired.

## Key Claims
- macOS instability on high-RAM machines is usually **VM-compressor segment exhaustion**,
  not raw RSS. Fingerprint: jetsam reason `vm-compressor-space-shortage` and panic-log
  `Compressor Info: ... 100% of segments limit (BAD) with N swapfiles`.
- A per-process RSS watchdog is the **wrong signal** for compressor-driven OOM — the
  deployed `mem-watchdog.sh` has 0 kills in its entire history and was itself CPU-starved
  (heartbeat gaps up to 25 min) during the pressure window.
- A userspace-watchdog kernel panic cannot be intercepted from userland once WindowServer
  is wedged past the 164 s check-in deadline.
- The live `~/bin/mem-watchdog.sh` has drifted ahead of its git-tracked templates
  (`dotfiles/bin`, `backup/Mac/bin`); reinstall/restore would silently downgrade it.
- Durable fix: Chrome/Comet **Memory Saver Maximum** via `MemorySaverModeSavings=2` policy
  plus the **Auto Tab Discard** extension (native Chrome 140+ has no per-minute timer).

## Key Quotes
> "userspace watchdog timeout: no successful checkins from WindowServer (2 induced crashes) in 164 seconds" — panic log, crash 2
> "Compressor Info: 30% of compressed pages limit (OK) and 100% of segments limit (BAD) with 47 swapfiles" — panic log

## Connections
- [[MacCompressorOOMPressureSignal]] — the reusable lesson: watch aggregate compressor/swap pressure, not per-process RSS
- [[WatchdogOfWatchdogsArchitecture]] — related watchdog design; this is a signal-selection failure of that family
- [[MemoryManagement]] — macOS VM compressor / swap behavior
- bd-o18 — tracking bead for the two follow-up fixes (repo backup of policy; pressure signal)
