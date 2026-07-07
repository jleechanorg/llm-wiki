---
title: "jeff-ubuntu OOM runner starvation — 12GB colima VM + desktop apps"
type: source
tags: [jeff-ubuntu, colima, oom, self-hosted-runners, infrastructure]
date: 2026-07-07
source_file: raw/project_2026-07-07_jeff_ubuntu_oom_runner_starvation.md
---

## Summary
On 2026-07-06/07, jeff-ubuntu's 16-container self-hosted GitHub Actions runner fleet went largely dark. Root cause: the colima VM was sized at 12GB while desktop applications on the same 62Gi host added enough additional memory pressure to trigger OOM kills, starving 13 of 16 runner containers. Staged (not simultaneous) container restart recovered 15/16.

## Key Claims
- The runner containers run inside the colima/Lima VM, not directly on the host Docker daemon, so a host-level `docker ps` alone does not reveal container-level OOM starvation happening inside the VM.
- This is a distinct failure mode from the previously-documented Lima VM silent hang (VM itself becoming unresponsive while `limactl` reports "Running") — here the VM stays up and even a live SSH session can look fine while runner containers inside are being OOM-killed one at a time.
- A simultaneous mass restart of all 16 containers would likely reproduce the same OOM condition (cold-start memory spike higher than steady-state); staging the restart in small batches avoided that.
- Adjacent open beads surfaced during investigation but not yet root-caused: `rev-gxv98` (colima VM full stop at 2026-07-07T01:11:04Z — possibly the same pressure event escalating past container-level OOM to a VM-level stop), `rev-88wm6` (the monitor.sh/lima-watchdog.sh cron jobs had silently stopped logging since the last reboot, reducing observability during this exact window), `rev-ih7n6` (separate disk-exhaustion resource axis).

## Connections
- [[MacCompressorOOMPressureSignal]] — same aggregate-pressure-not-single-process-RSS diagnostic pattern, macOS analog
- [[lima-watchdog]] — the existing watchdog that should have caught this but had stopped logging (rev-88wm6)
- [[jeff-ubuntu]] — the host entity
- [[Self-Hosted-Runner-Infra-Flake-vs-Real-Failure]]
