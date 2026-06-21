---
name: macos-compressor-driven-oom-windowserver-watchdog-panic-browser-renderer-fleet
description: Two 2026-06-20 Mac crashes traced to Chrome+Comet renderer fleet maxing the VM compressor; mem-watchdog watches per-process RSS only and has no pressure signal. Fix = Memory Saver Maximum policy + Auto Tab Discard.
metadata: 
  node_type: memory
  type: project
  bead: bd-o18
  originSessionId: 848007f3-1f3f-4de5-a20f-3605e7e058f5
---

# macOS compressor-driven OOM + WindowServer watchdog panic

**Classification:** Critical / Anti-Pattern (wrong watchdog signal)
**Date:** 2026-06-20 · Mac (48 GB, Darwin 24.5.0)

## Context — two crashes, one root driver
1. **19:14 jetsam mass-kill** — reason `vm-compressor-space-shortage` killed ~37 Apple
   daemons (trustd, securityd, tccd, CommCenter, backupd…). At 19:10 the kernel logged
   `memorystatus: failed to kill a process and no memory was reclaimed` with the
   compressor at ~25 GB (1.66M pages). cmux PID 3780 died at 19:10:14 as collateral
   (never named as a jetsam victim) and was relaunched.
2. **WindowServer userspace-watchdog kernel panic** — `panic(... userspace watchdog
   timeout: no successful checkins from WindowServer (2 induced crashes) in 164 seconds`.
   Backtrace through `com.apple.driver.AppleAVD` (hardware video decoder) +
   `AppleARMWatchdogTimer`; highest-CPU userland thread = `Google Chrome Helper
   (Renderer)`. Panic log: `Compressor Info: 30% of compressed pages limit (OK) and
   100% of segments limit (BAD) with 47 swapfiles`.

**Root driver for BOTH:** the browser/Electron renderer fleet (Chrome **and** Comet
running together) maxing the VM compressor segments + swap on 48 GB. Crash (2) is a
graphics/video-decode hang made far more likely by the compressor pressure from (1).

## Why nothing caught it — the watchdog gap (root cause)
Deployed `/Users/jleechan/bin/mem-watchdog.sh` (launchd `com.jleechan.mem-watchdog`,
RunAtLoad+KeepAlive) watches **per-process RSS only** via `ps … rss`, with high caps
(default 15 GB/proc, chrome group 32 GB, cmux 2 GB/8 GB). It has **0 KILLING events in
its entire log history**, and during the 2026-06-20 pressure windows the watchdog loop
was itself CPU-starved — heartbeat gaps up to **25 min (16:11)** and 15 min (14:21) in
a `sleep 5` loop. It has **no system-pressure / compressor-segment / swapfile / 
`memory_pressure` signal**, so it structurally cannot catch a compressor-driven OOM or
a WindowServer watchdog panic. A userspace-watchdog kernel panic also cannot be
intercepted from userland once WindowServer is 164s wedged.

**Anti-pattern:** per-process RSS is the wrong signal for compressor-driven instability.
The metric that actually maxed out (100% compressor segments, 47 swapfiles) is invisible
to an RSS reaper.

## Template-drift defect (latent)
Live `~/bin/mem-watchdog.sh` (only copy with cmux/chrome/ollama logic) is **ahead of**
both git-tracked copies: `dotfiles/bin/mem-watchdog.sh` (installer source, no cmux logic)
and `backup/Mac/bin/mem-watchdog.sh` (cmux added in `8f6a5fb7f` then regressed by a later
snapshot). `scripts/install_mem_watchdog.sh` reinstall or a backup restore would
**downgrade** the live guard and silently remove cmux protection. Violates the
launchd-plist-template / automation-completeness contract (deployed binary not faithfully
tracked in its owning repo).

## Fix applied (2026-06-20)
- **Memory Saver → Maximum**, durable via macOS managed policy (no sudo, user domain):
  `defaults write com.google.Chrome MemorySaverModeSavings -int 2` +
  `HighEfficiencyModeEnabled -bool true`. Same keys under `ai.perplexity.comet` (Comet
  is Chromium but may not honor it — verify at `comet://settings/performance`).
  Values: 0=Moderate, 1=Balanced, 2=Maximum; only applies when Memory Saver is enabled.
- **Auto Tab Discard** extension installed for a hard discard timer. Official rNeomy /
  joue.quroi Chrome listing ID = `jhnleheckmknfcgijgkadoemagpecfol`. Native Chrome (140+,
  Sept 2025) replaced the configurable discard timer with an ML model — **there is no
  per-minute timer in stable Chrome in 2026**, hence the extension.

## Follow-ups (bd-o18)
1. Back the Memory Saver policy into `backup/Mac/` so it survives reinstall.
2. Add a compressor-segment / swapfile / `memory_pressure` aggregate signal to
   `mem-watchdog.sh` (and sync live → `dotfiles/bin` + `backup/Mac/bin` to end the drift).

## Reusable pattern
- macOS OOM/instability on high-RAM machines is usually **VM-compressor segment
  exhaustion**, not raw RSS. Read the panic log's `Compressor Info:` line and the
  jetsam reason (`vm-compressor-space-shortage`) — `100% of segments limit (BAD)` +
  many swapfiles is the fingerprint.
- A memory watchdog must sample an **aggregate pressure signal** (compressor %,
  swapfile count, `memory_pressure -l`), not just per-process RSS, or it will sit at
  0 kills through every real event.
- Chrome/Comet **Memory Saver Maximum** = `MemorySaverModeSavings=2` policy; for a real
  timer use Auto Tab Discard (`jhnleheckmknfcgijgkadoemagpecfol`).
- Keep the live watchdog binary in sync with its repo template, or install/restore will
  silently downgrade protection. See [[project_2026-06-12_regrowth_prevention_prs]].

## References
- `~/bin/mem-watchdog.sh` (deployed), `~/Library/Logs/mem-watchdog/mem-watchdog.log`
- `~/Library/LaunchAgents/com.jleechan.mem-watchdog.plist`
- `dotfiles/bin/mem-watchdog.sh`, `backup/Mac/bin/mem-watchdog.sh`, `scripts/install_mem_watchdog.sh`
- Bead: bd-o18
