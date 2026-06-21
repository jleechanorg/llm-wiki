---
title: "Mac compressor OOM — watch pressure, not per-process RSS"
type: concept
tags: [macos, oom, watchdog, vm-compressor, monitoring, anti-pattern]
date: 2026-06-20
---

## Concept
On modern high-RAM Macs, out-of-memory crashes and WindowServer hangs are almost always
**VM-compressor segment exhaustion**, not a single process exceeding a raw RSS cap. A
memory watchdog that samples only per-process RSS will sit at zero interventions through
every real event, because the failure is an *aggregate* of many mid-sized processes (e.g. a
browser/Electron renderer fleet) compressing and swapping until the compressor's segment
table hits 100%.

## Fingerprint
- Jetsam reason: `vm-compressor-space-shortage`
- Kernel log: `memorystatus: failed to kill a process and no memory was reclaimed`
- Panic log line: `Compressor Info: X% of compressed pages limit (OK) and 100% of segments limit (BAD) with N swapfiles`
- High swapfile count (e.g. 47) is a strong pressure indicator.

## Rule
A macOS memory watchdog MUST sample an aggregate pressure signal — compressor segment %,
swapfile count, or `memory_pressure -l warn|critical` — and act on it, in addition to (not
instead of) per-process RSS. A `sleep N` userland loop can also be CPU-starved during the
exact pressure window it must act in; give it elevated scheduling priority and treat a
stale heartbeat as its own alert.

## Mitigations
- Reduce the renderer fleet: don't run Chrome **and** a second Chromium browser (Comet)
  with large tab counts simultaneously.
- Chrome/Comet **Memory Saver = Maximum**: `defaults write com.google.Chrome MemorySaverModeSavings -int 2` (+ `HighEfficiencyModeEnabled -bool true`).
- Hard discard timer: **Auto Tab Discard** extension (`jhnleheckmknfcgijgkadoemagpecfol`) —
  native Chrome 140+ replaced the configurable timer with an ML model.

## Connections
- [project-2026-06-20-browser-compressor-oom](../sources/project-2026-06-20-browser-compressor-oom.md) — the incident that produced this concept
- [WatchdogOfWatchdogsArchitecture](WatchdogOfWatchdogsArchitecture.md)
- [MemoryManagement](MemoryManagement.md)
