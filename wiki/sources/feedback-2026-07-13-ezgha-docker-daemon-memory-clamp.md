---
title: "ezgha memory detection needs explicit vm_total_mb override"
type: source
tags: [ezgha, github-actions, runner, colima, docker, memory-clamp]
date: 2026-07-13
source_file: feedback_2026-07-13_ezgha_docker_daemon_memory_clamp.md
---

## Summary

ezgha's `daemon_capacity()` reads `docker info --format {{.MemTotal}}` which returns the docker daemon's view (15957MB on a 24GB Colima VM), NOT the actual VM ceiling. Without `vm_total_mb` config, ezgha silently clamps per-runner memory to (daemon_mem - reserve) / count. PR #77 in jleechanorg/ez-gh-actions fixes this by routing `vm_total_mb` through `effective_limits()`.

## Key Claims

- `docker info MemTotal` reports the daemon's view inside the VM, not the VM's actual ceiling.
- For 6 mac runners at 3GB each + 2GB reserve, the VM must be ≥ 20GB.
- Per-runner memory math: `per_runner = (vm_total_mb - guest_reserve_mb) / count`.
- The startup fail-loud guard (`derive_memory_budget()`) already used `vm_total_mb`; PR #77 makes the runtime `effective_limits()` consistent with it.

## Key Quotes

> "On a 24GiB Colima VM, `docker info --format {{.MemTotal}}` returns 15957MB, so the per-runner clamp silently degraded from the configured 3072MB to 2318MB (-25%)."

## Connections

- [[EzghaRunnerSupervisor]] — Cargo binary managing self-hosted GitHub Actions runners
- [[ColimaVM]] — Lima-based Docker-on-Mac
- [[JleechanorgEzGhActions]] — repo where the fix lives (PR #77)
- [[CITrimForwardProjections]] — parallel lesson; this fix was part of the runner restore that enabled the CI trim rounds
