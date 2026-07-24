---
title: "Lima VM (colima)"
type: entity
tags: [self-hosted-runners, lima, qemu, infrastructure]
date: 2026-06-23
last_updated: 2026-06-23
---

## Lima VM — `colima` on jeff-ubuntu

A QEMU virtual machine named `colima` running on the Ubuntu host `jeff-ubuntu`. Created and managed by Lima (https://github.com/lima-vm/lima). Hosts the 16 self-hosted Linux GitHub Actions runners (`org-runner-1..16`) used by `jleechanorg/worldarchitect.ai`.

### Specs

- **CPU**: 4 cores
- **Memory**: 12 GiB
- **Disk**: 120 GiB
- **Guest OS**: Ubuntu 24.04 (noble) x86_64
- **SSH port on host loopback**: 40257 (pinned via `ssh.localPort` in lima.yaml)
- **Docker daemon forwarding**: `~/.lima/colima/sock/docker.sock` (on host) ↔ `/var/run/docker.sock` (in guest)
- **Lima home on host**: `~/.lima/colima/`

### Reachability from Mac

Two-stage SSH hop required. The Mac cannot directly reach the Lima guest because the QEMU network is internal to jeff-ubuntu.

```bash
ssh jeff-ubuntu "ssh -p 40257 -i ~/.lima/_config/user \
    -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no \
    127.0.0.1 'uname -a'"
```

One-hop alternative via limactl:

```bash
ssh jeff-ubuntu "~/.local/bin/limactl shell colima -- <cmd>"
```

### Common operations

| Action | Command |
|--------|---------|
| Status | `limactl list` (on jeff-ubuntu) |
| Restart | `limactl stop colima && limactl start colima` |
| Force kill (after hang) | `pkill -9 qemu-system-x86_64` then `limactl start colima` |
| Disk check | `limactl shell colima -- df -h /` |
| Container check | `limactl shell colima -- docker ps` |

### Known failure modes

1. **QEMU hang** — Lima appears "Running" in `limactl list` but SSH is dead; docker socket has stale mtime. Detection: SSH probe on port 40257. Recovery: force-kill QEMU, restart limactl. (See [[LimaWatchdog]] — auto-recovery every 5 min via cron.)
2. **Port randomization** — Without `ssh.localPort` in lima.yaml, Lima picks a random ephemeral port on each restart, breaking any hardcoded probe. Detection: `limactl list` shows different port (e.g. 46447 instead of 40257). Recovery: patch lima.yaml + restart.
3. **Disk fill** — Lima has only 120 GiB disk. Docker container writeable layers accumulate between jobs; the dominant consumer (64+ GiB after extended use) can only be reclaimed via `docker compose down` → `docker system prune -af` → `docker compose up -d`. (See [[SelfHostedRunners]] disk management.)

### References

- Source: [[LimaVMSSHCommunication]]
- PR #7843 (`fix/runner-watchdog-hardening`): added lima-watchdog.sh for auto-recovery
- PR #7851 (`fix/runner-disk-cleanup-systematic`): daily hard-cleanup, daily image prune, port pin
- Skill: `self-hosted-colima/scripts/lima-watchdog.sh`
