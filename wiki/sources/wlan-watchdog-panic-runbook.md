---
title: "Wi-Fi Watchdog Panic Runbook"
type: source
tags: [macos, kernel-panic, wifi, troubleshooting, runbook]
sources: []
last_updated: 2026-04-14
---

## Summary

Runbook for macOS kernel panics with `busy timeout[0], (60s): 'wlan'` pattern. Different from OOM panics — this is Wi-Fi stack / DriverKit instability.

## Key Claims

- watchdogd is NOT the root cause — it forces panic after kernel/DriverKit service stays stuck
- User-space memory watchdog does NOT help this failure mode
- Escalation criteria: busy timeout[0] + watchdogd panicked task + normal memory pressure + airportd cannot see Wi-Fi interface or AppleBCMWLANBusInterfacePCIe crash

## First-Response Workflow

1. Confirm it was NOT OOM:
   - grep panic-full-*.panic for "busy timeout", "Panicked task", "Compressor Info"
2. Pull Wi-Fi and airportd lines from prior boot:
   - log show --last 2h --predicate 'process == "airportd" || eventMessage CONTAINS[c] "AppleBCMWLAN"'
3. Apple-supported recovery path:
   - Install latest macOS updates
   - Retry on known-good Wi-Fi network
   - Remove/disable VPN and third-party network filters
   - Use Wireless Diagnostics, Safe Mode, Apple Diagnostics

## Scope Limits

- Does NOT prevent kernel/DriverKit stalls like 'wlan' busy timeout
- For that incident class, this runbook is the correct reference

## Connections

- [[OOMGuardSetup]] — Memory watchdog for OOM panics (different failure class)

## Contradictions

- None identified
