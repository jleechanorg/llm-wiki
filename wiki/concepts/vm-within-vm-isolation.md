---
title: "VM-within-VM Isolation"
type: concept
tags: [architecture, isolation, runner, ezgha]
date: 2026-07-05
---

## Definition

A runner workload executes inside a container, which itself runs inside a VM,
which itself runs on a host OS that may or may not be the same kernel. The
host kernel can never be reached directly by the runner process.

## ez-gh-actions deployment

- Mac: container in Docker daemon, which runs inside Colima Lima VM (Linux
  kernel on macOS), which runs on Darwin host. 3 layers.
- jeff-ubuntu: container in Docker daemon, which runs inside QEMU microVM
  (per ezgha policy `minimum_isolation=vm`), which runs on Ubuntu host kernel.
  3 layers.

## Why this matters

- Process isolation alone (the legacy `myoung34/github-runner` model) lets a
  malicious CI job escape via kernel bugs (CVE-class). VM isolation reduces
  this to VM-escape class bugs, which are far rarer and more researched.
- The runner process is bounded by the container's cgroup limits (cpu, memory,
  pids). The VM is bounded by its hypervisor limits. The host is bounded by
  its own OS. A runaway container can fill its container's quota but cannot
  exhaust the host's RAM.
- ezgha's `[policy] minimum_isolation = "vm"` enforces this at config-load
  time. If the daemon's runtime is detected as bare-metal docker (not inside
  a VM), `ezgha doctor` warns and the daemon refuses to spawn.

## References

- [[Project2026-07-05-ezgha-supersedes-self-hosted-oss]]
- [[EzGhaDaemon]]
