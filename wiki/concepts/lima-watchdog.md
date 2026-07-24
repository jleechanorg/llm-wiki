---
title: "Lima Watchdog"
type: concept
tags: [self-hosted-runners, watchdog, lima, infrastructure, automation]
date: 2026-06-23
last_updated: 2026-06-23
---

## Lima Watchdog

A 5-minute cron watchdog that detects and recovers a hung Lima/Colima VM on `jeff-ubuntu`. Lives at `~/.local/share/worldarchitect-colima-runners/lima-watchdog.sh` (stable installed path) after `install.sh` runs.

### Source

Created in PR #7843 (`fix/runner-watchdog-hardening`) after the June 18-23 incident where the Lima QEMU process hung for 5 days while appearing "Running" in `limactl list`. No automated detection existed at the time.

### What it checks (every 5 minutes)

1. **SSH liveness** — connect to `127.0.0.1:40257` via SSH key `~/.lima/_config/user`.
2. If SSH fails, inspect QEMU PID from `~/.lima/colima/qemu.pid`:
   - QEMU uptime < 60s → skip (VM may still be booting).
   - QEMU uptime ≥ 60s → VM is hung; begin recovery.
3. **Recovery sequence**:
   1. `kill -9` QEMU PID
   2. Remove stale disk lock `~/.colima/_lima/_disks/colima/in_use_by` if PID is dead
   3. `limactl start colima` (poll SSH every 5s up to 90s)
   4. Once Lima responds: `docker compose up -d` in the runner project dir
4. **Docker liveness** (only when VM SSH is healthy): run `docker ps` with 3-second timeout via `limactl shell`. If unresponsive → restart dockerd.

### Why a cron, not launchd

The watchdog runs on **jeff-ubuntu (Linux)**, not on the Mac. Linux has no launchd, so the wiring uses cron: `*/5 * * * * bash $HOOK_INSTALL_DIR/lima-watchdog.sh >>$HOME/.worldarchitect-runner/work/lima-watchdog.log 2>&1`.

### Companion tools

- **Mac-side**: `self-hosted-oss/ubuntu-runner-health.sh` has `check_lima_vm()` that SSH-hops mac→jeff-ubuntu→Lima guest on port 40257. On "dead", fires `alert_both()` to Slack `#ai-general` for human escalation. Does NOT auto-restart (lima-watchdog handles that on the host).
- **Lima config**: `ssh.localPort: 40257` must be set in `lima.yaml` for the watchdog probe to land on the right port.

### Why stable-path install

`install.sh` copies `lima-watchdog.sh` to `~/.local/share/worldarchitect-colima-runners/lima-watchdog.sh` (not the repo path). This means the watchdog keeps running even if the worktree branch is deleted, switched, or merged. The runtime mirror pattern is the same one used for the pre-job hook and the cleanup scripts.

### References

- PR #7843
- Source: [[LimaVMSSHCommunication]]
- Related: [[LimaVM]], [[SelfHostedRunners]], [[RuntimeMirror]]
