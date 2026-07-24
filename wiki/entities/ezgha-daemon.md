---
title: "EzGhaDaemon"
type: entity
tags: [ez-gh-actions, daemon, github-actions, jleechanorg, rust]
date: 2026-07-05
---

## Definition

The Rust binary `ezgha` that ships in [jleechanorg/ez-gh-actions](https://github.com/jleechanorg/ez-gh-actions).
Manages a pool of ephemeral self-hosted GitHub Actions runners via JIT
registration. One binary, installed as a user systemd/launchd service.

## Architecture

- `src/main.rs` — CLI dispatch (init, doctor, start, serve, stop, status, install-service)
- `src/docker_backend.rs` — slot allocation + container lifecycle
- `src/github.rs` — gh CLI wrapper for JIT config + list_runners
- `src/platform.rs` — host capability detection (kvm, virsh, sysbox, daemon_in_vm)
- `src/config.rs` — `~/.config/ezgha/config.toml` parser
- `src/service.rs` — install_launchd() / install_systemd() write the service files

## Why it supersedes self-hosted-oss/*

See [[Project2026-07-05-ezgha-supersedes-self-hosted-oss]].

## References

- [GitHub: jleechanorg/ez-gh-actions](https://github.com/jleechanorg/ez-gh-actions)
- [[JitRegistrationPattern]]
- [[VmWithinVmIsolation]]
- [[SelfHostedOssLegacy]]

## Fleet operations lessons (2026-07-07)

- **Watchdog:** `Type=notify` + `WatchdogSec` requires `sd_notify` pings inside every long `gh api` path, not only the 30s serve loop. Shipped in 045cd66 (300s window).
- **Reset:** Prefer soft supervisor restart; hard reset (rm all containers + slot file) wedges when GitHub runners are `offline+busy`.
- **Mac policy:** `minimum_isolation=container` on Colima — see `config/config.toml.mac.example`.
- **External watchdog:** `ezgha-watchdog.timer` is separate from systemd watchdog; uncommitted script (bead ez-gh-actions-2ik).

Source: [[../sources/feedback-2026-07-07-ezgha-fleet-incident-recap.md]]
