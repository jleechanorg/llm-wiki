---
title: "OOM Guard Setup (Machine Protection)"
type: source
tags: [macos, memory, watchdog, kernel-panic, troubleshooting]
sources: []
last_updated: 2026-04-14
---

## Summary

Machine protection against runaway agent-spawned processes that consume all RAM in seconds and cause memory-pressure panics. Implemented via mem-watchdog LaunchAgent + rgignore + rg-safe wrapper.

## Key Claims

- mem-watchdog (launchd): scans all processes every 5 seconds and kills rg/Python/codex/node above 15 GB RSS, language_server_macos_arm above 10 GB
- Also performs scheduled Antigravity restart during early-morning window
- Uses native macOS supervisor (no cron, no third-party daemon)
- ~/.rgignore: tells ripgrep to skip VMs, containers, caches, system dirs, databases, build artifacts
- ~/bin/rg-safe: memory-limited rg wrapper with 4GB soft / 8GB hard VM limits

## What This Guards Against

- 2026-03-05 incident: Two Python processes consumed 115 GB (Codex orchestration) causing kernel panic
- 2026-03-05 incident: Two rg + codex processes consumed 45 GB (cmux DEV) causing kernel panic
- Both: system hit 99% compressor limit, WindowServer starved, watchdogd panicked kernel

## What This Does NOT Guard Against

- Kernel or DriverKit stalls (wlan busy timeout, airportd ifCount[0])
- Use [[WLANWatchdogPanicRunbook]] for that incident class

## Connections

- [[WLANWatchdogPanicRunbook]] — Different failure class (Wi-Fi stack)

## Contradictions

- None identified
